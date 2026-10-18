#pragma once
#include <cambc.h>
#include <array>
#include <cstdint>

namespace camp_claims {
// Protocol v1: byte 0 = 0xD1, bytes 1..6 = individual body intents, byte 7 unused.
// Body slots are sorted immutable ally handles, including BOTH Cassi/Issac bodies.
// Only that body writes its byte. One SDK byte write publishes the complete token:
// low 6 bits = sorted camp-group index + 1 (0 releases), high 2 = round modulo 4.
// Claims communicate intent only, never position, camp state or shared vision.
constexpr std::uint8_t version = 0xD1;
constexpr unsigned max_bodies = 6;
constexpr unsigned max_groups = 63;
constexpr float duplicate_penalty = 1.5f;

constexpr std::uint8_t encode(unsigned group, unsigned round) {
    return group < max_groups ? static_cast<std::uint8_t>((group + 1) | ((round & 3) << 6)) : 0;
}
constexpr int decode(std::uint8_t token) { return int(token & 63) - 1; }

struct observation {
    std::uint8_t token = 0;
    unsigned changed_round = 0;
    bool seen = false;

    constexpr void update(std::uint8_t value, unsigned now) {
        if (!seen || token != value) changed_round = now;
        token = value;
        seen = true;
    }
    constexpr bool fresh(unsigned now) const {
        // Both a short modulo age and a PRIVATE nonwrapping change deadline are
        // required. An abandoned byte cannot revive every fourth round. A newly
        // observed abandoned token can look fresh for at most two observations.
        return seen && decode(token) >= 0 && now - changed_round <= 1
            && ((now - (token >> 6)) & 3) <= 1;
    }
};

// Temporal regressions compile with the real policy, not a reimplemented model.
static_assert([] {
    for (unsigned group = 0; group < max_groups; ++group)
        for (unsigned now = 0; now < 12; ++now) {
            observation o;
            const auto token = encode(group, now);
            if (decode(token) != int(group)) return false;
            o.update(token, now);
            if (!o.fresh(now) || !o.fresh(now + 1)) return false;
            for (unsigned later = now + 2; later < now + 12; ++later) {
                o.update(token, later);
                if (o.fresh(later)) return false; // no modulo resurrection
            }
            o.update(encode(group, now + 12), now + 12);
            // Same byte after a skipped whole cycle is safely still expired.
            if (o.fresh(now + 12)) return false;
            o.update(encode(group, now + 13), now + 13);
            if (!o.fresh(now + 13)) return false; // changed heartbeat revives
            o.update(0, now + 14);
            if (o.fresh(now + 14) || decode(o.token) != -1) return false;
        }
    return encode(max_groups, 0) == 0;
}());

class board {
    bool initialized = false;
    bool enabled = false;
    int own_slot = -1;
    std::array<observation, max_bodies> peers{};

    void initialize() {
        initialized = true;
        if (cambc::shared_memory.size() != 8) return;
        const auto allies = cambc::champions(cambc::team::ally);
        if (allies.empty() || allies.size() > max_bodies) return;
        const auto mine = static_cast<cambc::handle_champion_t>(cambc::self());
        unsigned rank = 0;
        bool found = false;
        for (const auto& ally : allies) {
            const auto handle = static_cast<cambc::handle_champion_t>(ally);
            if (handle == mine) found = true;
            if (handle < mine) ++rank;
        }
        if (found) own_slot = static_cast<int>(rank);
    }

public:
    void begin_turn() {
        if (!initialized) initialize();
        enabled = false;
        if (own_slot < 0) return;
        auto header = static_cast<std::uint8_t>(cambc::shared_memory[0]);
        // Idempotent initialization, with no per-body data in the version byte.
        // Unknown versions are left untouched and use independent farming.
        if (header == 0) cambc::shared_memory[0] = version;
        else if (header != version) return;
        enabled = true;
        release(); // Dead/banking/recovering/stunned/channeling bodies release too.
        std::array<std::uint8_t, max_bodies> tokens{};
        cambc::shared_memory.read(1, std::span{tokens});
        const auto now = cambc::round_number();
        for (unsigned i = 0; i < max_bodies; ++i) peers[i].update(tokens[i], now);
    }

    void release() const {
        if (enabled) cambc::shared_memory[1 + own_slot] = std::uint8_t{0};
    }
    void publish(unsigned group, unsigned groups) const {
        if (enabled && groups <= max_groups)
            cambc::shared_memory[1 + own_slot] = encode(group, cambc::round_number());
    }
    unsigned others(unsigned group, unsigned groups) const {
        if (!enabled || groups > max_groups) return 0;
        unsigned count = 0;
        for (unsigned i = 0; i < max_bodies; ++i)
            if (int(i) != own_slot && peers[i].fresh(cambc::round_number())
                && decode(peers[i].token) == int(group)) ++count;
        return count;
    }
};
} // namespace camp_claims
