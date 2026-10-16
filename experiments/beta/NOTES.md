# Operational summary

Accepted baseline: commit `0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9`, source
`9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f`.
Pinned engine/SDK 2.1.6. Original bootstrap used the official C++ starter.
No interrupted edits or pending candidate were present; branch, HEAD and both
working/accepted snapshot source hashes matched the task envelope.

## task-19787a987c804a8ea512fde561a1b4c4 — complete spawn recovery

Playbook B (regression repair), using recovery timing in playbook C.
Hypothesis: yielding on allied spawn while wounded after shopping prevents
premature departure after recall, allowing full recovery at turn end and
reducing repeated low-health recalls. Falsifiable expectation: an alive,
non-channeling wounded champion at spawn takes no route/combat action that
turn; it can leave on the next turn when fully healed. Full-health spawn
behavior and the existing recall threshold remain unchanged.

Evidence: accepted evaluation `17b3eb677924784f6781e7045017903e0e7161eaac79ea7a0050bba6a383d919`
had no reported bot faults and three losses. Cases on the accepted source:
- collision, side B, match `2ea55d897829d837d2d71c66198c5e67dd6991fd3c1217ca8471d7c5a158a6cc`: 36 deaths.
- corners, side B, match `aa5eee7c876f7b4eb4d80cdb77aa81321c8a3795fa7cb2c68d188a54e2b76be0`: 16 deaths, 110 submitted gems.
- elkring, side A, match `169e3d8697903fa0ff9301f2f6e0c9648e8f61019d631a68a2964eb4e3756b76`: 43 deaths.
These aggregates motivate recovery inspection but do not establish death causes.
No turn traces were supplied. Source inspection found no wounded-spawn guard:
recall completion could fall directly through into banking/farming movement.
GameRules.md lines 122 and 373–375 explicitly require waiting until turn end.
Installed C++ binding health/max_health queries read current self state.

Change: after spawn shopping, return while health is below maximum. main.cpp
still calls end_turn. No new memory layout, parameters, draft or combat changes.
The accepted snapshot remains outside the edit transaction and unchanged.

Validation: `bot-check --owner-config /var/lib/battlecode-volume/config/beta.json`
exited 0, state PASSED: exact-source build and completed fault-free both-side
smokes per trusted wrapper. Candidate source:
`5ce83774dbb2ba2a893c9cf2c4a7d24919420b4f5a27ddbda77b8d106ae3a7b0`.
Report: `.agent/check-task-19787a987c804a8ea512fde561a1b4c4.json`.
Trusted report: `/srv/battlecode/checks/task-19787a987c804a8ea512fde561a1b4c4/5ce83774dbb2ba2a893c9cf2c4a7d24919420b4f5a27ddbda77b8d106ae3a7b0/report.json`.
Smoke IDs: `d820d0eea762b934b63c5254faa111fbdf9c993fc085741032c74707597d2504`,
`6d58aa2e81bb18fe9a5e04cf4a91cf6a347fe89d42bf9ddfc99d4f32321052d8`.
`git diff --check` passed. An optional listing of the arena's internal checks
folder was permission denied; no retry or permission change was attempted.
Validation claims rely on the trusted wrapper response, not that folder.
Remaining uncertainty: this guard's strategic benefit and frequency in accepted
losses are unmeasured. Smoke validity is not evidence of improved strength.
Next idea after evaluation: inspect recovery traces and repeated recall frequency.
Separate organizers' AGENTS.md remains unavailable, as recorded in RESEARCH.md.

## task-2a7a442a0b7e4920a536dcf46b9d23a0 — nearby tribute priority

Playbook C. Hypothesis: prioritizing an immediately available tribute over an
opportunistic enemy attack prevents combat from repeatedly delaying banking.
Falsifiable expectation: after existing channel/shop/recall guards, a carrier
within tribute range of an unlocked altar starts tribute without attacking,
even with an attackable enemy. Outside that case, combat/travel priorities stay
unchanged. Death, stun and locks can still prevent successful banking.

Identity: branch bot/beta, HEAD/input 02ab89d1e111f8c75f726004ee54346f5e7e4d8a.
Initial working and accepted snapshot source hashes both equal the baseline
9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
Initial diff removes the prior candidate's spawn guard; arena/worker.py
make_attempt explicitly restores accepted source before invocation. This is
expected setup, not interrupted work. No pending evaluation: supplied feedback
d895057d31eda679526427d5fe39fdafaca17fb31dc2bf8aeec13c26cf8b1807 is INCONCLUSIVE.
Engine/SDK remains 2.1.6; supplied documentation hashes match RESEARCH.md.
Accepted snapshot remains untouched outside this edit transaction.

Evidence limits: feedback evaluates candidate source
5ce83774dbb2ba2a893c9cf2c4a7d24919420b4f5a27ddbda77b8d106ae3a7b0,
not current baseline or this patch. Candidate losses include collision B,
match d3a449ab7793af6d1f7054f4cf54a1954bb8199615b32cb0dc49962dfebe8618
(858 submitted, 36 deaths), and elkring A,
match 9b6341ea49e134f09771bcf08babf6e505f6828c0a2b792fefd43e2e50e51b19
(504 submitted, 42 deaths). Neither has faults or supplied turn traces;
these totals do not prove combat delayed tribute. Source establishes the
reproducible decision pattern: attack_if_in_range returned before tribute.
GameRules.md:223 says ordinary damage does not interrupt tribute. Installed
C++ submit_gems returns void; has_altar_lock observes either team's locks.
Existing conservative lock exclusion is preserved.

Change: move only the in-range tribute attempt ahead of enemy combat, after
recall; retain banking movement after combat. Update priority comment in bot.h.
No shared-memory, draft, recall threshold or spawn-recovery changes.
Validation pending trusted wrapper below. Strategic gain remains unmeasured.
Next idea: evaluate this candidate against the accepted baseline; if traces
become available, measure turns spent attacking while tribute was available.

Validation: `bot-check --owner-config /var/lib/battlecode-volume/config/beta.json`
exited 0, trusted state PASSED for source
89bf52d2f9c5904b35afc5edc5851586a5a6cce7dcc48a879f473235589a45af.
Local report: .agent/check-task-2a7a442a0b7e4920a536dcf46b9d23a0.json.
Trusted report reference (not opened):
/srv/battlecode/checks/task-2a7a442a0b7e4920a536dcf46b9d23a0/89bf52d2f9c5904b35afc5edc5851586a5a6cce7dcc48a879f473235589a45af/report.json.
Wrapper match IDs: 18becb7e85db1c5f94ad705af6649b5cc510712bea5e4fba5c76efdec6747ee5,
edd864c4b2384543243a076dd6095d711b67ce7449ae5833b615c7fe1f558807.
`git diff --check` passed. No claim of strategic improvement or measured
banking-delay reduction; supervisor evaluation is the next action.
