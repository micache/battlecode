#pragma once
#include <cambc.h>
#include <vector>

// Private per-body state. No live shared-memory protocol or allied hidden vision.
class Bot {
    struct Farm {
        cambc::map::camp_group group;
        cambc::bitboard spawns;
        unsigned respawn_observed_until = 0;
        unsigned delivery_steps = cambc::distance_field::unreachable;
    };
    std::vector<Farm> farms;
    int target_group = -1;
    void buy_items();
    void farm_camps();
public:
    void play_turn();
};
