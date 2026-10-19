#pragma once
#include <algorithm>

namespace farm_value {
// A positive reward forces a bank trip in gamma's macro policy. Gold alone
// does not. Distances are optimistic static walking distances, not live routes.
constexpr float score(float acquisition_turns, unsigned gems, unsigned gold,
                      unsigned delivery_steps, unsigned move_speed, float tribute_turns) {
    const auto speed = std::max(1u, move_speed);
    const auto walking_turns = delivery_steps / speed + (delivery_steps % speed != 0);
    const float delivery = gems ? walking_turns + tribute_turns : 0.0f;
    return (acquisition_turns + delivery) / std::max(1.0f, gems + 0.12f * gold);
}

// Equal rewards: acquisition-only ranking chooses the farther delivery, while
// the full cycle chooses the cheaper completed tribute. A rich remote camp can
// still win, and gold-only camps never pay a fictitious tribute trip.
static_assert(15.0f / 24 < 20.0f / 24);
static_assert(score(20, 24, 0, 0, 1, 3) < score(15, 24, 0, 20, 1, 3));
static_assert(score(20, 100, 0, 10, 1, 10) < score(20, 24, 0, 0, 1, 3));
static_assert(score(20, 0, 35, 100, 1, 10) == score(20, 0, 35, 0, 1, 0));
static_assert(score(10, 10, 0, 3, 2, 1) == 1.3f);
static_assert(score(10, 10, 0, 3, 0, 1) == 1.4f);
} // namespace farm_value
