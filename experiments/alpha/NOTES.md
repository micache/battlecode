# Current experiment: task-adc0e4b46bef4259b242f5d17c07a43b

## Identity and prior work
- Bot alpha; branch bot/alpha; input HEAD cc18ffa1c572acde39728efc85e75750fc8b436f.
- Accepted edit start c0cebd720fcd55e2bbb51d57dd2c398889d4071e; base
  9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
- Entry, branch, HEAD, six source-file hashes and unchanged documentation verified.
  Installed C++ header SHA256 90f4242686f22305b28d76d4fa2297187931b3c974f96faf324199e93979203d.
- Engine/SDK 2.1.6; historical-panels-v1; engine lock
  00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668.
- Latest candidate evaluated INCONCLUSIVE, not pending. Previous NOTES archived as
  task-8cfc033e18f84ea4b0f8aed69be2964d.md. Older incomplete work already preserved;
  no recovery applied. Accepted Git snapshot remains outside this transaction.
- Routine iteration: RESEARCH.md, compact reference, playbook C and relevant
  tribute/SDK sections consulted. Separate organizers' AGENTS.md remains absent.

## One hypothesis: playbook C, tribute on arrival
Starting tribute on the same turn that banking movement reaches an unlocked
altar will increase mean submitted gems versus accepted source on matched
development cases. Unchanged or decreased mean submission falsifies this
prediction. Compare collection, deaths and outcomes for opportunity cost.

## Evidence and change
- Evaluation e922ae87f7fb5e3d2d1c2d6d5a8d423b2128fca0858cf84f2cb0c27d65982906:
  commit cc18ffa1c572acde39728efc85e75750fc8b436f; source
  f9b2cc2dc5088ee5110d2b8e6d1ac062b79aa3fef330bf70fd59d85373626706,
  NOT the accepted edit start. 7W/17L; delta 0.0; zero faults/missing cases.
- Collision A loss 27495c84a61f48a2ecad232cf513ad607c88ea5ba508957914a2cf544aefad60:
  collected 726, submitted 638, deaths 18, round 1334; opponent submitted 1012.
- Collision A loss 9edaafa289223d8b724c09f47fbc17897f105f0b19d3fc58555451b696cadd53:
  collected 418, submitted 264, deaths 20, round 858; opponent submitted 1012.
  Both report zero faults on both sides; strategic losses, no identified engine
  failure. Supplied metrics saved in this task's -evidence.json. No action trace
  establishes the frequency or causal impact of delayed tribute in these games.
- Source reproducibly returns immediately after banking movement, even when the
  resulting tile is in tribute range. This defers channel start/countdown one turn.
- Add a bounded altar scan only after successful banking movement, re-reading live
  position and lock visibility before submit_gems; return immediately on attempt.
  Existing pre-move submission, recall, enemy priority, farming and yield remain.
- This differs from prior banking-before-combat and leftover-melee-movement trials:
  only successful bank-arrival timing changes. No thresholds, search, RNG or memory.
- GameRules.md 116, 222-231: channel start prevents subsequent actions; starting
  turn counts toward tribute duration. SDK cambc.h 3690-3694: submit_gems is void;
  4723-4734: lock query handles hidden tiles. No can_channel API exists; legality
  after movement must be checked by trusted smoke. Range/lock use fresh queries.

## Validation and uncertainty
- git diff --check PASSED, exit 0. Accepted-relative source review: only the
  post-movement altar scan in bot.cpp; other five source files unchanged.
- bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json
  PASSED, exit 0; exact source
  ea2cdb8e32b90b6be32b2f2d3775b35eb5461619eb465e6f62bc9ed952ac22b3.
  Report: .agent/check-task-adc0e4b46bef4259b242f5d17c07a43b.json.
  Reference: check:task-adc0e4b46bef4259b242f5d17c07a43b:ea2cdb8e32b90b6be32b2f2d3775b35eb5461619eb465e6f62bc9ed952ac22b3.
  Smoke IDs cd7363f0acafd39bbd2581f8d94a5723ae4757aae52117f133725667ce6c92c7
  and 3779a5cad389dccec52bc67023d5bb36f66bfe5fb68adcb81d5c45193631bd50.
  Smoke finals/action logs not inspected. These IDs alone establish neither
  completed games nor branch coverage. No branch-specific legality claim.
- READY_FOR_EVAL; no tournament evaluation or strength gain claimed.
- Frequency, fuel headroom and strength gain are unmeasured. Earlier tribute
  prevents optional later actions, though this branch already returned anyway.
  Existing conservative skipping of friendly locks remains a limitation.
- Next: supervisor evaluates source ea2cdb8e32b90b6be32b2f2d3775b35eb5461619eb465e6f62bc9ed952ac22b3
  against accepted, comparing
  submitted gems, collection, deaths and outcomes; no publication by worker.
