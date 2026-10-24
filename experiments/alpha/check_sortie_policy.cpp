#include "../../bots/alpha/src/sortie_policy.h"
#include <cassert>
#include <iostream>

int main() {
    using namespace sortie_policy;
    // Purchasing across multiple visits must finish one passive, never overbuy it.
    assert(jungle_purchase(29, 30, 0, 5, false) == 0);
    assert(jungle_purchase(90, 30, 0, 5, false) == 3);
    assert(jungle_purchase(300, 30, 3, 5, false) == 2);
    assert(jungle_purchase(300, 30, 0, 5, true) == 0);
    assert(jungle_purchase(300, 30, 8, 5, false) == 0);

    recovery state;
    assert(state.update(true, false, 1.0f, false) == recovery_action::proceed);
    assert(state.update(true, false, .34f, false) == recovery_action::return_home);
    // Do not abandon recovery if a partial heal crosses the entry threshold.
    assert(state.update(true, false, .6f, false) == recovery_action::return_home);
    assert(state.update(true, true, .6f, false) == recovery_action::wait_for_heal);
    assert(state.update(true, true, 1.0f, false) == recovery_action::proceed);
    assert(state.update(true, false, .8f, false) == recovery_action::proceed);
    // A profitable empty-bag resupply is also a committed return.
    assert(state.update(true, false, .8f, true) == recovery_action::return_home);
    assert(state.update(false, false, 0.f, false) == recovery_action::proceed);
    assert(state.update(true, false, 1.f, false) == recovery_action::proceed);
    // Even unlatched recall/teleport arrivals need the end-of-turn spawn heal.
    assert(state.update(true, true, .99f, false) == recovery_action::wait_for_heal);
    std::cout << "sortie purchase and recovery scenarios passed\n";
}
