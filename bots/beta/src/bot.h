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
        unsigned gems = 0, gold = 0;
        int count = 0;
    };
    std::vector<Group> groups;
    // Private terrain estimates; current visibility is checked independently.
    std::vector<std::size_t> plan_order;
    std::vector<unsigned> plan_distance;
    unsigned plan_round = 0;
    cambc::vec2 plan_origin{};
    bool plan_valid = false;
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
