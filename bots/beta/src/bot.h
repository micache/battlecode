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
        unsigned observed_respawn_until = 0;
        unsigned gems = 0;
        unsigned gold = 0;
        unsigned bank_distance = 0;
        bool monolith = false;
    };
    std::vector<Group> groups;
    int target_group = -1;
    bool initialized = false;
    bool recovering = false;
    void buy_items();
    void farm_camps();
public:
    void play_turn();
};
