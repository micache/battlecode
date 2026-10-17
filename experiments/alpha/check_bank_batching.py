"""Check banking boundary decisions extracted from source, without SDK imports.

This checks the scalar policy and branch placement, not C++ execution or routing.
Compilation and engine smoke checks belong to bot-check.
"""
import argparse
import json
from pathlib import Path
import re
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--report', required=True)
args = parser.parse_args()
task = json.loads(Path('.agent/task.json').read_text())
source = Path('bots/alpha/src/bot.cpp').read_text()
turn = source.split('void Bot::play_turn() {', 1)[1]
bank = turn.split('if (me.gem_count() > 0) {', 1)[1]
minimum = int(re.search(r'constexpr unsigned bank_travel_minimum = (\d+);', bank)[1])
condition = re.search(r'if \((me.gem_count\(\) >= bank_travel_minimum.*?)\) \{', bank, re.S)[1]
expression = condition.replace('me.gem_count()', 'bag').replace(
    'cambc::global_submitted_gems(team::ally)', 'submitted').replace(
    'cambc::constants::winning_gems', 'winning').replace(
    'bank_travel_minimum', str(minimum)).replace('||', 'or')
expression = ' '.join(expression.split())
# Small ordinary bags farm; the threshold is inclusive; a winning bag overrides it.
cases = [
    (1, 0, 1000, False), (22, 0, 1000, False), (39, 0, 1000, False),
    (40, 0, 1000, True), (41, 0, 1000, True),
    (1, 999, 1000, True), (22, 978, 1000, True), (22, 977, 1000, False),
    (1, 1199, 1200, True), (1, 999, 1200, False),
]
checks = {}
for bag, submitted, winning, expected in cases:
    checks[f'bag={bag},submitted={submitted},winning={winning}'] = (
        eval(expression, {'__builtins__': {}}, dict(bag=bag, submitted=submitted, winning=winning))
        == expected)
checks['parameter_40_recorded'] = minimum == 40
# Guarding travel must not guard immediate tribute, or prevent farming afterward.
checks['adjacent_tribute_precedes_threshold'] = bank.index('me.submit_gems(altar);') < bank.index('bank_travel_minimum')
checks['small_bag_falls_through_to_farming'] = re.search(
    r'move_towards_closest\(goals\);\s*return;\s*}\s*}\s*farm_camps\(\);', bank) is not None
checks['channels_and_recall_precede_bank'] = turn.index('me.is_submitting_gems()') < turn.index('me.recall();') < turn.index('if (me.gem_count() > 0)')
checks['five_other_sources_unchanged'] = all(
    p.read_bytes() == subprocess.check_output(['git', 'show', f"{task['accepted_commit']}:{p.as_posix()}"])
    for p in Path('bots/alpha/src').iterdir() if p.name != 'bot.cpp')
report = {'passed': all(checks.values()), 'checks': checks,
          'limits': 'Extracted scalar guard and source contracts only; no runtime branch coverage, path safety, fuel or game result.'}
Path(args.report).write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report))
raise SystemExit(0 if report['passed'] else 1)
