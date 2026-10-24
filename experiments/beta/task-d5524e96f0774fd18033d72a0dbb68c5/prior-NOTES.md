# Operational summary

## task-04a6a36aad2a41859e4b099bab70dc30 — amortized objective routing

Identity: beta, bot/beta; input/HEAD c6bdbe58ecdcf31c181b48bcba2a0460c65da7d9.
Actual edit base and protected accepted commit: 0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9;
base source 9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
Trusted preparation reset all six starter files to that commit; independently
verified each file and branch. This was not incomplete worker work. Latest beta
candidate c6bdbe58 / cc05fd9d was evaluated REJECTED; no pending beta candidate.
Accepted source remains preserved in Git. Prior detailed notes remain in Git at
c6bdbe58:experiments/beta/NOTES.md and task-465e00389d2243759d3832a5f24e20f5/.

Hypothesis: reuse terrain routes and amortize global objective ranking within
our previous complete farming policy to improve matched wins and submitted gems
over starter 9e804e3e, with fewer fuel suspensions than measured cc05fd9d.
No matched win gain, lower submissions, or unchanged/increased suspensions
falsifies the prediction. Strength and broad fuel improvement are unmeasured.

Evidence: evaluation 47319140264e1dc54b6d3c460c7d439d624673e2c61e617d64416c4eb7f0d57e,
source c6bdbe58 / cc05fd9d: full-pool 234W/166L, rejected; development subset
214W/156L, 370 observations, mean own fuel suspensions 3.618919, no bot faults.
Do not attribute those scores to the starter edit base or today's candidate.
00ambush/B loss 2b2c02f418758a0d84ad5d997b665ceafbf1835453a28d5a74735722d000b3bd:
947:1011 submitted, 21 own suspensions, four deaths, no bag loss or bot faults.
00collision/A loss 69d69c7688b27c5e7308d489be254ed28e56b0e19935a0c80ff9eff0e0a82c01:
505:1013 submitted, 26 deaths, 214 bag loss, zero own suspensions or faults.
00elk-arena/A loss 02d462af56c98ce1daf92bf0f03da16ec66ae636cf7b180c64d4ce919f64d222:
240:1020 submitted, three own suspensions; gold/kills alone did not win.
Full compact summaries are saved in this task's experiment directory. These
final statistics support investigation; they do not prove a per-turn cause.

Source mechanism: cc05fd9d builds a terrain field and globally ranks all camp
groups every farming turn, then rebuilds a dynamic route field for movement.
The chosen change amortizes that work rather than repeating the previous
foundation experiment unchanged. Explicitly reuse our own c6bdbe58 draft,
combat/build/recovery/bank helpers as the coherent starting policy upgrade from
the trusted starter. No opponent source is copied wholesale.

Changes / current policy:
- Deliberate Varg/Vendetta/Tavi/Ryth/Marcella roster, truncated to actual picks;
  clear/capture/rotate, visible-state risk checks, Jungle/Monster/Durability then
  Power equipment, field Tavi shopping, healing hold and 30-gem/near-altar bank.
- Cache static camp rewards/counts and terrain-aware shortlist/travel estimates.
  Expire after six turns or displacement over six tiles. During commitment,
  evaluate only the active group's current state, visible health and occupants.
  Otherwise examine the best 12 plus a committed target if absent (max 13).
- Cache a route for the exact goal mask; refresh on changed goals
  or an unreached current position. Build with current observed blockers, then
  choose actual movement from freshly read blockers. New hidden obstructions
  refresh masks, at most two movement attempts.
- If descending is blocked, rebuild to current free goals with current blockers.
  A radius-limited repair was legal but harmed smoke throughput; corridor
  detours can require initially increasing the old field distance. Reuse the
  repaired route on subsequent turns. Searches retain explicit fuel guards.
- Do not begin searches below 45k remaining fuel; live scans stop below 55k;
  basic movement loop retains 18k. Insufficient-budget movement is deferred,
  not converted into a 12-round camp exclusion. Unavailable movement also does
  not invalidate a target. Main dispatch always reaches official end_turn.
- Compile-time regressions cover plan validity/age/displacement/time reversal,
  deferral versus blocked/arrived/unavailable movement, and prior bank/dash edges.
- All state is private. No live/draft memory writes and no per-turn logging.

Frozen opponents: manifest b939207e, six sources. Inspected shared boss
4feab379 / ea15ef0f / f4b4f65e config, draft, targeting, farm and turn dispatch:
fixed melee-reset/AoE roster, periodic travel refresh/retargeting, helper claims,
30-gem banks and 150-gold reinvestment. Transfer periodic geometry reuse while
retaining our own conservative clear budget and private coordination. Frozen
beta 054bc346 likewise bounds live shortlist checks; gamma ecdee203 is the
same starter hash as our edit base. Arena source is not official private code.
Rejected alternatives: shared rally protocol would not fix repeated route work;
combat avoidance addresses collision deaths but not large-map planning cost.
Do not repeat rejected strict 150-cash zero-gem camp caps or draft-only tweaks.

Rules/SDK unchanged since task-465e0038 full review. Consulted compact reference,
playbooks B/C/D/E/F/G, research and organizer ledger, relevant C++ SDK contracts.
CLI 3.0.5; engine lock ac2b5ad200d0df54380e94f82b1a327dd0407202533325808c8bf3af26c56136;
suite published-40-release-305-v1. Installed header independently matches
894229e17d886358719abb70cac9ab5993263a0c05bf7df14fc48fa04a8336d3.
Organizer Markdown hub does not establish all policies or production parity.

Validation: bot-check --owner-config /var/lib/battlecode-volume/config/beta.json
initial PASSED/0 for 5831f61f; saved task directory/check-initial.json.
Second check PASSED/0 for 4d72f980, but legal navigation regressed: A smoke
9a653d95 ended at round 2000 with 406:55 submitted; B smoke 6631b051 won
1003:4 at 1228. Both had zero own faults/suspensions. Preserved as
check-local-repair.json and local-repair-smoke-{a,b}.json. Do not mistake that
passing check for evidence of good objective throughput. Replaced static-only
routing/local repairs with reusable occupancy-aware routes and full repair
when blocked. Final `bot-check --owner-config /var/lib/battlecode-volume/config/beta.json`
PASSED/0 for source
4fcc082c28cb06bcac21ee3c5e27638a1111b80db1fdffa25664fc2e1dcc331a.
Saved task directory/check-final.json and exact-source-check.json; exact-source
check-report independently PASSED/0. No source changes after the final check.
Final A smoke 42dfd6946de7c177e53e07d94cfbb2f2f2a3a7295ebdf2c18806634cd0d23f8e:
COMPLETED at 925, 1008:4 submissions. Final B smoke
0bf340e099fe53d9836317415efa3da8e4b789464af3468504ca5f2d07f3f492:
COMPLETED at 1031, 1002:22 submissions. Both: zero own faults, suspensions,
deaths and bag loss. Both 41x41 fixtures, map hash
6e3c67956080f8da5a0042e68ea481189cd6f61061a742a8be0354a9ea5c5620;
map name/opponent revision unknown. Saved full smoke-{a,b}-summary.json.
Earlier cc05fd9d fixture wins (964/A, 945/B) establish that this smoke comparison
is mixed on speed, not proof of a competitive gain or independent repeats.
Final git diff --check PASSED/0; task directory/diff-check.txt.

Remaining uncertainty: cached occupancy can leave a suboptimal detour until
the next repair; six-turn ranks can miss new opportunities. Full ranking and
initialization are still nontrivial phases; dense-map headroom is not certified
by smoke. Collision deaths, cooperative monster rally and camp value bias remain
separate limitations. No competitive improvement is claimed from wrapper wins.
Next: supervisor evaluates exact checked source against edit base, prior cc05fd9d
and protected champion on matched maps/sides/opponents under unchanged gates;
compare submitted gems, wins, fuel suspension and dense-map nonprogress. If fuel
improves but wins do not, investigate collision combat and monster-only rally.
No agents, commits, publication, official actions or tournament polling.
