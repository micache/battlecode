"""Source safety invariants and finite geometry cases, not SDK/match simulation."""
import hashlib
import itertools
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
s = (ROOT / 'bots/gamma/src/bot.cpp').read_text()
d = (ROOT / 'bots/gamma/src/draft.cpp').read_text()
m = (ROOT / 'bots/gamma/src/main.cpp').read_text()
checks = {
    'hidden_group_queries_gated': 'if (seen) {\n            const auto state = f.group.state();' in s,
    'no_hidden_live_state_assumptions': 'else if (!visible.is_set(c.spawn_position()))' in s,
    'free_goals_only': 'goals &= ~blocked;' in s and '| cambc::vision::camp_tiles()' not in s.split('goals &=')[1].split(';')[0],
    'hidden_bump_refresh_even_without_movement': 'move_to(goals);\n    // A false move' in s and 'act_on_group(me.position() != before);' in s,
    'reset_followup_fresh_visibility_and_allowance': 'if (cast && live(target) && me.can_attack()' in s,
    'walk_exclusive_spells_guarded': 'if (walked && exclusive) continue;' in s,
    'self_resets_do_not_query_rangeless_mask': 'if (a.is_attack_reset())' in s.split('const auto valid = a.valid_tiles()')[0],
    'channels_preserved': 'if (me.is_recalling() || me.is_submitting_gems() || me.is_teleporting()) return;' in s,
    'spawn_healing_before_departure': 'if (at_spawn && me.health() < me.max_health() * HEALED_HEALTH) return;' in s,
    'capture_and_vacate_states_separate': 'goals = f.spawns;' in s and 'move_to(around(me.position(), 1) & ~f.spawns);' in s,
    'no_live_shared_memory_protocol': 'shared_memory' not in s and 'camp_claims' not in (ROOT / 'bots/gamma/src/bot.h').read_text(),
    'combat_refreshes_after_basic_kill': 'continue; // A kill must not strand the separate cast allowance.' in s,
    'combat_bounded_targets_steps_fuel': all(x in s for x in ('COMBAT_STEPS = 4', 'COMBAT_TARGETS = 12', 'COMBAT_FUEL = 18000', 'step < COMBAT_STEPS', '++examined > COMBAT_TARGETS')),
    'combat_visibility_before_health': s.index('if (!t.is_visible()) continue;') < s.index('const float hp = t.health();'),
    'combat_group_confinement': 'fight<cambc::camp>(f.group.camps(), walked)' in s,
    'combat_does_not_chase_champions': 'if (d > range || (d > 1 && hp > 2 * strength)) continue;' in s,
    'combat_compares_reset_and_useful_area': all(x in s for x in ('basic_score > best', 'combat_value::area(view, i, radius, damage, kill_bonus)', 'if (score > best)')),
    'compiled_exact_kernel_regressions': 'static_assert(hit(100, 20, 10) == 30)' in (ROOT / 'bots/gamma/src/combat_value.h').read_text(),
    'normal_fuel_and_yield': 'PLAN_FUEL = 30000' in s and 'retry < 2' in s and 'cambc::end_turn();' in m,
    'sdk_profile_validation': 'constants::winning_gems != 1000' in m and 'constants::max_rounds != 2000' in m,
    'combat_never_walks_after_exclusive_kill': s.index('if (!me.is_alive() || acted) return;') < s.index('const auto fresh_visible'),
    'stun_never_starts_channel': s.index('if (me.buffs().has_stun()) return;') < s.index('if (bank(false))'),
    'action_restrictions_respected': all('cambc::buff_restrictions::' + action in s for action in ['move', 'attack', 'cast']),
}
# Exhaust all draft histories up to the fifth pick, including non-policy choices.
names = ['ryth', 'vesper_vale', 'vendetta', 'cassi_and_issac', 'stellar', 'prism', 'marcella', 'willow', 'ren', 'varg', 'tavi']
order = [names.index(name) for name in re.findall(r'D::(\w+)', d)]
checks['composition_implements_reset_and_splash_farmers'] = order[:5] == [9, 2, 6, 0, 10]
checks['released_roster_complete_and_unique'] = sorted(order) == list(range(11))
checks['legal_draft_any_history_3_to_5_picks'] = all(
    next(p for p in order if p not in history) not in history
    for n in range(5) for history in itertools.combinations(range(11), n))
checks['draft_implementation_uses_nonduplicate_order'] = 'std::find(chosen.begin(), chosen.end(), pick) == chosen.end()' in d

# Stable geometry regression: a killed tile in a live line must not remain a
# destination. After full clearing, capture requires actual spawn occupancy.
def around(p, r):
    return {(p[0]+x,p[1]+y) for x in range(-r,r+1) for y in range(-r,r+1)}
spawns = {(10,10),(11,10),(12,10)}
current = (10,10)
alive = {(12,10)}
goals = set().union(*(around(p,1) for p in alive)) - alive
checks['cleared_member_is_not_a_live_approach_goal'] = current not in goals
checks['live_survivor_has_free_reachable_approach'] = (11,10) in goals
checks['capture_region_preserves_occupied_tile'] = current in spawns
checks['respawn_exit_vacates_entire_group'] = bool(around(current,1)-spawns) and not ((around(current,1)-spawns)&spawns)
checks['unseen_spawn_is_exploration_goal_not_hidden_occupant'] = current not in {(12,10)}
report = {'kind': 'source invariants and finite geometry only; no runtime/strength claim',
          'checks': checks, 'passed': all(checks.values()),
          'source_file_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in sorted((ROOT/'bots/gamma/src').glob('*'))}}
p = ROOT/'experiments/gamma/harvest-source-check.json'
p.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
raise SystemExit(0 if report['passed'] else 1)
