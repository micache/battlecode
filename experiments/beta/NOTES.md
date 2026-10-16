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
