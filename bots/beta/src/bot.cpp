#include <cambc.h>
#include "bot.h"
#include "policy.h"
#include "harvest_test.h"
#include <algorithm>
#include <array>
#include <limits>
#include <iostream>
#include <optional>
#include <type_traits>
#include <variant>

using cambc::vec2;
using cambc::team;
namespace {
constexpr float retreat_fraction = 0.45f;
constexpr unsigned shopping_gold = 300;
constexpr unsigned retry_delay = 12;
constexpr std::uint64_t planning_reserve = 18000;
constexpr std::uint64_t scan_reserve = 45000;
constexpr std::uint64_t search_reserve = 45000;

constexpr std::uint64_t lock_reserve = 30000;
constexpr int lock_placement_range = 2; // Pinned SDK consumable contract.
constexpr std::uint64_t dash_reserve = 45000;
constexpr unsigned dash_steps = 2;
int distance(vec2 a, vec2 b) { return static_cast<int>(a.chebyshev_distance(b)); }

cambc::bitboard around(vec2 p, int range) {
    cambc::bitboard result;
    result.draw_chebyshev(p, range);
    return result;
}

// Avoid allocating/intersecting a map-sized board just to test group visibility.
bool group_seen(const cambc::map::camp_group& group, const cambc::bitboard& visible) {
    for (const auto& member : group.camps())
        if (visible.is_set(member.spawn_position())) return true;
    return false;
}

// Spend inventory along our normal route, never detour or interrupt a channel.
// Friendly locks permit our tribute and cost opponents five basic attacks.
void lock_nearby_altar() {
    auto& me = cambc::self();
    if (cambc::fuel_remaining() < lock_reserve || !me.is_alive()
        || me.is_recalling() || me.is_submitting_gems() || me.is_teleporting()
        || me.restrictions().contains(cambc::buff_restrictions::consumable)) return;
    const auto& lock = me.consumables()[cambc::consumable_type::altar_lock];
    if (!lock.count()) return;
    // Missing hidden locks do not establish that an altar is empty.
    const auto candidates = around(me.position(), lock_placement_range)
        & cambc::map::altars() & cambc::vision::visible_tiles()
        & ~cambc::vision::altar_lock_tiles();
    for (auto altar : candidates.positions()) {
        // One attempt per observation phase, including a False reveal result.
        lock.use(altar);
        return;
    }
}

cambc::bitboard blocked_tiles() {
    auto result = cambc::map::walls() | cambc::map::holes() | cambc::map::altars()
        | cambc::map::spawn_region(team::enemy) | cambc::vision::champion_tiles()
        | cambc::vision::camp_tiles() | cambc::vision::teleport_tiles();
    result.set(cambc::self().position(), false);
    return result;
}

// Spend a cast only for two real route steps, never an unreachable-field artifact.
constexpr bool useful_dash(unsigned from, unsigned to) {
    return from != cambc::distance_field::unreachable
        && to != cambc::distance_field::unreachable && to < from
        && from - to >= dash_steps;
}
static_assert(useful_dash(2, 0));
static_assert(useful_dash(12, 10));
static_assert(!useful_dash(1, 0));
static_assert(!useful_dash(0, 0));
static_assert(!useful_dash(2, 3));
static_assert(!useful_dash(cambc::distance_field::unreachable, 0));
static_assert(!useful_dash(3, cambc::distance_field::unreachable));

// Walk first, retaining reset casts on arrival. Reuse the existing route field;
// only the occupancy/vision masks are refreshed after walking. No extra search.
void dash_along_route(const cambc::distance_field& field) {
    auto& me = cambc::self();
    const auto abilities = me.abilities();
    for (const auto& ability : abilities) {
        if (!ability.is_dash()) continue;
        if (cambc::fuel_remaining() < dash_reserve || !me.is_alive()
            || !me.can_cast() || me.is_recalling() || me.is_submitting_gems()
            || me.is_teleporting()) return;
        const auto restrictions = me.restrictions();
        if (restrictions.contains(cambc::buff_restrictions::move)
            || restrictions.contains(cambc::buff_restrictions::cast)) return;
        const auto info = ability.get<cambc::ability_dash>();
        if (info.exclusive_with_movement || info.range < dash_steps
            || !ability.can_target_ground() || !ability.is_ready()) return;
        const auto origin = me.position();
        const auto remaining = field.get(origin);
        if (!useful_dash(remaining, 0)) return;

        const auto blocked = blocked_tiles();
        const auto visible = cambc::vision::visible_tiles();
        const auto range = ability.valid_tiles();
        cambc::bitboard enemy_danger;
        for (const auto& enemy : cambc::vision::champions(team::enemy))
            if (enemy.is_visible() && enemy.health() > 0)
                enemy_danger |= around(enemy.position(), enemy.attack_range() + 1);

        constexpr std::array directions{vec2::north, vec2::north_east, vec2::east,
            vec2::south_east, vec2::south, vec2::south_west, vec2::west, vec2::north_west};
        auto destination = origin;
        auto best = remaining;
        for (auto direction : directions) {
            const auto middle = origin + direction;
            const auto landing = origin + direction * static_cast<int>(dash_steps);
            // A deliberately conservative legal subset: a straight, fully seen,
            // ordinary walkable path, including its intermediate tile. No holes.
            if (!cambc::map::is_in_bounds(landing) || !range.is_set(landing)
                || !visible.is_set(middle) || !visible.is_set(landing)
                || blocked.is_set(middle) || blocked.is_set(landing)
                || enemy_danger.is_set(landing)) continue;
            const auto value = field.get(landing);
            if (useful_dash(remaining, value) && value < best) {
                destination = landing;
                best = value;
            }
        }
        if (destination != origin && cambc::fuel_remaining() >= lock_reserve) {
            // False reveals an obstruction and preserves the cast. Stop this
            // phase; the caller refreshes observations before subsequent combat.
            if (ability.use(destination)) lock_nearby_altar();
        }
        return; // At most one dash attempt, including a hidden-blocker reveal.
    }
}

// Cache route geometry, never observations used to authorize an action. Current
// occupancy is read afresh for every step and a blocked route is repaired using
// current blockers, including after a hidden-blocker reveal. A field computed
// to the current tile contains the entire downhill route to its roots.
bool move_to(cambc::bitboard goals, bool* deferred = nullptr) {
    if (deferred) *deferred = false;
    const auto defer = [&] { if (deferred) *deferred = true; return false; };
    auto& me = cambc::self();
    if (!me.can_move()) return false;
    const auto terrain = cambc::map::walls() | cambc::map::holes() | cambc::map::altars()
        | cambc::map::spawn_region(team::enemy);
    goals &= ~terrain;
    if (goals.is_empty() || goals.is_set(me.position())) return false;
    struct Route {
        cambc::bitboard goals;
        cambc::distance_field field;
    };
    static std::optional<Route> route;
    if (!route || route->goals != goals
        || route->field.get(me.position()) == cambc::distance_field::unreachable) {
        // Do not start a nontrivial search after the planner spent our reserve.
        if (cambc::fuel_remaining() < search_reserve) return defer();
        const auto blocked = blocked_tiles();
        const auto free_goals = goals & ~blocked;
        if (free_goals.is_empty()) return false;
        route.emplace();
        route->goals = goals;
        cambc::bitboard visited;
        route->field.compute_to(blocked, free_goals, around(me.position(), 0), visited);
    }
    for (int attempt = 0; attempt < 2; ++attempt) {
        if (cambc::fuel_remaining() < planning_reserve) return defer();
        const auto origin = me.position();
        const auto blocked = blocked_tiles();
        const auto free_goals = goals & ~blocked;
        auto best = origin;
        auto value = route->field.get(origin);
        const auto steps = blocked.reachable_tiles(origin, me.base_stats().base_move_speed);
        for (auto tile : steps.positions())
            if (route->field.get(tile) < value) { best = tile; value = route->field.get(tile); }
        if (best == origin) {
            // A corridor detour can initially move away from every local
            // downhill waypoint. Rebuild the route rather than declaring that
            // valid objective unreachable after a radius-limited repair.
            if (cambc::fuel_remaining() < search_reserve) return defer();
            if (free_goals.is_empty()) return false;
            cambc::bitboard visited;
            route->field.compute_to(blocked, free_goals, around(origin, 0), visited);
            value = route->field.get(origin);
            for (auto tile : steps.positions())
                if (route->field.get(tile) < value) { best = tile; value = route->field.get(tile); }
        }
        if (best == origin) return false;
        if (me.move_absolute(best)) {
            lock_nearby_altar();
            dash_along_route(route->field);
            return true;
        }
        // False revealed an obstruction. Rebuild only the live masks; cached
        // terrain remains valid, but never retry a known occupied step.
    }
    return false;
}

bool exposed(vec2 position) {
    for (const auto& enemy : cambc::vision::champions(team::enemy))
        if (enemy.is_visible() && enemy.health() > 0
            && distance(position, enemy.position()) <= enemy.attack_range() + 1) return true;
    // Sleeping camps are harmless until pulled. Recall must escape awake camps.
    for (const auto& camp : cambc::vision::camps())
        if (camp.is_visible() && camp.health() > 0 && camp.is_awake() && camp.strength() > 0
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
    // Reserve ten gold before equipment spending, at spawn or while dead.
    // can_buy enforces stock, location and Tavi's consumable shop restrictions.
    const auto lock = cambc::consumable_type::altar_lock;
    if (me.can_buy(lock)) me.buy(lock);
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

void Bot::initialize() {
    // Static map layout is loaded once; it is not a live observation.
    for (auto group : cambc::map::camp_groups()) {
        auto spawns = group.spawn_tiles();
        float hp = 0, incoming = 0;
        for (const auto& camp : group.camps()) {
            const auto stats = camp.base_stats();
            hp += stats.base_health;
            incoming += stats.base_strength;
        }
        const auto anchor = group.camps().front().spawn_position();
        const auto gems = group.gem_value(), gold = group.gold_value();
        const auto count = static_cast<int>(group.camps().size());
        groups.push_back({std::move(group), std::move(spawns), anchor, hp, incoming,
            0, 0, gems, gold, count});
    }
    initialized = true;
}

bool Bot::hold_capture() {
    const auto position = cambc::self().position();
    for (const auto& g : groups) {
        if (!g.spawns.is_set(position)) continue;
        // Our occupied spawn tile is necessarily visible. Stay through completion,
        // even if we already carry a small bag from a preceding group.
        if (std::holds_alternative<cambc::map::camp_group_reward_available>(g.group.state()))
            return true;
    }
    return false;
}

void Bot::farm_camps() {
    auto& me = cambc::self();
    const auto position = me.position();
    const auto round = cambc::round_number();
    const auto visible = cambc::vision::visible_tiles();
    const auto allies = cambc::vision::champions(team::ally);
    const auto camps = cambc::vision::camps();
    const auto strength = std::max(1.0f, me.strength());
    const auto attack_range = me.attack_range();
    const auto cash = me.gold_count();
    const auto items = me.item_count();
    const float mitigation = items[cambc::item_type::jungle_emblem_of_strength] ? 0.7f : 1.0f;

    // Geometry is only a ranking estimate. Actual movement uses the cached
    // terrain/occupancy-aware route. Never require a whole-map field before
    // selecting an actionable local frontier.
    const bool committed = target_group >= 0;
    std::vector<std::size_t> order;
    if (committed) {
        order.push_back(static_cast<std::size_t>(target_group));
    } else {
        const int moved = plan_valid ? distance(position, plan_origin) : 0;
        if (policy::refresh_plan(plan_valid, round, plan_round, moved)) {
            const auto rank = [&](std::size_t i) {
                const auto& g = groups[i];
                const float walk = std::max(0, distance(position, g.anchor) - attack_range);
                const float wait = g.ready_round > round + walk ? g.ready_round - round - walk : 0;
                const float value = g.gems + policy::gold_value(cash) * g.gold;
                return round < g.retry_round ? -1.0f
                    : value / (walk + wait + g.initial_health / (strength * 1.125f) + 6.0f);
            };
            const auto better = [&](auto a, auto b) {
                const auto ra = rank(a), rb = rank(b);
                return ra != rb ? ra > rb : a < b;
            };
            // Retain good frontiers, but refresh their estimates at this origin.
            // Inspect at most 32 new static records. Ranking itself must not
            // become the next whole-map prerequisite on dense 100x100 maps.
            std::erase_if(plan_order, [&](auto i) { return rank(i) <= 0; });
            std::sort(plan_order.begin(), plan_order.end(), better);
            const auto count = std::min<std::size_t>(policy::ranking_batch, groups.size());
            for (std::size_t k = 0; k < count; ++k) {
                if (cambc::fuel_remaining() < scan_reserve + 10000) break;
                const auto i = rank_cursor;
                rank_cursor = policy::next_frontier(rank_cursor, groups.size());
                if (rank(i) <= 0 || std::find(plan_order.begin(), plan_order.end(), i) != plan_order.end()) continue;
                plan_order.push_back(i);
                std::sort(plan_order.begin(), plan_order.end(), better);
                if (plan_order.size() > policy::local_candidates) plan_order.pop_back();
            }
            plan_origin = position;
            plan_round = round;
            plan_valid = true;
        }
        // Put rotating work first so a fuel-limited local shortlist cannot
        // starve exploration. Advance the persistent cursor only after a check
        // actually starts, never merely because it was queued.
        auto cursor = scan_cursor;
        const auto rotate = std::min<std::size_t>(policy::exploration_candidates, groups.size());
        for (std::size_t k = 0; k < rotate; ++k) {
            order.push_back(cursor);
            cursor = policy::next_frontier(cursor, groups.size());
        }
        const auto n = std::min<std::size_t>(policy::local_candidates, plan_order.size());
        for (std::size_t k = 0; k < n; ++k)
            if (std::find(order.begin(), order.end(), plan_order[k]) == order.end()) order.push_back(plan_order[k]);
    }
    const auto checked = std::min<std::size_t>(order.size(), policy::frontier_batch);
    bool scan_complete = true;

    int chosen = -1, rally = -1;
    float best_score = -1, rally_score = -1;
    for (std::size_t n = 0; n < checked; ++n) {
        if (cambc::fuel_remaining() < scan_reserve) { scan_complete = false; break; }
        const auto i = order[n];
        if (!committed && i == scan_cursor)
            scan_cursor = policy::next_frontier(scan_cursor, groups.size());
        auto& g = groups[i];
        if (round < g.retry_round) continue;
        const int walk = std::max(0, distance(position, g.anchor) - attack_range);
        bool available = false;
        const bool seen = group_seen(g.group, visible);
        if (seen) {
            const auto state = g.group.state();
            if (const auto* respawn = std::get_if<cambc::map::camp_group_respawning>(&state)) {
                g.ready_round = round + std::max(1, respawn->timer);
                if (respawn->timer > walk + 5) {
                    g.retry_round = std::min(g.ready_round, round + retry_delay);
                    continue;
                }
            } else {
                g.ready_round = 0;
                available = std::holds_alternative<cambc::map::camp_group_reward_available>(state);
            }
        }
        // Occupancy alone is enough to avoid duplicating a completed capture.
        bool collector = false;
        float team_dps = strength * 1.125f;
        float ally_near = 0;
        for (const auto& ally : allies) {
            if (ally == me || !ally.is_visible() || !ally.is_alive()) continue;
            const auto ap = ally.position();
            if (g.spawns.is_set(ap)) collector = true;
            if (distance(ap, g.anchor) <= 6) {
                team_dps += ally.strength();
                ally_near += 1;
            }
        }
        if (available && collector) continue;
        float hp = g.initial_health, incoming = g.initial_strength;
        if (seen && g.ready_round == 0) {
            hp = 0; incoming = 0;
            for (const auto& c : g.group.camps()) {
                if (!visible.is_set(c.spawn_position())) {
                    const auto s = c.base_stats();
                    hp += s.base_health; incoming += s.base_strength;
                } else if (c.is_visible() && c.health() > 0) {
                    hp += c.health(); incoming += c.strength();
                }
            }
        }
        if (available) hp = incoming = 0;
        if (me.passive() == cambc::passive_type::splash_attack && g.count > 1)
            team_dps += strength * 0.6f;
        const float clear = hp / std::max(1.0f, team_dps);
        // A single monster deals full damage until dead. Groups lose attackers
        // progressively; price half their combined damage across the clear.
        const float loss = clear * incoming * mitigation
            * (g.count == 1 ? 1.0f : 0.65f);
        const float value = g.gems + policy::gold_value(cash) * g.gold;
        const float wait = g.ready_round > round + walk ? g.ready_round - round - walk : 0;
        float score = value / (walk + wait + clear + 6.0f);
        // Soft dispersion preserves help on monsters but avoids cluster sharing.
        if (incoming == 0 && ally_near > 0 && target_group != static_cast<int>(i)) score *= 0.3f;
        if (target_group == static_cast<int>(i)) score *= 1.25f;
        if (available) score *= 2;
        if (loss > policy::risk_fraction * me.health()) {
            if (score > rally_score) { rally = i; rally_score = score; }
            continue;
        }
        if (score > best_score) { chosen = i; best_score = score; }
    }
    if (chosen < 0) {
        // Fuel deferral is not evidence that this target is invalid. Preserve
        // intent for a fresh turn rather than repeatedly rebuilding the planner.
        if (!scan_complete) return;
        if (committed) {
            // Distinguish an invalid commitment from having searched all goals.
            target_group = -1;
            plan_valid = false;
            return;
        }
        if (me.gem_count()) { bank(); return; }
        if (rally >= 0) {
            // On monster-only maps gather outside attack range before pulling.
            auto& g = groups[rally];
            target_group = rally;
            int radius = 4;
            for (const auto& c : g.group.camps()) radius = std::max(radius, c.attack_range() + 1);
            if (distance(position, g.anchor) > radius)
                move_to(around(g.anchor, radius) & ~around(g.anchor, radius - 1));
            else if (me.health() < me.max_health() * 0.85f && !exposed(position)) {
                recovering = true; me.recall();
            }
            return;
        }
        // In particular vacate an occupied respawn region, rather than waiting
        // on the exact tile whose occupancy prevents the next crop.
        if (me.can_move()) move_to(cambc::map::spawn_region(team::ally));
        return;
    }
    target_group = chosen;
    auto& g = groups[chosen];
    // Keep the chosen objective, but consume restored allowances instead of
    // ending the turn after the first kill. Visibility, position, life state and
    // reward state are observed again after every attack, cast and movement.
    bool walked = false;
    const auto ready = [&] {
        return me.is_alive() && cambc::fuel_remaining() >= lock_reserve;
    };
    const auto reward_ready = [&] {
        if (!group_seen(g.group, cambc::vision::visible_tiles())) return false;
        return std::holds_alternative<cambc::map::camp_group_reward_available>(g.group.state());
    };
    const auto strike = [&] {
        if (!me.can_attack() && !me.can_cast()) return false;
        std::optional<cambc::camp> target;
        float hp = std::numeric_limits<float>::max();
        for (const auto& c : g.group.camps()) {
            if (!ready()) return false;
            if (c.is_visible() && c.health() > 0
                && distance(me.position(), c.position()) <= me.attack_range() && c.health() < hp) {
                target = c; hp = c.health();
            }
        }
        if (target && fight(*target, walked)) return true;
        // A ranged spell can make progress before walking. No stale camp list
        // or target state from before the preceding action authorizes this call.
        for (const auto& c : g.group.camps()) {
            if (!ready()) return false;
            if (fight(c, walked)) return true;
        }
        return false;
    };
    const auto advance = [&](bool capture) {
        auto goals = g.spawns;
        if (!capture) {
            cambc::bitboard approaches;
            for (const auto& c : g.group.camps()) {
                if (!ready()) return;
                if (c.is_visible() && c.health() > 0)
                    approaches |= around(c.position(), me.attack_range());
            }
            if (!approaches.is_empty()) goals = std::move(approaches);
            else if (g.ready_round > round) goals = around(g.anchor, 2) & ~g.spawns;
        }
        const auto origin = me.position();
        const bool could_move = me.can_move();
        bool deferred = false;
        if (move_to(goals, &deferred)) {
            walked = walked || me.position() != origin;
        } else if (policy::exclude_target(could_move, deferred, goals.is_set(me.position()))) {
            g.retry_round = round + retry_delay;
            target_group = -1;
            plan_valid = false;
        }
    };
    policy::harvest_turn(ready, reward_ready, strike, advance);
}

void Bot::diagnostic(const char* stage) const {
    if (cambc::round_number() % 100 != 0) return;
    const auto pos = cambc::self().position();
    std::cout << "frontier round=" << cambc::round_number() << " pos=" << pos.x << ',' << pos.y
        << " stage=" << stage << " fuel=" << cambc::fuel_remaining()
        << " target=" << target_group << " groups=" << groups.size() << '\n';
}

void Bot::play_turn() {
    auto& me = cambc::self();
    if (me.is_alive() && (me.is_recalling() || me.is_submitting_gems() || me.is_teleporting())) return;
    buy_items();
    if (!me.is_alive()) { recovering = false; target_group = -1; return; }
    if (!me.can_move() && !me.can_attack() && !me.can_cast()) return;
    lock_nearby_altar();
    const auto& spawn = cambc::map::spawn_region(team::ally);
    if (spawn.is_set(me.position())) {
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
    if (!initialized) initialize();
    diagnostic("ready");
    if (cambc::fuel_remaining() < scan_reserve) return;
    if (hold_capture()) return;

    int altar_distance = 10000;
    for (auto altar : cambc::map::altars().positions())
        altar_distance = std::min(altar_distance, std::max(0, distance(me.position(), altar) - cambc::constants::submit_gems_range));
    if (policy::bank_now(me.gem_count(), altar_distance, cambc::round_number(),
            cambc::constants::max_rounds, cambc::global_submitted_gems(team::ally), cambc::constants::winning_gems)) {
        bank(); return;
    }
    // Take useful defensive exchanges, without chasing enemies off our route.
    for (const auto& enemy : cambc::vision::champions(team::enemy))
        if (enemy.is_visible() && enemy.health() > 0
            && distance(me.position(), enemy.position()) <= me.attack_range()
            && (enemy.health() <= me.strength() * 2
                || distance(me.position(), enemy.position()) <= enemy.attack_range()))
            if (fight(enemy)) return;
    if (me.gold_count() >= shopping_gold && me.champion_name() != cambc::champion_type::tavi
        && me.gem_count() == 0 && !spawn.is_set(me.position()) && !exposed(me.position())) {
        recovering = true; target_group = -1; me.recall(); return;
    }
    diagnostic("farm");
    farm_camps();
    diagnostic("yield");
}
