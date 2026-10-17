"""Check the source invariant that wounded spawn occupants yield before actions.

This inspects control-flow placement, not engine execution or healing behavior.
It must also reject the accepted source and a guard missing either condition.
"""
from pathlib import Path
import re
import subprocess

SOURCE = Path('bots/beta/src/bot.cpp')
GUARD = re.compile(
    r'if\s*\(at_spawn\s*&&\s*me\.health\(\)\s*<\s*me\.max_health\(\)\)'
    r'\s*return\s*;'
)


def preserves_recovery(source):
    body = source.split('void Bot::play_turn() {', 1)[1]
    # Ignore comments when locating the first action after spawn shopping.
    body = re.sub(r'//[^\n]*', '', body)
    guard = GUARD.search(body)
    if guard is None:
        return False
    spawn = body.index('const bool at_spawn =')
    shop = body.index('buy_items();', spawn)
    first_action = min(body.index(x, shop) for x in
                       ('me.recall();', 'attack_if_in_range(enemy)',
                        'me.submit_gems(altar);', 'move_towards_closest(goals)',
                        'farm_camps();'))
    return body.index('if (!me.is_alive()') < spawn < shop < guard.start() < first_action


source = SOURCE.read_text()
assert preserves_recovery(source), 'injured spawn occupants can reach field actions'
baseline = subprocess.check_output([
    'git', 'show',
    '0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9:' + str(SOURCE)
], text=True)
assert not preserves_recovery(baseline), 'test must detect the accepted-source defect'
for condition in ('at_spawn && ', 'me.health() < me.max_health()'):
    assert not preserves_recovery(source.replace(condition, '', 1))
print('PASS: spawn recovery guard precedes field actions; accepted source and both condition-removal mutations are rejected.')
