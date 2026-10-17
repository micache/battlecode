"""Check banking control-flow invariants; not a runtime engine fixture."""
import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[2]
BASE = "1a0675ca881d4b67cb5c6cb1822ce2ae1602dc4d"
SOURCE = "bots/gamma/src/bot.cpp"


def accepted(path):
    return subprocess.check_output(
        ["git", "show", f"{BASE}:{path}"], cwd=ROOT, text=True
    )


def strip_comments(source):
    return re.sub(r"//[^\n]*|/\*.*?\*/", "", source, flags=re.S)


def braced_body(source, opening):
    depth, end = 1, opening + 1
    while depth:
        depth += (source[end] == "{") - (source[end] == "}")
        end += 1
    return source[opening + 1:end - 1], end


current = (ROOT / SOURCE).read_text()
old = accepted(SOURCE)
bank_start = current.index("if (me.gem_count() > 0) {")
move = current.index("if (move_towards_closest(goals)) {", bank_start)
arrival, end = braced_body(current, current.index("{", move))
clean = strip_comments(arrival)
submission = clean.index("me.submit_gems(altar);")
checks = {
    "accepted_reproduces_move_then_unconditional_return":
        "move_towards_closest(goals);\n        return;" in old[old.index("if (me.gem_count() > 0) {"):],
    "arrival_reads_current_position_and_lock_before_submission":
        0 <= clean.index("distance(me.position(), altar)") < submission
        and 0 <= clean.index("!cambc::vision::has_altar_lock(altar)") < submission
        and "<= cambc::constants::submit_gems_range" in clean,
    "one_submission_then_return_per_successful_move":
        clean.count("me.submit_gems(altar);") == 1
        and re.search(r"me\.submit_gems\(altar\);\s*return;", clean) is not None,
    "failed_or_nonqualifying_arrival_returns_without_more_actions":
        current[end:].lstrip().startswith("return;"),
    "only_banking_arrival_changed":
        re.sub(r"\s+", "", strip_comments(
            current[:move] + "move_towards_closest(goals);" + current[end:]))
        == re.sub(r"\s+", "", strip_comments(old)),
    "other_source_files_and_official_yield_preserved": all(
        path.read_text() == accepted(str(path.relative_to(ROOT)))
        for path in (ROOT / "bots/gamma/src").iterdir()
        if path.name != "bot.cpp"
    ) and "cambc::end_turn();" in (ROOT / "bots/gamma/src/main.cpp").read_text(),
}
report = {
    "kind": "source invariants only; no runtime legality, fuel or strategic result inferred",
    "bot_cpp_sha256": hashlib.sha256(current.encode()).hexdigest(),
    "checks": checks,
    "passed": all(checks.values()),
}
(ROOT / "experiments/gamma/tribute-arrival-source-check.json").write_text(
    json.dumps(report, indent=2) + "\n"
)
print(json.dumps(report, indent=2))
raise SystemExit(0 if report["passed"] else 1)
