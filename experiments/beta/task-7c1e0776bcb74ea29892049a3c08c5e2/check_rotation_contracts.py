"""Source integration contracts; temporal policy assertions compile in bot-check.

These do not simulate engine actions, establish fuel headroom or measure wins.
"""
from pathlib import Path

source = Path('bots/beta/src/bot.cpp').read_text()


def valid(s):
    farm = s.split('void Bot::farm_camps() {', 1)[1].split('void Bot::play_turn()', 1)[0]
    gather = farm.split('std::partial_sort', 1)[0]
    assert 'std::vector<std::size_t> order;' in gather
    assert 'if (camp_rotation::eligible(round, g.retry_round, g.cooldown)) order.push_back(i);' in gather
    # Capture on our visible tile must survive even an old retry/cooldown record.
    own = gather.split('if (g.spawns.is_set(position)) {', 1)[1]
    assert own.index('g.group.state()') < own.index('camp_group_reward_available')
    capture = own.split('camp_group_reward_available', 1)[1].split('if (const auto* respawn', 1)[0]
    assert 'g.cooldown.clear();' in capture and 'return;' in capture
    assert own.index('return;') < own.index('camp_rotation::eligible')
    # Other live state is queried only after current visibility is established.
    scan = farm.split('for (std::size_t n = 0;', 1)[1]
    assert 'if (seen) {\n            const auto state = g.group.state();' in scan
    assert 'g.cooldown.record(round, respawn->timer);' in scan
    assert 'g.cooldown.clear();' in scan
    assert 'const auto checked = std::min(max_group_checks, order.size());' in farm
    assert 'if (n > 0 && cambc::fuel_remaining() < scan_reserve) break;' in farm
    # Vacating is only a no-work fallback and never supplies this group's tiles.
    fallback = farm.split('if (chosen < 0) {', 1)[1].split('target_group = chosen;', 1)[0]
    assert 'occupied_cooldown >= 0 && cambc::fuel_remaining() >= planning_reserve' in fallback
    assert 'move_to(around(position, 1) & ~groups[occupied_cooldown].spawns);' in fallback
    assert fallback.index('move_to(') < fallback.index('return;')


valid(source)
mutations = [
    ('if (camp_rotation::eligible(round, g.retry_round, g.cooldown)) order.push_back(i);', 'order.push_back(i);'),
    ('if (g.spawns.is_set(position)) {', 'if (true) {'),
    ('if (seen) {\n            const auto state', 'if (true) {\n            const auto state'),
    ('g.cooldown.record(round, respawn->timer);', 'g.cooldown.clear();'),
    ('& ~groups[occupied_cooldown].spawns', '| groups[occupied_cooldown].spawns'),
]
for old, new in mutations:
    assert old in source
    try:
        valid(source.replace(old, new))
    except (AssertionError, IndexError, ValueError):
        continue
    raise AssertionError('unsafe mutation accepted: ' + old)
print('PASS: eligibility precedes shortlist; capture overrides cached deferral; '
      'observations require visibility; scan and vacate bounds retained; '
      'five unsafe mutations rejected. Source contracts only.')
