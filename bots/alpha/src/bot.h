#pragma once

// Per-champion state survives between turns.
class Bot {
    bool initialized = false;

    // Spend only on Power shards of Strength for the basic-attack policy.
    void buy_items();

public:
    // Priorities: shop and recall, attack enemies in range, bank gems, then farm.
    void play_turn();
};
