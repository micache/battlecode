# Cooldown-aware shortlist rotation

Hypothesis: excluding observed camp downtime and active route retries before
the bounded shortlist, while vacating claimed regions when idle, improves
submitted gems and matched wins versus 50a0d7d5 / 6d66a77f. No win gain,
lower submissions, or increased deaths/faults/fuel suspension falsifies it.
The causal mechanism is an unmeasured source/rules deduction.

Bottleneck: the edit base selects twelve groups by geometry, then discards
respawning and retry-delayed groups. Those entries can consume every slot
repeatedly. It forgets observed respawn timers and can remain on a collected
gold-only group if the resulting scan finds no work. Occupancy delays respawn.

Evidence: evidence.json records exact edit/input/evaluation identities and
separate same-source self-play. Interlock A loss ce4f287e (round 608) has
810:1024 submitted, one own death, 22 lost gems, no faults/suspensions;
fragment B loss 4413ca20 (round 558) has 308:1003 submitted, five own deaths,
58 lost gems, no faults/suspensions. Both use edit source 6d66a77f against
7ed7e6a3. Collision on that same source contrasts with 2W/0L per side in the
supplied self-play window; individual winning IDs are unavailable. These final
statistics motivate throughput work but do not prove the proposed turn-level
mechanism. No replay omniscience becomes runtime information.

Frozen-source adaptation: alpha 046f1c3a / 07022bad's camp_rotation.h and gamma
63d05e37 / a4d664c8's bot.cpp use timestamped observed cooldowns. Reuse the
observation discipline inside beta's existing bounded group planner. Do not
import their complete scheduler/composition. Frozen files do not establish
official opponents' strategies or the source of either historical self-play foe.

Policy: private per-group last-observed round/earliest respawn/valid flag.
Positive remaining timers exclude only before expiry; zero excludes the
observed round only. Expiry means unknown, never assumed alive. Only currently
visible state records/clears observations. Remove cooldown/retry entries before
partial_sort; preserve original geometry, twelve-group cap and fuel reserves.
An occupied reward-available group is held before deferral filtering. On a
no-work result, one normal legal move attempts to leave an occupied respawning
region. No additional field or broad live-state scan, no shared-memory writes.

Alternatives rejected: repeat gold-only penalty (latest candidate +0.044643
matched development delta but collision/interlock regressions; edit base was
retained); restore the full reachable reward/time scheduler (prior +0.041667
with interlock regression); speculative roster/combat changes. This isolates
cooldown rotation from the earlier scheduler's changed scoring/path costs.

Expected observation: fewer turns with a full rejected shortlist and improved
gem participation/submissions, especially on dense camp maps. Risks: earlier
travel toward unknown/riskier groups, different farming routes, extra occupied
group query, and opportunities lost to the unchanged geometric twelve-slot
cap. Existing gold loops and combat deaths can remain. Actual mechanism
coverage and fuel headroom are unmeasured.

Validation: trusted check PASSED/0 for exact source e05d7dfc0b99af0c3e7f7154858e09ce04eb23d472db8ed1ae5ec08b1c1078bf;
check-report.json records both smoke IDs. Boundary assertions compile with
the bot. rotation-contracts.txt rejects five unsafe integration mutations;
invariants.txt retains existing seven-mutation safety checks. Smoke own stdout
is empty on both sides; that does not prove completed competitive games or
strategic gains. Supervisor owns matched evaluation and promotion.
