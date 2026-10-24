// Champion decisions. main.cpp dispatches here after the draft.
#include <cambc.h>
#include "bot.h"
#include "altar_control.h"
#include "group_farming.h"
#include <array>
#include <iostream>
#include "random.h"
#include <cstdint>
#include <span>
#include <algorithm>
#include <optional>
#include <type_traits>
#include <variant>

using cambc::vec2;
using cambc::team;

int distance(vec2 a, vec2 b) {
    return static_cast<int>(a.chebyshev_distance(b));
}

cambc::bitboard tiles_around(vec2 position, int radius) {
    cambc::bitboard tiles;
    tiles.clear();
    tiles.draw_chebyshev(position, radius);
    return tiles;
}

// Combine terrain and visible occupants using native bitboard operations.
cambc::bitboard blocked_tiles() {
    auto blocked = cambc::map::walls() | cambc::map::holes() | cambc::map::altars()
        | cambc::map::spawn_region(team::enemy) | cambc::vision::champion_tiles()
        | cambc::vision::camp_tiles() | cambc::vision::teleport_tiles();
    blocked.set(cambc::self().position(), false);
    return blocked;
}

bool move_towards_closest(cambc::bitboard goals) {
    auto& me = cambc::self();
    if (!me.can_move() || me.restrictions().contains(cambc::buff_restrictions::move)
        || goals.is_set(me.position()) || cambc::fuel_remaining() < 22000) return false;
    // Goals are free approach/capture tiles, never occupied monster/altar tiles.
    auto blocked = blocked_tiles();
    goals &= ~blocked;
    if (goals.is_empty()) return false;
    cambc::distance_field field;
    cambc::bitboard visited;
    field.compute_to(blocked, goals, tiles_around(me.position(), 0), visited);
    for (unsigned retry = 0; retry < 2; ++retry) {
        auto step = me.position();
        for (auto tile : blocked.reachable_tiles(step, me.base_stats().base_move_speed).positions())
            if (field.get(tile) < field.get(step)) step = tile;
        if (step == me.position()) return false;
        if (me.move_absolute(step)) { altar_control::place_lock(); return true; }
        // False may reveal an occupant. Refresh before the bounded alternative.
        blocked = blocked_tiles();
        if (cambc::fuel_remaining() < 22000) break;
    }
    return false;
}

void Bot::buy_items() {
    auto& me = cambc::self();
    using I = cambc::item_type;
    const auto items = me.item_count();
    if (!items[I::jungle_emblem_of_strength]) {
        const unsigned needed = 5 - std::min(5u, items[I::jungle_shard_of_strength]);
        const unsigned count = std::min(needed, me.gold_count() / I::jungle_shard_of_strength.cost());
        if (count && me.can_buy(I::jungle_shard_of_strength, count)) me.buy(I::jungle_shard_of_strength, count);
    }
    const unsigned count = me.gold_count() / I::power_shard_of_strength.cost();
    // Finish Jungle before starting a second family.
    if (me.item_count()[I::jungle_emblem_of_strength] && count && me.can_buy(I::power_shard_of_strength, count))
        me.buy(I::power_shard_of_strength, count);
}

// Bound extra combat work; this is a planning reserve, not measured fuel headroom.
constexpr std::uint64_t combat_fuel_reserve = 18000;
constexpr unsigned combat_target_limit = 16;

// Turn-local group filter. Reset before any champion combat or new target choice.
std::optional<cambc::bitboard> farming_tiles;

// Handles are refreshed through vision on every action, never cached across turns.
template<class Target>
auto combat_targets() {
    if constexpr (std::is_same_v<Target, cambc::camp>) {
        auto camps = cambc::vision::camps();
        if (farming_tiles) std::erase_if(camps, [](const auto& c) {
            return !farming_tiles->is_set(c.spawn_position());
        });
        return camps;
    }
    else
        return cambc::vision::champions(team::enemy);
}

template<class Target>
std::optional<Target> basic_target() {
    auto& me = cambc::self();
    if (!me.is_alive() || !me.can_attack()
        || me.restrictions().contains(cambc::buff_restrictions::attack))
        return std::nullopt;
    const auto range = me.attack_tiles();
    unsigned examined = 0;
    for (const auto& target : combat_targets<Target>()) {
        if (++examined > combat_target_limit || cambc::fuel_remaining() < combat_fuel_reserve)
            break;
        if (target.is_visible() && target.health() > 0 && range.is_set(target.position()))
            return target;
    }
    return std::nullopt;
}

bool cast_ready(const cambc::ability& ability, bool walked) {
    if (!ability.info() || !ability.is_ready()
        || cambc::self().restrictions().contains(cambc::buff_restrictions::cast))
        return false;
    // is_ready() checks cooldown/can_cast, but not the movement exclusion.
    return !walked || !std::visit([](const auto& info) {
        return info.exclusive_with_movement;
    }, *ability.info());
}

// Spend the separate basic and cast allowances. Never walk after this routine
// acts: a spell may exclude movement even when can_move() still reports true.
template<class Target>
bool fight(bool walked = false) {
    auto& me = cambc::self();
    bool acted = false;
    if (const auto target = basic_target<Target>()) {
        me.attack(*target);
        acted = true;
    }
    if (!me.is_alive() || !me.can_cast()
        || cambc::fuel_remaining() < combat_fuel_reserve)
        return acted;

    // At most two slots and sixteen visible aim points per slot; no tile search.
    // Compare useful direct damage against the additional basic from a reset.
    std::optional<cambc::ability> selected;
    std::optional<Target> selected_target;
    float best_score = 0;
    const auto abilities = me.abilities();
    for (const auto& ability : abilities) {
        if (cambc::fuel_remaining() < combat_fuel_reserve || !cast_ready(ability, walked))
            continue;
        if (ability.is_attack_reset()) {
            // Resets have no range; only spend one when a new basic is possible.
            if (me.can_attack() || me.restrictions().contains(cambc::buff_restrictions::attack))
                continue;
            const auto range = me.attack_tiles();
            unsigned examined = 0;
            for (const auto& target : combat_targets<Target>()) {
                if (++examined > combat_target_limit || cambc::fuel_remaining() < combat_fuel_reserve)
                    break;
                if (!target.is_visible() || target.health() <= 0 || !range.is_set(target.position()))
                    continue;
                const float score = std::min(me.strength(), target.health());
                if (score > best_score) {
                    best_score = score;
                    selected = ability;
                    selected_target = target;
                }
                break; // Match the first-target basic policy used after the reset.
            }
            continue;
        }
        const bool ground = ability.is_aoe_damage() && ability.can_target_ground();
        const bool unit = (ability.is_damage() || ability.is_cc()) &&
            (std::is_same_v<Target, cambc::camp> ? ability.can_target_camps() : ability.can_target_enemies());
        if (!ground && !unit)
            continue;
        const auto range = ability.valid_tiles();
        const float damage = ability.damage_amount();
        unsigned examined = 0;
        for (const auto& target : combat_targets<Target>()) {
            if (++examined > combat_target_limit || cambc::fuel_remaining() < combat_fuel_reserve)
                break;
            if (!target.is_visible() || target.health() <= 0 || !range.is_set(target.position()))
                continue;
            // Ground spells aim at a visible enemy/camp, not unexplored terrain.
            // Only the primary damage is scored: splash is a conservative bonus.
            float score = std::min(damage, target.health());
            if constexpr (!std::is_same_v<Target, cambc::camp>) {
                const bool control = ability.is_cc() ||
                    (ground && ability.get<cambc::ability_aoe_damage>().duration > 0);
                if (control) score += 20; // prefer actual crowd control in PvP
            }
            if (score > best_score) {
                best_score = score;
                selected = ability;
                selected_target = target;
            }
        }
    }
    if (selected && selected_target && me.is_alive() && cast_ready(*selected, walked)
        && selected_target->is_visible() && selected_target->health() > 0) {
        bool cast = false;
        if (selected->is_attack_reset())
            cast = selected->use();
        else if (selected->is_aoe_damage())
            cast = selected->use(selected_target->position());
        else
            cast = selected->use(*selected_target);
        if (cast) {
            acted = true;
            // Refresh after the cast: a kill, splash or retaliation changes targets.
            if (const auto next = basic_target<Target>()) me.attack(*next);
        }
    }

    // Use defensive kits when no damage/reset cast was chosen. No speculative dash.
    if (acted && me.is_alive() && me.can_cast()) {
        for (const auto& ability : abilities) {
            if (cambc::fuel_remaining() < combat_fuel_reserve || !cast_ready(ability, walked))
                continue;
            if (ability.is_shield() && ability.can_target_self()
                && me.health() < me.max_health() * 0.75f) {
                if (ability.use()) break;
            }
            if (ability.is_heal() && ability.can_target_allies()) {
                const auto range = ability.valid_tiles();
                unsigned examined = 0;
                for (const auto& ally : cambc::vision::champions(team::ally)) {
                    if (++examined > combat_target_limit || cambc::fuel_remaining() < combat_fuel_reserve)
                        break;
                    if (ally == me || !ally.is_visible() || !ally.is_alive()
                        || !range.is_set(ally.position())) continue;
                    if (ally.max_health() - ally.health() < ability.heal_amount() * 0.5f)
                        continue;
                    if (ability.use(ally)) break;
                }
            }
        }
    }
    return acted;
}

// Finish one selected physical group, then occupy its reward region.
void farm_camps() {
    auto& plan = group_farming::memory();
    const auto* target = plan.choose();
    if (!target || cambc::fuel_remaining() < combat_fuel_reserve) return;
    farming_tiles = target->spawns;
    if (target->observed == static_cast<int>(cambc::round_number()) && target->reward) {
        if (!target->spawns.is_set(cambc::self().position())) move_towards_closest(target->spawns);
        return; // Preserve capture occupancy through round start.
    }
    if (fight<cambc::camp>()) { plan.engage(); return; }
    if (cambc::fuel_remaining() < 28000) return;
    auto& me = cambc::self();
    const auto visible = cambc::vision::visible_tiles();
    const auto occupied = cambc::vision::camp_tiles();
    cambc::bitboard goals;
    unsigned examined = 0;
    for (const auto& camp : target->group) {
        if (++examined > 128 || cambc::fuel_remaining() < 26000) break;
        const auto spawn = camp.spawn_position();
        if (!visible.is_set(spawn)) goals.set(spawn); // Explore, no live query.
        else if (occupied.is_set(spawn)) goals |= tiles_around(spawn, me.attack_range());
    }
    if (goals.is_empty()) {
        // Fresh lifecycle after a kill by us or an ally. state() is visibility-gated.
        if (!(target->spawns & visible).is_empty()
            && std::holds_alternative<cambc::map::camp_group_reward_available>(target->group.state()))
            move_towards_closest(target->spawns);
        else plan.blocked();
        return;
    }
    if (move_towards_closest(goals)) {
        if (fight<cambc::camp>(true)) plan.engage();
    }
    else if (!goals.is_set(me.position())) plan.blocked();
}

void Bot::play_turn() {
    auto& me = cambc::self();
    auto& plan = group_farming::memory();
    farming_tiles.reset();
    if (!me.is_alive()) {
        recovering = false;
        plan.reset_target();
        altar_control::buy_lock();
        buy_items();
        return;
    }
    if (me.is_recalling() || me.is_submitting_gems() || me.is_teleporting()) return;
    if (!me.can_move() && !me.can_attack() && !me.can_cast()) return;
    const auto spawn = cambc::map::spawn_region(team::ally);
    const bool at_spawn = spawn.is_set(me.position());
    if (at_spawn || me.passive() == cambc::passive_type::remote_shop) buy_items();
    if (at_spawn) {
        altar_control::buy_lock();
        // Recall resolves before this turn; healing only happens at its end.
        if (me.health() < me.max_health() * .95f) return;
        recovering = false;
    }
    altar_control::place_lock();
    if (!at_spawn && me.health() < me.max_health() * .35f) recovering = true;
    if (recovering) {
        plan.reset_target();
        move_towards_closest(spawn);
        if (!spawn.is_set(me.position())) me.recall();
        return;
    }
    plan.update();
    if (plan.capture_here()) return;
    // Adjacent tribute wins over incidental combat. Hostile locks use basics.
    if (me.gem_count() && altar_control::bank_or_clear_lock()) return;
    if (fight<cambc::champion>() || cambc::fuel_remaining() < combat_fuel_reserve) return;
    // Keep safe, prompt banking. Route selection is the experiment's core change.
    if (me.gem_count()) {
        cambc::bitboard goals, locked_goals;
        const auto hostile = cambc::vision::altar_lock_tiles(team::enemy);
        for (auto altar : cambc::map::altars().positions()) {
            const auto approach = tiles_around(altar, cambc::constants::submit_gems_range);
            if (hostile.is_set(altar)) locked_goals |= approach;
            else goals |= approach;
        }
        if (goals.is_empty()) goals = locked_goals;
        move_towards_closest(goals);
        // Fresh postmove range/lock state: begin tribute without an idle turn.
        if (cambc::fuel_remaining() >= combat_fuel_reserve) altar_control::bank_or_clear_lock();
        return;
    }
    // Turn earned gold into clear speed; Tavi already shops remotely.
    if (!at_spawn && me.passive() != cambc::passive_type::remote_shop && me.gold_count() >= 150
        && cambc::vision::champion_tiles(team::enemy).is_empty()
        && cambc::vision::awake_camp_tiles().is_empty()) {
        plan.reset_target();
        me.recall();
        return;
    }
    farm_camps();
}
