"""Integration/preservation contracts; semantic policy tests compile in bot-check."""
import json
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[2]
source = (root / 'bots/alpha/src/bot.cpp').read_text()
base = subprocess.check_output(['git', 'show', '1f5e71f3111c5a492a20f4aaf0bbd3bd0c6fff97:bots/alpha/src/bot.cpp'], cwd=root, text=True)
turn = source[source.index('void Bot::play_turn()'):]
checks = {
    'prism_only': 'if (me.passive() == cambc::passive_type::gem_focus)' in turn,
    'bank_gate': 'if (me.gem_count() > 0 && bank_bag)' in turn,
    'policy_after_channel_guard_before_shop': turn.find('prism_bank.update(') > turn.find('me.is_teleporting()') and 0 <= turn.find('prism_bank.update(') < turn.find('if (at_spawn)'),
    'death_commits_surviving_bag': 'prism_bank.commit();' in turn[turn.index('if (!me.is_alive())'):turn.index('// Leave channels')],
    'only_personal_enemy_vision': 'cambc::vision::champion_tiles(team::enemy).is_empty()' in turn,
    'pre_turn_logic_unchanged': source[source.index('using cambc::vec2;'):source.index('void Bot::play_turn()')] == base[base.index('using cambc::vec2;'):base.index('void Bot::play_turn()')],
    'bank_body_and_farming_unchanged': source[source.index('        // Capture resolves before this turn:'):] == base[base.index('        // Capture resolves before this turn:'):],
}
report = {'checks': checks, 'passed': all(checks.values()), 'scope': 'integration/source preservation, not runtime evidence'}
(root / 'experiments/alpha/task-ddd66f66-source-check.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report))
raise SystemExit(0 if report['passed'] else 1)
