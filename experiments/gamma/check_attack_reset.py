"""Source safety invariants only; bot-check supplies the real SDK/build/smoke.

This is deliberately limited to the current simple helper, not a C++ parser.
Refactoring its control flow requires review of these assertions.
"""
import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[2]
SOURCE = "bots/gamma/src/bot.cpp"
BASE = "1a0675ca881d4b67cb5c6cb1822ce2ae1602dc4d"
current = (ROOT / SOURCE).read_text()
accepted = subprocess.check_output(
    ["git", "show", f"{BASE}:{SOURCE}"], cwd=ROOT, text=True
)
code = re.sub(r"//[^\n]*|/\*.*?\*/", "", current, flags=re.S)
helper = code.split("bool attack_if_in_range(const Target& target) {", 1)[1]
helper = helper.split("void farm_camps()", 1)[0]
after_first = helper.split("me.attack(target);", 1)[1]
before_cast, after_cast = after_first.split("ability.use()", 1)
checks = {
    "accepted_source_has_no_attack_reset_policy": "ability.use()" not in accepted,
    "initial_attack_checks_allowance_visibility_health_range": bool(re.search(
        r"if \(!me.can_attack\(\) \|\| !target.is_visible\(\) \|\| target.health\(\) <= 0"
        r"\s*\|\| !me.attack_tiles\(\).is_set\(target.position\(\)\)\)"
        r"\s*\{\s*return false;\s*\}\s*me.attack\(target\);", helper
    )),
    "no_reset_for_dead_or_hidden_target": bool(re.search(
        r"if \(!target.is_visible\(\) \|\| target.health\(\) <= 0\)\s*return true;",
        before_cast,
    )),
    "only_ready_self_targeted_attack_resets": bool(re.search(
        r"if \(!ability.is_attack_reset\(\) \|\| !ability.can_target_self\(\)"
        r" \|\| !ability.is_ready\(\)\)\s*continue;", before_cast
    )),
    "followup_rechecks_allowance_visibility_health_range": bool(re.search(
        r" && me.can_attack\(\) && target.is_visible\(\) && target.health\(\) > 0"
        r"\s*&& me.attack_tiles\(\).is_set\(target.position\(\)\)\)"
        r"\s*me.attack\(target\);\s*break;", after_cast
    )),
    "bounded_two_attacks_one_cast_attempt": (
        helper.count("me.attack(target);") == 2
        and helper.count("ability.use()") == 1
        and helper.count("for (") == 1
        and "while" not in helper and "attack_if_in_range(" not in helper
    ),
    "official_dispatcher_yields": "cambc::end_turn();" in (
        ROOT / "bots/gamma/src/main.cpp"
    ).read_text(),
}
report = {
    "kind": "source safety invariants; not runtime combat or match evidence",
    "bot_cpp_sha256": hashlib.sha256(current.encode()).hexdigest(),
    "checks": checks,
    "passed": all(checks.values()),
}
path = ROOT / "experiments/gamma/attack-reset-source-check.json"
path.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
raise SystemExit(0 if report["passed"] else 1)
