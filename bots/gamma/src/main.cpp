// Dispatch draft and gameplay; a failed turn is logged and still yields.
#include <cambc.h>
#include <iostream>
#include <limits>
#include <algorithm>
#include "bot.h"
#include "draft.h"

int main() {
    Bot bot;
    bool settings_checked = false;
    auto minimum_fuel = std::numeric_limits<std::uint64_t>::max();
    while (true) {
        try {
            if (cambc::is_draft())
                play_draft();
            else {
                if (!settings_checked) {
                    settings_checked = true;
                    if (cambc::constants::winning_gems != 1000 || cambc::constants::max_rounds != 2000
                        || cambc::constants::shared_memory_bytes != 8 || cambc::constants::draft_memory_bytes != 1024)
                        std::cout << "handbook settings mismatch" << '\n';
                }
                const auto started_round = cambc::round_number();
                bot.play_turn();
                const auto finished_round = cambc::round_number();
                const auto fuel = cambc::fuel_remaining();
                if (started_round > 1) minimum_fuel = std::min(minimum_fuel, fuel);
                if (started_round != finished_round)
                    std::cout << "harvest suspended " << started_round << " -> " << finished_round << '\n';
                if (finished_round % 100 == 0)
                    std::cout << "harvest round " << finished_round << " fuel " << fuel
                              << " minimum " << minimum_fuel << '\n';
            }
        } catch (const std::exception& error) {
            std::cout << "bot error: " << error.what() << std::endl;
        } catch (...) {
            std::cout << "bot error: unknown exception" << std::endl;
        }

        cambc::end_turn();
    }
}
