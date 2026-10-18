"""Check patch isolation and observation/action safety; not an engine fixture."""
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

start = source.index('    if (goals.is_set(cambc::self().position())) {', source.index('void farm_camps()'))
end = source.index('    // Fresh vision after movement', start)
recovery = source[start:end]
hstart = header.index('    // Being on a spawn only means')
hend = header.index('\n};', hstart)
helper = header[hstart:hend]
checks = {
    'all_other_turn_policy_matches_edit_base': source[:start] + source[end:] == base('bot.cpp'),
    'cooldown_memory_unchanged': header[:hstart].rstrip() + header[hend:] == base('camp_rotation.h').rstrip() + '\n',
    'other_source_files_match_edit_base': all(
        p.read_text() == base(p.name) for p in root.iterdir()
        if p.is_file() and p.name not in ('bot.cpp', 'camp_rotation.h')),
    'occupied_visible_group_checked_before_live_state': helper.index('entry.spawns.is_set(position)')
        < helper.index('entry.spawns & visible') < helper.index('entry.group.state()'),
    'only_alive_group_can_supply_movement_goals': helper.index('camp_group_alive')
        < helper.index('entry.group.camps()') < helper.index('result.draw_chebyshev'),
    'member_live_reads_follow_visibility': helper.index('!member.is_visible()')
        < helper.index('member.health()') < helper.index('member.position()'),
    'free_goals_and_fresh_post_move_combat': recovery.index('approaches &= ~blocked_tiles()')
        < recovery.index('move_towards_closest(approaches)') < recovery.index('fight<cambc::camp>(true)'),
    'no_new_persistent_or_team_state': 'shared_memory' not in helper and '    static ' not in helper
        and 'occupied_group_approaches() const' in helper,
    'bounded_work_and_action_guards': '++examined > observation_limit' in helper
        and helper.count('fuel_remaining() < observation_fuel_reserve') >= 3
        and '!me.can_move()' in helper and '!me.can_attack()' in helper
        and 'buff_restrictions::move' in helper and 'buff_restrictions::attack' in helper,
}
report = {
    'task_id': task['task_id'],
    'scope': 'Source isolation and safety checks only. No runtime branch coverage, fuel or strength claim.',
    'checks': checks, 'passed': all(checks.values()),
    'source_files': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                     for p in sorted(root.iterdir()) if p.is_file()},
}
out = Path(f"experiments/alpha/{task['task_id']}-source-check.json")
out.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
raise SystemExit(0 if report['passed'] else 1)
