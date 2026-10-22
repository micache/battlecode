// Real-engine acceptance fixture, never a scoring opponent or worker candidate.
#include <cambc.h>
#include <algorithm>
#include <iostream>

int main() {
    int calls = 0;
    for (;;) {
        if (calls < 2) {
            std::cout << "PROFILE draft=" << cambc::is_draft()
                      << " call=" << calls << " round=" << cambc::round_number()
                      << " max_rounds=" << cambc::constants::max_rounds
                      << " winning_gems=" << cambc::constants::winning_gems
                      << " draft_bytes=" << cambc::draft_memory.size()
                      << " live_bytes=" << cambc::shared_memory.size()
                      << " remaining_fuel=" << cambc::fuel_remaining() << '\n';
            std::cout << "BALANCE kill_gold=" << cambc::constants::kill_gold
                      << " ward_cooldown=" << cambc::constants::ward_cooldown
                      << " altar_lock_hits=" << cambc::constants::altar_lock_hits << '\n';
        }
        if (cambc::is_draft()) {
            auto picked = cambc::draft::current_draft(cambc::team::ally);
            for (int i = 0; i < 11; ++i) {
                auto pick = static_cast<cambc::champion_draft>(i);
                if (std::find(picked.begin(), picked.end(), pick) == picked.end()) {
                    cambc::draft::pick(pick);
                    break;
                }
            }
        }
        ++calls;
        cambc::end_turn();
    }
}
