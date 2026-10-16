// Deliberate guest trap: not a champion death or a fuel suspension.
#include <cambc.h>
#include <algorithm>
int main() {
    for (;;) {
        if (cambc::is_draft()) {
            const auto chosen = cambc::draft::current_draft(cambc::team::ally);
            for (int i = 0; i < 11; ++i) {
                auto pick = static_cast<cambc::champion_draft>(i);
                if (std::find(chosen.begin(), chosen.end(), pick) == chosen.end()) {
                    cambc::draft::pick(pick);
                    break;
                }
            }
        } else {
            __builtin_trap();
        }
        cambc::end_turn();
    }
}
