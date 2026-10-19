#pragma once

namespace economy_policy {
// Five shards buy one emblem. Cash already sufficient for that investment
// should not justify another trip to a camp that cannot advance tribute.
constexpr unsigned unspent_gold_cap = 150;
constexpr bool eligible(unsigned group_gems, unsigned unspent_gold) {
    return group_gems > 0 || unspent_gold < unspent_gold_cap;
}

// Eligibility uses current cash, never lifetime gold or purchased equipment.
static_assert(eligible(0, 0));
static_assert(eligible(0, unspent_gold_cap - 1));
static_assert(!eligible(0, unspent_gold_cap));
static_assert(!eligible(0, 1697));
static_assert(eligible(1, unspent_gold_cap));
static_assert(eligible(24, 1697));
} // namespace economy_policy
