#pragma once

// Pure admission policy. Distances/work are estimates, never hidden live state.
namespace circuit {
inline constexpr unsigned bag_limit = 96;
inline constexpr unsigned round_limit = 24;
inline constexpr int radius = 6;
inline constexpr int detour = 6;
inline constexpr float minimum_health = 0.75f;

constexpr bool must_bank(unsigned gems, unsigned age, float health_fraction,
    bool threat, unsigned submitted, unsigned winning, unsigned round, unsigned max_rounds) {
    return gems >= bag_limit || age >= round_limit || health_fraction < minimum_health
        || threat || submitted + gems >= winning || round + round_limit + 10 >= max_rounds;
}

constexpr bool admits(bool fully_observed_safe, unsigned gems, int travel,
    int onward_bank, int direct_bank, float work, unsigned age) {
    return fully_observed_safe && gems > 0 && travel <= radius
        && travel + onward_bank <= direct_bank + detour && age + work <= round_limit;
}

// Compile-time behavioral regressions run in the trusted bot-check build.
static_assert(!must_bank(22, 0, 1.0f, false, 0, 1000, 100, 2000));
static_assert(must_bank(96, 0, 1.0f, false, 0, 1000, 100, 2000));
static_assert(must_bank(22, 24, 1.0f, false, 0, 1000, 100, 2000));
static_assert(must_bank(22, 0, 0.74f, false, 0, 1000, 100, 2000));
static_assert(must_bank(22, 0, 1.0f, true, 0, 1000, 100, 2000));
static_assert(must_bank(22, 0, 1.0f, false, 978, 1000, 100, 2000));
static_assert(must_bank(22, 0, 1.0f, false, 0, 1000, 1966, 2000));
static_assert(admits(true, 24, 2, 8, 9, 15.0f, 0));
static_assert(!admits(false, 24, 2, 8, 9, 15.0f, 0));
static_assert(!admits(true, 0, 2, 8, 9, 15.0f, 0));
static_assert(!admits(true, 24, 7, 8, 9, 15.0f, 0));
static_assert(!admits(true, 24, 6, 10, 9, 15.0f, 0));
static_assert(!admits(true, 24, 2, 8, 9, 15.0f, 10));
} // namespace circuit
