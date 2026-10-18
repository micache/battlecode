"""Safety/scope integration checks; C++ trace scenarios compile via bot-check."""
import hashlib
import json
from pathlib import Path
import subprocess

task = json.loads(Path('.agent/task.json').read_text())
root = Path('bots/alpha/src')
source = (root / 'bot.cpp').read_text()
header = (root / 'camp_rotation.h').read_text()

def base(name):
    return subprocess.check_output(
        ['git', 'show', f"{task['edit_commit']}:{root}/{name}"], text=True)

old = base('bot.cpp')
combat = source[source.index('template<class Target>\nbool fight'):source.index('// Attack a camp already in range')]
old_combat = old[old.index('template<class Target>\nbool fight'):old.index('// Attack a camp already in range')]
restored = combat.replace('bool fight(bool walked = false, camp_rotation::clear_trace* trace = nullptr)',
                          'bool fight(bool walked = false)')
restored = restored.replace('''        if constexpr (std::is_same_v<Target, cambc::camp>)
            if (trace) trace->note_target(target->spawn_position());
''', '')
restored = restored.replace('''            trace_cast(trace, *selected);
            if constexpr (std::is_same_v<Target, cambc::camp>)
                if (trace) trace->note_target(selected_target->spawn_position());
''', '')
restored = restored.replace('''            if (const auto next = basic_target<Target>()) {
                me.attack(*next);
                if constexpr (std::is_same_v<Target, cambc::camp>)
                    if (trace) trace->note_target(next->spawn_position());
            }''', '            if (const auto next = basic_target<Target>()) me.attack(*next);')
restored = restored.replace('if (ability.use()) { trace_cast(trace, ability); break; }',
                            'if (ability.use()) break;')
restored = restored.replace('if (ability.use(ally)) { trace_cast(trace, ability); break; }',
                            'if (ability.use(ally)) break;')
capture = header[header.index('    cambc::bitboard capture_goals'):header.index('    void observe()')]
farm = source[source.index('void farm_camps()'):source.index('void Bot::play_turn()')]
checks = {
    'combat_actions_scoring_and_order_unchanged_except_trace': restored == old_combat,
    'navigation_shopping_and_readiness_unchanged': source[:source.index('void trace_cast')]
        == old[:old.index('// Spend the separate basic and cast allowances.')],
    'whole_turn_policy_unchanged': source[source.index('void Bot::play_turn()'):]
        == old[old.index('void Bot::play_turn()'):],
    'ordinary_route_and_postwalk_combat_unchanged': farm[farm.index('    // Include unknown/expired groups'):]
        == old[old.index('    // Include unknown/expired groups'):old.index('void Bot::play_turn()')],
    'cooldown_observer_and_eligibility_unchanged': header[header.index('    void observe()'):]
        == base('camp_rotation.h')[base('camp_rotation.h').index('    void observe()'):],
    'other_executable_files_match_edit_base': all(p.read_text() == base(p.name)
        for p in root.iterdir() if p.is_file() and p.name not in ('bot.cpp', 'camp_rotation.h')),
    'successful_spell_trace_includes_damage_and_defensive_paths':
        'if (cast) {\n            trace_cast(trace, *selected);' in combat
        and 'if (ability.use()) { trace_cast(trace, ability); break; }' in combat
        and 'if (ability.use(ally)) { trace_cast(trace, ability); break; }' in combat,
    'alive_move_and_spell_exclusion_guard': 'trace.permits_followthrough(me.is_alive(), me.can_move())' in farm
        and 'count > 0 && !movement_blocked && alive && can_move' in header,
    'only_touched_visible_local_reward_groups': capture.index('if (!touched) continue;')
        < capture.index('entry.spawns & visible & vicinity')
        < capture.index('if (candidates.is_empty()) continue;')
        < capture.index('entry.group.state()')
        and 'camp_group_reward_available' in capture,
    'postcombat_fresh_blockers_and_single_legal_move': farm.index('fight<cambc::camp>(false, &trace)')
        < farm.index('const auto blocked = blocked_tiles();')
        < farm.index('goals &= blocked.reachable_tiles')
        < farm.index('me.move_absolute(goals.positions()[0])')
        and 'me.base_stats().base_move_speed) & ~blocked' in farm
        and farm.count('me.move_absolute(') == 1,
    'already_on_capture_region_does_not_move': '!goals.is_set(me.position())' in farm,
    'extra_work_and_action_have_fuel_guards': 'fuel_remaining() < observation_fuel_reserve' in capture
        and 'fuel_remaining() >= camp_rotation::observation_fuel_reserve' in farm
        and 'fuel_remaining() >= combat_fuel_reserve' in farm,
    'bounded_trace_and_no_new_shared_protocol': 'std::array<cambc::vec2, 3>' in header
        and 'if (count < targets.size())' in header and 'shared_memory' not in header,
    'official_yield_survives_exceptions': (root / 'main.cpp').read_text().index('cambc::end_turn();')
        > (root / 'main.cpp').read_text().index('catch (...)'),
}
report = {
    'task_id': task['task_id'],
    'scope': 'Source integration invariants. Pure C++ trace scenarios require bot-check; no engine coverage/fuel/strength claim.',
    'checks': checks, 'passed': all(checks.values()),
    'source_files': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(root.iterdir()) if p.is_file()},
}
path = Path(f"experiments/alpha/{task['task_id']}-source-check.json")
path.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
raise SystemExit(0 if report['passed'] else 1)
