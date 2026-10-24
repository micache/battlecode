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
constexpr int tribute_ticks(int gems) { return gems > 0 ? (gems + 9) / 10 : 1; }
constexpr float value(int gems, int gold, int round) {
    return 5.0f * gems + (round < 900 ? 1.0f : 0.35f) * gold;
}
constexpr float route_score(float reward, float travel, float clear, int wait) {
    return reward / (8.0f + travel + clear + wait);
}
static_assert(plan_header + 2 * max_groups <= 1024);
static_assert(tribute_ticks(1) == 1 && tribute_ticks(10) == 1 && tribute_ticks(11) == 2);
static_assert(value(7, 0, 1) > 0 && value(0, 20, 1) > value(0, 20, 1200));
static_assert(route_score(35, 2, 2, 0) > route_score(35, 20, 2, 0));
}
