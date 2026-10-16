#pragma once

// Per-champion state survives between turns. Pick a build and keep buying it.
class Bot {
    int chosen_stat = -1;

    // Power build choices: Strength, Strength, Health; preserve the three-way draw.
    void buy_items();

public:
    // Priorities: shop and recall, attack enemies in range, bank gems, then farm.
    void play_turn();
};
