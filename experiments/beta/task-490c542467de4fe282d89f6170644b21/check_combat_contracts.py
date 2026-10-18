"""Source safety regressions; no engine, fuel or comparative-performance claim."""
from pathlib import Path

source = Path('bots/beta/src/bot.cpp').read_text()
main = Path('bots/beta/src/main.cpp').read_text()

def check(s):
    observe = s.split('auto observe_targets(')[1].split('template<class Target>')[0]
    fight = s.split('bool fight(ReadTargets')[1].split('\nbool bank()')[0]
    play = s.split('void Bot::play_turn()')[1]
    # No hidden health/position queries, and observation work has a fixed cap.
    assert observe.index('if (!target.is_visible()) continue;') < observe.index('target.health()') < observe.index('target.position()')
    assert '++examined > combat_target_limit' in observe
    assert 'fuel_remaining() < combat_scan_reserve' in observe
    # Reset requires a currently observed legal basic target; an unrelated corpse
    # must not terminate the entire ability phase after the first basic.
    assert 'if (!me.can_attack() && reset_target && ability.can_target_self()' in fight
    assert 'const auto reset_target = basic_target(targets);' in fight
    assert fight.index('me.attack(target->target);\n                acted = true;') < fight.index('const auto reset_target')
    assert 'if (walked && excludes_walk) continue;' in fight
    assert 'buff_restrictions::attack' in fight and 'buff_restrictions::cast' in fight
    assert 'if (!best || !aim || !me.is_alive() || !me.can_cast()' in fight
    assert '!aim->target.is_visible() || aim->target.health() <= 0' in fight
    # The follow-up is selected from a new scan; it never attacks the saved aim.
    follow = fight.split('auto attack_fresh = [&]')[1].split('if (can_attack()) {')[0]
    assert 'observe_targets<Target>(read_targets, eligible)' in follow
    assert 'basic_target(targets)' in follow
    assert 'if (me.is_alive()) attack_fresh();' in fight
    assert 'me.attack(aim->target)' not in fight
    assert fight.count('best->use()') == 1 and 'while (' not in fight
    # Existing lifecycle/navigation contracts must survive the combat upgrade.
    assert play.index('buy_items();') < play.index('if (!me.is_alive())')
    assert play.index('me.is_recalling() || me.is_submitting_gems() || me.is_teleporting()') < play.index('move_to(spawn)')
    assert 'if (me.health() < me.max_health()) return;' in play
    assert play.index('if (bank()) return;') < play.index('fight<cambc::champion>')
    assert 'if (seen) {\n            const auto state = g.group.state();' in s
    assert s.index('if (available && g.spawns.is_set(me.position())) return;') < s.index('if (available && !(g.spawns & allies).is_empty()) continue;')
    assert 'goals &= ~blocked;' in s and 'goals &= ~blocked |' not in s
    assert 'for (int attempt = 0; attempt < 2; ++attempt)' in s
    assert 'shared_memory' not in s

check(source)
mutations = [
    ('if (!target.is_visible()) continue;', ''),
    ('++examined > combat_target_limit', 'false'),
    ('!me.can_attack() && reset_target && ability.can_target_self()', '!me.can_attack() && ability.can_target_self()'),
    ('if (walked && excludes_walk) continue;', ''),
    ('!aim->target.is_visible() || aim->target.health() <= 0', 'false'),
    ('if (me.is_alive()) attack_fresh();', 'if (me.is_alive()) me.attack(aim->target);'),
    ('if (me.health() < me.max_health()) return;', ''),
    ('goals &= ~blocked;', 'goals &= ~blocked | cambc::vision::camp_tiles();'),
]
for old, new in mutations:
    assert old in source
    try:
        check(source.replace(old, new, 1))
    except (AssertionError, ValueError):
        continue
    raise AssertionError('unsafe mutation survived: ' + old)
assert main.index('catch (...)') < main.index('cambc::end_turn();')
print('PASS: refreshed combat targets, reset validity, visibility, restrictions, bounded scans/casts, unchanged channel/capture/recovery/free-root contracts; eight unsafe mutations rejected. Six hit-value static assertions compiled by bot-check. Source contracts only.')
