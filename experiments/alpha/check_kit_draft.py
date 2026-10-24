from pathlib import Path
import json
root = Path(__file__).resolve().parents[2]
draft = (root / "bots/alpha/src/draft.cpp").read_text()
assert "draft_policy::select" in draft, "draft still chooses a uniformly random pick"
assert "champion_designs" in draft, "draft must read immutable physical designs"
assert "team_size()" in draft, "draft must respect map pick count"
assert "heart_of_ruin" in draft, "released roster must include Heart of Ruin"
assert "cassi_and_issac" in draft and "champion_type::issac" in draft
policy = (root / "bots/alpha/src/draft_policy.h").read_text()
assert "static_assert" in policy and "equipment_policy::plan" in policy
bot = (root / "bots/alpha/src/bot.cpp").read_text()
assert "equipment_model::estimate" in bot and "equipment_model::estimate" in draft
assert "cambc::end_turn();" in (root / "bots/alpha/src/main.cpp").read_text()
print(json.dumps({"status": "PASSED", "scope": "source integration; pure semantics compiled by bot-check"}))
