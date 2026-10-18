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

    constexpr bool excludes_at_arrival(std::uint32_t now, int distance, int speed) const {
        if (!excludes(now)) return false;
        // A zero countdown is an occupancy observation, not a respawn promise.
        if (earliest_round <= observed_round || speed <= 0) return true;
        const int moves = (std::max(0, distance) + speed - 1) / speed;
        // The first move happens THIS round, after the respawn phase. Reaching
        // a spawn in one move is therefore not a one-round wait for respawning.
        const auto arrival = now + static_cast<std::uint32_t>(std::max(0, moves - 1));
        return arrival < earliest_round;
    }
};

// A cached rectangle gives a cheap LOWER bound on distance to every spawn.
// Holes in a group's shape, walls and visible occupants only lengthen travel.
// Underestimating distance conservatively excludes some useful return trips.
struct spawn_bounds {
    bool valid = false;
    int min_x = 0, max_x = 0, min_y = 0, max_y = 0;

    constexpr void include(int x, int y) {
        if (!valid) {
            min_x = max_x = x;
            min_y = max_y = y;
            valid = true;
        } else {
            min_x = std::min(min_x, x); max_x = std::max(max_x, x);
            min_y = std::min(min_y, y); max_y = std::max(max_y, y);
        }
    }
    constexpr int distance_lower_bound(int x, int y) const {
        if (!valid) return 0;
        return std::max({0, min_x - x, x - max_x, min_y - y, y - max_y});
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

// Timing regressions: do not enter a cooling spawn before its respawn phase;
// include exact-deadline arrivals, keep zero-timer semantics and handle speed.
static_assert([] {
    respawn_observation observation;
    observation.record(10, 3);
    if (!observation.excludes_at_arrival(10, 3, 1)
        || observation.excludes_at_arrival(10, 4, 1)) return false;
    if (!observation.excludes_at_arrival(10, 6, 2)
        || observation.excludes_at_arrival(10, 7, 2)) return false;
    if (!observation.excludes_at_arrival(10, 0, 1)
        || !observation.excludes_at_arrival(10, 100, 0)) return false;
    observation.record(20, 0);
    if (!observation.excludes_at_arrival(20, 100, 1)
        || observation.excludes_at_arrival(21, 0, 1)) return false;
    observation.clear();
    return !observation.excludes_at_arrival(20, 0, 1);
}());

static_assert([] {
    spawn_bounds bounds;
    if (bounds.distance_lower_bound(50, 50) != 0) return false;
    bounds.include(10, 10); bounds.include(12, 14);
    if (bounds.distance_lower_bound(11, 12) != 0
        || bounds.distance_lower_bound(15, 16) != 3
        || bounds.distance_lower_bound(8, 7) != 3) return false;
    // For every tested admitted trip, even an unobstructed fastest walk cannot
    // enter any member's spawn before the remembered positive deadline.
    for (int x = 0; x < 20; ++x) for (int y = 0; y < 20; ++y)
        for (int timer = 1; timer <= 5; ++timer) {
            respawn_observation observation;
            observation.record(100, timer);
            if (observation.excludes_at_arrival(100, bounds.distance_lower_bound(x, y), 1))
                continue;
            for (const auto spawn : {cambc::vec2{10, 10}, cambc::vec2{12, 14}})
                if (std::max(0, static_cast<int>(spawn.chebyshev_distance({x, y})) - 1) < timer)
                    return false;
        }
    return true;
}());

constexpr std::uint64_t observation_fuel_reserve = 45000;
constexpr unsigned observation_limit = 16;

struct tracked_group {
    cambc::map::camp_group group;
    cambc::bitboard spawns;
    respawn_observation cooldown;
    spawn_bounds bounds;
};

class rotation {
    std::vector<tracked_group> groups;
    std::size_t cursor = 0;

    void initialise() {
        if (!groups.empty()) return;
        // Cache only immutable identities/geometry; live state is never cached
        // by the SDK map object itself. No per-turn map-layout reconstruction.
        for (const auto& group : cambc::map::camp_groups()) {
            spawn_bounds bounds;
            for (const auto& member : group.camps()) {
                const auto spawn = member.spawn_position(); // immutable SDK metadata
                bounds.include(spawn.x, spawn.y);
            }
            groups.push_back({group, group.spawn_tiles(), {}, bounds});
        }
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
        const auto position = cambc::self().position();
        const auto speed = cambc::self().base_stats().base_move_speed;
        for (const auto& entry : groups)
            if (!entry.cooldown.excludes(now)
                || !entry.cooldown.excludes_at_arrival(now,
                    entry.bounds.distance_lower_bound(position.x, position.y), speed))
                result |= entry.spawns;
        return result;
    }
};

// Each WASM champion has its own process/private persistent state. No team bytes.
inline rotation& memory() {
    static rotation instance;
    return instance;
}

} // namespace camp_rotation
