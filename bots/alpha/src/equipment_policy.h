#pragma once
#include <array>
#include <algorithm>

namespace equipment_policy {
// A shop-only model, not a prediction of hidden camps or an exact fight.
// Weight clear speed twice and sortie health once: H * damage_per_turn^2.
// Draft, routing, item family and combat execution are independent of this model.
constexpr unsigned purchase_limit = 64;
constexpr unsigned entry_fuel_reserve = 45000;
constexpr unsigned purchase_fuel_reserve = 28000;
constexpr float area_targets = 1.5f;
constexpr float shield_credit = 0.5f;

struct model {
    float health, strength, focus;
    std::array<float, 3> growth; // Strength, Focus, Health
    float basic_rate = 1;
    float focus_rate = 0;
    float shield_scale = 0;
    float health_to_strength = 0;

    constexpr float value() const {
        const float damage = std::max(0.0f, strength * basic_rate + focus * focus_rate);
        return std::max(1.0f, health + focus * shield_scale) * damage * damage;
    }
    constexpr void add(unsigned stat, unsigned points) {
        const float delta = growth[stat] * points;
        if (stat == 0) strength += delta;
        if (stat == 1) focus += delta;
        if (stat == 2) {
            health += delta;
            strength += delta * health_to_strength;
        }
    }
};

// Snapshot once, simulate locally, then execute at most three bulk purchases.
// Matching fifth Power shard contributes two growth points (six for five).
constexpr std::array<unsigned, 3> plan(model current, unsigned affordable,
                                      std::array<unsigned, 3> residues,
                                      unsigned combine, unsigned tie_start) {
    std::array<unsigned, 3> counts{};
    if (!combine) return counts;
    for (unsigned n = 0; n < std::min(affordable, purchase_limit); ++n) {
        unsigned best = tie_start % 3;
        float best_value = current.value();
        for (unsigned offset = 0; offset < 3; ++offset) {
            const unsigned stat = (tie_start + offset) % 3;
            auto next = current;
            next.add(stat, (residues[stat] + 1) % combine == 0 ? 2 : 1);
            if (next.value() > best_value) {
                best_value = next.value();
                best = stat;
            }
        }
        if (best_value <= current.value()) break;
        current.add(best, (residues[best] + 1) % combine == 0 ? 2 : 1);
        residues[best] = (residues[best] + 1) % combine;
        ++counts[best];
    }
    return counts;
}

// Jungle's documented 30% camp mitigation is discounted for mixed damage.
// These are deterministic workload assumptions, not measured damage forecasts.
constexpr float camp_exposure_fraction = 0.8f;
constexpr float jungle_reduction = 0.3f;
constexpr float bundle_advantage = 1.05f;

struct bundle {
    unsigned cost, combine, residue;
};
struct bundle_choice {
    unsigned stat = 0, count = 0;
};

// Compare immediately completed protection with exactly the same gold in the
// existing Power allocator. Never strand gold in an unfinished passive family.
// Three alternatives, each with at most 64 local Power choices; normal bundles
// cost only five choices. Existing emblems in ANY stat suppress the whole family.
constexpr bundle_choice choose_jungle(model current, unsigned gold,
        unsigned power_cost, std::array<unsigned, 3> power_residues,
        unsigned power_combine, std::array<bundle, 3> bundles,
        bool already_owned, unsigned tie_start) {
    bundle_choice result;
    if (already_owned || !power_cost || !power_combine) return result;
    float best_ratio = bundle_advantage;
    for (unsigned offset = 0; offset < 3; ++offset) {
        const unsigned stat = (tie_start + offset) % 3;
        const auto b = bundles[stat];
        if (!b.cost || !b.combine || b.combine > purchase_limit) continue;
        const unsigned needed = b.combine - b.residue % b.combine;
        if (needed > gold / b.cost) continue;
        const unsigned equivalent = needed * b.cost / power_cost;
        if (equivalent > purchase_limit) continue;
        auto power = current;
        const auto counts = plan(current, equivalent, power_residues,
                                 power_combine, tie_start);
        for (unsigned s = 0; s < 3; ++s)
            power.add(s, counts[s] + (power_residues[s] + counts[s]) / power_combine);
        auto jungle = current;
        jungle.add(stat, needed); // no Power-family extra stat point
        const float denominator = power.value() * (1 - camp_exposure_fraction * jungle_reduction);
        if (denominator <= 0) continue;
        const float ratio = jungle.value() / denominator;
        if (ratio > best_ratio) {
            best_ratio = ratio;
            result = {stat, needed};
        }
    }
    return result;
}

static_assert([] {
    const model fighter{1000, 100, 50, {6, 0, 60}};
    const std::array<bundle, 3> full{{{30, 5, 0}, {30, 5, 0}, {30, 5, 0}}};
    const auto choose = [&](unsigned gold, bool owned = false) {
        return choose_jungle(fighter, gold, 30, {}, 5, full, owned, 1);
    };
    if (choose(149).count || choose(150, true).count) return false;
    const auto ready = choose(150);
    if (ready.count != 5 || ready.stat == 1) return false; // no unused Focus
    auto partial = full;
    partial[ready.stat].residue = 4;
    const auto finish = choose_jungle(fighter, 30, 30, {}, 5, partial, false, 1);
    if (finish.count != 1 || finish.stat != ready.stat) return false;
    auto expensive = full;
    for (auto& b : expensive) b.cost = 300;
    if (choose_jungle(fighter, 1500, 30, {}, 5, expensive, false, 0).count) return false;
    auto invalid = full;
    for (auto& b : invalid) b.combine = 0;
    return !choose_jungle(fighter, 10000, 30, {}, 5, invalid, false, 0).count
        && !choose_jungle(fighter, 10000, 0, {}, 5, full, false, 0).count;
}());

static_assert([] {
    model reset{1000, 50, 80, {6, 10, 80}, 1.125f};
    const auto early = plan(reset, 1, {}, 5, 1);
    if (early[0] != 1 || early[1] || early[2]) return false;
    reset.strength = 1000; // large offense now makes health the marginal choice
    const auto late = plan(reset, 1, {}, 5, 0);
    if (late[2] != 1) return false;
    model caster{650, 30, 70, {1, 13, 20}, 1, 0.5f};
    if (plan(caster, 1, {}, 5, 0)[1] != 1) return false;
    model passive{1200, 45, 100, {5, 10, 100}};
    passive.health_to_strength = 0.01f;
    passive.add(2, 2);
    if (passive.health != 1400 || passive.strength != 47) return false;
    // Completion bonus can beat a competing stat; no nonexistent focus scaling.
    model finish{1000, 100, 0, {5, 0, 110}};
    if (plan(finish, 1, {4, 0, 0}, 5, 2)[0] != 1) return false;
    const auto bounded = plan(caster, 10000, {}, 5, 0);
    return bounded[0] + bounded[1] + bounded[2] == purchase_limit
        && plan(caster, 0, {}, 5, 0) == std::array<unsigned, 3>{}
        && plan(caster, 10, {}, 0, 0) == std::array<unsigned, 3>{};
}());
} // namespace equipment_policy
