"""Source-level safety contracts for the integrated farming candidate; no engine mock."""
import hashlib
import json
from pathlib import Path
import re

root = Path('bots/alpha/src')
bot = (root / 'bot.cpp').read_text()
main = (root / 'main.cpp').read_text()
draft = (root / 'draft.cpp').read_text()
play = bot[bot.index('void Bot::play_turn()'):]
checks = {
    'deliberate_unique_complete_draft': len(set(re.findall(r'champion_draft::(\w+)', draft))) == 11
        and 'cambc::draft::team_size()' in draft and 'cambc::draft::pick(pick)' in draft,
    'channels_before_navigation': play.index('me.is_recalling()') < play.index('initialize()')
        < play.index('navigate(spawn)'),
    'capture_before_banking': play.index('collect_here()') < play.index('bank(true)'),
    'heal_through_spawn_turn_end': 'if (at_spawn && me.health() < me.max_health()) return;' in play,
    'only_free_navigation_goals': 'const auto free_goals = goals & ~blocked;' in bot
        and 'field.compute_to(blocked, free_goals' in bot,
    'bounded_hidden_obstruction_retry': 'attempt < 2' in bot,
    'movement_exclusivity_checked': 'return !walked || !std::visit' in bot
        and 'info.exclusive_with_movement' in bot and 'engage(true)' in bot,
    'visibility_before_live_queries': 'return target.is_visible() && target.health() > 0;' in bot
        and 'if (seen) {' in bot,
    'no_live_shared_memory_protocol': 'shared_memory' not in bot,
    'unreachable_goal_expires': 'plan.avoid_until = cambc::round_number() + 8;' in bot
        and 'if (now < plan.avoid_until) continue;' in bot,
    'official_yield_survives_exception': main.index('cambc::end_turn();') > main.index('catch (...)'),
    'fuel_observed_without_budget_override': 'cambc::fuel_remaining()' in main
        and 'planning_reserve' in bot,
}
report = {'kind': 'source_contracts_only', 'checks': checks,
          'files': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in root.iterdir() if p.is_file()},
          'passed': all(checks.values())}
out = Path('experiments/alpha/task-4133354c587642a699e191721aab2290-source-check.json')
out.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
raise SystemExit(0 if report['passed'] else 1)
