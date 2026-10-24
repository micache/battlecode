# Gamma operational notes

## task-93a56bca32614c11b13bb0bc448670dd — reachable objective routing

- Refinement; branch bot/gamma. Trusted edit base/protected champion
  1a0675ca881d4b67cb5c6cb1822ce2ae1602dc4d, source
  9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
  HEAD/input aae86b28b8ceb20dba746ddd8b597be83f69deea differs deliberately.
  All six starting files matched the trusted base; prepared plan.h deletion was
  intentional. Reused inspected own HEAD melee implementation explicitly as
  part of this candidate, not as a change of edit base.
- Prior task d684842d had QUOTA_WAIT, zero checks/evaluations, no publication.
  Its exact source equals this trusted starter. Its checkpoint patch and notes
  remain intact at the supplied recovery paths; no unfinished strategy found.
- Hypothesis: topology-aware camp shortlisting and bank timing on the measured
  melee economy increases matched wins AND mean tribute over aae86b28/source
  7762c7e2, retains its gain over the trusted starter, without new own faults or
  fuel suspensions. Non-positive win/tribute change or new reliability failures
  falsifies it. Routing mechanism is an unmeasured rules/source deduction.

## Evidence and decision

- Evaluation43a38de3, source7762c7e2: REJECTED,270W/130L. Matched development
  delta+0.5027027 versus starter over185 side-paired cases, not a near-zero delta.
  Per-map candidate/base: islands0.1/0.4, corridors0.2/0.2, ambush0.5/0.3.
  Development mean tribute705.37, collection785.29, bag loss55.05; zero own
  faults/suspensions in370 observations. These statistics evaluate the previous
  candidate, not today's source; rejection remains a negative finding.
- Development loss29487e014d4ce38b92a30ba405f829a8f92ecfdfc6762bcf8191bc8c03f7f939,
  A/00ambush, source7762c7e2: tribute695/1007, collection732/1007, deaths8/3,
  no own bag loss. Ryth collected18, Marcella0; not proof of a pathfinding cause.
- Loss2bcc768849540be3454ab4d05688cf0a97c1577f4ffb229e6b8a2c1d2002f233,
  A/00ambush, same source: tribute583/1013, collection915/1101, own bag loss207,
  carried125. Multiple bottlenecks remain; kills15/5 did not win the objective.
  Full compact summaries saved under29487e01-summary.json and2bcc7688-summary.json.
- All six frozen opponent file sets verified against manifest9ef7d19b. Relevant
  boss ea15ef0f/sourcef4b4f65e uses reachable distances, risk budgets, shared claims,
  Vendetta/Varg/Ryth, local-power combat and30-gem banking. Beta7cab9b0f uses
  Varg/Tavi/Ryth, reset farming and staged defensive items. Imported the reachable
  distance principle independently; retained our roster/soft-risk policy and
  private routes. Opponent source predicts policy, not observed runtime events.
- Alternatives deferred: repeating harder camp vetoes (prior negative finding),
  delivery-cost ranking (prior inconclusive), or live claims without evidence of
  duplicate work. Historical detail is in archive/task-423449f15111476db311d689ef85b218.md
  and older archives. No claim that topology alone explains the measured losses.

## Candidate policy and contracts

- Retain measured melee vertical slice: Varg/Vendetta/Ryth/Marcella/Heart;
  legal resets and abilities, completed captures, Jungle Strength then Monster
  Strength then Durability Health then Power Strength,150/300-gold safe shop
  recall,40%HP retreat,98%spawn-heal wait,24-gem/near/winning/deadline tribute.
  Ordinary damage does not cancel tribute; preserve active channels.
- First draft encodes GA/version1/count16/xy8 static anchors, max509 groups,
  <=1023/1024 bytes. Cache anchor coordinates before sorting to remove repeated
  camp-member queries in the comparator. Live eight-byte memory remains unused.
- Cache a static altar field once. Near-bank/deadline decisions use reachable
  walking distance instead of Chebyshev distance; unreachable altars cannot
  trigger the normal bank branch. Actual moves still exclude visible occupants.
- Refresh a private source-rooted static distance field after4 topological tiles
  or12 rounds, only with>=65k fuel. Cache one distance per anchor; nearest-eight
  shortlist and route scoring use topology. A lower bound combines geometric
  distance with old distance minus topological displacement. Disconnected routes
  stay excluded only while in the same component; recall/respawn component
  changes invalidate the cache. Missing cache falls back to geometry.
- Existing45k planning floor and18k movement entry floor remain. No new all-map
  group scans in gameplay. Preserve a valid committed target if planning runs
  out of headroom. With no reachable work, deliver a small reachable bag before
  recovery. Bounded100-turn logs now include position and route-cache age.
- Regression assertions cover unreachable preservation, uninitialized fallback,
  topological displacement and geometric lower bounds, alongside prior memory,
  tribute and value invariants. Reviewed actual SDK DistanceField contracts.
  Documentation unchanged; no full unchanged export reread required. Engine3.0.5,
  lockac2b5ad2, suitepublished-40-release-305-v1; SDK894229e17d886358.
  RESEARCH/organizer ledger limits remain; download hub is not full policy review.

## Validation and next action

- Final bot-check --owner-config /var/lib/battlecode-volume/config/gamma.json
  PASSED exit0; exact source54c19acff8fb33174a4a428e37eb86c925b0de461514ebc2cc990ab23a7930e6.
  Report .agent/check-task-93a56bca32614c11b13bb0bc448670dd.json;
  check-report saved reachable-final-diagnostics.json. Initial97049a68 also
  passed; reachable-initial-check.json preserves that superseded report.
- Final smoke0c7c1562, sideA: completed round977, tribute1008/52.
  Final smoke0dcbf59c, sideB: completed round940, tribute1001/12.
  Both sides zero faults and suspensions in both games; same41x41 map hash
  6e3c67956080f8da5a0042e68ea481189cd6f61061a742a8be0354a9ea5c5620.
  Engine1.0.3/fcb6c3e8. Map name and opponent revision unknown. Saved full
  summaries reachable-final-smoke-a.json and-b.json. Validity, not broad strength.
- git diff --check PASSED. No source edits after final trusted check.
  Exact file hashes, provenance and final diagnostics: reachable-evidence.json.
- Risks: static distances ignore congestion; stale estimates can misrank nearby
  camps; extra fields need large-map fuel coverage; no crystal island routing;
  no live claims; existing safety/PvP and hostile-lock detours remain imperfect.
  Smoke does not test all these conditions or isolate routing's causal gain.
- Next: supervisor evaluates exact checked source against edit base and previous
  candidate on matched maps/sides/opponents, retaining all promotion gates.
  Prioritize corridors/islands/obstructed routes, submitted gems and suspensions;
  inspect actual route logs before deciding on claims, crystal travel or safety.
