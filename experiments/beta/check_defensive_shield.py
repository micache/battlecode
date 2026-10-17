"""Check the shield safety invariant and patch scope; not a combat simulation."""
from pathlib import Path
import re
import subprocess


def compact(text):
    return re.sub(r'\s+', '', re.sub(r'//[^\n]*', '', text))


def guarded_shield(source):
    code = compact(source)
    try:
        helper = code.split('template<classTarget>', 1)[1].split('voidfarm_camps()', 1)[0]
        ordered = [
            'if(!me.can_attack()||!target.is_visible()||target.health()<=0'
            '||!me.attack_tiles().is_set(target.position())){returnfalse;}',
            'if(target.strength()>0&&target.attack_tiles().is_set(me.position())){',
            'for(constauto&ability:me.abilities()){',
            'if(ability.is_shield()&&ability.can_target_self()&&ability.is_ready())',
            'if(ability.use())break;',
            'if(!me.can_attack())returnfalse;',
            'me.attack(target);',
        ]
        indices = [helper.index(token) for token in ordered]
        return indices == sorted(indices) and code.count('ability.use(') == 1
    except (ValueError, IndexError):
        return False


path = Path('bots/beta/src/bot.cpp')
source = path.read_text()
accepted = subprocess.check_output([
    'git', 'show', '0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9:' + str(path)
], text=True)
assert guarded_shield(source), 'missing shield guard or unsafe action order'
assert not guarded_shield(accepted), 'baseline must lack defensive shield'
start = source.index('\n    // Shield before exposing')
end = source.index('    me.attack(target);', start)
assert source[:start] + source[end:] == accepted, 'unrelated behavior changed'
for before, after in (
    ('!target.is_visible() || ', ''),
    ('target.strength() > 0 && ', ''),
    ('target.attack_tiles().is_set(me.position())', 'true'),
    ('ability.is_shield() && ', ''),
    ('ability.can_target_self() && ', ''),
    (' && ability.is_ready()', ''),
    ('if (ability.use()) break;', 'ability.use();'),
    ('if (!me.can_attack()) return false;', ''),
):
    assert before in source
    assert not guarded_shield(source.replace(before, after)), before
print('PASS: legal visible living attack target precedes shield; positive Strength, '
      'threat range, shield kind, self permission and readiness required; at most '
      'one successful cast; attack allowance refreshed. Baseline and eight unsafe '
      'mutations rejected. Only this block differs from accepted bot.cpp. '
      'Source invariant only; no runtime survival or fuel claim.')
