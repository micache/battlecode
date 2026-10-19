#pragma once
#include <cambc.h>
#include <algorithm>
#include <cstdint>
#include <vector>

namespace camp_rotation {

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
