#pragma once
#include <cstddef>
#include <cstdint>

namespace policy {
// Draft protocol v1: magic GA, version, u16 count, then (u8 x,u8 y).
// Static anchors only. No live observations, per-body records or live writes.
inline constexpr std::size_t plan_header = 5, max_groups = 509;
inline constexpr int shortlist = 8, bank_bag = 24, near_bank = 6;
inline constexpr float retreat_fraction = 0.40f, leave_spawn_fraction = 0.98f;
inline constexpr std::uint64_t planning_floor = 45000, action_floor = 18000;
inline constexpr std::uint64_t distance_floor = 65000;
inline constexpr int travel_refresh_steps = 4, travel_refresh_rounds = 12;
inline constexpr int unreachable = 1000000;
// Field shoppers reinvest without a gold-only recall; health recovery remains
// independent of this predicate, including after non-healing field Health buys.
constexpr bool needs_shop_trip(bool field_shopper, unsigned gold, unsigned threshold) {
    return !field_shopper && gold >= threshold;
}
static_assert(!needs_shop_trip(true, 1000, 150));
static_assert(!needs_shop_trip(false, 149, 150));
static_assert(needs_shop_trip(false, 150, 150));
static_assert(needs_shop_trip(false, 300, 300));
// A cached exact distance is a lower bound after moving at most displacement.
// Unreachable stays unreachable within the same walk-connected component.
constexpr int route_distance(int cached, int displacement, int geometric) {
    return cached < 0 ? geometric : cached == unreachable ? unreachable
        : (cached - displacement > geometric ? cached - displacement : geometric);
}
constexpr int tribute_ticks(int gems) { return gems > 0 ? (gems + 9) / 10 : 1; }
constexpr float value(int gems, int gold, int round) {
    return 5.0f * gems + (round < 900 ? 1.0f : 0.35f) * gold;
}
constexpr float route_score(float reward, float travel, float clear, int wait) {
    return reward / (8.0f + travel + clear + wait);
}
static_assert(route_distance(unreachable, 4, 1) == unreachable);
static_assert(route_distance(30, 4, 1) == 26);
static_assert(route_distance(-1, 0, 9) == 9);
static_assert(route_distance(2, 4, 1) == 1);
static_assert(plan_header + 2 * max_groups <= 1024);
static_assert(tribute_ticks(1) == 1 && tribute_ticks(10) == 1 && tribute_ticks(11) == 2);
static_assert(value(7, 0, 1) > 0 && value(0, 20, 1) > value(0, 20, 1200));
static_assert(route_score(35, 2, 2, 0) > route_score(35, 20, 2, 0));
}
