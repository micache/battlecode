#pragma once
#include <algorithm>

namespace camp_rotation {
// Private, timestamped lower bound from a visible group's remaining timer.
// Expiry makes the group UNKNOWN again; it never establishes live occupancy.
struct cooldown_observation {
    unsigned observed_round = 0;
    unsigned earliest_round = 0;
    bool valid = false;

    constexpr void record(unsigned now, int remaining) {
        observed_round = now;
        earliest_round = now + static_cast<unsigned>(std::max(0, remaining));
        valid = true;
    }
    constexpr void clear() { valid = false; }
    constexpr bool excludes(unsigned now) const {
        // Zero means occupied/blocked NOW, not a forecast of future occupancy.
        return valid && (now == observed_round || now < earliest_round);
    }
};

constexpr bool eligible(unsigned now, unsigned retry_round,
    const cooldown_observation& cooldown) {
    return now >= retry_round && !cooldown.excludes(now);
}

// Stable lifecycle boundaries, compiled by the trusted WASM check.
static_assert([] {
    cooldown_observation c;
    if (!eligible(10, 0, c)) return false; // Unknown remains explorable.
    c.record(10, 3);
    if (eligible(10, 0, c) || eligible(12, 0, c)
        || !eligible(13, 0, c)) return false; // Exact expiry.
    c.clear();
    if (!eligible(11, 0, c)) return false; // Fresh live/reward overrides.
    c.record(20, 0);
    if (eligible(20, 0, c) || !eligible(21, 0, c)) return false;
    c.record(30, 8);
    c.record(32, 1);
    if (!eligible(33, 0, c)) return false; // Latest observation wins.
    c.record(40, -1);
    if (eligible(40, 0, c) || !eligible(41, 0, c)) return false;
    c.clear();
    return !eligible(49, 50, c) && eligible(50, 50, c);
}());
} // namespace camp_rotation
