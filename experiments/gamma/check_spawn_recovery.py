"""Source regression only: protect end-of-turn spawn healing before departure.

The official engine/build is checked separately by bot-check. This check also
requires the accepted source to fail, so it detects the original missing guard.
"""
import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[2]
BASE = "1a0675ca881d4b67cb5c6cb1822ce2ae1602dc4d"
SOURCE = "bots/gamma/src/bot.cpp"


def protects_recovery(source):
    # Strip comments so prose cannot satisfy the invariant. Require the yield
    # before every existing tactical branch, with shopping before the HP check.
    source = re.sub(r"//[^\n]*|/\*.*?\*/", "", source, flags=re.S)
    turn = source.split("void Bot::play_turn() {", 1)[1]
    wait = re.search(
        r"if\s*\(at_spawn\)\s*\{\s*buy_items\(\);\s*"
        r"if\s*\(me.health\(\)\s*<\s*me.max_health\(\)\)\s*return;\s*\}",
        turn,
    )
    if wait is None:
        return False
    # This deliberately checks the current simple control flow, not arbitrary
    # C++. A refactor requires review instead of silently passing this fixture.
    return (
        turn.index("!me.is_alive()") < wait.start()
        and turn.index("me.is_recalling()") < wait.start()
        and turn.index("me.is_submitting_gems()") < wait.start()
        and turn.index("me.is_teleporting()") < wait.start()
        and all(turn.index(action) > wait.end() for action in (
            "me.recall();", "attack_if_in_range(enemy)",
            "me.submit_gems(altar);", "move_towards_closest(goals);", "farm_camps();"
        ))
    )


current = (ROOT / SOURCE).read_text()
accepted = subprocess.check_output(
    ["git", "show", f"{BASE}:{SOURCE}"], cwd=ROOT, text=True
)
main = (ROOT / "bots/gamma/src/main.cpp").read_text()
checks = {
    "accepted_source_reproduces_missing_recovery_guard": not protects_recovery(accepted),
    "candidate_yields_before_tactical_actions_while_injured_on_spawn": protects_recovery(current),
    "official_dispatcher_still_yields": "cambc::end_turn();" in main,
}
report = {
    "kind": "source-level regression; not an engine scenario or match",
    "bot_cpp_sha256": hashlib.sha256(current.encode()).hexdigest(),
    "checks": checks,
    "passed": all(checks.values()),
}
path = ROOT / "experiments/gamma/spawn-recovery-source-check.json"
path.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
raise SystemExit(0 if report["passed"] else 1)
