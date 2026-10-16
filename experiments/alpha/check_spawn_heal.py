"""Bounded source regression; runtime verification belongs to bot-check."""
import json
from pathlib import Path
import subprocess

task = json.loads(Path('.agent/task.json').read_text())
source = Path('bots/alpha/src')
text = (source / 'bot.cpp').read_text()
guard = '''    // Recall arrives before actions; spawn healing happens at turn end.
    if (at_spawn && me.health() < me.max_health())
        return;

'''


def accepted(path):
    return subprocess.check_output([
        'git', 'show', f"{task['accepted_commit']}:{path.as_posix()}"
    ])


checks = {
    'exactly_one_healing_guard': text.count(guard) == 1,
    'guard_after_shop_before_combat_and_routes': (
        text.index('        buy_items();') < text.index(guard)
        < text.index('    // Recall immediately')
        < text.index('    // Attack the first enemy')
        < text.index('    // Bank any carried gems')
    ),
    'only_accepted_behavior_delta': (
        text.replace(guard, '').encode() == accepted(source / 'bot.cpp')
    ),
    'other_source_unchanged': all(
        path.read_bytes() == accepted(path)
        for path in source.iterdir() if path.name != 'bot.cpp' and path.is_file()
    ),
    'official_yield_retained': 'cambc::end_turn();' in (source / 'main.cpp').read_text(),
}
report = {
    'task_id': task['task_id'],
    'scope': 'source invariants only; no runtime or fuel claims',
    'checks': checks,
    'passed': all(checks.values()),
}
Path(f"experiments/alpha/{task['task_id']}-source-check.json").write_text(
    json.dumps(report, indent=2) + '\n'
)
print(json.dumps(report, indent=2))
assert report['passed']
