#pragma once
#include <cambc.h>
#include "camp_navigation.h"
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
    bool observed_alive = false;
    std::uint32_t state_round = 0;
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
            entry.observed_alive = std::holds_alternative<cambc::map::camp_group_alive>(state);
            entry.state_round = now;
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

        // No extra planning when observation/combat already consumed the budget.
        // Retain the original exploration/capture goals on every bounded fallback.
        if (cambc::fuel_remaining() < observation_fuel_reserve) return result;
        const auto occupied = cambc::vision::camp_tiles();
        const auto targets = occupied.positions();
        if (targets.empty() || targets.size() > observation_limit) return result;

        cambc::bitboard live_spawns;
        cambc::bitboard approaches;
        const auto range = cambc::self().attack_range();
        for (const auto position : targets) {
            if (cambc::fuel_remaining() < observation_fuel_reserve) return result;
            // This mask contains current personal-vision camps, not cached units.
            // Only immutable spawn metadata is read; position comes from the mask.
            const auto camp = cambc::vision::camp_at(position);
            if (!result.is_set(camp.spawn_position())) continue;
            live_spawns.set(camp.spawn_position());
            approaches.draw_chebyshev(position, range);
        }
        if (live_spawns.is_empty()) return result;

        const auto visible = cambc::vision::visible_tiles();
        cambc::bitboard revised;
        for (const auto& entry : groups) {
            if (entry.cooldown.excludes(now)) continue;
            // Reward tiles remain capture destinations. Stale/unknown observations
            // and groups without a positively observed member keep the base goals.
            const bool pursue = entry.observed_alive && entry.state_round == now
                && !(entry.spawns & live_spawns).is_empty();
            revised |= camp_navigation::exploration_spawns(entry.spawns, visible, pursue);
        }
        // A camp/ally/terrain square is never an approach destination. Do not let
        // occupied monsters seed a path through a wall of other occupied camps.
        const auto blocked = cambc::map::walls() | cambc::map::holes()
            | cambc::map::altars() | cambc::map::spawn_region(cambc::team::enemy)
            | cambc::vision::champion_tiles() | occupied | cambc::vision::teleport_tiles();
        auto free_approaches = approaches & ~blocked;
        // Self is a legal goal when already in range (combat tried before routing).
        const auto here = cambc::self().position();
        if (approaches.is_set(here)) free_approaches.set(here);
        // No reachable/free attack approach must not erase the exploration fallback.
        if (free_approaches.is_empty()) return result;
        return revised | free_approaches;
    }
};

// Each WASM champion has its own process/private persistent state. No team bytes.
inline rotation& memory() {
    static rotation instance;
    return instance;
}

} // namespace camp_rotation
