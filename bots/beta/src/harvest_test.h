#pragma once
#include "harvest.h"

// Compile-time controller fixtures; no game state or runtime test instructions.
namespace harvest_regression {
struct Arena {
    int monsters = 3, strikes = 0, moves = 0, captures = 0;
    bool in_range = true, allowed = true, reset_on_kill = true;
    unsigned events = 0;
    constexpr void run() {
        policy::harvest_turn([&]{return allowed;}, [&]{return monsters == 0;}, [&]{
            if (!in_range || !allowed) return false;
            events = events * 10 + 1;
            ++strikes; --monsters;
            if (!reset_on_kill) allowed = false;
            return true;
        }, [&](bool capture){
            events = events * 10 + (capture ? 3 : 2);
            if (capture) ++captures;
            else { ++moves; in_range = true; }
        });
    }
};
constexpr bool fixtures() {
    { Arena a; a.run(); if (a.events != 1113) return false; }
    { Arena a; a.in_range = false; a.run(); if (a.events != 21113) return false; }
    { Arena a; a.monsters = 0; a.run(); if (a.events != 3) return false; }
    { Arena a; a.reset_on_kill = false; a.run(); if (a.events != 1) return false; }
    { Arena a; a.allowed = false; a.run(); if (a.events != 0) return false; }
    { Arena a; a.monsters = 100; a.run(); if (a.strikes > 6 || a.captures) return false; }
    { Arena a; a.monsters = 6; a.run(); if (a.events != 1111113) return false; }
    { int moves = 0, attacks = 0;
      policy::harvest_turn([]{return true;}, []{return false;},
          [&]{++attacks; return false;}, [&](bool capture){if (!capture) ++moves;});
      if (moves != 1 || attacks != 2) return false;
    }
    return true;
}
static_assert(fixtures(), "harvest ordering, fuel cutoff or action bounds regressed");
}
