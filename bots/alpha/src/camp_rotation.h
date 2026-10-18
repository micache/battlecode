#pragma once
#include <cambc.h>
#include "camp_route_policy.h"
#include <algorithm>
#include <array>
#include <cstdint>
#include <vector>

namespace camp_rotation {

// Private to one champion instance. This is an expiring observation, not shared
// vision or a claim that a hidden group has respawned when the deadline passes.
struct respawn_observation {
    bool respawning = false;
    std::uint32_t observed_round = 0;
    std::uint32_t earliest_round = 0;

    constexpr void record(std::uint32_t now, int remaining) {
        respawning = true;
        observed_round = now;
        earliest_round = now + static_cast<std::uint32_t>(std::max(0, remaining));
    }
    constexpr void clear() { respawning = false; }
    constexpr bool excludes(std::uint32_t now) const {
        // A zero timer means occupancy blocks respawning NOW. Do not extrapolate
        // that occupancy into the next round, even if the group becomes hidden.
        return respawning && (now == observed_round || now < earliest_round);
    }
};

// Stable temporal contracts compiled by the trusted wrapper, without engine calls.
static_assert([] {
    respawn_observation observation;
    if (observation.excludes(10)) return false; // unknown groups remain eligible
    observation.record(10, 3);
    if (!observation.excludes(10) || !observation.excludes(12)
        || observation.excludes(13)) return false; // exact expiry
    observation.clear();
    if (observation.excludes(11)) return false; // fresh alive/reward overrides
    observation.record(20, 0);
    if (!observation.excludes(20) || observation.excludes(21)) return false;
    observation.record(30, 5);
    observation.record(32, 1); // latest observation replaces the previous deadline
    return observation.excludes(32) && !observation.excludes(33);
}());

constexpr std::uint64_t observation_fuel_reserve = 45000;
constexpr unsigned observation_limit = 16;

struct tracked_group {
    cambc::map::camp_group group;
    cambc::bitboard spawns;
    respawn_observation cooldown;
    float initial_health = 0;
    bool reward = false;
    bool observed = false;
    std::uint32_t observed_round = 0;
};

// One turn plan: focus identity is immutable spawn geometry, not live state.
struct farm_plan {
    cambc::bitboard goals;
    cambc::bitboard member_spawns;
    bool focused = false;
    bool holding_capture = false;
};

class rotation {
    std::vector<tracked_group> groups;
    std::size_t cursor = 0;
    int committed_group = -1;

    void initialise() {
        if (!groups.empty()) return;
        // Cache only immutable identities/geometry; live state is never cached
        // by the SDK map object itself. No per-turn map-layout reconstruction.
        std::array<float, 5> design_health{};
        for (const auto& group : cambc::map::camp_groups()) {
            float health = 0;
            for (const auto& camp : group.camps()) {
                auto& design = design_health[static_cast<unsigned>(camp.kind())];
                if (design == 0) design = camp.base_stats().base_health;
                health += design;
            }
            groups.push_back({group, group.spawn_tiles(), {}, health});
        }
    }

    // Caller must establish fresh personal spawn visibility before querying.
    void observe_group(tracked_group& entry, std::uint32_t now) {
        const auto state = entry.group.state();
        entry.observed = true;
        entry.observed_round = now;
        entry.reward = std::holds_alternative<cambc::map::camp_group_reward_available>(state);
        if (const auto* respawn = std::get_if<cambc::map::camp_group_respawning>(&state))
            entry.cooldown.record(now, respawn->timer);
        else
            entry.cooldown.clear();
    }

    cambc::bitboard eligible_goals(std::uint32_t now) const {
        cambc::bitboard result;
        result.clear();
        for (const auto& entry : groups)
            if (!entry.cooldown.excludes(now)) result |= entry.spawns;
        return result;
    }

public:
    void observe() {
        if (cambc::fuel_remaining() < observation_fuel_reserve) return;
        initialise();
        const auto visible = cambc::vision::visible_tiles();
        const auto now = cambc::round_number();
        unsigned queried = 0;
        // Rotate the scan start so the cap cannot permanently starve later IDs.
        for (std::size_t scanned = 0; scanned < groups.size(); ++scanned) {
            if (queried >= observation_limit
                || cambc::fuel_remaining() < observation_fuel_reserve) break;
            auto& entry = groups[cursor];
            cursor = (cursor + 1) % groups.size();
            if ((entry.spawns & visible).is_empty()) continue;
            ++queried;
            observe_group(entry, now);
        }
    }

    cambc::bitboard goals() {
        observe();
        return eligible_goals(cambc::round_number());
    }

    // Choose work before camp combat, so a nearby low-return camp cannot preempt
    // the selected objective. Low fuel retains the original unfocused policy.
    // No shared memory: the commitment is private and is revalidated every turn.
    farm_plan plan(const cambc::bitboard& blocked) {
        observe();
        const auto now = cambc::round_number();
        auto& me = cambc::self();
        const auto position = me.position();
        const auto visible = cambc::vision::visible_tiles();
        // Preserve an ongoing capture. Self is visible even if the scan cap did
        // not reach this group. Do not divert a collector based on route scores.
        for (auto& entry : groups) {
            if (!entry.spawns.is_set(position)) continue;
            if (!(entry.spawns & visible).is_empty()) observe_group(entry, now);
            if (entry.reward) return {entry.spawns, entry.spawns, true, true};
        }
        constexpr std::uint64_t route_start_reserve = 65000;
        if (cambc::fuel_remaining() < route_start_reserve) return {eligible_goals(now), {}, false, false};

        struct candidate { std::size_t index; float estimate; };
        std::vector<candidate> candidates;
        candidates.reserve(route_candidate_limit + 1);
        const float strength = me.strength();
        const int speed = std::max(1, me.base_stats().base_move_speed);
        const auto capture = cambc::constants::capture_time;
        for (std::size_t i = 0; i < groups.size(); ++i) {
            if (cambc::fuel_remaining() < observation_fuel_reserve) break;
            const auto& entry = groups[i];
            if (entry.cooldown.excludes(now) || entry.group.camps().size() > route_member_limit) continue;
            int near = 100000;
            for (const auto& camp : entry.group.camps())
                near = std::min(near, int(position.chebyshev_distance(camp.spawn_position())));
            const bool reward = entry.observed && entry.observed_round == now && entry.reward;
            float estimate = route_cost(float(near) / speed, reward ? 0 : entry.initial_health,
                strength, entry.group.gem_value(), entry.group.gold_value(), capture);
            if (int(i) == committed_group) estimate *= commitment_discount;
            const auto insertion = std::find_if(candidates.begin(), candidates.end(),
                [&](const candidate& c) { return estimate < c.estimate; });
            candidates.insert(insertion, {i, estimate});
            if (candidates.size() > route_candidate_limit) candidates.pop_back();
        }
        // Static full-health estimates can hide nearly finished work. Always
        // re-evaluate our previous group with fresh visibility before switching.
        if (committed_group >= 0 && std::size_t(committed_group) < groups.size()) {
            const auto& entry = groups[committed_group];
            const bool listed = std::any_of(candidates.begin(), candidates.end(),
                [&](const auto& c) { return int(c.index) == committed_group; });
            if (!listed && !entry.cooldown.excludes(now)
                && entry.group.camps().size() <= route_member_limit) {
                if (candidates.size() == route_candidate_limit) candidates.pop_back();
                candidates.push_back({std::size_t(committed_group), 0});
            }
        }
        if (candidates.empty() || cambc::fuel_remaining() < observation_fuel_reserve) return {eligible_goals(now), {}, false, false};

        // One native forward field serves all candidates, not one search each.
        cambc::bitboard origin;
        origin.clear(); origin.set(position);
        cambc::bitboard visited;
        cambc::distance_field travel;
        travel.compute(blocked, origin, visited);
        cambc::bitboard selected_goals;
        selected_goals.clear();
        float best = 1.0e30f;
        int selected = -1;
        for (const auto& candidate : candidates) {
            if (cambc::fuel_remaining() < observation_fuel_reserve) break;
            auto& entry = groups[candidate.index];
            const bool seen = !(entry.spawns & visible).is_empty();
            if (seen && (!entry.observed || entry.observed_round != now)) observe_group(entry, now);
            if (entry.cooldown.excludes(now)) continue;
            const bool reward = seen && entry.observed_round == now && entry.reward;
            cambc::bitboard goals;
            goals.clear();
            float health = 0;
            bool complete = true;
            if (reward) goals = entry.spawns;
            else for (const auto& camp : entry.group.camps()) {
                if (cambc::fuel_remaining() < observation_fuel_reserve) { complete = false; break; }
                if (camp.is_visible()) {
                    const float hp = camp.health();
                    if (hp <= 0) continue;
                    health += hp;
                    cambc::bitboard approach;
                    approach.clear();
                    approach.draw_chebyshev(camp.position(), me.attack_range());
                    goals |= approach;
                } else if (!visible.is_set(camp.spawn_position())) {
                    // Unknown members get a design estimate, never hidden live
                    // state. Enter an unseen spawn to reveal it, not a blind ring.
                    health += camp.base_stats().base_health;
                    goals.set(camp.spawn_position());
                }
            }
            if (!complete) break;
            goals &= ~blocked;
            unsigned steps = cambc::distance_field::unreachable;
            for (const auto tile : goals.positions()) {
                if (cambc::fuel_remaining() < observation_fuel_reserve) { complete = false; break; }
                steps = std::min(steps, unsigned(travel.get(tile)));
            }
            if (!complete) break;
            if (steps == cambc::distance_field::unreachable) continue;
            float score = route_cost(float(steps) / speed, health, strength,
                entry.group.gem_value(), entry.group.gold_value(), capture);
            if (int(candidate.index) == committed_group) score *= commitment_discount;
            if (score < best) {
                best = score; selected = int(candidate.index); selected_goals = std::move(goals);
            }
        }
        if (selected < 0) return {eligible_goals(now), {}, false, false};
        committed_group = selected;
        return {selected_goals, groups[selected].spawns, true, false};
    }
};

// Each WASM champion has its own process/private persistent state. No team bytes.
inline rotation& memory() {
    static rotation instance;
    return instance;
}

} // namespace camp_rotation
