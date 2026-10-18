#pragma once
#include <algorithm>
#include <span>

namespace combat_scoring {
// One current visible observation. Damage is predicted health loss, not raw
// spell power, when the SDK offers a target-specific prediction.
struct target {
    int x, y;
    float health, damage;
};

constexpr float hit(const target& target, float finish_bonus, float control_bonus = 0) {
    if (target.health <= 0) return 0;
    const float damage = std::clamp(target.damage, 0.0f, target.health);
    return damage + (damage >= target.health ? finish_bonus : 0) + control_bonus;
}

constexpr float area(std::span<const target> targets, int x, int y, float radius,
                     float finish_bonus, float control_bonus = 0) {
    float score = 0;
    for (const auto& target : targets) {
        const int dx = target.x > x ? target.x - x : x - target.x;
        const int dy = target.y > y ? target.y - y : y - target.y;
        if (std::max(dx, dy) <= radius)
            score += hit(target, finish_bonus, control_bonus);
    }
    return score;
}

// Compile-time regressions run in the actual bot build, with no runtime cost.
namespace checks {
inline constexpr target cluster[]{{0, 0, 500, 100}, {1, 0, 500, 100},
                                  {2, 0, 500, 100}, {8, 8, 500, 100}};
static_assert(area(cluster, 1, 0, 1, 20) == 300); // central aim hits three
static_assert(area(cluster, 0, 0, 1, 20) == 200); // edge aim hits only two
static_assert(area(cluster, 8, 8, 1, 20) == 100); // isolated aim hits one
static_assert(hit({0, 0, 25, 200}, 20) == 45);   // cap overkill, reward finish
static_assert(hit({0, 0, 80, 80}, 100) > hit({0, 0, 500, 150}, 100));
static_assert(hit({0, 0, 100, 0}, 100) == 0);    // shielded damage is worthless
static_assert(hit({0, 0, 100, 0}, 100, 20) == 20); // control still has value
static_assert(hit({0, 0, 0, 200}, 100, 20) == 0); // no dead-unit value
}
}
