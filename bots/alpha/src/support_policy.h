#pragma once
#include <algorithm>
#include <cstdint>

namespace support_policy {
constexpr std::uint64_t entry_fuel_reserve = 50000;
constexpr std::uint64_t scan_fuel_reserve = 38000;
constexpr unsigned observation_limit = 16;
constexpr float injured_ratio = 0.85f;
constexpr float minimum_efficiency = 0.5f;

// A raw volley is only evidence of exposure, never a prediction of who is hit.
constexpr bool shield_worthwhile(float hp, float maximum, float shield,
                                 int duration, float volley, bool active) {
    return !active && hp > 0 && maximum > 0 && shield > 0 && duration > 0
        && volley > 0 && (hp < maximum * injured_ratio
            || volley * duration >= shield * minimum_efficiency);
}

constexpr float heal_score(float hp, float maximum, float amount) {
    if (hp <= 0 || maximum <= 0 || amount <= 0 || hp >= maximum * injured_ratio)
        return 0;
    const float useful = std::min(amount, maximum - hp);
    if (useful < amount * minimum_efficiency) return 0;
    return useful * (2 - hp / maximum);
}

static_assert(!shield_worthwhile(500, 1000, 300, 2, 0, false));
static_assert(!shield_worthwhile(500, 1000, 300, 2, 100, true));
static_assert(shield_worthwhile(800, 1000, 300, 2, 20, false));
static_assert(!shield_worthwhile(1000, 1000, 300, 2, 20, false));
static_assert(shield_worthwhile(1000, 1000, 300, 2, 75, false));
static_assert(!shield_worthwhile(500, 1000, 300, 0, 100, false));
static_assert(heal_score(0, 1000, 300) == 0);
static_assert(heal_score(900, 1000, 300) == 0);
static_assert(heal_score(800, 1000, 500) == 0); // insufficient useful healing
static_assert(heal_score(800, 1000, 400) > 0); // exact efficiency boundary
static_assert(heal_score(300, 1000, 300) > heal_score(600, 1000, 300));
static_assert(heal_score(800, 1000, 0) == 0);
} // namespace support_policy
