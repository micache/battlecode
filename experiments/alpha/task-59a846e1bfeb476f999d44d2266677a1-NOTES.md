# Current experiment: task-59a846e1bfeb476f999d44d2266677a1

## Identity and status
- Alpha, bot/alpha. Input HEAD 2dcd14cf3ed7e4e224208ea02920fc90b0f69a5c;
  edit commit 5f73d0787014e3f712d0eb6234f088fee489b4d8, base source
  ba646c6e0b2f1259645b5eb6160f8b836c5ef8926cbbf777702b0dc3d8892a8f.
  All eight starting files byte-matched edit_commit. HEAD differences were trusted
  preparation, not unfinished work. Latest candidate evaluated, not awaiting it.
  Accepted champion c0cebd720fcd55e2bbb51d57dd2c398889d4071e remains protected in Git.
- Engine/SDK 2.2.5; lock 0cabb3c78ae3c240c6bad22314505c71d3c16af68655326522d5f96bdae0a51d;
  suite published-17-release-225-v1. SDK header verified ee131e29...b72e264.
- Changed-document review: complete handbook, C++ export and pinned header;
  BOT_REFERENCE, playbooks A/B/C/D/F/G, RESEARCH, organizer and verification ledger.
  Material changes: camp awake/asleep queries now exist in the installed header;
  ward::owner is documented but absent, and is not used. Release mode skips
  debug_block bodies. Defaults remain 1000 tribute, 2000 rounds, 100k C++ fuel,
  1024/8 memory bytes; tie order tribute/lifetime gold/kills/absolute B.
  Organizer page is a download hub; no full policy/production parity certification.
- Previous NOTES archived as task-844841b0ef694b819a6ab2fcf1a89387-NOTES.md.

## One hypothesis
Predicting visible awake-camp volleys and choosing lower-exposure escape steps
through completed spawn recovery increases matched development win rate over the
edit base. Unchanged or lower win rate falsifies this prediction. Fewer deaths
and higher collected/submitted gems are mechanism diagnostics. This is a source/
rules deduction, not a traced explanation of any match's retreat timing.

## Evidence and choice
- Latest evaluation 710f58a196dd1fc67d5e820bbd1947dfb56b16ca153e6dc159005df7db377ab5
  evaluates 2dcd14cf / source 822811f4...892ed5f1c, NOT today's edit base.
  Development 82W/30L versus edit base 85W/27L; matched delta -0.0267857,
  56 side-paired cases, no faults/missing/unknown. Group-first route planning
  regressed overall and is not reapplied. Protected champion comparison is separate.
- Ambush A loss 7cc676c2623db79add9852fddcaa18f6ca1ba87987a40bd981c849f519820dc9:
  source 822811f4, round 726, tribute/collection 548 vs 1009/1062, deaths 5 vs 4,
  zero PvP damage/kills/bag loss. Own camp damage taken 22070; no bot faults.
  Vesper died twice, Ryth once, Willow twice. This establishes camp mortality,
  not the position or health of any retreat. Saved complete summary under task ID.
  Opponent strategy matches the frozen melee farming roster; exact match opponent
  revision is unknown in summary, so no source version is inferred from roster.
- Ambush B loss a6ea1f7148f65a156223d2e1d4d5b5e06db0bc628c51b5dadc724d32ca1ce246:
  same evaluated source, round 858, collection/tribute 654/548 vs 1080/1080,
  deaths 11 vs 4, camp damage taken 30670, faults zero (supplied task metrics).
- Contrasting development coverage: this edit base wins elkring 8/8 and expanse
  8/8, but ambush 3/8. Latest experiment wins elkring 8/8, ambush 2/8.
  These map aggregates do not reconstruct individual turn decisions.
- Frozen manifest dad2898a...fdf64: verified all six source file sets. Inspected
  beta d2d57274 / 7daa9117 and gamma 1b34f42a / 3ce565f6. They use melee-heavy
  farming, selective PvP and safe recovery, with farming passives and group costs.
  Beta's old source explicitly lacked wake-state queries; its conservative
  all-camps danger test is not copied now that installed SDK exposes awake state.
- Base retreats at 35% health toward spawn without pricing exposure of a step.
  Repeated camp damage can cancel recall; staying on spawn is required to heal.
  Prior spawn-heal-only, spawn-directed/threat-gated/retry recall, items/draft,
  resupply, banking/batching, AoE, focus-fire, travel-dash and camp route trials
  remain negative/deferred. New rationale: a bounded awake-volley model and
  exposure-first escape are coupled to completed recovery; not just another
  spawn-heal guard or an isolated threshold adjustment.

## Candidate policy
- recovery.h contains one-turn bounded observations and pure exposure/choice
  contracts. bot.h owns one private recovering flag; cleared on death/full recovery.
- Healthy >=70% turns skip scans. Otherwise inspect at most 32 visible damaging
  awake camps/enemies, stop at 45k fuel. Enemy range adds one base movement step;
  camps use actual design range and current strength. Sleeping camps are omitted.
  No hidden live state, allied vision, cross-turn enemy handles or extra shared bytes.
- Keep 35% ordinary retreat; below 70%, also recover when health <= two observed
  raw basic volleys. This estimate ignores mitigation/shields/target selection and
  future spells/hidden units. Conservative early retreats can sacrifice farming.
- During recovery use a ready walking-compatible self shield when exposed, without
  overwriting an active shield. At a quiet complete observation, recall immediately.
  Otherwise compute one native home field and compare <=9 legal ordinary choices:
  minimize raw damage, then weighted depth inside threat ranges, then home distance.
  A reachable spawn tile wins because turn-end healing precedes the next camp phase.
- Only move with >=28k fuel. Refresh observations after any move attempt, including
  False/reveal, before optional recall. Partial scans never certify a quiet tile;
  below scan reserve yield after movement and retry fresh next turn. No fuel override.
  Maintain recovery to spawn and stay through turn end if still injured.
- Draft/stat RNG, farming/rotation/capture, ordinary fight, banking/locks, four-byte
  shared-round protocol, channel preservation and official yield otherwise remain
  edit-base-identical. Accepted source remains outside this transaction.

## Checks, uncertainty and next step
- Embedded constexpr regression contracts cover summed overlapping volleys,
  out-of-range safety, escaping flat exposure despite a longer home path,
  exposure dominating home distance, quiet distance tie-breaks and recovery gates.
  These are pure policy cases, not engine scenario or branch coverage.
- bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json PASSED,
  exit 0; source 07022bad764ef37711c5afeddb10a434a0d5f9c5581e519f8bb575ced706fca2.
  Local report inspected: .agent/check-task-59a846e1bfeb476f999d44d2266677a1.json.
  Smoke IDs 2c31e9776c4aa50929869b13b230c7aef70e0483af3d0605e7e58dec4e250330
  and 2acf67f0b067e512deda18a404881b574f270339cc2d145f2eef8cccf5b9c84b.
  Summary alone does not establish full-game completion, recovery branch coverage
  or normal-turn fuel headroom. Embedded contracts compiled in the trusted build.
- git diff --check PASSED, exit 0. Source hashes unchanged after trusted check.
  Decision JSON records exact identities, parameters, document/opponent hashes,
  supplied development evidence and source file hashes. READY_FOR_EVAL.
- Risks: conservative danger can abandon finishable camps/captures; hidden threats
  and enemy spells are unmodeled; threat caps/fuel can force long walks; local
  exposure minima can delay escape; a freshly awakened first volley can precede
  the next turn; linked deaths are not coordinated; normal-turn headroom unmeasured.
- Supervisor should compare the exact checked candidate with edit base and protected
  champion across maps/both sides. If win rate is unchanged/lower, reject; inspect
  deaths, collection/tribute and recovery travel before any threshold tuning.
  No agents, tournament invocation, publication, commit/push or official submission.
