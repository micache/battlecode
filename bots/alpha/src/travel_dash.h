#pragma once

#include <cstdint>
#include <limits>
#include <optional>

namespace travel {
constexpr unsigned dash_steps = 2;
constexpr unsigned minimum_dash_gain = 2;

// Search eight straight two-step paths, deliberately avoiding hole jumps and
// bent paths. Callbacks use the current occupancy and an existing route field.
// This stays independent of SDK allocation/state so geometry can be regressed.
template<class Position, class Free, class Distance>
constexpr std::optional<Position> dash_destination(Position origin, int width, int height,
                                         Free free, Distance distance) {
    const auto start = distance(origin);
    if (start == std::numeric_limits<std::uint16_t>::max()) return std::nullopt;
    auto best = start;
    std::optional<Position> result;
    for (int dy = -1; dy <= 1; ++dy) {
        for (int dx = -1; dx <= 1; ++dx) {
            if (dx == 0 && dy == 0) continue;
            const Position middle{origin.x + dx, origin.y + dy};
            const Position end{origin.x + 2 * dx, origin.y + 2 * dy};
            if (end.x < 0 || end.y < 0 || end.x >= width || end.y >= height)
                continue;
            if (!free(middle) || !free(end)) continue;
            const auto remaining = distance(end);
            if (remaining < best && start - remaining >= minimum_dash_gain) {
                best = remaining;
                result = end;
            }
        }
    }
    return result;
}
} // namespace travel
