"""Source contracts only; compilation and runtime validation require bot-check."""
import json
from pathlib import Path
import subprocess

task = json.loads(Path('.agent/task.json').read_text())
source = Path('bots/alpha/src')
text = (source / 'bot.cpp').read_text()
header = (source / 'bot.h').read_text()
channel_guard = text.index('if (!me.is_alive() || me.is_recalling()')
consume = text.index('const bool retrying_recall = recall_pending && !at_spawn;')
branch = text[text.index('    // Preserve the first attempt;'):text.index('    // Attack the first enemy')]
checks = {
    'running_channels_preserved_before_retry_state_consumed': channel_guard < consume,
    'state_consumed_on_next_actionable_turn': 'recall_pending = false;' in text[consume:text.index('    // Preserve the first attempt;')],
    'first_attempt_never_moves': 'if (retrying_recall)\n            move_towards_closest(spawn);' in branch,
    'at_most_one_retreat': branch.count('move_towards_closest(') == 1,
    'arrival_rechecked_before_recall': branch.index('move_towards_closest(spawn)') < branch.index('if (!spawn.is_set(me.position()))') < branch.index('me.recall();'),
    'only_observed_active_recall_arms_retry': branch.index('me.recall();') < branch.index('recall_pending = me.is_recalling();'),
    'private_state_initially_empty': 'bool recall_pending = false;' in header,
    'official_yield_retained': 'cambc::end_turn();' in (source / 'main.cpp').read_text(),
}
for name in ['main.cpp', 'draft.cpp', 'draft.h', 'random.h']:
    accepted = subprocess.check_output(['git', 'show', f"{task['accepted_commit']}:bots/alpha/src/{name}"])
    checks[f'{name}_unchanged'] = (source / name).read_bytes() == accepted
report = {'task_id': task['task_id'], 'scope': 'source contracts, not runtime branch coverage',
          'checks': checks, 'passed': all(checks.values())}
Path(f"experiments/alpha/{task['task_id']}-source-check.json").write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
assert report['passed']
