#pragma once
#include <cstdint>

namespace objective_policy {
constexpr std::uint64_t bootstrap_capital = 150;
constexpr float capture_rounds = 6.0f; // First capture phase plus five countdowns.
constexpr float clearing_multiplier = 1.12f;
constexpr float commitment_discount = 0.85f;

constexpr bool objective_mode(std::uint64_t capital) {
    return capital >= bootstrap_capital;
}

// Strict preference, not an additive penalty: a nearby committed gold group
// must not beat an eligible gem group after the first emblem's endowment.
constexpr unsigned tier(bool objective, unsigned gems) {
    return objective && gems == 0 ? 1 : 0;
}

constexpr bool farmable(bool monolith, bool reward_available) {
    return !monolith || reward_available;
}

constexpr float completion_cost(unsigned outbound, float clearing, unsigned bank,
                                unsigned gems, unsigned gold, bool committed) {
    const auto tribute = (gems + 9) / 10;
    const float value = gems ? static_cast<float>(gems)
        : gold ? static_cast<float>(gold) * 0.12f : 1.0f;
    const float rounds = outbound + clearing + capture_rounds
        + (gems ? bank + tribute : 0);
    return rounds / value * (committed ? commitment_discount : 1.0f);
}

static_assert(!farmable(true, false) && farmable(true, true));
static_assert(farmable(false, false));
static_assert(!objective_mode(149) && objective_mode(150));
static_assert(tier(true, 24) < tier(true, 0));
static_assert(tier(false, 0) == tier(false, 24));
// Equal-yield near camps beat distant ones; clearing and banking both matter.
static_assert(completion_cost(1, 4, 1, 24, 0, false)
    < completion_cost(20, 4, 1, 24, 0, false));
static_assert(completion_cost(1, 4, 1, 24, 0, false)
    < completion_cost(1, 40, 1, 24, 0, false));
static_assert(completion_cost(1, 4, 1, 24, 0, false)
    < completion_cost(1, 4, 20, 24, 0, false));
// A 200-gem monolith is not automatically more efficient than a gem cluster.
static_assert(completion_cost(2, 500.0f / 100, 4, 24, 0, false)
    < completion_cost(2, 20000.0f / 100, 4, 200, 300, false));
// But a cleared monolith can be the best reward. Preserve commitment smoothly.
static_assert(completion_cost(2, 0, 4, 200, 300, false)
    < completion_cost(2, 5, 4, 24, 0, false));
static_assert(completion_cost(2, 5, 4, 24, 0, true)
    < completion_cost(2, 5, 4, 24, 0, false));
} // namespace objective_policy
