#pragma once
#include <algorithm>

namespace camp_rotation {

// Policy estimates, not claims about hidden health or exact ability throughput.
// Gold is useful for later sorties, but gems remain the principal objective.
constexpr float gold_weight = 0.12f;
constexpr float commitment_discount = 0.90f;
constexpr unsigned route_candidate_limit = 8;
constexpr unsigned route_member_limit = 16;

constexpr float route_cost(float travel, float health, float strength,
                           unsigned gems, unsigned gold, unsigned capture_time) {
    const float value = std::max(1.0f, float(gems) + gold_weight * float(gold));
    const unsigned tribute = (gems + 9) / 10;
    return (travel + health / std::max(1.0f, strength) + capture_time + tribute + 1) / value;
}

// Executed by the trusted compiler: reward, work and travel all affect selection.
static_assert(route_cost(10, 500, 50, 24, 0, 5) < route_cost(10, 1350, 50, 22, 90, 5));
static_assert(route_cost(10, 0, 50, 24, 0, 5) < route_cost(10, 500, 50, 24, 0, 5));
static_assert(route_cost(5, 500, 50, 24, 0, 5) < route_cost(20, 500, 50, 24, 0, 5));
static_assert(route_cost(10, 500, 100, 24, 0, 5) < route_cost(10, 500, 50, 24, 0, 5));
static_assert(route_cost(0, 500, 0, 0, 0, 5) > 0); // finite at zero stats/reward

} // namespace camp_rotation
