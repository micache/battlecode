#pragma once
#include "sortie_policy.h"

class Bot {
    sortie_policy::recovery recovery;
    // Complete one Jungle emblem, then stack basic-attack damage.
    void buy_items();
public:
    void play_turn();
};
