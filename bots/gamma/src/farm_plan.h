#pragma once
#include <algorithm>
#include <cstddef>
#include <numeric>
#include <vector>

namespace farm_plan {
// Static estimates order work only; runtime visibility and exact scoring decide
// the destination. One rotating probe prevents permanent shortlist starvation.
inline constexpr std::vector<std::size_t> candidates(const std::vector<float>& ranks,
                                         int committed, std::size_t probe,
                                         std::size_t limit) {
    std::vector<std::size_t> order(ranks.size());
    std::iota(order.begin(), order.end(), 0);
    if (order.empty()) return order;
    probe %= order.size();
    const auto priority = [&](std::size_t i) {
        return static_cast<int>(i) == committed ? 0 : i == probe ? 1 : 2;
    };
    const auto count = std::min(limit, order.size());
    std::partial_sort(order.begin(), order.begin() + count, order.end(), [&](auto a, auto b) {
        if (priority(a) != priority(b)) return priority(a) < priority(b);
        return ranks[a] != ranks[b] ? ranks[a] < ranks[b] : a < b;
    });
    order.resize(count);
    return order;
}
// Compile-time regressions run against the actual scheduler, not a second model.
static_assert(candidates({}, -1, 0, 12).empty());
static_assert(candidates({3, 1, 2}, -1, 0, 0).empty());
static_assert(candidates({3, 1, 2}, 2, 0, 3) == std::vector<std::size_t>{2, 0, 1});
static_assert(candidates({1, 1, 1, 1}, -1, 9, 3) == std::vector<std::size_t>{1, 0, 2});
static_assert([] {
    for (std::size_t n = 1; n <= 16; ++n) {
        const std::vector<float> ranks(n, 1);
        for (std::size_t probe = 0; probe < n; ++probe) {
            const auto order = candidates(ranks, static_cast<int>(n - 1), probe, 3);
            if (order.size() != std::min(n, std::size_t{3}) || order[0] != n - 1) return false;
            if (std::find(order.begin(), order.end(), probe) == order.end()) return false;
            for (std::size_t a = 0; a < order.size(); ++a) {
                if (order[a] >= n) return false;
                for (std::size_t b = a + 1; b < order.size(); ++b)
                    if (order[a] == order[b]) return false;
            }
        }
    }
    return true;
}());
} // namespace farm_plan
