#pragma once
#include <cambc.h>
#include <algorithm>
#include <cstdint>

namespace route_teleport {

constexpr int crystal_range = 3; // Pinned handbook/SDK consumable contract.
constexpr unsigned minimum_net_saving = 3;
constexpr std::uint64_t planning_reserve = 45000;
constexpr std::uint64_t action_reserve = 28000;
constexpr unsigned camp_limit = 32;

// Fields count ordinary tile steps. Reject disconnected origins rather than
// spending our only crystal to enter a region with no known walking way back.
constexpr bool useful(unsigned from, unsigned to, unsigned speed, unsigned channel) {
    if (!speed || from == cambc::distance_field::unreachable
        || to == cambc::distance_field::unreachable || to >= from) return false;
    const auto before = (from + speed - 1) / speed;
    const auto after = (to + speed - 1) / speed;
    return before >= after + channel + minimum_net_saving;
}

static_assert(useful(12, 6, 1, 3));
static_assert(!useful(11, 6, 1, 3));
static_assert(!useful(3, 0, 1, 3)); // Ordinary open-ground jumps lose time.
static_assert(!useful(12, 6, 2, 3));
static_assert(useful(24, 12, 2, 3));
static_assert(!useful(12, 6, 1, 4)); // Honour the actual SDK channel duration.
static_assert(!useful(cambc::distance_field::unreachable, 0, 1, 3));
static_assert(!useful(12, cambc::distance_field::unreachable, 1, 3));
static_assert(!useful(12, 6, 0, 3));

inline void buy_crystal() {
    auto& me = cambc::self();
    if (me.can_buy(cambc::consumable_type::tp_crystal))
        me.buy(cambc::consumable_type::tp_crystal);
}

inline bool ready() {
    auto& me = cambc::self();
    if (cambc::fuel_remaining() < planning_reserve || !me.is_alive()
        || !me.can_move() || me.is_recalling() || me.is_submitting_gems()
        || me.is_teleporting()) return false;
    const auto restrictions = me.restrictions();
    return !restrictions.contains(cambc::buff_restrictions::move)
        && !restrictions.contains(cambc::buff_restrictions::consumable)
        && me.consumables()[cambc::consumable_type::tp_crystal].count() > 0;
}

// Returns true for ANY use attempt. A False can reveal an obstruction: the
// caller must stop, not walk or fight with pre-attempt fields/observations.
inline bool try_shortcut(const cambc::distance_field& route,
                         const cambc::bitboard& blocked) {
    if (!ready()) return false;
    auto& me = cambc::self();
    const auto origin = me.position();
    const auto from = route.get(origin);
    const auto speed = static_cast<unsigned>(me.base_stats().base_move_speed);
    const auto channel = static_cast<unsigned>(std::max(1, cambc::constants::tp_crystal_time));
    if (!useful(from, 0, speed, channel)) return false;

    // Require a genuine terrain bypass, not a transient ally-induced detour.
    auto terrain = cambc::map::walls() | cambc::map::holes() | cambc::map::altars()
        | cambc::map::spawn_region(cambc::team::enemy);
    const auto ordinary_nearby = terrain.reachable_tiles(origin, crystal_range);
    cambc::bitboard candidates;
    candidates.draw_chebyshev(origin, crystal_range);
    candidates &= cambc::vision::visible_tiles() & ~blocked & ~ordinary_nearby;
    if (candidates.is_empty()) return false;

    // Price the full channel, not just this turn. Sleeping damaging camps are
    // included because an ally might wake them while we cannot move. Hidden
    // units and future spells remain uncertainty; never read hidden live state.
    cambc::bitboard danger;
    unsigned examined = 0;
    for (const auto& camp : cambc::vision::camps()) {
        if (++examined > camp_limit || cambc::fuel_remaining() < action_reserve)
            return false; // An incomplete scan cannot certify a quiet channel.
        if (!camp.is_visible() || camp.health() <= 0 || camp.strength() <= 0) continue;
        danger.draw_chebyshev(camp.position(), camp.attack_range());
    }
    unsigned enemies = 0;
    for (const auto& enemy : cambc::vision::champions(cambc::team::enemy)) {
        if (++enemies > 6 || cambc::fuel_remaining() < action_reserve) return false;
        if (!enemy.is_visible() || !enemy.is_alive()) continue;
        // Four covers the published unit/ground spell range. Account for up to
        // one ordinary enemy move per channel tick; dashes/hidden CC unmodeled.
        const int reach = std::max(4, enemy.attack_range())
            + static_cast<int>(channel) * enemy.base_stats().base_move_speed;
        danger.draw_chebyshev(enemy.position(), reach);
    }
    if (danger.is_set(origin)) return false;
    candidates &= ~danger;

    auto destination = origin;
    auto best = from;
    for (const auto tile : candidates.positions()) {
        if (cambc::fuel_remaining() < action_reserve) return false;
        const auto remaining = route.get(tile);
        if (useful(from, remaining, speed, channel) && remaining < best) {
            destination = tile;
            best = remaining;
        }
    }
    if (destination == origin || cambc::fuel_remaining() < action_reserve) return false;
    me.consumables()[cambc::consumable_type::tp_crystal].use(destination);
    return true; // One attempt. Existing main/channel guards preserve the yield.
}

} // namespace route_teleport
