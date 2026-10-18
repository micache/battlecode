#pragma once
#include <cambc.h>
#include <vector>
#include "camp_claims.h"

// Private camp observations; shared bytes carry only expiring target intents.
class Bot {
    struct Farm {
        cambc::map::camp_group group;
        cambc::bitboard spawns;
        unsigned respawn_observed_until = 0;
    };
    std::vector<Farm> farms;
    camp_claims::board claims;
    int target_group = -1;
    void buy_items();
    void farm_camps();
public:
    void play_turn();
};
