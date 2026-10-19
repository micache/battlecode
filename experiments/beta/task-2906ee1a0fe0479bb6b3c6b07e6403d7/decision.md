# Melee-first farming composition

Hypothesis: drafting Varg/Vendetta/Ryth/Marcella/Tavi in that order will improve
matched wins and submitted gems against edit 50a0d7d5 / 6d66a77f by replacing
Tavi with a mobile melee farmer on three-pick maps and adding Marcella before
Tavi on four-pick maps. No win gain, lower submitted gems, or increased own
faults/fuel suspension falsifies it. This is an unmeasured composition hypothesis.

## Decision and attribution

- All six initial source files matched edit_commit Git blobs and handoff hashes.
  HEAD 503f893d deliberately differs from edit 50a0d7d5. Prior task was PUBLISHED
  and evaluated; prepared differences/deleted objective_policy.h are restoration,
  not interrupted work. Protected champion 0ca5c04e stays preserved in Git.
- Latest evaluation 8b2b205d tested 503f893d / 4ba62e96, NOT this edit base.
  Its strict gem-routing change gained only +0.00892857 versus the edit on 56
  development side pairs and regressed collision (1.0 -> 0.5) and swirl
  (0.875 -> 0.5), while improving ambush (0.5 -> 1.0). These are map win rates,
  not independent reruns or direct evidence of a composition effect.
- Development collision losses a7d4a431 (A, round 1015) and 6931f83e (B, round
  1089), of that latest candidate, motivate examining per-champion output.
  Own Tavi submitted 152/22 with 4/2 deaths; own Ryth 260/476 with 2/0 deaths.
  Opposing Vendetta submitted 398/620 with 3/3 deaths. Cross-team figures are
  confounded by different policies, routes and fights, not a champion ablation.
  Full IDs, exact-source attribution and compact summaries are saved locally.
  They do not establish what current edit code would do on those games.
  Opponent revision is unknown in these supplied failure records; a similar
  roster is not an identity. No action trace establishes draft as their cause.
- Contrasting development aggregate wins of that evaluated candidate: ambush
  4W/0L per side; expanse A 4W/0L; stampede A 4W/0L. Individual winning IDs
  unavailable in the compact map table. Protect these cases during evaluation.
- Frozen manifest b3f17681: inspected gamma ecbc8203 / ff511c52, revision
  bd4078cd26f091dc34cbaa80a9d40d04d7a2e53cc7ae156430d1ec212e6c6974.
  It drafts Varg/Vendetta/Marcella/Ryth/Tavi, walks then attacks with melee,
  prioritizes reset casts, banks each bag and uses cost/reward farm routing.
  We adapt early Vendetta, keeping beta's Ryth third and existing gameplay;
  no copying of its recovery, shop, target scoring or defensive policy.
  Shared arena code does not establish official opponent behavior.

## Mechanism

Rules GameRules.md Vendetta/Tavi kits and BOT_REFERENCE sections 3/5 establish:
Vendetta starts at 70 Strength versus Tavi's 35; she has compatible walk/basic
attack/reset, two-tile dash, and camp kills refresh ability cooldowns. Tavi
instead has ranged attacks, field shard buying and a strong stationary spell.
The installed SDK draft contracts confirm owning completed-pick vectors,
map-dependent team size and deliberate pick submission. Our existing fight
and dash_along_route already support Vendetta; no new combat loop is needed.
Earlier dash work could not help the three-pick Varg/Tavi/Ryth roster because
none has a dash. Early Vendetta makes that implementation useful there.

Three picks: Varg splash, Vendetta mobile Strength farmer, Ryth durable AoE.
Four picks: add Marcella's melee reset and stun immunity.
Five picks: add Tavi field shopping/ranged control. Same five-body set as edit;
changed ordering can still change spawn assignment, collisions and act order.
All eleven fallback choices remain distinct, with map-size and duplicate guards.
No draft/live shared memory or hidden information introduced.

## Alternatives and risks

Repeated gold penalties, strict gem tiers, full schedulers and recovery changes
have measured regressions or small gains. Another such threshold would overlap
recent experiments. The earlier isolated Varg-first experiment concerned an old
random-draft/attack-only source, not this roster with active resets and travel
dash. It does not test early Vendetta on the current farming implementation.
Avoid restoring the broad combat rewrite (-0.041667 matched result in notes).

Main risks: losing ranged reach, field shopping and Tavi's control; additional
melee exposure and contested approach tiles; slower investment without Tavi;
Vendetta's dash spending a cast needed for a reset. The unchanged farm ranking,
45% retreat, shop policy, bank-first behavior and fuel guards retain their known
limitations. A composition-only ablation gives a clear evaluation question.
No claim of faster actual routes, more ability use or strategic gain yet.

## Validation and continuation

Use the approved bot-check for exact-source compilation and both smoke sides.
No new source-pattern test: the changed deterministic order is directly
reviewable; duplicate/size guards and gameplay are unchanged. Smoke validity
is not competitive evaluation or proof of measured fuel headroom.
Supervisor should compare exact checked candidate vs 50a0d7d5 / 6d66a77f on
matched maps/sides/opponents, stratifying 3/4/5 picks. Wins and submitted gems
are primary; Vendetta/Tavi contribution, deaths and bag losses explain results.
Retain the full champion promotion gate. If this fails, inspect three-pick
Vendetta's route/cast use before adding combat behavior or changing thresholds.

Observed validation: bot-check PASSED/0, exact source
9f2540790f9f048d6f404bb0f20a1e9e03180191c9c043c5322171f838253360.
Local wrapper report copied to check.json; exact-source check-report PASSED/0
saved as check-report.json. git diff --check PASSED/0 (diff-check.txt).
No source edits after bot-check. No competitive evaluation run.
