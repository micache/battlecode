#pragma once

// Per-champion state survives between turns. Pick one stat and keep buying it.
class Bot {
    int chosen_stat = -1;

    // Spend only on power shards of the randomly chosen stat.
    void buy_items();

public:
    // Shop/recall first; bags >=36 skip enemy combat to bank; otherwise combat, bank, farm.
    void play_turn();
};
