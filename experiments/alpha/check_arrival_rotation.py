"""Scope/observation invariants; temporal/geometric regressions compile in bot-check."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

task = json.loads(Path('.agent/task.json').read_text())
root = Path('bots/alpha/src')


def base(name):
    return subprocess.check_output(
        ['git', 'show', f"{task['edit_commit']}:{root}/{name}"], text=True)


def without_comments(text):
    return re.sub(r'//[^\n]*', '', text)


header = (root / 'camp_rotation.h').read_text()
original = base('camp_rotation.h')
observer_start, observer_end = '    void observe()', '    cambc::bitboard goals()'
observer = lambda text: text[text.index(observer_start):text.index(observer_end)]
checks = {
    'all_other_executable_policy_unchanged': all(
        without_comments(p.read_text()) == without_comments(base(p.name))
        for p in root.iterdir() if p.is_file() and p.name != 'camp_rotation.h'),
    'live_observation_policy_unchanged': observer(header) == observer(original),
    'no_extra_group_state_queries': header.count('.group.state()') == original.count('.group.state()') == 1,
    'visibility_precedes_live_state': observer(header).index('entry.spawns & visible')
        < observer(header).index('entry.group.state()'),
    'no_new_shared_memory': 'shared_memory' not in header,
    'geometry_uses_static_spawn_metadata': 'member.spawn_position()' in header
        and 'member.position()' not in header,
    'observation_budget_preserved': 'observation_fuel_reserve = 45000' in header
        and 'observation_limit = 16' in header,
    'existing_temporal_regression_retained': original[original.index('static_assert([]'):original.index('constexpr std::uint64_t')]
        .strip() in header,
    'arrival_and_geometry_regressions_in_trusted_build': header.count('static_assert([]') == 3,
    'official_yield_after_exception_handling': (root / 'main.cpp').read_text().index('cambc::end_turn();')
        > (root / 'main.cpp').read_text().index('catch (...)'),
}
report = {
    'task_id': task['task_id'],
    'scope': 'Source invariants only. bot-check compiles C++ timing/bounds static_asserts; no strength/fuel claim.',
    'checks': checks,
    'passed': all(checks.values()),
    'source_files': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                     for p in sorted(root.iterdir()) if p.is_file()},
}
path = Path(f"experiments/alpha/{task['task_id']}-source-check.json")
path.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
raise SystemExit(0 if report['passed'] else 1)
