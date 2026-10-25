"""Source integration contracts; numerical cases compile in the trusted SDK build."""
from pathlib import Path

root = Path(__file__).resolve().parents[2]
source = (root / "bots/alpha/src/bot.cpp").read_text()
header = root / "bots/alpha/src/camp_pull.h"
assert header.exists(), "missing sleeping-camp pull assessment"
policy = header.read_text()
assert "group_limit = 6" in policy and "camp_limit = 32" in policy
assert "fuel_reserve = 55000" in policy
assert "vision::visible_tiles()" in policy and "vision::awake_camp_tiles()" in policy
assert "spawns & visible" in policy and "spawns & awake" in policy
assert "ally.is_visible()" in policy and "ally.is_alive()" in policy
assert "static_assert" in policy and "sustainable(" in policy
assert "shared_memory" not in policy and "recall(" not in policy
farm = source[source.index("void farm_camps()"):source.index("void Bot::play_turn()")]
assert farm.count("camp_pull::assess(goals)") == 2, "reassess after walking"
assert "goals &= ~excluded" in farm
assert "fight<cambc::camp>(false, &excluded)" in farm
assert "fight<cambc::camp>(true, &excluded)" in farm
assert "basic_target<Target>(excluded)" in source
assert "camp_pull::permits" in source
assert source.count("fight<cambc::champion>()") == 2, "unchanged PvP call sites"
turn = source[source.index("void Bot::play_turn()") :]
assert turn.index("me.is_recalling()") < turn.index("farm_camps()")
assert "cambc::end_turn();" in (root / "bots/alpha/src/main.cpp").read_text()
print("camp-pull source contracts passed; numeric contracts require bot-check")
