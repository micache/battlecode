"""Safety contract checks on the integrated policy; not a game simulation."""
from pathlib import Path
import re

src = Path('bots/beta/src/bot.cpp').read_text()
main = Path('bots/beta/src/main.cpp').read_text()
draft = Path('bots/beta/src/draft.cpp').read_text()

def check(s):
    p = s.split('void Bot::play_turn() {')[1]
    assert p.index('buy_items();') < p.index('if (!me.is_alive())')
    assert p.index('me.is_recalling() || me.is_submitting_gems() || me.is_teleporting()') < p.index('move_to(spawn)')
    assert re.search(r'if \(spawn.is_set\(me.position\(\)\)\) \{\s*//[^\n]*\n\s*if \(me.health\(\) < me.max_health\(\)\) return;', p)
    assert p.index('if (bank()) return;') < p.index('fight(enemy)')
    assert 'if (seen) {\n            const auto state = g.group.state();' in s
    assert 'if (available && g.spawns.is_set(me.position())) return;' in s
    assert s.index('if (available && g.spawns.is_set(me.position())) return;') < s.index('if (available && !(g.spawns & allies).is_empty()) continue;')
    assert 'goals &= ~blocked;' in s and 'goals &= ~blocked |' not in s
    assert 'if (walked && excludes_walk) continue;' in s
    assert 'if (!me.is_alive() || !target.is_visible() || target.health() <= 0 || !me.can_cast()) return acted;' in s
    assert '&& target.health() > 0 && me.can_attack()' in s
    assert 'for (int attempt = 0; attempt < 2; ++attempt)' in s
    assert 'if (cambc::fuel_remaining() < planning_reserve)' in s
    assert 'shared_memory' not in s

check(src)
mutations = [
    ('if (me.health() < me.max_health()) return;', ''),
    ('if (seen) {\n            const auto state', 'if (true) {\n            const auto state'),
    ('if (available && g.spawns.is_set(me.position())) return;', ''),
    ('goals &= ~blocked;', 'goals &= ~blocked | cambc::vision::camp_tiles();'),
    ('if (walked && excludes_walk) continue;', ''),
    ('|| !target.is_visible() || target.health() <= 0 || !me.can_cast()', '|| !me.can_cast()'),
    ('for (int attempt = 0; attempt < 2; ++attempt)', 'while (true)'),
]
for old, new in mutations:
    assert old in src
    try:
        check(src.replace(old, new, 1))
    except AssertionError:
        pass
    else:
        raise AssertionError('missed unsafe mutation: ' + old)
assert 'cambc::end_turn();' in main and main.index('catch (...)') < main.index('cambc::end_turn();')
assert 'draft::team_size()' in draft and 'std::find(chosen.begin(), chosen.end(), pick)' in draft
print('PASS: channel/spawn/capture preservation, dead shopping, observation guards, free roots, bounded retries, movement exclusions and reset guards; seven unsafe mutations rejected. Source contracts only, no runtime/fuel claim.')
