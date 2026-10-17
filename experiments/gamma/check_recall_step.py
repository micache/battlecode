"""Focused source invariants; official compilation/runtime use bot-check."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
BASE = '1a0675ca881d4b67cb5c6cb1822ce2ae1602dc4d'
SOURCE = 'bots/gamma/src/bot.cpp'
accepted = subprocess.check_output(['git', 'show', f'{BASE}:{SOURCE}'], cwd=ROOT, text=True)
current = (ROOT / SOURCE).read_text()


def code(text):
    return re.sub(r'//[^\n]*|/\*.*?\*/', '', text, flags=re.S)


def recovery(text):
    match = re.search(
        r'if \(!at_spawn && me.health\(\) < me.max_health\(\) \* 0\.35f\) \{([^}]+)\}',
        code(text))
    assert match, 'Expected one bounded low-health recovery branch'
    return match.group(1)


def retreats_before_recall(text):
    return re.fullmatch(
        r'\s*const auto spawn = cambc::map::spawn_region\(team::ally\);'
        r'\s*move_towards_closest\(spawn\);'
        r'\s*if \(!spawn.is_set\(me.position\(\)\)\)'
        r'\s*me.recall\(\);\s*return;\s*', recovery(text)) is not None


checks = {
    'accepted_reproduces_stationary_recall_initiation': not retreats_before_recall(accepted)
        and recovery(accepted).strip() == 'me.recall();\n        return;',
    'candidate_attempts_one_spawnward_move_before_recall': retreats_before_recall(current),
    'only_recovery_branch_behavior_changes': (
        code(accepted).replace(recovery(accepted), '')
        == code(current).replace(recovery(current), '')),
    'existing_channels_preserved_before_recovery': (
        current.index('me.is_recalling()') < current.index('if (!at_spawn && me.health()')
        and current.index('me.is_submitting_gems()') < current.index('if (!at_spawn && me.health()')
        and current.index('me.is_teleporting()') < current.index('if (!at_spawn && me.health()')),
}
for name in ['bot.h', 'main.cpp', 'draft.h', 'draft.cpp', 'random.h']:
    path = f'bots/gamma/src/{name}'
    checks[f'unchanged_{name}'] = (ROOT / path).read_bytes() == subprocess.check_output(
        ['git', 'show', f'{BASE}:{path}'], cwd=ROOT)
main = code((ROOT / 'bots/gamma/src/main.cpp').read_text())
checks['dispatcher_still_yields_after_fallback_catches'] = (
    main.count('cambc::end_turn();') == 1
    and main.index('cambc::end_turn();') > main.index('catch (...)'))
diff = subprocess.run(['git', 'diff', '--check'], cwd=ROOT, capture_output=True, text=True)
checks['diff_check'] = diff.returncode == 0
report = {
    'kind': 'Source invariants only; no engine timing, movement or strategic gain established',
    'base_commit': BASE,
    'bot_cpp_sha256': hashlib.sha256(current.encode()).hexdigest(),
    'checks': checks,
    'diff_check_exit_code': diff.returncode,
    'passed': all(checks.values()),
}
path = ROOT / 'experiments/gamma/recall-step-source-check.json'
path.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
raise SystemExit(0 if report['passed'] else 1)
