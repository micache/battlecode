#pragma once
#include <cambc.h>
#include <algorithm>
#include <array>
#include <cstdint>
#include <vector>

namespace camp_rotation {

// One combat invocation: basic, cast, reset-follow-up basic. Spawn positions
// are immutable metadata, so recording a target after its death is safe.
struct clear_trace {
    std::array<cambc::vec2, 3> targets{};
    unsigned count = 0;
    bool movement_blocked = false;

    constexpr void note_target(cambc::vec2 spawn) {
        if (count < targets.size()) targets[count++] = spawn;
    }
    constexpr void note_cast(bool exclusive_with_movement) {
        movement_blocked |= exclusive_with_movement;
    }
    constexpr bool permits_followthrough(bool alive, bool can_move) const {
        return count > 0 && !movement_blocked && alive && can_move;
    }
};

static_assert([] {
    clear_trace trace;
    if (trace.permits_followthrough(true, true)) return false;
    trace.note_target({3, 4}); // Basic-only finish can retain its melee move.
    if (!trace.permits_followthrough(true, true)
        || trace.permits_followthrough(false, true)
        || trace.permits_followthrough(true, false)) return false;
    trace.note_cast(false); // A compatible reset preserves the opportunity.
    if (!trace.permits_followthrough(true, true)) return false;
    trace.note_cast(true); // A ranged spell forbids walking even if can_move is set.
    trace.note_cast(false); // Later compatible actions cannot erase that exclusion.
    for (int i = 0; i < 8; ++i) trace.note_target({i, i});
    return !trace.permits_followthrough(true, true) && trace.count == 3
        && trace.targets[0].x == 3 && trace.targets[0].y == 4;
}());

// Private to one champion instance. This is an expiring observation, not shared
// vision or a claim that a hidden group has respawned when the deadline passes.
struct respawn_observation {
    bool respawning = false;
    std::uint32_t observed_round = 0;
    std::uint32_t earliest_round = 0;

    constexpr void record(std::uint32_t now, int remaining) {
        respawning = true;
        observed_round = now;
        earliest_round = now + static_cast<std::uint32_t>(std::max(0, remaining));
    }
    constexpr void clear() { respawning = false; }
    constexpr bool excludes(std::uint32_t now) const {
        // A zero timer means occupancy blocks respawning NOW. Do not extrapolate
        // that occupancy into the next round, even if the group becomes hidden.
        return respawning && (now == observed_round || now < earliest_round);
    }
};

// Stable temporal contracts compiled by the trusted wrapper, without engine calls.
static_assert([] {
    respawn_observation observation;
    if (observation.excludes(10)) return false; // unknown groups remain eligible
    observation.record(10, 3);
    if (!observation.excludes(10) || !observation.excludes(12)
        || observation.excludes(13)) return false; // exact expiry
    observation.clear();
    if (observation.excludes(11)) return false; // fresh alive/reward overrides
    observation.record(20, 0);
    if (!observation.excludes(20) || observation.excludes(21)) return false;
    observation.record(30, 5);
    observation.record(32, 1); // latest observation replaces the previous deadline
    return observation.excludes(32) && !observation.excludes(33);
}());

constexpr std::uint64_t observation_fuel_reserve = 45000;
constexpr unsigned observation_limit = 16;

struct tracked_group {
    cambc::map::camp_group group;
    cambc::bitboard spawns;
    respawn_observation cooldown;
};

class rotation {
    std::vector<tracked_group> groups;
    std::size_t cursor = 0;

    void initialise() {
        if (!groups.empty()) return;
        // Cache only immutable identities/geometry; live state is never cached
        // by the SDK map object itself. No per-turn map-layout reconstruction.
        for (const auto& group : cambc::map::camp_groups())
            groups.push_back({group, group.spawn_tiles(), {}});
    }

public:
    // Only a group touched by this turn's combat can receive a follow-through.
    // This is not a new global reward route or a pre-combat capture priority.
    cambc::bitboard capture_goals(const clear_trace& trace,
                                 const cambc::bitboard& vicinity) {
        cambc::bitboard result;
        result.clear();
        if (trace.movement_blocked || !trace.count
            || cambc::fuel_remaining() < observation_fuel_reserve) return result;
        initialise();
        const auto visible = cambc::vision::visible_tiles();
        for (const auto& entry : groups) {
            if (cambc::fuel_remaining() < observation_fuel_reserve) break;
            bool touched = false;
            for (unsigned i = 0; i < trace.count; ++i)
                touched |= entry.spawns.is_set(trace.targets[i]);
            if (!touched) continue;
            const auto candidates = entry.spawns & visible & vicinity;
            if (candidates.is_empty()) continue;
            // Current personal spawn vision precedes every live group query.
            if (std::holds_alternative<cambc::map::camp_group_reward_available>(entry.group.state()))
                result |= candidates;
        }
        return result;
    }

    void observe() {
        if (cambc::fuel_remaining() < observation_fuel_reserve) return;
        initialise();
        const auto visible = cambc::vision::visible_tiles();
        const auto now = cambc::round_number();
        unsigned queried = 0;
        // Rotate the scan start so the cap cannot permanently starve later IDs.
        for (std::size_t scanned = 0; scanned < groups.size(); ++scanned) {
            if (queried >= observation_limit
                || cambc::fuel_remaining() < observation_fuel_reserve) break;
            auto& entry = groups[cursor];
            cursor = (cursor + 1) % groups.size();
            if ((entry.spawns & visible).is_empty()) continue;
            ++queried;
            const auto state = entry.group.state();
            if (const auto* respawn = std::get_if<cambc::map::camp_group_respawning>(&state))
                entry.cooldown.record(now, respawn->timer);
            else
                entry.cooldown.clear();
        }
    }

    cambc::bitboard goals() {
        observe();
        cambc::bitboard result;
        result.clear();
        const auto now = cambc::round_number();
        for (const auto& entry : groups)
            if (!entry.cooldown.excludes(now)) result |= entry.spawns;
        return result;
    }
};

// Each WASM champion has its own process/private persistent state. No team bytes.
inline rotation& memory() {
    static rotation instance;
    return instance;
}

} // namespace camp_rotation
