#pragma once
#include <cambc.h>
#include <cstdint>

namespace altar_control {

constexpr std::uint64_t fuel_reserve = 18000;
// The pinned SDK documents two-tile placement; no placement-range setting exists.
constexpr int lock_placement_range = 2;

inline bool channeling() {
    const auto& me = cambc::self();
    return me.is_recalling() || me.is_submitting_gems() || me.is_teleporting();
}

// can_buy checks location, gold and the one-lock inventory cap, including death.
inline void buy_lock() {
    auto& me = cambc::self();
    if (me.can_buy(cambc::consumable_type::altar_lock))
        me.buy(cambc::consumable_type::altar_lock);
}

// No detour: lock a visible, unoccupied altar encountered on our existing route.
// This uses neither walking, basic nor cast allowance. Never interrupt our channel.
inline void place_lock() {
    auto& me = cambc::self();
    if (cambc::fuel_remaining() < fuel_reserve || !me.is_alive() || channeling()
        || me.restrictions().contains(cambc::buff_restrictions::consumable))
        return;
    const auto& lock = me.consumables()[cambc::consumable_type::altar_lock];
    if (!lock.count()) return;
    cambc::bitboard nearby;
    nearby.clear();
    nearby.draw_chebyshev(me.position(), lock_placement_range);
    // A missing hidden lock is not evidence that a hidden altar is available.
    nearby &= cambc::map::altars() & cambc::vision::visible_tiles();
    nearby &= ~cambc::vision::altar_lock_tiles();
    for (const auto altar : nearby.positions()) {
        // At most 25 local tiles and one use attempt; reobserve next turn on False.
        lock.use(altar);
        return;
    }
}

// Prefer immediate tribute, including through a friendly lock. If every adjacent
// altar has a hostile lock, spend one legal basic on a fresh enemy-lock snapshot.
inline bool bank_or_clear_lock() {
    auto& me = cambc::self();
    if (!me.is_alive() || channeling() || !me.gem_count()
        || cambc::fuel_remaining() < fuel_reserve)
        return false;
    cambc::bitboard nearby;
    nearby.clear();
    nearby.draw_chebyshev(me.position(), cambc::constants::submit_gems_range);
    nearby &= cambc::map::altars() & cambc::vision::visible_tiles();
    const auto hostile = cambc::vision::altar_lock_tiles(cambc::team::enemy);
    for (const auto altar : (nearby & ~hostile).positions()) {
        me.submit_gems(altar); // void: a completed action, not a Boolean query
        return true;
    }
    if ((nearby & hostile).is_empty() || !me.can_attack()
        || me.restrictions().contains(cambc::buff_restrictions::attack))
        return false;
    const auto range = me.attack_tiles();
    for (const auto& lock : cambc::vision::altar_locks(cambc::team::enemy)) {
        if (cambc::fuel_remaining() < fuel_reserve) break;
        if (nearby.is_set(lock.position()) && range.is_set(lock.position())) {
            me.attack(lock);
            return true;
        }
    }
    return false;
}

} // namespace altar_control
