"""Check purchase-policy boundaries; engine behavior is checked by bot-check."""
import json
from pathlib import Path
import subprocess

task = json.loads(Path('.agent/task.json').read_text())
src = Path('bots/alpha/src')
text = (src / 'bot.cpp').read_text()


def accepted(path):
    return subprocess.check_output(
        ['git', 'show', f"{task['accepted_commit']}:{path}"]
    ).decode()


before = accepted(src / 'bot.cpp')
start = text.index('    // Complete one Jungle emblem')
end = text.index('    const std::array items{', start)
purchase = text[start:end]
checks = {
    'only_purchase_policy_changed': (
        (text[:start] + text[end:]).replace('#include <algorithm>\n', '') == before
    ),
    'same_stat_order_as_power': all(
        purchase.index('jungle_shard_of_' + a)
        < purchase.index('jungle_shard_of_' + b)
        for a, b in [('strength', 'focus'), ('focus', 'health')]
    ),
    'skip_jungle_after_emblem':
        'if (info.result && inventory[*info.result] == 0) {' in purchase,
    'cap_purchase_at_emblem_completion': all(s in purchase for s in [
        'info.combine_count - inventory[jungle]',
        'std::min(me.gold_count() / info.cost, missing)',
        'if (!count || !me.can_buy(jungle, count)) return;',
        'me.buy(jungle, count);',
        'if (count < missing) return;',
    ]),
    'refresh_gold_for_power_after_jungle':
        'const unsigned count = me.gold_count() / item.cost();' in text[end:],
    'other_executable_source_unchanged': all(
        path.read_text() == accepted(path)
        for path in src.iterdir() if path.is_file() and path.name not in ['bot.cpp', 'bot.h']
    ),
    'header_only_comment_changed': (src / 'bot.h').read_text().replace(
        '// Buy one Jungle emblem, then Power shards of the randomly chosen stat.',
        '// Spend only on power shards of the randomly chosen stat.'
    ) == accepted(src / 'bot.h'),
    'official_yield_retained': 'cambc::end_turn();' in (src / 'main.cpp').read_text(),
}
report = {'task_id': task['task_id'], 'scope': 'source invariants, not runtime or fuel',
          'checks': checks, 'passed': all(checks.values())}
Path(f"experiments/alpha/{task['task_id']}-source-check.json").write_text(
    json.dumps(report, indent=2) + '\n'
)
print(json.dumps(report, indent=2))
assert report['passed']
