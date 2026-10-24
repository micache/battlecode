# Gamma operational notes

## task-423449f15111476db311d689ef85b218 — melee objective foundation

- Trusted envelope phase **foundation**, brief experiment label exploration.
  Bot gamma, branch bot/gamma, HEAD/input c0c61f22592660fbd222d6f9130a9c2562f31183.
  Actual edit base/protected champion 1a0675ca881d4b67cb5c6cb1822ce2ae1602dc4d,
  source 9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
  All six starting source files matched that commit; prepared restoration and
  farm_risk.h deletion were intentional. No pending own evaluation was supplied.
  Old operational notes archived as task-e523e59b36b9442d9c09d5225bf2167d.md.
- Hypothesis: deliberate melee farming with draft-cached layout, ability
  sequencing, completed capture, deterministic reinvestment and timely tribute
  increases matched win rate AND mean submitted gems over the trusted starter,
  without new own faults. Non-positive win change, non-increasing mean tribute
  or a new own fault falsifies it. This is a rules/source foundation deduction;
  smoke results establish execution only, not matched superiority.

## Audit and chosen policy

- Starter bottlenecks: random draft/build, zero ability use, no gold recall,
  nearest-only camp selection, arbitrary PvP priority, no safe recall escape
  or spawn-heal wait. Existing draft dispatch and unconditional main-loop yield
  remain. Latest evaluated c0c61f22/source1d8ee413 is NOT this edit base:
  d25feff5 reported234W/166L, zero faults, development delta-0.0648649 against
  ecbc8203/sourceff511c52 over185 pairs. It does not evaluate today's source.
- Draft Varg, Vendetta, Ryth, Marcella, Heart of Ruin, then legal fallbacks.
  Melee walking plus attacking supports clear/capture turnover. Varg handles
  dense camps, Vendetta finishes, Ryth/Marcella control. Heart appears only on
  five-pick maps and is newly supported by SDK3.0.5; no five-pick smoke yet.
- First draft computes layout once and writes static anchors using protocol
  GA/version1/count16/xy8 pairs, <=1023 of1024 bytes. Retain nearest509 groups
  if capacity exceeded. Gameplay lazily loads shortlisted groups by anchor.
  The eight live shared bytes are unused; no hidden ally vision is assumed.
- Shortlist8 nearby groups plus committed target and rotating probe. Score
  (5*gems + gold weighted1 before round900,0.35 later)/(8+travel+clear+capture).
  Clear uses current visible HP, otherwise design HP; 1.12 reset estimate,
  Varg splash factor capped2.5. Exposure0.45*clear*summedStrength*mitigation
  adds recovery cost; predicted loss>currentHP multiplies score0.15, no hard veto.
  Commitment bonus1.30, slot affinity1.15, nearer-visible-ally penalty0.65.
  Another collector on a cleared region suppresses duplicate capture.
- Remain on reward tiles through capture; enter on the final-kill turn when
  movement remains. Leave after collection. Respawn estimates expire at their
  observed timer; current state reads require visible original spawn tiles.
  Eight failed path attempts defer a route12 rounds. Stationary attack/capture
  turns do NOT increment this counter (corrected during this invocation).
- Attack then reset then fresh target check, or legal direct/ground damage.
  One successful cast respected across slots. Shields under pressure; conservative
  dash paths use free landing tiles and ordinary passable intermediate tiles.
  Walk goals always exclude known occupants/terrain; two bounded hidden-block
  retries refresh observations. No blocked altar/monster passed to move_towards.
- Buy Jungle Strength, Monster Strength, Durability Health, then Power Strength.
  Finish each emblem before next stage; spend dead/spawn turns. Shop recall at
 150 gold before Jungle,300 later, only safe and empty-bag. Hold spawn until98%HP.
- Bank at24 gems, within6 estimated walking tiles of altar, winning bag or
  endgame deadline. Fresh post-move altar/lock check starts tribute on arrival.
  Allied locks permit tribute; hostile locks are attacked; buy/place spare locks.
  Preserve existing channels. Retreat below40%HP, leave awake-camp/enemy threat
  before recall. Unfavorable visible PvP (enemy power>1.2*local ally power)
  retreats toward spawn. No long chase. Capture can use shield/adjacent defense.
- Planning stops below45k fuel; movement has18k entry floor and two attempts.
  These are policy guardrails, not universal measured cost bounds. Exact normal
  C++ budget remains100k; no fuel/round overrides or host compiler used.

## Opponents and rules evidence

- Manifest b4d5b861251d0319b3338a866ca85ba71c8391af92169e679f3c0f9ec6fc666d,
  all six source file sets hash-verified. Relevant strategy source inspected.
  Boss ea15ef0f/sourcef4b4f65e: Vendetta/Varg/Ryth opening, shared claims,
  exposure-budgeted camps, support shields, local-power PvP,30-gem/near-altar
  banking,150-gold shopping. This candidate adopts the basic throughput mechanics
  while keeping independent routes and a soft exposure cost. No boss code copied.
- Alpha82a14a04 and5f73d078: random draft/Power stat build, legal combat and
  timestamped rotation. Beta7cab9b0f: Varg/Tavi/Ryth draft, reset farming,
  defensive item stages, bounded camp scan. Beta0ca5c04 matches our starter.
  Historical boss192daa8e uses a similar coordinated economy. Frozen sources
  reveal policies, not per-turn events or official-opponent behavior.
- Changed-document review: current GameRules, C++ API/installed cambc.h,
  BOT_REFERENCE, RESEARCH, organizer ledger and playbooksA/C/D/E/F/G.
  CLI3.0.5/engine1.0.3 buildfcb6c3e8; lockac2b5ad2, suitepublished-40-release-305-v1.
  SDK SHA256894229e17d886358719abb70cac9ab5993263a0c05bf7df14fc48fa04a8336d3.
  Material updates: Golem/Heart, camp awake masks, five-hit locks,10-turn wards,
  move_towards target considered free but known blocked landing still throws.
  Objective uses SDK winning_gems/max_rounds and rules1000/2000; gold tie counts
  lifetime earned, final complete tie favors B. Tribute ignores ordinary damage;
  recall does not; spawn heals at turn end; extra collectors do not speed capture.
  Organizer Agents page is a download hub, not a full event-policy certification.

## Checks and next action

- Final bot-check --owner-config /var/lib/battlecode-volume/config/gamma.json
  PASSED exit0; source7762c7e20f4bc127d2f4d165123a4d2fd950fb0cc132f544433c977fb6c8c89f.
  Report .agent/check-task-423449f15111476db311d689ef85b218.json.
  Compile-time assertions cover draft capacity, tribute boundary ticks and value/
  travel monotonicity. Initial source243fdff2 passed too; its report is archived
  in foundation-initial-check.json, not evidence of the final source.
- Final smoke7222a6ae, sideA: completed round967,1016 vs52 tribute, zero faults
  and suspensions both sides. Final smoke2baa5da6, sideB: completed round881,
 1006 vs12 tribute, zero faults/suspensions both sides. Both map hash6e3c6795,
  41x41, engine1.0.3/fcb6c3e8. Map name and opponent revision unknown in summary.
  Full summaries saved foundation-final-smoke-a.json and -b.json.
- git diff --check PASSED. Final file hashes and decision: foundation-evidence.json.
  No source changes after the final trusted check. No commits/push/submissions.
- Risks: geometric travel misranks obstructed routes; no live claims means
  duplicate clearing; soft exposure can still start unsafe fights; recovery can
  abandon near-finished camps; max509 plan truncation and larger maps untested.
  Wards and teleport-crystal island routing remain unused. Broad strength and
  current-boss performance are unmeasured. No claims of production parity.
- Next: supervisor compares final source to9e804e3e on matched development maps,
  sides and frozen opponents under unchanged gates, then full champion gate.
  Inspect tribute, early economy, duplicate camp work, deaths and fuel on large
  maps. Next useful experiment: measured claims or reachable-distance ranking,
  choosing whichever actual losses identify as the larger throughput bottleneck.
