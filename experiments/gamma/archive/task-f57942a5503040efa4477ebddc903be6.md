# Gamma operational notes

## task-f57942a5503040efa4477ebddc903be6 — reset across camp kills

- Refinement, bot/gamma; input/HEAD69f2a534, editf01d496c/source
  54c19acff8fb33174a4a428e37eb86c925b0de461514ebc2cc990ab23a7930e6.
  All seven starting files matched the trusted edit commit. The prepared
  three-file restoration was deliberate; no unfinished strategy patch or
  pending latest own evaluation. Accepted1a0675ca remains protected separately.
- Hypothesis: bounded reset retargeting after camp kills increases matched wins
  AND mean collected and submitted gems over the edit base, without new own
  faults or suspensions. Nonpositive gains or new reliability failures falsify it.
  This is an UNMEASURED rules/source deduction, not a replay-proven missed cast.

## Evidence and decision

- Latest evaluation4cb6d065, commit69f2a534/source8fb6844e: INCONCLUSIVE,
  299W/101L, zero faults; matched development delta vs edit base -0.0432432
  over185 side pairs. Development370 games: collection862.99, bag loss59.98,
  deaths8.13. This evaluated contact-farming candidate is NOT the edit source.
  Its full prior notes are retained in archive/task-fb147fa32a584508b58c80f102eede3a.md.
- Completed supplied loss35158db9, A/00ambush, that later source: tribute916/1005,
  collected916/1005, bag loss0, deaths4/2, both sides faults/suspensions0.
  Completed loss245b563b, B/00ambush, same source: tribute881/1026,
  collected1078/1026, own bag loss164, deaths6/19, own faults/suspensions0;
  opponent suspensions39. Opponent source revisions UNKNOWN in these summaries.
  Saved full compact summaries as refinement-loss-{a,b}.json. Finals motivate
  clearing and conversion work but cannot establish a turn-level missed reset.
- Contrasting exact-base smoke wins0c7c1562(A),0dcbf59c(B): tribute1008/52,
  1001/12, both sides zero faults/suspensions; reachable-final-smoke-{a,b}.json.
  Map/opponent revisions unknown; these are validity, not controlled comparisons.
- Source: fight() returned immediately when a basic killed its camp target.
  Later post-move calls could not reset without first making another basic.
  Thus a surviving neighbour could not receive a reset-enabled second hit.
  Vendetta camp kills refresh ability cooldowns; all chosen melee farmers except
  Heart have resets. Extra useful basics may shorten clear/capture cycles.
- Verified all6 frozen file sets against manifest2b2111ec. Relevant boss
  ea15ef0f/f4b4f65e uses Vendetta/Varg/Ryth, risk-budgeted clears, shared claims,
  local-power combat and30-gem banking. Its reset helper also keeps the original
  target. Our bounded retarget policy is independent, not a copied macro policy.
- Deferred: repeat contact transit, cooldown routing, gem reweighting, blanket
  claims, generic damage ranking or hard safety vetoes after earlier negative
  findings. No evidence justifies bundling a draft/item change into this test.

## Candidate policy and safety

- Keep Varg/Vendetta/Ryth/Marcella/Heart; current items, route shortlists,
  topology,24-gem/near/winning/deadline banking,40% retreat,98% healing,
  capture occupancy and useful channels. Champion combat selection is unchanged.
- Count actual camp basics in private state, reset each owner turn. Permit a
  self reset only after a real basic and with a visible, living in-range target;
  cap camp basics at2 across pre/post-move fight calls. Do not chase or switch
  groups to spend a reset. Refresh readiness and allowances after every action.
- If a basic killed its camp, at>=26k fuel with a ready self reset inspect only
  fresh visible camp tiles in basic range. Check static spawn membership in the
  current group and select the weakest living survivor. Never read hidden HP.
  If no survivor/reset/headroom remains, preserve the old early return and let
  farm enter capture. No new search, shared memory or all-map scan.
- Deferred post-walk resets require a previous actual camp basic this turn;
  a fresh normal allowance is preferred. Counter reset_next in existing bounded
  logs counts actual follow-ups after retargeting or a prior pre-walk basic.
- Five compiled assertions cover no unearned reset, one-hit follow-up, two-hit
  limit, dead target and out-of-range target. All compiled in the trusted build.
- Consulted compact reference, playbooksB/C/D/F, relevant rules/API and installed
  C++ declarations. SDK894229e1, CLI3.0.5/engine1.0.3, lockac2b5ad2,
  suitepublished-40-release-305-v1. Unchanged documentation full-review handoff.
  Organizer download hub does not establish full event-policy/production parity.

## Validation, uncertainty and next action

- bot-check --owner-config /var/lib/battlecode-volume/config/gamma.json PASSED,
  exit0, exact source3a93b2177ef5ea3edb74d9c8b15a68724ecd7f35637c802ad3db4b222c20e5b7.
  Report.agent/check-task-f57942a5503040efa4477ebddc903be6.json; canonical
  check-report saved as reset-retarget-check.json. No source edits after check.
- Smoke2c244df6 completed round974, tribute A1008/B52. Smoke3c83f3f2 completed round932,
  tribute A12/B1004. Both sides zero faults/suspensions in both games.
  Full summaries: reset-retarget-smoke.json;41x41/map hash6e3c6795,
  engine1.0.3/fcb6c3e8. Map name, opponent source and candidate-side attribution
  UNKNOWN in compact diagnostics. These are validity checks only.
- First smoke bot-a sampled log shows reset_next=1 by r201: the follow-up
  branch executed, not proof of faster clearing. reset-retarget-log-sample.json
  preserves the exact match/slice and bounded lines. Five compile-time assertions
  passed in the trusted check. git diff --check PASSED. Per-file hashes,
  decision, compact results and provenance: reset-retarget-evidence.json.
- Risks: consuming a reset can defer another target/shield; extra local queries
  cost fuel. This cannot solve route congestion, contested captures or bag loss.
- Next: supervisor evaluates the exact checked source against edit base, protected
  champion and frozen opponents under unchanged gates. Compare wins, collected
  and submitted gems, reset_next execution, deaths, bag loss and reliability.
  Do not promote on these smoke checks or pool distinct source revisions.
