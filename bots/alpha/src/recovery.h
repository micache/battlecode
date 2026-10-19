#pragma once
#include <cambc.h>
#include <array>
#include <algorithm>
#include <cstdint>

namespace recovery {

constexpr float retreat_fraction = 0.35f;
constexpr float scan_health_fraction = 0.70f;
constexpr float reserve_volleys = 2.0f;
constexpr std::uint64_t scan_reserve = 45000;
constexpr std::uint64_t navigation_reserve = 28000;
constexpr std::uint64_t action_reserve = 18000;
constexpr unsigned threat_limit = 32;

struct threat {
    cambc::vec2 position;
    int range;
    float damage;
};

struct exposure {
    float damage = 0;
    float depth = 0;
};

// Raw visible basic damage is a conservative estimate, not a combat simulator:
// it ignores mitigation, target selection, future spells and hidden attackers.
struct observation {
    std::array<threat, threat_limit> threats{};
    unsigned count = 0;
    bool complete = true;

    constexpr exposure at(cambc::vec2 tile) const {
        exposure result;
        for (unsigned i = 0; i < count; ++i) {
            const auto& t = threats[i];
            const auto d = tile.chebyshev_distance(t.position);
            if (d <= t.range) {
                result.damage += t.damage;
                // Resolve flat damage plateaus by walking towards their edge.
                result.depth += t.damage * (t.range + 1 - d);
            }
        }
        return result;
    }
};

constexpr bool needs_recovery(float health, float maximum, float volley) {
    return health < maximum * retreat_fraction
        || (health < maximum * scan_health_fraction && volley > 0
            && health <= reserve_volleys * volley);
}

constexpr bool safer(exposure candidate, unsigned candidate_distance,
                     exposure current, unsigned current_distance) {
    if (candidate.damage != current.damage) return candidate.damage < current.damage;
    if (candidate.depth != current.depth) return candidate.depth < current.depth;
    return candidate_distance < current_distance;
}

// Stable contracts: additive volleys, staying outside range, escaping a flat
// plateau even when spawn is the opposite way, and unchanged healthy decisions.
static_assert([] {
    observation seen;
    seen.threats[seen.count++] = {{0, 0}, 3, 60};
    seen.threats[seen.count++] = {{1, 0}, 3, 60};
    if (seen.at({2, 0}).damage != 120 || seen.at({5, 0}).damage != 0) return false;
    if (!safer(seen.at({3, 0}), 10, seen.at({2, 0}), 9)) return false;
    if (!safer(seen.at({5, 0}), 20, seen.at({3, 0}), 1)) return false;
    if (safer(seen.at({3, 0}), 1, seen.at({5, 0}), 20)) return false;
    if (!safer({0, 0}, 4, {0, 0}, 5) || safer({0, 0}, 5, {0, 0}, 4)) return false;
    return needs_recovery(230, 700, 120) && !needs_recovery(500, 700, 120)
        && needs_recovery(300, 700, 180) && !needs_recovery(700, 700, 500)
        && needs_recovery(200, 700, 0) && !needs_recovery(400, 700, 0);
}());

inline observation observe() {
    observation result;
    if (cambc::fuel_remaining() < scan_reserve) {
        result.complete = false;
        return result;
    }
    // Enemy champions can move before attacking; camps cannot chase. Read live
    // properties only after visibility. No handles survive this observation.
    for (const auto& enemy : cambc::vision::champions(cambc::team::enemy)) {
        if (result.count == threat_limit || cambc::fuel_remaining() < scan_reserve) {
            result.complete = false;
            return result;
        }
        if (!enemy.is_visible() || !enemy.is_alive()) continue;
        result.threats[result.count++] = {enemy.position(),
            enemy.attack_range() + enemy.base_stats().base_move_speed, enemy.strength()};
    }
    for (const auto& camp : cambc::vision::camps()) {
        if (result.count == threat_limit || cambc::fuel_remaining() < scan_reserve) {
            result.complete = false;
            return result;
        }
        if (!camp.is_visible() || camp.health() <= 0 || !camp.is_awake()) continue;
        const auto damage = camp.strength();
        if (damage > 0)
            result.threats[result.count++] = {camp.position(), camp.attack_range(), damage};
    }
    return result;
}

inline void shield(const observation& seen) {
    auto& me = cambc::self();
    if (seen.at(me.position()).damage <= 0 || !me.can_cast()
        || me.restrictions().contains(cambc::buff_restrictions::cast)
        || me.buffs().has_shield()) return;
    for (const auto& ability : me.abilities()) {
        if (cambc::fuel_remaining() < action_reserve) return;
        if (!ability.is_shield() || !ability.is_ready() || !ability.can_target_self()) continue;
        // Preserve walking for the escape, even if a future kit adds a shield
        // which excludes it. Existing Varg shield is walking-compatible.
        if (ability.get<cambc::ability_shield>().exclusive_with_movement) continue;
        if (ability.use()) return;
    }
}

// Caller supplies a fresh legal occupancy mask and the native spawn distance
// field. Consider at most the nine ordinary one-step choices, including staying.
inline cambc::vec2 escape(const observation& seen, const cambc::bitboard& blocked,
                         const cambc::distance_field& home) {
    const auto& me = cambc::self();
    const auto& spawn = cambc::map::spawn_region(cambc::team::ally);
    auto best = me.position();
    auto risk = seen.at(best);
    auto distance = home.get(best);
    for (const auto tile : blocked.reachable_tiles(best, 1).positions()) {
        // Reaching spawn heals at this turn end, before the next camp phase.
        if (spawn.is_set(tile)) return tile;
        const auto next = seen.at(tile);
        const auto next_distance = home.get(tile);
        if (safer(next, next_distance, risk, distance)) {
            best = tile;
            risk = next;
            distance = next_distance;
        }
    }
    return best;
}

} // namespace recovery
