# Operational summary

## task-490c542467de4fe282d89f6170644b21 — bounded combat retargeting

Hypothesis: selecting useful damage/finishes across the current camp group or
eligible visible threats, then refreshing targets after each basic/cast, will
increase clearing/defensive combat efficiency, submitted gems and matched wins.
Falsifier: matched win/throughput regression or more deaths/fuel suspension.
Mechanism is a source/rules deduction; no per-turn trace establishes causation.
Decision and full final-statistics artifacts: task-490c542467de4fe282d89f6170644b21/.

Identity: beta, bot/beta; task as above. HEAD/input
27dedf6219cbf10a44f92bbe76d1a328f1d8adab. Trusted edit
 d2d57274232ca7cead5bacf650d6f51fd5b3bc3d / base source
7daa9117b8727b0da55d9282f8693e88107406d3b554eb644f3b9cf7b6f4ad6e.
All six files matched edit Git blobs at entry; prepared bot.cpp/bot.h differences
and absent HEAD farm_policy.h were intentional. No incomplete unpublished work.
Latest candidate evaluation completed; no evaluation was awaited or started.
Protected champion 0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9 remains in Git.

Evidence: evaluation 858f5f0f30f93eaca6b10cb4f5ca1adb64dd102b5b41a4d7a09c9e0951bc5a3a
measured 27dedf62 / ec6ad44a, not this edit base or new candidate. Development
35W/13L, zero faults; matched edit-base delta +0.041667 with interlock regression.
Collision losses 19bdaff916c9c5c9d84a2a686bc0ac3e97832b8b236fb28e023b098b58944f73
(beta A, round 627, 132 submitted/386 collected, 7 deaths) and
774bf8fc72bf6a8aad68066c56e6abe7f07a9b01a892d24c46150c03540ca2f6
(beta B, round 899, 788/912, 8 deaths) motivate combat/survival investigation.
Contrasting final b6788e499d20fca9766f4075be19301f06142fa66aa53f716283d46658e9f937
(A, round 573, 1030 submitted, zero deaths) is listed in development-selection
evidence for that evaluation, but map and exact own source are unknown in its
final artifact. Do not treat it as a controlled current-source win. Final files
are hindsight, never runtime inputs. Embedded engineVersion 0.0.1 does not by
itself certify parity with the pinned runner/SDK version 2.1.6.

Frozen manifest 0bc95225443049e87bc4c0460a6ddb7d423dffc0f3a13d7866ee6a89ca3166e9
inspected. Alpha 6af1685b / 87b9be45 refreshes targets after casts, compares
capped damage/reset, uses enemy-first combat, random roster/stats and camp unions.
Gamma 1b34f42a / 3ce565f6 focuses a target, tracks observed respawn deadlines
and reachable value/time. Adopted alpha's compatible action-refresh idea only;
no private worker state, opponent edits or assumptions about official opponents.

Current strategy: Varg/Tavi/Ryth/Vendetta/Marcella farming roster; Jungle Strength,
Monster Strength, Durability Health, then Power Strength. Explicit camp capture;
bank each bag; complete spawn healing; no live shared memory. Routing, draft,
shopping, shield use, banking and recovery policy remain as in edit base.
This experiment changes only combat targeting/action sequencing:
- Snapshot at most 16 visible live targets, checking visibility before health
  and position. Keep snapshots within one action phase, never across turns.
- Rank basic targets by capped damage plus 0.5 Strength for finishes; include
  observed Varg splash. Ground AoE compares visible damage across aim points.
- Refresh after the initial basic even if it killed the previous target. Select
  resets only with a surviving in-range target and available attack permission.
- After successful cast, reacquire/rank targets for a fresh basic. Check engine
  allowances/restrictions; do not assume kills restore cast allowance.
- At most one initial basic, one cast (including existing shield), one follow-up
  basic. Preserve movement exclusions and do not walk after successful combat.
- Stop optional scans below 30k fuel; retain 18k action reserve and fixed scans.
  These are planning reserves, not measured suspension-free headroom.
- combat_policy.h has six constexpr hit-value regressions, compiled by bot-check.

Engine 2.1.6; lock 00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668;
suite historical-panels-v1. Documentation/SDK unchanged per trusted handoff.
Consulted BOT_REFERENCE, RESEARCH, organizer record, Playbooks B/C/D/E/F/G and
relevant handbook/C++ API/pinned-header combat, visibility and action contracts.
Pinned header SHA256 90f4242686f22305b28d76d4fa2297187931b3c974f96faf324199e93979203d.
Organizer page is a download hub; production parity/additional policies unknown.

Checks on final bot source (no source changes afterward):
`bot-check --owner-config /var/lib/battlecode-volume/config/beta.json`
PASSED, exit 0; source
6d52acdbd7f1a71f6fa9ef3592dfd6ecf3a82ccbcee05d33d335460f0355bc75.
Report .agent/check-task-490c542467de4fe282d89f6170644b21.json;
check:task-490c542467de4fe282d89f6170644b21:6d52acdbd7f1a71f6fa9ef3592dfd6ecf3a82ccbcee05d33d335460f0355bc75.
Exact-source check-report independently returned PASSED/0. Smoke IDs
c0653c7bec77f1cdf2fadbb36e431f1231e8fcc18a07b30ff14e6c2de5af2e62
and 5c84f2a787ca7235be5416050182d8cfb437c598c3a69533fa58819d58e1d67f.
Permitted own-side stdout exports exited 0 and contain zero bytes, saved as
smoke-a.json/smoke-b.json. They do not prove complete games or no suspensions.
`python3 experiments/beta/task-490c542467de4fe282d89f6170644b21/check_combat_contracts.py`
PASSED/0, report invariants.txt in that directory. Source safety contracts cover
fresh targets, visibility, reset validity, restrictions, bounded casts/scans,
channels, capture, recovery and free roots; eight unsafe mutations rejected.
The first harness run raised ValueError when a mutation removed a required guard;
the harness now treats that as rejection. No bot fault or source repair involved.
These are source contracts, not a game simulation. `git diff --check` PASSED/0;
report diff-check.txt in this task directory.

Risks: additional live queries, 16-target cap, damage estimates ignore mitigation
and shields, finish/splash ranking may split focus, existing shield competes with
reset. Comparative gains, fuel headroom and effect on survival remain unmeasured.
Prior scheduling gained only +0.041667 with interlock regression and was not the
selected edit base; harvest circuits had zero matched gain. Prior isolated draft,
item, weak-camp and shield variants did not establish additive gains. Previous
notes including negative findings archived in archive/through-task-c28fb5b460264834ae1f67c600db2eae.md.

Next: supervisor evaluates exact checked source against d2d57274 on matched maps,
both sides and frozen opponents. Compare wins, submitted/collected gems, deaths
and available fuel telemetry. Keep the full accepted-champion gate mandatory.
