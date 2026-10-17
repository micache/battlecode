# Operational summary

## task-3bd44d5f08a2471e9caede76707138de — finish spawn recovery

Playbook C. Hypothesis: returning before field actions when injured on allied
spawn prevents leaving before the turn-end heal after recall. Falsifiable
expectation: after normal channel/alive guards and shopping, health < max_health
on allied spawn returns without movement/combat/banking; full-health champions
and injured champions away from spawn keep the existing policy. This should
reduce low-health departures and repeat recalls; win-rate benefit is unmeasured.

Identity: beta, bot/beta, HEAD/input 29355cc80fddebe918e9d896de2ee430d8c64852.
Accepted commit 0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9; base source
9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
All six source-file hashes and git blobs match handoff.edit_start before editing.
Engine 2.1.6, lock 00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668;
suite historical-panels-v1. Matching installed C++ header SHA-256 verified.
All documentation hashes match unchanged reviewed manifest; routine targeted
reading only. Separate organizer AGENTS.md remains unavailable.
Accepted source is preserved by accepted_commit and supplied accepted_snapshot;
no duplicate source backup. Initial bot.cpp diff is the trusted source restoration.

Prior task-8f47664e32194d58986ac9ee549f9482 failed before task reads; inspected
its exact notes, final and checkpoint patch at supplied own-attempt paths.
Its patch only restores accepted source; trusted handoff confirms unchanged
source and infrastructure repair. Original artifacts remain preserved in place.
No candidate awaits evaluation. Previous shopping candidate was REJECTED:
evaluation 2ea4885729559a546c94274b9c4449cd312a00fa2e5fb02c1e20e5ba2aa6aedb,
source 3036b3fac8c535a946dee4a06be419d84110294e7afec6621600d6073fa1504c,
commit 29355cc80fddebe918e9d896de2ee430d8c64852, 23W/31L, delta 0, faults 0.
That evaluated source is not this task's edit start. Previous notes archived in
archive/through-task-a291761b3e4d4f59b5a9ae5abde282b8.md.

Evidence: collision B losses
- efa28f2261380bab9d77cd9c5cbdaeb7a019b9984789675e2f2537d690fef722:
  round 1448, B deaths 36, submitted 814 vs 1012, faults 0.
- 5c6e08600b83c3a52c717c5541d2d8b37244d97a28e7728cec63a6bb208c77e9:
  round 1072, B deaths 29, submitted 396 vs 1012, faults 0.
These are development observations of the rejected shopping source. No trace
establishes missed heals caused these losses. They motivate recovery safety,
not a measured diagnosis of those games. Source reproduction: wounded at spawn,
no enemy in range, reachable off-spawn goal -> existing policy may leave before
healing. Rules GameRules.md:122,355–375 and BOT_REFERENCE.md section 3 confirm
recall resolves at turn start and staying until turn end heals fully.
SDK self health/max_health and spawn_region contracts support the guard.

Implemented: after spawn shopping, return if at_spawn and health < max_health.
No new state, thresholds, RNG or search. Existing main.cpp still always yields.
Focused invariant: `python3 experiments/beta/check_spawn_recovery.py` exited 0;
report experiments/beta/spawn-recovery-invariant.txt. Checks guard placement
before field actions and rejects accepted source plus either missing condition.
This is a source control-flow check, not an engine-level heal/turn trace.
`git diff --check` exited 0. Accepted-to-candidate source diff is four added lines
in bot.cpp; all other source files remain accepted.
Trusted command: `bot-check --owner-config /var/lib/battlecode-volume/config/beta.json`
exited 0, PASSED, source
02a532272622522f2c853fe557c16d98633bdd7898e75e4a82a03a311968b6b1.
Report: .agent/check-task-3bd44d5f08a2471e9caede76707138de.json.
Reference: check:task-3bd44d5f08a2471e9caede76707138de:02a532272622522f2c853fe557c16d98633bdd7898e75e4a82a03a311968b6b1.
Smoke IDs: c945febbac03d615865d96d373f9148483cec90a7678353bd9ae274031314061,
41efe090e544212ddd5e6ee89a9f32036948607317379892eb0d0cdf9733bd8a.
No turn-level recovery behavior or strategic improvement inferred from PASSED.
Remaining uncertainty: frequency of missed recovery, repeated recalls, fuel
headroom and strategic benefit are unmeasured. Extra spawn turns could delay
banking or routes; no claim of completed evaluation or stronger play.
Next action: supervisor evaluates the exact checked candidate against baseline.
