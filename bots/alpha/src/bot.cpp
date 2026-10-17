// Objective policy: clear one useful group, secure its capture, bank, rotate.
#include <cambc.h>
#include "bot.h"
#include <algorithm>
#include <array>
#include <limits>
#include <optional>
#include <type_traits>
#include <variant>

using cambc::vec2;
using cambc::team;
namespace {
constexpr float recall_fraction = 0.35f;
constexpr unsigned planning_reserve = 18000;
constexpr unsigned reselect_after_failures = 3;
constexpr float foreign_role_cost = 8.0f;

int distance(vec2 a, vec2 b) { return static_cast<int>(a.chebyshev_distance(b)); }
cambc::bitboard around(vec2 p, int radius) {
    cambc::bitboard result;
    result.draw_chebyshev(p, radius);
    return result;
}
cambc::bitboard blocked_tiles() {
    auto blocked = cambc::map::walls() | cambc::map::holes() | cambc::map::altars()
        | cambc::map::spawn_region(team::enemy) | cambc::vision::champion_tiles()
        | cambc::vision::camp_tiles() | cambc::vision::teleport_tiles();
    blocked.set(cambc::self().position(), false);
    return blocked;
}

// All goals are FREE approach/capture tiles. Never make an occupied camp a root.
// A false move reveals an obstruction; refresh and retry at most once.
bool navigate(cambc::bitboard goals) {
    auto& me = cambc::self();
    if (!me.can_move() || me.restrictions().contains(cambc::buff_restrictions::move)
        || goals.is_set(me.position())) return false;
    for (int attempt = 0; attempt < 2; ++attempt) {
        auto blocked = blocked_tiles();
        const auto free_goals = goals & ~blocked;
        if (free_goals.is_empty()) return false;
        cambc::distance_field field;
        cambc::bitboard visited;
        field.compute_to(blocked, free_goals, around(me.position(), 0), visited);
        auto best = me.position();
        for (auto p : blocked.reachable_tiles(best, me.base_stats().base_move_speed).positions())
            if (field.get(p) < field.get(best)) best = p;
        if (best == me.position()) return false;
        if (me.move_absolute(best)) return true;
        if (!me.can_move() || cambc::fuel_remaining() < planning_reserve) break;
    }
    return false;
}

bool live(const cambc::unit& target) {
    return target.is_visible() && target.health() > 0;
}

// is_ready() does NOT test movement exclusivity in the installed SDK.
bool ready(const cambc::ability& ability, bool walked) {
    if (!ability.info() || !ability.is_ready()
        || cambc::self().restrictions().contains(cambc::buff_restrictions::cast)) return false;
    return !walked || !std::visit([](const auto& info) {
        return info.exclusive_with_movement;
    }, *ability.info());
}

template<class Target>
bool fight(const Target& target, bool walked) {
    auto& me = cambc::self();
    if (!live(target)) return false;
    bool acted = false;
    if (me.can_attack() && !me.restrictions().contains(cambc::buff_restrictions::attack)
        && distance(me.position(), target.position()) <= me.attack_range()) {
        me.attack(target);
        acted = true;
    }
    // Retaliation/splash/basic damage may have killed caster or target.
    if (!me.is_alive() || !live(target)) return acted;
    const auto abilities = me.abilities();
    int best = -1;
    float value = 0;
    for (int i = 0; i < 2; ++i) {
        const auto& ability = abilities[i];
        if (!ready(ability, walked)) continue;
        if (ability.is_attack_reset()) {
            if (!me.can_attack() && ability.can_target_self()
                && distance(me.position(), target.position()) <= me.attack_range()
                && me.strength() > value) { best = i; value = me.strength(); }
        } else if (ability.is_damage() || ability.is_cc() || ability.is_aoe_damage()) {
            bool category;
            if constexpr (std::is_same_v<Target, cambc::camp>) category = ability.can_target_camps();
            else category = ability.can_target_enemies();
            if (!(category || (ability.is_aoe_damage() && ability.can_target_ground()))
                || !ability.valid_tiles().is_set(target.position())) continue;
            float damage = ability.damage_amount();
            // AoE only aims at an observed target; no unseen-unit assumptions.
            if (ability.is_aoe_damage()) {
                const auto radius = ability.get<cambc::ability_aoe_damage>().radius;
                unsigned count = 0;
                for (const auto& camp : cambc::vision::camps())
                    if (live(camp) && distance(camp.position(), target.position()) <= radius) ++count;
                damage *= std::max(1u, count);
            }
            if (damage > value) { best = i; value = damage; }
        }
    }
    if (best >= 0) {
        const auto& ability = abilities[best];
        bool cast = ability.is_attack_reset() ? ability.use()
            : ability.is_aoe_damage() ? ability.use(target.position()) : ability.use(target);
        acted |= cast;
        if (cast && me.is_alive() && live(target) && me.can_attack()
            && !me.restrictions().contains(cambc::buff_restrictions::attack)
            && distance(me.position(), target.position()) <= me.attack_range()) {
            me.attack(target);
            acted = true;
        }
    } else if (me.health() < me.max_health() * 0.7f) {
        for (const auto& ability : abilities)
            if (ability.is_shield() && ability.can_target_self() && ready(ability, walked)) {
                acted |= ability.use();
                break;
            }
    }
    return acted;
}

bool bank(bool allow_movement) {
    auto& me = cambc::self();
    if (!me.gem_count()) return false;
    const auto hostile_locks = cambc::vision::altar_lock_tiles(team::enemy);
    cambc::bitboard approaches;
    for (auto altar : cambc::map::altars().positions()) {
        if (distance(me.position(), altar) <= cambc::constants::submit_gems_range) {
            if (hostile_locks.is_set(altar)) {
                // submit_gems is void and can attack a hostile lock. Do not assume
                // that an attack allowance spent by movement can clear it.
                if (me.can_attack() && !me.restrictions().contains(cambc::buff_restrictions::attack)) me.submit_gems(altar);
                else continue;
            } else me.submit_gems(altar); // Allied locks permit our tribute.
            return true;
        }
        if (!hostile_locks.is_set(altar)) approaches |= around(altar, cambc::constants::submit_gems_range);
    }
    // If every visible altar is locked, approach one and spend three basic hits.
    if (approaches.is_empty())
        for (auto altar : cambc::map::altars().positions()) approaches |= around(altar, cambc::constants::submit_gems_range);
    if (allow_movement) {
        navigate(approaches);
        bank(false); // Refresh position and lock observations; channel this turn.
    }
    return true;
}
}

void Bot::initialize() {
    auto allies = cambc::champions(team::ally); // Identity list, not shared live vision.
    const auto id = static_cast<unsigned>(static_cast<cambc::handle_champion_t>(cambc::self()));
    team_size = std::max(1u, static_cast<unsigned>(allies.size()));
    for (const auto& ally : allies)
        role += static_cast<unsigned>(static_cast<cambc::handle_champion_t>(ally)) < id;
    const auto all_groups = cambc::map::camp_groups();
    for (const auto& group : all_groups) {
        if (group.camps().empty()) continue;
        float hp = 0, damage = 0;
        bool monolith = false;
        for (const auto& camp : group) {
            const auto design = camp.base_stats(); // Static design is public outside vision.
            hp += design.base_health;
            damage += design.base_strength;
            monolith |= camp.is_monolith();
        }
        camps.push_back({group, group.spawn_tiles(), group.camps()[0].spawn_position(), hp, damage, monolith});
    }
    cambc::self().set_priority(100 - static_cast<int>(role));
    initialized = true;
}

void Bot::buy_items() {
    auto& me = cambc::self();
    using I = cambc::item_type;
    const auto inventory = me.item_count();
    // Finish each passive once; duplicates do not stack. All builds support basics
    // and resets instead of buying Focus on champions that never scale damage with it.
    I item = I::power_shard_of_strength;
    unsigned needed = std::numeric_limits<unsigned>::max();
    if (!inventory[I::jungle_emblem_of_strength]) {
        item = I::jungle_shard_of_strength;
        needed = 5 - std::min(5u, inventory[item]);
    } else if (!inventory[I::monster_emblem_of_strength]) {
        item = I::monster_shard_of_strength;
        needed = 5 - std::min(5u, inventory[item]);
    }
    auto count = std::min(needed, me.gold_count() / item.cost());
    if (count && me.can_buy(item, count)) {
        me.buy(item, count);
        // Up to two stage boundaries plus the final bulk purchase, no gold loop.
        if (count == needed) buy_items();
    }
}

// Preserve a useful capture even if other attackable camps are nearby.
bool Bot::collect_here() {
    auto& me = cambc::self();
    for (auto& plan : camps) {
        if (!plan.tiles.is_set(me.position())) continue;
        const auto state = plan.group.state(); // Our position proves group visibility.
        if (!std::holds_alternative<cambc::map::camp_group_reward_available>(state)) return false;
        bool other_collector = false;
        for (const auto& ally : cambc::vision::champions(team::ally))
            if (!(ally == me) && live(ally) && plan.tiles.is_set(ally.position())
                && static_cast<unsigned>(static_cast<cambc::handle_champion_t>(ally))
                    < static_cast<unsigned>(static_cast<cambc::handle_champion_t>(me))) other_collector = true;
        if (other_collector) return false; // Lower-ID collector owns this capture.
        for (const auto& enemy : cambc::vision::champions(team::enemy))
            if (live(enemy) && plan.tiles.is_set(enemy.position())) {
                if (!fight(enemy, false)) {
                    const bool walked = navigate(around(enemy.position(), me.attack_range()));
                    if (walked) fight(enemy, true);
                }
                return true;
            }
        return true; // Stay through all capture phases; extra allies do not speed it.
    }
    return false;
}

int Bot::choose_camp() {
    auto& me = cambc::self();
    const auto visible = cambc::vision::visible_tiles();
    const auto allies = cambc::vision::champions(team::ally);
    const auto now = cambc::round_number();
    float best_value = -1;
    int best = -1;
    for (unsigned i = 0; i < camps.size(); ++i) {
        if (cambc::fuel_remaining() < planning_reserve) break;
        auto& plan = camps[i];
        if (now < plan.avoid_until) continue;
        const bool seen = !(plan.tiles & visible).is_empty();
        bool reward = false;
        if (seen) {
            const auto state = plan.group.state();
            if (const auto* respawn = std::get_if<cambc::map::camp_group_respawning>(&state)) {
                plan.ready_round = now + std::max(1, respawn->timer);
                continue; // Never wait on respawn tiles.
            }
            plan.ready_round = 0;
            reward = std::holds_alternative<cambc::map::camp_group_reward_available>(state);
        } else if (now < plan.ready_round) continue; // Uncertain prediction, re-observe on arrival.
        float travel = distance(me.position(), plan.anchor);
        unsigned helpers = 0;
        bool collector = false;
        for (const auto& ally : allies) {
            if (ally == me || !live(ally)) continue;
            if (distance(ally.position(), plan.anchor) <= 3) ++helpers;
            if (plan.tiles.is_set(ally.position())) collector = true;
            if (distance(ally.position(), plan.anchor) + 2 < travel) travel += 8;
        }
        if (reward && collector) continue;
        // Strongly defer solo monoliths, but retain a playable fallback on maps
        // where they are the only available income. Nearby farmers can converge.
        if (plan.monolith && !reward && me.strength() < 200 && helpers < 2) travel += 80;
        float health = plan.health;
        if (seen && !reward) {
            // Partial visibility is a lower bound; retain estimates for hidden members.
            health = 0;
            for (const auto& camp : plan.group)
                health += camp.is_visible() ? std::max(0.0f, camp.health()) : camp.base_stats().base_health;
        }
        const float clear = reward ? 0.0f : health / std::max(1.0f, me.strength() * (1 + 0.7f * helpers));
        const float danger = reward ? 0.0f : plan.damage / std::max(1.0f, me.health()) * clear * 8;
        const float affinity = i % team_size == role ? 0 : foreign_role_cost;
        // Soft ownership spreads the opening without forbidding nearby profitable work.
        const float cost = 8 + travel + clear + danger + affinity + (static_cast<int>(i) == target ? -6 : 0);
        const float value = (plan.group.gem_value() + plan.group.gold_value() * 0.12f + 8) / std::max(1.0f, cost);
        if (value > best_value) { best_value = value; best = static_cast<int>(i); }
    }
    return best;
}

void Bot::farm() {
    auto& me = cambc::self();
    target = choose_camp();
    if (target < 0) {
        // Vacate captured spawn tiles even when every productive group is cooling.
        auto safe = cambc::map::spawn_region(team::ally);
        for (const auto& plan : camps) safe &= ~plan.tiles;
        navigate(safe);
        return;
    }
    auto& plan = camps[target];
    const auto visible = cambc::vision::visible_tiles();
    bool reward = !(plan.tiles & visible).is_empty()
        && std::holds_alternative<cambc::map::camp_group_reward_available>(plan.group.state());
    if (reward) {
        if (!navigate(plan.tiles) && !plan.tiles.is_set(me.position())
            && ++failed_moves >= reselect_after_failures) {
            plan.avoid_until = cambc::round_number() + 8;
            failed_moves = 0;
            target = -1;
        }
        return;
    }
    // Only clear our selected group, finishing low-health members before switching.
    auto engage = [&](bool walked) {
        const cambc::camp* best = nullptr;
        float hp = std::numeric_limits<float>::max();
        for (const auto& camp : plan.group)
            if (live(camp) && distance(me.position(), camp.position()) <= std::max(4, me.attack_range())
                && camp.health() < hp) { best = &camp; hp = camp.health(); }
        return best && fight(*best, walked);
    };
    const bool acted = engage(false);
    if (!me.is_alive() || cambc::fuel_remaining() < planning_reserve) return;
    cambc::bitboard goals;
    for (const auto& camp : plan.group)
        if (!camp.is_visible() || camp.health() > 0)
            goals |= around(camp.spawn_position(), me.attack_range());
    if (goals.is_empty()) goals = plan.tiles;
    const bool walked = navigate(goals);
    if (walked && me.is_alive()) engage(true); // Fresh live checks after movement.
    if (walked || acted) failed_moves = 0;
    else if (++failed_moves >= reselect_after_failures) {
        plan.avoid_until = cambc::round_number() + 8;
        target = -1;
        failed_moves = 0;
    }
}

void Bot::play_turn() {
    auto& me = cambc::self();
    // Dead turns can still shop. Channels must survive all navigation and combat.
    if (!me.is_alive()) { buy_items(); target = -1; return; }
    if (me.is_recalling() || me.is_submitting_gems() || me.is_teleporting()) return;
    if (me.buffs().has_stun()) return;
    if (!me.can_move() && !me.can_attack() && !me.can_cast()) return;
    if (!initialized) initialize();
    const auto spawn = cambc::map::spawn_region(team::ally);
    const bool at_spawn = spawn.is_set(me.position());
    if (at_spawn || me.champion_name() == cambc::champion_type::tavi) buy_items();
    if (at_spawn && me.health() < me.max_health()) return; // Heal at turn end.
    if (!at_spawn && me.health() < me.max_health() * recall_fraction) {
        navigate(spawn);
        if (!spawn.is_set(me.position())) me.recall();
        return;
    }
    if (collect_here()) return;
    if (me.gem_count()) { bank(true); return; }
    // No chase: defend in current basic range, then use any remaining movement.
    for (const auto& enemy : cambc::vision::champions(team::enemy))
        if (live(enemy) && distance(me.position(), enemy.position()) <= me.attack_range()) {
            fight(enemy, false);
            break;
        }
    if (me.is_alive() && cambc::fuel_remaining() >= planning_reserve) farm();
}
