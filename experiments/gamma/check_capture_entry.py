"""Capture-entry safety/source isolation checks; not an engine simulation."""
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = "ecbc8203fd2ef0696ef7784c8b39528bb182ad7b"
source = (ROOT / "bots/gamma/src/bot.cpp").read_text()
base = subprocess.check_output(
    ["git", "show", f"{BASE}:bots/gamma/src/bot.cpp"], cwd=ROOT, text=True
)
combat = source[source.index("bool fight("):source.index("bool threatened()")]
entry = source[source.index("if (acted) {", source.index("void Bot::farm_camps()")):
               source.index("const auto fresh_visible", source.index("return; // One attempt;"))]

checks = {
    "cast_failure_does_not_record_exclusion": bool(re.search(
        r"if \(!ability.use\(args\.\.\.\)\) return false;\s*if \(excluded_walk\)", combat)),
    "all_four_spell_paths_record_successful_exclusive_casts":
        combat.count(".use(") == 1 and combat.count("cast(a") == 4
        and "*excluded_walk |= std::visit" in combat
        and "return info.exclusive_with_movement;" in combat,
    "fresh_movement_allowance_restrictions_and_fuel_guard": all(s in entry for s in [
        "excluded_walk || !me.can_move()", "buff_restrictions::move",
        "cambc::fuel_remaining() < PLAN_FUEL", "f.spawns.is_set(me.position())"]),
    "visible_authoritative_reward_state_before_entry":
        entry.index("(f.spawns & fresh_visible).is_empty()")
        < entry.index("f.group.state()") < entry.index("me.move_absolute(entry)"),
    "collector_and_fresh_occupancy_guards":
        "f.spawns & cambc::vision::champion_tiles(team::ally)" in entry
        and "const auto blocked = blocked_tiles();" in entry
        and "f.spawns & fresh_visible & local & ~blocked" in entry,
    "local_only_one_attempt_no_search_or_followup_combat":
        entry.count("me.move_absolute(entry)") == 1
        and "return; // One attempt;" in entry
        and "distance_field" not in entry and "act_on_group(" not in entry,
    "bounded_private_logging": "capture_entries_logged < 3" in entry,
    "shop_defense_banking_recovery_and_noncombat_movement_unchanged": all(
        source[source.index(start):source.index(end)] == base[base.index(start):base.index(end)]
        for start, end in [
            ("void lock_nearby_altar()", "// Visibility is checked"),
            ("bool threatened()", "void Bot::farm_camps()"),
        ]
    ) and source[source.index("void Bot::play_turn()"):]
        == base[base.index("void Bot::play_turn()"):],
    "draft_main_and_yield_unchanged": all(
        path.read_bytes() == subprocess.check_output(
            ["git", "show", f"{BASE}:{path.relative_to(ROOT)}"], cwd=ROOT)
        for path in (ROOT / "bots/gamma/src").iterdir()
        if path.name not in ["bot.cpp", "bot.h"]
    ),
}
report = {
    "kind": "source safety invariants, not runtime or performance evidence",
    "source_sha256": hashlib.sha256(source.encode()).hexdigest(),
    "checks": checks,
    "passed": all(checks.values()),
}
(ROOT / "experiments/gamma/capture-entry-source-check.json").write_text(
    json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
raise SystemExit(0 if report["passed"] else 1)
