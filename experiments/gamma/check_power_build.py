"""Check the no-Focus spending invariant for the current basic-attack policy."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
PATH = "bots/gamma/src/bot.cpp"
BASE = "1a0675ca881d4b67cb5c6cb1822ce2ae1602dc4d"
current = (ROOT / PATH).read_text()
accepted = subprocess.check_output(
    ["git", "show", f"{BASE}:{PATH}"], cwd=ROOT, text=True
)


def code(text):
    return re.sub(r"//[^\n]*|/\*.*?\*/", "", text, flags=re.S)


def choices(text):
    shop = code(text).split("void Bot::buy_items() {", 1)[1].split("}\n", 1)[0]
    return re.findall(r"cambc::item_type::(\w+)", shop)


old, new = choices(accepted), choices(current)
strength, focus, health = (
    "power_shard_of_strength", "power_shard_of_focus", "power_shard_of_health"
)
checks = {
    "accepted_reproduces_focus_spending": old == [strength, focus, health],
    "every_build_buys_a_used_stat": len(new) == 3 and set(new) <= {strength, health},
    "existing_damage_and_survival_choices_preserved": new[0] == old[0] and new[2] == old[2],
    "only_unused_focus_choice_redirected_to_strength": new[1] == strength,
    "policy_has_no_focus_scaled_cast": not re.search(r"\bcast\w*\s*\(", code(current)),
    "no_other_executable_changes_including_rng_and_buy_guards": (
        code(accepted).replace(f"cambc::item_type::{focus}", f"cambc::item_type::{strength}").split()
        == code(current).split()
    ),
}
for name in ("bot.h", "main.cpp", "draft.cpp", "draft.h", "random.h"):
    path = f"bots/gamma/src/{name}"
    checks[f"{name}_preserved"] = (ROOT / path).read_bytes() == subprocess.check_output(
        ["git", "show", f"{BASE}:{path}"], cwd=ROOT
    )
report = {
    "kind": "source invariants only; no engine behavior or strategic gain inferred",
    "bot_cpp_sha256": hashlib.sha256(current.encode()).hexdigest(),
    "checks": checks,
    "passed": all(checks.values()),
}
path = ROOT / "experiments/gamma/power-build-source-check.json"
path.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
raise SystemExit(0 if report["passed"] else 1)
