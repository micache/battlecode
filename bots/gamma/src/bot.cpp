#include "bot.h"
#include "plan.h"
#include <algorithm>
#include <array>
#include <cmath>
#include <iostream>
#include <limits>
#include <variant>

namespace bc = cambc;
using bc::vec2;
using bc::team;
namespace {
int dist(vec2 a, vec2 b) { return static_cast<int>(a.chebyshev_distance(b)); }
bc::bitboard around(vec2 p, int r) {
    bc::bitboard b; b.draw_chebyshev(p, r); return b;
}
float cast_range(const bc::ability& a) {
    return std::visit([](const auto& x) -> float {
        if constexpr (requires { x.range; }) return x.range;
        else return 0;
    }, a.info().value());
}
bool exclusive(const bc::ability& a) {
    return std::visit([](const auto& x) { return x.exclusive_with_movement; }, a.info().value());
}
bc::bitboard blockers(const bc::bitboard& terrain) {
    auto b = terrain | bc::vision::champion_tiles() | bc::vision::camp_tiles() | bc::vision::teleport_tiles();
    b.set(bc::self().position(), false); return b;
}
bool usable(const bc::unit& t) { return t.is_visible() && t.health() > 0; }
}

void Bot::initialize() {
    auto& me = bc::self();
    terrain = bc::map::walls() | bc::map::holes() | bc::map::altars() | bc::map::spawn_region(team::enemy);
    spawn = bc::map::spawn_region(team::ally);
    altars = bc::map::altars().positions();
    for (auto a : altars) altar_goals |= around(a, bc::constants::submit_gems_range);
    altar_goals &= ~terrain;
    // Static topology only: occupants are refreshed separately for legal moves.
    // First play has 2x fuel; cache the bank field once, not per route query.
    altar_field.emplace();
    bc::bitboard visited;
    altar_field->compute(terrain, altar_goals, visited);
    const auto& bytes = bc::draft_memory;
    if (bytes.size() >= policy::plan_header && std::to_integer<int>(bytes[0]) == 'G'
        && std::to_integer<int>(bytes[1]) == 'A' && std::to_integer<int>(bytes[2]) == 1) {
        const auto n = std::to_integer<unsigned>(bytes[3]) + (std::to_integer<unsigned>(bytes[4]) << 8);
        if (n <= policy::max_groups && 5 + 2*n <= bytes.size()) {
            routes.reserve(n);
            for (unsigned i = 0; i < n; ++i) {
                const vec2 p{std::to_integer<int>(bytes[5+2*i]), std::to_integer<int>(bytes[6+2*i])};
                if (bc::map::is_in_bounds(p)) routes.push_back(Route{p});
            }
        }
    }
    // No per-body shared-memory records: visible allies and deterministic route
    // affinity coordinate work. All eight live shared bytes remain untouched.
    const auto roster = bc::champions(team::ally);
    for (unsigned i = 0; i < roster.size(); ++i) if (roster[i] == me) slot = i;
    me.set_priority(100 - slot);
    initialized = true;
}

void Bot::refresh_travel() {
    travel_position = bc::self().position();
    if (travel_field) {
        // Use topological displacement, not straight-line separation: walking
        // around a wall can return geometrically near the old origin.
        const auto d = travel_field->get(travel_position);
        if (d == bc::distance_field::unreachable) {
            // Recall/respawn can change connected component. Old unreachable
            // observations must not veto the new component's objectives.
            travel_field.reset();
            travel_round = -1;
            for (auto& r : routes) r.travel = -1;
        } else travel_displacement = d;
    }
    if (travel_round >= 0 && travel_displacement < policy::travel_refresh_steps
        && now - travel_round < policy::travel_refresh_rounds) return;
    // At most one field, with room for a normal legal action and turn yield.
    if (bc::fuel_remaining() < policy::distance_floor) return;
    if (!travel_field) travel_field.emplace();
    bc::bitboard visited;
    travel_field->compute(terrain, around(travel_position, 0), visited);
    travel_displacement = 0;
    travel_round = now;
    for (auto& r : routes) {
        const auto d = travel_field->get(r.anchor);
        r.travel = d == bc::distance_field::unreachable ? policy::unreachable : d;
    }
}

int Bot::route_distance(int i) const {
    return policy::route_distance(routes[i].travel, travel_displacement,
        dist(travel_position, routes[i].anchor));
}

void Bot::buy_items() {
    using I = bc::item_type;
    auto& me = bc::self();
    const auto count = me.item_count();
    struct Stage { I shard, emblem; };
    const std::array stages{Stage{I::jungle_shard_of_strength, I::jungle_emblem_of_strength},
        Stage{I::monster_shard_of_strength, I::monster_emblem_of_strength},
        Stage{I::durability_shard_of_health, I::durability_emblem_of_health}};
    for (const auto& stage : stages) {
        if (count[stage.emblem]) continue;
        const unsigned n = std::min(5u-count[stage.shard], me.gold_count()/stage.shard.cost());
        if (n && me.can_buy(stage.shard, n)) me.buy(stage.shard, n);
        if (n + count[stage.shard] < 5) return;
    }
    const unsigned n = me.gold_count()/I::power_shard_of_strength.cost();
    if (n && me.can_buy(I::power_shard_of_strength, n)) me.buy(I::power_shard_of_strength, n);
    if (me.can_buy(bc::consumable_type::altar_lock)) me.buy(bc::consumable_type::altar_lock);
}

bool Bot::walk(bc::bitboard goals, bool dash) {
    auto& me = bc::self();
    if (!me.can_move() || bc::fuel_remaining() < policy::action_floor) return false;
    // At most two attempts: a hidden blocker can be revealed without consuming
    // an allowance. Rebuild occupants, never path onto a known blocked goal.
    for (int attempt = 0; attempt < 2 && bc::fuel_remaining() >= policy::action_floor; ++attempt) {
        auto blocked = blockers(terrain);
        auto free_goals = goals & ~blocked;
        const auto origin = me.position();
        if (free_goals.is_empty() || free_goals.is_set(origin)) return false;
        bc::distance_field f;
        bc::bitboard visited;
        f.compute_to(blocked, free_goals, around(origin, 0), visited);
        if (dash && me.can_cast() && bc::fuel_remaining() > 27000) {
            for (const auto& a : me.abilities()) {
                if (!a.is_dash() || !a.is_ready()) continue;
                // Conservative legal dash path: ordinary passable intermediate
                // tiles only. This forgoes hole crossing rather than guessing.
                auto candidates = blocked.reachable_tiles(origin, 2) & a.valid_tiles() & ~blocked;
                auto best = origin;
                for (auto p : candidates.positions()) if (f.get(p) < f.get(best)) best = p;
                if (dist(origin, best) == 2 && f.get(best) + 1 < f.get(origin) && a.use(best)) return true;
            }
        }
        auto best = origin;
        for (auto p : blocked.reachable_tiles(origin, me.base_stats().base_move_speed).positions())
            if (f.get(p) < f.get(best)) best = p;
        if (best == origin) { ++stuck; return false; }
        if (me.move_absolute(best)) { stuck = 0; return true; }
        ++stuck;
    }
    return false;
}

bool Bot::threatened(vec2 p) {
    for (const auto& e : bc::vision::champions(team::enemy))
        if (e.is_visible() && e.health() > 0 && dist(p, e.position()) <= std::max(5, e.attack_range()+1)) return true;
    for (auto t : bc::vision::awake_camp_tiles().positions()) {
        auto c = bc::vision::camp_at(t);
        if (c.is_visible() && dist(p,t) <= c.attack_range()) return true;
    }
    return false;
}

void Bot::shield() {
    auto& me = bc::self();
    if (!me.can_cast() || me.buffs().has_shield()) return;
    for (const auto& a : me.abilities())
        if (a.is_shield() && a.can_target_self() && a.is_ready()) { a.use(); return; }
}

bool Bot::bank() {
    auto& me = bc::self();
    if (!me.gem_count() || !me.can_move() || !me.can_attack()) return false;
    // A hostile lock adds five hits; prefer an unlocked altar when available,
    // but keep locked altars reachable if all local routes are locked.
    auto tribute_here = [&]() {
        for (auto a : altars) {
            if (dist(me.position(),a) > bc::constants::submit_gems_range) continue;
            const auto enemy_locks = bc::vision::altar_lock_tiles(team::enemy);
            if (enemy_locks.is_set(a)) {
                if (me.can_attack()) {
                    for (const auto& lock : bc::vision::altar_locks(team::enemy))
                        if (lock.position() == a) { me.attack(lock); break; }
                }
                return true;
            }
            const auto& lock = me.consumables()[bc::consumable_type::altar_lock];
            if (lock.count() && !bc::vision::altar_lock_tiles(team::ally).is_set(a)
                && !me.restrictions().contains(bc::buff_restrictions::consumable)) lock.use(a);
            me.submit_gems(a);
            return true;
        }
        return false;
    };
    if (tribute_here()) return true;
    auto goals = altar_goals;
    bc::bitboard unlocked;
    const auto hostile = bc::vision::altar_lock_tiles(team::enemy);
    for (auto a : altars) if (!hostile.is_set(a)) unlocked |= around(a, bc::constants::submit_gems_range);
    if (!unlocked.is_empty()) goals &= unlocked;
    // Walking is compatible with melee tribute. Refresh position and locks on
    // arrival, and start the channel immediately rather than wasting a round.
    walk(goals, true);
    tribute_here();
    return true;
}

bool Bot::fight(bool moved, bool champions_only) {
    auto& me = bc::self();
    if (!me.can_attack() && !me.can_cast()) return false;
    std::optional<bc::champion> enemy;
    for (const auto& e : bc::vision::champions(team::enemy)) {
        if (!e.is_visible() || e.health() <= 0 || dist(me.position(),e.position()) > me.attack_range()) continue;
        if (!enemy || e.health() < enemy->health()) enemy = e;
    }
    std::optional<bc::camp> camp;
    if (!enemy && !champions_only && target >= 0 && routes[target].group) {
        for (const auto& c : routes[target].group->camps()) {
            if (!c.is_visible() || c.health() <= 0) continue;
            if (dist(me.position(),c.position()) > std::max(4, me.attack_range())) continue;
            if (!camp || (dist(me.position(),c.position()) <= me.attack_range()
                && dist(me.position(),camp->position()) > me.attack_range())
                || (dist(me.position(),c.position()) <= me.attack_range()
                    && c.health() < camp->health())) camp = c;
        }
    }
    const bc::unit* t = enemy ? static_cast<const bc::unit*>(&*enemy) : camp ? static_cast<const bc::unit*>(&*camp) : nullptr;
    if (!t) return false;
    bool acted = false;
    auto cast_damage = [&]() {
        for (const auto& a : me.abilities()) {
            if (!me.can_cast() || !a.is_ready() || (exclusive(a) && moved)) continue;
            if (!(a.is_damage() || a.is_cc() || a.is_aoe_damage())) continue;
            if (dist(me.position(),t->position()) > cast_range(a)) continue;
            if (a.is_aoe_damage() && a.can_target_ground()) return a.use(t->position());
            if (enemy && a.can_target_enemies()) return a.use(*enemy);
            if (camp && a.can_target_camps()) return a.use(*camp);
        }
        return false;
    };
    // Reset after a real attack. Re-check the target after each action: a basic,
    // Varg splash, or spell can kill it, and Vendetta can refresh cooldowns.
    if (me.can_attack() && dist(me.position(),t->position()) <= me.attack_range()) {
        me.attack(*t); acted = true;
        if (!usable(*t)) return true;
        for (const auto& a : me.abilities()) {
            if (a.is_attack_reset() && a.is_ready() && a.can_target_self()) {
                if (a.use() && me.can_attack() && usable(*t)
                    && dist(me.position(),t->position()) <= me.attack_range()) me.attack(*t);
                break;
            }
        }
    }
    if (usable(*t) && me.can_cast()) acted = cast_damage() || acted;
    return acted;
}

bool Bot::load_route(int i) {
    auto& r = routes[i];
    if (r.group) return true;
    if (bc::fuel_remaining() < policy::planning_floor) return false;
    r.group = bc::map::camp(r.anchor).camp_group();
    for (const auto& c : r.group->camps()) {
        const auto stats = c.base_stats();
        r.hp += stats.base_health; r.strength += stats.base_strength;
    }
    return true;
}

void Bot::observe(int i, const bc::bitboard& visible) {
    auto& r = routes[i];
    if (!r.group) return;
    bool seen = false;
    for (const auto& c : r.group->camps()) if (visible.is_set(c.spawn_position())) { seen = true; break; }
    if (!seen) return;
    const auto state = r.group->state();
    r.observed_at = now;
    if (auto* s = std::get_if<bc::map::camp_group_respawning>(&state)) {
        r.state = 3; r.ready_at = now + std::max(1,s->timer);
    } else r.state = std::holds_alternative<bc::map::camp_group_reward_available>(state) ? 2 : 1;
}

bool Bot::recovery_cashout() {
    auto& me = bc::self();
    if (now >= recovery_cashout_until || !policy::cashout_healthy(me.health(), me.max_health())
        || !me.can_move() || !me.can_attack()
        || bc::fuel_remaining() < policy::cashout_fuel_floor) return false;
    const auto visible = bc::vision::visible_tiles();
    // Current visible observations only. The safety mask is a conservative
    // one-step threat estimate, not a claim that unseen reinforcements are absent.
    const auto observed_danger = [&](bc::bitboard& danger, std::uint64_t reserve) {
        for (const auto& e : bc::vision::champions(team::enemy)) {
            if (bc::fuel_remaining() < reserve) return false;
            if (e.is_visible() && e.health() > 0)
                danger |= around(e.position(), std::max(5, e.attack_range() + e.base_stats().base_move_speed));
        }
        int inspected = 0;
        for (auto p : bc::vision::awake_camp_tiles().positions()) {
            if (++inspected > 16 || bc::fuel_remaining() < reserve) return false;
            const auto c = bc::vision::camp_at(p);
            if (c.is_visible() && c.health() > 0)
                danger |= around(c.position(), c.attack_range() + c.base_stats().base_move_speed);
        }
        return bc::fuel_remaining() >= reserve;
    };
    bc::bitboard danger;
    if (!observed_danger(danger, 35000)) return false;
    if (danger.is_set(me.position())) return false;
    // Finish an already occupied, cleared camp before healing. Never start a
    // new clear or travel to a capture here; each extra turn consumes the same
    // episode deadline, and new danger aborts this opportunity permanently.
    if (target >= 0 && routes[target].group) {
        observe(target, visible);
        const auto& r = routes[target];
        if (r.state == 2 && r.observed_at == now && r.group->spawn_tiles().is_set(me.position())) {
            ++cashout_captures;
            return true;
        }
    }
    if (!me.gem_count()) return false;
    auto blocked = blockers(terrain) | danger | ~visible;
    bc::bitboard goals;
    const auto hostile = bc::vision::altar_lock_tiles(team::enemy);
    for (auto a : altars)
        if (visible.is_set(a) && !hostile.is_set(a))
            goals |= around(a, bc::constants::submit_gems_range);
    goals &= ~blocked;
    if (goals.is_empty()) return false;
    // The whole approach must be currently visible and free of modeled danger.
    // Unlike the ordinary bank route this never detours toward a hidden altar.
    bc::distance_field field;
    bc::bitboard visited;
    field.compute_to(blocked, goals, around(me.position(), 0), visited);
    const auto d = field.get(me.position());
    if (d == bc::distance_field::unreachable
        || !policy::cashout_fits(d, me.gem_count(), recovery_cashout_until - now)
        || bc::fuel_remaining() < policy::action_floor) return false;
    if (d > 0) {
        auto best = me.position();
        for (auto p : blocked.reachable_tiles(best, me.base_stats().base_move_speed).positions())
            if (field.get(p) < field.get(best)) best = p;
        if (best == me.position()) return false;
        // A newly revealed blocker is not a failed submission. Replan next turn
        // within the fixed deadline; no stale path or mask is retained.
        if (!me.move_absolute(best)) return true;
    }
    // Movement can reveal an enemy or lock. Refresh before starting tribute;
    // a fresh threat aborts further cash-out attempts in this recovery episode.
    bc::bitboard fresh_danger;
    if (!observed_danger(fresh_danger, 24000) || fresh_danger.is_set(me.position())) {
        recovery_cashout_until = 0;
        return true;
    }
    const auto fresh_visible = bc::vision::visible_tiles();
    const auto fresh_hostile = bc::vision::altar_lock_tiles(team::enemy);
    if (me.can_attack()) for (auto a : altars)
        if (fresh_visible.is_set(a) && !fresh_hostile.is_set(a)
            && dist(me.position(), a) <= bc::constants::submit_gems_range) {
            me.submit_gems(a);
            ++cashout_submissions;
            break;
        }
    return true;
}

void Bot::recover() {
    auto& me = bc::self();
    if (recovery_cashout()) return;
    // No safe, short conversion remains. Do not retry or renew the deadline
    // until this body has actually recovered at spawn (or died).
    recovery_cashout_until = 0;
    target = -1;
    if (spawn.is_set(me.position())) { recovering = false; return; }
    if (!threatened(me.position()) && me.can_move() && me.can_attack()) { me.recall(); return; }
    shield();
    walk(spawn, true);
    // Damage interrupts recall. Only channel after a fresh post-move threat
    // check and while both allowances remain (dash may preserve them).
    if (!spawn.is_set(me.position()) && !threatened(me.position()) && me.can_move() && me.can_attack()) me.recall();
    else fight(true, true);
}

void Bot::farm() {
    auto& me = bc::self();
    if (routes.empty()) { fight(false); return; }
    refresh_travel();
    const auto visible = bc::vision::visible_tiles();
    if (target >= 0) {
        observe(target, visible);
        auto& r = routes[target];
        if (r.state == 2 && r.observed_at == now && r.group->spawn_tiles().is_set(me.position())) return;
        if (stuck >= 8) { r.ready_at = now + 12; stuck = 0; }
        if (r.ready_at > now) target = -1;
    }
    // Cheap global shortlist, then bounded live evaluation. Committed and
    // rotating probe slots prevent permanent exclusion by the shortlist.
    std::vector<std::pair<int,int>> near;
    near.reserve(policy::shortlist+2);
    for (unsigned i = 0; i < routes.size(); ++i) {
        if (routes[i].ready_at > now) continue;
        const int d = route_distance(i);
        if (d == policy::unreachable) continue;
        auto at = std::lower_bound(near.begin(), near.end(), std::pair{d,static_cast<int>(i)});
        near.insert(at,{d,static_cast<int>(i)});
        if (near.size() > policy::shortlist) near.pop_back();
        if (i % 32 == 0 && bc::fuel_remaining() < policy::planning_floor) break;
    }
    if (target >= 0 && route_distance(target) < policy::unreachable) near.insert(near.begin(), {0,target});
    const int probe = cursor++ % routes.size();
    if (routes[probe].ready_at <= now && route_distance(probe) < policy::unreachable)
        near.push_back({route_distance(probe),probe});
    float best_score = -1;
    int best = target >= 0 && route_distance(target) < policy::unreachable
        && routes[target].ready_at <= now ? target : -1;
    const auto allies = bc::vision::champions(team::ally);
    const auto items = me.item_count();
    const float mitigation = (items[bc::item_type::jungle_emblem_of_strength] ? 0.7f : 1.0f)
        * (items[bc::item_type::durability_emblem_of_health] ? 0.9f : 1.0f);
    for (auto [unused,i] : near) {
        if (bc::fuel_remaining() < policy::planning_floor) break;
        if (!load_route(i)) break;
        observe(i, visible);
        auto& r = routes[i];
        if (r.ready_at > now) continue;
        const auto& g = *r.group;
        if (r.state == 2 && r.observed_at == now) {
            bool collector = false;
            const auto tiles = g.spawn_tiles();
            for (const auto& a : allies) if (a != me && a.is_visible() && tiles.is_set(a.position())) collector = true;
            if (collector) continue;
        }
        float hp = r.hp;
        // Use current HP only for visible members. Invisible members retain
        // their immutable design estimate, never cached live health.
        for (const auto& c : g.camps()) {
            if (c.is_visible()) hp += c.health() - c.base_stats().base_health;
            else if (visible.is_set(c.spawn_position()) && !bc::vision::has_camp(c.spawn_position())) hp -= c.base_stats().base_health;
        }
        hp = std::max(0.0f,hp);
        if (r.state == 2 && r.observed_at == now) hp = 0;
        const float splash = me.champion_name() == bc::champion_type::varg ? std::min(2.5f,static_cast<float>(g.camps().size())) : 1.0f;
        const float clear = hp / std::max(1.0f,me.strength()*1.12f*splash);
        const float exposure = 0.45f * clear * r.strength * mitigation;
        // Soft recovery cost rather than an absolute risk veto: hard exclusions
        // previously regressed on another edit base. Large camps are penalized.
        float score = policy::route_score(policy::value(g.gem_value(),g.gold_value(),now),
            route_distance(i), clear + 20.0f*exposure/std::max(1.0f,me.health()), bc::constants::capture_time);
        if (exposure > me.health()) score *= 0.15f;
        if (i == target) score *= 1.30f;
        // Stable affinity spreads the opening; a visible nearer ally overrides
        // affinity and discourages duplicate clear/capture work.
        if (i % 5 == static_cast<unsigned>(slot)) score *= 1.15f;
        for (const auto& a : allies) if (a != me && a.is_visible()
            && dist(a.position(),r.anchor)+2 < dist(me.position(),r.anchor)) score *= 0.65f;
        if (score > best_score) { best_score = score; best = i; }
    }
    target = best;
    if (target < 0 || !routes[target].group) {
        // No reachable work: deliver even a small bag before recovery.
        if (me.gem_count() && altar_field->get(me.position()) != bc::distance_field::unreachable) bank();
        else recover();
        return;
    }
    auto& r = routes[target];
    observe(target, bc::vision::visible_tiles());
    if (r.state == 3 && r.observed_at == now) { target = -1; walk(around(me.position(),1) & ~r.group->spawn_tiles()); return; }
    if (r.state == 2 && r.observed_at == now) {
        walk(r.group->spawn_tiles(),true); return;
    }
    fight(false);
    if (bc::fuel_remaining() < policy::action_floor) return;
    // A kill may expose the now-empty capture tile during the same turn.
    observe(target,bc::vision::visible_tiles());
    if (r.state == 2 && r.observed_at == now) { walk(r.group->spawn_tiles()); return; }
    bc::bitboard goals;
    for (const auto& c : r.group->camps()) {
        if (c.is_visible() && c.health() > 0) goals |= around(c.position(),me.attack_range());
        else if (!bc::vision::in_vision(c.spawn_position())) goals |= around(c.spawn_position(),1);
    }
    const bool moved = walk(goals,true);
    if (bc::fuel_remaining() > policy::action_floor) fight(moved);
    if (bc::fuel_remaining() > policy::action_floor && me.can_move()) {
        observe(target,bc::vision::visible_tiles());
        if (r.state == 2 && r.observed_at == now) walk(r.group->spawn_tiles());
    }
}

void Bot::log(const char* mode) {
    if (now-last_log < 100 || bc::fuel_remaining() < 6000) return;
    last_log = now;
    auto& me = bc::self();
    std::cout << "r=" << now << " mode=" << mode << " target=" << target
        << " hp=" << static_cast<int>(me.health()) << " gems=" << me.gem_count()
        << " xy=" << me.position().x << "," << me.position().y
        << " route_age=" << (travel_round < 0 ? -1 : now-travel_round)
        << " cashout=" << cashout_captures << "," << cashout_submissions
        << " fuel=" << bc::fuel_remaining() << '\n';
}

void Bot::play_turn() {
    auto& me = bc::self();
    now = bc::round_number();
    if (!me.is_alive()) { buy_items(); target = -1; recovering = false; recovery_cashout_until = 0; return; }
    if (me.is_recalling() || me.is_submitting_gems() || me.is_teleporting()) return;
    if (!initialized) initialize();
    if (!me.can_move() && !me.can_attack() && !me.can_cast()) return;
    const bool home = spawn.is_set(me.position());
    if (home) {
        buy_items();
        if (me.health() < policy::leave_spawn_fraction*me.max_health()) { log("heal"); return; }
        recovering = false;
        recovery_cashout_until = 0;
    }
    if (me.health() < policy::retreat_fraction*me.max_health() && !home && !recovering) {
        recovering = true;
        recovery_cashout_until = now + policy::recovery_cashout_rounds;
    }
    if (recovering) { recover(); log("recover"); return; }
    // Preserve uncontested capture even when carrying an earlier small bag.
    if (target >= 0 && routes[target].group) {
        observe(target,bc::vision::visible_tiles());
        if (routes[target].state == 2 && routes[target].observed_at == now
            && routes[target].group->spawn_tiles().is_set(me.position())) {
            if (threatened(me.position())) { shield(); fight(false,true); }
            log("capture"); return;
        }
    }
    const auto bank_distance = altar_field->get(me.position());
    const int altar_distance = bank_distance == bc::distance_field::unreachable
        ? policy::unreachable : bank_distance;
    const int gems = me.gem_count();
    if (gems && altar_distance < policy::unreachable && (gems >= policy::bank_bag || altar_distance <= policy::near_bank
        || gems + bc::global_submitted_gems(team::ally) >= bc::constants::winning_gems
        || now + altar_distance + policy::tribute_ticks(gems)+25 >= static_cast<int>(bc::constants::max_rounds))) {
        bank(); log("bank"); return;
    }
    // Do not let empty-bag farming devolve into unwinnable PvP. Visible local
    // power is a policy estimate, not knowledge of unseen reinforcements.
    float ours = me.health()*me.strength(), theirs = 0;
    bool enemy_near = false;
    for (const auto& a : bc::vision::champions(team::ally))
        if (a != me && a.is_visible() && dist(a.position(),me.position()) <= 5) ours += a.health()*a.strength();
    for (const auto& e : bc::vision::champions(team::enemy))
        if (e.is_visible() && dist(e.position(),me.position()) <= 5) { theirs += e.health()*e.strength(); enemy_near = true; }
    if (enemy_near && theirs > 1.2f*ours && !home) {
        shield(); walk(spawn,true); fight(true,true); log("evade"); return;
    }
    if (enemy_near && fight(false,true)) { log("defend"); return; }
    const int shop_gold = me.item_count()[bc::item_type::jungle_emblem_of_strength] ? 300 : 150;
    if (!home && gems == 0 && me.gold_count() >= static_cast<unsigned>(shop_gold) && !threatened(me.position())
        && me.can_move() && me.can_attack()) { me.recall(); target = -1; log("shop"); return; }
    if (me.health() < 0.85f*me.max_health() && threatened(me.position())) shield();
    farm();
    log("farm");
}
