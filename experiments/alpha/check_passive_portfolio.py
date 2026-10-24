"""Integration/preservation contracts. Pure semantic cases compile in bot-check."""
import json
from pathlib import Path
import subprocess

root = Path('bots/alpha/src')
task = json.loads(Path('.agent/task.json').read_text())
base = lambda p: subprocess.check_output(['git','show',task['edit_commit']+':'+str(p)])
bot = (root/'bot.cpp').read_text()
old = base(root/'bot.cpp').decode()
shop = bot.split('void Bot::buy_items()',1)[1].split('// Bound extra combat',1)[0]
checks = {
    'portfolio_selector_integrated': 'equipment_portfolio::choose' in shop,
    'all_family_passives_checked': 'for (const auto emblem : family_emblems[family])' in shop,
    'full_bundle_legality_checked': 'me.can_buy(shard, choice.count)' in shop,
    'fresh_power_budget': 'me.gold_count() / cost' in shop and 'inventory = me.item_count();' in shop,
    'non_shop_behavior_preserved': bot.split('// Bound extra combat',1)[1] == old.split('// Bound extra combat',1)[1],
    'power_model_preserved': (root/'equipment_policy.h').read_bytes() == base(root/'equipment_policy.h'),
    'other_base_sources_preserved': all(p.read_bytes()==base(p) for p in root.iterdir() if p.name not in {'bot.cpp','equipment_portfolio.h'}),
}
report = {'task_id':task['task_id'],'scope':'source contracts, not runtime proof','checks':checks,'passed':all(checks.values())}
p = Path('experiments/alpha/task-2fce257a-source-check.json')
p.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
raise SystemExit(0 if report['passed'] else 1)
