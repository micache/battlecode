#pragma once
#include <cambc.h>
#include <array>
#include <cstdint>

namespace economy_route {

constexpr std::uint64_t bootstrap_capital = 300;
constexpr unsigned gem_detour_steps = 12;
constexpr std::uint64_t planning_reserve = 60000;
constexpr std::uint64_t second_field_reserve = 40000;
constexpr std::uint64_t movement_reserve = 28000;

constexpr bool prefer_gems(std::uint64_t capital, unsigned ordinary_distance,
                           unsigned gem_distance, bool on_group) {
    return capital >= bootstrap_capital && !on_group
        && ordinary_distance != cambc::distance_field::unreachable
        && gem_distance != cambc::distance_field::unreachable
        && gem_distance <= ordinary_distance + gem_detour_steps;
}

// Policy boundaries, fallback for unreachable gems, and preservation of a
// current group's occupancy (including an unfinished gold-only capture).
static_assert(!prefer_gems(299, 1, 1, false));
static_assert(prefer_gems(300, 1, 13, false));
static_assert(!prefer_gems(300, 1, 14, false));
static_assert(prefer_gems(10000, 0, 12, false));
static_assert(!prefer_gems(10000, 0, 12, true));
static_assert(!prefer_gems(300, 1, cambc::distance_field::unreachable, false));
static_assert(!prefer_gems(300, cambc::distance_field::unreachable, 1, false));

inline std::uint64_t capital() {
    const auto& me = cambc::self();
    auto result = std::uint64_t(me.gold_count());
    if (result >= bootstrap_capital) return result;
    // Count cash plus actual purchase value, not bonus stat points. These are
    // the only equipment families this bot buys. Combined emblems retain cost.
    using I = cambc::item_type;
    const auto counts = me.item_count();
    const std::array items{I::power_shard_of_strength, I::power_emblem_of_strength,
        I::power_shard_of_focus, I::power_emblem_of_focus,
        I::power_shard_of_health, I::power_emblem_of_health};
    for (const auto item : items) {
        if (counts[item]) result += std::uint64_t(counts[item]) * item.cost();
        if (result >= bootstrap_capital) break;
    }
    return result;
}

} // namespace economy_route
