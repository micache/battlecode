#pragma once

namespace policy {
// A conservative budget leaves enough health to escape after the last kill.
constexpr float risk_fraction = 0.65f;
constexpr unsigned bank_bag = 30;
constexpr int near_altar = 7;
constexpr unsigned end_margin = 20;
constexpr unsigned plan_lifetime = 8;
constexpr unsigned frontier_batch = 6;
constexpr unsigned ranking_batch = 32;
constexpr unsigned local_candidates = 4;
constexpr unsigned exploration_candidates = frontier_batch - local_candidates;
constexpr unsigned next_frontier(unsigned cursor, unsigned count) {
    return count == 0 ? 0 : (cursor + 1) % count;
}
static_assert(exploration_candidates == 2);
static_assert(next_frontier(0, 0) == 0);
static_assert(next_frontier(0, 1) == 0);
static_assert(next_frontier(16, 17) == 0);
static_assert(next_frontier(7, 17) == 8);
constexpr int plan_radius = 6;
constexpr bool refresh_plan(bool valid, unsigned now, unsigned observed, int moved) {
    return !valid || now < observed || now - observed >= plan_lifetime || moved > plan_radius;
}
static_assert(refresh_plan(false, 100, 100, 0));
static_assert(!refresh_plan(true, 105, 100, 6));
static_assert(refresh_plan(true, 100 + plan_lifetime, 100, 0));
static_assert(refresh_plan(true, 101, 100, 7));
static_assert(refresh_plan(true, 99, 100, 0));
constexpr bool exclude_target(bool could_move, bool deferred, bool at_goal) {
    return could_move && !deferred && !at_goal;
}
static_assert(exclude_target(true, false, false));
static_assert(!exclude_target(true, true, false));
static_assert(!exclude_target(false, false, false));
static_assert(!exclude_target(true, false, true));
constexpr float gold_value(unsigned cash) { return cash < 150 ? 0.18f : 0.04f; }
constexpr bool bank_now(unsigned bag, int altar_steps, unsigned round,
                        unsigned limit, unsigned submitted, unsigned winning) {
    return bag > 0 && (bag >= bank_bag || altar_steps <= near_altar
        || submitted + bag >= winning
        || round + static_cast<unsigned>(altar_steps) + (bag + 9) / 10 + end_margin >= limit);
}
static_assert(!bank_now(0, 0, 100, 2000, 0, 1000));
static_assert(!bank_now(7, 10, 100, 2000, 0, 1000));
static_assert(bank_now(7, 7, 100, 2000, 0, 1000));
static_assert(bank_now(30, 50, 100, 2000, 0, 1000));
static_assert(bank_now(5, 50, 100, 2000, 995, 1000));
static_assert(bank_now(7, 10, 1970, 2000, 0, 1000));
}
