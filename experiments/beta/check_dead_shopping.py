"""Source invariant only: dead shopping must precede all live-state decisions."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "experiments/beta/task-a291761b3e4d4f59b5a9ae5abde282b8/accepted-src"


def strip_comments(source):
    return re.sub(r"//[^\n]*|/\*.*?\*/", "", source, flags=re.S)


def dead_shop_precedes_live_queries(source):
    turn = strip_comments(source).split("void Bot::play_turn() {", 1)[1]
    branch = re.search(r"if\s*\(!me\.is_alive\(\)\)\s*\{\s*buy_items\(\);\s*return;\s*\}", turn)
    if not branch:
        return False
    before = turn[:branch.start()]
    return not re.search(r"me\.(position|is_recalling|is_submitting_gems|is_teleporting|can_move|can_attack|health|gem_count)\(", before)


baseline = (BASE / "bot.cpp").read_text()
candidate = (ROOT / "bots/beta/src/bot.cpp").read_text()
assert not dead_shop_precedes_live_queries(baseline), "baseline unexpectedly supports dead shopping"
assert dead_shop_precedes_live_queries(candidate), "dead shopping must immediately return before live queries"
# The existing purchase permission/count guard must remain intact.
base_shop = baseline.split("void Bot::buy_items() {", 1)[1].split("\n}", 1)[0]
new_shop = candidate.split("void Bot::buy_items() {", 1)[1].split("\n}", 1)[0]
assert base_shop == new_shop
assert "if (count && me.can_buy(item, count)) me.buy(item, count);" in new_shop
main = (ROOT / "bots/beta/src/main.cpp").read_text()
assert main == (BASE / "main.cpp").read_text() and "cambc::end_turn();" in main
print("PASS: accepted baseline lacks dead shopping; candidate shops and returns before live queries.")
print("PASS: purchase count/permission guard and official turn-yield dispatch are unchanged.")
print("Source invariants only; engine behavior and strength require trusted checks/evaluation.")
