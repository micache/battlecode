#pragma once

namespace policy {
// Progress is an actual successful combat action, not an attempted action.
// Engine allowances and observations remain the caller's responsibility.
// A failed action gets one movement/reveal phase, never an unbounded retry.
constexpr unsigned harvest_action_limit = 6;
template<class Ready, class Reward, class Strike, class Move>
constexpr void harvest_turn(Ready ready, Reward reward, Strike strike, Move move) {
    bool moved = false;
    for (unsigned actions = 0; actions < harvest_action_limit;) {
        if (!ready()) return;
        if (reward()) { move(true); return; }
        if (strike()) { ++actions; continue; }
        if (moved || !ready()) return;
        move(false);
        moved = true;
    }
    // The final allowed strike may have killed the group's last member.
    if (ready() && reward()) move(true);
}
}
