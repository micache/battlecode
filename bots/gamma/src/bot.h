#pragma once
#include <cambc.h>
#include <vector>

// Private per-body state. No live shared-memory protocol or allied hidden vision.
class Bot {
    struct Farm {
        cambc::map::camp_group group;
        cambc::bitboard spawns;
        unsigned respawn_observed_until = 0;
        cambc::vec2 center;
        float initial_health = 0;
    };
    std::vector<Farm> farms;
    int target_group = -1;
    std::size_t farm_probe = 0;
    void buy_items();
    void farm_camps();
public:
    void play_turn();
};
