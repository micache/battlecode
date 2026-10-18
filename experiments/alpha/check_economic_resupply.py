"""Source safety contracts; actual C++ compilation/runtime use bot-check."""
import json
from pathlib import Path
import subprocess

root = Path('bots/alpha/src')
task = json.loads(Path('.agent/task.json').read_text())
text = (root / 'bot.cpp').read_text()
base = subprocess.check_output([
    'git', 'show', f"{task['edit_commit']}:bots/alpha/src/bot.cpp"
]).decode()
policy = text.split('bool economic_recall(', 1)[1].split('// Handles are refreshed', 1)[0]
turn = text.split('void Bot::play_turn()', 1)[1]
checks = {
    'channel_guard_before_live_shopping': turn.index('me.is_recalling()') < turn.index('buy_items(); //'),
    'resupply_after_retreat_combat_and_banking_before_farming': (
        turn.index('me.health() <') < turn.index('fight<cambc::champion>()')
        < turn.index('if (me.gem_count() > 0)')
        < turn.index('economic_recall(next_resupply_round)') < turn.index('farm_camps();')
    ),
    'empty_bag_spawn_action_and_fuel_guards': all(s in policy for s in [
        'me.gem_count()', '!me.can_move()',
        'spawn_region(team::ally).is_set(me.position())',
        'cambc::fuel_remaining() < combat_fuel_reserve',
    ]),
    'visible_camp_before_live_health_and_range': (
        policy.index('camp.is_visible()') < policy.index('camp.health()')
        < policy.index('camp.strength()') < policy.index('camp.attack_tiles()')
    ),
    'capture_state_only_after_occupancy_guard': (
        policy.index('group.spawn_tiles().is_set(me.position())') < policy.index('group.state()')
        < policy.index('me.recall();')
    ),
    'retry_deadline_committed_before_recall': (
        'cambc::round_number() < next_attempt' in policy
        and policy.index('next_attempt = cambc::round_number() + resupply_retry_rounds;')
        < policy.index('me.recall();')
    ),
    'purchase_count_and_legality_unchanged': (
        text.split('void Bot::buy_items()', 1)[1].split('// Bound extra combat', 1)[0]
        == base.split('void Bot::buy_items()', 1)[1].split('// Bound extra combat', 1)[0]
    ),
    'combat_and_farming_unchanged': (
        text.split('// Handles are refreshed', 1)[1].split('void Bot::play_turn()', 1)[0]
        == base.split('// Handles are refreshed', 1)[1].split('void Bot::play_turn()', 1)[0]
    ),
    'other_executable_sources_unchanged': all(
        p.read_bytes() == subprocess.check_output([
            'git', 'show', f"{task['edit_commit']}:{p.as_posix()}"
        ]) for p in root.iterdir() if p.is_file() and p.name not in ['bot.cpp', 'bot.h']
    ),
    'yield_retained': 'cambc::end_turn();' in (root / 'main.cpp').read_text(),
}
report = {'task_id': task['task_id'], 'scope': 'source contracts, not engine fixtures or fuel measurements',
          'checks': checks, 'passed': all(checks.values())}
path = Path('experiments/alpha') / (task['task_id'] + '-source-check.json')
path.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
assert report['passed']
