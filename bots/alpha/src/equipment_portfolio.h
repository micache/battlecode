#pragma once
#include "equipment_policy.h"

namespace equipment_portfolio {
// Workload assumptions, not observations of hidden units or fitted parameters.
constexpr float camp_share = 0.8f;
constexpr float minimum_advantage = 1.05f;
constexpr unsigned family_count = 2;
constexpr unsigned family_fuel_reserve = 38000;

struct offer {
    std::array<unsigned, 3> residues{};
    unsigned cost = 0, combine = 0;
    float value_multiplier = 1;
    bool owned = false; // any stat's emblem supplies the one nonstacking passive
};
struct purchase {
    unsigned family = 0, stat = 0, count = 0;
    float advantage = minimum_advantage;
};

constexpr float jungle_value(float reduction) {
    return reduction > 0 && reduction < 1 ? 1 / (1 - camp_share * reduction) : 1;
}
constexpr float monster_value(float bonus) {
    const float rate = 1 + camp_share * bonus;
    return bonus > 0 && bonus < 1 ? rate * rate : 1;
}

// Six offers, each compared against <=64 local Power choices. No engine calls.
constexpr purchase choose(equipment_policy::model current, unsigned gold,
                           unsigned power_cost, unsigned power_combine,
                           std::array<unsigned, 3> power_residues,
                           const std::array<offer, family_count>& offers,
                           unsigned tie_start, unsigned remaining) {
    purchase best;
    if (!power_cost || !power_combine) return best;
    remaining = std::min(remaining, equipment_policy::purchase_limit);
    for (unsigned family = 0; family < family_count; ++family) {
        const auto& candidate = offers[family];
        if (candidate.owned || !candidate.cost || !candidate.combine
            || candidate.combine > equipment_policy::purchase_limit
            || candidate.value_multiplier <= 1) continue;
        for (unsigned offset = 0; offset < 3; ++offset) {
            const unsigned stat = (tie_start + offset) % 3;
            if (candidate.residues[stat] >= candidate.combine) continue;
            const unsigned needed = candidate.combine - candidate.residues[stat];
            if (needed > remaining || needed > gold / candidate.cost) continue;
            const unsigned spend = needed * candidate.cost; // <= gold, cannot overflow
            const unsigned power_count = spend / power_cost;
            if (power_count > remaining) continue; // compare only equally bounded plans
            auto ordinary = current;
            const auto counts = equipment_policy::plan(current, power_count,
                power_residues, power_combine, tie_start);
            for (unsigned s = 0; s < 3; ++s)
                ordinary.add(s, counts[s] + (power_residues[s] + counts[s]) / power_combine
                                            - power_residues[s] / power_combine);
            if (ordinary.value() <= 0) continue;
            auto bundle = current;
            bundle.add(stat, needed); // these families have five growth points, no Power bonus
            const float advantage = bundle.value() * candidate.value_multiplier / ordinary.value();
            if (advantage > best.advantage)
                best = {family, stat, needed, advantage};
        }
    }
    return best;
}

// Semantic regressions compiled with the actual bot by the trusted wrapper.
static_assert([] {
    using equipment_policy::model;
    model fighter{1000, 100, 0, {5, 0, 50}};
    std::array<offer, family_count> offers{{
        {{}, 30, 5, jungle_value(0.3f), false},
        {{}, 30, 5, monster_value(0.1f), false}}};
    const auto select = [&](model m, unsigned gold = 150, unsigned cap = 64) {
        return choose(m, gold, 30, 5, {}, offers, 0, cap);
    };
    // No partial family purchases, and a hard total-purchase cap.
    if (select(fighter, 149).count || select(fighter, 150, 4).count) return false;
    auto next = select(fighter);
    if (next.family != 0 || next.stat != 0 || next.count != 5) return false;
    // Ownership across ANY stat blocks the passive; Monster remains eligible.
    offers[0].owned = true;
    next = select(fighter);
    if (next.family != 1 || next.stat != 0 || next.count != 5) return false;
    offers[1].owned = true;
    if (select(fighter).count) return false;
    offers[0].owned = false;
    offers[1].owned = false;
    // Early high-growth offense can prefer Power's extra point to either passive.
    if (select(model{1000, 10, 0, {30, 0, 1}}).count) return false;
    // Focus is used only for a kit that actually scales its damage with Focus.
    model caster{650, 30, 70, {1, 13, 20}, 1, 0.5f};
    if (select(caster).stat != 1) return false;
    // Finish existing shards immediately even with a one-shard budget.
    offers[0].residues[2] = 4;
    next = select(fighter, 30, 1);
    if (next.family != 0 || next.stat != 2 || next.count != 1) return false;
    // Invalid settings and overpriced offers are rejected safely.
    offers[0].combine = 0;
    offers[1].cost = 1000;
    if (select(fighter).count) return false;
    offers[0].combine = 10000;
    if (select(fighter, 100000).count) return false;
    if (choose(fighter, 150, 0, 5, {}, offers, 0, 64).count
        || choose(fighter, 150, 30, 0, {}, offers, 0, 64).count) return false;
    return jungle_value(0) == 1 && jungle_value(1) == 1
        && monster_value(0) == 1 && monster_value(1) == 1;
}());
} // namespace equipment_portfolio
