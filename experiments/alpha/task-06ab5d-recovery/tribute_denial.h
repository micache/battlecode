#pragma once
#include <cambc.h>
#include <array>
#include <cstdint>
#include <iostream>
#include <optional>
#include <variant>

namespace tribute_denial {

// Only a live tribute has immediate objective value. Ordinary damage cannot
// cancel it; stun immunity makes even a damaging stun unsuitable for denial.
constexpr std::uint32_t bank_value(bool submitting, bool immune, std::uint32_t bag) {
    return submitting && !immune ? bag : 0;
}

static_assert(bank_value(true, false, 30) == 30);
static_assert(bank_value(true, false, 1) == 1);
static_assert(bank_value(true, false, 0) == 0);
static_assert(bank_value(false, false, 30) == 0);
static_assert(bank_value(true, true, 30) == 0);
static_assert(bank_value(false, true, 30) == 0);
static_assert(bank_value(true, false, 1000) > bank_value(true, false, 30));

enum class tool { none, unit_stun, ground_stun, enhanced_basic };

inline tool kind(const cambc::ability& ability) {
    if (ability.is_cc() && ability.can_target_enemies()
        && ability.get<cambc::ability_cc>().duration > 0)
        return tool::unit_stun;
    if (ability.is_aoe_damage() && ability.can_target_ground()
        && ability.get<cambc::ability_aoe_damage>().duration > 0)
        return tool::ground_stun;
    if (ability.is_attack_reset()
        && ability.get<cambc::ability_attack_reset>().enhanced_attack)
        return tool::enhanced_basic;
    return tool::none; // Pure damage, slow-free AoE and ordinary resets do not deny.
}

// Planning reserves; normal-budget headroom is checked by the trusted smokes.
constexpr std::uint64_t entry_fuel_reserve = 45000;
constexpr std::uint64_t scan_fuel_reserve = 28000;
constexpr unsigned enemy_limit = 6; // Five picks may include Cassi and Issac.

// No walking/chasing here. The caller ends combat after a successful action.
inline bool attempt(bool walked) {
    using cambc::team;
    auto& me = cambc::self();
    if (cambc::fuel_remaining() < entry_fuel_reserve || !me.is_alive()
        || !me.can_cast() || me.is_recalling() || me.is_submitting_gems()
        || me.is_teleporting() || me.restrictions().contains(cambc::buff_restrictions::cast))
        return false;

    const auto abilities = me.abilities();
    std::array<tool, 2> tools{};
    std::array<std::optional<cambc::bitboard>, 2> ranges;
    bool available = false;
    for (unsigned slot = 0; slot < tools.size(); ++slot) {
        const auto& ability = abilities[slot];
        if (!ability.info()) continue;
        const auto type = kind(ability);
        if (type == tool::none || !ability.is_ready()) continue;
        if (walked && std::visit([](const auto& info) {
            return info.exclusive_with_movement;
        }, *ability.info())) continue;
        if (type == tool::enhanced_basic
            && me.restrictions().contains(cambc::buff_restrictions::attack)) continue;
        tools[slot] = type;
        ranges[slot] = type == tool::enhanced_basic ? me.attack_tiles() : ability.valid_tiles();
        available = true;
    }
    if (!available) return false; // Most kits incur no enemy scan.

    std::optional<cambc::champion> target;
    unsigned selected_slot = 0;
    std::uint32_t best_bag = 0;
    unsigned examined = 0;
    for (const auto& enemy : cambc::vision::champions(team::enemy)) {
        if (++examined > enemy_limit || cambc::fuel_remaining() < scan_fuel_reserve) break;
        // Visibility precedes every hidden-state read. No cached enemy records.
        if (!enemy.is_visible() || enemy.health() <= 0 || !enemy.is_submitting_gems()) continue;
        const auto bag = bank_value(true, enemy.passive() == cambc::passive_type::stun_immunity,
            enemy.gem_count());
        if (bag <= best_bag) continue;
        for (unsigned slot = 0; slot < tools.size(); ++slot) {
            if (ranges[slot] && ranges[slot]->is_set(enemy.position())) {
                target = enemy;
                selected_slot = slot;
                best_bag = bag;
                break;
            }
        }
    }
    if (!target || cambc::fuel_remaining() < scan_fuel_reserve) return false;

    const auto& ability = abilities[selected_slot];
    const auto type = tools[selected_slot];
    if (!target->is_visible() || target->health() <= 0 || !target->is_submitting_gems()
        || !ability.is_ready()) return false;
    const auto range = type == tool::enhanced_basic ? me.attack_tiles() : ability.valid_tiles();
    if (!range.is_set(target->position())) return false;
    bool used = false;
    if (type == tool::enhanced_basic) {
        // Cast BEFORE the basic: an ordinary first hit does not interrupt tribute.
        if (me.restrictions().contains(cambc::buff_restrictions::attack)) return false;
        used = ability.use();
        if (used && me.is_alive() && me.can_attack() && target->is_visible()
            && target->health() > 0 && me.attack_tiles().is_set(target->position())
            && !me.restrictions().contains(cambc::buff_restrictions::attack))
            me.attack(*target);
    } else if (type == tool::ground_stun) {
        used = ability.use(target->position());
    } else {
        used = ability.use(*target);
    }
    // This records a used denial tool, not proof that the enemy lost the game.
    if (used) std::cout << "tribute denial: bag=" << best_bag
        << " tool=" << static_cast<int>(type) << '\n';
    return used;
}

} // namespace tribute_denial
