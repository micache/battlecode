# Current experiment: task-b61dfbca8f5349ac832abc6a600f85ab

## Identity and status
- Bot alpha, branch bot/alpha; input b05df0c086ce758e54c5b153509355f4864f7783.
- Edit commit 6af1685b849ad23ee9eaadb1a8de18742318d87b; base source
  87b9be4549dd0ee3a3038907bcfb86b79cfb2d33f344f8749d9532a8e6382e01.
  All six entry files matched that commit. Initial HEAD diff/deleted scoring
  header was trusted preparation. No unfinished patch; latest task PUBLISHED
  with completed INCONCLUSIVE evaluation. Pending self-play is separate.
- Protected champion c0cebd720fcd55e2bbb51d57dd2c398889d4071e remains in Git.
  No agents, commits, publication, submission or tournament evaluation here.
- Engine/SDK 2.1.6, historical-panels-v1; lock
  00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668.
- Unchanged documentation hashes verified; review basis task-d71c11f9549c4960bf74ec303723f6a8.
  Read compact reference, research/organizer limits, relevant C/D/F playbooks,
  handbook movement/dash kits/capture/recovery, API and installed SDK contracts.
  Header hash matches brief. Organizer page is a download hub; event-policy and
  production-parity limits remain. Previous notes archived by task ID.

## One hypothesis
Using ready, walk-compatible dashes to cut at least two steps from existing
objective routes will reduce paired-win completion rounds without reducing
matched win rate versus the edit base. Unchanged/increased rounds or a win-rate
regression falsifies the hypothesis. This is an unmeasured rules/source deduction;
travel costs and dash branch coverage are not available from supplied aggregates.

## Evidence and decision
- Evaluation 086044d9b74acef4f173cfbd02aac8733cc1774a39533598b3f52fade9308124
  measures b05df0c / b87639faa949861e2afb04cf863943dae3ea1ad95c3b58999fe1bd456c31e4fd,
  not the edit source: 40W/8L, no faults/missing/unknown. Matched development-base
  delta -0.041667 across 24 side-paired cells; corners/lanes regressed. Do not
  repeat its area/finish scoring. Supplied base self-play is 24 unique wins,
  mean round 538.083; deterministic repeats are not independent samples.
- Latest-source collision A loss c83f8af10aeca117908d230411b826453ebf0bc807354f469031e6b48b84fd2e:
  round 657, submitted 198 vs 1004, deaths 12 vs 2. Corners A loss
  752aae9fac7a4d3dc660f68a5605f9df64b4d6fc25d45c9bb871421d27c28f11:
  round 380, submitted 200 vs 1004, deaths 5 vs 0. Opponent is frozen alpha
  6af1685b / 87b9be45. No trace supports attributing these losses to travel.
  Contrasting supplied aggregate: collision B 4W/0L for that latest source.
- Frozen manifest 433d8f5d4fff6ecbc8d9c61b10b876cc2357f96a69679fbfec3509c6ffe811e7:
  all four source sets hash-verified. Beta 6450f600 basic+unit spell; gamma
  e9704a21 and starter 144ab5a9 basics; alpha 6af1685b equals edit source.
  Random draft/build, nearest-camp routes and immediate banking are shared.
  None uses dash. These source observations do not establish runtime events.
- Handbook: walk one tile, dash two with compatible walking and eight-turn-end
  cooldown. Four draft possibilities have dashes, but base never casts them.
  Travel is repeated for farming, banking and retreat, making unused mobility
  a distinct throughput opportunity without replacing the strong combat policy.
- Prior global capture priority, fixed composition/Strength package, 40-gem
  batching and repeated spawn-heal-only experiments remain negative/deferred.

## Candidate policy
- Added travel_dash.h selector and compile-time geometry checks; changed only
  navigation in bot.cpp relative to edit source. Draft/build, independent combat
  allowances/scoring, capture/banking priorities, memory and yield remain intact.
- Normal walking first. If a dash was ready and walk-compatible, recheck cast
  availability/restrictions/cooldown and rebuild observed blockers after movement.
  Only use existing dashes with SDK range >=2; no hard-coded champion identity.
- Reuse the route distance field as a hint; search eight straight two-step rays.
  Both intermediate/landing tiles must be in range and free of known walls,
  holes, altars, enemy spawn, units and teleport reservations. Require >=2 field
  distance improvement; never leave an already-reached route goal to dash.
- One cast attempt. A hidden obstruction returning false gets no blind retry;
  caller refreshes vision before any post-movement camp combat. No cached enemy
  state or new shared memory. No hole crossings or bent dash paths in this test.
- 30,000-fuel guard before dash planning/attempt; original 18,000 combat guard
  retained. At most eight endpoint evaluations, no additional route-field solve
  except replacing the singleton shortcut when a usable dash exists. Guards are
  policy reserves, not measured headroom. No fuel setting changes.

## Validation and uncertainty
- git diff --check PASSED, exit 0.
- Host exhaustive geometry fixture compile attempt FAILED, exit 127: no c++
  compiler (clang++/g++/clang/gcc also unavailable). Fixture did not execute.
  See decision JSON for exact attempted command. Do not claim exhaustive coverage.
- Eight focused geometry assertions are compiled into the trusted bot build:
  open two-step travel, fresh midpoint/landing blockers, boundary/goal occupancy,
  one-step remainder, insufficient gain, unreachable origin and reverse travel.
- bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json PASSED,
  exit 0, source 8608f03590f10c590a539ccc7070ef74c080607b26aa897df0138be59391dc4e.
  Report .agent/check-task-b61dfbca8f5349ac832abc6a600f85ab.json;
  check:task-b61dfbca8f5349ac832abc6a600f85ab:8608f03590f10c590a539ccc7070ef74c080607b26aa897df0138be59391dc4e.
  Approved check-report agrees; summary exposes no detailed runtime diagnostics.
  Smoke IDs ab9d3e31392b097fcfc88ac670d6af40ec3cdfb6535ed7c1a70d277ed714be89
  and b70a3bc67736ba9460869c03885b5608b172518be04b3d1e8c05a8443b879e09.
  IDs alone do not establish full-game completion, dash coverage or improvement.
- Source audit/decision/evidence: this task's -decision.json. No bot-source edits
  after trusted check. Eight static assertions passed, exhaustive fixture unrun.
- Risks: a travel dash consumes the reset allowance's competing cast, can approach
  threats faster, and follows a field from before newly exposed blockers. Fresh
  local geometry enforces legality but not globally optimal or safe routing.
- Next: supervisor evaluates exact checked source against edit base and protected
  champion across maps/both sides. Reject win-rate regression; compare paired-win
  rounds, deaths and submitted gems. If mobility regresses, inspect dash destinations
  and reset opportunity cost before adding hole jumps or combat chase behavior.
