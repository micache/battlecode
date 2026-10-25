#pragma once
#include "prism_banking.h"

// Per-champion state survives between turns. RNG breaks equal shop scores.
class Bot {
    int chosen_stat = -1;
    prism_banking::policy prism_bank;

    // Allocate Power shards using current stats and usable kit scaling.
    void buy_items();

public:
    // Priorities: shop and recall, attack enemies in range, bank gems, then farm.
    void play_turn();
};
