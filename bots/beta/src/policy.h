#pragma once

namespace policy {
// A conservative budget leaves enough health to escape after the last kill.
constexpr float risk_fraction = 0.65f;
constexpr unsigned bank_bag = 30;
constexpr int near_altar = 7;
constexpr unsigned end_margin = 20;
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
