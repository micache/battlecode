# Operational summary

## task-41dc854784904d468837b2cde087ddc6 — finish weak camps first

Playbook D. Hypothesis: selecting the lowest-current-health visible, living
camp in basic-attack range instead of the first vision entry will finish kills
sooner, reduce active monster damage, and improve collected/submitted gems.
Falsifiable invariant: each pre/post-move farming attack chooses minimum
positive health among currently visible in-range camps; ties retain vision
order; no attack when unavailable or no legal target exists.

Identity: beta; bot/beta; HEAD/input 33d663b92cc2f3a0d73ad340922fefb5e287acc6.
Accepted edit start 0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9; base source
9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
All six initial source files matched accepted Git blobs; initial draft diff
against HEAD is trusted restoration. Accepted Git preserves the baseline.
Latest prior task PUBLISHED and evaluated, not awaiting evaluation. Existing
recovery artifacts preserved; prior notes archived through task-d5ef7f6c9874483a9382f7fc82e50e1f.
Engine/SDK 2.1.6; lock
00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668;
suite historical-panels-v1. Handoff says docs unchanged. Read compact reference,
RESEARCH.md, Playbook D, rules camp section and relevant installed C++ bindings.
Separate organizer AGENTS.md remains absent.

Evidence: evaluation e1336f6c8b194df9a8157bc1dac04ab94b9b3be81b2aca0f35f5491d35e0eadd
is INCONCLUSIVE/provisional-three-map-wiring, 4W/20L, zero reported bot faults,
missing results or unknown reliability. Candidate commit
33d663b92cc2f3a0d73ad340922fefb5e287acc6, source
f92d77a6923a38854bbfd899b558bf6762a313a98bd1eafa23baa5ff36f04ff8.
Collision losses: 62bb059654452273f80002539dbfecb855e47a8ceafd86012ec509c66648949d
(side B), 2d0104f003e493c691371a6b98e5882022bccff3871c9b1e69ce4d597e051554
(side A). Development means: 588.08 collected, 453.75 submitted, 28.125 deaths.
These evaluate the Varg draft candidate, NOT restored accepted source.
No engine/bot fault evidenced; strategic losses motivate throughput work.
No match-level targeting trace establishes this cause. Accepted source itself
reproduces first-entry targeting regardless of relative camp health, both
before and after moving. Prior archived experiments do not test this priority.

Contracts: GameRules.md:169–205 gives monster damage, death and group capture.
Installed cambc.h:2931–2960 requires visibility for live health/position;
:4826–4837 returns a fresh owning vector of visible camps on each call.
Thus selection pointers remain valid until the local vector is destroyed;
no persistent camp handle/cache or hidden-state query is introduced.

Change: bot.cpp adds one linear scan for minimum positive health after
visibility, attack-availability and range guards. One cached range mask per
selection. Existing attack_if_in_range revalidates the selected camp. Farming
calls it before movement and again with fresh observations after successful
movement. No movement/routing, enemy target priority, draft, items, channels,
shared memory, RNG or main.cpp dispatch/yield changes relative to accepted.

Checks: `python3 experiments/beta/check_weak_camp_targeting.py` PASSED, exit 0;
report experiments/beta/weak-camp-targeting-invariant.txt. Source checks verify
strict-minimum ranking, visibility before live queries, range/alive/availability
guards, fresh post-move selection, stable ties and accepted-source scope.
Accepted source and six unsafe mutations are rejected. Initial run failed in
the test harness because one mutation matched the earlier generic helper;
scoped that mutation to the selector and reran successfully. Bot unchanged.
`git diff --check` PASSED, exit 0.
Trusted command:
`bot-check --owner-config /var/lib/battlecode-volume/config/beta.json`
PASSED, exit 0, exact candidate source
fc461f9ba86b39b60ee220037052685a761354cf0fc4eb9926c41e01deebeb93.
Report: .agent/check-task-41dc854784904d468837b2cde087ddc6.json.
Reference: check:task-41dc854784904d468837b2cde087ddc6:fc461f9ba86b39b60ee220037052685a761354cf0fc4eb9926c41e01deebeb93.
Smoke IDs: 951ac3e753f23fbbe47d3f7ee45ea9b43d4fd712a781e058437e4599c02b6d94,
965700180b56d908ebe1dce2ad1feae1875c35ab11389282fc5af1ab2f2f026a.
Trusted compilation/smoke passed; local summary does not expose completed-game
outcomes, target-order trace or fuel measurements.
Uncertainty: lowest health is not minimum hits under target-dependent damage;
may prefer harmless clusters or switch groups and delay capture. No actual
kill-order, fuel headroom or strength claim. More visible candidates require
more health queries; trusted smoke does not measure remaining fuel.
Next: supervisor evaluates exact checked candidate; compare collected/submitted
gems and deaths, and first-entry versus selected target/kill timing if available.
