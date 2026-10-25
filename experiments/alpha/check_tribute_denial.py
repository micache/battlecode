"""Source integration invariants; runtime strength remains an arena question."""
from pathlib import Path
import re
src = Path('bots/alpha/src/bot.cpp').read_text()
header_path = Path('bots/alpha/src/tribute_denial.h')
assert header_path.exists(), 'missing tribute-denial policy'
h = header_path.read_text()
start = src.index('bool fight(bool walked = false)')
end = src.index('// Attack a camp already in range', start)
fight = src[start:end]
assert re.search(r'if constexpr \(std::is_same_v<Target, cambc::champion>\)\s*\{\s*if \(tribute_denial::attempt\(walked\)\) return true;', fight), 'champion-only successful denial must end fight'
assert fight.index('tribute_denial::attempt') < fight.index('basic_target<Target>'), 'denial must precede ordinary basic'
assert not re.search(r'\.(move|move_absolute|move_towards|recall|submit_gems)\(', h), 'denial must not move or start channels'
scan = h[h.index('for (const auto& enemy'):h.index('if (!target ||')]
assert scan.index('enemy.is_visible()') < scan.index('enemy.health()') < scan.index('enemy.gem_count()'), 'live state requires visibility'
assert 'enemy_limit = 6' in h and 'scan_fuel_reserve' in scan, 'bounded scan including twins'
assert 'stun_immunity' in scan and 'enemy.is_submitting_gems()' in scan, 'interruptible live channels only'
play = src[src.index('void Bot::play_turn()'):]
assert play.index('me.is_submitting_gems()') < play.index('fight<cambc::champion>()'), 'preserve own channels'
assert 'cambc::end_turn();' in Path('bots/alpha/src/main.cpp').read_text(), 'official yield retained'
print('PASS: denial integration, visibility, bounds, channels and yield invariants')
