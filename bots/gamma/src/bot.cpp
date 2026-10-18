#include <cambc.h>
#include "bot.h"
#include "combat_value.h"
#include <array>
#include <span>
#include <algorithm>
#include <cmath>
#include <limits>
#include <optional>
#include <type_traits>
#include <variant>

using cambc::vec2;
using cambc::team;
namespace {
constexpr float RETREAT_HEALTH = 0.35f;
constexpr float HEALED_HEALTH = 0.98f;
constexpr unsigned SHOP_RECALL_GOLD = 300;
constexpr std::uint64_t PLAN_FUEL = 30000;
constexpr std::uint64_t ACTION_FUEL = 10000;

int distance(vec2 a, vec2 b) { return static_cast<int>(a.chebyshev_distance(b)); }
cambc::bitboard around(vec2 p, int r) {
    cambc::bitboard mask;
    mask.draw_chebyshev(p, r);
    return mask;
}
cambc::bitboard blocked_tiles() {
    auto result = cambc::map::walls() | cambc::map::holes() | cambc::map::altars()
        | cambc::map::spawn_region(team::enemy) | cambc::vision::champion_tiles()
        | cambc::vision::camp_tiles() | cambc::vision::teleport_tiles();
    result.set(cambc::self().position(), false);
    return result;
}

// Goals are FREE approach/capture tiles, never occupied camps or an altar.
// A failed hidden-obstruction step permits one refreshed alternative.
bool move_to(cambc::bitboard goals) {
    auto& me = cambc::self();
    if (!me.can_move() || me.restrictions().contains(cambc::buff_restrictions::move)
        || cambc::fuel_remaining() < ACTION_FUEL) return false;
    for (int retry = 0; retry < 2; ++retry) {
        auto blocked = blocked_tiles();
        goals &= ~blocked;
        if (goals.is_empty() || goals.is_set(me.position())) return false;
        cambc::distance_field field;
        cambc::bitboard visited;
        field.compute_to(blocked, goals, around(me.position(), 0), visited);
        auto step = me.position();
        auto best = field.get(step);
        for (auto p : blocked.reachable_tiles(me.position(), me.base_stats().base_move_speed).positions()) {
            if (field.get(p) < best) { step = p; best = field.get(p); }
        }
        if (step == me.position()) return false;
        if (me.move_absolute(step)) return true;
        if (!me.can_move() || cambc::fuel_remaining() < ACTION_FUEL) return false;
    }
    return false;
}

// Visibility is checked again after every action; retaliation can kill self.
template<class Target>
bool live(const Target& t) {
    return cambc::self().is_alive() && t.is_visible() && t.health() > 0;
}
// Only the supplied camp group or defensive shortlist may be attacked. No chase.
// Snapshot live observations again after EVERY action; handles are identities only.
constexpr std::uint64_t COMBAT_FUEL = 18000;
constexpr unsigned COMBAT_STEPS = 4;
constexpr unsigned COMBAT_TARGETS = 12;
template<class Target>
bool fight(std::span<const Target> candidates, bool walked) {
    auto& me = cambc::self();
    bool acted = false;
    const bool splash = me.passive() == cambc::passive_type::splash_attack;
    const float strength = me.strength();
    float basic_damage = strength;
    if constexpr (std::is_same_v<Target, cambc::camp>) {
        const auto items = me.item_count();
        if (items[cambc::item_type::monster_emblem_of_strength]
            || items[cambc::item_type::monster_emblem_of_health]
            || items[cambc::item_type::monster_emblem_of_focus]) basic_damage *= 1.1f;
    }
    // A small finishing preference rewards removed threats, not just raw damage.
    const float kill_bonus = strength * 0.25f;
    for (unsigned step = 0; step < COMBAT_STEPS; ++step) {
        if (!me.is_alive() || cambc::fuel_remaining() < COMBAT_FUEL) break;
        const auto restrictions = me.restrictions();
        const bool attack_allowed = !restrictions.contains(cambc::buff_restrictions::attack);
        const auto position = me.position();
        const auto range = me.attack_range();
        std::vector<Target> targets;
        std::array<combat_value::target, COMBAT_TARGETS> observations{};
        unsigned examined = 0;
        for (const auto& t : candidates) {
            if (++examined > COMBAT_TARGETS || cambc::fuel_remaining() < COMBAT_FUEL) break;
            if (!t.is_visible()) continue;
            const float hp = t.health();
            if (hp <= 0) continue;
            const auto p = t.position();
            const auto d = distance(position, p);
            if constexpr (std::is_same_v<Target, cambc::champion>) {
                if (d > range || (d > 1 && hp > 2 * strength)) continue;
            }
            observations[targets.size()] = {p.x, p.y, hp, d <= range};
            targets.push_back(t);
        }
        if (targets.empty()) break;
        const auto view = std::span<const combat_value::target>(observations.data(), targets.size());
        int basic = -1;
        float basic_score = 0;
        for (std::size_t i = 0; i < targets.size(); ++i) {
            if (!view[i].in_range || !attack_allowed) continue;
            const float score = combat_value::basic(view, i, splash, basic_damage, kill_bonus);
            if (score > basic_score) { basic = static_cast<int>(i); basic_score = score; }
        }
        if (basic >= 0 && me.can_attack()) {
            me.attack(targets[basic]);
            acted = true;
            continue; // A kill must not strand the separate cast allowance.
        }
        if (!me.can_cast() || restrictions.contains(cambc::buff_restrictions::cast)) break;
        const auto abilities = me.abilities();
        // Preserve the base's health protection; never replace an active shield.
        if (me.health() < me.max_health() * 0.75f && !me.buffs().has_shield()) {
            bool dangerous = false;
            for (const auto& t : targets)
                if (distance(position, t.position()) <= 3 && t.strength() > 0) { dangerous = true; break; }
            if (dangerous) {
                for (const auto& a : abilities)
                    if (a.is_shield() && a.can_target_self() && a.is_ready() && a.use()) return true;
            }
        }
        std::optional<cambc::ability> selected;
        int aim = -1;
        float best = 0;
        for (const auto& a : abilities) {
            if (cambc::fuel_remaining() < COMBAT_FUEL || !a.info() || !a.is_ready()) continue;
            const bool exclusive = std::visit([](const auto& info) { return info.exclusive_with_movement; }, *a.info());
            if (walked && exclusive) continue;
            if (a.is_attack_reset()) {
                // No range query for a rangeless reset; only buy a useful new hit.
                if (basic >= 0 && !me.can_attack() && a.can_target_self() && basic_score > best) {
                    best = basic_score; selected = a; aim = basic;
                }
                continue;
            }
            if (!(a.is_damage() || a.is_aoe_damage() || a.is_cc())) continue;
            const bool ground = a.is_aoe_damage() && a.can_target_ground();
            const bool unit = std::is_same_v<Target, cambc::camp> ? a.can_target_camps() : a.can_target_enemies();
            if (!ground && !unit) continue;
            const auto valid = a.valid_tiles();
            const float damage = a.damage_amount();
            const int radius = ground ? static_cast<int>(a.get<cambc::ability_aoe_damage>().radius) : 0;
            for (std::size_t i = 0; i < targets.size(); ++i) {
                if (!valid.is_set(targets[i].position())) continue;
                float score = ground ? combat_value::area(view, i, radius, damage, kill_bonus)
                    : combat_value::hit(damage, view[i].health, kill_bonus);
                if constexpr (std::is_same_v<Target, cambc::champion>) {
                    if (a.is_cc() || (ground && a.get<cambc::ability_aoe_damage>().duration > 0))
                        score += strength * 0.25f;
                }
                if (score > best) { best = score; selected = a; aim = static_cast<int>(i); }
            }
        }
        if (!selected || aim < 0 || cambc::fuel_remaining() < ACTION_FUEL) break;
        const auto& target = targets[aim];
        if (!live(target)) break;
        bool cast = false;
        if (selected->is_attack_reset()) {
            cast = selected->use();
            // Complete reset + basic together, including at the loop/fuel boundary.
            if (cast && live(target) && me.can_attack()
                && !me.restrictions().contains(cambc::buff_restrictions::attack)
                && distance(me.position(), target.position()) <= me.attack_range()) me.attack(target);
        } else if (selected->is_aoe_damage() && selected->can_target_ground())
            cast = selected->use(target.position());
        else cast = selected->use(target);
        if (!cast) break; // Bounded fallback after a newly invalid action.
        acted = true; // Rebuild observations; do not assume a killed target survived.
    }
    return acted;
}

bool threatened() {
    auto& me = cambc::self();
    for (const auto& e : cambc::vision::champions(team::enemy))
        if (e.is_visible() && e.health() > 0 && distance(me.position(), e.position()) <= e.attack_range() + 1)
            return true;
    for (const auto& c : cambc::vision::camps())
        if (c.is_visible() && c.health() > 0 && c.strength() > 0
            && distance(me.position(), c.position()) <= c.attack_range()) return true;
    return false;
}

// Score first, fight only adjacent threats/cheap finishes; never chase enemies.
bool defend(bool walked) {
    const auto enemies = cambc::vision::champions(team::enemy);
    return fight<cambc::champion>(enemies, walked);
}

bool bank(bool allow_move) {
    auto& me = cambc::self();
    if (!me.gem_count()) return false;
    auto try_submit = [&]() {
        // Enemy locks, rather than friendly locks, are the obstruction.
        const auto hostile = cambc::vision::altar_lock_tiles(team::enemy);
        for (auto altar : cambc::map::altars().positions()) {
            if (distance(me.position(), altar) > cambc::constants::submit_gems_range) continue;
            if (hostile.is_set(altar) && (!me.can_attack()
                || me.restrictions().contains(cambc::buff_restrictions::attack))) continue;
            me.submit_gems(altar); // May hit a hostile lock; never a boolean.
            return true;
        }
        return false;
    };
    if (try_submit()) return true;
    if (!allow_move) return false;
    cambc::bitboard goals;
    // A locked altar remains reachable: three attacks can clear it.
    for (auto altar : cambc::map::altars().positions())
        goals |= around(altar, cambc::constants::submit_gems_range);
    if (move_to(goals)) try_submit(); // Refresh vision and position after walking.
    return true;
}
} // namespace

void Bot::buy_items() {
    auto& me = cambc::self();
    using I = cambc::item_type;
    // Strength powers every basic/reset/splash. Complete each passive once.
    for (auto pair : {std::pair{I::jungle_shard_of_strength, I::jungle_emblem_of_strength},
                      std::pair{I::monster_shard_of_strength, I::monster_emblem_of_strength}}) {
        const auto counts = me.item_count();
        if (counts[pair.second]) continue;
        const unsigned need = pair.first.combine_count() - counts[pair.first];
        const unsigned count = std::min(need, me.gold_count() / pair.first.cost());
        if (count && me.can_buy(pair.first, count)) me.buy(pair.first, count);
        if (!me.item_count()[pair.second]) return;
    }
    const auto item = I::power_shard_of_strength;
    const unsigned count = me.gold_count() / item.cost();
    if (count && me.can_buy(item, count)) me.buy(item, count);
}

void Bot::farm_camps() {
    auto& me = cambc::self();
    if (farms.empty()) {
        for (const auto& group : cambc::map::camp_groups())
            farms.push_back({group, group.spawn_tiles(), 0});
    }
    const unsigned now = cambc::round_number();
    const auto visible = cambc::vision::visible_tiles();
    const auto allies = cambc::vision::champion_tiles(team::ally);
    const auto enemies = cambc::vision::champion_tiles(team::enemy);
    // Retain capture occupancy even if another camp/enemy could be attacked.
    for (std::size_t i = 0; i < farms.size(); ++i) {
        const auto& f = farms[i];
        if (f.spawns.is_set(me.position())
            && std::holds_alternative<cambc::map::camp_group_reward_available>(f.group.state())) {
            target_group = static_cast<int>(i);
            defend(false);
            return;
        }
    }
    if (cambc::fuel_remaining() < PLAN_FUEL) {
        // Cheap legal fallback; no search or hidden state reads.
        unsigned inspected = 0;
        for (const auto& c : cambc::vision::camps()) {
            if (++inspected > 8 || cambc::fuel_remaining() < ACTION_FUEL) break;
            if (!c.is_monolith() && c.is_visible() && c.health() > 0
                && distance(me.position(), c.position()) <= me.attack_range()
                && fight<cambc::camp>(std::span<const cambc::camp>(&c, 1), false)) return;
        }
        return;
    }
    const auto blocked = blocked_tiles();
    cambc::distance_field travel;
    cambc::bitboard visited;
    travel.compute(blocked, around(me.position(), 0), visited);
    int selected = -1;
    float best_score = std::numeric_limits<float>::max();
    for (std::size_t i = 0; i < farms.size(); ++i) {
        if (cambc::fuel_remaining() < PLAN_FUEL) break;
        auto& f = farms[i];
        const bool seen = !(f.spawns & visible).is_empty();
        bool reward = false;
        if (seen) {
            const auto state = f.group.state();
            if (const auto* respawn = std::get_if<cambc::map::camp_group_respawning>(&state)) {
                f.respawn_observed_until = now + std::max(1, respawn->timer);
                continue;
            }
            f.respawn_observed_until = 0;
            reward = std::holds_alternative<cambc::map::camp_group_reward_available>(state);
        } else if (now < f.respawn_observed_until) continue; // Timestamped observation, not hidden truth.
        // Extra collectors do not accelerate capture. A visible ally already on
        // an uncontested cleared group owns collection; we rotate elsewhere.
        if (reward && !(f.spawns & allies).is_empty() && (f.spawns & enemies).is_empty()) continue;
        float hp = 0;
        bool monolith = false;
        cambc::bitboard goals;
        for (const auto& c : f.group.camps()) {
            monolith |= c.is_monolith();
            if (reward) { goals.set(c.spawn_position()); continue; }
            if (c.is_visible()) {
                if (c.health() <= 0) continue;
                hp += c.health();
                goals |= around(c.position(), me.attack_range());
            } else if (!visible.is_set(c.spawn_position())) {
                hp += c.base_stats().base_health; // Explicit uncertain design estimate.
                goals.set(c.spawn_position()); // Enter unseen spawn to reveal, not a blind approach ring.
            }
        }
        if (monolith && !reward) continue; // Do not solo a 20,000-HP, 200-damage objective.
        goals &= ~blocked;
        unsigned dist = cambc::distance_field::unreachable;
        for (auto p : goals.positions()) dist = std::min(dist, unsigned(travel.get(p)));
        if (dist == cambc::distance_field::unreachable) continue;
        const float value = float(f.group.gem_value()) + 0.12f * f.group.gold_value();
        // Reward / (travel + clearing + capture). Resets improve clear estimates.
        const float cost = dist + hp / std::max(1.0f, me.strength() * 1.12f) + cambc::constants::capture_time + 1;
        float score = cost / std::max(1.0f, value);
        if (static_cast<int>(i) == target_group) score *= 0.85f; // Avoid target thrashing.
        if (score < best_score) { best_score = score; selected = static_cast<int>(i); }
    }
    target_group = selected;
    if (selected < 0) {
        // Vacate collected regions even if every other group is cooling down.
        for (const auto& f : farms) if (f.spawns.is_set(me.position())) {
            move_to(around(me.position(), 1) & ~f.spawns);
            break;
        }
        return;
    }
    auto& f = farms[selected];
    auto act_on_group = [&](bool walked) {
        return fight<cambc::camp>(f.group.camps(), walked);
    };
    const bool acted = act_on_group(false);
    // can_move() alone need not encode a just-cast spell's walk exclusion.
    // Replan capture next turn after combat, including a last-monster kill.
    if (!me.is_alive() || acted) return;
    const auto fresh_visible = cambc::vision::visible_tiles();
    cambc::bitboard goals;
    const bool seen = !(f.spawns & fresh_visible).is_empty();
    if (seen && std::holds_alternative<cambc::map::camp_group_reward_available>(f.group.state()))
        goals = f.spawns; // Finish clearing by occupying the actual capture region.
    else {
        for (const auto& c : f.group.camps()) {
            if (c.is_visible()) {
                if (c.health() > 0) goals |= around(c.position(), me.attack_range());
            } else if (!fresh_visible.is_set(c.spawn_position())) goals.set(c.spawn_position());
        }
    }
    const auto before = me.position();
    move_to(goals);
    // A false move can reveal a hidden camp without spending the move allowance.
    act_on_group(me.position() != before);
}

void Bot::play_turn() {
    auto& me = cambc::self();
    // Dead units can shop, but cannot inspect position or perform live actions.
    if (!me.is_alive()) { buy_items(); target_group = -1; return; }
    if (me.is_recalling() || me.is_submitting_gems() || me.is_teleporting()) return;
    buy_items(); // can_buy validates spawn/dead/Tavi and active shop restrictions.
    if (me.buffs().has_stun()) return;
    const bool at_spawn = cambc::map::spawn_region(team::ally).is_set(me.position());
    if (at_spawn && me.health() < me.max_health() * HEALED_HEALTH) return;
    if (!me.can_move() && !me.can_attack() && !me.can_cast()) return;
    // Bank immediately when already adjacent, before combat distractions.
    if (bank(false)) return;
    if (!at_spawn && me.health() < me.max_health() * RETREAT_HEALTH) {
        const auto& spawn = cambc::map::spawn_region(team::ally);
        move_to(spawn);
        if (!spawn.is_set(me.position()) && (me.can_move() || me.can_attack() || me.can_cast())) me.recall();
        return;
    }
    if (me.gem_count() > 0) { bank(true); return; }
    // Gold needs to become damage; safe recalls preserve the full bag policy.
    if (!at_spawn && me.gold_count() >= SHOP_RECALL_GOLD && !threatened()) { me.recall(); return; }
    if (defend(false)) return;
    farm_camps();
}
