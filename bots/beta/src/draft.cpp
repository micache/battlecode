#include <cambc.h>
#include "draft.h"
#include <algorithm>
#include <array>

void play_draft() {
    using D = cambc::champion_draft;
    // Splash farmer, field shopper, durable AoE, high-Strength reset, stun immunity.
    constexpr std::array order{D::varg, D::tavi, D::ryth, D::vendetta, D::marcella,
        D::vesper_vale, D::ren, D::stellar, D::prism, D::willow, D::cassi_and_issac};
    const auto chosen = cambc::draft::current_draft(cambc::team::ally);
    const auto size = cambc::draft::team_size();
    if (chosen.size() >= size) return;
    for (auto pick : order)
        if (std::find(chosen.begin(), chosen.end(), pick) == chosen.end()) {
            cambc::draft::pick(pick);
            return;
        }
}
