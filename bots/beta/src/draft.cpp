#include <cambc.h>
#include "draft.h"
#include <algorithm>
#include <array>

void play_draft() {
    using D = cambc::champion_draft;
    // Splash clearing, kill resets, field investment, durable AoE, safe tributes.
    constexpr std::array order{D::varg, D::vendetta, D::tavi, D::ryth, D::marcella,
        D::vesper_vale, D::ren, D::heart_of_ruin, D::stellar, D::prism,
        D::willow, D::cassi_and_issac};
    const auto chosen = cambc::draft::current_draft(cambc::team::ally);
    if (chosen.size() >= cambc::draft::team_size()) return;
    for (auto pick : order) {
        if (std::find(chosen.begin(), chosen.end(), pick) != chosen.end()) continue;
        cambc::draft::pick(pick);
        return;
    }
}
