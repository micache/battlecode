"""Source invariants for one-emblem shopping; no engine simulation."""
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
BASE = "0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9"


def accepted(path):
    return subprocess.check_output(["git", "show", f"{BASE}:{path}"], cwd=ROOT).decode()


def policy_holds(source):
    shop = source.split("void Bot::buy_items() {", 1)[1].split("\n}", 1)[0]
    shop = re.sub(r"//[^\n]*", "", shop)
    required = (
        "const auto jungle = jungle_items[chosen_stat];",
        "const auto inventory = me.item_count();",
        "const auto emblem = jungle.result();",
        "const auto required = jungle.combine_count();",
        "if (emblem && inventory[*emblem] == 0 && inventory[jungle] < required)",
        "std::min(me.gold_count() / jungle.cost(), required - inventory[jungle])",
        "if (count && me.can_buy(jungle, count)) me.buy(jungle, count);",
    )
    if not all(part in shop for part in required):
        return False
    for stat in ("strength", "focus", "health"):
        if f"cambc::item_type::jungle_shard_of_{stat}" not in shop:
            return False
    return shop.index("me.buy(jungle, count)") < shop.index("const std::array items{")


path = "bots/beta/src/bot.cpp"
source = (ROOT / path).read_text()
baseline = accepted(path)
assert not policy_holds(baseline)
assert policy_holds(source)

# No changes to Power shopping, its fresh gold query, or any field decisions.
prefix, remainder = source.split("    // Complete one Jungle emblem", 1)
_, suffix = remainder.split("    const std::array items{", 1)
restored = prefix + "    const std::array items{" + suffix
assert restored.replace("#include <algorithm>\n", "", 1) == baseline
for p in (ROOT / "bots/beta/src").iterdir():
    if p.name == "bot.cpp":
        continue
    text = p.read_text()
    if p.name == "bot.h":
        text = text.replace(
            "Complete one Jungle emblem, then buy Power shards of the chosen stat.",
            "Spend only on power shards of the randomly chosen stat.",
        )
    assert text == accepted(p.relative_to(ROOT).as_posix()), p

mutations = (
    ("inventory[*emblem] == 0", "inventory[*emblem] >= 0"),
    ("inventory[jungle] < required", "true"),
    ("required - inventory[jungle]", "required"),
    ("std::min(me.gold_count() / jungle.cost(), required - inventory[jungle])", "me.gold_count() / jungle.cost()"),
    ("if (count && me.can_buy(jungle, count))", "if (count)"),
    ("jungle_items[chosen_stat]", "jungle_items[0]"),
)
for before, after in mutations:
    assert before in source
    assert not policy_holds(source.replace(before, after, 1)), before

print("PASS: one Jungle emblem maximum, missing-shard/affordability cap, chosen stat and can_buy guard.")
print("PASS: fresh Power shopping and all field decisions/other source preserved against accepted.")
print("PASS: accepted baseline and six guard/cap/stat mutations rejected.")
print("Source checks only; auto-combination, runtime fuel and strategic benefit require trusted evidence.")
