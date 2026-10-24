"""Source integration contracts; semantic cases compile via trusted bot-check."""
import json, subprocess
from pathlib import Path
root=Path('bots/alpha/src')
task=json.loads(Path('.agent/task.json').read_text())
base=lambda p: subprocess.check_output(['git','show',task['edit_commit']+':'+str(p)])
bot=(root/'bot.cpp').read_text()
old=base(root/'bot.cpp').decode()
checks={
 'early_support': '    proactive_support();' in bot and bot.index('    proactive_support();') < bot.index('    // Retreat before recall'),
 'no_combat_support_gate': '// Use defensive kits when no damage/reset cast was chosen.' not in bot,
 'pure_policy_present': (root/'support_policy.h').exists(),
 'remaining_sources_preserved': all(p.read_bytes()==base(p) for p in root.iterdir() if p.name not in {'bot.cpp','support_policy.h'}),
 'draft_shop_and_navigation_preserved': bot.split('// Bound extra combat')[0].replace('#include "support_policy.h"\n','') == old.split('// Bound extra combat')[0],
}
# Ordinary combat comparison is made explicitly after removing the old fallback.
start='// Spend the separate basic'; end='// Attack a camp already in range'
a=bot.split(start,1)[1].split(end,1)[0]
b=old.split(start,1)[1].split(end,1)[0]
b=b.split('    // Use defensive kits',1)[0]+'    return acted;\n}\n\n'
checks['ordinary_combat_preserved']=a==b
report={'scope':'source contracts, not runtime proof','checks':checks,'passed':all(checks.values())}
Path('experiments/alpha/task-a5122d9c-source-check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2));raise SystemExit(0 if report['passed'] else 1)
