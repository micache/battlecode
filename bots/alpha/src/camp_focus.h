#pragma once
#include <cambc.h>
#include <cstdint>
#include <optional>

namespace camp_focus {

constexpr std::uint64_t fuel_reserve = 18000;
constexpr unsigned target_limit = 16;

// All basics from this body have the same damage. Among legal static camps,
// lower remaining HP minimizes hits to the next kill. Exact ties keep engine
// order so equal-health targets do not introduce a new arbitrary preference.
constexpr bool prefer(float health, float incumbent_health) {
    return health > 0 && (incumbent_health <= 0 || health < incumbent_health);
}

static_assert([] {
    // A wounded later camp beats an untouched earlier one; a dead camp never
    // steals focus. Re-evaluating after a kill chooses the next living camp.
    constexpr float before[]{1350, 80, 500, 0, 80};
    float health = 0;
    unsigned chosen = 99;
    for (unsigned i = 0; i < 5; ++i)
        if (prefer(before[i], health)) { health = before[i]; chosen = i; }
    if (chosen != 1 || prefer(80, health) || prefer(0, health)) return false;
    constexpr float after[]{1350, 0, 500, 0, 80};
    health = 0;
    for (unsigned i = 0; i < 5; ++i)
        if (prefer(after[i], health)) { health = after[i]; chosen = i; }
    return chosen == 4 && !prefer(0, 0) && !prefer(-1, 0);
}());

// One fresh observation only: range masks do not certify visibility or health.
// This deliberately does not choose routes, consult groups, or cache live state.
inline std::optional<cambc::camp> select(const cambc::bitboard& range) {
    std::optional<cambc::camp> selected;
    float health = 0;
    unsigned examined = 0;
    for (const auto& camp : cambc::vision::camps()) {
        if (++examined > target_limit || cambc::fuel_remaining() < fuel_reserve) break;
        if (!camp.is_visible() || !range.is_set(camp.position())) continue;
        const float remaining = camp.health();
        if (prefer(remaining, health)) {
            selected = camp;
            health = remaining;
        }
    }
    return selected;
}

} // namespace camp_focus
