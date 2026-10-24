#pragma once
#include <cstddef>
#include <cstdint>

namespace policy {
// Draft protocol v1: magic GA, version, u16 count, then (u8 x,u8 y).
// Static anchors only. No live observations, per-body records or live writes.
inline constexpr std::size_t plan_header = 5, max_groups = 509;
inline constexpr int shortlist = 8, bank_bag = 24, near_bank = 6;
inline constexpr int max_return_wait = 3;
inline constexpr float retreat_fraction = 0.40f, leave_spawn_fraction = 0.98f;
inline constexpr std::uint64_t planning_floor = 45000, action_floor = 18000;
inline constexpr std::uint64_t distance_floor = 65000;
inline constexpr int travel_refresh_steps = 4, travel_refresh_rounds = 12;
inline constexpr int unreachable = 1000000;
// A cached exact distance is a lower bound after moving at most displacement.
// Unreachable stays unreachable within the same walk-connected component.
constexpr int route_distance(int cached, int displacement, int geometric) {
    return cached < 0 ? geometric : cached == unreachable ? unreachable
        : (cached - displacement > geometric ? cached - displacement : geometric);
}
constexpr int tribute_ticks(int gems) { return gems > 0 ? (gems + 9) / 10 : 1; }
// First movement is this round, after the respawn phase. Distance is a lower
// bound to an attack approach, not distance to an arbitrary group anchor.
constexpr int return_wait(int ready, int now, int distance, int speed) {
    if (ready <= now) return 0;
    if (speed <= 0) return ready - now;
    const int moves = (distance + speed - 1) / speed;
    const int arrival = now + (moves > 0 ? moves - 1 : 0);
    return ready > arrival ? ready - arrival : 0;
}
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
static_assert(return_wait(13, 10, 3, 1) == 1);
static_assert(return_wait(13, 10, 4, 1) == 0);
static_assert(return_wait(13, 10, 6, 2) == 1);
static_assert(return_wait(13, 10, 7, 2) == 0);
static_assert(return_wait(11, 10, 0, 1) == 1);
static_assert(return_wait(10, 10, 0, 1) == 0);
static_assert(return_wait(20, 10, 100, 0) > max_return_wait);
static_assert(value(7, 0, 1) > 0 && value(0, 20, 1) > value(0, 20, 1200));
static_assert(route_score(35, 2, 2, 0) > route_score(35, 20, 2, 0));
}
