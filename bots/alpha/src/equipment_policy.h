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
                                      unsigned combine, unsigned tie_start,
                                      bool allow_health = true) {
    std::array<unsigned, 3> counts{};
    if (!combine) return counts;
    for (unsigned n = 0; n < std::min(affordable, purchase_limit); ++n) {
        unsigned best = tie_start % 3;
        float best_value = current.value();
        for (unsigned offset = 0; offset < 3; ++offset) {
            const unsigned stat = (tie_start + offset) % 3;
            if (!allow_health && stat == 2) continue;
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

// Field purchases must improve offense without assuming a Health purchase heals.
// Keep spawn planning exactly equivalent to the original default eligibility.
static_assert([] {
    model tavi{900, 4500, 110, {5, 10, 75}, 1.125f, 0.175f};
    if (plan(tavi, 1, {}, 5, 2)[2] != 1) return false; // spawn favors Health
    const auto field = plan(tavi, 64, {}, 5, 2, false);
    if (field[2] || field[0] + field[1] != 64) return false;
    model focus{900, 45, 110, {0, 10, 75}, 1.125f, 0.175f};
    if (plan(focus, 1, {}, 5, 2, false)[1] != 1) return false;
    model finish{900, 45, 110, {5, 10, 75}, 1.125f, 0.175f};
    if (plan(finish, 1, {4, 0, 0}, 5, 2, false)[0] != 1) return false;
    model no_offense{900, 45, 110, {0, 0, 75}};
    if (plan(no_offense, 5, {}, 5, 2, false) != std::array<unsigned, 3>{}) return false;
    if (plan(tavi, 0, {}, 5, 0, false) != std::array<unsigned, 3>{}) return false;
    if (plan(tavi, 5, {}, 0, 0, false) != std::array<unsigned, 3>{}) return false;
    return plan(finish, 12, {2, 1, 4}, 5, 1) == plan(finish, 12, {2, 1, 4}, 5, 1, true);
}());
} // namespace equipment_policy
