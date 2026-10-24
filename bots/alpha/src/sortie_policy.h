#pragma once
#include <algorithm>
#include <cstdint>

namespace sortie_policy {
constexpr float retreat_fraction = 0.35f;
constexpr float resupply_health_fraction = 0.8f;
constexpr std::uint32_t resupply_gold = 150;

constexpr std::uint32_t jungle_purchase(std::uint32_t gold, std::uint32_t cost,
    std::uint32_t held, std::uint32_t combine, bool completed) {
    // Saturate before subtracting: completed or inconsistent inventories must
    // not underflow into an enormous purchase count.
    if (completed || !cost || held >= combine) return 0;
    return std::min(gold / cost, combine - held);
}
enum class recovery_action { proceed, return_home, wait_for_heal };
class recovery {
    bool returning = false; // Private to this champion, reset by death/full healing.
public:
    constexpr recovery_action update(bool alive, bool at_spawn, float health_fraction,
        bool resupply) {
        if (!alive) {
            returning = false;
            return recovery_action::proceed;
        }
        // Spawn healing occurs at turn END, after recall arrives at turn start.
        if (at_spawn) {
            if (health_fraction < 1.f) return recovery_action::wait_for_heal;
            returning = false;
            return recovery_action::proceed;
        }
        returning = returning || health_fraction < retreat_fraction || resupply;
        return returning ? recovery_action::return_home : recovery_action::proceed;
    }
};

static_assert(jungle_purchase(90, 30, 0, 5, false) == 3);
static_assert(jungle_purchase(300, 30, 3, 5, false) == 2);
static_assert(jungle_purchase(300, 30, 0, 5, true) == 0);
static_assert(jungle_purchase(29, 30, 0, 5, false) == 0);
static_assert(jungle_purchase(300, 30, 8, 5, false) == 0);
static_assert([] {
    recovery r;
    if (r.update(true, false, 1.f, false) != recovery_action::proceed) return false;
    if (r.update(true, false, .34f, false) != recovery_action::return_home) return false;
    if (r.update(true, false, .6f, false) != recovery_action::return_home) return false;
    if (r.update(true, true, .6f, false) != recovery_action::wait_for_heal) return false;
    if (r.update(true, true, 1.f, false) != recovery_action::proceed) return false;
    if (r.update(true, false, .8f, false) != recovery_action::proceed) return false;
    if (r.update(true, false, .8f, true) != recovery_action::return_home) return false;
    r.update(false, false, 0.f, false);
    if (r.update(true, false, 1.f, false) != recovery_action::proceed) return false;
    return r.update(true, true, .99f, false) == recovery_action::wait_for_heal;
}());
} // namespace sortie_policy
