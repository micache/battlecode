// Host geometry regression for the actual bot selector, not an engine fixture.
#include "travel_dash.h"
#include <algorithm>
#include <array>
#include <cassert>
#include <iostream>
#include <queue>

struct Tile {
    int x, y;
    bool operator==(const Tile&) const = default;
};

struct Grid {
    static constexpr int width = 7, height = 7;
    static constexpr auto unreachable = std::numeric_limits<std::uint16_t>::max();
    std::array<bool, width * height> blocked{};
    std::array<std::uint16_t, width * height> distances{};

    bool inside(Tile p) const { return p.x >= 0 && p.y >= 0 && p.x < width && p.y < height; }
    int index(Tile p) const { assert(inside(p)); return p.y * width + p.x; }
    bool free(Tile p) const { return !blocked[index(p)]; }
    unsigned distance(Tile p) const { return distances[index(p)]; }
    void field(Tile goal) {
        distances.fill(unreachable);
        distances[index(goal)] = 0;
        std::queue<Tile> frontier;
        frontier.push(goal);
        while (!frontier.empty()) {
            const auto p = frontier.front(); frontier.pop();
            for (int dy = -1; dy <= 1; ++dy)
                for (int dx = -1; dx <= 1; ++dx) {
                    const Tile next{p.x + dx, p.y + dy};
                    if (!inside(next) || !free(next) || distance(next) != unreachable) continue;
                    distances[index(next)] = distance(p) + 1;
                    frontier.push(next);
                }
        }
    }
    auto choose(Tile origin) const {
        return travel::dash_destination(origin, width, height,
            [&](Tile p) { return free(p); }, [&](Tile p) { return distance(p); });
    }
};

int main() {
    unsigned scenarios = 0;
    Grid corridor;
    corridor.blocked.fill(true);
    for (int x = 0; x < Grid::width; ++x) corridor.blocked[corridor.index({x, 3})] = false;
    corridor.field({6, 3});
    assert(corridor.choose({0, 3}) == (Tile{2, 3})); ++scenarios;

    // New blockers after computing the field must invalidate either segment.
    corridor.blocked[corridor.index({1, 3})] = true;
    assert(!corridor.choose({0, 3})); ++scenarios;
    corridor.blocked[corridor.index({1, 3})] = false;
    corridor.blocked[corridor.index({2, 3})] = true;
    assert(!corridor.choose({0, 3})); ++scenarios;
    corridor.field({6, 3});
    assert(!corridor.choose({0, 3})); ++scenarios; // unreachable origin

    Grid short_route;
    short_route.field({6, 3});
    assert(!short_route.choose({5, 3})); ++scenarios; // one step is not worth a cast
    assert(!short_route.choose({6, 3})); ++scenarios; // preserve goal occupancy
    short_route.distances.fill(4);
    short_route.distances[short_route.index({3, 3})] = 5;
    assert(!short_route.choose({3, 3})); ++scenarios; // two-tile detour saves only one

    // Exhaust every origin/goal with a wall, hole or occupied-tile pattern.
    // The selector must never read off-map, cross a blocker or gain < 2 steps.
    for (unsigned pattern = 0; pattern < 4; ++pattern) {
        Grid grid;
        for (int y = 0; y < Grid::height; ++y)
            for (int x = 0; x < Grid::width; ++x)
                grid.blocked[grid.index({x, y})] = pattern && (x * 7 + y * 11) % (pattern + 3) == 0;
        for (int gy = 0; gy < Grid::height; ++gy) for (int gx = 0; gx < Grid::width; ++gx) {
            const Tile goal{gx, gy};
            if (!grid.free(goal)) continue;
            grid.field(goal);
            for (int y = 0; y < Grid::height; ++y) for (int x = 0; x < Grid::width; ++x) {
                const Tile origin{x, y};
                if (!grid.free(origin)) continue;
                const auto end = grid.choose(origin);
                if (end) {
                    const Tile delta{end->x - x, end->y - y};
                    assert(std::max(std::abs(delta.x), std::abs(delta.y)) == 2);
                    assert(delta.x == 0 || delta.y == 0 || std::abs(delta.x) == std::abs(delta.y));
                    assert(grid.free(*end));
                    assert(grid.free({x + delta.x / 2, y + delta.y / 2}));
                    assert(grid.distance(origin) != Grid::unreachable);
                    assert(grid.distance(*end) + travel::minimum_dash_gain <= grid.distance(origin));
                }
                ++scenarios;
            }
        }
    }
    std::cout << "PASS: " << scenarios << " travel-dash geometry scenarios\n";
}
