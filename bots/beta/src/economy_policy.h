#pragma once
#include <cstdint>

namespace economy_policy {
// Two farming emblems' purchase value ends the gold-only bootstrap phase.
constexpr std::uint64_t bootstrap_capital = 300;
// Same score units as 30 geometric travel steps. A soft penalty retains a
// fallback when gem groups are cooling down, occupied or too far away.
constexpr float gold_only_penalty = 90.0f;
constexpr float opportunity_penalty(unsigned gems, std::uint64_t capital) {
    return gems == 0 && capital >= bootstrap_capital ? gold_only_penalty : 0.0f;
}
static_assert(opportunity_penalty(0, 299) == 0);
static_assert(opportunity_penalty(0, 300) == gold_only_penalty);
static_assert(opportunity_penalty(0, 10000) == gold_only_penalty);
static_assert(opportunity_penalty(1, 300) == 0);
static_assert(opportunity_penalty(24, 10000) == 0);
// Even committed gold clearing (+12 hysteresis) loses to a comparable gem
// route 20 steps farther away; extremely remote gems do not forbid fallback.
static_assert(opportunity_penalty(0, 300) - 12 > 20 * 3);
static_assert(opportunity_penalty(0, 300) < 40 * 3);
}
