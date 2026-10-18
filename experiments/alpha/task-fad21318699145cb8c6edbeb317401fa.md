# Current experiment: task-fad21318699145cb8c6edbeb317401fa

## Identity and status
- Bot alpha; branch bot/alpha; input HEAD 8a8819e101d7d70ff99cf010662456b4184e846c.
- Edit commit 6af1685b849ad23ee9eaadb1a8de18742318d87b; base source
  87b9be4549dd0ee3a3038907bcfb86b79cfb2d33f344f8749d9532a8e6382e01.
  All six source files verified byte-identical to edit commit before editing.
  Initial HEAD diff/deleted dash headers were trusted preparation, not unfinished work.
- Latest candidate has completed INCONCLUSIVE evaluation; pending self-play is
  separate. Protected champion c0cebd720fcd55e2bbb51d57dd2c398889d4071e remains in Git.
  Prior operational notes archived as task-b61dfbca8f5349ac832abc6a600f85ab.md.
- Engine/SDK 2.1.6; historical-panels-v1; lock
  00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668.
- Routine unchanged-doc iteration; prior full-review basis task-b61dfbca8f5349ac832abc6a600f85ab.
  Consulted compact reference, research/organizer limits, economy/combat playbooks,
  relevant handbook/API and installed SDK contracts. Header hash matches brief.
  Organizer page is a download hub; event-policy and production-parity limits remain.

## One hypothesis
Focusing champion basic attacks and reset follow-ups on the lowest-health legal
visible enemy, breaking equal-health ties by carried gems, will increase matched
development win rate over the edit base. Unchanged or lower win rate falsifies
this hypothesis. Kills, deaths and submitted gems diagnose the mechanism.
This is an unmeasured source/rules deduction, not a causal claim about a loss.

## Evidence and decision
- Evaluation b4c8b53911a3b94679ff7e1a1ff36e0fcf03e541da6d790ef8439b2b1ceeb9f2
  measures 8a8819e / source 8608f03590f10c590a539ccc7070ef74c080607b26aa897df0138be59391dc4e,
  not the source edited here. Development: 42W/6L, no faults/missing/unknown;
  matched development-base delta 0.0 across 24 side-paired cells.
  Contrasting map coverage: collision A/B each 4W/0L; elkring A and B each 3W/1L.
  Aggregates do not establish target choices or missed finishing attacks.
- Frozen manifest 13a21f2cd26eab071a4b4743a9e465c4b81c17db25d5a4ee76b2d1b06bc6fdb1:
  all four source sets hash-verified. Alpha 6af1685b equals edit base; beta 6450f600
  uses a post-basic unit spell; gamma e9704a21 and starter 144ab5a9 use basics.
  All select first in-range basic target, with random draft/build, nearest-camp
  routes and immediate banking. Source observations are not runtime traces.
- Canonical final slices saved in this task's -evidence.json: historical dash
  source, corners A loss 57599b1c1943087d7580b16a1693de18401161734d03839db10e214f030b2010,
  round 415, submitted 292 vs 1004, deaths 5 vs 0; elkring A loss
  7821425f5bb7c52d1b313cd8c80db1e939f6cf7c2d1d47056ceac18f7eef135c,
  round 593, submitted 612 vs 1008, deaths 8 vs 7. Both have zero faults.
  Opponent revision unknown in these final artifacts; no target-choice traces.
  Artifact engineVersion 0.0.1 is not envelope CLI/SDK 2.1.6.
- Basic enumeration order ignores wounds and carried value. Repeated basics on
  one wounded enemy can remove damage/contest sooner, with independently observing
  allies tending to converge without a shared-memory protocol.
- Prior area/finish spell scoring regressed matched development (-0.041667).
  This candidate keeps all spell/camp selection intact and changes champion basics.
  Do not repeat rejected global capture, fixed draft/Strength, 40-gem batching or
  spawn-heal-only changes. Latest dashes had zero matched win-rate delta.

## Candidate policy
- Only bot.cpp differs from edit base. Five other source files unchanged.
- Scan at most 16 candidates; visibility precedes all live reads, and only living
  in-range enemies qualify. Prefer minimum absolute health, then maximum carried
  gems; exact ties retain stable engine order. Camp basics retain first-target order.
- Reset prediction uses the same selector, ignoring only the spent basic allowance.
  Actual attack reselects with full allowance/restriction checks after the cast.
  No cross-turn target cache, new memory, AoE search or fuel overrides.
- Existing 18,000-fuel reserve bounds scans and leaves cheap legal behavior/yield.
  This is a guard, not measured headroom. Draft, build, navigation, channels,
  recovery, banking, spell scores and defensive casts retain edit-base behavior.

## Validation and uncertainty
- Decision/identity/source audit: task-fad21318699145cb8c6edbeb317401fa-decision.json.
- git diff --check passed before trusted check.
- bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json PASSED,
  exit 0, exact source e028774f1102eeffb4372ca9eee3f54044819b2f48718548dfac7ea262840347.
  Report .agent/check-task-fad21318699145cb8c6edbeb317401fa.json;
  check:task-fad21318699145cb8c6edbeb317401fa:e028774f1102eeffb4372ca9eee3f54044819b2f48718548dfac7ea262840347.
  Smoke IDs 85a92fa459a40301b1fc2d53270c0888a02e3241741bae798607d03068c0e798
  and ef5bfcbc95392f19890151a922f9bdfc25a342b707c13c5273741dc3fef23b41.
  Inspected actual summary report: no detailed runtime diagnostics. IDs/exit alone
  do not establish completed full games, targeting coverage or improvement.
- Final git diff --check passed. No bot-source edits after trusted check.
- No tournament evaluation run here. Tactical branch coverage, fuel headroom and
  win-rate improvement remain unknown. Absolute health ignores shields/mitigation;
  selecting a wounded shielded enemy may be poor. Different ally vision prevents
  guaranteed focus. Expanded champion scans increase fuel use.
- Next: supervisor evaluates exact checked source against edit base and protected
  champion across maps/both sides. Reject unchanged/lower matched win rate; use
  deaths, kills and submitted gems to diagnose targeting before changing spells.
