# Gamma operational notes

## task-9406d58abd0e4f0e8ccc42430d074465 — expiring camp intents

- Refinement; bot/gamma, HEAD/input537e8fc37f395dcf4aef54c64dbe8d93411b9964.
  Edit f01d496cbc5028475ceda1b5ac558e10056b2175/source
  54c19acff8fb33174a4a428e37eb86c925b0de461514ebc2cc990ab23a7930e6.
  All seven starting files matched this edit commit. Prepared source differences
  from HEAD are intentional restoration, not unfinished work. Latest supplied
  evaluation is completed; none awaiting evaluation. Protected champion1a0675ca
  is separately preserved. Previous notes archived under task-0500e89ad682455e88f990b59ecd33a9.
- Hypothesis: soft expiring camp intents on the current topology-aware farmer
  increase matched wins AND mean tributed gems over the edit base, reduce duplicate
  opening targets, and introduce no own faults or fuel suspensions. Nonpositive
  win/tribute gain, unchanged duplication, or new reliability failures falsifies it.
  Duplication is observed on the later Tavi source; a causal gain on this Ryth
  edit base is UNMEASURED. This is one coordination experiment, not a roster change.

## Evidence and decision

- Latest evaluation96cb2190, commit537e8fc3/source6b27b8a7: INCONCLUSIVE,
  325W/75L overall, zero faults. Development301W/69L, matched delta+0.0216216
  over edit base across185 side pairs. Not a test of today's edited source.
- Loss9ec60cd9f1ad931743045fe56989261d7c624bfa480fb382f45a3c69b08dfe6d,
  B/00ambush per trusted brief, later source6b27b8a7: completed2000,
  tribute506/845, collected692/862, bag loss153/17, deaths4/31;
  own faults/suspensions0/0, opposing0/23. Saved refine-ambush-summary.json.
  Its own first-page runtime logs explicitly show ALL FIVE r1 farmers selecting
  target4; at r101 two pairs still share target10 and target2. Saved bounded
  r= lines in refine-ambush-log.json. This proves shared targets, not idle time,
  path blockers, or a causal explanation of the loss. Opponent revision UNKNOWN
  in these slices; don't infer it from roster similarity.
- Lossb9bafeb4c03cf9a68b4878591722c08addf3e1eced1f747335ef5e23b9a7c252,
  A/00collision per brief, same later source: completed1392, tribute973/1017,
  collection1200/1116, bag loss161/99, carried66/0, deaths14/6;
  own faults/suspensions0/0, opposing0/1. First two own r1 farmers share target5;
  third selects7. Full refine-collision-summary.json and bounded -log.json saved.
  Two maps/sizes and different rosters exhibit duplication. Finals also show
  bag-loss/recovery weaknesses; this candidate does not claim to solve them.
- Contrasting exact-base validity wins remain reachable-final-smoke-{a,b}.json:
  A1008/52, B1001/12 tribute, zero faults/suspensions; map hash6e3c6795,
  map name/opponent revision unknown. No controlled strength inference.
- Frozen manifest ae308f96 and all6 source file sets hash-verified. Inspected
  boss4feab379/ea15ef0f/sourcef4b4f65e: Vendetta/Varg/Ryth, shared target
  claims, risk budgets, local-power skirmishes,30-gem banking, spawn shopping.
  Beta054bc346/7cab9b0f/sourcefd5e2554 uses Varg/Tavi/Ryth and visible-ally
  proximity penalties; independent farmers cannot coordinate unseen targets.
  Adapt only soft intent coordination, retaining gamma's macro/roster/build.
- Earlier intent trialce3692cb on source3ce565f6, engine2.1.6, was not selected;
  it had no observed duplication trace and supported only63 groups. Current
  rationale adds actual duplicate-target logs and a different topology-aware
  edit base; current packet covers all509 draft routes with a softer penalty.
  Prior negative claims, combat, corridor clearing, gem repricing and dash
  experiments remain archived; no evidence that coordination must improve wins.

## Candidate policy and bounds

- Retain Varg/Vendetta/Ryth/Marcella/Heart; Jungle Strength -> Monster Strength
  -> Durability Health -> Power Strength; reachable shortlist/cache,24-gem/
  near/winning/deadline tribute,40% retreat,98%spawn healing, capture occupancy,
  legal attacks/resets, existing movement and intentional dispatcher yield.
- camp_intents.h protocolD uses EXACTLY8 live bytes: low4bits versionD, then
  five12-bit records. Each record has9bits route index+1 (0 releases) and
  3bits round modulo8. Immutable actual roster slot owns its record. Disable
  coordination for >5 bodies, empty/>509 routes, or insufficient memory; unknown
  versions are untouched. Canonical indices come from unchanged draft-v1 anchors.
- Before early exits, clear own prior intent; only farm/capture republish.
  Each publish rereads current8bytes and commits one8-byte SDK write preserving
  peers, with>=10k fuel. No snapshot survives planning into a later write.
  Cached peer hints are used only for this turn's scoring. No ally hidden live
  state or shared vision is read; claims never assert group visibility/state.
- Accept modulo age<=1 AND <=1 round since locally observed token change.
  Abandoned unchanged records cannot revive on modulo wrap. An old record first
  seen during a matching stamp can appear fresh for at most2 observations.
  Changed heartbeat recovers after skipped observations; releases invalidate.
- Divide existing route score by(1+fresh other intents). This is soft, so a rich
  shared camp can still beat poor alternatives. Existing visible collector
  reservations, affinity, hysteresis and ally proximity penalty remain.
- No added route scans/path fields: read five peer records and count <=5 per
  scored camp. Bounded logs add peers for selected target. Compile-time checks
  cover packet boundary, largest route/last slot, peer preservation on release,
  unknown versions, age/wrap/abandoned record expiry and soft cooperation.
- Consulted playbooksB/C/D/E/F/G, reference, memory/capture/items rules and the
  installed C++ shared_memory read/write/size contracts. Unchanged review handoff
  applies: SDK894229e1, CLI3.0.5, engine1.0.3/fcb6c3e8, lockac2b5ad2,
  suitepublished-40-release-305-v1. Organizer hub is not full policy review;
  official production parity remains unverified.

## Validation and next action

- bot-check --owner-config /var/lib/battlecode-volume/config/gamma.json PASSED,
  exit0, exact source5306ecd5b5716d22f434b3767a20178b9989e77f53a0d9d8f01041884354823d.
  Report.agent/check-task-9406d58abd0e4f0e8ccc42430d074465.json; canonical
  check-report saved as intents-check-response.json. No source edits afterward.
  Packet/expiry/scoring static assertions compiled in this trusted check.
- Smoke47d7164e, sideA: completed round1032, tribute1000/131; smokedfa48dac,
  sideB: completed round879, tribute1023/55. Both sides zero faults/suspensions;
  own deaths/bag loss0 in both. Full summaries intents-smoke-{a,b}.json.
  Map41x41/hash6e3c6795, engine1.0.3/fcb6c3e8; map name and opponent source
  UNKNOWN in smoke slices. Validity only; no claim of matched superiority.
- Own r1 targets are5/7/2 in A and5/8/2 in B, demonstrating distinct opening
  intents in these smoke games. Saved first-page r= lines in
  intents-smoke-log-{a,b}.json. These are not the supplied loss inputs, and
  diversity alone does not establish gain. Lowest sampled running fuel4731;
  fuel below10k skips publication and leaves the earlier release in place.
  All-map fuel headroom and capture efficiency remain unmeasured.
- git diff --check PASSED. Exact file hashes, decision, provenance and actual
  compact smoke metrics saved in intents-evidence.json.
- Risks: splitting loses cooperative clear speed or combat protection; expiry
  can briefly over/understate intent; a peer can change course after this body's
  snapshot; extra SDK memory calls consume fuel. Soft scoring and normal fallback
  stay legal even if hints are wrong. Opening target diversity is only a proxy.
- Next: supervisor evaluates exact checked source against edit base, accepted
  champion and frozen opponents under unchanged gates. Compare matched wins,
  tribute, collection, opening target diversity, deaths/bag loss and reliability.
  Include crowded openings and large maps; do not promote from smoke wins.
