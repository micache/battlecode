#pragma once
#include <cambc.h>
#include "camp_rotation.h"
#include <algorithm>
#include <cstdint>
#include <vector>

namespace camp_pull {

constexpr unsigned group_limit = 6;
constexpr unsigned camp_limit = 32;
constexpr std::uint64_t fuel_reserve = 55000;
constexpr int helper_range = 4;
constexpr float health_budget = 0.8f;
constexpr float exposure_fraction = 0.6f;

// Workload estimate, not an engine damage prediction. Nearby basics are the
// sustainable floor; no imagined future spells, purchases or hidden allies.
constexpr bool sustainable(float work, float incoming, float dps, float health) {
    if (incoming <= 0 || work <= 0) return true;
    if (dps <= 0 || health <= 0) return false;
    const auto turns = static_cast<unsigned>(work / dps)
        + (work > dps * static_cast<unsigned>(work / dps) ? 1u : 0u);
    return exposure_fraction * incoming * turns <= health_budget * health;
}

static_assert(sustainable(120, 0, 1, 1)); // clusters never need protection
static_assert(sustainable(1350, 20, 90, 1000)); // solo wolf
static_assert(!sustainable(2400, 60, 90, 1000)); // weak solo elk pull
static_assert(sustainable(2400, 60, 180, 2000)); // nearby ally changes feasibility
static_assert(!sustainable(5000, 120, 90, 1000)); // early solo golem
static_assert(sustainable(5000, 120, 600, 2000)); // upgrades reopen the group
static_assert(!sustainable(100, 10, 0, 100));
static_assert(sustainable(100, 10, 10, 75)); // exactly on the 80% budget
static_assert(!sustainable(101, 10, 10, 75)); // round clearing work upward

// A per-call mask, never a cross-turn belief about hidden camps or helpers.
inline cambc::bitboard assess(const cambc::bitboard& goals) {
    cambc::bitboard excluded;
    excluded.clear();
    if (goals.is_empty() || cambc::fuel_remaining() < fuel_reserve) return excluded;
    const auto visible = cambc::vision::visible_tiles();
    const auto awake = cambc::vision::awake_camp_tiles();
    const auto camps = cambc::vision::camps();
    if (camps.size() > camp_limit) return excluded;
    auto& me = cambc::self();
    const auto my_position = me.position();
    const float my_health = me.health(), my_dps = me.strength();
    struct helper { cambc::vec2 position; float health, dps; };
    std::vector<helper> helpers;
    unsigned examined = 0;
    for (const auto& ally : cambc::vision::champions(cambc::team::ally)) {
        if (++examined > 6 || cambc::fuel_remaining() < fuel_reserve) break;
        if (ally == me || !ally.is_visible() || !ally.is_alive()) continue;
        if (ally.is_recalling() || ally.is_submitting_gems() || ally.is_teleporting()
            || ally.health() < 0.35f * ally.max_health()) continue;
        helpers.push_back({ally.position(), ally.health(), ally.strength()});
    }
    unsigned priced = 0;
    for (const auto& entry : camp_rotation::memory().layout()) {
        if (priced >= group_limit || cambc::fuel_remaining() < fuel_reserve) break;
        if (entry.group.camps().size() > camp_limit) continue;
        const auto& spawns = entry.spawns;
        // Only complete current vision permits pricing a pull. Partly hidden
        // and already-awake groups retain the original fighting policy.
        if ((spawns & visible) != spawns || !(spawns & awake).is_empty()) continue;
        // Reward/cooldown groups have no live monsters and need no pull gate.
        if ((spawns & cambc::vision::camp_tiles()).is_empty()) continue;
        ++priced;
        const auto anchor = entry.group.camps().front().spawn_position();
        float work = 0, incoming = 0;
        bool complete = true;
        for (const auto& member : camps) {
            if (cambc::fuel_remaining() < fuel_reserve) { complete = false; break; }
            if (!spawns.is_set(member.spawn_position()) || !member.is_visible()) continue;
            work += member.health();
            incoming += member.strength();
        }
        if (!complete) break; // never price a partial sum as a safe whole group
        float health = my_health, dps = my_dps;
        // Helpers must be close to this pull and the acting champion. Merely
        // seeing an ally elsewhere does not make its health/damage available.
        for (const auto& ally : helpers)
            if (ally.position.chebyshev_distance(anchor) <= helper_range
                && ally.position.chebyshev_distance(my_position) <= helper_range) {
                health += ally.health;
                dps += ally.dps;
            }
        if (!sustainable(work, incoming, dps, health)) excluded |= spawns;
    }
    // Never remove the last eligible objective: maps with only hard camps must
    // retain the base policy rather than waiting indefinitely for safe work.
    if ((goals & ~excluded).is_empty()) excluded.clear();
    return excluded;
}

inline bool permits(const cambc::camp& target, const cambc::bitboard* excluded, float radius = 0) {
    if (!excluded || excluded->is_empty()) return true;
    if (excluded->is_set(target.spawn_position())) return false;
    if (radius <= 0) return true;
    cambc::bitboard area;
    area.clear();
    area.draw_chebyshev(target.position(), radius);
    return (area & *excluded).is_empty();
}

} // namespace camp_pull
