#include <cambc.h>
#include "draft.h"
#include <algorithm>
#include <string_view>
#include <vector>
#include "random.h"

void play_draft() {
    // Guarantee a basic-attack splash farmer, then choose random remaining picks.
    const auto chosen = cambc::draft::current_draft(cambc::team::ally);
    std::vector<cambc::champion_draft> available;
    for (int i = 0; i < 11; ++i) { // Released champions only.
        auto pick = static_cast<cambc::champion_draft>(i);
        if (std::find(chosen.begin(), chosen.end(), pick) == chosen.end()) available.push_back(pick);
    }

    // Draft memory starts at byte zero and is copied to each champion.
    cambc::draft_memory = std::string_view("hello world");
    const auto fallback = available.at(random_number(available.size()));
    const auto farmer = std::find(available.begin(), available.end(), cambc::champion_draft::varg);
    cambc::draft::pick(farmer != available.end() ? *farmer : fallback);
}
