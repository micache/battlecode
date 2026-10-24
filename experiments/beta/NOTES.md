# Operational summary

## task-54ade8916f7d4fbfb65933f2fd780c1a — bounded clear/capture action economy

Identity: beta, branch bot/beta; input/HEAD/edit commit
863825b744eb21ee366370c9b1919ce73210d9d4; base source
c9c933a21b50bd9e01ca1dfdaca7bd290b0259e8cd51bc7c59ad340853232c11.
Protected champion remains 0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9.
All seven edit-base files matched task handoff SHA256 values; initial tree clean.
Prior QUOTA_WAIT task-0692138046ba40cca7c75c63fb2cf7cd had empty checkpoint,
unchanged source/notes and no result/check/candidate; nothing to recover.
Previous notes archived in this experiment's prior-NOTES.md.

Hypothesis: consuming legal kill-reset allowances and moving onto the capture
area after a final kill will increase matched wins, collected gems and submitted
gems over c9c933a2 without additional faults or fuel suspensions. No win/tribute
gain, lower collection or new reliability failures falsifies this prediction.
The mechanism is a source-grounded, unmeasured deduction; not a traced cause
of the aggregate losses.

Evidence (CLI 3.0.5, unchanged engine lock ac2b5ad2, suite
published-40-release-305-v1): evaluation b6b4c582b802ad60732d04df0469fcd801b4ab582329e3d788d433d67b76dc89
for the exact edit base was INCONCLUSIVE, 237W/163L, zero fault matches;
frozen boss 4feab379: 21W/59L. Development mean collection 621.77, tribute
564.87; 01corridors remains 0/10. Saved evaluation fields in evidence.json.
- 00ambush/A loss 1d7f6eedeee076dbbb3a3d872327dfc84b4798e5286051ce0d9a9b325376a51e:
  round 1722, 541:1032 submitted, 611:1032 collected, 12:2 deaths;
  own faults/suspensions 0/0. Opponent revision unknown.
- 00ambush/A loss f937dd30ba1ff1b9c773d3bd133d120bfe5353b3ebdc206e297a7d25d26b1926:
  round 2000, 548:959 tribute, 790:1015 collection, 8518:5058 gold,
  own faults/suspensions 0/0. Opponent revision unknown.
- Contrasting loss 85ebe39b7d4e32f64f7d64c0d8f34b4a3c0d30be5b331374f4e59a4ec6ae35bb,
  same map/side/base: zero own deaths, 7390:6366 gold but 510:866 collection,
  444:792 tribute. Combat losses alone do not explain poor gem throughput.
Final timelines/log slices retained; samples do not reconstruct every decision.
The base's previous fixture wins (9484a7a3/A, d4cff166/B) were 1026/1033 rounds;
source-specific diagnostics, not a matched comparison to this candidate.

Frozen opponent study: manifest 40570349, six sources. Read shared boss
4feab379 / ea15ef0f / f4b4f65e config, draft, skirmish and objective selection;
it uses local power ratios, melee resets, squad feasibility, hysteresis,
30-gem banks, 150-gold reinvestment and kit-specific builds. Read relevant
harvest/rotation sections of frozen gamma 01ae9e41 / f01d496c / 54c19acf:
it refreshes reward state after combat and can move onto a newly emptied group.
Transfer only this clear-to-capture timing idea; our roster/frontier policy stays
independent. Frozen sources are not proof of official opponent behavior.

Chosen change:
- Base returned after the first successful fight(), wasting restored allowances
  and delaying post-kill occupancy. New harvest.h controller permits at most six
  successful combat steps, one approach/reveal phase, then fresh combat checks.
  A completed clear gets a capture move even after the sixth successful step.
- bot.cpp refreshes life, fuel, visibility, position, target health, action
  allowances and group reward state at each phase. Keep 30k phase reserve;
  existing movement search reserve still defers an unaffordable route.
- Ready failure stops immediately; failed combat gets at most one approach,
  so hidden blockers/cooldowns cannot cause an unbounded retry loop.
- Existing Varg/Vendetta/Tavi/Ryth/Marcella draft; Jungle/Monster/Durability then
  Power; frontier ranking, capture hold, banking, lock/dash, healing and yield
  behavior retained. No shared-memory writes or fuel-setting changes.

Validation (artifacts in this experiment directory):
- Local host C++ probe failed/127: c++ is unavailable. No native test claimed.
  Moved eight SDK-independent controller fixtures to compile-time static_asserts
  in harvest_test.h; they emit no runtime test code.
- Exact command: bot-check --owner-config /var/lib/battlecode-volume/config/beta.json
  Red FAILED/1, source 766eeab2, check-red.json: missing harvest.h as expected
  before implementation. Final PASSED/0, check-final.json and check-report.json,
  source 94c4456585bbf31b89a32f9a5161a8b243a253638168083b016b0fda5f195fa7.
  Fixtures cover reset chains, approach/observation refresh, immediate capture,
  fuel cutoff, initial deferral, bounded progress and failed-action retries.
- Smoke A cd12ad19092e99530ec9db15124b8424f0cfcdee9475e1d984b63cefb216d63b:
  COMPLETED, win round 961, 1036:4 submitted, own deaths 1.
- Smoke B 3db6bdfd00621bb6c9d2fb4ad19c381849c65af48c2c3012766f3d665db28a25:
  COMPLETED, win round 1784, 1001:40 own:opponent submitted, own deaths 0.
  Both own faults/suspensions 0/0, full normalized summaries saved.
  Same 41x41 map hash 6e3c67956080f8da5a0042e68ea481189cd6f61061a742a8be0354a9ea5c5620;
  map name/opponent source unknown. Observed engine seed 17615240315955964814;
  no seed flag used. Sparse B yield samples include 24,577 fuel remaining,
  not a certified all-turn minimum. No source changed after final check.
- git diff --check PASSED/0; final-source-files.json pins per-file hashes.

Risks/negative findings: smoke timing is mixed versus prior base fixtures and
B is substantially slower; seed/opponent identities for those older fixtures
are not established here, so no causal comparison or speedup is claimed.
Repeated state/target checks may consume more fuel on dense groups. Geometric
frontier detours, excessive commitment, bank-route blockage, combat balance and
monster-only rally are still unresolved. Do not promote from smoke wins.
Rejected alternatives this invocation: gold weighting/cash caps (previous
strict caps failed), broader reranking (route churn/fuel risk), draft-only changes.
Rules/SDK unchanged per trusted handoff; consulted compact reference, relevant
playbooks, research/organizer evidence limits and installed allowance/path APIs.
Organizer hub does not establish every event policy or production parity.

Next: supervisor evaluates exact checked source against edit base and protected
champion under unchanged gates on matched maps/sides/opponents. Prioritize gem
collection, tribute, clear-to-occupancy timing, Vendetta kill chains and reliability;
if no gain, inspect reset usage before changing ranking, economy or composition.
No commits, pushes, agents, official submissions or comparative evaluation here.
