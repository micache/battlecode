#pragma once
#include <cambc.h>
#include <algorithm>
#include <array>

namespace farming_equipment {

// Preserve each champion's chosen stat. Complete one non-stacking defensive
// passive, then spend all subsequent equipment gold on the original Power line.
inline const std::array jungle_shards{
    cambc::item_type::jungle_shard_of_strength,
    cambc::item_type::jungle_shard_of_focus,
    cambc::item_type::jungle_shard_of_health};
inline const std::array jungle_emblems{
    cambc::item_type::jungle_emblem_of_strength,
    cambc::item_type::jungle_emblem_of_focus,
    cambc::item_type::jungle_emblem_of_health};

inline bool has_jungle(const cambc::enum_map<cambc::item_type>& inventory) {
    for (const auto emblem : jungle_emblems)
        if (inventory[emblem]) return true;
    return false;
}

constexpr unsigned purchase_count(unsigned shards, unsigned combine,
                                  unsigned gold, unsigned cost) {
    if (!cost || shards >= combine) return 0;
    return std::min(combine - shards, gold / cost);
}

// Pinned handbook: only the completed Jungle emblem reduces camp damage by 30%.
// This does not model shields, other mitigation or the camp's choice of victim.
constexpr float camp_volley(float strength, bool jungle) {
    return strength * (jungle ? 0.70f : 1.0f);
}

static_assert(purchase_count(0, 5, 29, 30) == 0);
static_assert(purchase_count(0, 5, 60, 30) == 2);
static_assert(purchase_count(2, 5, 300, 30) == 3); // finish, never buy a duplicate
static_assert(purchase_count(4, 5, 30, 30) == 1);
static_assert(purchase_count(5, 5, 300, 30) == 0);
static_assert(purchase_count(6, 5, 300, 30) == 0); // no unsigned underflow
static_assert(camp_volley(100, false) == 100 && camp_volley(100, true) == 70);

} // namespace farming_equipment
