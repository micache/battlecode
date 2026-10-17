#pragma once

// Per-champion state survives between turns. Pick one stat and keep buying it.
class Bot {
    int chosen_stat = -1;

    // Complete one Jungle emblem, then buy Power shards of the chosen stat.
    void buy_items();

public:
    // Priorities: shop and recall, attack enemies in range, bank gems, then farm.
    void play_turn();
};
