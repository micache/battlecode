#pragma once
namespace combat_policy {
// Damage is a ranking estimate, not a prediction of mitigation or shields.
constexpr float hit_value(float health, float damage, float strength) {
    if (health <= 0 || damage <= 0) return 0;
    return (health < damage ? health : damage) + (health <= damage ? strength * 0.5f : 0);
}
static_assert(hit_value(0, 100, 100) == 0);
static_assert(hit_value(100, 0, 100) == 0);
static_assert(hit_value(400, 100, 100) == 100);
static_assert(hit_value(100, 100, 100) == 150);
static_assert(hit_value(10, 100, 100) == 60); // avoid scoring 100 overkill damage
static_assert(hit_value(80, 100, 100) > hit_value(500, 100, 100));
}
