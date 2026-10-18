#pragma once

// Pure, deterministic scheduling estimates. These are policy parameters, not
// claims about hidden camp state or measured damage per turn.
namespace farm_policy {
constexpr unsigned observed_deadline(unsigned now, int timer) {
    return now + static_cast<unsigned>(timer > 0 ? timer : 1);
}
constexpr bool cooling_down(unsigned now, unsigned observed_until) {
    return now < observed_until;
}
constexpr float score(unsigned travel_tiles, unsigned speed, float health,
    float strength, unsigned gems, unsigned gold, unsigned capture_ticks,
    bool committed, bool crowded) {
    const auto step = speed > 0 ? speed : 1;
    const float travel = (travel_tiles + step - 1) / step;
    const float clearing = health / (strength > 1 ? strength : 1);
    const float value = gems + 0.12f * gold;
    const float cost = travel + clearing + capture_ticks + 1;
    return cost / (value > 1 ? value : 1)
        * (committed ? 0.85f : 1.0f) * (crowded ? 1.35f : 1.0f);
}

// Lifecycle boundary: expired observations become unknown, including at zero.
static_assert(observed_deadline(20, 7) == 27);
static_assert(observed_deadline(20, 0) == 21);
static_assert(cooling_down(26, 27) && !cooling_down(27, 27));
// A nearby camp across a long wall can lose to a farther reachable one.
static_assert(score(30, 1, 500, 100, 24, 0, 5, false, false)
    > score(8, 1, 500, 100, 24, 0, 5, false, false));
// A free reward is useful, but cannot justify unlimited travel.
static_assert(score(2, 1, 0, 100, 24, 0, 5, false, false)
    < score(2, 1, 500, 100, 24, 0, 5, false, false));
static_assert(score(40, 1, 0, 100, 24, 0, 5, false, false)
    > score(2, 1, 500, 100, 24, 0, 5, false, false));
// Actual reward value can outweigh proximity; zero-gem gold still has value.
static_assert(score(8, 1, 1000, 100, 72, 90, 5, false, false)
    < score(2, 1, 500, 100, 24, 0, 5, false, false));
static_assert(score(2, 1, 500, 100, 0, 35, 5, false, false)
    > score(2, 1, 500, 100, 24, 0, 5, false, false));
static_assert(score(2, 1, 500, 100, 24, 0, 5, true, false)
    < score(2, 1, 500, 100, 24, 0, 5, false, false));
static_assert(score(2, 1, 500, 100, 24, 0, 5, false, true)
    > score(2, 1, 500, 100, 24, 0, 5, false, false));
} // namespace farm_policy
