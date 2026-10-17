"""Source invariants only: does not execute C++ or simulate the engine."""
from pathlib import Path
import re
import subprocess

SOURCE = Path('bots/beta/src/bot.cpp')
BASE = '0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9'
source = SOURCE.read_text()


def compact(text):
    return re.sub(r'\s+', '', text)


def valid(text):
    try:
        helper = text.split('bool attack_weakest_camp_in_range() {', 1)[1].split(
            '// Attack a camp already in range,', 1)[0]
        c = compact(helper)
        ordered = [
            'if(!me.can_attack())returnfalse;',
            'constautoattack_tiles=me.attack_tiles();',
            'constautocamps=cambc::vision::camps();',
            'for(constauto&camp:camps){',
            'if(!camp.is_visible())continue;',
            'constautohealth=camp.health();',
            'if(health<=0||!attack_tiles.is_set(camp.position()))continue;',
            'if(!weakest||health<weakest_health){weakest=&camp;weakest_health=health;}',
            'returnweakest&&attack_if_in_range(*weakest);',
        ]
        positions = [c.index(token) for token in ordered]
        if positions != sorted(positions) or c.count('for(') != 1:
            return False
        farm = compact(text.split('void farm_camps() {', 1)[1].split('void Bot::play_turn()', 1)[0])
        return (farm.startswith('if(attack_weakest_camp_in_range())return;')
                and farm.count('attack_weakest_camp_in_range()') == 2
                and 'if(move_towards_closest(goals))attack_weakest_camp_in_range();' in farm)
    except (IndexError, ValueError):
        return False


assert valid(source), 'minimum-health selection or refreshed post-move selection missing'
for before, after in [
    ('!camp.is_visible()', 'false'),
    ('health < weakest_health', 'health > weakest_health'),
    ('health <= 0 || !attack_tiles.is_set(camp.position())', 'health <= 0'),
    ('!me.can_attack()', 'false'),
    ('health < weakest_health', 'health <= weakest_health'),
    ('if (move_towards_closest(goals))\n        attack_weakest_camp_in_range();',
     'move_towards_closest(goals);'),
]:
    prefix, selector_onward = source.split('bool attack_weakest_camp_in_range()', 1)
    assert before in selector_onward
    mutated = prefix + 'bool attack_weakest_camp_in_range()' + selector_onward.replace(before, after, 1)
    assert not valid(mutated), before

baseline = subprocess.check_output(['git', 'show', f'{BASE}:{SOURCE}'], text=True)
assert not valid(baseline), 'accepted first-entry selection must fail the invariant'
# Reverse only the two call sites and inserted selector to verify experiment scope.
start = source.index('// Finish the lowest-health legal camp first;')
end = source.index('// Attack a camp already in range,', start)
restored = source[:start] + source[end:]
restored = restored.replace(
    '    if (attack_weakest_camp_in_range())\n        return;',
    '    for (const auto& camp : cambc::vision::camps())\n'
    '        if (attack_if_in_range(camp))\n            return;', 1)
restored = restored.replace(
    '    if (move_towards_closest(goals))\n        attack_weakest_camp_in_range();',
    '    if (move_towards_closest(goals))\n'
    '        for (const auto& camp : cambc::vision::camps())\n'
    '            if (attack_if_in_range(camp))\n                return;', 1)
assert restored == baseline, 'unrelated champion policy changed'
for path in SOURCE.parent.iterdir():
    if path.is_file() and path != SOURCE:
        assert path.read_bytes() == subprocess.check_output(['git', 'show', f'{BASE}:{path}']), path
print('PASS: visible living in-range strict minimum-health scan, stable ties, availability guard, fresh post-move selection.')
print('PASS: accepted source and six unsafe mutations rejected; only camp target selection differs from accepted.')
print('Source invariants only; C++ execution, fuel and strategic value require trusted checks/evaluation.')
