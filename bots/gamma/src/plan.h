#pragma once
#include <cstddef>
#include <cstdint>

namespace policy {
// Draft protocol v2: GA, version, u16 count, (u8 x,u8 y), optional gem bitset.
// Bit i denotes a group with a nonzero immutable gem reward. Omit the entire
// bitset if it would exceed 1024 bytes; v1/missing metadata remains eligible.
// No live observations, per-body records or live writes.
inline constexpr std::size_t plan_header = 5, max_groups = 509;
inline constexpr int shortlist = 8, bank_bag = 24, near_bank = 6;
inline constexpr int gem_shortlist = 4;
constexpr std::size_t reward_offset(std::size_t n, std::size_t i) {
    return plan_header + 2*n + i/8;
}
constexpr unsigned reward_bit(std::size_t i) { return 1u << (i%8); }
constexpr std::size_t reward_plan_size(std::size_t n) {
    return plan_header + 2*n + (n+7)/8;
}
constexpr bool reward_mask_fits(std::size_t n) { return reward_plan_size(n) <= 1024; }
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
inline constexpr float developed_gold_weight = 0.20f;
constexpr float value(int gems, int gold, int round, bool farming_core = false) {
    return 5.0f * gems + (round < 900 ? 1.0f : 0.35f)
        * (farming_core ? developed_gold_weight : 1.0f) * gold;
}
constexpr float route_score(float reward, float travel, float clear, int wait) {
    return reward / (8.0f + travel + clear + wait);
}
static_assert(route_distance(unreachable, 4, 1) == unreachable);
static_assert(route_distance(30, 4, 1) == 26);
static_assert(route_distance(-1, 0, 9) == 9);
static_assert(route_distance(2, 4, 1) == 1);
static_assert(plan_header + 2 * max_groups <= 1024);
static_assert(reward_plan_size(479) == 1023 && !reward_mask_fits(480));
static_assert(!reward_mask_fits(max_groups)); // Fall back without dropping anchors.
static_assert(reward_offset(9, 8) == 24 && reward_bit(8) == 1);
static_assert(reward_offset(479, 478) < reward_plan_size(479));
static_assert(tribute_ticks(1) == 1 && tribute_ticks(10) == 1 && tribute_ticks(11) == 2);
static_assert(value(7, 0, 1) > 0 && value(0, 20, 1) > value(0, 20, 1200));
static_assert(route_score(35, 2, 2, 0) > route_score(35, 20, 2, 0));
// Keep the opening economy. Once both farming emblems exist, a seven-gem
// group ten steps away beats a nearby forty-gold group (equal clear/capture).
static_assert(route_score(value(0, 40, 100), 2, 2, 5)
    > route_score(value(7, 0, 100), 10, 2, 5));
static_assert(route_score(value(0, 40, 100, true), 2, 2, 5)
    < route_score(value(7, 0, 100, true), 10, 2, 5));
static_assert(value(0, 20, 1200, true) > 0); // Gold fallback is never prohibited.
}
