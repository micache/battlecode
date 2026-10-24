# Gamma operational notes

## task-79ea9383992346ad9b2f7d7b0474cc11 — banking through occupied corridors

- Refinement; branch bot/gamma; clean HEAD/input/edit commit f01d496cbc5028475ceda1b5ac558e10056b2175,
  source54c19acff8fb33174a4a428e37eb86c925b0de461514ebc2cc990ab23a7930e6.
  All seven edit files verified against feedback.handoff. Protected champion
  1a0675ca881d4b67cb5c6cb1822ce2ae1602dc4d remains outside this edit transaction.
- Prior task93a56bca is published and evaluated, not awaiting evaluation. Its
  notes are archived under archive/task-93a56bca32614c11b13bb0bc448670dd.md.
  Historical d684842d recovery remains preserved; no incomplete patch on entry.
- Hypothesis: progress-aware banking that clears visible corridor camps and
  retains reachable locked altars increases matched wins and mean tribute over
  f01d496c, reduces extended banking stalls, and adds no faults/suspensions.
  Non-positive win/tribute gains or new reliability failures falsify it.

## Evidence and decision

- Evaluation6cb05e4b, exact edit source54c19acf: INCONCLUSIVE,316W/84L across400
  games. Development370 observations: collection882.09, bag loss68.19,
  carried33.96, tribute779.94, deaths8.35, own faults0, suspensions0.0162.
  Champion promotion is not established.
- Boss lossfb29d6e2c7d1b3dfca5b270b748116204f47088c88bc0c9bc8ff9cb1ab7d2c62,
  B/01the-farm, f01d496c/source54c19acf against boss ea15ef0f/sourcef4b4f65e:
  completed2000, tribute92/229, collected216/338, carried95/109, deaths1/0.
  Own faults0 and suspensions0; opposing suspensions9. Engine reports1.0.3/
  fcb6c3e8; task CLI3.0.5/lockac2b5ad2. Preserve that version distinction.
- Its bounded runtime logs show r1548 Vendetta bank37 at31,15; r1648/r1748
  bank37 at29,15. Two other carriers log bank29 at29,14 and30,17 unchanged
  r1601/r1701/r1801. This establishes long bank-mode stalls with retained bags,
  not exact camp/lock causality. Saved initial/late log slices and summary.
- Source deduction: bank() always returned after movement, never attacked a
  blocking camp, and removed all locked altar goals whenever any unlocked
  altar existed (without reachability validation). Dynamic movement cannot
  pass through living camps. The proposed cause remains unmeasured.
- All six frozen opponent file sets verified against manifest2d7f4a75.
  Boss4feab379 uses Vendetta/Varg/Ryth,30-gem banking, nearest static altar
  field, lock attacks, shared claims, local-power combat and bounded detours.
  Alpha7c9eeed0 places locks and prefers unlocked goals; beta054bc346 softly
  penalizes gold-only work after300 capital. Opponent source predicts policy,
  not runtime events. Borrowed nearest-altar principle, not the whole strategy.
- Rejected/deferred: changing roster/items or adding harder camp vetoes would
  not directly address the observed bank loop. Prior hard camp veto regressions,
  delivery-value inconclusive evidence and earlier failed candidates remain in
  archived notes. Do not interpret those older results as tests of this patch.

## Candidate contracts

- Retain measured Varg/Vendetta/Ryth/Marcella/Heart farming, draft v1 static
  anchors, reachable camp shortlist, capture completion, items and recovery.
  Live shared8 bytes remain unused; all new progress state is instance-private.
- Bank toward the union of all static altar approach tiles, accepting five
  hostile-lock hits instead of globally excluding a potentially reachable bank.
  Existing fresh arrival tribute and active-channel preservation remain intact.
- Track best static bank distance and last improving round. After4 rounds
  without net improvement, inspect visible camps within5 tiles. Accept only
  camps closer to a bank on a shortest corridor or one-step detour, with a free
  attack approach reachable within5 under refreshed visible blockers. Select
  nearest, then lowest HP. Never use hidden live state or allied bodies as targets.
- Reuse existing attack/reset/spell handling with an explicit optional obstacle
  target, refresh visibility/health after attacks and movement, and shield while
  clearing. Ordinary farming still uses its own group target. If no eligible
  obstacle exists, try in-range enemy defense, then normal bank navigation.
- Progress resets after submission/death/nonbank work.100-round logs include
  bank_stall. Existing45k planning and18k action fuel floors remain unchanged.
  Static assertions cover corridor eligibility, behind/off-route camps and
  unreachable origins; built with the trusted wrapper, not a host compiler.
- Current docs/SDK unchanged according to trusted handoff. Consulted relevant
  playbooksB/C/D/F, reference and installed C++ declarations. Prior full review
  applies. RESEARCH/organizer ledger still does not establish full event policy
  review or production parity; no official action authorized or performed.

## Validation and uncertainty

- bot-check --owner-config /var/lib/battlecode-volume/config/gamma.json PASSED
  exit0, sourcee17f373d5623d1494442e9eea12816db00487a9b50e1f6d4b5f846de4c16065b.
  Report.agent/check-task-79ea9383992346ad9b2f7d7b0474cc11.json; copied canonical
  check-report into bank-corridor-check.json. No source edits after this check.
- Smoke ccb23bea, sideA: completed valid terminal round987, tribute1053/52.
  Smoke e8976a82, sideB: completed valid terminal round940, tribute1001/12.
  Both sides have zero faults/suspensions in both games; map41x41/hash6e3c6795,
  engine1.0.3/fcb6c3e8. Smoke map name/opponent source unknown; this is validity
  evidence, not an evaluation against the boss or the-farm. Full summaries saved.
- Static assertions compile in that check; git diff --check passed. Exact file
  identities, decisions, evidence limits and provenance: bank-corridor-evidence.json.
- Additional loss1fe09d55, A/00collision, source54c19acf: tribute2/1006,
  collected213/1006, own carried118, bag loss93, no faults/suspensions.
  Lossf1b420d7, A/00ambush, same source: tribute651/1009, bag loss186.
  Contrasting win79a0887b: tribute782/759; exact candidate-side revision unknown
  in compact record, so do not attribute it to this source. Raw summaries saved.
  Multiple weaknesses remain; these totals alone do not explain individual turns.
- Risks: clearing a large monster costs HP/time; static corridor eligibility is
  approximate; allies or far blockers can still congest a bank; removing unlocked
  preference can expose carriers to hostile locking. Low-health retreat remains.
- Next: supervisor evaluates exact checked source against f01d496c and protected
  champion under unchanged gates. Prioritize the-farm and other narrow routes,
  bank_stall logs, submitted gems, deaths and fuel suspensions. Inspect actual
  path blockers if long stalls persist before changing thresholds or adding roles.
