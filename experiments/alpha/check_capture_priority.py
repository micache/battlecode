"""Capture policy safety/order invariants; runtime verification uses bot-check."""
import json
from pathlib import Path
import subprocess

task = json.loads(Path('.agent/task.json').read_text())
src = Path('bots/alpha/src')
text = (src / 'bot.cpp').read_text()


def accepted(path):
    return subprocess.check_output([
        'git', 'show', f"{task['accepted_commit']}:{path.as_posix()}"
    ]).decode()


before = accepted(src / 'bot.cpp')
start = text.index('// Collect visible cleared groups')
end = text.index('    // Fresh vision after movement', start)
old_start = before.index('// Attack a camp already in range')
old_end = before.index('    // Fresh vision after movement', old_start)
policy = text[start:end]
guard = '''    if (!rewards.is_empty()
        && (rewards.is_set(cambc::self().position()) || move_towards_closest(rewards)))
        return;
'''
checks = {
    'only_farming_selection_changed': (
        text[:start] == before[:old_start] and text[end:] == before[old_end:]
    ),
    'live_group_state_guarded_by_visibility': '''        if (!(spawns & visible).is_empty()) {
            const auto state = group.state();''' in policy,
    'reward_mask_only_from_cleared_visible_groups': '''            if (std::holds_alternative<cambc::map::camp_group_reward_available>(state))
                rewards |= spawns;
        }''' in policy,
    'respawning_groups_excluded': '''            if (std::holds_alternative<cambc::map::camp_group_respawning>(state))
                continue;''' in policy,
    'hold_or_move_before_attacks_with_failure_fallback': (
        guard in policy
        and policy.index(guard) < policy.index('for (const auto& camp : cambc::vision::camps())')
        and 'if (attack_if_in_range(camp))' in policy
    ),
    'other_source_unchanged': all(
        p.read_text() == accepted(p)
        for p in src.iterdir() if p.is_file() and p.name != 'bot.cpp'
    ),
    'official_yield_retained': 'cambc::end_turn();' in (src / 'main.cpp').read_text(),
}
report = {'task_id': task['task_id'], 'scope': 'source invariants only; no runtime or fuel claims',
          'checks': checks, 'passed': all(checks.values())}
Path(f"experiments/alpha/{task['task_id']}-source-check.json").write_text(
    json.dumps(report, indent=2) + '\n'
)
print(json.dumps(report, indent=2))
assert report['passed']
