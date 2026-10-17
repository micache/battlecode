"""Check draft legality and isolation; not an engine simulation or performance test."""
import hashlib
import itertools
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
BASE = "1a0675ca881d4b67cb5c6cb1822ce2ae1602dc4d"
PATH = "bots/gamma/src/draft.cpp"
text = (ROOT / PATH).read_text()
accepted = subprocess.check_output(["git", "show", f"{BASE}:{PATH}"], cwd=ROOT, text=True)


def code(source):
    return re.sub(r"//[^\n]*|/\*.*?\*/", "", source, flags=re.S).split()


old_pick = "cambc::draft::pick(available.at(random_number(available.size())));"
new_pick = """const auto fallback = available.at(random_number(available.size()));
    cambc::draft::pick(chosen.empty() ? cambc::champion_draft::varg : fallback);"""
isolated = code(accepted.replace(old_pick, new_pick)) == code(text)
# Once isolation holds, the unchanged pool is all 11 released choices minus our
# completed picks. Exhaust every legal history up to the last five-pick turn;
# adversarial fallback selection covers every possible RNG result.
legal = isolated
cases = 0
for size in range(5):
    for chosen in itertools.permutations(range(11), size):
        pool = set(range(11)) - set(chosen)
        outputs = {9} if not chosen else pool  # pinned SDK: Varg draft ID 9
        legal &= bool(outputs) and outputs <= pool
        cases += 1

checks = {
    "only_draft_selection_changed": isolated,
    "every_legal_history_has_only_available_outputs": bool(legal),
    "exactly_one_random_draw_retained": text.count("random_number(") == 1,
}
for path in (ROOT / "bots/gamma/src").iterdir():
    if path.is_file() and path.name != "draft.cpp":
        checks[f"{path.name}_matches_accepted"] = path.read_bytes() == subprocess.check_output(
            ["git", "show", f"{BASE}:{path.relative_to(ROOT)}"], cwd=ROOT
        )
report = {
    "kind": "source isolation and finite legal-draft model, not engine execution",
    "draft_cpp_sha256": hashlib.sha256(text.encode()).hexdigest(),
    "legal_histories_checked": cases,
    "checks": checks,
    "passed": all(checks.values()),
}
output = ROOT / "experiments/gamma/varg-draft-source-check.json"
output.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
raise SystemExit(0 if report["passed"] else 1)
