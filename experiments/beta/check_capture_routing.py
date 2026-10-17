"""Source invariant for visible collector routing, not an engine simulation.

Reject accepted source and mutations that abandon own captures, inspect hidden
state, omit the cleared-state condition, or treat self as another collector.
"""
from pathlib import Path
import re
import subprocess


def collector_guard(source):
    body = source.split('void farm_camps() {', 1)[1].split('void Bot::play_turn()', 1)[0]
    body = re.sub(r'//[^\n]*', '', body)
    return bool(re.search(
        r'auto other_allies = cambc::vision::champion_tiles\(team::ally\);\s*'
        r'const auto position = cambc::self\(\).position\(\);\s*'
        r'other_allies.set\(position, false\);\s*'
        r'for \(const auto& group : cambc::map::camp_groups\(\)\) \{\s*'
        r'const auto spawns = group.spawn_tiles\(\);\s*'
        r'const bool group_visible = !\(spawns & visible\).is_empty\(\);\s*'
        r'if \(group_visible\) \{\s*'
        r'const auto state = group.state\(\);\s*'
        r'if \(std::holds_alternative<cambc::map::camp_group_respawning>\(state\)\)\s*'
        r'continue;\s*'
        r'if \(std::holds_alternative<cambc::map::camp_group_reward_available>\(state\)\s*'
        r'&& !spawns.is_set\(position\) && !\(spawns & other_allies\).is_empty\(\)\)\s*'
        r'continue;\s*\}\s*goals \|= spawns;', body))


path = Path('bots/beta/src/bot.cpp')
source = path.read_text()
assert collector_guard(source), 'collector routing invariant missing'
accepted = subprocess.check_output([
    'git', 'show', '0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9:' + str(path)
], text=True)
assert not collector_guard(accepted), 'must detect baseline redundant destinations'
for old, new in (
    ('if (group_visible)', 'if (true)'),
    ('other_allies.set(position, false);', ''),
    ('!spawns.is_set(position)', 'true'),
    ('std::holds_alternative<cambc::map::camp_group_reward_available>(state)', 'true'),
    ('!(spawns & other_allies).is_empty()', '(spawns & other_allies).is_empty()'),
):
    assert old in source
    assert not collector_guard(source.replace(old, new, 1)), old

# Keep this experiment confined to farming destination construction. Attacks,
# banking, draft, item selection, RNG, shared memory, and yielding are unchanged.
start = '    // Union every group'
end = '    // Fresh vision after movement'
old_begin, old_end = accepted.index(start), accepted.index(end)
new_begin = source.index('    // Route to groups needing work')
new_end = source.index(end)
assert source[:new_begin] == accepted[:old_begin]
assert source[new_end:] == accepted[old_end:]
for p in path.parent.iterdir():
    if p.is_file() and p != path:
        assert p.read_bytes() == subprocess.check_output([
            'git', 'show', '0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9:' + str(p)
        ]), p
print('PASS: visible cleared groups with another allied collector are excluded; '
      'own captures and hidden/alive groups remain eligible. Accepted source and '
      'five guard mutations rejected; all other source unchanged. Source check only.')
