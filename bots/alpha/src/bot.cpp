// Champion decisions. main.cpp dispatches here after the draft.
#include <cambc.h>
#include "bot.h"
#include "altar_control.h"
#include "camp_rotation.h"
#include "camp_pull.h"
#include "equipment_policy.h"
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
    if (!me.can_move() || goals.is_set(me.position()))
        return false;

    // Only free goals or occupied camp tiles can seed the field.
    const auto blocked = blocked_tiles();
    goals &= ~blocked | cambc::vision::camp_tiles();
    if (goals.is_empty())
        return false;
    if (goals.count() == 1 && !blocked.is_set(goals.positions()[0])) {
        const bool moved = me.move_towards(goals.positions()[0]);
        if (moved) altar_control::place_lock();
        return moved;
    }

    // Expand from the goals until our current tile is reached.
    const auto path_walls = blocked & ~goals;
    cambc::distance_field field;
    cambc::bitboard visited;
    field.compute_to(path_walls, goals, tiles_around(me.position(), 0), visited);

    // Choose a reachable step with a smaller distance to the goal.
    auto step = me.position();
    for (auto tile : blocked.reachable_tiles(step, me.base_stats().base_move_speed).positions())
        if (field.get(tile) < field.get(step)) step = tile;

    const bool moved = step != me.position() && me.move_absolute(step);
    if (moved) altar_control::place_lock();
    return moved;
}

void Bot::buy_items() {
    auto& me = cambc::self();
    const std::array items{cambc::item_type::power_shard_of_strength,
        cambc::item_type::power_shard_of_focus, cambc::item_type::power_shard_of_health};
    const auto cost = items[0].cost();
    if (!cost || me.gold_count() < cost || cambc::fuel_remaining() < equipment_policy::entry_fuel_reserve) return;
    const auto stats = me.base_stats();
    equipment_policy::model estimate{me.max_health(), me.strength(), me.focus(),
        {stats.strength_growth, stats.focus_growth, stats.health_growth}};
    const auto passive = me.passive();
    if (passive == cambc::passive_type::health_strength)
        estimate.health_to_strength = cambc::constants::passive_abilities::ryth_health_strength_ratio;
    if (passive == cambc::passive_type::splash_attack)
        estimate.basic_rate = equipment_policy::area_targets;
    if (passive == cambc::passive_type::retaliation)
        estimate.focus_rate = cambc::constants::passive_abilities::ren_retaliation_focus_ratio; // one incoming basic/round, uncertain workload
    for (const auto& ability : me.abilities()) {
        if (!ability.info()) continue;
        std::visit([&](const auto& info) {
            using T = std::decay_t<decltype(info)>;
            const float cooldown = static_cast<float>(std::max(1, info.max_cooldown));
            if constexpr (std::is_same_v<T, cambc::ability_attack_reset>)
                estimate.basic_rate += estimate.basic_rate / cooldown;
            if constexpr (std::is_same_v<T, cambc::ability_damage>
                          || std::is_same_v<T, cambc::ability_cc>) {
                if (ability.can_target_camps()) estimate.focus_rate += info.modifier / cooldown;
            }
            if constexpr (std::is_same_v<T, cambc::ability_aoe_damage>)
                estimate.focus_rate += equipment_policy::area_targets * info.modifier / cooldown;
            if constexpr (std::is_same_v<T, cambc::ability_shield>) {
                if (ability.can_target_self())
                    estimate.shield_scale = equipment_policy::shield_credit * info.modifier;
            }
            // Do not price unused dash damage or another champion's healing.
        }, *ability.info());
    }
    const auto inventory = me.item_count();
    const std::array<unsigned, 3> residues{inventory[items[0]], inventory[items[1]], inventory[items[2]]};
    const auto counts = equipment_policy::plan(estimate, me.gold_count() / cost,
        residues, items[0].combine_count(), static_cast<unsigned>(chosen_stat));
    for (unsigned stat = 0; stat < items.size(); ++stat) {
        if (cambc::fuel_remaining() < equipment_policy::purchase_fuel_reserve) break;
        if (counts[stat] && me.can_buy(items[stat], counts[stat])) me.buy(items[stat], counts[stat]);
    }
}

// Bound extra combat work; this is a planning reserve, not measured fuel headroom.
constexpr std::uint64_t combat_fuel_reserve = 18000;
constexpr unsigned combat_target_limit = 16;

// Handles are refreshed through vision on every action, never cached across turns.
template<class Target>
auto combat_targets() {
    if constexpr (std::is_same_v<Target, cambc::camp>)
        return cambc::vision::camps();
    else
        return cambc::vision::champions(team::enemy);
}

template<class Target>
std::optional<Target> basic_target(const cambc::bitboard* excluded = nullptr) {
    auto& me = cambc::self();
    if (!me.is_alive() || !me.can_attack()
        || me.restrictions().contains(cambc::buff_restrictions::attack))
        return std::nullopt;
    const auto range = me.attack_tiles();
    unsigned examined = 0;
    for (const auto& target : combat_targets<Target>()) {
        if (++examined > combat_target_limit || cambc::fuel_remaining() < combat_fuel_reserve)
            break;
        if constexpr (std::is_same_v<Target, cambc::camp>) {
            if (!target.is_visible() || !camp_pull::permits(target, excluded,
                me.passive() == cambc::passive_type::splash_attack ? 1.f : 0.f)) continue;
        }
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
bool fight(bool walked = false, const cambc::bitboard* excluded = nullptr) {
    auto& me = cambc::self();
    bool acted = false;
    if (const auto target = basic_target<Target>(excluded)) {
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
                if constexpr (std::is_same_v<Target, cambc::camp>) {
                    if (!camp_pull::permits(target, excluded,
                        me.passive() == cambc::passive_type::splash_attack ? 1.f : 0.f)) continue;
                }
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
            if constexpr (std::is_same_v<Target, cambc::camp>) {
                if (!camp_pull::permits(target, excluded,
                    ground ? ability.get<cambc::ability_aoe_damage>().radius : 0.f)) continue;
            }
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
            if (const auto next = basic_target<Target>(excluded)) me.attack(*next);
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

// Attack a camp already in range, otherwise move toward the nearest camp tiles.
void farm_camps() {
    // Include unknown/expired groups, but do not revisit a personally observed
    // cooldown early merely because its spawn tiles have left our vision.
    auto goals = camp_rotation::memory().goals();
    auto excluded = camp_pull::assess(goals);
    if (fight<cambc::camp>(false, &excluded) || cambc::fuel_remaining() < combat_fuel_reserve)
        return;
    goals &= ~excluded;

    // Fresh vision after movement may reveal a camp already in range.
    if (move_towards_closest(goals)) {
        excluded = camp_pull::assess(goals);
        fight<cambc::camp>(true, &excluded);
    }
}

void Bot::play_turn() {
    // Retain the base RNG draw as a deterministic tie preference, not a stat lock.
    if (chosen_stat < 0) {
        chosen_stat = random_number(3);
        std::cout << "draft: " << std::string(reinterpret_cast<const char*>(cambc::draft_memory.data()), 11) << '\n';
    }

    // Read before writing: little-endian u32 at shared-memory byte offset zero.
    std::uint32_t round = 0;
    cambc::shared_memory.read(0, std::span{&round, 1});
    std::cout << "shared round: " << round << '\n';
    round = cambc::round_number();
    cambc::shared_memory.write(0, std::span{&round, 1});

    auto& me = cambc::self();

    // Refill control tools while dead so the next sortie can deny an altar.
    if (!me.is_alive()) {
        altar_control::buy_lock();
        return;
    }

    // Leave channels running and skip turns where we cannot act.
    if (me.is_recalling() || me.is_submitting_gems() || me.is_teleporting()
        || (!me.can_move() && !me.can_attack() && !me.can_cast()))
        return;

    // Shop before leaving spawn.
    const bool at_spawn = cambc::map::spawn_region(team::ally).is_set(me.position());
    if (at_spawn) {
        // Ten gold buys persistent denial; remaining gold follows the base build.
        altar_control::buy_lock();
        buy_items();
        // Spawn Health purchases heal their increment immediately; remain for
        // turn-end recovery of any earlier injury. Defend without leaving spawn.
        if (me.health() < me.max_health()) {
            fight<cambc::champion>();
            return;
        }
    }

    altar_control::place_lock();

    // Retreat before recall so repeated damage interruptions still allow progress.
    if (!at_spawn && me.health() < me.max_health() * 0.35f) {
        const auto spawn = cambc::map::spawn_region(team::ally);
        move_towards_closest(spawn);
        // Arrival by walking can heal at turn end without starting a channel.
        if (!spawn.is_set(me.position()))
            me.recall();
        return;
    }

    // Keep the enemy-first policy, spending independent combat allowances.
    if (fight<cambc::champion>() || cambc::fuel_remaining() < combat_fuel_reserve)
        return;

    // Bank any carried gems before farming.
    if (me.gem_count() > 0) {
        // Capture resolves before this turn: remember the newly cooling group
        // before leaving it with the reward. No movement or channel is started.
        camp_rotation::memory().observe();
        if (altar_control::bank_or_clear_lock()) return;
        if (cambc::fuel_remaining() < combat_fuel_reserve) return;
        // Union all altar approach tiles: the field chooses the nearest reachable altar.
        cambc::bitboard goals;
        goals.clear();
        cambc::bitboard locked_goals;
        locked_goals.clear();
        const auto hostile = cambc::vision::altar_lock_tiles(team::enemy);
        for (auto altar : cambc::map::altars().positions()) {
            const auto approach = tiles_around(altar, cambc::constants::submit_gems_range);
            if (hostile.is_set(altar)) locked_goals |= approach;
            else goals |= approach; // Friendly locks permit our tribute.
        }
        // If all altars are visibly hostile, approach one and clear it next turn.
        if (goals.is_empty()) goals = locked_goals;
        move_towards_closest(goals);
        return;
    }

    farm_camps();

    me.set_priority(1 + random_number(100));
}
