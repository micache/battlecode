#pragma once
#include <algorithm>
#include <span>
#include <cstddef>

// Deterministic local estimates, not hidden state or an exact combat simulator.
namespace combat_value {
struct target { int x, y; float health; bool in_range; };
constexpr float hit(float damage, float health, float kill_bonus) {
    if (damage <= 0 || health <= 0) return 0;
    return std::min(damage, health) + (damage >= health ? kill_bonus : 0);
}
constexpr int magnitude(int value) { return value < 0 ? -value : value; }
constexpr float area(std::span<const target> targets, std::size_t aim, int radius,
                     float damage, float kill_bonus) {
    float score = 0;
    for (const auto& t : targets)
        if (std::max(magnitude(t.x - targets[aim].x), magnitude(t.y - targets[aim].y)) <= radius)
            score += hit(damage, t.health, kill_bonus);
    return score;
}
constexpr float basic(std::span<const target> targets, std::size_t aim, bool splash,
                      float damage, float kill_bonus) {
    return splash ? area(targets, aim, 1, damage, kill_bonus)
                  : hit(damage, targets[aim].health, kill_bonus);
}

// These exact policy-kernel cases compile under the trusted SDK/build check.
static_assert(hit(100, 20, 10) == 30); // Overkill is capped.
static_assert(hit(0, 20, 10) == 0 && hit(100, 0, 10) == 0);
static_assert([] {
    constexpr target group[]{{0, 0, 500, true}, {1, 0, 500, true}, {2, 0, 500, false}};
    // Varg aims at the middle; primary is counted exactly once.
    if (basic(group, 1, true, 50, 10) != 150 || basic(group, 0, true, 50, 10) != 100) return false;
    if (basic(group, 1, false, 50, 10) != 50) return false;
    // Ryth's three-target AoE beats a single reset.
    if (area(group, 1, 1, 100, 10) <= basic(group, 1, false, 50, 10)) return false;
    // Later Strength growth can correctly reverse that ordering for one target.
    constexpr target lone[]{{0, 0, 500, true}};
    return basic(lone, 0, false, 150, 10) > area(lone, 0, 1, 100, 10);
}());
} // namespace combat_value
