"""Static safety/isolation contracts; engine behavior is checked by bot-check."""
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / 'bots/beta/src/bot.cpp'
BASE = '9f7ae1c88a1bd0d5d62ed7713956efd40c95be33'


def function(text, name):
    start = text.index(name)
    opening = text.index('{', start)
    depth = 1
    end = opening + 1
    while depth:
        depth += (text[end] == '{') - (text[end] == '}')
        end += 1
    return text[start:end]


def contracts(source):
    body = re.sub(r'//[^\n]*', '', function(source, 'bool Bot::return_to_shop()'))
    before_recall = body[:body.index('me.recall();')]
    guards = ['gold < shopping_gold', 'me.gem_count() != 0',
              'me.champion_name() == cambc::champion_type::tavi',
              'spawn.is_set(me.position())',
              'me.restrictions().contains(cambc::buff_restrictions::move)',
              'g.spawns.is_set(me.position())',
              'std::holds_alternative<cambc::map::camp_group_reward_available>(g.group.state())',
              'if (exposed(me.position())) return false;']
    if not all(g in before_recall for g in guards):
        return False
    if before_recall.index('g.spawns.is_set(me.position())') > before_recall.index('g.group.state()'):
        return False
    economic = body[body.index('const auto walk_rounds'):]
    if 'recovering = true' in economic:
        return False
    return all(g in economic for g in [
        '!walk_rounds || cambc::fuel_remaining() < scan_reserve',
        'field.compute_to(terrain, spawn, around(me.position(), 0), visited, max_steps)',
        'field.get(me.position()) == cambc::distance_field::unreachable',
        'cambc::fuel_remaining() < planning_reserve'])


source = SOURCE.read_text()
base = subprocess.check_output(['git', 'show', f'{BASE}:bots/beta/src/bot.cpp'], cwd=ROOT, text=True)
assert contracts(source)
# Verify unsafe edits fail the contracts, rather than merely accepting any helper.
mutants = [
    ('me.gem_count() != 0', 'false'),
    ('spawn.is_set(me.position())', 'false'),
    ('g.spawns.is_set(me.position())', 'true'),
    ('camp_group_reward_available>(g.group.state())', 'camp_group_alive>(g.group.state())'),
    ('if (exposed(me.position())) return false;', ''),
    ('!walk_rounds || cambc::fuel_remaining() < scan_reserve', '!walk_rounds'),
    ('visited, max_steps)', 'visited)'),
    ('field.get(me.position()) == cambc::distance_field::unreachable', 'false'),
    ('cambc::fuel_remaining() < planning_reserve) return false;\n    // No recovery latch',
     'false) return false;\n    // No recovery latch'),
    ('// No recovery latch:', 'recovering = true; // No recovery latch:'),
]
helper = function(source, 'bool Bot::return_to_shop()')
for old, new in mutants:
    assert old in helper, old
    assert not contracts(source.replace(helper, helper.replace(old, new))), old
for name in ['void Bot::buy_items()', 'void Bot::farm_camps()', 'bool bank()',
             'bool move_to(', 'bool fight(', 'bool exposed(']:
    assert function(source, name) == function(base, name), name
turn = function(source, 'void Bot::play_turn()')
assert turn.index('if (bank()) return;') < turn.index('if (return_to_shop()) return;')
assert turn.index('if (return_to_shop()) return;') < turn.index('farm_camps();')
for name in ['main.cpp', 'draft.cpp', 'draft.h', 'random.h']:
    expected = subprocess.check_output(['git', 'show', f'{BASE}:bots/beta/src/{name}'], cwd=ROOT)
    assert (ROOT / 'bots/beta/src' / name).read_bytes() == expected, name
print('PASS: shopping safety contracts; ten unsafe mutations rejected.')
print('PASS: banking, camp policy, combat, items, draft and official yield preserved.')
print('Policy budget boundaries are static_asserts compiled by the trusted wrapper.')
print('Static contracts do not establish recall coverage, fuel headroom or strength.')
