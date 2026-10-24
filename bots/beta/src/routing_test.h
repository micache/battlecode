#pragma once
#include "policy.h"
// Behavioral boundaries: maze detours, local search horizon, stale origin and
// target review. These execute at compile time in the trusted build.
namespace routing_tests {
constexpr unsigned unreachable = 65535;
static_assert(policy::travel_steps(3, 17, 0, unreachable) == 17);
static_assert(policy::travel_steps(3, unreachable, 0, unreachable) == 25);
static_assert(policy::travel_steps(40, unreachable, 0, unreachable) == 40);
static_assert(policy::travel_steps(3, 17, 4, unreachable) == 13);
static_assert(policy::travel_steps(15, 17, 4, unreachable) == 15);
static_assert(policy::travel_steps(0, 0, 0, unreachable) == 0);
static_assert(!policy::review_target(100, 100));
static_assert(!policy::review_target(115, 100));
static_assert(policy::review_target(116, 100));
static_assert(policy::review_target(99, 100));
// Same reward/clear: the geometrically near camp behind a wall loses to a
// slightly farther directly reachable camp, even with 25% target hysteresis.
constexpr float detour_score = 7.0f / (policy::travel_steps(3, 20, 0, unreachable) + 7);
constexpr float direct_score = 7.0f / (policy::travel_steps(8, 8, 0, unreachable) + 7);
static_assert(direct_score > 1.25f * detour_score);
}
