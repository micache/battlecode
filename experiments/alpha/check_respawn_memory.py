"""Source safety checks; temporal C++ contracts compile through bot-check."""
import hashlib
import json
from pathlib import Path
import subprocess

task = json.loads(Path('.agent/task.json').read_text())
root = Path('bots/alpha/src')
source = (root / 'bot.cpp').read_text()
header = (root / 'camp_rotation.h').read_text()
base = subprocess.check_output(
    ['git', 'show', f"{task['edit_commit']}:{root}/bot.cpp"], text=True)
marker = "// Attack a camp already in range, otherwise move toward the nearest camp tiles."
end = 'void Bot::play_turn()'
restored = source.replace('#include "camp_rotation.h"\n', '')
restored = (restored[:restored.index(marker)]
            + base[base.index(marker):base.index(end)]
            + restored[restored.index(end):])
restored = restored.replace('''        // Capture resolves before this turn: remember the newly cooling group
        // before leaving it with the reward. No movement or channel is started.
        camp_rotation::memory().observe();
''', '')
observe = header[header.index('    void observe()'):header.index('    cambc::bitboard goals()')]
checks = {
    'other_policy_matches_edit_base': restored == base,
    'other_source_files_match_edit_base': all(
        p.read_bytes() == subprocess.check_output(
            ['git', 'show', f"{task['edit_commit']}:{p}"])
        for p in root.iterdir()
        if p.is_file() and p.name not in ('bot.cpp', 'camp_rotation.h')),
    'current_visibility_precedes_live_state': observe.index('entry.spawns & visible')
        < observe.index('entry.group.state()'),
    'channels_preserved_before_new_bank_observation': source.index('if (me.is_recalling()')
        < source.index('camp_rotation::memory().observe()'),
    'fresh_nonrespawn_observation_invalidates_old_cooldown':
        'else\n                entry.cooldown.clear();' in observe,
    'bounded_observation_work': 'queried >= observation_limit' in observe
        and 'fuel_remaining() < observation_fuel_reserve' in observe,
    'no_new_live_team_memory': 'shared_memory' not in header,
    'temporal_contracts_in_trusted_build': 'static_assert([]' in header,
    'official_yield_preserved': (root / 'main.cpp').read_text().index('cambc::end_turn();')
        > (root / 'main.cpp').read_text().index('catch (...)'),
}
report = {
    'task_id': task['task_id'],
    'scope': 'Source invariants; C++ temporal static_assert requires bot-check. No game-strength or fuel claim.',
    'checks': checks,
    'passed': all(checks.values()),
    'source_files': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                     for p in sorted(root.iterdir()) if p.is_file()},
}
path = Path(f"experiments/alpha/{task['task_id']}-source-check.json")
path.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
raise SystemExit(0 if report['passed'] else 1)
