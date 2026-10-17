"""Source invariant and finite goal-mask fixtures; not an SDK/engine simulation."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
BASE = '1a0675ca881d4b67cb5c6cb1822ce2ae1602dc4d'
SOURCE = 'bots/gamma/src/bot.cpp'
old_block = '''    // Union every group's spawn tiles except visibly respawning groups.
    cambc::bitboard goals;
    goals.clear();
    const auto visible = cambc::vision::visible_tiles();
    for (const auto& group : cambc::map::camp_groups()) {
        const bool group_visible = !(group.spawn_tiles() & visible).is_empty();
        if (group_visible && std::holds_alternative<cambc::map::camp_group_respawning>(group.state()))
            continue;
        goals |= group.spawn_tiles();
    }
'''
new_block = '''    // Keep capture/exploration goals, but do not stop at a killed member of a live group.
    cambc::bitboard goals;
    goals.clear();
    const auto visible = cambc::vision::visible_tiles();
    const auto living_camps = cambc::vision::camp_tiles();
    for (const auto& group : cambc::map::camp_groups()) {
        auto spawns = group.spawn_tiles();
        if (!(spawns & visible).is_empty()) {
            const auto state = group.state();
            if (std::holds_alternative<cambc::map::camp_group_respawning>(state))
                continue;
            if (std::holds_alternative<cambc::map::camp_group_alive>(state))
                spawns &= living_camps | ~visible;
        }
        goals |= spawns;
    }
'''
accepted = subprocess.check_output(['git', 'show', f'{BASE}:{SOURCE}'], cwd=ROOT, text=True)
current = (ROOT / SOURCE).read_text()
checks = {
    'accepted_has_unfiltered_spawn_goals': accepted.count(old_block) == 1,
    'only_live_group_goal_selection_changed': current == accepted.replace(old_block, new_block),
    'standing_on_goal_still_preserves_capture': 'if (!me.can_move() || goals.is_set(me.position()))' in current,
    'fresh_post_move_camp_scan_preserved': '''if (move_towards_closest(goals))
        for (const auto& camp : cambc::vision::camps())''' in current,
}
for name in ['bot.h', 'main.cpp', 'draft.h', 'draft.cpp', 'random.h']:
    path = f'bots/gamma/src/{name}'
    checks[f'unchanged_{name}'] = (ROOT / path).read_bytes() == subprocess.check_output(
        ['git', 'show', f'{BASE}:{path}'], cwd=ROOT)

# Finite-set interpretation of the exact checked bitboard expression above.
# Query recorder ensures fully hidden groups do not consume a live state.
def goals(spawns, visible, living, read_state):
    if spawns & visible:
        state = read_state()
        if state == 'respawning':
            return set()
        if state == 'alive':
            return (spawns & living) | (spawns - visible)
    return spawns

spawns = {(10, 10), (11, 10), (12, 10)}
current_tile, survivor = (10, 10), (12, 10)
filtered = goals(spawns, spawns, {survivor}, lambda: 'alive')
checks['old_three_member_line_stalls_outside_melee_range'] = (
    current_tile in spawns and max(abs(a-b) for a,b in zip(current_tile, survivor)) > 1)
checks['new_line_has_reachable_progress_toward_survivor'] = (
    current_tile not in filtered and filtered == {survivor}
    and (11, 10) not in {survivor})
checks['reward_group_keeps_current_capture_tile'] = (
    goals(spawns, spawns, set(), lambda: 'reward') == spawns)
checks['respawning_group_has_no_goals'] = (
    goals(spawns, spawns, set(), lambda: 'respawning') == set())
checks['partial_vision_retains_unseen_members_only'] = (
    goals(spawns, {current_tile}, set(), lambda: 'alive') == spawns - {current_tile})
def forbidden_state_query():
    raise AssertionError('hidden group state read')
checks['fully_hidden_group_preserves_exploration_without_state_read'] = (
    goals(spawns, set(), set(), forbidden_state_query) == spawns)
checks['unrelated_live_camp_not_added_as_goal'] = (
    goals(spawns, spawns, {survivor, (20, 20)}, lambda: 'alive') == {survivor})
diff = subprocess.run(['git', 'diff', '--check'], cwd=ROOT, capture_output=True, text=True)
checks['diff_check'] = diff.returncode == 0
report = {
    'kind': 'source invariant and finite-set fixtures only; no runtime or strategic result',
    'base_commit': BASE,
    'bot_cpp_sha256': hashlib.sha256(current.encode()).hexdigest(),
    'checks': checks,
    'diff_check_exit_code': diff.returncode,
    'passed': all(checks.values()),
}
path = ROOT / 'experiments/gamma/camp-goals-source-check.json'
path.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
raise SystemExit(0 if report['passed'] else 1)
