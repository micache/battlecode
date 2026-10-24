#pragma once
#include <cambc.h>
#include "camp_rotation.h"
#include <algorithm>
#include <vector>

namespace group_farming {
// All knowledge is private to this instance. Hidden groups use static work and
// expiring cooldown observations, never hidden health or allied vision.
constexpr std::uint64_t planning_reserve = 42000;
constexpr unsigned observation_limit = 12, candidate_limit = 64;
constexpr float commitment_bonus = 1.25f;

constexpr float throughput(float value, float travel, float work, float risk) {
    return value / ((travel + work + 7.f) * (1.f + 2.f * risk));
}
static_assert(throughput(56, 2, 2, 0) > throughput(56, 2, 30, 0));
static_assert(throughput(56, 2, 2, 0) > throughput(56, 2, 2, 1));
static_assert(throughput(112, 2, 2, 0) > throughput(56, 2, 2, 0));

struct record {
    cambc::map::camp_group group;
    cambc::bitboard spawns;
    float hp = 0, damage = 0;
    camp_rotation::respawn_observation cooldown;
    int observed = -1;
    bool reward = false;
    int unreachable_until = 0;
    bool prepared = false;
};

class planner {
    std::vector<cambc::map::camp_group> layout;
    std::vector<record> groups;
    bool loaded = false;
    std::size_t cursor = 0, score_cursor = 0;
    int selected = -1;
    bool committed = false, building = false;
    std::size_t member_cursor = 0;

    void observe_one(record& r, const cambc::bitboard& visible, int now) {
        if (!r.prepared || (r.spawns & visible).is_empty()) return;
        const auto state = r.group.state();
        r.observed = now;
        r.reward = std::holds_alternative<cambc::map::camp_group_reward_available>(state);
        if (const auto* respawn = std::get_if<cambc::map::camp_group_respawning>(&state))
            r.cooldown.record(now, respawn->timer);
        else r.cooldown.clear();
    }

public:
    void reset_target() { selected = -1; committed = false; }
    void engage() { committed = true; }
    void update() {
        if (cambc::fuel_remaining() < planning_reserve) return;
        if (!loaded) { layout = cambc::map::camp_groups(); loaded = true; }
        // Bounded by members as well as fuel, including unusually large groups.
        // The prepared prefix is already playable while later groups are built.
        for (unsigned n = 0; (building || groups.size() < layout.size()) && n < 16
             && cambc::fuel_remaining() > 70000; ++n) {
            if (!building) {
                groups.push_back({layout[groups.size()], {}});
                building = true;
                member_cursor = 0;
            }
            auto& r = groups.back();
            const auto& camp = r.group.camps()[member_cursor++];
            r.spawns.set(camp.spawn_position());
            const auto stats = camp.base_stats();
            r.hp += stats.base_health;
            r.damage += stats.base_strength;
            if (member_cursor == r.group.camps().size()) {
                r.prepared = true;
                building = false;
            }
        }
        if (groups.empty()) return;
        const auto visible = cambc::vision::visible_tiles();
        const int now = cambc::round_number();
        if (selected >= 0) observe_one(groups[selected], visible, now);
        for (unsigned n = 0; n < observation_limit && n < groups.size()
             && cambc::fuel_remaining() > 58000; ++n) {
            auto& r = groups[cursor];
            cursor = (cursor + 1) % groups.size();
            observe_one(r, visible, now);
        }
    }

    // Current reward occupancy outranks starting another fight or a banking trip.
    const record* capture_here() {
        auto& me = cambc::self();
        const auto pos = me.position();
        const int now = cambc::round_number();
        for (const auto& r : groups)
            if (r.observed == now && r.reward && r.spawns.is_set(pos)) return &r;
        return nullptr;
    }

    const record* target() const {
        return selected < 0 ? nullptr : &groups[selected];
    }

    const record* choose() {
        if (groups.empty() || cambc::fuel_remaining() < planning_reserve) return target();
        auto& me = cambc::self();
        const auto pos = me.position();
        const int now = cambc::round_number();
        const auto allies = cambc::vision::champion_tiles(cambc::team::ally);
        auto others = allies; others.set(pos, false);
        // Once we have spent damage on a visible live group, finish it before
        // comparing new routes. Recovery and an unreachable approach can abort.
        if (committed && selected >= 0) {
            const auto& r = groups[selected];
            if (r.observed == now && !r.reward && !r.cooldown.excludes(now)) return &r;
        }
        const auto equipment = me.item_count();
        const bool jungle = equipment[cambc::item_type::jungle_emblem_of_strength] > 0;
        const float dps = std::max(1.f, me.strength()) * 1.125f
            * me.base_stats().camp_damage_multiplier;
        const bool splash = me.passive() == cambc::passive_type::splash_attack;
        auto terrain = cambc::map::walls() | cambc::map::holes() | cambc::map::altars()
            | cambc::map::spawn_region(cambc::team::enemy);
        cambc::bitboard root, visited;
        root.set(pos);
        cambc::distance_field distances;
        distances.compute(terrain, root, visited);
        const auto score = [&](int index) {
            const auto& r = groups[index];
            if (!r.prepared || r.unreachable_until > now || r.cooldown.excludes(now)) return 0.f;
            // An observed collector needs no duplicate body or reward split.
            if (r.observed == now && r.reward && !(r.spawns & others).is_empty()) return 0.f;
            int travel = cambc::distance_field::unreachable;
            unsigned members = 0;
            for (const auto& camp : r.group) {
                if (++members > 128) break; // approximate very large groups
                if (cambc::fuel_remaining() < planning_reserve) return 0.f;
                travel = std::min(travel, static_cast<int>(distances.get(camp.spawn_position())));
            }
            if (travel == cambc::distance_field::unreachable) return 0.f;
            const bool reward_now = r.reward && r.observed == now;
            float work = reward_now ? 0.f : r.hp / (dps * (splash && r.group.camps().size() > 1 ? 1.6f : 1.f));
            const float risk = reward_now ? 0.f : .55f * r.damage * work
                * (jungle ? .7f : 1.f) / std::max(1.f, me.health());
            const float gold_weight = me.strength() < 100.f ? 1.f : .3f;
            return throughput(8.f * r.group.gem_value() + gold_weight * r.group.gold_value(),
                              travel, work, risk);
        };
        int best = selected;
        float best_score = selected < 0 ? 0.f : score(selected) * commitment_bonus;
        for (unsigned n = 0; n < candidate_limit && n < groups.size()
             && cambc::fuel_remaining() > planning_reserve; ++n) {
            const int i = score_cursor;
            score_cursor = (score_cursor + 1) % groups.size();
            const float value = score(i);
            if (value > best_score) { best = i; best_score = value; }
        }
        const int previous = selected;
        selected = best_score > 0 ? best : -1;
        if (selected != previous) committed = false;
        return target();
    }

    void blocked() {
        if (selected >= 0) groups[selected].unreachable_until = cambc::round_number() + 6;
        reset_target();
    }
};
inline planner& memory() { static planner p; return p; }
} // namespace group_farming
