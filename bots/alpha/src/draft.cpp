#include <cambc.h>
#include "draft.h"
#include <algorithm>
#include <array>

void play_draft() {
    // Farming kits: high base Strength, splash, tribute income, field shopping.
    using C = cambc::champion_draft;
    constexpr std::array preference{C::vendetta, C::varg, C::marcella,
        C::tavi, C::vesper_vale, C::ryth, C::heart_of_ruin, C::ren,
        C::prism, C::stellar, C::willow, C::cassi_and_issac};
    const auto chosen = cambc::draft::current_draft(cambc::team::ally);
    if (chosen.size() >= cambc::draft::team_size()) return;
    for (const auto pick : preference) {
        if (std::find(chosen.begin(), chosen.end(), pick) != chosen.end()) continue;
        cambc::draft::pick(pick);
        return;
    }
}
