"""Source contracts; execution and strategic value require trusted checks."""
from pathlib import Path
p = Path('bots/beta/src/bot.cpp').read_text()
h = Path('bots/beta/src/bot.h').read_text()
assert 'rank_cursor' in h and 'policy::ranking_batch' in p, 'cheap ranking must also be bounded'
assert 'plan_order.resize(groups.size())' not in p, 'do not rebuild a whole-map ranking'
assert 'scan_cursor' in h, 'frontier coverage must persist across turns'
farm = p.split('void Bot::farm_camps() {', 1)[1].split('void Bot::play_turn()', 1)[0]
assert 'travel.compute(' not in farm, 'ranking must not require a full terrain search'
assert 'scan_complete' in farm and 'if (!scan_complete)' in farm, 'exhausted scans must preserve intent'
assert 'policy::frontier_batch' in farm, 'candidate inspection must be bounded'
scan = farm.split('for (std::size_t n = 0; n < checked; ++n) {', 1)[1]
assert scan.index('fuel_remaining() < scan_reserve') < scan.index('scan_cursor ='), 'deferral must not consume a queued frontier'
assert farm.index('order.push_back(cursor)') < farm.index('order.push_back(plan_order[k])'), 'local candidates must not starve rotation'
assert 'group_seen(g.group, visible)' in farm, 'group lifecycle reads require fresh visibility'
assert 'const bool committed = target_group >= 0' in farm
assert 'diagnostic("farm")' in p, 'bounded stage evidence needed for nonprogress diagnosis'
assert 'shared_memory.write' not in p, 'this experiment has no live memory protocol'
print('PASS: persistent bounded frontier, no full ranking field, scan deferral, visibility gate, private state.')
