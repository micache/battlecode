"""Source contracts only; trusted bot-check compiles constexpr behavior cases."""
import json
from pathlib import Path
import subprocess

root = Path('bots/alpha/src')
task = json.loads(Path('.agent/task.json').read_text())
bot = (root / 'bot.cpp').read_text()
header = (root / 'equipment_policy.h').read_text()
base_header = subprocess.check_output(['git', 'show', task['edit_commit']+':bots/alpha/src/equipment_policy.h']).decode()
base = subprocess.check_output(['git', 'show', task['edit_commit']+':bots/alpha/src/bot.cpp']).decode()
shop = bot.split('void Bot::buy_items()',1)[1].split('// Bound extra combat',1)[0]
checks = {
    'bundle_selector_integrated': 'equipment_policy::choose_jungle' in shop,
    'full_bundle_legality': 'me.can_buy(jungle[choice.stat], choice.count)' in shop,
    'all_stat_emblems_block_duplicate_passive': all('inventory[jungle_emblems['+str(i)+']]' in shop for i in range(3)),
    'refresh_power_budget_after_bundle': 'me.buy(jungle[choice.stat], choice.count)' in shop and 'inventory = me.item_count();' in shop and shop.rindex('inventory = me.item_count();') > shop.index('me.buy(jungle[choice.stat], choice.count)'),
    'original_model_and_power_allocator_byte_identical': header.split('// Jungle\'s documented',1)[0] == base_header.split('static_assert',1)[0],
    'non_shop_policy_byte_identical': bot.split('// Bound extra combat',1)[1] == base.split('// Bound extra combat',1)[1],
    'other_sources_unchanged': all(p.read_bytes() == subprocess.check_output(['git','show',task['edit_commit']+':'+str(p)]) for p in root.iterdir() if p.name not in ['bot.cpp','equipment_policy.h']),
}
report={'task_id':task['task_id'],'scope':'source contracts, not engine fixtures','checks':checks,'passed':all(checks.values())}
path=Path('experiments/alpha/task-3d6485a9-source-check.json')
path.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
raise SystemExit(0 if report['passed'] else 1)
