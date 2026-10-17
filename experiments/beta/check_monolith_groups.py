"""Source safety invariant, not an engine or strategic-performance test."""
from pathlib import Path
import re
import subprocess


def valid(source):
    if 'const cambc::bitboard& monolith_group_tiles() {' not in source:
        return False
    helper = source.split('const cambc::bitboard& monolith_group_tiles() {', 1)[1]
    helper = helper.split('// Attack a camp', 1)[0]
    farm = source.split('void farm_camps() {', 1)[1].split('void Bot::play_turn()', 1)[0]
    # Classification must cover the entire group, use immutable metadata only,
    # and be cached rather than repeatedly loading every group per attack.
    if not all(part in helper for part in (
        'static const auto tiles = []', 'result.clear();',
        'for (const auto& group : cambc::map::camp_groups())',
        'for (const auto& camp : group.camps())', 'if (camp.is_monolith())',
        'result |= group.spawn_tiles();', 'return tiles;',
    )):
        return False
    if any(part in helper for part in ('.state()', '.health()', '.position()')):
        return False
    guarded = '!excluded.is_set(camp.spawn_position()) && attack_if_in_range(camp)'
    if farm.count('attack_if_in_range(camp)') != 2 or farm.count(guarded) != 2:
        return False
    # Unknown Monolith groups must short-circuit before a live state query;
    # only current visible reward-available groups may supply travel goals.
    route = re.compile(
        r'if \(!\(group.spawn_tiles\(\) & excluded\).is_empty\(\)\s*'
        r'&& \(!group_visible \|\| !std::holds_alternative'
        r'<cambc::map::camp_group_reward_available>\(group.state\(\)\)\)\)\s*'
        r'continue;')
    match = route.search(farm)
    return (match is not None and match.end() < farm.index('goals |= group.spawn_tiles();')
            and 'const auto& excluded = monolith_group_tiles();' in farm)


path = Path('bots/beta/src/bot.cpp')
source = path.read_text()
accepted = '0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9'
baseline = subprocess.check_output(['git', 'show', f'{accepted}:{path}'], text=True)
assert valid(source), 'missing attack/routing/visibility safety invariant'
assert not valid(baseline), 'baseline should lack the Monolith policy'
for old, new in (
    ('result |= group.spawn_tiles();', 'result.set(camp.spawn_position());'),
    ('!excluded.is_set(camp.spawn_position()) && ', ''),
    ('!group_visible || ', ''),
    ('!group_visible || ', '!group_visible && '),
    ('camp_group_reward_available>(group.state())', 'camp_group_alive>(group.state())'),
):
    assert old in source
    assert not valid(source.replace(old, new, 1)), old

# No other champion policy or source file changes are part of this experiment.
prefix = '// Immutable metadata: do not spend basic attacks'
end = '// Attack a camp already in range'
restored = source[:source.index(prefix)] + source[source.index(end):]
restored = restored.replace('    const auto& excluded = monolith_group_tiles();\n', '', 1)
restored = restored.replace('!excluded.is_set(camp.spawn_position()) && ', '')
start = restored.index('        // Keep free captures')
stop = restored.index('        if (group_visible && ', start)
restored = restored[:start] + restored[stop:]
assert restored == baseline, 'unrelated source change'
for other in path.parent.iterdir():
    if other != path and other.is_file():
        assert other.read_bytes() == subprocess.check_output(
            ['git', 'show', f'{accepted}:{other}']), other
print('PASS: both farming attack paths exclude all members of Monolith groups; '
      'routing retains only visible cleared Monolith groups with visibility '
      'short-circuiting before live state reads. Classification uses cached '
      'static metadata. Baseline and five unsafe mutations rejected; unrelated '
      'source matches accepted. Runtime engagement, fuel and benefit unmeasured.')
