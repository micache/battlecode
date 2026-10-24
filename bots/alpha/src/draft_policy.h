#pragma once
#include "equipment_policy.h"
#include <array>

namespace draft_policy {
constexpr unsigned roster_size = 12;
constexpr unsigned opening_shards = 5;
constexpr float linked_survival_credit = 0.5f;

// Equal weight on first-sortie capability and one completed opening investment.
constexpr float opening_value(equipment_policy::model base, unsigned combine) {
    auto grown = base;
    const auto allocation = equipment_policy::plan(base, opening_shards, {}, combine, 0);
    if (combine) {
        for (unsigned stat = 0; stat < 3; ++stat)
            grown.add(stat, allocation[stat] + allocation[stat] / combine);
    }
    return base.value() + grown.value();
}

// A legal pick, never a physical instance index. Engine order on unequal scores;
// a seeded cyclic preference only resolves equal values. roster_size means none.
constexpr unsigned select(const std::array<float, roster_size>& values,
                          const std::array<bool, roster_size>& taken,
                          unsigned tie_start) {
    unsigned best = roster_size;
    for (unsigned offset = 0; offset < roster_size; ++offset) {
        const unsigned pick = (tie_start + offset) % roster_size;
        if (!taken[pick] && (best == roster_size || values[pick] > values[best])) best = pick;
    }
    return best;
}

static_assert([] {
    std::array<float, roster_size> values{};
    std::array<bool, roster_size> taken{};
    if (select(values, taken, 3) != 3) return false;
    values[11] = 8; // all released picks, including the newest, are selectable
    if (select(values, taken, 0) != 11) return false;
    taken[11] = true;
    values[2] = 7;
    if (select(values, taken, 0) != 2) return false;
    for (unsigned n = 0; n < roster_size - 1; ++n) {
        const auto pick = select(values, taken, n);
        if (pick >= roster_size || taken[pick]) return false;
        taken[pick] = true;
    }
    if (select(values, taken, 0) != roster_size) return false;
    equipment_policy::model basic{1000, 70, 100, {6, 10, 100}};
    if (opening_value(basic, 5) <= 2 * basic.value()) return false;
    if (opening_value(basic, 0) != 2 * basic.value()) return false;
    // Fifth-shard growth is the real six-point Power completion, not five.
    equipment_policy::model offense{1000000, 10, 0, {10, 0, 0}};
    auto grown = offense;
    grown.add(0, 6);
    return opening_value(offense, 5) == offense.value() + grown.value();
}());
} // namespace draft_policy
