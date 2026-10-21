#pragma once
#include <cambc.h>
#include <algorithm>
#include <cstdint>

namespace skirmish {

constexpr int support_radius = 5;
constexpr int danger_radius = 4;
constexpr float retreat_power_ratio = 0.80f;
constexpr unsigned champion_limit = 16;
constexpr std::uint64_t scan_reserve = 65000;

// A rough simultaneous basic-damage race, not a spell/shield combat simulator.
// Only personally visible, living champions contribute; self is counted once.
struct balance {
    float ours = 0;
    float theirs = 0;
    bool nearby_enemy = false;

    constexpr void ally(int distance, float health, float strength) {
        if (distance <= support_radius)
            ours += health * std::max(1.0f, strength);
    }
    constexpr void enemy(int distance, float health, float strength) {
        if (distance <= support_radius)
            theirs += health * std::max(1.0f, strength);
        nearby_enemy |= distance <= danger_radius;
    }
    constexpr bool outmatched() const {
        return nearby_enemy && ours < retreat_power_ratio * theirs;
    }
};

// The threshold must preserve equal/favourable trades, include local support,
// exclude distant support, and require a nearby enemy before forcing a retreat.
static_assert([] {
    balance b;
    b.ally(0, 1000, 100);
    b.enemy(2, 1000, 100);
    if (b.outmatched()) return false;
    b.enemy(5, 1000, 50);
    if (!b.outmatched()) return false;
    b.ally(6, 1000, 100);
    if (!b.outmatched()) return false;
    b.ally(5, 1000, 50);
    if (b.outmatched()) return false;
    balance distant;
    distant.ally(0, 1000, 100);
    distant.enemy(5, 1000, 200);
    if (distant.outmatched()) return false;
    balance boundary{80, 100, true};
    return !boundary.outmatched() && balance{79, 100, true}.outmatched();
}());

inline bool outmatched() {
    auto& me = cambc::self();
    // Most turns cost one native geometry intersection, with no unit scans.
    cambc::bitboard nearby;
    nearby.clear();
    nearby.draw_chebyshev(me.position(), danger_radius);
    if ((nearby & cambc::vision::champion_tiles(cambc::team::enemy)).is_empty()
        || cambc::fuel_remaining() < scan_reserve)
        return false;

    const auto origin = me.position();
    balance estimate;
    estimate.ally(0, me.health(), me.strength());
    unsigned examined = 0;
    for (const auto& enemy : cambc::vision::champions(cambc::team::enemy)) {
        if (++examined > champion_limit || cambc::fuel_remaining() < scan_reserve)
            return false; // Partial observations never force an early retreat.
        if (!enemy.is_visible() || !enemy.is_alive()) continue;
        const auto distance = origin.chebyshev_distance(enemy.position());
        if (distance <= support_radius)
            estimate.enemy(distance, enemy.health(), enemy.strength());
    }
    if (!estimate.outmatched()) return false; // Allies can only improve the ratio.
    examined = 0;
    for (const auto& ally : cambc::vision::champions(cambc::team::ally)) {
        if (++examined > champion_limit || cambc::fuel_remaining() < scan_reserve)
            return false;
        if (ally == me || !ally.is_visible() || !ally.is_alive()) continue;
        const auto distance = origin.chebyshev_distance(ally.position());
        if (distance <= support_radius)
            estimate.ally(distance, ally.health(), ally.strength());
    }
    return estimate.outmatched();
}

} // namespace skirmish
