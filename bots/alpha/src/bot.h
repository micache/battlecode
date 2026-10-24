#pragma once

// Per-champion state survives between turns. RNG breaks equal shop scores.
class Bot {
    int chosen_stat = -1;

    // Allocate Power shards using current stats and usable kit scaling.
    // Field Health raises max HP without healing, so it is spawn-only.
    void buy_items(bool at_spawn = true);

public:
    // Priorities: shop and recall, attack enemies in range, bank gems, then farm.
    void play_turn();
};
