"""Source invariant for carrier banking priority; not an engine simulation."""
import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[2]
SOURCE = "bots/gamma/src/bot.cpp"
BASE = "1a0675ca881d4b67cb5c6cb1822ce2ae1602dc4d"


def turn_body(source):
    source = re.sub(r"//[^\n]*|/\*.*?\*/", "", source, flags=re.S)
    return source.split("void Bot::play_turn() {", 1)[1]


def bank_block(turn):
    start = turn.index("if (me.gem_count() > 0) {")
    opening = turn.index("{", start)
    depth = 1
    end = opening + 1
    while depth:
        depth += (turn[end] == "{") - (turn[end] == "}")
        end += 1
    return start, end, turn[opening + 1:end - 1]


current = (ROOT / SOURCE).read_text()
accepted = subprocess.check_output(
    ["git", "show", f"{BASE}:{SOURCE}"], cwd=ROOT, text=True
)
turn, old = turn_body(current), turn_body(accepted)
start, end, bank = bank_block(turn)
old_start, _, old_bank = bank_block(old)
combat = "for (const auto& enemy : cambc::vision::champions(team::enemy))"
checks = {
    "accepted_source_reproduces_combat_before_carrier_bank": old.index(combat) < old_start,
    "carrier_bank_precedes_enemy_scan_and_farming": end < turn.index(combat) < turn.index("farm_camps();"),
    "carrier_bank_returns_without_falling_into_combat": bank.rstrip().endswith("return;"),
    "submission_and_route_logic_preserved": bank == old_bank,
    "channel_guards_and_recall_still_precede_banking": all(
        turn.index(guard) < start for guard in (
            "!me.is_alive()", "me.is_recalling()", "me.is_submitting_gems()",
            "me.is_teleporting()", "me.recall();",
        )
    ),
    "official_dispatcher_still_yields": "cambc::end_turn();" in (ROOT / "bots/gamma/src/main.cpp").read_text(),
}
report = {
    "kind": "source invariant only; no runtime safety or strategic result inferred",
    "bot_cpp_sha256": hashlib.sha256(current.encode()).hexdigest(),
    "checks": checks,
    "passed": all(checks.values()),
}
path = ROOT / "experiments/gamma/banking-priority-source-check.json"
path.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
raise SystemExit(0 if report["passed"] else 1)
