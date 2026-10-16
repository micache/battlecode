"""Source invariants only; compilation and runtime checks belong to bot-check."""
from pathlib import Path
import json

TASK = 'task-1dc3b256a0de46648114a0975812d515'
source = Path('bots/alpha/src')
def base_file(name):
    return Path(f'experiments/alpha/{TASK}-accepted-{name}')
text = (source / 'bot.cpp').read_text()
start = text.index('// Spend at most one ready reset')
end = text.index('// Attack a camp already in range', start)
helper = text[start:end]
checks = {}
checks['first_attack_required'] = 'if (!attack_if_in_range(camp))\n        return false;' in helper
checks['live_survivor_and_cast_guard'] = 'camp.is_visible() && camp.health() > 0 && me.can_cast()' in helper
checks['public_ability_accessor'] = 'me.abilities()' in helper and '.ability_slots' not in text
checks['only_ready_reset'] = 'if (ability.is_attack_reset() && ability.is_ready())' in helper
checks['bounded_single_cast'] = helper.count('ability.use()') == 1 and 'break;' in helper and 'while' not in helper
checks['followup_uses_fresh_legality'] = 'if (ability.use())\n                    attack_if_in_range(camp);' in helper
checks['both_farming_sites'] = text.count('if (attack_camp_with_reset(camp))') == 2
restored = (text[:start] + text[end:]).replace('if (attack_camp_with_reset(camp))', 'if (attack_if_in_range(camp))')
checks['only_intended_delta_from_accepted'] = restored == base_file('bot.cpp').read_text()
checks['other_source_unchanged_from_accepted'] = all(p.read_bytes() == base_file(p.name).read_bytes() for p in source.iterdir() if p.name != 'bot.cpp')
checks['yield_retained'] = 'cambc::end_turn();' in (source / 'main.cpp').read_text()
report = {'task_id': TASK, 'scope': 'source invariants, not runtime execution', 'checks': checks, 'passed': all(checks.values())}
Path(f'experiments/alpha/{TASK}-source-check.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
assert report['passed']
