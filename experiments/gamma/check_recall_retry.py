"""Source invariants only; official compilation/runtime are checked by bot-check."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
BASE = '1a0675ca881d4b67cb5c6cb1822ce2ae1602dc4d'
PATH = 'bots/gamma/src/bot.cpp'
current = (ROOT / PATH).read_text()
accepted = subprocess.check_output(['git', 'show', f'{BASE}:{PATH}'], cwd=ROOT, text=True)


def code(text):
    return re.sub(r'//[^\n]*|/\*.*?\*/', '', text, flags=re.S)


def compact(text):
    return re.sub(r'\s+', '', code(text))


start = current.index('    // Keep the first recall stationary;')
end = current.index('    // Attack the first enemy champion', start)
recovery = code(current[start:end])
checks = {
    'first_attempt_cannot_walk_and_retry_attempts_at_most_one_move': bool(re.search(
        r'if \(recall_attempted\)\s+move_towards_closest\(spawn\);', recovery))
        and recovery.count('move_towards_closest(') == 1,
    'movement_failure_still_allows_recall_and_position_is_refreshed': bool(re.search(
        r'move_towards_closest\(spawn\);\s*if \(!spawn.is_set\(me.position\(\)\)\) \{'
        r'\s*me.recall\(\);\s*recall_attempted = true;', recovery)),
    'flag_set_only_after_successful_recall': current.count('recall_attempted = true;') == 1
        and 'me.recall();\n            recall_attempted = true;' in recovery,
    'arrival_and_episode_exit_clear_flag': bool(re.search(
        r'} else \{\s*recall_attempted = false;\s*}\s*return;\s*}'
        r'\s*recall_attempted = false;', recovery)),
    'death_clears_flag_before_preserved_channel_guard': bool(re.search(
        r'if \(!me.is_alive\(\)\) \{\s*recall_attempted = false;\s*return;\s*}'
        r'\s*if \(me.is_recalling\(\) \|\| me.is_submitting_gems\(\) \|\| me.is_teleporting\(\)',
        code(current))),
    'channels_and_inaction_return_before_recovery': current.index(
        '|| (!me.can_move() && !me.can_attack()))\n        return;') < start,
}
# Normalize only the intended edits back to accepted source; catch unrelated changes.
old_start = accepted.index('    // Recall immediately when badly hurt away from spawn.')
old_end = accepted.index('    // Attack the first enemy champion', old_start)
normalized = current[:start] + accepted[old_start:old_end] + current[end:]
normalized = re.sub(
    r'    if \(!me.is_alive\(\)\) \{\s*recall_attempted = false;\s*return;\s*}\s*',
    '', normalized)
normalized = normalized.replace('if (me.is_recalling() ||', 'if (!me.is_alive() || me.is_recalling() ||', 1)
checks['only_recovery_behavior_changed'] = compact(normalized) == compact(accepted)
header_path = 'bots/gamma/src/bot.h'
header = (ROOT / header_path).read_text()
base_header = subprocess.check_output(['git', 'show', f'{BASE}:{header_path}'], cwd=ROOT, text=True)
checks['one_private_initialized_body_flag_only'] = compact(header).replace(
    'boolrecall_attempted=false;', '') == compact(base_header)
for name in ['main.cpp', 'draft.cpp', 'draft.h', 'random.h']:
    path = f'bots/gamma/src/{name}'
    checks[f'unchanged_{name}'] = (ROOT / path).read_bytes() == subprocess.check_output(
        ['git', 'show', f'{BASE}:{path}'], cwd=ROOT)
checks['dispatcher_yields_after_exception_handlers'] = compact(
    (ROOT / 'bots/gamma/src/main.cpp').read_text()).endswith('cambc::end_turn();}}')
report = {
    'scope': 'Source invariants; no engine movement, channel timing or strength inferred',
    'base_commit': BASE,
    'bot_cpp_sha256': hashlib.sha256(current.encode()).hexdigest(),
    'checks': checks,
    'passed': all(checks.values()),
}
(ROOT / 'experiments/gamma/recall-retry-source-check.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
raise SystemExit(0 if report['passed'] else 1)
