"""Source invariant for the last-hit continuation; not an engine simulation."""
from pathlib import Path
import re
import subprocess


def continuation(source):
    farm = source.split('void farm_camps() {', 1)[1]
    return farm.split('// Union every group', 1)[0]


def valid(source):
    branch = re.sub(r'//[^\n]*', '', continuation(source))
    return re.fullmatch(
        r'\s*for \(const auto& camp : cambc::vision::camps\(\)\)\s*'
        r'if \(attack_if_in_range\(camp\)\) \{\s*'
        r'auto& me = cambc::self\(\);\s*'
        r'if \(me.is_alive\(\) && me.can_move\(\)\) \{\s*'
        r'const auto group = camp.camp_group\(\);\s*'
        r'const auto spawns = group.spawn_tiles\(\);\s*'
        r'if \(!\(spawns & cambc::vision::visible_tiles\(\)\).is_empty\(\)\s*'
        r'&& std::holds_alternative<cambc::map::camp_group_reward_available>'
        r'\(group.state\(\)\)\)\s*'
        r'move_towards_closest\(spawns\);\s*\}\s*return;\s*\}\s*',
        branch) is not None


path = Path('bots/beta/src/bot.cpp')
source = path.read_text()
accepted = '0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9'
baseline = subprocess.check_output(['git', 'show', f'{accepted}:{path}'], text=True)
assert valid(source), 'unsafe or missing last-hit capture continuation'
assert not valid(baseline), 'accepted source must expose the missed continuation'

for old, new in (
    ('if (attack_if_in_range(camp)) {', 'if (true) {'),
    ('me.is_alive() && me.can_move()', 'me.can_move()'),
    ('me.is_alive() && me.can_move()', 'me.is_alive()'),
    ('camp.camp_group()', 'other.camp_group()'),
    ('!(spawns & cambc::vision::visible_tiles()).is_empty()', 'true'),
    ('camp_group_reward_available>(group.state())', 'camp_group_alive>(group.state())'),
    ('move_towards_closest(spawns)', 'move_towards_closest(all_spawns)'),
    ('            return;\n        }', '        }'),
):
    assert old in source, old
    assert not valid(source.replace(old, new, 1)), old

# Only this stationary-attack branch changes. Post-movement attacks, target
# order, routing fallback, channel/combat/banking and end_turn are preserved.
original_branch = continuation(baseline)
restored = source.replace(continuation(source), original_branch, 1)
assert restored == baseline, 'unrelated accepted behavior changed'
helper = source.split('bool move_towards_closest', 1)[1].split('void Bot::buy_items', 1)[0]
assert 'if (!me.can_move() || goals.is_set(me.position()))\n        return false;' in helper
for other in path.parent.iterdir():
    if other != path and other.is_file():
        assert other.read_bytes() == subprocess.check_output(
            ['git', 'show', f'{accepted}:{other}']), other
print('PASS: successful stationary camp attack gates an alive/movement check, '
      'fresh visibility and cleared state before approaching that same group; '
      'already-on-goal holds. Accepted source and eight mutations rejected. '
      'All other source matches accepted. Source invariant only; actual capture '
      'timing, fuel headroom and strategic value remain unmeasured.')
