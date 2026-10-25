# Gamma operational notes

## task-0500e89ad682455e88f990b59ecd33a9 — field-shopping third farmer

- Refinement, bot/gamma; input/HEAD ad033b46b172d4c9619952ac9357b264b91904d9.
  Edit f01d496cbc5028475ceda1b5ac558e10056b2175/source
  54c19acff8fb33174a4a428e37eb86c925b0de461514ebc2cc990ab23a7930e6.
  All seven starting files matched the trusted edit commit. Prepared three-file
  differences from HEAD were restoration, not incomplete work. Latest own
  evaluation completed; none pending. Accepted1a0675ca remains separately saved.
  Prior notes preserved in archive/task-41dc196439b045f6aeb4f903bbf275a8.md.
- Hypothesis: third-pick Tavi with immediate field reinvestment increases matched
  wins AND mean submitted gems over the edit base without new own faults or fuel
  suspensions. Nonpositive gains or new reliability failures falsify it.
  This is an UNMEASURED rules/source deduction, not a traced Ryth failure.

## Evidence and decision

- Latest evaluation38bc63e2, ad033b46/source36bf1ed3: INCONCLUSIVE,313W/87L
  across400 games, zero fault matches. Development-only287W/83L; matched
  development delta -0.0162162 versus this edit base over185 side pairs.
  Dash continuation was not selected. These are NOT this candidate's results.
- Loss03e08648, B/01corridors, that later source, vs6af1685b/source87b9be45:
  completed2000, own tribute551 vs743, collection968 vs809, bag loss315 vs58,
  deaths29 vs35; both sides zero faults/suspensions. Own Ryth collected42,
  submitted0, died6; Vendetta298/242/4, Marcella242/111/3. Stored full compact
  summary in refinement-corridors-summary.json; first-page own logs retained
  with literal zero padding removed in refinement-corridors-log.json.
- Loss0ad1e1cd, B/01concentrated-wealth, same later source, vs boss
  ea15ef0f/sourcef4b4f65e: completed2000, own tribute883 vs891, collection981
  vs977, bag loss61 vs71, deaths15 vs16. Own faults0/suspensions1, opposing
  faults0/suspensions3. Ryth28/28/4, Vendetta401/379/1, Marcella276/241/2
  for collected/submitted/deaths. Full refinement-wealth-summary.json retained.
  Low Ryth contribution occurs in both losses; totals do not explain its cause.
- Counterevidence: exact-base smoke wins0c7c1562(A),0dcbf59c(B), saved in
  reachable-final-smoke-{a,b}.json, have Ryth353/327 and364/364 collection/tribute,
  zero own deaths. Replacing Ryth can sacrifice a strong farmer on easy maps.
  Those opponents' sources/map names are unknown; no matched strength inference.
- All6 frozen file sets verified against manifestf397e84a. Beta7cab9b0f/
  fd5e2554 drafts Varg/Tavi/Ryth and runs staged Jungle/Monster/Durability/Power
  buys each turn, excluding Tavi from shopping recall. Adapt this field-shop role
  to our strongest first two melee picks; preserve our macro, build and routes.
  Boss ea15ef0f uses melee farming, risk budgets, shared claims and local-power
  combat. Opponent code predicts policy, not runtime events in these losses.
- Deferred repeating generic combat ranking, reset retargeting, dash continuation,
  contact farming, corridor banking and shared claims after negative/inconclusive
  findings. This integrated roster/economy trial changes the third farming role.

## Candidate policy and safety

- Draft Varg/Vendetta/Tavi/Marcella/Heart; Ryth is the sixth fallback. Legal
  map-dependent3–5 picks retain draft-v1 static anchors, no live memory writes.
- Tavi buys existing Jungle Strength, Monster Strength, Durability Health then
  Power Strength in ordinary field turns whenever at least one shard is affordable.
  Each purchase uses can_buy; consumables keep its separate spawn/dead restriction.
  Already active channels are preserved. Dead and spawn shopping remain intact.
- Exclude field shoppers from gold-only recall. Health recovery still runs after
  field buying, using the actual post-purchase health/max_health ratio. Field
  Health does not heal; no max-HP increase is treated as recovered health.
- Existing fight/walk can_* checks handle ranged movement/basic exclusivity.
  Retain capture occupancy, refreshed post-move observations,24-gem/near/winning/
  deadline banking,40% retreat,98%spawn healing and bounded fuel fallbacks.
- Four compile-time invariants cover field-shop recall exclusion and ordinary
  149/150/300-gold thresholds. Private cumulative field_spent records actual gold
  spent outside spawn. It consumes no shared bytes and appears in bounded logs.
- Consulted compact reference, playbooksB/C/D/E/F/G, Tavi/items rules and installed
  C++ can_buy/buy contracts. Unchanged full-review handoff applies: SDK894229e1,
  CLI3.0.5/engine1.0.3-fcb6c3e8, lockac2b5ad2, suitepublished-40-release-305-v1.
  Organizer hub is not complete policy review; no official production-parity claim.

## Validation and next action

- bot-check --owner-config /var/lib/battlecode-volume/config/gamma.json PASSED,
  exit0, exact source6b27b8a760a54cc853439416e4a3b34fa930a36ee860f1506f883dbe28898ddb.
  Report.agent/check-task-0500e89ad682455e88f990b59ecd33a9.json; canonical
  check-report saved in field-shop-check.json. No source edits after check.
- Smoke20f3d8fc, A: completed round942, tribute1032/52; Tavi262 collected,
  251 submitted,0 deaths. Smokee9bc02e0, B: completed round904, tribute1053/26;
  Tavi368 collected/submitted,0 deaths. Both sides zero faults/suspensions in
  both games. Full summaries: field-shop-smoke-{a,b}.json. Map41x41/hash6e3c6795;
  map name and opponent source unknown. Validity only, not broad strength.
- First smoke log shows field_spent120 by round201, proving field purchases
  actually executed. Bounded sample retained in field-shop-smoke-log.json;
  these samples do not prove all-map fuel headroom or a causal throughput gain.
- git diff --check PASSED. Exact source hashes, decision, provenance and limits
  saved in field-shop-evidence.json.
- Risks: Tavi has lower starting HP, trades movement for ranged basics, and may
  enter capture later. Field Health can trigger recovery; Ryth's area control
  and reset are lost. The existing macro can still stall or lose carried bags.
- Next: supervisor compares the exact checked source with edit base, accepted
  champion and frozen opponents under unchanged gates. Compare matched wins,
  tribute, third-pick collection/deaths, recovery, field_spent and reliability;
  include cramped maps and easy-map regressions. No promotion from smoke wins.
