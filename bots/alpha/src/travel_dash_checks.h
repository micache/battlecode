#pragma once
#include "travel_dash.h"

// Compiled in the trusted bot build; no runtime work or engine-state assumptions.
namespace travel::checks {
struct Tile {
    int x, y;
    constexpr bool operator==(const Tile&) const = default;
};
constexpr bool corridor_free(Tile p) {
    if (p.x < 0 || p.x >= 7 || p.y != 0) throw "off-map callback";
    return true;
}
constexpr auto corridor_distance = [](Tile p) { return 6u - p.x; };
static_assert(dash_destination(Tile{0, 0}, 7, 1, corridor_free, corridor_distance) == Tile{2, 0});
// Walking reveals a blocker: reject both an occupied midpoint and landing even
// if the old route field still rates the destination highly.
static_assert(!dash_destination(Tile{0, 0}, 7, 1,
    [](Tile p) { return corridor_free(p) && p.x != 1; }, corridor_distance));
static_assert(!dash_destination(Tile{0, 0}, 7, 1,
    [](Tile p) { return corridor_free(p) && p.x != 2; }, corridor_distance));
// No off-map callbacks, no leaving a goal, no one-step "saving", no unreachable
// origin mistaken for a large distance that justifies a dash.
static_assert(!dash_destination(Tile{6, 0}, 7, 1, corridor_free, corridor_distance));
static_assert(!dash_destination(Tile{5, 0}, 7, 1, corridor_free, corridor_distance));
static_assert(!dash_destination(Tile{0, 0}, 7, 1, corridor_free,
    [](Tile p) { return p.x == 0 ? 5u : 4u; }));
static_assert(!dash_destination(Tile{0, 0}, 7, 1, corridor_free,
    [](Tile) { return std::numeric_limits<std::uint16_t>::max(); }));
static_assert(dash_destination(Tile{6, 0}, 7, 1, corridor_free,
    [](Tile p) { return static_cast<unsigned>(p.x); }) == Tile{4, 0});
} // namespace travel::checks
