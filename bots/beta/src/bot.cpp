#include <cambc.h>
#include "bot.h"
#include "farm_policy.h"
#include <algorithm>
#include <array>
#include <limits>
#include <optional>
#include <type_traits>
#include <variant>

using cambc::vec2;
using cambc::team;
namespace {
constexpr float retreat_fraction = 0.45f;
constexpr unsigned shopping_gold = 150;
constexpr unsigned retry_delay = 12;
constexpr std::uint64_t planning_reserve = 18000;
constexpr std::uint64_t scan_reserve = 45000;
constexpr std::uint64_t routing_start_reserve = 65000;
constexpr std::size_t max_group_checks = 12;
int distance(vec2 a, vec2 b) { return static_cast<int>(a.chebyshev_distance(b)); }

cambc::bitboard around(vec2 p, int range) {
    cambc::bitboard result;
    result.draw_chebyshev(p, range);
    return result;
}

cambc::bitboard blocked_tiles() {
    auto result = cambc::map::walls() | cambc::map::holes() | cambc::map::altars()
        | cambc::map::spawn_region(team::enemy) | cambc::vision::champion_tiles()
        | cambc::vision::camp_tiles() | cambc::vision::teleport_tiles();
    result.set(cambc::self().position(), false);
    return result;
}

// Every root is a free approach tile. Retry once after a hidden obstruction.
bool move_to(cambc::bitboard goals) {
    auto& me = cambc::self();
    if (!me.can_move()) return false;
    for (int attempt = 0; attempt < 2; ++attempt) {
        const auto blocked = blocked_tiles();
        goals &= ~blocked;
        if (goals.is_empty() || goals.is_set(me.position())) return false;
        cambc::distance_field field;
        cambc::bitboard visited;
        field.compute_to(blocked, goals, around(me.position(), 0), visited);
        auto best = me.position();
        auto value = field.get(best);
        for (auto tile : blocked.reachable_tiles(me.position(), me.base_stats().base_move_speed).positions())
            if (field.get(tile) < value) { best = tile; value = field.get(tile); }
        if (best == me.position()) return false;
        if (me.move_absolute(best)) return true;
        if (cambc::fuel_remaining() < planning_reserve) return false;
    }
    return false;
}

bool exposed(vec2 position) {
    for (const auto& enemy : cambc::vision::champions(team::enemy))
        if (enemy.is_visible() && enemy.health() > 0
            && distance(position, enemy.position()) <= enemy.attack_range() + 1) return true;
    // Conservatively treat damaging camps in range as threats; wake state is not
    // available in this pinned header, even though the newer export describes it.
    for (const auto& camp : cambc::vision::camps())
        if (camp.is_visible() && camp.health() > 0 && camp.strength() > 0
            && distance(position, camp.position()) <= camp.attack_range()) return true;
    return false;
}

void shield_if_exposed() {
    auto& me = cambc::self();
    if (!me.can_cast() || !exposed(me.position())) return;
    for (const auto& ability : me.abilities())
        if (ability.is_shield() && ability.can_target_self() && ability.is_ready()) {
            if (ability.use()) return;
        }
}

// One basic attack and at most one successful cast, with a refreshed reset attack.
// Ground AoE uses the observed target tile; unit spells require their own mask.
template<class Target>
bool fight(const Target& target, bool walked = false) {
    auto& me = cambc::self();
    if (!target.is_visible() || target.health() <= 0) return false;
    bool acted = false;
    if (me.can_attack() && distance(me.position(), target.position()) <= me.attack_range()) {
        shield_if_exposed();
        if (me.can_attack()) { me.attack(target); acted = true; }
    }
    if (!me.is_alive() || !target.is_visible() || target.health() <= 0 || !me.can_cast()) return acted;

    std::optional<cambc::ability> best;
    float best_value = 0;
    for (const auto& ability : me.abilities()) {
        if (!ability.is_ready()) continue;
        const bool excludes_walk = std::visit([](const auto& info) { return info.exclusive_with_movement; }, ability.info().value());
        if (walked && excludes_walk) continue;
        if (ability.is_attack_reset()) {
            if (acted && !me.can_attack() && ability.can_target_self()
                && distance(me.position(), target.position()) <= me.attack_range()
                && me.strength() > best_value) { best = ability; best_value = me.strength(); }
            continue;
        }
        if (!(ability.is_damage() || ability.is_cc() || ability.is_aoe_damage())) continue;
        if (ability.is_aoe_damage()) {
            if (!ability.can_target_ground()) continue;
        } else if constexpr (std::is_same_v<Target, cambc::camp>) {
            if (!ability.can_target_camps()) continue;
        } else {
            if (!ability.can_target_enemies()) continue;
        }
        if (!ability.valid_tiles().is_set(target.position())) continue;
        float value = ability.damage_amount();
        if (ability.is_cc()) value += me.strength();
        if (ability.is_aoe_damage()) {
            const auto radius = ability.get<cambc::ability_aoe_damage>().radius;
            for (const auto& camp : cambc::vision::camps())
                if (camp.is_visible() && camp.health() > 0 && camp.position() != target.position()
                    && distance(camp.position(), target.position()) <= radius) value += ability.damage_amount();
        }
        if (value > best_value) { best = ability; best_value = value; }
    }
    if (!best) return acted;
    const bool cast = best->is_attack_reset() ? best->use()
        : best->is_aoe_damage() ? best->use(target.position()) : best->use(target);
    if (cast && best->is_attack_reset() && me.is_alive() && target.is_visible()
        && target.health() > 0 && me.can_attack()
        && distance(me.position(), target.position()) <= me.attack_range()) me.attack(target);
    return acted || cast;
}

bool bank() {
    auto& me = cambc::self();
    if (me.gem_count() == 0) return false;
    auto enemy_locks = cambc::vision::altar_lock_tiles(team::enemy);
    cambc::bitboard unlocked, locked;
    for (auto altar : cambc::map::altars().positions()) {
        if (distance(me.position(), altar) <= cambc::constants::submit_gems_range) {
            // SDK converts a hostile lock to an attack; preserve this legal fallback.
            if (!enemy_locks.is_set(altar) || me.can_attack()) {
                me.submit_gems(altar);
                return true;
            }
        }
        if (enemy_locks.is_set(altar)) locked |= around(altar, cambc::constants::submit_gems_range);
        else unlocked |= around(altar, cambc::constants::submit_gems_range);
    }
    if (!unlocked.is_empty() && move_to(unlocked)) return true;
    if (!locked.is_empty()) move_to(locked);
    return true;
}
} // namespace

void Bot::buy_items() {
    auto& me = cambc::self();
    using I = cambc::item_type;
    auto counts = me.item_count();
    // Finish each unique farming passive once, then stack useful stats.
    const std::array shards{I::jungle_shard_of_strength, I::monster_shard_of_strength,
        I::durability_shard_of_health};
    const std::array emblems{I::jungle_emblem_of_strength, I::monster_emblem_of_strength,
        I::durability_emblem_of_health};
    for (std::size_t i = 0; i < shards.size(); ++i) {
        if (counts[emblems[i]] != 0) continue;
        const auto needed = shards[i].combine_count() - counts[shards[i]];
        const auto n = std::min(needed, me.gold_count() / shards[i].cost());
        if (n && me.can_buy(shards[i], n)) me.buy(shards[i], n);
        if (n < needed) return;
    }
    const auto n = me.gold_count() / I::power_shard_of_strength.cost();
    if (n && me.can_buy(I::power_shard_of_strength, n)) me.buy(I::power_shard_of_strength, n);
}

void Bot::farm_camps() {
    auto& me = cambc::self();
    const auto visible = cambc::vision::visible_tiles();
    const auto allies = cambc::vision::champion_tiles(team::ally);
    const auto round = cambc::round_number();
    int chosen = -1;
    float best_score = std::numeric_limits<float>::max();
    bool reward = false;
    cambc::bitboard best_goals;
    const auto position = me.position();
    const auto strength = std::max(1.0f, me.strength());
    // No new field when earlier decisions consumed the planning budget. Keep a
    // bounded legal combat fallback and leave final yield to main.cpp.
    if (cambc::fuel_remaining() < routing_start_reserve) {
        unsigned inspected = 0;
        for (const auto& camp : cambc::vision::camps()) {
            if (++inspected > 8 || cambc::fuel_remaining() < planning_reserve) break;
            if (fight(camp)) return;
        }
        return;
    }
    const auto blocked = blocked_tiles();
    cambc::distance_field travel;
    cambc::bitboard visited;
    travel.compute(blocked, around(position, 0), visited);
    // Rank with cached geometry before making expensive visibility/state calls.
    // Include our committed group first so an ongoing capture is always checked.
    std::vector<std::size_t> order;
    order.reserve(groups.size());
    for (std::size_t i = 0; i < groups.size(); ++i)
        if (round >= groups[i].retry_round
            && !farm_policy::cooling_down(round, groups[i].respawn_observed_until))
            order.push_back(i);
    const auto checked = std::min(max_group_checks, order.size());
    std::partial_sort(order.begin(), order.begin() + checked, order.end(), [&](auto a, auto b) {
        if (static_cast<int>(a) == target_group) return static_cast<int>(b) != target_group;
        if (static_cast<int>(b) == target_group) return false;
        const auto rank = [&](auto i) {
            return distance(position, groups[i].center) * 3.0f
                + groups[i].initial_health / strength * 0.35f;
        };
        const auto ra = rank(a), rb = rank(b);
        return ra != rb ? ra < rb : a < b;
    });
    for (std::size_t n = 0; n < checked; ++n) {
        // Leave enough fuel to choose a legal step and yield, not only to stop scanning.
        if (n > 0 && cambc::fuel_remaining() < scan_reserve) break;
        const auto i = order[n];
        auto& g = groups[i];
        const bool seen = !(g.spawns & visible).is_empty();
        bool available = false;
        if (seen) {
            const auto state = g.group.state();
            if (const auto* cooldown = std::get_if<cambc::map::camp_group_respawning>(&state)) {
                g.respawn_observed_until = farm_policy::observed_deadline(round, cooldown->timer);
                continue;
            }
            g.respawn_observed_until = 0;
            available = std::holds_alternative<cambc::map::camp_group_reward_available>(state);
        }
        if (available && g.spawns.is_set(me.position())) return; // Keep capture timer intact.
        if (available && !(g.spawns & allies).is_empty()) continue; // One collector suffices.
        float hp = 0;
        cambc::bitboard goals;
        bool complete = true;
        if (available) goals = g.spawns;
        else for (const auto& camp : g.group.camps()) {
            if (cambc::fuel_remaining() < scan_reserve) { complete = false; break; }
            if (camp.is_visible()) {
                const auto health = camp.health();
                if (health <= 0) continue;
                hp += health;
                goals |= around(camp.position(), me.attack_range());
            } else {
                hp += camp.base_stats().base_health;
                // Scout unseen spawns directly. A currently visible, empty
                // spawn is not a useful scouting goal for a hidden camp.
                if (!visible.is_set(camp.spawn_position())) goals.set(camp.spawn_position());
            }
        }
        if (!complete) break; // Never score a partly inspected group as cheap.
        goals &= ~blocked;
        unsigned steps = cambc::distance_field::unreachable;
        for (auto tile : goals.positions()) {
            if (cambc::fuel_remaining() < scan_reserve) { complete = false; break; }
            steps = std::min(steps, unsigned(travel.get(tile)));
            if (steps == 0) break;
        }
        if (!complete) break;
        if (steps == cambc::distance_field::unreachable) {
            // Rotate unreachable shortlist entries out so the next turn can
            // discover reachable groups beyond the bounded geometric shortlist.
            g.retry_round = round + retry_delay;
            continue;
        }
        const bool crowded = !available && !(around(g.center, 2) & allies).is_empty()
            && !around(g.center, 2).is_set(position);
        const float score = farm_policy::score(steps, me.base_stats().base_move_speed,
            hp, strength, g.group.gem_value(), g.group.gold_value(), cambc::constants::capture_time,
            static_cast<int>(i) == target_group, crowded);
        if (score < best_score) {
            best_score = score; chosen = i; reward = available; best_goals = std::move(goals);
        }
    }
    if (chosen < 0) {
        target_group = -1;
        // An empty bag may be a gold-only capture. Do not block its next spawn
        // forever just because every other inspected group is cooling down.
        if (cambc::fuel_remaining() >= planning_reserve)
            for (const auto& g : groups)
                if (g.spawns.is_set(position)) { move_to(around(position, 1) & ~g.spawns); break; }
        return;
    }
    target_group = chosen;
    auto& g = groups[chosen];
    if (!reward) {
        // Stay focused on one physical group; Varg splash and Ryth AoE clear it together.
        for (const auto& camp : g.group.camps())
            if (fight(camp)) return;
    }
    auto goals = std::move(best_goals);
    if (cambc::fuel_remaining() < planning_reserve) return;
    const bool moved = move_to(goals);
    // Successful movement and failed hidden-blocker reveals both change vision.
    // Static group handles query fresh live observations inside fight().
    for (const auto& camp : g.group.camps())
        if (cambc::fuel_remaining() >= planning_reserve && fight(camp, moved)) return;
    if (!moved && !goals.is_set(me.position())) {
        g.retry_round = round + retry_delay;
        target_group = -1;
    }
}

void Bot::play_turn() {
    auto& me = cambc::self();
    // can_buy handles dead shopping and Tavi's field exception without live position queries.
    buy_items();
    if (!me.is_alive()) { recovering = false; target_group = -1; return; }
    if (me.is_recalling() || me.is_submitting_gems() || me.is_teleporting()) return;
    if (!me.can_move() && !me.can_attack() && !me.can_cast()) return;

    const auto& spawn = cambc::map::spawn_region(team::ally);
    if (spawn.is_set(me.position())) {
        // Recall resolves before this turn; healing happens only at its END.
        if (me.health() < me.max_health()) return;
        recovering = false;
    }
    if (me.health() < me.max_health() * retreat_fraction) recovering = true;
    if (recovering) {
        shield_if_exposed();
        move_to(spawn);
        if (!spawn.is_set(me.position()) && !exposed(me.position())
            && !me.restrictions().contains(cambc::buff_restrictions::move)) me.recall();
        return;
    }
    // Secure bags before accepting unrelated fights.
    if (bank()) return;
    for (const auto& enemy : cambc::vision::champions(team::enemy))
        if (enemy.is_visible() && enemy.health() > 0
            && distance(me.position(), enemy.position()) <= me.attack_range()
            && (enemy.health() <= me.strength() * 2
                || distance(me.position(), enemy.position()) <= enemy.attack_range()))
            if (fight(enemy)) return;

    if (!initialized) {
        for (auto group : cambc::map::camp_groups()) {
            auto spawns = group.spawn_tiles();
            vec2 center{};
            float hp = 0;
            for (const auto& camp : group.camps()) {
                center += camp.spawn_position(); hp += camp.base_stats().base_health;
            }
            center /= static_cast<int>(group.camps().size());
            groups.push_back({std::move(group), std::move(spawns), center, hp});
        }
        initialized = true;
    }
    // Reinvest captured gold on safe empty-bag returns; field shoppers need no trip.
    if (me.gold_count() >= shopping_gold && me.champion_name() != cambc::champion_type::tavi
        && me.health() < me.max_health() * 0.8f && !exposed(me.position())) {
        recovering = true;
        me.recall();
        return;
    }
    farm_camps();
}
