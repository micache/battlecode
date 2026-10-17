"""Source-level banking invariant; does not simulate channel completion.

Reject the accepted control flow and mutations removing eligibility conditions.
The trusted wrapper supplies compilation and engine smoke coverage.
"""
from pathlib import Path
import re
import subprocess


def takes_immediate_tribute(source):
    body = source.split('void Bot::play_turn() {', 1)[1]
    body = re.sub(r'//[^\n]*', '', body)
    combat = body.index('for (const auto& enemy :')
    early = body[:combat]
    eligibility = re.search(
        r'if\s*\(me\.gem_count\(\) > 0\)\s*\{\s*'
        r'for \(auto altar : cambc::map::altars\(\).positions\(\)\)\s*\{\s*'
        r'if \(distance\(me.position\(\), altar\) <= cambc::constants::submit_gems_range'
        r'\s*&& !cambc::vision::has_altar_lock\(altar\)\)\s*\{\s*'
        r'me.submit_gems\(altar\);\s*return;\s*\}\s*\}\s*\}', early)
    if eligibility is None:
        return False
    guards = ('!me.is_alive()', 'me.is_recalling()', 'me.is_submitting_gems()',
              'me.is_teleporting()', '(!me.can_move() && !me.can_attack())',
              'me.recall();')
    return (all(early.index(g) < eligibility.start() for g in guards)
            and body.count('me.submit_gems(altar);') == 1
            and combat < body.index('move_towards_closest(goals)')
            and combat < body.index('farm_camps();'))


source_path = Path('bots/beta/src/bot.cpp')
source = source_path.read_text()
assert takes_immediate_tribute(source), 'eligible immediate tribute can lose to combat'
baseline = subprocess.check_output([
    'git', 'show', '0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9:' + str(source_path)
], text=True)
assert not takes_immediate_tribute(baseline), 'must detect accepted combat-first policy'
for old, new in (
    ('me.gem_count() > 0', 'true'),
    ('distance(me.position(), altar) <= cambc::constants::submit_gems_range', 'true'),
    ('!cambc::vision::has_altar_lock(altar)', 'true'),
    ('me.submit_gems(altar);\n                return;', 'me.submit_gems(altar);'),
):
    assert old in source
    assert not takes_immediate_tribute(source.replace(old, new, 1)), old
print('PASS: eligible immediate tribute precedes combat after existing guards; '
      'accepted source and four eligibility/return mutations rejected. '
      'Distant routing and farming remain after combat. Source invariant only.')
