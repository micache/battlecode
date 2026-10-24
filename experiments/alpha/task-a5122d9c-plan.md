# Proactive support implementation plan

Goal: test whether support independent of successful combat improves objective throughput.
Authority: one autonomous bounded candidate per trusted task. User forbids agents,
commits, publication, new worktrees and waiting for evaluation; those override
interactive design/implementation skill defaults. Implement inline in owned paths.

## Decision
Bottleneck: camp exposure remains material, while existing support requires a
successful basic/spell first. Willow cannot heal during travel, capture, banking
approach or recovery, and Varg cannot shield before a threatened melee approach.
Latest loss fbf8281b...ba84e6, A/00ambush, d94b461d/f7e2d6b1: own camp damage
50952 versus champion damage 4300, 18 deaths and 585 collection. These statistics
do not identify cast opportunities. Frozen boss ea15ef0f/f4b4f65e calls support
before main decisions. Transfer timing, not its draft/routes/items or fixed HP rule.

Hypothesis: early exposure-aware self shields and efficient ally heals increase
matched wins and tribute over dd7c6c99. Nonpositive matched win gain falsifies it;
deaths, shielding/healing, collection and reliability diagnose the mechanism.

Alternatives: another item portfolio has only +0.01081 development delta in latest
experiment; wait for supervisor selection rather than reuse it. Camp focus,
routes, capture, retreat and drafts have prior negative/deferred findings. Choose
support timing as a distinct mechanism. Do not alter those systems.

Policy: ready walking-compatible support before recovery/combat/bank/farm. Self
shield only under personally visible damaging awake-camp or enemy basic range,
without an active shield; require HP <85% or expected duration*raw volley >= half
shield. Heal a visible living nonself ally outside spawn with >=50% heal efficiency
and HP <85%; rank actual useful heal with urgency. Healing competes with reset.
Use SDK amount/range/readiness, max16 observations, 50k entry/38k scan reserves.
No hidden reads, memory changes, rerouting, self-heal or fuel inflation.

## Steps
- [x] Add failing source integration/preservation regression; observe RED.
- [x] Add support_policy.h pure scoring contracts and bounded proactive cast helper.
- [x] Integrate after spawn care, before retreat; remove old combat-only support.
- [x] Run source contracts and trusted bot-check; inspect diagnostics and smokes.
- [x] Self-review legality, fuel, channel preservation; update compact NOTES.

Review focus: no healthy quiet shields, no active-shield overwrite, no Willow self
heal or spawn-heal waste, visibility before live queries, cast/walk compatibility,
no turn lost just because support cast succeeds, budget guards on scans. Partial
threat scan can justify a shield but cannot certify safety. No safety inference.
