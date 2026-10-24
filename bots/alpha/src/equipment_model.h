#pragma once
#include <cambc.h>
#include "equipment_policy.h"
#include <type_traits>

namespace equipment_model {
// The same immutable kit model for draft and shop. Live stats are supplied only
// by the observing champion; draft supplies base stats, never a live unit query.
inline equipment_policy::model estimate(const cambc::champion& champion,
                                        float health, float strength, float focus) {
    const auto stats = champion.base_stats();
    equipment_policy::model result{health, strength, focus,
        {stats.strength_growth, stats.focus_growth, stats.health_growth}};
    const auto passive = champion.passive();
    if (passive == cambc::passive_type::health_strength)
        result.health_to_strength = cambc::constants::passive_abilities::ryth_health_strength_ratio;
    if (passive == cambc::passive_type::splash_attack)
        result.basic_rate = equipment_policy::area_targets;
    if (passive == cambc::passive_type::retaliation)
        result.focus_rate = cambc::constants::passive_abilities::ren_retaliation_focus_ratio; // one incoming basic/round, uncertain workload
    for (const auto& ability : champion.abilities()) {
        if (!ability.info()) continue;
        std::visit([&](const auto& info) {
            using T = std::decay_t<decltype(info)>;
            const float cooldown = static_cast<float>(std::max(1, info.max_cooldown));
            if constexpr (std::is_same_v<T, cambc::ability_attack_reset>)
                result.basic_rate += result.basic_rate / cooldown;
            if constexpr (std::is_same_v<T, cambc::ability_damage>
                          || std::is_same_v<T, cambc::ability_cc>) {
                if (ability.can_target_camps()) result.focus_rate += info.modifier / cooldown;
            }
            if constexpr (std::is_same_v<T, cambc::ability_aoe_damage>)
                result.focus_rate += equipment_policy::area_targets * info.modifier / cooldown;
            if constexpr (std::is_same_v<T, cambc::ability_shield>) {
                if (ability.can_target_self())
                    result.shield_scale = equipment_policy::shield_credit * info.modifier;
            }
            // Do not price unused dash damage or another champion's healing.
        }, *ability.info());
    }
    return result;
}
} // namespace equipment_model
