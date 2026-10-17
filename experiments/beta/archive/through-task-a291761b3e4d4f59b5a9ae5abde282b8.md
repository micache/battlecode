# Operational summary

## task-a291761b3e4d4f59b5a9ae5abde282b8 — shop while dead

Playbook C. Hypothesis: shopping during dead turns equips affordable selected
power shards before respawn, reducing gold held idle through the respawn wait.
Falsifiable expectation: each dead turn invokes the existing guarded purchase,
buying floor(gold / shard cost) copies when can_buy permits; below-cost gold or
can_buy=false makes no purchase. The dead branch returns before position,
channel, movement, combat, recall or banking queries. Live policy stays the same.

Identity verified: beta, branch bot/beta, HEAD/input
`e6ef96f3788484ea89310f1de6f09a3a66c7d3b9`; accepted commit
`0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9`, source
`9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f`.
All six source-file hashes match handoff.edit_start. Entry trusted preparation
verifies accepted source; engine lock is the supplied
`00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668`.
SDK 2.1.6 cambc.h SHA-256 matches supplied 90f4242686f22305b28d76d4fa2297187931b3c974f96faf324199e93979203d.
No private engine-lock discovery. All six documentation hashes match handoff;
complete supplied rules/API exports, BOT_REFERENCE and C++ header read this task.
Separate organizer AGENTS.md remains unavailable. Accepted source is preserved
in this task's accepted-src/ directory and the task's accepted_snapshot.
Initial bot.cpp diff simply removes the prior reset candidate as preparation
restores accepted source; it is not an interrupted source edit.

Recovery: prior task-40d0fac06d944338a6ad7b95d26248c1 stopped before implementation.
Its exact notes, result and checkpoint patch are preserved under recovery/ with
that task ID. This invocation reissues its deferred, untested hypothesis;
no patch was blindly reapplied. Older current notes archived under archive/
through-task-32b6f4ccb8f54f1ead2a0e7c4bdcac48.md. No evaluation is pending.

Evidence: feedback 40881e4b4fa49a255e47bded00ebb82be29bc92df67840c2ef9e501f8fb63de2
is INCONCLUSIVE and evaluates reset candidate source
84ce3be7f5068fd196cd564885f695db7e16f2cb6a4ee7666c9ce65502812dac,
not the accepted source now on disk. Representative losses: corners A,
58932892f709016e850da88c2fb02af6f6b02b53802fca394801340f96355f29
(18 deaths, 140 unspent gold); elkring A,
fe658cc8a96b6e7a07ba8510fa46684c07b9947161c0d074569c3f1444e60b94
(42 deaths, 715 unspent gold). No reported bot faults; strategic losses rather
than evidenced arena failures. Totals do not prove unused dead-shop opportunities.
Source play_turn's !is_alive guard always skips shopping. Rules sections
A champion turn, Items & gold, Death confirm dead turns may shop. Installed C++
can_buy checks engine shop permission and affordability; gold_count requires
self, without position/visibility queries. buy_items already guards count/can_buy.

Implemented: a dead-only buy_items call followed by immediate return, before
the existing live channel/action guard. No new thresholds, item choices or RNG.
Validation so far: source invariant passed and rejects accepted baseline; the
existing count/can_buy guard and end_turn dispatch remain unchanged.
`git diff --check` exited 0. Exact trusted command:
`bot-check --owner-config /var/lib/battlecode-volume/config/beta.json`
exited 0, state PASSED for candidate source
`3036b3fac8c535a946dee4a06be419d84110294e7afec6621600d6073fa1504c`.
Local report: .agent/check-task-a291761b3e4d4f59b5a9ae5abde282b8.json.
Trusted reference:
check:task-a291761b3e4d4f59b5a9ae5abde282b8:3036b3fac8c535a946dee4a06be419d84110294e7afec6621600d6073fa1504c.
Recorded smoke match IDs:
42baa4198e71532a8bd1509f2ce74bc6a8b726adcc1895fd6eef6bbf51d92cc1,
ed80b131cc885e4ad9e6cd8c8ddfc14a225529fad0a5ad4edc71797139abc6f3.
No per-turn dead-purchase trace or strategic improvement inferred from PASSED.
Focused command: `python3 experiments/beta/check_dead_shopping.py` exited 0;
output saved in this task's dead-shopping-invariant.txt.
Remaining uncertainty: how often dead champions have affordable gold, timing
of actual purchases, fuel headroom and strategic benefit are unmeasured.
Next action: supervisor validates/evaluates the candidate; inspect dead shopping
opportunities if bounded turn telemetry becomes available.
