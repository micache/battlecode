#include <cambc.h>
#include "draft.h"
#include <algorithm>
#include <array>

void play_draft() {
    using D = cambc::champion_draft;
    // Front-load melee farmers: walking preserves their basic attack, and
    // Vendetta's monster kills refresh the reset/dash used by our farming routes.
    // Keep Ryth's durable AoE in three-pick teams; add stun immunity fourth.
    // Field shopping and ranged control remain available on five-pick maps.
    constexpr std::array order{D::varg, D::vendetta, D::ryth, D::marcella, D::tavi,
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
