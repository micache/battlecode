"""Check the same-turn arrival invariant, not engine channel execution.

Require a fresh position/range/lock check after successful banking movement,
and retain the accepted policy everywhere outside that arrival continuation.
"""
from pathlib import Path
import re
import subprocess


def arrival_continuation(source):
    bank = source.split('// Bank any carried gems before farming.', 1)[1]
    return bank.split('\n    farm_camps();', 1)[0]


def valid_arrival(source):
    bank = re.sub(r'//[^\n]*', '', arrival_continuation(source))
    return re.search(
        r'if \(move_towards_closest\(goals\)\) \{\s*'
        r'for \(auto altar : cambc::map::altars\(\).positions\(\)\) \{\s*'
        r'if \(distance\(me.position\(\), altar\) <= cambc::constants::submit_gems_range'
        r'\s*&& !cambc::vision::has_altar_lock\(altar\)\) \{\s*'
        r'me.submit_gems\(altar\);\s*return;\s*\}\s*\}\s*\}\s*'
        r'return;\s*\}\s*$', bank) is not None


path = Path('bots/beta/src/bot.cpp')
source = path.read_text()
accepted = '0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9'
baseline = subprocess.check_output(['git', 'show', f'{accepted}:{path}'], text=True)
assert valid_arrival(source), 'arrival can yield without starting eligible tribute'
assert not valid_arrival(baseline), 'must detect accepted arrival delay'

# Each mutation affects only the newly added continuation.
marker = '        // Start the countdown on arrival,'
prefix, continuation = source.split(marker, 1)
for old, new in (
    ('if (move_towards_closest(goals))', 'if (true)'),
    ('distance(me.position(), altar)', 'distance(old_position, altar)'),
    ('<= cambc::constants::submit_gems_range', '<= 100'),
    ('!cambc::vision::has_altar_lock(altar)', 'true'),
    ('me.submit_gems(altar);\n                    return;', 'me.submit_gems(altar);'),
):
    assert old in continuation
    assert not valid_arrival(prefix + marker + continuation.replace(old, new, 1)), old

# Removing the insertion must recover accepted code, including original combat,
# channel preservation, immediate tribute and fallback behavior.
end = continuation.index('        return;\n    }')
restored = prefix + '        move_towards_closest(goals);\n' + continuation[end:]
assert restored == baseline, 'unrelated accepted behavior changed'
for other in path.parent.iterdir():
    if other == path or not other.is_file():
        continue
    assert other.read_bytes() == subprocess.check_output(
        ['git', 'show', f'{accepted}:{other}']), other
print('PASS: successful banking arrival checks fresh position, range and lock; '
      'starts tribute before returning. Accepted source and five guard/staleness/'
      'return mutations rejected. All other source matches accepted. '
      'Source invariant only; engine timing and strategic value remain unmeasured.')
