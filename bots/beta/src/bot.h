#pragma once

// Per-champion state survives between turns. Pick one stat and keep buying it.
class Bot {
    int chosen_stat = -1;

    // Spend only on power shards of the randomly chosen stat.
    void buy_items();

public:
    // Priorities: shop and recall, nearby tribute, combat, bank travel, then farm.
    void play_turn();
};
