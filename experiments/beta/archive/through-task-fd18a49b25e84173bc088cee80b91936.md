# Operational summary

## task-fd18a49b25e84173bc088cee80b91936 — opportunistic altar denial

Hypothesis: buying one ten-gold lock at legal shop opportunities and placing it
on a visible empty altar along existing routes will delay opposing tribute and
improve matched wins while preserving our own banking. Falsifier: no matched
win gain, lower own submitted gems, or increased faults/fuel suspension versus
d2d57274 / 7daa9117. This is an unmeasured rules/source deduction.
Decision, evidence summary, checks and diagnostics: task-fd18a49b25e84173bc088cee80b91936/.

Identity: beta / bot/beta; HEAD/input fd1a894bb861e9d8fd3d65bbe3d7df506bf05960.
Trusted edit d2d57274232ca7cead5bacf650d6f51fd5b3bc3d; base source
7daa9117b8727b0da55d9282f8693e88107406d3b554eb644f3b9cf7b6f4ad6e.
All six source files byte-matched edit Git blobs at entry. The absent HEAD
combat_policy.h and prepared bot.cpp differences are intentional. Prior task
was PUBLISHED and evaluated; no unpublished candidate awaited evaluation.
Protected accepted 0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9 remains in Git and
the trusted accepted snapshot. No commit, push, agents or evaluation invoked.

Evidence: evaluation 47ef12cb516310ac155418a45e5d9e7cd1e8a9827e78b9a09f1459195bbecb84
measured fd1a894b / 6d52acdb, not the edit base/new source: 31W/17L, zero
reported faults, INCONCLUSIVE; matched edit-base delta -0.041667 on 24 side pairs.
Collision losses b7003f0d (A, round 684: 176 submitted/352 collected, 13 deaths)
and f85ac835 (B, round 792: 608/784, 8 deaths) show objective-conversion losses,
not a traced lock mechanism. Full IDs and summaries saved in evidence.json.
Contrasting saved final b6788e49 (A, round 573, 1030/1052, zero deaths) has
unknown map/exact own source in its final artifact; not a controlled current
win. Details/limits in decision.md; finals are hindsight only.

Frozen manifest 8446678b81be646cda6e98d6e1e9fd5a97a1376110f0b84d6463da5478e3132d:
starter 144ab5a9 / 9e804e3e and alpha 6af1685b / 87b9be45 exclude all visible
locked altars from banking goals without clearing them. New alpha 5f73d078 /
ba646c6e buys/places locks along routes; its safety pattern fits our farmer.
Gamma 1b34f42a / 3ce565f6 and our edit base handle hostile locks and permit
friendly ones. Adopted only the consumable-denial concept; opponent source is
not evidence of official opponents or a measured exploit. No private notes read.

Current strategy remains Varg/Tavi/Ryth/Vendetta/Marcella farming; Jungle
Strength, Monster Strength, Durability Health, then Power Strength; group
capture, bank each bag, complete spawn recovery. No live shared-memory protocol.
This candidate adds only:
- Buy one altar lock before shards when SDK can_buy permits, including death.
  Tavi's field-shard exception does not authorize field consumables.
- At turn start and after successful movement, attempt one visible empty altar
  within two tiles. No detour, patrol or capture/channel interruption.
- Require alive, inventory, no recall/tribute/teleport, no consumable restriction,
  and >=30k fuel. Intersect static altars with current visibility and no locks.
  Even a False use result ends this phase; subsequent phase refreshes observation.
- Existing banking already permits friendly locks and legally attacks hostile
  locks through submit_gems. Draft, combat, camp selection and recovery preserved.

Engine 2.1.6; lock 00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668;
suite historical-panels-v1. Documentation unchanged per trusted handoff; consulted
BOT_REFERENCE, RESEARCH, organizer record, Playbooks B/C/D/F/G and relevant
GameRules/C++ API/installed-header consumable, shop, visibility/channel sections.
SDK hash 90f4242686f22305b28d76d4fa2297187931b3c974f96faf324199e93979203d.
Organizer page is a download hub, not certification of all policies or parity.

Final source check (no bot-source edits afterward):
`bot-check --owner-config /var/lib/battlecode-volume/config/beta.json`
PASSED, exit 0; source
b4e969c76d293beb3fdfd75251814a80cb81d2e147e64ee34f5d7feedcdbb1a1.
Report .agent/check-task-fd18a49b25e84173bc088cee80b91936.json;
check:task-fd18a49b25e84173bc088cee80b91936:b4e969c76d293beb3fdfd75251814a80cb81d2e147e64ee34f5d7feedcdbb1a1.
Exact-source check-report independently returned PASSED/0, saved as
check-report.json. Smoke IDs a06b2d35e0543b1c7e7f73e187e33e637621b87b2a38d4e10b440d09b2326750
and ffb0829596bac15c07d892feb8e96f34956d5be121109d13ff426954a8cb8ef1.
Own-side stdout exports exited 0, contain zero bytes, saved as smoke-a/b.json.
These do not prove complete games, lock placement coverage or no suspensions.
`python3 experiments/beta/task-fd18a49b25e84173bc088cee80b91936/check_lock_contracts.py`
PASSED/0, report invariants.txt: safety contracts and ten unsafe mutations,
plus preserved base combat/farming/recovery/draft/yield. Static checks only.
`git diff --check` PASSED/0, report diff-check.txt.

Risks: spending 10g can delay an emblem; remote routes may leave locks unused;
clearing-capable enemies pay just three basics. Fuel reserve is a policy bound,
not measured headroom. Neither competitive gains nor denial coverage established.
Rejected another combat rewrite after its regression and a threat planner without
a causal trace; no patrols or previously tested arrival-tribute change bundled.
Prior routing +0.041667 with interlock regression, zero-gain harvest circuits,
and isolated item/draft/shield results did not establish additive gains.
Prior notes/negative findings archived through task-490c542467de4fe282d89f6170644b21.

Next: supervisor evaluates exact checked source against d2d57274 on matched maps,
both sides and frozen opponents. Compare wins, both teams' submitted gems, own
equipment progression/deaths and available fuel or lock telemetry. Accepted
champion promotion still requires the full gate.
