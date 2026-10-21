#pragma once

// Per-champion state survives between turns. Pick one stat and keep buying it.
class Bot {
    int chosen_stat = -1;
    bool recovering = false;
    bool disengaging = false;

    // Spend only on power shards of the randomly chosen stat.
    void buy_items();
    bool recover();

public:
    // Priorities: shop and recall, attack enemies in range, bank gems, then farm.
    void play_turn();
};
