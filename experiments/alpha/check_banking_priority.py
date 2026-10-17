"""Source invariants only; runtime legality and performance need trusted checks."""
import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--report", required=True)
args = parser.parse_args()
source = Path("bots/alpha/src/bot.cpp").read_text()
turn = source.split("void Bot::play_turn() {", 1)[1]
bank = turn.index("if (me.gem_count() > 0)")
fight = turn.index("for (const auto& enemy : cambc::vision::champions(team::enemy))")
farm = turn.index("farm_camps();")
checks = {
    "active_channels_preserved_before_banking":
        turn.index("me.is_submitting_gems()") < bank,
    "recall_precedes_banking": turn.index("me.recall();") < bank,
    "banking_precedes_enemy_target_selection": bank < fight < farm,
    "successful_bank_movement_returns":
        "if (move_towards_closest(goals))\n            return;" in turn[bank:fight],
    "failed_bank_route_can_fall_through_to_combat":
        turn[bank:fight].split("if (move_towards_closest(goals))", 1)[1]
        .split("//", 1)[0].strip() == "return;\n    }",
    "carrier_guard_prevents_farming_after_failed_route":
        "if (me.gem_count() > 0)\n        return;" in turn[fight:farm],
    "tribute_keeps_range_and_lock_checks":
        "distance(me.position(), altar) <= cambc::constants::submit_gems_range"
        in turn[bank:fight] and "!cambc::vision::has_altar_lock(altar)" in turn[bank:fight],
    "dispatcher_still_yields":
        "cambc::end_turn();" in Path("bots/alpha/src/main.cpp").read_text(),
}
report = {"checks": checks, "passed": all(checks.values()),
          "limits": "Source ordering and guard checks; no simulated game or fuel measurement."}
Path(args.report).write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report))
raise SystemExit(0 if report["passed"] else 1)
