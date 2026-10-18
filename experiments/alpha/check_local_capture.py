"""Source safety contracts; engine compilation/smoke belongs to bot-check."""
import hashlib
import json
from pathlib import Path
import subprocess

task = json.loads(Path('.agent/task.json').read_text())
root = Path('bots/alpha/src')
source = (root / 'bot.cpp').read_text()
base = subprocess.check_output(['git', 'show', f"{task['edit_commit']}:{root}/bot.cpp"]).decode()
start = source.index('// Local collection is deliberately different')
end = source.index('// Attack a camp already in range', start)
helper = source[start:end]
farming = source[end:source.index('void Bot::play_turn()')]
restored = source[:start] + source[end:]
restored = restored.replace('''    cambc::bitboard delegated;
    delegated.clear();
    if (collect_local_reward(delegated)) return;
''', '')
restored = restored.replace('goals |= group.spawn_tiles() & ~delegated;', 'goals |= group.spawn_tiles();')
checks = {
    'only_local_farming_policy_changed': restored == base,
    'other_executable_files_match_edit_base': all(
        p.read_bytes() == subprocess.check_output(['git', 'show', f"{task['edit_commit']}:{p}"])
        for p in root.iterdir() if p.is_file() and p.name != 'bot.cpp'),
    'live_group_queries_require_current_local_vision': helper.index('spawns & vicinity & visible') < helper.index('group.state()'),
    'only_cleared_groups_collect': helper.index('camp_group_reward_available') < helper.index('spawns.is_set(position)) return true'),
    'ongoing_capture_precedes_other_camp_attacks': farming.index('collect_local_reward(delegated)') < farming.index('fight<cambc::camp>()'),
    'walk_distance_and_free_goals_checked': 'local_capture_steps = 3;' in helper
        and 'blocked.reachable_tiles(position, local_capture_steps) & ~blocked' in helper,
    'existing_collector_precedes_election': helper.index('spawns & allied_tiles') < helper.index('bool assigned_elsewhere'),
    'delegated_tiles_not_navigation_goals': 'goals |= group.spawn_tiles() & ~delegated;' in farming,
    'ally_live_state_requires_visibility': helper.index('!ally.is_visible() || !ally.is_alive()') < helper.index('ally.gem_count()'),
    'deterministic_tie_and_no_new_shared_state': 'champion_id(ally) < champion_id(me)' in helper and 'shared_memory' not in helper,
    'bounded_scan_and_fallback': 'local_capture_group_limit = 16;' in helper
        and 'allies_examined > 6' in helper and 'capture_scan_reserve = 45000;' in helper
        and 'return move_towards_closest(rewards);' in helper,
    'yield_survives_exceptions': (root / 'main.cpp').read_text().index('cambc::end_turn();')
        > (root / 'main.cpp').read_text().index('catch (...)'),
}
report = {'task_id': task['task_id'], 'scope': 'Source invariants only; no runtime, fuel or strength claim',
          'checks': checks, 'passed': all(checks.values()),
          'source_files': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in root.iterdir() if p.is_file()}}
out = Path(f"experiments/alpha/{task['task_id']}-source-check.json")
out.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
raise SystemExit(0 if report['passed'] else 1)
