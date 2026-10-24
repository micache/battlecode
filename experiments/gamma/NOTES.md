# Gamma operational notes

## task-6acb6427618146c2a60cd1af13ff649f — post-bootstrap gem priority

- Refinement; task/bot/branch verified against entry and task envelope.
  HEAD/input3849da5ee90f759b23b4369a46efeda8e7ace430 deliberately differs
  from edit commitf01d496cbc5028475ceda1b5ac558e10056b2175/source
  54c19acff8fb33174a4a428e37eb86c925b0de461514ebc2cc990ab23a7930e6.
  All seven starting source files matched that edit commit byte-for-byte.
  The prepared three-file working diff was the trusted edit-base restoration,
  not unfinished work. Prior banking candidate was evaluated, not pending.
  Protected champion1a0675ca881d4b67cb5c6cb1822ce2ae1602dc4d untouched.
- Hypothesis: reducing gold's route value after both farming emblems, while
  reserving shortlist slots for gem camps, increases matched wins and mean
  tribute over source54c19acf without new faults or fuel suspensions.
  Non-positive win/tribute change or a new reliability failure falsifies it.
  Expected mechanism: fewer post-bootstrap gold-only captures and more gems
  collected per round. This is an unmeasured rules/source deduction.

## Evidence and decision

- Latest evaluationb7769b1c, commit3849da5e/sourcee17f373d, INCONCLUSIVE,
  335W/65L overall. Development370 games:311W/59L, mean collection940.88,
  tribute841.19, gold6031.79, deaths8.62, bag loss69.15, own faults0,
  suspensions0.0189. This evaluates the later banking experiment, NOT today's
  source. Matched development delta over today's edit base was+0.04865;
  it remains unselected as edit base. Do not infer a promotion from that delta.
- Supplied losses4413971d andc941775e: A/00collision, sourcee17f373d,
  completed games, own faults/suspensions0. Full compact summaries saved as
  gem-priority-<match-prefix>.json. Boss loss08109019: B/01shortcut, same
  candidate revision, tribute801/1014. Collision4413971d had similar earned
  gold5250/5342 but collection740/1048 and tribute427/1011; c941775e had
  collection754/1076, tribute471/1065. In contrast this revision won10/10
  development games on00great-wall. Totals do not prove gold overfarming.
- All six frozen source sets verified against manifestd9427d98.
  Beta054bc346/sourcefd5e2554 uses a soft gold-only opportunity penalty after
  300 capital; retained that principle rather than its additive score or draft.
  Boss4feab379/sourcef4b4f65e uses shared claims, reachable fields, risk budgets,
  Vendetta/Varg/Ryth and30-gem banking; its scoring still values gold by round.
  Alpha7c9eeed0 uses arrival-aware respawn observations, not incorporated here.
  Opponent source predicts policy; it is not measured evidence of its success.
- Current source valued gold at full weight before900 regardless of equipment;
  nearest-eight shortlist could hide farther gem camps even after repricing.
  Coupling draft reward metadata, shortlist admission and scoring addresses
  both policy layers. Gold remains useful for upgrades and the deadline tie.
- Deferred: latest corridor clearing/lock changes are not automatically merged
  from HEAD; their aggregate gain did not establish promotion. Earlier delivery
  cost, claims and combat experiments remain negative/inconclusive in archives.
  Items/draft roster/respawn policy are held to the trusted edit source.

## Candidate policy and contracts

- Keep Varg/Vendetta/Ryth/Marcella/Heart, existing resets, capture completion,
  Jungle Strength -> Monster Strength -> Durability Health -> Power Strength,
  40% retreat,98% spawn healing and24-gem/near/winning/deadline banking.
- Actual possession of BOTH Jungle and Monster Strength emblems activates
  developed economy; opening score is unchanged. Thereafter multiply gold's
  existing time weight by0.20; gems keep5x weight. No hard gold-only veto.
- Reserve four of the existing eight shortlist slots for nearest reachable,
  ready gem-bearing routes; fill other slots with nearest work of any kind.
  Existing committed-target and rotating-probe additions,45k planning/18k
  action fuel floors and static route-distance cache remain. Evaluation count
  stays bounded as before, although cheap shortlist bookkeeping increases.
- Draft GA/version2 retains u16 count and xy8 anchors, adding a packed immutable
  gem-reward bit per group. At<=479 groups the full packet fits1024 bytes;
  above479 omit all reward bits and retain all up-to509 anchors. Decoder accepts
  v1/missing metadata conservatively; unknown groups stay gem-eligible until
  lazy static group loading refines them. No hidden live state encoded/read.
  All live8 shared bytes remain unused; no ownership/expiry protocol needed.
- Compiled assertions cover packet limit/bit boundaries, no anchor truncation
  for missing metadata, unchanged opening reward ranking, developed gem-vs-gold
  ranking and positive late gold fallback. Relevant playbooks B/C/E/F and current
  reference/API/installed C++ static reward and memory contracts consulted.
  SDK894229e17d886358, engineCLI3.0.5/lockac2b5ad2, suitepublished-40-release-305-v1.
  Unchanged-document handoff supplies prior full review; organizer hub is not
  a complete event-policy review, and official runtime parity remains unverified.

## Validation, risks and continuation

- bot-check --owner-config /var/lib/battlecode-volume/config/gamma.json PASSED,
  exit0, exact source286bac8e6473584f8a5c3a3ab581f7f2045e3c2062a6a96e2bf8d3b0160e5b81.
  Report.agent/check-task-6acb6427618146c2a60cd1af13ff649f.json;
  canonical check-report copied to gem-priority-check.json. No source edited
  after this check. Static regression assertions compiled in this trusted build.
- Both wrapper smoke games completed, zero faults/suspensions on BOTH sides.
  4be40210: terminal round995, tribute A1059/B56; 03b723e0: round917,
  tribute A8/B1001. Saved full summaries gem-priority-smoke-a.json and-b.json.
  CLI3.0.5; reported engine1.0.3/fcb6c3e8;41x41/hash6e3c6795. Smoke map name
  and opponent revision unknown; wrapper order suggests own A/B respectively,
  but summary does not independently identify candidate side. Validity only.
- git diff --check PASSED. Source identities, frozen manifest verification,
  decision and regression limits saved in gem-priority-evidence.json.
- Risks: lower gold investment can slow scaling; distant gem camps can displace
  safer nearby work; gem slots can increase travel/contested farming; extra
  shortlist work may affect fuel on large maps. Soft risk scoring is unchanged.
  Missing reward metadata weakens shortlist specialization but remains playable.
- Next: supervisor compares the exact checked candidate with source54c19acf
  and protected champion under unchanged gates. Prioritize wins/tribute, then
  post-core gold-only capture share, collection rate, travel, deaths and fuel.
  No comparative games run by this worker; smoke validity cannot show strength.
