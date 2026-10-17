#include <cambc.h>
#include "draft.h"
#include <algorithm>
#include <array>

void play_draft() {
    // Independent durable farmers: splash, high Strength/kill resets, then tank.
    // Extra map-dependent picks add ranged economy and a field shopper.
    constexpr std::array roster{cambc::champion_draft::varg,
        cambc::champion_draft::vendetta, cambc::champion_draft::ryth,
        cambc::champion_draft::vesper_vale, cambc::champion_draft::tavi,
        cambc::champion_draft::marcella, cambc::champion_draft::stellar,
        cambc::champion_draft::prism, cambc::champion_draft::ren,
        cambc::champion_draft::willow, cambc::champion_draft::cassi_and_issac};
    const auto chosen = cambc::draft::current_draft(cambc::team::ally);
    if (chosen.size() >= cambc::draft::team_size()) return;
    for (auto pick : roster)
        if (std::find(chosen.begin(), chosen.end(), pick) == chosen.end()) {
            cambc::draft::pick(pick);
            return;
        }
}
