# Gamma operational notes

## task-030af596030548ff86a766ff488f5dbc — bounded bank corridor reopening

- Refinement; bot/gamma; input/HEAD b852527faa1b52648ba415fd2dddb3828e1626c8.
  Edit f01d496cbc5028475ceda1b5ac558e10056b2175/source
  54c19acff8fb33174a4a428e37eb86c925b0de461514ebc2cc990ab23a7930e6.
  All seven starting source files matched edit commit; prepared three-file
  differences from HEAD were intentional restoration. Latest own evaluation
  completed; no unfinished candidate found. Accepted1a0675ca stays preserved.
  Prior notes archived as archive/task-58e82cb0b7da4e89a80dcbea445560b6.md.
- Hypothesis: bounded corridor clearing with all reachable altar approaches
  increases matched wins AND mean submitted gems over the edit base, without
  increased own faults or fuel suspensions. Nonpositive gains or either
  reliability regression falsifies it. Expect fewer extended bank stalls.
  The precise blocker mechanism remains a source/rules deduction.

## Evidence and decision

- Latest evaluation e5de5a88, b852527f/source def166c7: INCONCLUSIVE,
  314W/86L overall; development291W/79L, matched delta -0.0054054 over this
  edit base across185 side pairs. Recovery conversion was not selected.
  This result does not evaluate today's source. Self-play5306ecd5 is another
  revision and is not pooled with this experiment.
- Latest supplied loss04303c9c, A/00ambush, b852527f/source def166c7:
  completed1846, tribute651/1009, collection837/1034, own bag loss186/deaths8;
  own faults/suspensions0/0, opposing0/30. Full compact summary saved as
  refine-ambush-loss-full.json. Opponent source ff511c52/commit ecbc8203
  from task feedback's bd4078cd opponent. Totals show multiple weaknesses,
  not proof of a bank obstruction or that the recovery branch executed.
- Exact-base historical loss fb29d6e2c7d1b3dfca5b270b748116204f47088c88bc0c9bc8ff9cb1ab7d2c62,
  B/01the-farm versus boss ea15ef0f/source f4b4f65e: completed2000,
  tribute92/229, collection216/338, carried95/109, deaths1/0, own faults/
  suspensions0/0. Prior saved bounded logs record repeated bank37 at29,15
  and bank29 at29,14/30,17 hundreds of rounds apart. Proven stalls, not
  proven camp/lock causality. bank-corridor-evidence.json and archived
  task-79ea9383992346ad9b2f7d7b0474cc11.md retain exact provenance.
- That older corridor candidate3849da5e/source e17f373d was INCONCLUSIVE:
  development311W/59L, matched delta+0.0486486 versus this edit base,
  tribute841.19 vs779.94. Own suspension means0.0189189 vs0.0162162;
  both zero faults. It was not selected as edit base. The extra suspension
  is NOT causally attributed to clearing. Evidence: gem-priority archived
  notes/task-6acb6427618146c2a60cd1af13ff649f.md and source in Git.
- Changed rationale for revisiting it: retain its measured promising banking
  mechanism, replace repeated potentially large radius-five live scans with
  a smaller capped, spaced probe and a short-lived private obstacle hint.
  Broader safety claims, generic combat ranking, claims, Tavi draft and
  recovery changes remain deferred after negative/inconclusive findings.
- Contrasting exact-base validity wins0c7c1562(A)/0dcbf59c(B), saved
  reachable-final-smoke-{a,b}.json: tribute1008/52 and1001/12, zero own
  deaths/faults/suspensions. Map/opponent revisions unknown; not controlled
  strength evidence. Full match IDs are preserved in reachable-evidence.json.
- All6 frozen opponent file sets verified against manifest49ffc379.
  Inspected boss4feab379/ea15ef0f/f4b4f65e: Vendetta/Varg/Ryth, shared claims,
  risk-budget farming, local-power skirmishes,30-gem banking and spawn shops.
  Its tribute uses the nearest static bank field and attacks local locks;
  gamma independently retains objective-first banking and private routes.
  Source predicts policy, not runtime success or official-opponent behavior.

## Policy, contracts and risks

- Keep Varg/Vendetta/Ryth/Marcella/Heart, Jungle Strength -> Monster Strength ->
  Durability Health -> Power Strength;24-gem/near/winning/deadline banking,
  topology route fields, capture completion,40% retreat,98% spawn healing,
  resets/dashes, useful channels and unconditional dispatcher turn yield.
- Bank goals include every static altar approach. Do not globally exclude the
  only reachable locked bank just because some distant altar is unlocked.
  A local hostile lock is attacked; fresh arrival tribute remains intact.
- Private episode tracks best static bank distance; after4 rounds without
  improvement, optional probe requires65k fuel. At most one radius4 reachable
  flood and8 visible camp inspections, stopping live scan below45k fuel.
  Failed/new probes are spaced4 rounds apart; rotating samples avoid permanent
  exclusion of later candidates. No all-map group scan or per-candidate field.
- Eligible camp is within4, decreases static altar distance, lies on a shortest
  corridor or one-tile detour, and has a free attack approach actually reachable
  within4 current blocked-map steps. Nearest then lowest HP. Seven compiled
  assertions cover corridor/detour/off-route/behind/unreachable/radius boundaries.
- Retain the chosen handle for at most4 rounds, rechecking visibility before
  live HP/position each turn; refresh after movement/attacks. Refresh free
  approaches every probe. Use existing shield/attack/reset/spell code with an
  explicit obstacle override, retaining in-range enemy priority. At most one
  walk invocation in clearing; skip it below32k fuel, preserve18k action floor.
  walk itself retains its two bounded hidden-blocker attempts.
- Probe failure/budget skip falls back to normal legal bank movement. Nonbank
  gaps, death or submission expire episode/hint. No shared-memory writes,
  hidden live reads, ally vision, new channels or changed fuel allowance.
- Bounded100-round logs: bank_stall, cumulative bank_probe, bank_clear and
  bank_budget. bank_clear counts successful fight() calls while reopening,
  including enemy defense; it does NOT count destroyed camps or deposits.
- Risks: finite sampling can delay a useful blocker; allied congestion can
  invalidate an approach; clearing wakes a whole group and consumes HP/time;
  static corridor tests are approximate. All-goal routing can encounter locks
  more often. New branch fuel coverage on large maps remains unmeasured.
- Consulted playbooks B/C/D/F, compact reference, current capture/channel/item
  and movement rules, matching C++ unit/ability/field/submission contracts.
  Unchanged full-review handoff: SDK894229e1, CLI3.0.5, lockac2b5ad2,
  suitepublished-40-release-305-v1. Organizer hub is not complete policy review;
  reported engine1.0.3/fcb6c3e8 is distinct from CLI version; parity unverified.

## Validation and next action

- Initial trusted check PASSED exit0/source f5546e9b; superseded after review
  removed an overly strict post-move can_move guard to preserve arrival tribute.
  Saved bounded-bank-initial-check-response.json. No strength claim from it.
- Final bot-check --owner-config /var/lib/battlecode-volume/config/gamma.json
  PASSED exit0/source1f400f14832378d2cf97c61a9047def2e61aafdae1d74b742c266e1dca81a90b.
  Report.agent/check-task-030af596030548ff86a766ff488f5dbc.json; canonical
  check-report and wrapper response saved as bounded-bank-check{,-response}.json.
  Seven static assertions compiled. No bot source edits after this final check.
- Smoke6ed9277f(A): completed977, tribute1008/52. Smoke5e7008bf(B):
  completed940, tribute1001/12. Both sides zero faults/suspensions in both;
  own deaths/bag loss0. Full bounded-bank-smoke-{a,b}.json saved. Same41x41/
  hash6e3c6795, engine1.0.3/fcb6c3e8; map name/opponent sources unknown.
  Scores match exact-base validity smokes; no measured strength gain.
- First-page logs confirm the new source counters on A/B; sampled probes/actions
  are0. Positive clearing-branch coverage is NOT established. Bounded cleaned
  samples and transport provenance: bounded-bank-log-sample.json. All-map fuel
  remains uncertain. git diff --check PASSED; exact hashes/provenance and final
  diagnostics saved in bounded-bank-evidence.json.
- Next: supervisor evaluates the exact final checked source versus edit base,
  protected champion and frozen opponents under unchanged gates. Compare matched
  wins/tribute, extended bank stalls, probe/action coverage, bag loss, deaths,
  faults and fuel suspensions; do not promote from validity smoke games.
