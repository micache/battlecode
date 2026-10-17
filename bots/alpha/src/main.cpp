// Dispatch draft and gameplay; a failed turn is logged and still yields.
#include <cambc.h>
#include <iostream>
#include "bot.h"
#include "draft.h"

int main() {
    Bot bot;
    unsigned turns = 0;
    std::uint64_t lowest_fuel = 1000000;
    while (true) {
        try {
            if (cambc::is_draft())
                play_draft();
            else
                bot.play_turn();
        } catch (const std::exception& error) {
            std::cout << "bot error: " << error.what() << std::endl;
        } catch (...) {
            std::cout << "bot error: unknown exception" << std::endl;
        }

        if (!cambc::is_draft()) {
            const auto fuel = cambc::fuel_remaining();
            lowest_fuel = std::min(lowest_fuel, fuel);
            if (++turns <= 8 || turns % 128 == 0)
                std::cout << "fuel_end " << turns << ' ' << fuel << " minimum " << lowest_fuel << '\n';
        }
        cambc::end_turn();
    }
}
