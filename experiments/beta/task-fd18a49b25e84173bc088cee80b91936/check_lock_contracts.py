"""Static safety regression: placement uses visible empty altars and bounded work.

This checks observation/action contracts, not engine execution or strategic gains.
The trusted wrapper compiles and smoke-checks the actual C++ source.
"""
from pathlib import Path
import re
import subprocess

PATH = Path('bots/beta/src/bot.cpp')
source = PATH.read_text()
base = subprocess.check_output([
    'git', 'show', 'd2d57274232ca7cead5bacf650d6f51fd5b3bc3d:' + str(PATH)
], text=True)


def code(text):
    return re.sub(r'//[^\n]*|/\*.*?\*/', '', text, flags=re.S)


def contracts(text):
    try:
        text = code(text)
        lock = text.split('void lock_nearby_altar() {', 1)[1].split('\n}\n', 1)[0]
        use = lock.index('lock.use(altar);')
        guard = lock[:lock.index('const auto& lock')]
        for required in ('cambc::fuel_remaining() < lock_reserve', '!me.is_alive()',
                         'me.is_recalling()', 'me.is_submitting_gems()',
                         'me.is_teleporting()',
                         'me.restrictions().contains(cambc::buff_restrictions::consumable)'):
            assert required in guard
        assert 'return;' in guard
        assert lock.index('if (!lock.count()) return;') < use
        mask = lock.split('const auto candidates =', 1)[1].split(';', 1)[0]
        for term in ('around(me.position(), lock_placement_range)',
                     '& cambc::map::altars()', '& cambc::vision::visible_tiles()',
                     '& ~cambc::vision::altar_lock_tiles()'):
            assert term in mask
        assert re.search(r'lock.use\(altar\);\s*return;', lock)
        assert 'while' not in lock and lock.count('lock.use(') == 1
        assert 'constexpr int lock_placement_range = 2;' in text
        move = text.split('bool move_to(', 1)[1].split('\nbool exposed(', 1)[0]
        assert re.search(r'if \(me.move_absolute\(best\)\) \{\s*lock_nearby_altar\(\);\s*return true;', move)
        turn = text.split('void Bot::play_turn() {', 1)[1]
        assert turn.index('me.is_teleporting()) return;') < turn.index('lock_nearby_altar();')
        shop = text.split('void Bot::buy_items() {', 1)[1].split('void Bot::farm_camps()', 1)[0]
        assert shop.index('if (me.can_buy(lock)) me.buy(lock);') < shop.index('using I =')
        # Friendly locks must not prevent our own banking. Hostile locks retain
        # attack-permission gating and the engine's lock-attack fallback.
        bank = text.split('bool bank() {', 1)[1].split('} // namespace', 1)[0]
        assert 'altar_lock_tiles(team::enemy)' in bank
        assert 'if (!enemy_locks.is_set(altar) || me.can_attack())' in bank
        assert 'me.submit_gems(altar);' in bank
        return True
    except (AssertionError, ValueError, IndexError):
        return False


assert contracts(source), 'unsafe placement/shop/banking contract'
mutations = [
    ('|| me.is_submitting_gems()', ''),
    ('|| me.restrictions().contains(cambc::buff_restrictions::consumable)', ''),
    ('if (!lock.count()) return;', ''),
    ('& cambc::vision::visible_tiles()', ''),
    ('& ~cambc::vision::altar_lock_tiles()', ''),
    ('around(me.position(), lock_placement_range)', 'cambc::map::altars()'),
    ('lock.use(altar);\n        return;', 'lock.use(altar);'),
    ('if (me.can_buy(lock)) me.buy(lock);', 'me.buy(lock);'),
    ('altar_lock_tiles(team::enemy)', 'altar_lock_tiles()'),
    ('if (me.move_absolute(best)) {', 'if (true) {'),
]
for old, new in mutations:
    assert old in source, old
    assert not contracts(source.replace(old, new, 1)), old
assert not contracts(base)
# Scope check: farming/combat/recovery/draft and turn-yield logic are preserved.
for marker in ('bool exposed(', 'bool bank()', 'void Bot::farm_camps()'):
    def body(s):
        return s.split(marker, 1)[1].split('\n}\n', 1)[0]
    assert body(source) == body(base), marker
for filename in ('bot.h', 'main.cpp', 'draft.cpp', 'draft.h', 'random.h'):
    p = PATH.parent / filename
    assert p.read_bytes() == subprocess.check_output([
        'git', 'show', 'd2d57274232ca7cead5bacf650d6f51fd5b3bc3d:' + str(p)])
print('PASS: placement visibility, range, occupancy, inventory, channel, restriction, fuel and bounded-attempt contracts.')
print('PASS: guarded consumable purchase and fresh post-movement placement; friendly/hostile bank semantics preserved.')
print('PASS: 10 unsafe mutations rejected; farming/combat/recovery, draft and official yield remain at edit base.')
print('Static contracts only; fuel headroom, match completion and competitive gains are not established.')
