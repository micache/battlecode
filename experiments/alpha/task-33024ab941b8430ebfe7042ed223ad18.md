# Current experiment: task-33024ab941b8430ebfe7042ed223ad18

## Identity and prior work
- Bot alpha; branch bot/alpha; input HEAD bf616d85ce50cbb69c611788b2fc1660dbd465a2.
- Accepted edit start c0cebd720fcd55e2bbb51d57dd2c398889d4071e; base source
  9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
- Entry and all six source files matched accepted edit start before editing;
  initial working diff was trusted source restoration, not unfinished new work.
  Accepted Git snapshot remains outside this transaction. Previous NOTES saved
  as task-1d40090f953b4001923fb46ca3b542b8.md; older recovery artifacts retained.
- Latest candidate evaluated INCONCLUSIVE, not pending; eight supplied recent
  tasks PUBLISHED. No recovery, publication or evaluation requested here.
- Engine/SDK 2.1.6; historical-panels-v1; engine lock
  00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668.
  Installed C++ header SHA256 matches supplied 90f4242686f22305b28d76d4fa2297187931b3c974f96faf324199e93979203d.
- Documentation manifest verified unchanged; routine iteration consulted compact
  reference, RESEARCH.md, playbook C, relevant handbook and SDK sections.
  Separate organizers' AGENTS.md remains absent and unreviewed.

## One hypothesis: playbook C, interrupted low-health recovery
Moving toward allied spawn only before retrying an interrupted low-health recall
will reduce mean champion deaths versus accepted source on matched development
cases. Unchanged or increased deaths falsifies this prediction. Compare submitted
and collected gems and outcomes to assess objective cost; compare the prior
unconditional-retreat candidate descriptively, without pooling source revisions.

## Evidence and change
- Evaluation 1304894436dcf2cdb4d134cbbd15c66c9071c59b1eeec55aa44bd1ddc02b9d94
  evaluates commit bf616d85ce50cbb69c611788b2fc1660dbd465a2 / source
  0c91f9bf05bff0bfbf70eb1a00633ec2699e650db57a1dcda0316055df93dd26,
  NOT accepted edit start. Development 18W/6L, no faults/missing/unknown;
  mean deaths 3.2083. Provisional suite, no strength conclusion.
- Collision B loss 3994df201d3d20795493872243ea7a74003180230571b321bd0768ff75eb0867:
  round 1083, 10 deaths, 814 collected, 704 submitted vs A's 1012.
  botFaults [0,0]; outcome teamA. Complete final reconstructed from two bounded
  arena-client slices, saved in this task's -collision-final.json.
- Also supplied collision A loss 65af7fb0944b457136f8545ef905473b0859fc80f5a411720a76c351b9851d5a;
  detailed runtime cause unknown. Both match references belong to the above
  evaluated source. Aggregate loss/death metrics do not prove interruptions.
- Reproducible accepted-source behavior: every actionable low-health turn away
  from spawn recalls without moving. Damage can cancel that channel, leading to
  stationary retries. Latest unconditional-retreat results motivate refinement:
  avoid detours on the initial recall attempt while retaining movement on retries.
- Add one private per-champion boolean, armed only after observing an active
  recall started by this bot. Existing live/dead/channel guard retains it while
  unable to act. At the next actionable nonchannel turn, consume the flag;
  spawn arrival or recovered health expires it without a retreat.
- On a flagged low-health retry away from spawn, call existing bounded navigation
  once toward allied spawn. Refresh own position. Start/observe recall only if
  still away; walking arrival yields through end_turn for spawn healing.
  A failed move retains recall fallback. Initial attempts remain stationary.
- No shared-memory layout, draft, combat, shopping, threshold (35%), randomness
  or runtime settings changed. Four other source files remain accepted-identical.
- Rules: GameRules.md 116,122,270-274,369-375 (action/channel timing, damage
  cancellation, spawn healing). SDK cambc.h 3448,3661-3665 (live recall state and
  self-only void recall command). Only own live state is added as a runtime input.

## Validation and remaining uncertainty
- Source contract regression PASSED; report this task's -source-check.json.
  Checks private state, first-attempt gating, one move, channel preservation,
  refreshed arrival, observed start, unchanged other sources and official yield.
  This is source inspection, not runtime branch coverage or fuel measurement.
- git diff --check PASSED, exit 0; accepted-relative diff reviewed.
- bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json
  PASSED, exit 0. Exact checked source
  d08f6defabd911f8664dac894f139d683dcc31c686186d5dbb56c3b1f9b12202.
  Report .agent/check-task-33024ab941b8430ebfe7042ed223ad18.json;
  reference check:task-33024ab941b8430ebfe7042ed223ad18:d08f6defabd911f8664dac894f139d683dcc31c686186d5dbb56c3b1f9b12202.
  Smoke IDs 4289c931c167d7bee66811a7a61f77f718957c63595a2fe6b0bc17fceb6ca6a0
  and 73c64b6da10cadc1dd0e044f6155b7c4785149f3c4a3005042b28a019b2c9e0a.
  Smoke finals/action logs not inspected; no completed-game or branch-coverage
  claim follows from those IDs. Source unchanged after trusted check.
- READY_FOR_EVAL; no strength claim, publication or tournament invocation.
- Mortality cause and actual interruption frequency remain unknown. Retreat may
  approach threats, reveal blockers, fail, or use fuel; no safety/path monotonicity
  is claimed. The accepted post-recall early-departure behavior remains a risk.
- final.json exports engineVersion 0.0.1 / packed 65536 while trusted task pins
  CLI/SDK 2.1.6. Slice carries no lock identity; relationship of that field to CLI
  version is unknown, and no engine mismatch is inferred from it alone.
- Next: supervisor evaluates exact checked candidate against accepted source;
  compare deaths, submitted/collected gems and outcomes. If mortality does not
  improve, obtain bounded interruption traces before further recovery changes.
