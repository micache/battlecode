# Gamma operational notes

## task-58e82cb0b7da4e89a80dcbea445560b6 — bounded conversion before recovery

- Exploration; bot/gamma; HEAD/input62111c7210dd10e58f0ab4c1384ad9dcc8e7dce1.
  Edit f01d496cbc5028475ceda1b5ac558e10056b2175/source
  54c19acff8fb33174a4a428e37eb86c925b0de461514ebc2cc990ab23a7930e6.
  All seven starting files matched edit commit; camp_intents.h was already
  absent in this prepared edit base. Dirty differences from HEAD are intentional
  restoration. Accepted champion1a0675ca remains preserved outside this edit.
  Latest supplied evaluation is complete, not awaiting evaluation. Prior notes
  preserved in archive/task-9406d58abd0e4f0e8ccc42430d074465.md.
- Hypothesis: bounded safe conversion before recall increases matched wins AND
  mean tribute over the edit base, without increased mean bag loss or new own
  faults/fuel suspensions. Nonpositive gains or either regression falsify it.
  Recovery's causal effect is an UNMEASURED source/rules deduction. One new
  recovery policy; not an attempt to repeat previous bank-risk or combat tuning.

## Evidence and decision

- Evaluation51b8638f, candidate62111c72/source5306ecd5, INCONCLUSIVE:309W/91L,
  zero faults overall. Development289W/81L, matched delta-0.01081081 over this
  edit base across185 side pairs. The expiring-intent source was not selected as
  this task's edit base. Its results do not evaluate the new code on disk.
- Loss a61d762a50453f5c2d55e138fa2439d8f2540edb630eba1f4dc336735f6b015a,
  B/00ambush, that later source: completed round1826, tribute717/1029,
  collected995/1066, own carried125, bag loss153, deaths4, own faults/suspensions
  0/0 (opposing0/27). Ryth finished with51 carried/33 tribute, Marcella37/107.
- Loss5151405e9b28cf1583796afd2a0e6758ff882bf2d2a8480a9c0c4e0479233709,
  B/00collision, same later source: completed1298, tribute787/1003, own
  collection920, bag loss133, deaths19, faults/suspensions0/0 on both sides.
  Own r205 log explicitly shows heal hp360 gems15 at3,39. This establishes a
  wounded carrier on spawn, not its route, cause, or a safe alternative bank.
  Opponent revisions UNKNOWN in these slices. Full compact summaries saved as
  explore-{ambush,collision}-summary-full.json; bounded log lines saved separately.
- Contrasting exact-base validity wins: reachable-final-smoke-{a,b}.json,
  tribute1008/52 and1001/12, own zero deaths/faults/suspensions; rounds977/940.
  Map hash6e3c6795; map name/opponent revisions unknown. Not controlled strength
  evidence. Finals show both conversion and combat weaknesses, not a sole cause.
- Frozen manifest2c8433f4: all six file sets hash-verified. Inspected shared boss
  4feab379/ea15ef0f/sourcef4b4f65e: Vendetta/Varg/Ryth, shared claims, risk-budget
  camp scoring, favorable-power skirmishes,30-gem banking, spawn shopping.
  Its low-health retreat precedes banking. Beta054bc346/7cab9b0f/sourcefd5e2554
  uses Varg/Tavi/Ryth, Jungle/Monster/Durability/Power, reset farming, and also
  prioritizes recovery before banking. Source policy is not runtime evidence.
- Chosen departure: briefly convert already cleared/carried value before healing,
  instead of carrying every small bag through recall, spawn healing, and a second
  outward journey. Preserve the recovery latch after conversion. Do not chase,
  start another clear, or reroute the healthy farmer. Earlier generic combat
  ranking, protected transit, claims and threat-aware bank routing were negative
  or inconclusive; their notes remain archived. No causal gain claimed here.

## Policy and engineering bounds

- Retain Varg/Vendetta/Ryth/Marcella/Heart, existing items,24-gem/near/deadline
  normal bank, topology cache, capture/respawn,40% retreat,98% spawn healing,
  resets/dashes, action floors, no live shared memory, and dispatcher yield.
- On entering a low-health recovery episode, set one private deadline now+12.
  Never renew while recovering; abort permanently on unsafe/no feasible work,
  insufficient fuel, or below20% HP. Spawn recovery/death clears episode state.
- Before dropping the old target, retain an already occupied, visibly cleared
  camp only outside modeled danger. No new camp travel/attack. Holding capture
  consumes the same12-round budget; remote contest can still waste this budget.
- With a bag, choose a free approach to a currently visible unlocked altar.
  Entire path lies in current own vision and outside terrain/visible occupants/
  teleport reservations/danger. Actual safe path length<=6; distance + tribute
  ticks +1 must fit remaining episode time. No hostile-lock attacks or detours.
- Danger uses visible living champions' max(5,range+base speed), and awake living
  camps' range+base speed. Visibility precedes live reads. Current observations
  only; no cached enemy live state or ally vision. Unknown reinforcements and
  sleeping camps that wake later remain risks, not guaranteed absent threats.
- At most16 awake camp observations; fail closed on more. Optional entry55k fuel,
  initial scan35k reserve. Rebuild danger after movement with24k reserve; abort
  further conversion if new danger or insufficient headroom. One path field and
  at most one ordinary move per turn; refresh locks/vision before submission.
  Hidden-blocker False gets a later replan under the same fixed deadline.
- Useful channels return early unchanged. Tribute completion deposits the whole
  bag; after completion the still-latched recovery resumes. No channel cancels.
  Bounded100-round logs cashout=A,B count capture-hold TURNS and submission STARTS,
  not completed captures/deposits. Pure compile-time regressions cover6-step/
  unreachable/empty-bag/deadline/tribute-budget and20%-health boundaries.
- Consulted reference/playbooksB/C/D/F/G; recovery/channel/items rules and matching
  C++ state, camp, field and submission contracts. Unchanged review applies:
  SDK894229e1, CLI3.0.5, lockac2b5ad2, suitepublished-40-release-305-v1.
  Organizer download hub is not full policy review; official parity unverified.

## Validation and next action

- Initial trusted bot-check PASSED exit0/source946103e34ac17e866dd5bf186900704c22c59e777f22dbb0bdc9f9af0195ab88.
  Saved recovery-cashout-initial-check.json. Superseded by the bounded refreshed
  danger scan added after review of optional-branch fuel headroom.
- Final bot-check --owner-config /var/lib/battlecode-volume/config/gamma.json
  PASSED exit0, exact sourcedef166c7afa2500d509dc32e959254aeeac2c5cc81d4525aca86a819fe74695a.
  Report.agent/check-task-58e82cb0b7da4e89a80dcbea445560b6.json; canonical
  response saved recovery-cashout-check-response.json. Static assertions compiled.
  No source edits after this final trusted check.
- Final smoke952f0c67 sideA: completed977, tribute1008/52; smoke116823f0
  sideB: completed940, tribute1001/12. Both sides zero faults/suspensions,
  own deaths/bag loss0 in both. Full recovery-cashout-smoke-{a,b}.json saved.
  Same41x41/hash6e3c6795, engine1.0.3/fcb6c3e8; map name and opponent revision
  UNKNOWN. These final aggregate metrics equal the old base smokes; no gain
  measured. First/last-page sampled logs show cashout=0,0 through rounds909/903; actual
  positive-branch coverage is not established. A B r901 recover log still has
  hp263/gems23, so conversion is deliberately conditional, not guaranteed.
  New-policy all-map coverage remains unknown.
- git diff --check PASSED. Exact file hashes, attributed losses, contrasts,
  final check and smoke metrics are in recovery-cashout-evidence.json.
- Risks: deferred healing can expose a wounded body; masks only model visible
  one-step threats; interrupted tribute can use the remaining budget; conditional
  cash-out branches need broader-map fuel coverage. Smoke is validity only.
- Next: supervisor evaluates exact checked source versus edit base, accepted
  champion and frozen opponents under unchanged gates. Compare matched wins,
  tribute, bag loss, deaths, wounded-carrier turnaround and reliability; use new
  counters to identify actual branch exposure. No promotion from smoke games.
