#pragma once
#include <cstdint>

namespace camp_navigation {

// Same operation for native bitboards and compact synthetic cluster fixtures.
// Only current, positive live-member observations justify pruning spawn goals.
template<class Mask>
constexpr Mask exploration_spawns(const Mask& spawns, const Mask& visible,
                                  bool pursue_live_member) {
    return pursue_live_member ? spawns & ~visible : spawns;
}

// A two-member group: left spawn has been cleared, right member is still alive.
// Walking at the left spawn must not remain an already-satisfied route goal.
static_assert(exploration_spawns<std::uint32_t>(0b0011, 0b0011, true) == 0);
// A hidden member's original spawn remains a possible exploration destination.
static_assert(exploration_spawns<std::uint32_t>(0b0011, 0b0001, true) == 0b0010);
// Rewards, stale/unknown groups and groups without a visible member retain tiles.
static_assert(exploration_spawns<std::uint32_t>(0b0011, 0b0011, false) == 0b0011);
// Observations of an unrelated group cannot remove this group's hidden tiles.
static_assert(exploration_spawns<std::uint32_t>(0b0011, 0b1100, true) == 0b0011);

} // namespace camp_navigation
