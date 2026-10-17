# Current experiment: task-2609ebf30ef34c9eb5ec2dfb854822a1

## Identity and prior work
- Bot alpha; branch bot/alpha; input HEAD bfd7a947b2bc90ab52804ad2ff8730586591b3d3.
- Edit start accepted commit c0cebd720fcd55e2bbb51d57dd2c398889d4071e;
  base 9e804e3e3e2d0c183cd5badd983c2bacea7679788942d22df764f785ff0e115f.
- Engine/SDK 2.1.6; suite historical-panels-v1; engine lock
  00c70d6c0d9a4bb9525fb53cd9d4db56f12270b38b08431e9d4803a70a9ea668.
- Entry identities, six accepted source files, unchanged documentation and installed
  C++ header verified; saved in this task's -identity.json. Accepted Git snapshot
  remains outside this edit. No full bootstrap reread on unchanged documentation.
- Latest candidate evaluated INCONCLUSIVE, not pending. Prior NOTES archived as
  task-fc527578bbbf42f5be88544f50e93a50.md. Older interrupted patches/notes were
  already preserved in owned experiments; none recovered/applied in this task.

## One hypothesis: playbook C, banking before optional combat
Giving gem carriers priority to submit or move toward an altar before attacking
an enemy will increase mean submitted gems versus accepted source on matched
development cases. Unchanged or decreased mean submitted gems falsifies this
prediction. Compare collected gems, deaths and outcomes for opportunity cost.

## Evidence and focused change
- Evaluation 59f8b837255ea5741a43c9ba25e2decf1021f80085ba5edd5aed7d97bd10bcc2:
  source de641864b31c9d6705aed5fdb4f9c7c9e5f1a4c643df09a614ba88324dce0f14,
  commit equal to input HEAD; revision
  a945c76d5f9ee326e6c26e0b8dc34e9fb1772381da5be6ef2a285126ba5e64dc.
  This evaluated capture-policy candidate is NOT the accepted source edited here.
- Collision B losses a5d7998141b8ec5fc8db16146e566a93115cdd7529986eb4d2d826bffe769f6a
  and d6c71981ae4f2f229f135f48ef91a0ae1893255c57e4d490bf950291afbe24d3:
  collected 858, submitted 660, carried 22, deaths 36, round 1314; zero faults
  on both sides. Identical finals are not independent causal observations.
- Collision A loss 5f0f867895e849a5955a63991814b810600e6334e18221a006c83b482ffe6196:
  collected 880, submitted 572, carried 22, deaths 21, round 1163, zero faults.
- Supplied metrics preserved in this task's -evidence.json. These are strategic
  losses with conversion deficits; no identified engine failure or bot fault.
  No action trace: missed banking opportunities and bag loss causes are unknown.
- Accepted source attacks any in-range enemy before banking, always returning.
  A carrier can repeatedly defer tribute; a ranged basic also consumes walking.
- Move existing bank block before enemy targeting. Return after tribute start or
  successful movement. Failed bank movement falls through to a fresh enemy scan;
  carriers then return instead of farming. Empty champions retain prior behavior.
- Recall, channel preservation, tribute range/lock checks, navigation and yield
  dispatcher retained. No added thresholds, shared state or random draws.
- GameRules.md 116, 217-241: ranged walking/basic share allowance; carried gems
  do not score; ordinary damage does not cancel tribute. SDK cambc.h 3690-3694:
  submit_gems returns void. Existing conservative either-team lock policy retained.
- Read compact reference, playbook C, relevant rules/SDK, and RESEARCH.md.
  Separate organizers' AGENTS.md remains unavailable.

## Validation and uncertainty
- python3 experiments/alpha/check_banking_priority.py --report
  experiments/alpha/task-2609ebf30ef34c9eb5ec2dfb854822a1-source-check.json
  PASSED, exit 0: source ordering, channel/recall guards, fallback and no carrier
  farming invariants. Static checks do not establish runtime legality or benefit.
- git diff --check PASSED, exit 0. Accepted-relative diff reviewed.
- bot-check --owner-config /var/lib/battlecode-volume/config/alpha.json
  PASSED, exit 0; exact checked source
  4db7aeeb7fca7b20464d7f97c4d79cd29d68cbcaad8080ea5030192fa29fb322.
  Report: .agent/check-task-2609ebf30ef34c9eb5ec2dfb854822a1.json;
  preserved as this task's -bot-check.json. Trusted reference:
  check:task-2609ebf30ef34c9eb5ec2dfb854822a1:4db7aeeb7fca7b20464d7f97c4d79cd29d68cbcaad8080ea5030192fa29fb322.
- Smoke IDs 2fe077d901e43199eb19d052f132f38a609e2025058c7357ac80f4f5d1b4b26b
  and e582c916948f90167a6a14dae7c421d61090a40d9472fcd1a0c8f61b5f817539.
  Smoke finals not inspected; IDs alone do not establish completed full games.
- Outcome READY_FOR_EVAL; no tournament evaluation or improvement claimed.
- Risks: carriers may walk into hostile pressure instead of finishing a kill;
  foregoing melee attacks may reduce deterrence. Recall still preempts banking
  below 35% health. Hidden locks and entirely locked routes remain limitations.
  Fuel headroom and frequency of delayed-bank situations are unmeasured.
- Next: supervisor evaluation of exact checked source against
  accepted source; compare mean submitted gems, collection, deaths and outcomes.
  If conversion fails to improve, inspect carrier combat/route traces next.
