"""Scope and target-isolation regressions; does not simulate engine actions."""
import json
from pathlib import Path
import subprocess

TASK = "task-844841b0ef694b819a6ab2fcf1a89387"
EDIT = "5f73d0787014e3f712d0eb6234f088fee489b4d8"
ROOT = Path("bots/alpha/src")


def original(name):
    return subprocess.check_output(
        ["git", "show", f"{EDIT}:bots/alpha/src/{name}"], text=True
    )


source = (ROOT / "bot.cpp").read_text()
base = original("bot.cpp")
start = "template<class Target>\nstd::optional<Target> basic_target"
combat = source[source.index(start):source.index("// Route choice")]
combat = combat.replace(
    "const cambc::bitboard* camp_spawns = nullptr", ""
).replace(
    "bool walked = false, )", "bool walked = false)"
).replace("(camp_spawns)", "()")
checks = {
    "entire_play_turn_unchanged": source[source.index("void Bot::play_turn()"):] ==
        base[base.index("void Bot::play_turn()"):],
    "navigation_and_items_unchanged": source[:source.index("template<class Target>")] ==
        base[:base.index("template<class Target>")],
    "combat_policy_unchanged_except_group_filter": combat ==
        base[base.index(start):base.index("// Attack a camp already in range")],
    "select_before_camp_combat": source.index("memory().plan(blocked_tiles())") <
        source.index("fight<cambc::camp>(false, focus)"),
    "fresh_camp_handles_filtered_by_spawn_identity":
        "auto targets = cambc::vision::camps();" in source and
        "!camp_spawns->is_set(camp.spawn_position())" in source,
    "basic_spell_reset_queries_all_filtered":
        source.count("combat_targets<Target>(camp_spawns)") == 3 and
        source.count("basic_target<Target>(camp_spawns)") == 2,
    "fresh_postmove_combat_and_walk_exclusion":
        "fight<cambc::camp>(cambc::self().position() != before, focus)" in source,
}
for name in ["bot.h", "main.cpp", "draft.cpp", "draft.h", "random.h", "altar_control.h"]:
    checks[name + "_unchanged"] = (ROOT / name).read_text() == original(name)

report = {"task_id": TASK, "edit_commit": EDIT, "checks": checks,
          "limitations": "Source invariants, not engine branch coverage or strength evidence."}
path = Path("experiments/alpha") / (TASK + "-source-check.json")
path.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(checks, indent=2))
assert all(checks.values())
