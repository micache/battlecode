# Operational summary

## task-c28fb5b460264834ae1f67c600db2eae — reachable camp scheduling

Hypothesis: remembering observed camp cooldowns and ranking reachable travel,
clearing and capture cost per reward increases submitted gems and matched wins,
especially corners. This is an unmeasured rules/source deduction. Falsifier:
matched win/throughput regression or increased fuel suspension. Decision and
saved development metrics: task-c28fb5b460264834ae1f67c600db2eae/decision.md
and development-evidence.json.

Identity: beta, bot/beta; input/HEAD aa89dd9b284e35125c9e218d79a6e0c7ae380183.
Trusted edit d2d57274232ca7cead5bacf650d6f51fd5b3bc3d / base source
7daa9117b8727b0da55d9282f8693e88107406d3b554eb644f3b9cf7b6f4ad6e.
All six source files matched edit Git blobs on entry. Initial differences from
HEAD, including absent circuit_policy.h, were trusted preparation. Accepted
champion 0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9 is preserved in Git.
Latest candidate evaluation completed; pending self-play for that already
measured source is not a pending unpublished experiment. No recovery needed.

Evidence: evaluation e151696ef79a97a3a76652ed6f71c443041bf017fccd9261401932315f3ab80f
measured aa89dd9b/source 7a4e377b (harvest circuits), not today's edit source.
Development-six-map: 33W/15L, zero faults; comparison against today's edit base
was delta 0.0 over 24 side-paired cases. Corners 3W/5L contrasts lanes and
interlock at 7W/1L each. Collision loss ac40ab67 (beta A, round 684) had 13 deaths,
352 collected/176 submitted; c886ab82 (beta B, round 740) had 9 deaths, 594/418.
No per-turn trace establishes their causal mechanism. Full IDs in saved JSON.
Base-source self-play has 10W/9L across 19 unique cells, zero faults; older
external observations have different sources/unknown opponents and patch.

Frozen manifest 5f1d852bc02f2028f069e4a0a444450add0da587ca0596044e410e399a645d8d
inspected. Gamma 1b34f42a/3ce565f6 uses observed respawn deadlines and reachable
value/time. Alpha 6af1685b/87b9be45 uses enemy-first combat, random roster/stats
and nearest-camp unions. Adapted gamma's compatible observation discipline;
beta retains its own bounded shortlist and farming strategy. No private state.

Current strategy: roster Varg/Tavi/Ryth/Vendetta/Marcella; Jungle Strength,
Monster Strength, Durability Health then Power Strength; active combat kits;
explicit capture; bank each bag; full spawn recovery; no live shared memory.
This experiment changes only camp scheduling and its observation/action flow:
- Remember visible respawn deadlines; filter before the 12-group shortlist.
  At expiry state is unknown again, not assumed respawned.
- Native forward field measures free reachable attack/capture/scouting goals.
  Unknown camps use unseen spawn goals; visible empty spawns do not cause a
  zero-distance scouting stall. Temporarily defer unreachable entries 12 rounds.
- Score (ceil(path/move speed) + health/Strength + capture_time+1) /
  (gems + 0.12*gold); commitment x0.85, visible allied congestion x1.35.
  Unknown health remains a static design estimate; no hidden live reads.
- Preserve own capture and avoid extra collectors. Vacate collected spawns when
  no work is selected. Refresh combat observations after successful moves and
  failed hidden-blocker reveals; respect actual movement for exclusive spells.
- Start new fields only with at least 65k fuel; stop scans at 45k, reserve 18k for
  actions. Discard incomplete estimates. Bounded combat fallback and final yield.
- farm_policy.h contains ten compile-time lifecycle/ranking regressions.

Engine 2.1.6 / lock 00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668;
suite historical-panels-v1. Current docs/SDK unchanged. Consulted BOT_REFERENCE,
RESEARCH, organizer record, Playbooks B/C/F, handbook camp lifecycle, current
C++ API and pinned header's camp-group/distance-field contracts. SDK SHA256
90f4242686f22305b28d76d4fa2297187931b3c974f96faf324199e93979203d.
Organizer page is a download hub; production parity/additional policy unknown.

Checks:
`bot-check --owner-config /var/lib/battlecode-volume/config/beta.json`
PASSED, exit 0; final source
ec6ad44a1d7a1ed8bea0e6e3eaefdc8fcf8a51be85b94a0702f41be777df2633.
Report .agent/check-task-c28fb5b460264834ae1f67c600db2eae.json;
check:task-c28fb5b460264834ae1f67c600db2eae:ec6ad44a1d7a1ed8bea0e6e3eaefdc8fcf8a51be85b94a0702f41be777df2633.
Exact-source check-report independently returned PASSED, exit 0. Ten constexpr
regressions compiled. Smoke IDs 3f90a9ace98cc760b00e76039b8d658043f22bdb840f56c28195245d4ab9fa55
and 854e4b3e5cc7f59e3ef8a94bb994760537e6a12c6f64bb6452580735fd968ea6.
`python3 experiments/beta/task-bc8c3246ad3449e39155d369ae07c9e0/check_invariants.py`
PASSED, exit 0, report task-c28fb5b460264834ae1f67c600db2eae/invariants.txt;
existing source contracts cover observation, capture/channel preservation,
recovery, free roots, bounded retry, spell exclusions/reset and draft. Seven
unsafe source mutations rejected. These are contracts, not a game simulation.
`git diff --check` PASSED, exit 0; report this task's diff-check.txt.
Both approved own-side smoke stdout exports exited 0 and are empty (size 0);
saved as this task's smoke-a.json and smoke-b.json. Empty logs do not establish
complete games, no suspensions or comparative gains.
No source edits after trusted check. Notes/artifacts do not change bot source.

Risks: extra field/query fuel, conservative clear estimates, missed distant
opportunities beyond the bounded shortlist, dynamic blockers and unseen enemies.
Actual fuel headroom and comparative win/objective gains remain unmeasured.
Harvest circuits had zero matched gain; prior isolated weak-camp, draft, item
and shield variants did not establish additive gains. Prior full notes preserved
in archive/through-task-4acc026b087b4a278e69d874a032cb52.md. Rejected a repeated
banking experiment and speculative combat/roster changes for this invocation.

Next: supervisor evaluates exact checked source against d2d57274 on matched
maps, both sides and frozen opponents. Compare wins, submitted/collected gems,
round, deaths and suspension telemetry. Inspect corners route throughput and
collision survival separately; full accepted-champion gate remains mandatory.
