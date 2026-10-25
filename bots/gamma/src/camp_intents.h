#pragma once
#include <cstdint>

namespace intents {
// Protocol D: low four bits are version D; five 12-bit body records follow.
// Each record is (round mod 8):3, (draft route index + 1):9; zero releases.
// Only that body's immutable roster slot owns its record. A full eight-byte
// read/modify/write preserves peers and commits through ONE SDK write call.
inline constexpr int bodies = 5, max_routes = 509;
inline constexpr std::uint64_t version = 0xD;
constexpr bool compatible(std::uint64_t word) { return word == 0 || (word & 15) == version; }
constexpr unsigned record(std::uint64_t word, int slot) {
    return slot >= 0 && slot < bodies && (word & 15) == version
        ? (word >> (4 + 12*slot)) & 4095 : 0;
}
constexpr unsigned token(int route, int round) {
    return route >= 0 && route < max_routes ? ((round & 7) << 9) | (route + 1) : 0;
}
constexpr std::uint64_t replace(std::uint64_t word, int slot, unsigned value) {
    if (!compatible(word) || slot < 0 || slot >= bodies) return word;
    const int shift = 4 + 12*slot;
    return (word & ~(std::uint64_t{4095} << shift)) | version
        | (std::uint64_t{value & 4095} << shift);
}
struct Observation {
    int previous = -1, changed_at = -1;
    constexpr int target(unsigned value, int round) {
        if (previous != static_cast<int>(value)) { previous = value; changed_at = round; }
        const int route = (value & 511) - 1;
        // The local change clock prevents an abandoned record reviving every
        // eight rounds. An initially observed stale token can fool at most two
        // consecutive observations; hints never assert hidden position/state.
        const int age = (round - static_cast<int>(value >> 9)) & 7;
        return route >= 0 && route < max_routes && age <= 1
            && round - changed_at <= 1 ? route : -1;
    }
};
constexpr float score(float unclaimed, int peers) { return unclaimed / (1.0f + peers); }

static_assert(4 + 12*bodies == 64);
static_assert(token(508, 7) == (7 << 9) + 509 && token(509, 0) == 0);
static_assert(record(replace(0, 4, token(508, 7)), 4) == token(508, 7));
static_assert(replace(0xE, 0, 1) == 0xE && record(0xE, 0) == 0);
static_assert(replace(version, 5, 1) == version);
constexpr bool packet_regression() {
    std::uint64_t word = 0;
    for (int i = 0; i < bodies; ++i) word = replace(word, i, token(i*100, i));
    word = replace(word, 2, 0);
    for (int i = 0; i < bodies; ++i)
        if (record(word, i) != (i == 2 ? 0 : token(i*100, i))) return false;
    return (word & 15) == version;
}
constexpr bool expiry_regression() {
    Observation seen;
    const auto t = token(508, 7);
    if (seen.target(t, 7) != 508 || seen.target(t, 8) != 508
        || seen.target(t, 9) != -1 || seen.target(t, 15) != -1) return false;
    if (seen.target(token(508, 0), 16) != 508 || seen.target(0, 17) != -1) return false;
    Observation delayed;
    return delayed.target(token(1, 2), 4) == -1;
}
static_assert(packet_regression() && expiry_regression());
// Soft ownership still permits cooperation when a camp is much better.
static_assert(score(10, 1) < score(6, 0) && score(20, 1) > score(6, 0));
}
