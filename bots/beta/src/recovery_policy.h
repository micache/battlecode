#pragma once
#include <cambc.h>
#include <array>

// Private, same-observation estimates only. Not a combat simulator: raw basic
// damage ignores target selection, mitigation, shields, spells and hidden units.
namespace recovery_policy {
constexpr unsigned threat_limit = 32;
struct threat {
    cambc::vec2 position;
    int range;
    float damage;
};
struct risk {
    float damage = 0;
    float depth = 0;
};
struct observation {
    std::array<threat, threat_limit> threats{};
    unsigned count = 0;
    bool complete = true;

    constexpr risk at(cambc::vec2 tile) const {
        risk result;
        for (unsigned i = 0; i < count; ++i) {
            const auto& t = threats[i];
            const auto d = tile.chebyshev_distance(t.position);
            if (d <= t.range) {
                result.damage += t.damage;
                // Break equal-damage plateaus by approaching the range edge.
                result.depth += t.damage * (t.range + 1 - d);
            }
        }
        return result;
    }
};

constexpr bool prefer(risk candidate, unsigned home_distance,
                      risk incumbent, unsigned incumbent_home_distance) {
    if (candidate.damage != incumbent.damage) return candidate.damage < incumbent.damage;
    if (candidate.depth != incumbent.depth) return candidate.depth < incumbent.depth;
    return home_distance < incumbent_home_distance;
}

// Stable decision fixtures: escape overlapping ranges even away from home,
// cross equal-damage plateaus, retain home progress when danger is equal, and
// never trade extra incoming damage for a shorter path. Compiled by bot-check.
static_assert([] {
    observation seen;
    seen.threats[seen.count++] = {{0, 0}, 3, 60};
    seen.threats[seen.count++] = {{1, 0}, 3, 40};
    if (seen.at({2, 0}).damage != 100 || seen.at({5, 0}).damage != 0) return false;
    if (!prefer(seen.at({3, 0}), 20, seen.at({2, 0}), 1)) return false;
    if (!prefer(seen.at({4, 0}), 21, seen.at({3, 0}), 1)) return false;
    if (!prefer(seen.at({5, 0}), 22, seen.at({4, 0}), 1)) return false;
    if (prefer(seen.at({4, 0}), 1, seen.at({5, 0}), 22)) return false;
    if (!prefer({0, 0}, 4, {0, 0}, 5) || prefer({0, 0}, 5, {0, 0}, 4)) return false;
    if (prefer({100, 1}, 0, {60, 1000}, 100)) return false;
    if (prefer({0, 0}, 0, {0, 0}, 0)) return false;
    return true;
}());
} // namespace recovery_policy
