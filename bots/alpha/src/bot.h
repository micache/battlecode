#pragma once

// Per-champion state survives between turns. Pick one stat and keep buying it.
class Bot {
    int chosen_stat = -1;
    // Private to this champion; retained while our recall channel is active.
    bool recall_pending = false;

    // Spend only on power shards of the randomly chosen stat.
    void buy_items();

public:
    // Priorities: shop and recall, attack enemies in range, bank gems, then farm.
    void play_turn();
};
