"""Static action-safety regressions; does not simulate the engine."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

root = Path(__file__).resolve().parents[2]
source = (root / "bots/gamma/src/bot.cpp").read_text()
helper = source.split("bool attack_if_in_range(", 1)[1].split("\n// Attack a camp", 1)[0]
farm = source.split("void farm_camps()", 1)[1].split("void Bot::play_turn()", 1)[0]
checks = {}

def check(name, condition):
    checks[name] = bool(condition)
    assert condition, name

check("visibility_before_initial_live_reads",
      helper.index("!target.is_visible()") < helper.index("target.health()")
      < helper.index("target.position()") < helper.index("me.attack(target)"))
post = helper.split("me.attack(target);", 1)[1]
check("post_attack_visibility_and_life_gate",
      post.index("before_movement && target.is_visible() && target.health() > 0")
      < post.index("ability.use(target)"))
check("readiness_and_restrictions_gate",
      "me.can_cast()" in post and "buff_restrictions::cast" in post
      and post.index("!ability.is_ready()") < post.index("ability.use(target)"))
check("only_unit_damage_with_category_and_range_checks",
      "!ability.is_damage()" in post and "std::is_same_v<Target, cambc::camp>" in post
      and "!ability.can_target_camps()" in post and "!ability.can_target_enemies()" in post
      and post.index("!ability.valid_tiles().is_set(target.position())")
      < post.index("ability.use(target)"))
check("bounded_attempt_after_basic",
      helper.count("me.attack(target);") == 1 and helper.count("ability.use(target);") == 1
      and "for (const auto& ability : me.abilities())" in helper
      and re.search(r"ability.use\(target\);\s*break;", post) is not None
      and "while" not in helper)
calls = re.findall(r"attack_if_in_range\((camp|enemy), (true|false)\)", source)
check("all_calls_accounted_for", calls == [("camp", "true"), ("camp", "false"), ("enemy", "true")])
check("movement_disables_casts",
      farm.index("attack_if_in_range(camp, true)") < farm.index("move_towards_closest(goals)")
      < farm.index("attack_if_in_range(camp, false)"))

base = subprocess.check_output([
    "git", "show", "1a0675ca881d4b67cb5c6cb1822ce2ae1602dc4d:bots/gamma/src/bot.cpp"
], cwd=root, text=True)
check("shop_navigation_and_turn_priorities_preserved",
      source.split("// Make one basic attack", 1)[0].replace("#include <type_traits>\n", "")
      == base.split("// Make one basic attack", 1)[0]
      and source.split("void Bot::play_turn()", 1)[1].replace("attack_if_in_range(enemy, true)", "attack_if_in_range(enemy)")
      == base.split("void Bot::play_turn()", 1)[1])
for name in ("main.cpp", "draft.cpp", "draft.h", "random.h", "bot.h"):
    accepted = subprocess.check_output([
        "git", "show", f"1a0675ca881d4b67cb5c6cb1822ce2ae1602dc4d:bots/gamma/src/{name}"
    ], cwd=root)
    check(f"unchanged_{name}", (root / f"bots/gamma/src/{name}").read_bytes() == accepted)
report = {"scope": "source invariants only; no engine/fuel simulation", "checks": checks,
          "bot_cpp_sha256": hashlib.sha256(source.encode()).hexdigest()}
path = root / "experiments/gamma/direct-damage-source-check.json"
path.write_text(json.dumps(report, indent=2) + "\n")
print(f"PASS: {len(checks)} source invariants; {path.relative_to(root)}")
