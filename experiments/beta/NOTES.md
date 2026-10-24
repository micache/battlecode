# Operational summary

## task-465e00389d2243759d3832a5f24e20f5 — complete farming foundation

Hypothesis: a deliberate farming roster plus a complete, risk-budgeted
clear/capture/invest/tribute policy will improve matched wins and mean submitted
gems over starter source 9e804e3e, without new bot faults or fuel suspensions.
No positive matched win gain, lower submissions, or increased faults/suspensions
falsifies it. Strategic gain is unmeasured; smoke validity is established below.

Identity: beta / bot/beta. HEAD/input 237c010e8e8b2a2d7e176ee1f160abf7380d056a;
actual edit and protected accepted commit 0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9;
edit hash 9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
All six on-disk starter files matched that edit commit before editing.
Preparation's Git diff against HEAD is the trusted source reset, not unfinished
worker work. Prior task was evaluated REJECTED; no pending beta candidate found.
Accepted source remains preserved in Git and trusted snapshot 81aa2616.
Task strategy.phase is foundation; brief's final mode label says refinement.
The actual starter capabilities and trusted strategy.phase guided this candidate.
Previous operational summary is archived in this experiment's previous-notes.md.

Bottleneck / rules deduction: the actual starter uses random draft/builds, no
abilities, no committed whole-group clearing, no clear safety estimate and no
reliable spawn-healing hold. Nearest-camp attacks can fragment clearing; kills
alone never award capture rewards. Capture needs uncontested occupancy through
five countdown rounds; extra allies do not accelerate it. Carried gems do not
score. Tribute is not cancelled by ordinary damage; recall is. Unmeasured causal
claim, not an interpretation of older candidate scores.

Implementation:
- Draft Varg/Vendetta/Tavi/Ryth/Marcella, truncated to actual map draft size.
  Varg supplies splash, Vendetta resets, Tavi invests without travel; later picks
  add durable AoE and stun-immune tributes. No linked-death pick in normal roster.
- Reuse our input revision's reviewed movement/combat/item helpers, updating
  asleep/awake threat semantics and five-hit lock comment for SDK 3.0.5.
  This is an explicit transfer of working systems, not a claim that input scores
  evaluate this newly constructed foundation.
- Load static groups once. Native terrain distance search ranks all groups by
  gems plus discounted gold per travel/clear/capture time. Inspect at most 12
  with a 45k fuel scan reserve; maintain 25% target commitment bonus.
- Estimate current remaining HP/damage only from visible camps, with full static
  design values for hidden members. Use visible nearby ally Strength, Varg
  splash estimate and Jungle mitigation. Predicted clear loss must fit 65% of
  current HP. Otherwise rally outside monster range on monster-only layouts.
- Hold occupied available rewards before banking. Skip another visible collector;
  discount duplicate cluster work. Store timestamp-derived respawn predictions,
  expire retry exclusions after 12 rounds, and vacate spent regions.
- Basic attacks, resets, damaging casts, AoE and shields; refresh after movement.
  Free approach roots, two bounded reveal retries and conservative route dashes.
  Main dispatch still catches invalid actions and always calls official yield.
- Bank at 30 gems, within seven geometric approach steps of an altar, for a
  winning bag or near SDK round limit. No feasible farm also banks small bags.
  Hostile locks are attacked; friendly locks allow tribute. Preserve channels.
- Retreat below 45% HP, escape awake monsters before recall, remain on spawn
  through turn end to heal. Empty-bag safe recall at 300 cash permits healthy
  reinvestment. Tavi shops remotely. Build Jungle Strength, Monster Strength,
  Durability Health, then Power Strength; opportunistic ten-gold altar locks.
- No draft/live memory protocol or per-turn logging. All state is private.
  policy.h compile-time assertions cover empty bags, bag/range boundaries,
  winning bags and round-limit banking.

Frozen manifest 2414fd9b inspected shared boss 4feab379 / ea15ef0f / f4b4f65e:
fixed reset/splash farmers; value/(travel+clear+wait) routing, claims/helpers,
clear-risk estimates, 30-gem banking, Jungle/Monster builds and 150-gold recall.
Relevant source: config.h, draft.cpp, bot.h and bot.cpp targeting/farm/tribute/
play sections. Frozen beta 054bc346 / 7cab9b0f drafts Varg/Tavi/Ryth/Vendetta/
Marcella. Transfer these mechanics selectively while retaining private,
visibility-based coordination and a more conservative health budget.
Arena source does not establish official private-opponent behavior.

Negative findings retained: later candidate 237c010e / 6145b56e was REJECTED,
276W/124L on the full pool; this is not evidence for today's starter edit base.
Do not repeat its strict 150-cash zero-gem eligibility cap: this candidate uses
soft cash-dependent gold value plus actual reinvestment. Older draft-only and
combat experiments do not isolate the effects of this integrated foundation.

Rules/SDK: CLI 3.0.5, engine lock ac2b5ad200d0df54380e94f82b1a327dd0407202533325808c8bf3af26c56136;
suite published-40-release-305-v1. Reviewed current GameRules, C++ API, matching
SDK, compact reference, research/organizer ledger and playbooks A–G. Material
updates: Golem, Heart of Ruin, five-hit locks, ten-turn wards, awake/asleep queries
and blocked-target move_towards behavior. Winning gems, round limit and tribute
range use SDK settings, with handbook profile 1000/2000/range 1. Static design
queries supply camp HP/Strength/range. SDK SHA256 894229e17d886358719abb70cac9ab5993263a0c05bf7df14fc48fa04a8336d3.
Organizer download hub does not certify all event policies or production parity.

Validation: first bot-check FAILED/1, source 2d715761, on an out-of-scope `seen`
variable; saved check-build-failed.json. Repaired before final check.
Final `bot-check --owner-config /var/lib/battlecode-volume/config/beta.json`
PASSED/0 for source cc05fd9d169d4956603c3f9fafde4d88901fc70217218384b775fc195c715079.
Report .agent/check-task-465e00389d2243759d3832a5f24e20f5.json, preserved in
this experiment/check-report.json. Exact-source check-report PASSED/0, saved as
exact-source-check.json. No source changes after that trusted check.
Smoke 56f48721a68c7464ded4e1c7673239410a9cff3ec04cefed844376b4b8c5c8ca:
our A roster, COMPLETED at round 964, 1000:4 submitted, zero own deaths, bag loss,
faults and suspensions. Smoke 4dafb8c8be03d3ff96974479fd61b1f2c93da4d17c04e10fa89323341648b470:
our B roster, COMPLETED at round 945, 1017:4 submitted, same zero own failures.
Both: 41x41 map hash 6e3c67956080f8da5a0042e68ea481189cd6f61061a742a8be0354a9ea5c5620,
map name and opponent revision unknown. These are wrapper smoke fixtures, not
controlled broad strength evidence. Saved summary slices include A's tail.
`git diff --check` PASSED/0; saved diff-check.txt.

Risks: partial vision/remote allies can distort clear-risk estimates; no shared
reservations; near-altar decision uses geometric distance; contested capture can
stall; shortlisting may omit a feasible choice. Rally coordination and dense-map
fuel headroom are unmeasured outside smoke. No measured advantage over boss.
Next: supervisor evaluates exact checked source against edit base/champion on
matched maps/sides/frozen opponents. Inspect submissions, deaths and suspension
counts, with monster-only and dense maps as critical contrasts. Full promotion
gate remains mandatory. No agents, publication, official actions or eval polling.
