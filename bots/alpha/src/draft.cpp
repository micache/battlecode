#include <cambc.h>
#include "draft.h"
#include <algorithm>
#include <array>

void play_draft() {
    using D = cambc::champion_draft;
    // Four melee reset farmers can walk and attack; Tavi reinvests in the field.
    constexpr std::array order{D::varg, D::vendetta, D::marcella, D::ryth, D::tavi};
    const auto chosen = cambc::draft::current_draft(cambc::team::ally);
    if (chosen.size() >= cambc::draft::team_size()) return;
    for (const auto pick : order) {
        if (std::find(chosen.begin(), chosen.end(), pick) == chosen.end()) {
            cambc::draft::pick(pick);
            return;
        }
    }
}
