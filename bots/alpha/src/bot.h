#pragma once
#include <cambc.h>
#include <vector>

class Bot {
    struct CampPlan {
        cambc::map::camp_group group;
        cambc::bitboard tiles;
        cambc::vec2 anchor;
        float health, damage;
        bool monolith;
        // Last personally observed respawn deadline; a prediction, never live state.
        unsigned ready_round = 0;
        unsigned avoid_until = 0;
    };
    std::vector<CampPlan> camps;
    int target = -1;
    unsigned role = 0, team_size = 1, failed_moves = 0;
    bool initialized = false;
    void initialize();
    void buy_items();
    int choose_camp();
    bool collect_here();
    void farm();
public:
    void play_turn();
};
