#include <cambc.h>
#include "draft.h"
#include <algorithm>
#include <array>

void play_draft() {
    using D = cambc::champion_draft;
    // Durable melee farmers can walk, basic attack and reset in one turn.
    // Varg supplies splash; Vendetta can reset again after a monster kill.
    constexpr std::array order{D::varg, D::vendetta, D::marcella, D::ryth,
        D::tavi, D::vesper_vale, D::ren, D::stellar, D::prism,
        D::willow, D::cassi_and_issac};
    const auto chosen = cambc::draft::current_draft(cambc::team::ally);
    for (auto pick : order) {
        if (std::find(chosen.begin(), chosen.end(), pick) == chosen.end()) {
            cambc::draft::pick(pick);
            return;
        }
    }
}
