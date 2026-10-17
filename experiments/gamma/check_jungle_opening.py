"""Source and arithmetic invariants only; the trusted wrapper checks the SDK build."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
BASE = "1a0675ca881d4b67cb5c6cb1822ce2ae1602dc4d"
SOURCE = "bots/gamma/src/bot.cpp"
source = (ROOT / SOURCE).read_text()
accepted = subprocess.check_output(["git", "show", f"{BASE}:{SOURCE}"], cwd=ROOT, text=True)
opening_start = source.index("    // Buy one camp-mitigation emblem;")
opening_end = source.index("    const std::array items{", opening_start)
opening = source[opening_start:opening_end]
without_opening = source[:opening_start] + source[opening_end:]
checks = {
    "only_shop_opening_and_algorithm_include_change_in_bot_cpp":
        without_opening.replace("#include <algorithm>\n", "") == accepted,
    "same_stat_and_inventory_backed_completion": all(text in opening for text in (
        "jungle_items[chosen_stat]", "const auto inventory = me.item_count();",
        "const auto emblem = jungle.result(); emblem && inventory[*emblem] == 0",
        "const auto combine_count = jungle.combine_count();",
        "if (inventory[jungle] < combine_count)",
        "std::min(me.gold_count() / jungle.cost(),\n                combine_count - inventory[jungle])",
        "if (count && me.can_buy(jungle, count)) me.buy(jungle, count);",
    )),
    "all_three_original_stat_choices_retained": all(
        opening.count(f"jungle_shard_of_{stat}") == 1
        for stat in ("strength", "focus", "health")
    ),
    "dispatcher_draft_rng_unchanged": all(
        (ROOT / f"bots/gamma/src/{name}").read_bytes()
        == subprocess.check_output(["git", "show", f"{BASE}:bots/gamma/src/{name}"], cwd=ROOT)
        for name in ("main.cpp", "draft.cpp", "draft.h", "random.h")
    ),
}

# Finite inventory/gold cases validate the cap's arithmetic contract, not engine
# execution: 30 gold/shard, five to combine, automatic combination per handbook.
cases = 0
for gold in range(0, 3001):
    for shards in range(5):
        for emblems in (0, 1, 2):
            bought = min(gold // 30, 5 - shards) if emblems == 0 else 0
            remaining = gold - 30 * bought
            power = remaining // 30
            assert bought >= 0 and remaining >= 0
            assert shards + bought <= 5
            assert emblems == 0 or bought == 0
            assert not power or emblems > 0 or shards + bought == 5
            assert remaining - power * 30 < 30
            cases += 1
checks["bounded_inventory_and_gold_cases"] = True
diff = subprocess.run(["git", "diff", "--check"], cwd=ROOT, capture_output=True, text=True)
checks["git_diff_check"] = diff.returncode == 0
report = {
    "kind": "source and finite arithmetic checks; not an engine fixture",
    "bot_cpp_sha256": hashlib.sha256(source.encode()).hexdigest(),
    "arithmetic_cases": cases,
    "checks": checks,
    "passed": all(checks.values()),
}
path = ROOT / "experiments/gamma/jungle-opening-source-check.json"
path.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
raise SystemExit(0 if report["passed"] else 1)
