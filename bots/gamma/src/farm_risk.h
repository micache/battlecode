#pragma once

namespace farm_risk {
// Policy estimates, not engine damage predictions: some members die early or
// sleep while another is focused. Do not assume unseen allies will tank for us.
inline constexpr float EXPOSURE = 0.60f;
inline constexpr float CLEAR_MULTIPLIER = 1.12f;
inline constexpr float HEALTH_RESERVE = 0.35f;

constexpr float expected_damage(float hp, float incoming, float strength,
                                bool jungle, bool durability) {
    const float dps = strength * CLEAR_MULTIPLIER;
    return hp * incoming * EXPOSURE / (dps > 1.0f ? dps : 1.0f)
        * (jungle ? 0.70f : 1.0f) * (durability ? 0.90f : 1.0f);
}

constexpr bool feasible(float hp, float incoming, float strength,
                        float health, float max_health, bool jungle, bool durability) {
    // Cleared rewards and harmless clusters must remain available at any HP.
    if (hp <= 0 || incoming <= 0) return true;
    return expected_damage(hp, incoming, strength, jungle, durability)
        <= health - HEALTH_RESERVE * max_health;
}

// Compile the actual policy's stable cases in the trusted build.
static_assert(feasible(1350, 20, 70, 800, 800, false, false));
static_assert(!feasible(2400, 60, 70, 800, 800, false, false));
static_assert(feasible(2400, 60, 200, 1200, 1200, true, true));
static_assert(!feasible(1350, 20, 70, 400, 800, false, false));
static_assert(feasible(500, 0, 1, 1, 1200, false, false));
static_assert(feasible(0, 200, 1, 1, 1200, false, false));
static_assert(expected_damage(1350, 20, 70, true, true)
              < expected_damage(1350, 20, 70, false, false));
static_assert(expected_damage(1350, 20, 0, false, false) > 0);
} // namespace farm_risk
