# Operational summary

## task-2906ee1a0fe0479bb6b3c6b07e6403d7 — melee-first farming draft

Hypothesis: Varg/Vendetta/Ryth/Marcella/Tavi draft order improves matched wins
and submitted gems versus edit 50a0d7d5 / 6d66a77f. No win gain, lower
submissions, or increased own faults/fuel suspension falsifies it. Composition
mechanism and strategic gain remain unmeasured. Decision/evidence/check files:
experiments/beta/task-2906ee1a0fe0479bb6b3c6b07e6403d7/.
Previous operational summary archived through task-382a14ec.

Identity: beta / bot/beta; input HEAD 503f893df4f6df62bbfc9677ccf72e9741f406d8;
edit 50a0d7d5ecbd99c70536b4c71c54e404f2daa2b1 / base source
6d66a77fa2db70675f473e34dde3c608cea2f08443a23646545ac4eb6076b6b2.
All six initial source files matched trusted edit blobs and handoff hashes.
Prepared bot.cpp/bot.h changes and deleted objective_policy.h relative to HEAD
are intentional restoration. Only draft.cpp changes from the actual edit base.
Prior task PUBLISHED and evaluated; no unpublished work awaiting evaluation.
Accepted champion 0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9 stays in trusted Git.
No agents, commit, push, official action or comparative tournament run.

Evidence: evaluation 8b2b205ddc38e7f4a6dff8b179fc10cf29902df721c9c24ec95247ad5d13b2e2
measured 503f893d / 4ba62e96 (strict gem routing), NOT edit/current candidate.
INCONCLUSIVE/full-map-pool, 98W/38L; development 81W/31L, zero own faults.
Matched development delta +0.00892857 on 56 side pairs. Collision regressed
1.0 -> 0.5, swirl 0.875 -> 0.5; ambush improved 0.5 -> 1.0.
- Collision A a7d4a4317f43be8dc5eeca9c494b0019c410561324971a512f4bc2c610b245bc:
  round 1015, 672:1024 submitted. Own Tavi 152 collected/submitted, 4 deaths;
  Ryth 260/260, 2 deaths. Opposing Vendetta submitted 398, 3 deaths.
- Collision B 6931f83e8b1424b0aff48b2ecb12738c7d280159e65719328e8b87008f868676:
  round 1089, 974:1032 submitted. Own Tavi 166 collected/22 submitted,
  2 deaths; Ryth 584/476, no deaths. Opposing Vendetta submitted 620, 3 deaths.
  Both summaries completed, zero faults/suspensions. Opponent revision unknown
  in these records; do not infer identity from draft. No draft-causality trace.
- Contrast: latest development ambush 4W/0L per side, expanse A and stampede A
  4W/0L. Individual winning IDs unavailable in compact table. Protect these.
- External official observations are different/older own code, unknown opponent
  versions, and uncontrolled; no imported scores used to select this candidate.

Frozen manifest b3f17681: inspected gamma ecbc8203 / ff511c52, revision
bd4078cd26f091dc34cbaa80a9d40d04d7a2e53cc7ae156430d1ec212e6c6974:
Varg/Vendetta/Marcella/Ryth/Tavi; melee walk+attack/reset, reward/time routes,
300-gold shopping recalls, each-bag banking. Adapt early Vendetta, keep Ryth
third and beta gameplay. Shared source is not proof of official behavior.

Current strategy: three picks Varg/Vendetta/Ryth; fourth Marcella; fifth Tavi.
Vendetta starts with 70 Strength versus Tavi 35; melee walk/basic/reset, camp-kill
cooldown refresh and two-step dash fit existing fight and route dash code.
Original three-pick roster lacked any dash, so could not use that travel policy.
Ryth keeps durable AoE third; Marcella adds stun immunity and melee reset fourth.
Five-pick roster has same bodies as edit but scheduling/spawn order can change.
All eleven unique fallbacks, current_draft exclusion, team_size guard and
one-pick return retained. No new memory, search, runtime logs or champion logic.
Jungle Strength, Monster Strength, Durability Health then Power Strength;
independent group captures, each-bag banking, 45% recovery, full spawn healing,
opportunistic locks, guarded route dash and bounded 12-group ranking remain.
No live team-memory protocol.

Risk: less ranged reach/control and field shopping; more melee exposure or
congested approach tiles; cast spent on travel rather than reset; slower
investment without Tavi. Current target ranking/visibility/fuel limitations
persist. Final scores motivate composition work but do not prove its mechanism.
Prior negatives retained: strict objective routing +0.008929 with map losses;
recovery +0.026786; full scheduler +0.041667 with interlock regression;
gold penalty +0.044643 with regressions; combat rewrite -0.041667; healthy
shopping/bank detours zero gain. Isolated draft/items/shield/harvest gains
unestablished. Old Varg-first random-draft trial is not this melee-first policy.

Engine 2.2.5; lock 0cabb3c78ae3c240c6bad22314505c71d3c16af68655326522d5f96bdae0a51d;
suite published-17-release-225-v1. Docs unchanged per handoff. Consulted compact
BOT_REFERENCE, RESEARCH, organizer record, Playbooks B/C/D/E/F/G, relevant
handbook kits/action rules, C++ draft API and installed SDK draft contracts.
SDK hash ee131e2981c16f696cb82cd6b04dc1871f45323057e51f7bb676a893ab72e264.
Organizer hub does not certify all event policies or production parity.

Validation: `bot-check --owner-config /var/lib/battlecode-volume/config/beta.json`
PASSED/0, exact source 9f2540790f9f048d6f404bb0f20a1e9e03180191c9c043c5322171f838253360.
Report .agent/check-task-2906ee1a0fe0479bb6b3c6b07e6403d7.json, copied check.json.
Exact-source check-report PASSED/0, saved check-report.json. No source edits
following check. `git diff --check` PASSED/0 (diff-check.txt).
Smoke IDs 31a7c0ea46a7b084e5007b4b3ccf4ee62c9b47790caf924441115044849dca46
and 2016e028c24209d525ba7d3b23959bb3d5dff2050bc01a78fe34737d3960ed3e.
Own-side stdout exports exited 0 and were empty (smoke-a.json, smoke-b.json).
Smoke success is not proof of complete competitive games, actual dash/reset
coverage, measured fuel headroom, zero suspensions, or strategic improvement.
No new source-pattern regression: simple order is reviewable, legality guards
and gameplay unchanged; trusted wrapper supplies compilation/engine smoke.

Next: supervisor evaluates exact checked candidate vs 50a0d7d5 / 6d66a77f on
matched maps, sides and frozen opponents. Prioritize wins/submitted gems; split
results by 3/4/5 picks and inspect Vendetta contribution, deaths and bag loss.
If it fails, inspect three-pick Vendetta route/cast use before combat changes.
Full champion promotion gate remains mandatory.
