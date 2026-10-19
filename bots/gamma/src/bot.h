#pragma once
#include <cambc.h>
#include <vector>

// Private per-body state. No live shared-memory protocol or allied hidden vision.
class Bot {
    struct Farm {
        cambc::map::camp_group group;
        cambc::bitboard spawns;
        unsigned respawn_observed_until = 0;
    };
    std::vector<Farm> farms;
    int target_group = -1;
    unsigned capture_entries_logged = 0; // Private, capped diagnostics per body.
    void buy_items();
    void farm_camps();
public:
    void play_turn();
};
