// Fuel is deliberately exhausted once per champion, then execution must resume.
#include <cambc.h>
#include <algorithm>
#include <iostream>
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
            static bool exhausted = false;
            if (!exhausted) {
                exhausted = true;
                std::cout << "FUEL fixture start round=" << cambc::round_number() << std::endl;
                volatile unsigned value = 0;
                for (unsigned i = 0; i < 100000; ++i) value = value + i;
                std::cout << "FUEL fixture resumed round=" << cambc::round_number() << std::endl;
            }
        }
        cambc::end_turn();
    }
}
