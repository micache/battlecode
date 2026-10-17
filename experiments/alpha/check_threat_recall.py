"""Source safety contracts only; trusted bot-check owns compilation/runtime checks."""
import json
from pathlib import Path
import subprocess

task = json.loads(Path('.agent/task.json').read_text())
root = Path('bots/alpha/src')
text = (root / 'bot.cpp').read_text()
helper_start = text.index('// Range is a conservative threat test')
helper_end = text.index('void Bot::play_turn()', helper_start)
helper = text[helper_start:helper_end]
branch_start = text.index('    // Make progress home before a recall')
branch_end = text.index('    // Attack the first enemy', branch_start)
branch = text[branch_start:branch_end]
accepted = subprocess.check_output([
    'git', 'show', f"{task['accepted_commit']}:bots/alpha/src/bot.cpp"
]).decode()
old_start = accepted.index('    // Recall immediately when badly hurt')
old_end = accepted.index('    // Attack the first enemy', old_start)
restored = text[:branch_start] + accepted[old_start:old_end] + text[branch_end:]
restored = restored.replace(helper, '', 1)
checks = {
    'only_threat_helper_and_recall_branch_changed': restored == accepted,
    'visibility_short_circuits_all_live_threat_queries':
        'unit.is_visible() && unit.health() > 0 && unit.strength() > 0\n'
        '            && unit.attack_tiles().is_set(position)' in helper,
    'both_enemy_champions_and_camps_checked': all(s in helper for s in [
        'champions(team::enemy)', 'cambc::vision::camps()']),
    'channels_guarded_before_new_queries':
        text.index('if (!me.is_alive() || me.is_recalling()') < branch_start,
    'low_health_and_away_from_spawn_gate_unchanged':
        'if (!at_spawn && me.health() < me.max_health() * 0.35f)' in branch,
    'single_threat_gated_retreat': branch.count('move_towards_closest(') == 1
        and 'if (under_basic_attack_threat(me.position()))\n'
        '            move_towards_closest(spawn);' in branch,
    'fresh_position_guards_recall_after_movement':
        branch.index('move_towards_closest(spawn);')
        < branch.index('if (!spawn.is_set(me.position()))') < branch.index('me.recall();'),
    'failed_move_does_not_suppress_recall':
        'if (move_towards_closest' not in branch and branch.count('me.recall();') == 1,
    'official_yield_preserved': 'cambc::end_turn();' in (root / 'main.cpp').read_text(),
}
for name in ['bot.h', 'main.cpp', 'draft.cpp', 'draft.h', 'random.h']:
    baseline = subprocess.check_output([
        'git', 'show', f"{task['accepted_commit']}:bots/alpha/src/{name}"
    ])
    checks[f'{name}_unchanged'] = (root / name).read_bytes() == baseline
report = {'task_id': task['task_id'], 'scope': 'source contracts, not runtime coverage',
          'checks': checks, 'passed': all(checks.values())}
path = Path(f"experiments/alpha/{task['task_id']}-source-check.json")
path.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
assert report['passed']
