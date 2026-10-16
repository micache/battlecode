# Operational summary

## task-40d0fac06d944338a6ad7b95d26248c1 — BLOCKED before implementation

Playbook C. Deferred hypothesis: shop during dead turns so affordable shards
are equipped before respawn. Falsifiable expectation: a dead champion with
enough gold buys its selected shard; an unaffordable purchase is skipped.
Source buy_items already checks count/can_buy, but play_turn returns on
!is_alive before reaching shopping. BOT_REFERENCE.md sections 1 and 4 say
dead champions can shop. No implementation or strategic benefit is claimed.

Task feedback 40881e4b4fa49a255e47bded00ebb82be29bc92df67840c2ef9e501f8fb63de2
evaluates prior reset source 84ce3be7f5068fd196cd564885f695db7e16f2cb6a4ee7666c9ce65502812dac,
not this working baseline. Its faults are zero; unspent-gold mean is 720.83.
This aggregate does not establish missed dead-shopping opportunities.
Branch and HEAD match task bot/beta and input e6ef96f3788484ea89310f1de6f09a3a66c7d3b9.
Initial bot.cpp diff removes the previous reset experiment, consistent with
make_attempt restoring accepted source. No source edits made this invocation.

A broad rg --files search under /var/lib/battlecode-volume/arena, intended to
locate the engine lock, erroneously traversed arena-private directories despite
glob exclusions. It exited 2 with Permission denied. Stopped without retry,
permission changes or further investigation, as AGENTS.md requires. bot-check
was NOT_RUN. Source/snapshot and engine-lock identities were not fully verified.
Next action: supervisor reissue a bounded task; use supplied paths directly
and never recursively search the arena root. Hypothesis remains untested.

Accepted baseline: commit `0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9`, source
`9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f`.
Engine/SDK 2.1.6. Prior experiments archived in
`archive/through-task-71c9eb3108ef49ebb55a7414dded1ec1.md`.

## task-32b6f4ccb8f54f1ead2a0e7c4bdcac48 — use one attack reset

Playbook D. Hypothesis: after a basic attack leaves a target alive and in range,
using a ready self-targeted attack reset and attacking once more increases
damage per eligible turn and shortens clearing/fights. Falsifiable expectation:
an eligible survivor receives two basic attacks with one reset cast; a killed,
hidden or out-of-range target receives no follow-up or wasted reset. At most
one reset is attempted per attack decision, even with Vendetta kill resets.

Identity: beta, bot/beta, HEAD/input c1e4817b7462f135d009e24e1971604187bb3af1.
Initial working and accepted snapshot source both match base
9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
The initial diff removes the prior capture experiment because make_attempt
restores accepted source. No interrupted work or pending evaluation: feedback
7721495cdd3613a1c77199c86b3914bb44195ed363c06f9421cc40bd7fb4b5f4
is INCONCLUSIVE. Engine lock canonical identity matches the task; SDK 2.1.6
header hash matches that lock. Supplied documentation hashes match RESEARCH.md.
Accepted snapshot remains outside the edit transaction. Organizer AGENTS.md
remains unavailable.

Evidence: feedback evaluates c35aa333ec97f25235b09630777b16febbac86cd80423946d2065bb2321ccf02,
not this accepted source or patch. Representative losses: collision B,
3fd672d4f5f86dc4aaecc2da0a78b3f7f11d566f0c393d653f70a8c14a54c9e1
(528 submitted, 36 deaths); elkring A,
5fe5b927be17188ac5d2cb7c638276bd2926f5ea9a87d6c59fa8ef371ab6a74e
(396 submitted, 48 deaths). All reported bot faults are zero. These aggregates
motivate inspecting damage efficiency but do not prove missed reset costs.
Source proves attack_if_in_range always stops after one attack, with no ability
casts anywhere. GameRules.md:100,116,458–462 describes reset allowance, shared
cast budget and self targeting. SDK ability.is_ready checks cooldown/can_cast;
is_attack_reset identifies either slot without champion-name assumptions.

Change: extend the existing attack helper with one bounded reset and
follow-up, refreshing self/target legality after actions. No route, draft,
banking, recall, shared-memory or shopping policy changes. Strategic benefit,
reset-use frequency and fuel headroom remain unmeasured. No isolated action
trace proves the two-attack expectation; source review checks the legality guards
and one-reset bound. Next action: supervisor evaluation against accepted source;
measure clearing time/reset usage if bounded telemetry becomes available.

Validation: `bot-check --owner-config /var/lib/battlecode-volume/config/beta.json`
exited 0, trusted state PASSED for exact source
84ce3be7f5068fd196cd564885f695db7e16f2cb6a4ee7666c9ce65502812dac.
Local report: .agent/check-task-32b6f4ccb8f54f1ead2a0e7c4bdcac48.json.
Trusted report reference (not opened):
/srv/battlecode/checks/task-32b6f4ccb8f54f1ead2a0e7c4bdcac48/84ce3be7f5068fd196cd564885f695db7e16f2cb6a4ee7666c9ce65502812dac/report.json.
Smoke IDs: be056629b1e4078cdbece1b33ca797604a8c0c499e3258a8e7bcd2d7f3531e90,
dd323d9eaf593d61d741b183db014d7034fdd4ad0a3c554455fb9cd2b50e9c90.
The trusted wrapper requires completed, fault-free games on both sides for
PASSED (arena/supervisor.py check_source). `git diff --check` passed. Smokes
establish execution validity, not strategic improvement or per-turn fuel use.

## task-3b818b28bcb04cca83683548f6c579dc — collect cleared camps first

Playbook C. Hypothesis: prioritizing visible reward-available groups before
basic attacks on other camps reduces delays between clearing and collection.
Falsifiable expectation: when farming on a reward-available group's spawn tile,
the champion holds position; otherwise a successful step toward a cleared group
ends farming for this turn, even when another camp was initially attackable.
Unreachable/blocked capture goals fall back to baseline farming. Once captured,
respawning state removes the capture priority. Combat, banking, recall and
channel priorities outside farm_camps remain unchanged.

Identity: bot beta, branch bot/beta, HEAD/input
`d929b5e61078ce87da57906f59d6887216434770`. Working and accepted-snapshot
source hashes both matched baseline above before edits. Initial diff reset the
prior candidate, as arena/worker.py make_attempt explicitly restores accepted
source. No interrupted edits or pending evaluation: supplied feedback
`17ac318eeb4ef7475c3af14f6c08d4b83bc884c31ef0043caf63f5770b735ef0`
is INCONCLUSIVE. Documentation hashes match RESEARCH.md. Accepted snapshot
remains outside the edit transaction; separate organizer AGENTS.md unavailable.

Evidence: feedback evaluates source
`4a47b50ba1d4170055dba73a6b3abdf1788967dbe44ec4135b3e722830b66947`,
not the baseline or this patch. Losses include corners B,
`d23d5734931588329ef179f082c6a33730618f9d852b80e3f394c1ad8ac022b8`
(230 collected, 124 submitted, 16 deaths), and elkring A,
`ac94627a35ddedbc1f0d258cf11b373406ba506e750384d54c624e60bcbffdce`
(522 collected, 324 submitted, 43 deaths). No reported bot faults. These totals
motivate economy inspection but do not prove missed captures. Capture completion
and turn traces are unavailable. Source proves in-range camp attacks precede
movement onto cleared spawn tiles. Rules GameRules.md:191–205 require uncontested
spawn occupancy for five rounds. Installed C++ SDK camp_group_reward_available
means all camps defeated; vision::camp_groups filters by current visibility.

Change: within farm_camps, union visible cleared spawn tiles, hold if already
occupying one, otherwise attempt capture movement before ordinary camp attacks.
No extra shared memory or policy thresholds. Existing movement fallback and
main.cpp end_turn are retained. This is a single farming-priority experiment.

Remaining uncertainty: capture benefit, duplicated collectors, contested groups,
and fuel headroom are unmeasured. Prioritizing an occupied/unreachable group may
still fail and use baseline fallback; no safety or strength improvement claimed.
Next action: supervisor evaluation against accepted baseline; measure collection
delays if bounded traces become available.

Validation: `bot-check --owner-config /var/lib/battlecode-volume/config/beta.json`
exited 0, state PASSED for exact source
`c35aa333ec97f25235b09630777b16febbac86cd80423946d2065bb2321ccf02`.
Local report: `.agent/check-task-3b818b28bcb04cca83683548f6c579dc.json`.
Trusted report reference (not opened):
`/srv/battlecode/checks/task-3b818b28bcb04cca83683548f6c579dc/c35aa333ec97f25235b09630777b16febbac86cd80423946d2065bb2321ccf02/report.json`.
Wrapper smoke IDs:
`403003eb4b1fc7840a2ff4a8bcf05200d610b8120dd2ea7fb6618a1490cb6154`,
`3fd672d4f5f86dc4aaecc2da0a78b3f7f11d566f0c393d653f70a8c14a54c9e1`.
The trusted wrapper requires completed, fault-free games on both sides for
PASSED (arena/supervisor.py check_source). `git diff --check` passed.
These smokes validate execution, not the capture hypothesis or improved strength.
