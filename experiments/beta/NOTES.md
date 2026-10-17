# Operational summary

## task-d5ef7f6c9874483a9382f7fc82e50e1f — guarantee a splash farmer

Playbook E (draft composition). Hypothesis: selecting Varg before the existing
random remaining picks guarantees a basic-attack splash farmer, shortening
multi-camp clears and improving collected/submitted gems under the accepted
attack-only policy. Falsifiable policy invariant: every normal 3–5-pick draft
starts with exactly one Varg; later picks are legal, distinct remaining choices.
Every draft turn still consumes one existing random selection, and champion
play remains byte-identical to accepted. Strategic benefit requires evaluation.

Identity: beta; bot/beta; task-d5ef7f6c9874483a9382f7fc82e50e1f.
HEAD/input 24c06ca235ebf67a730eebfc5fa8163190172299; accepted edit start
0ca5c04ecf26a8fa677ef2ac2b9af249b688a5d9; base source
9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
All six source files matched accepted Git blobs before editing. Initial
bot.cpp diff against HEAD is trusted restoration, not unfinished work.
Accepted Git and supplied snapshot preserve baseline outside this transaction.
Latest prior task PUBLISHED/evaluated, not awaiting evaluation; pending
continuous self-play jobs do not replace its completed canonical evaluation.
Earlier recovery artifacts preserved; previous summary archived through
task-da50c1aeba344934bf1b0d69b529d7be.
Engine/SDK 2.1.6; lock
00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668;
suite historical-panels-v1. Documentation unchanged per trusted handoff;
compact reference, Playbook E, relevant rules and C++ draft contracts read.
Separate organizer AGENTS.md remains absent.

Evidence context: evaluation
a582f63a7be21a142650908698abcb0b74169100c55164932c0a6871c026d29f
for candidate 24c06ca235ebf67a730eebfc5fa8163190172299, source
55d70a726fed2422dac95fb0ce87a701fc6a81be3bbb473fa1fa57e2495ce48f:
INCONCLUSIVE/provisional-three-map-wiring, 5W/19L, zero reported faults,
missing or unknown reliability. Collision losses:
0bb352b7edcc6a49b3b87db090d61b13a59594202cfda05a88aca1d14178ff02 (B),
3b0abaa2ee94639ee676bdd879fb8d249cc67d8051a0110325c4c764c0e4cb49 (A).
Development means: 618.92 collected, 487.5 submitted gems, 26.92 deaths.
These evaluate the Monolith-exclusion candidate, NOT the restored source.
No engine/bot failure evidenced. No draft/clear-time trace establishes cause.
Source reproduces uniformly random distinct draft picks with no guaranteed
splash farmer and no ability casts. Previous compact experiment records cover
banking, shopping, capture, spells and Monolith exclusion, not this draft policy.

Contracts: GameRules.md:48–69 gives 3–5 unique own picks; opposing choices do
not exclude ours. :169–205 requires all grouped camps dead before capture.
:767–788 gives Varg Strength splash radius one, excluding a second primary
hit, and melee movement/basic attacks. Installed cambc.h:261–285 exposes Varg
as a released draft choice; :4957–4990 provides completed own picks and pick().
Policy uses only the legal available list and adds no memory layout or roles.

Implementation: draft.cpp retains its existing own-team exclusion list and
random available fallback, then selects Varg only through a found iterator in
that same list. Varg is therefore first and cannot be repeated. There remains
one RNG draw and one official pick per draft turn. No fixed team size is added.
All five non-draft source files remain byte-identical to accepted. Existing
main.cpp dispatch/yield, memory contents and champion decision code preserved.

Inline `python3 -` scope/legality assertions PASSED, exit 0. Report:
experiments/beta/task-d5ef7f6c9874483a9382f7fc82e50e1f/draft-invariant.txt.
The source comparison bounds the change to this draft preference. Independent
contract enumeration covers all 5,850 remaining-choice orderings for 3–5 picks.
This is source/contract evidence, not C++ execution or an engine simulation.
`git diff --check` PASSED, exit 0.
Trusted command:
`bot-check --owner-config /var/lib/battlecode-volume/config/beta.json`
PASSED, exit 0; exact candidate source
f92d77a6923a38854bbfd899b558bf6762a313a98bd1eafa23baa5ff36f04ff8.
Report: .agent/check-task-d5ef7f6c9874483a9382f7fc82e50e1f.json.
Reference: check:task-d5ef7f6c9874483a9382f7fc82e50e1f:f92d77a6923a38854bbfd899b558bf6762a313a98bd1eafa23baa5ff36f04ff8.
Smoke IDs:
9f3f6a21a281a448a9384dacf48fd63747f1af457d5940e392f882149c0dc042,
62bb059654452273f80002539dbfecb855e47a8ceafd86012ec509c66648949d.
The trusted wrapper validates compilation/smoke for this exact source. Its
local summary exposes no completed-game outcomes, camp-clear timing or fuel
trace; success does not establish improved farming or playing strength.
Uncertainty: splash can wake multiple monsters and increase incoming damage;
Varg displaces another champion and can underperform on isolated camps. Its
unused reset/shield remain unused. All other random picks can change downstream
as the available list changes; same RNG-call count does not mean same team.
No claim of improved strength, actual clear speed or fuel headroom.
Next: supervisor evaluates exact checked candidate against accepted; compare
collected/submitted gems, deaths and grouped-camp clear times if available.
