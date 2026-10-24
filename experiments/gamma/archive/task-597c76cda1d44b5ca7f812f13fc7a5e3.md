# Gamma operational notes

## task-597c76cda1d44b5ca7f812f13fc7a5e3 — arrival-aware camp returns

- Refinement; task/bot/branch/input verified from task and entry. All seven
  starting files matched edit commit f01d496cbc5028475ceda1b5ac558e10056b2175,
  source 54c19acff8fb33174a4a428e37eb86c925b0de461514ebc2cc990ab23a7930e6.
  HEAD/input802263ae differs deliberately; the prepared four-file restoration
  was trusted edit-base preparation, not unfinished work. Latest candidate was
  evaluated, not pending. Protected champion1a0675ca untouched.
- Hypothesis: arrival-aware return planning with nonblocking staging increases
  matched wins AND mean submitted gems over source54c19acf without new own
  faults or fuel suspensions. Non-positive win gain, non-increasing tribute or
  new reliability failures falsifies it. Unmeasured rules/source deduction.
- Bottleneck: farm excluded every remembered respawning group until ready_at,
  even when travel exceeded the remaining cooldown. With no ready work it
  banked/recovered instead of positioning for a return. This source behavior
  is established; the supplied losses do not prove its cost in those games.

## Evidence and decision

- Evaluation029ae127, commit802263ae/source286bac8e, INCONCLUSIVE:311W/89L,
  zero faults. Matched development delta versus today's edit base -0.0081081
  over185 side pairs. Development mean collection888.28, tribute792.99,
  deaths8.23, bag loss65.33, suspensions0.0135. This evaluates the gem-priority
  experiment, NOT the restored source or this new candidate.
- Supplied completed losses: cf913e89, A/00ambush, source286bac8e: collection
  966/1072, tribute933/1035, deaths11/4, own faults/suspensions0. 1cad4a7f,
  B/00ambush, same source: collection1026/989, tribute746/938, bag loss229,
  own deaths8, faults/suspensions0. Full compact summaries retained under
  rotation-loss-<prefix>.json; opponent revision unknown in these summaries.
- Exact edit-base historical loss f1b420d7, A/00ambush, source54c19acf:
  tribute651/1009, collection837/1034, own faults/suspensions0. Contrasting
  completed archived win79a0887b has tribute782/759, but candidate side/source
  are UNKNOWN in the compact provenance; do not attribute it to the edit base.
  Existing routing-summary artifacts and bank-corridor-evidence.json retain
  these limits. Totals alone cannot diagnose cooldown-related missed turns.
- All six frozen file sets verified against manifest1405e3a0. Boss ea15ef0f /
  f4b4f65e prices cooldown after travel, uses claims, Vendetta/Varg/Ryth and
  30-gem banking. Alpha82a14a04/6e362fd7 uses group bounds and arrival-aware
  respawn eligibility. Transfer that timing principle with gamma's own route
  scoring and explicit off-spawn staging; do not clone composition or claims.
- Beta7cab9b0f/fd5e2554 soft-penalizes gold-only work after300 capital; current
  gem-priority experiment did not improve this base, so do not bundle it.
  Beta863825b7/c9c933a2 bounds frontier planning and caches plans. No roster,
  combat or search architecture transferred. Sources predict policies, not
  measured success. No opponent private worker state accessed.
- Alternatives deferred: repeat gem reweighting after its matched regression;
  target-aware combat previously unselected; another harder risk veto without
  new trace evidence. Arrival-aware staging was an explicit untried follow-up
  in archive/task-ff42f1f4a5724e2a898c2cea340c1a75.md.

## Candidate policy and contracts

- Retain Varg/Vendetta/Ryth/Marcella/Heart, current resets/shields, capture
  completion, Jungle Strength -> Monster Strength -> Durability Health -> Power
  Strength,40% retreat,98% spawn healing and24-gem/near/winning/deadline banking.
- Separate hard stuck deferral from uncertain respawn deadlines. Admit cooling
  routes with <=3 predicted wait rounds after arrival at attack approach.
  First move is THIS round after respawn phase: arrival delay=max(0,moves-1).
  Cached spawn bounding rectangles give a conservative distance lower bound;
  walls/congestion can only lengthen travel. No new distance fields or live
  shared bytes; retain GA/v1 immutable draft packet and existing route cache.
- Price residual wait in shortlist and route scores. Cooling groups use full
  design HP/strength, never the previous clear's dead handles as free reward.
  Fresh visible alive/reward observations clear the remembered deadline.
- For still-cooling groups, approach the outer one-tile ring. Block the entire
  group's spawn mask in pathfinding, including intermediate movement; allow
  leaving an occupied origin. Disable dash while staging. Reobserve after
  moving; require fresh visible alive/reward state before normal clearing or
  capture entry. Remembered deadline expiry alone never grants hidden state.
- Waiting on the ring increments existing stuck counter;8 stalled turns defer
  that route12 rounds. This bounds zero-timer waiting when another occupant
  blocks respawn. Never depart an existing uncontested capture for staging.
- Preserve moved status into combat after staging reveals a live camp, so an
  exclusive spell cannot follow walking. Planning floor45k/action18k remain;
  check shortlist fuel every16 entries even on excluded routes. Read self
  range/speed once per planning pass; route wait calculations are arithmetic.
- Relevant playbooks B/C/E/F, compact reference, installed C++ state/spawn-mask,
  movement, shift and stats contracts consulted. Seven compiled temporal
  assertions cover first-move/expiry/speed/zero-timer/immobile boundaries.
  SDK894229e17d886358, CLI3.0.5/lockac2b5ad2, published-40-release-305-v1.
  Unchanged-document handoff retains prior full review. Organizer download hub
  is not full policy review; official runtime/source parity remains unverified.

## Validation, risks and continuation

- bot-check --owner-config /var/lib/battlecode-volume/config/gamma.json PASSED,
  exit0, final source6c10372302c4821019cd43306b3b195c896f7e2f33dded12e6b38103f8cc85ad.
  Report.agent/check-task-597c76cda1d44b5ca7f812f13fc7a5e3.json; canonical
  check-report saved in rotation-check.json. No source edits after final check.
- Initial check also passed on source43c5762b; reports retained as
  rotation-check-initial*.json. Final rerun validates the later cached-stat
  and skip-independent fuel guard optimization. Assertions compiled in both.
- Final smoke21ec1370: completed round949, tribute A1006/B70;47b8f6fb:
  completed round889, tribute A23/B1007. BOTH sides zero faults/suspensions
  in both. Engine1.0.3/fcb6c3e8;41x41/hash6e3c6795. Map name/opponent revision
  unknown; candidate A/B follows wrapper ordering, not independent summary
  attribution. Full summaries: rotation-smoke.json. Validity only, no strength
  claim. git diff --check passed; exact source identities in rotation-evidence.json.
- Risks: waiting can displace immediately available work; other occupants can
  delay respawn; conservative geometric bounds omit useful topological returns;
  extra arithmetic/masks cost fuel. Large-map comparative performance unmeasured.
- Next: supervisor evaluates exact checked candidate versus edit base and
  protected champion under unchanged gates. Prioritize wins/tribute, collection
  rate, off-spawn waiting, repeated zero timers, deaths and fuel. If unsupported,
  inspect bounded return-choice traces before tuning wait allowance.
