#pragma once
// Stable policy invariants, evaluated by the trusted C++ build without runtime cost.
#include "policy.h"
static_assert(!policy::withdraw(false, false, 100, 200, 50, 100));
static_assert(!policy::withdraw(true, true, 100, 200, 50, 100));
static_assert(!policy::withdraw(true, false, 200, 100, 50, 100));
static_assert(!policy::withdraw(true, false, 100, 100, 50, 100));
static_assert(policy::withdraw(true, false, 80, 100, 50, 100));
static_assert(policy::withdraw(true, false, 200, 100, 90, 100));
static_assert(policy::contact_pressure(20, 1, 1) == 20);
static_assert(policy::contact_pressure(20, 1, 2) == 20);
static_assert(policy::contact_pressure(20, 1, 3) == 0);
static_assert(policy::contact_pressure(20, 3, 4) == 20);
static_assert(policy::escape_better(0, 3, 20, 20, 4, 1));
static_assert(!policy::escape_better(20, 4, 1, 0, 3, 20));
static_assert(policy::escape_better(20, 4, 20, 20, 3, 1));
static_assert(policy::escape_better(20, 4, 1, 20, 4, 2));
static_assert(!policy::escape_better(20, 4, 2, 20, 4, 1));
static_assert(!policy::escape_better(20, 4, 2, 20, 4, 2));
