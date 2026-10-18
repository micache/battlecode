# Operational summary

## task-1d43321af474473ebc71622f4c168925 — bounded banking detours

Hypothesis: avoiding currently visible enemy attack regions on banking routes,
when a reachable detour costs at most six extra walking steps, will reduce
carrier deaths and improve bag conversion and matched wins versus 9f7ae1c8 /
b4e969c7. Falsifier: no matched win gain, worse submitted/collected conversion,
or increased deaths/fuel suspension. This is an unmeasured source/rules
hypothesis; final statistics do not establish a banking-route cause of death.

Identity: beta / bot/beta; task ID above; HEAD/input/edit commit
9f7ae1c88a1bd0d5d62ed7713956efd40c95be33; base source
b4e969c76d293beb3fdfd75251814a80cb81d2e147e64ee34f5d7feedcdbb1a1.
All six source file SHA256 values matched trusted edit_start before editing;
initial working tree clean. Prior task PUBLISHED and evaluated, not awaiting
evaluation. Existing interrupted recovery artifacts retained. Protected accepted
0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9 remains in Git/trusted snapshot.
No agents, commits, publication, official actions or tournament runs invoked.

Evidence: evaluation a5df175f4daa1cec79538b74e4767f065bc6246390fb6f304c3654bbea485dea
measured this edit base: 42W/6L, zero faults/missing/unknown reliability,
INCONCLUSIVE/development-six-map; matched development-base delta +0.1875 on
24 side pairs. This is separate from protected champion delta +0.75.
- Collision loss 580f9745 (A, round 797): 682 submitted / 872 collected,
  58 carried, nine deaths; opposing old beta had three deaths, 1012 submitted.
- Corners loss 81041817 (A, round 409): 658/766, one death; opposing 1032.
  Uses trusted feedback summary; no full final exported for this case.
- Expanse loss 39a7bc8f (B, round 493) versus gamma: 858/928, zero deaths
  and zero champion damage taken on either team. Banking safety is unlikely
  to address this distinct farming-speed loss; expect unchanged routing when
  enemy threat masks do not intersect routes, apart from added query costs.
- Historical contrasting win b6788e49 (A, round 573): 1030/1052, zero deaths.
  Map and exact own revision unknown; not controlled evidence for today's edit.
Full IDs, source/opponent identities and computed final totals: this task's
evidence.json and two complete final.json exports. No omniscient state feeds
runtime policy. Final embedded engineVersion 0.0.1 is preserved as supplied;
trusted runner distribution identity is 2.1.6. No engine-failure cause inferred.

Frozen manifest b3e9b121b51589eb0f0522871455ef62e9e68b4a6db30ac56c3df39316e3ec8c:
gamma 1b34f42a / 3ce565f6 drafts Varg/Vendetta/Marcella first, with
melee walk-plus-attack/reset farming, cost/reward rotation, bank-before-fights,
legal lock clearing and no threat-aware banking path. Old beta d2d57274 / 7daa9117 matches our edit except lock additions;
it shares shortest-route banking and the current farm/recovery design.
Alpha 5f73d078 / ba646c6e places locks and explicitly clears hostile ones.
Inspected shared source, not private worker state or official-opponent code.
Lock-aware travel-cost selection was considered but not bundled: the measured
collision opponent buys no locks, so it does not explain that loss.

Current strategy: Varg/Tavi/Ryth/Vendetta/Marcella; Jungle Strength,
Monster Strength, Durability Health, then Power Strength; group capture,
bank each bag, complete spawn healing, opportunistic altar locks. No live
shared-memory protocol. This candidate modifies only movement policy for bank:
- Ordinary free-approach shortest path remains the fallback.
- With >=45k fuel after computing it, observe visible living enemies and mask
  Chebyshev attack_range + 1 (one next ordinary step). Clear our current tile
  from danger so a legal exit can be considered. No hidden health/position read.
- With >=30k fuel and nonempty safe goals, compute one additional reverse
  distance field. Use it only when reachable and <= direct distance + 6.
  Movement's reachable mask uses the SAME blocked board as the selected field.
- No route/no cheap detour/low fuel retains ordinary movement. One refreshed
  hidden-obstruction retry stays bounded as before. Channels and spawn recovery
  still return before banking; adjacent tribute and hostile-lock fallback stay
  unchanged. Nonbank callers retain their default movement policy.

Decision/risk: focus on carrier protection, not a general retreat planner.
Short detours bound the throughput cost and isolate the hypothesis from camp,
combat and draft changes. Enemy spell range, dashes, hidden opponents and future
movement remain uncertain. Camp damage is not masked. A moving enemy can cause
route oscillation; a six-step per-decision bound is not a bound on cumulative
travel. Excluding every approach falls back to risk rather than stalling.
Extra distance-field queries/copying add fuel cost; reserves are policy gates,
not measured suspension-free headroom. Existing wins may regress from delay.

Engine 2.1.6; lock 00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668;
suite historical-panels-v1; installed C++ SDK SHA256
90f4242686f22305b28d76d4fa2297187931b3c974f96faf324199e93979203d.
Documentation unchanged per handoff. Consulted compact BOT_REFERENCE, RESEARCH,
organizer access record, Playbooks B/C/D/F/G and movement/visibility/banking/
distance-field sections in rules, C++ export and installed header. Organizer
page is a download hub, not certification of all policies or production parity.

Final-source check (no bot-source edits afterward):
`bot-check --owner-config /var/lib/battlecode-volume/config/beta.json`
PASSED/0; source f3a34040840ca797a84b12e2ae9a0ed6992ce47fbaf58fe37bb568bb2e0df897.
Report: .agent/check-task-1d43321af474473ebc71622f4c168925.json.
Reference: check:task-1d43321af474473ebc71622f4c168925:f3a34040840ca797a84b12e2ae9a0ed6992ce47fbaf58fe37bb568bb2e0df897.
Smoke IDs 3c56d0a7e365d3757ae726ba03fde498c77a30e91257ea278c7296d318f78bb8,
736340f9ffdad930685cb9ea973fa67f0217acd39bbc3ba48230cdf6b1030fca.
`git diff --check` PASSED/0; this task's diff-check.txt.
Exact-source check-report independently returned PASSED/0. Both own-side smoke
stdout exports exited 0 and contain zero bytes; saved alongside evidence.
Compilation/smoke success is not a completed competitive win, banking-detour
coverage, or measured fuel headroom. Comparative strength remains unmeasured.

Negative findings retained in archive/through-task-fd18a49b25e84173bc088cee80b91936.md:
combat retargeting regressed -0.041667 against its edit base; camp scheduler
+0.041667 had interlock regression; harvest circuits had no established gain.
Earlier isolated arrival-tribute, draft/items/shield changes did not establish
additive gains. No previously rejected system is silently restored here.

Next: supervisor evaluates exact checked source against 9f7ae1c8 on matched
maps, sides and frozen opponents. Compare wins, carrier deaths, submitted and
collected gems and available fuel/route telemetry; separate collision combat
losses from expanse's combat-free speed loss. A later farming-speed experiment
needs its own measured candidate. Full promotion gate remains required.
