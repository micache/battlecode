#pragma once

// Per-champion state survives between turns. Keep the chosen stat across builds.
class Bot {
    int chosen_stat = -1;
    bool recovering = false;

    // One Jungle emblem, then Power shards of the randomly chosen stat.
    void buy_items();
    bool recover();

public:
    // Priorities: shop and recall, attack enemies in range, bank gems, then farm.
    void play_turn();
};
