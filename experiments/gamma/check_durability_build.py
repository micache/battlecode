"""Guard the bounded survival investment and isolate it from other policies.

Source contracts only; bot-check supplies compilation and engine smoke evidence.
"""
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
BASE = "1b34f42a5266051ee50bae4cf74197b99b1115cb"
PATH = "bots/gamma/src/bot.cpp"
current = (ROOT / PATH).read_text()
base = subprocess.check_output(["git", "show", f"{BASE}:{PATH}"], cwd=ROOT, text=True)


def code(text):
    return re.sub(r"//[^\n]*|/\*.*?\*/", "", text, flags=re.S)


shop = code(current).split("void Bot::buy_items() {", 1)[1].split("void Bot::farm_camps()", 1)[0]
pairs = re.findall(r"std::pair\{I::(\w+),\s*I::(\w+)\}", shop)
added = r",\s*std::pair\{I::durability_shard_of_health,\s*I::durability_emblem_of_health\}"
checks = {
    "one_survival_emblem_after_farming_core": pairs == [
        ("jungle_shard_of_strength", "jungle_emblem_of_strength"),
        ("monster_shard_of_strength", "monster_emblem_of_strength"),
        ("durability_shard_of_health", "durability_emblem_of_health"),
    ],
    "completed_emblem_skips_family": "if (counts[pair.second]) continue;" in shop,
    "partial_purchase_bounded_by_remaining_shards_and_gold": (
        "pair.first.combine_count() - counts[pair.first]" in shop
        and "std::min(need, me.gold_count() / pair.first.cost())" in shop
    ),
    "purchase_requires_nonzero_count_and_current_shop_permission": (
        "if (count && me.can_buy(pair.first, count)) me.buy(pair.first, count);" in shop
    ),
    "actual_completion_gates_later_families": (
        "if (!me.item_count()[pair.second]) return;" in shop
    ),
    "unbounded_scaling_returns_to_power_strength": (
        "const auto item = I::power_shard_of_strength;" in shop
    ),
    "only_executable_change_is_survival_stage": (
        re.sub(added, "", code(current)).split() == code(base).split()
    ),
}
for name in ("bot.h", "main.cpp", "draft.cpp", "draft.h", "random.h"):
    path = f"bots/gamma/src/{name}"
    checks[f"{name}_matches_edit_base"] = (ROOT / path).read_bytes() == subprocess.check_output(
        ["git", "show", f"{BASE}:{path}"], cwd=ROOT
    )
report = {
    "kind": "source invariants; no runtime purchase or strategic gain claim",
    "edit_commit": BASE,
    "bot_cpp_sha256": hashlib.sha256(current.encode()).hexdigest(),
    "checks": checks,
    "passed": all(checks.values()),
}
path = ROOT / "experiments/gamma/durability-build-source-check.json"
path.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
raise SystemExit(0 if report["passed"] else 1)
