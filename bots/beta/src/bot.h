#pragma once
#include <cambc.h>
#include <vector>

// All knowledge is private to this champion. No live shared-memory writes.
class Bot {
    struct Group {
        cambc::map::camp_group group;
        cambc::bitboard spawns;
        cambc::vec2 anchor;
        float initial_health, initial_strength;
        unsigned retry_round = 0;
        unsigned ready_round = 0; // prediction from a timestamped respawn observation
    };
    std::vector<Group> groups;
    int target_group = -1;
    bool initialized = false;
    bool recovering = false;
    void initialize();
    void buy_items();
    bool hold_capture();
    void farm_camps();
public:
    void play_turn();
};
