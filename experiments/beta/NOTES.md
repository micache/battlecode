# Operational summary

Accepted baseline: commit `0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9`, source
`9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f`.
Engine/SDK 2.1.6. Prior experiments archived in
`archive/through-task-71c9eb3108ef49ebb55a7414dded1ec1.md`.

## task-3b818b28bcb04cca83683548f6c579dc — collect cleared camps first

Playbook C. Hypothesis: prioritizing visible reward-available groups before
basic attacks on other camps reduces delays between clearing and collection.
Falsifiable expectation: when farming on a reward-available group's spawn tile,
the champion holds position; otherwise a successful step toward a cleared group
ends farming for this turn, even when another camp was initially attackable.
Unreachable/blocked capture goals fall back to baseline farming. Once captured,
respawning state removes the capture priority. Combat, banking, recall and
channel priorities outside farm_camps remain unchanged.

Identity: bot beta, branch bot/beta, HEAD/input
`d929b5e61078ce87da57906f59d6887216434770`. Working and accepted-snapshot
source hashes both matched baseline above before edits. Initial diff reset the
prior candidate, as arena/worker.py make_attempt explicitly restores accepted
source. No interrupted edits or pending evaluation: supplied feedback
`17ac318eeb4ef7475c3af14f6c08d4b83bc884c31ef0043caf63f5770b735ef0`
is INCONCLUSIVE. Documentation hashes match RESEARCH.md. Accepted snapshot
remains outside the edit transaction; separate organizer AGENTS.md unavailable.

Evidence: feedback evaluates source
`4a47b50ba1d4170055dba73a6b3abdf1788967dbe44ec4135b3e722830b66947`,
not the baseline or this patch. Losses include corners B,
`d23d5734931588329ef179f082c6a33730618f9d852b80e3f394c1ad8ac022b8`
(230 collected, 124 submitted, 16 deaths), and elkring A,
`ac94627a35ddedbc1f0d258cf11b373406ba506e750384d54c624e60bcbffdce`
(522 collected, 324 submitted, 43 deaths). No reported bot faults. These totals
motivate economy inspection but do not prove missed captures. Capture completion
and turn traces are unavailable. Source proves in-range camp attacks precede
movement onto cleared spawn tiles. Rules GameRules.md:191–205 require uncontested
spawn occupancy for five rounds. Installed C++ SDK camp_group_reward_available
means all camps defeated; vision::camp_groups filters by current visibility.

Change: within farm_camps, union visible cleared spawn tiles, hold if already
occupying one, otherwise attempt capture movement before ordinary camp attacks.
No extra shared memory or policy thresholds. Existing movement fallback and
main.cpp end_turn are retained. This is a single farming-priority experiment.

Remaining uncertainty: capture benefit, duplicated collectors, contested groups,
and fuel headroom are unmeasured. Prioritizing an occupied/unreachable group may
still fail and use baseline fallback; no safety or strength improvement claimed.
Next action: supervisor evaluation against accepted baseline; measure collection
delays if bounded traces become available.

Validation: `bot-check --owner-config /var/lib/battlecode-volume/config/beta.json`
exited 0, state PASSED for exact source
`c35aa333ec97f25235b09630777b16febbac86cd80423946d2065bb2321ccf02`.
Local report: `.agent/check-task-3b818b28bcb04cca83683548f6c579dc.json`.
Trusted report reference (not opened):
`/srv/battlecode/checks/task-3b818b28bcb04cca83683548f6c579dc/c35aa333ec97f25235b09630777b16febbac86cd80423946d2065bb2321ccf02/report.json`.
Wrapper smoke IDs:
`403003eb4b1fc7840a2ff4a8bcf05200d610b8120dd2ea7fb6618a1490cb6154`,
`3fd672d4f5f86dc4aaecc2da0a78b3f7f11d566f0c393d653f70a8c14a54c9e1`.
The trusted wrapper requires completed, fault-free games on both sides for
PASSED (arena/supervisor.py check_source). `git diff --check` passed.
These smokes validate execution, not the capture hypothesis or improved strength.
