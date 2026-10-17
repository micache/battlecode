"""Source invariant for spell legality guards; not an engine spell simulation."""
from pathlib import Path
import re
import subprocess


def guarded_spells(source):
    code = re.sub(r'//[^\n]*', '', source)
    code = re.sub(r'\s+', '', code)
    try:
        helper = code.split('template<classTarget>', 1)[1].split('voidfarm_camps()', 1)[0]
        signature = 'boolattack_if_in_range(constTarget&target,boolallow_spell=true)'
        initial = ('if(!me.can_attack()||!target.is_visible()||target.health()<=0'
                   '||!me.attack_tiles().is_set(target.position())){returnfalse;}')
        refreshed = ('if(!allow_spell||!me.is_alive()||!target.is_visible()'
                     '||target.health()<=0)returntrue;')
        ready = 'if(!(ability.is_damage()||ability.is_cc())||!ability.is_ready())continue;'
        category = ('ifconstexpr(std::is_same_v<Target,cambc::camp>){'
                    'if(!ability.can_target_camps())continue;}'
                    'else{if(!ability.can_target_enemies())continue;}')
        ranged = 'if(!ability.valid_tiles().is_set(target.position()))continue;'
        cast = 'if(ability.use(target))break;'
        ordered = [signature, initial, 'me.attack(target);', refreshed,
                   'for(constauto&ability:me.abilities()){', ready, category, ranged, cast]
        positions = [helper.index(part) for part in ordered]
        farming = code.split('voidfarm_camps()', 1)[1].split('voidBot::play_turn()', 1)[0]
        post_walk = ('if(move_towards_closest(goals))'
                     'for(constauto&camp:cambc::vision::camps())'
                     'if(attack_if_in_range(camp,false))return;')
        return (positions == sorted(positions)
                and helper.endswith('returntrue;}')
                and code.count('ability.use(') == 1
                and code.count('attack_if_in_range(') == 4  # definition + three callers
                and post_walk in farming)
    except (ValueError, IndexError):
        return False


path = Path('bots/beta/src/bot.cpp')
source = path.read_text()
assert guarded_spells(source), 'missing spell guard or unsafe post-walk call'
accepted = subprocess.check_output([
    'git', 'show', '0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9:' + str(path)
], text=True)
assert not guarded_spells(accepted), 'accepted source must lack spell follow-up'
mutations = (
    ('!allow_spell || ', ''),
    ('!me.is_alive() || ', ''),
    ('!target.is_visible() || target.health() <= 0', 'false'),
    ('!ability.is_ready()', 'false'),
    ('!ability.can_target_camps()', 'false'),
    ('!ability.can_target_enemies()', 'false'),
    ('!ability.valid_tiles().is_set(target.position())', 'false'),
    ('if (ability.use(target)) break;', 'ability.use(target);'),
    ('attack_if_in_range(camp, false)', 'attack_if_in_range(camp)'),
)
for before, after in mutations:
    assert before in source
    assert not guarded_spells(source.replace(before, after)), before
print('PASS: basic attack precedes guarded damage/CC follow-up; live survival, '
      'visibility, readiness, category, range and single-success checks present; '
      'post-walk spells disabled. Accepted source and nine mutations rejected. '
      'Source invariant only; no runtime damage/fuel claim.')
