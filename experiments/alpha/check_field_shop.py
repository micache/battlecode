"""Source integration contracts; semantic allocator cases compile in bot-check."""
import json
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[2]
source = (root / 'bots/alpha/src/bot.cpp').read_text()
header = (root / 'bots/alpha/src/equipment_policy.h').read_text()
base = subprocess.check_output([
    'git', 'show', '1f5e71f3111c5a492a20f4aaf0bbd3bd0c6fff97:bots/alpha/src/bot.cpp'
], cwd=root, text=True)
turn = source[source.index('void Bot::play_turn()'):]
field = turn.find('buy_items(false);')
checks = {
    'field_shop_after_channel_and_death_guards': field > turn.find('if (at_spawn)') > turn.find('me.is_recalling()') > turn.find('if (!me.is_alive())'),
    'field_shop_requires_remote_permission': 'else if (me.passive() == cambc::passive_type::remote_shop)' in turn,
    'field_health_excluded': 'if (!allow_health && stat == 2) continue;' in header,
    'spawn_default_health_retained': 'bool allow_health = true' in header,
    'nonshop_combat_navigation_preserved': source[source.index('// Bound extra combat work;'):source.index('void Bot::play_turn()')] == base[base.index('// Bound extra combat work;'):base.index('void Bot::play_turn()')],
    'bank_farm_recovery_preserved': source[source.index('    altar_control::place_lock();', source.index('void Bot::play_turn()')):] == base[base.index('    altar_control::place_lock();', base.index('void Bot::play_turn()')):],
}
report = {'checks': checks, 'passed': all(checks.values()), 'scope': 'source contracts, not runtime proof'}
(root / 'experiments/alpha/task-4a9b803a-source-check.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report))
raise SystemExit(0 if report['passed'] else 1)
