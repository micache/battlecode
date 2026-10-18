#pragma once
#include <cambc.h>
#include <vector>

// Private instance state only; no live shared-memory protocol.
class Bot {
    struct Group {
        cambc::map::camp_group group;
        cambc::bitboard spawns;
        cambc::vec2 center;
        float initial_health;
        unsigned retry_round = 0;
    };
    std::vector<Group> groups;
    int target_group = -1;
    bool initialized = false;
    bool recovering = false;
    unsigned bag_started_round = 0;
    bool bank_committed = false;
    void buy_items();
    bool farm_camps(bool carrying = false);
public:
    void play_turn();
};
