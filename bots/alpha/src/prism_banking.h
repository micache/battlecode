#pragma once
#include <cstdint>

namespace prism_banking {

// Policy parameters, not game constants. Forty gems add 60 Focus to Prism.
inline constexpr std::uint32_t retained_bag_limit = 40;
inline constexpr std::uint32_t retention_rounds = 80;
inline constexpr std::uint32_t endgame_margin = 200;
inline constexpr unsigned bank_health_percent = 65;

// Private per-instance state; no shared bytes or hidden enemy observations.
class policy {
    bool active = false;
    bool committed = false;
    std::uint32_t first_round = 0;

public:
    constexpr void reset() { active = committed = false; }
    constexpr void commit() { if (active) committed = true; }

    constexpr bool update(std::uint32_t gems, std::uint32_t now,
                          std::uint32_t submitted, std::uint32_t winning,
                          std::uint32_t max_rounds, float health, float max_health,
                          bool visible_enemy) {
        if (!gems) {
            reset();
            return false;
        }
        if (!active) {
            active = true;
            first_round = now;
        }
        // Avoid overflowing score/round addition. Once triggered, a bank trip
        // cannot oscillate back to farming after healing or losing enemy vision.
        const bool can_win = submitted >= winning || gems >= winning - submitted;
        const bool endgame = now >= max_rounds || max_rounds - now <= endgame_margin;
        committed = committed || gems >= retained_bag_limit
            || now - first_round >= retention_rounds || can_win || endgame
            || max_health <= 0 || health * 100 <= bank_health_percent * max_health
            || visible_enemy;
        return committed;
    }
};

// Compiled as part of the trusted bot build, without SDK calls.
static_assert([] {
    policy p;
    if (p.update(0, 100, 0, 1000, 2000, 700, 700, false)) return false;
    if (p.update(1, 100, 0, 1000, 2000, 700, 700, false)) return false;
    if (p.update(39, 179, 0, 1000, 2000, 700, 700, false)) return false;
    if (!p.update(39, 180, 0, 1000, 2000, 700, 700, false)) return false;
    if (!p.update(1, 181, 0, 1000, 2000, 700, 700, false)) return false;
    if (p.update(0, 182, 0, 1000, 2000, 700, 700, false)) return false;
    if (p.update(39, 183, 0, 1000, 2000, 700, 700, false)) return false;
    return p.update(40, 184, 0, 1000, 2000, 700, 700, false);
}());

static_assert([] {
    policy p;
    if (p.update(10, 100, 989, 1000, 2000, 700, 700, false)) return false;
    if (!p.update(10, 101, 990, 1000, 2000, 700, 700, false)) return false;
    p.reset();
    if (!p.update(1, 100, 1001, 1000, 2000, 700, 700, false)) return false;
    p.reset();
    if (p.update(1, 1799, 0, 1000, 2000, 700, 700, false)) return false;
    if (!p.update(1, 1800, 0, 1000, 2000, 700, 700, false)) return false;
    p.reset();
    return p.update(1, 2001, 0, 1000, 2000, 700, 700, false);
}());

static_assert([] {
    policy p;
    if (p.update(20, 100, 0, 1000, 2000, 456, 700, false)) return false;
    if (!p.update(20, 101, 0, 1000, 2000, 455, 700, false)) return false;
    if (!p.update(20, 102, 0, 1000, 2000, 700, 700, false)) return false;
    p.reset();
    if (!p.update(1, 100, 0, 1000, 2000, 700, 700, true)) return false;
    if (!p.update(1, 101, 0, 1000, 2000, 700, 700, false)) return false;
    p.reset();
    p.commit(); // death without an observed bag must not poison a later sortie
    if (p.update(1, 100, 0, 1000, 2000, 700, 700, false)) return false;
    p.commit(); // death with a previously observed bag commits surviving gems
    if (!p.update(1, 101, 0, 1000, 2000, 700, 700, false)) return false;
    p.update(0, 102, 0, 1000, 2000, 700, 700, false);
    return !p.update(1, 103, 0, 1000, 2000, 700, 700, false);
}());

} // namespace prism_banking
