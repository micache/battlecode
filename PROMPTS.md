# Copy-and-run task prompts

Copy the pack into your private project repository. Fill in the repository/host/owner details when you have them. These prompts request implementation and bounded coding work; they do not purchase infrastructure or authenticate teammates automatically.

## 1. Arena implementation agent

```text
ROLE: arena_implementer

Implement the Battlecode arena specified by README.md and ARENA.md in this repository.
Read AGENTS.md, RESEARCH.md, RULES_CHECKLIST.md, AUTH_AND_OPERATIONS.md,
BOT_REFERENCE.md, both supplied exports under sources/, and the example
config/schema before editing. Follow the selected simple architecture.

Project inputs:
- Private repository: <REPO_URL>
- Persistent Linux server / SSH alias: <SERVER_OR_LOCAL_IMPLEMENTATION_ONLY>
- Registered account owners and bot IDs: <OWNER_MAPPING_OR_CONFIG_PATH>

First inspect the existing project and current official cambc documentation/CLI.
Preserve existing code. Resolve event/SDK/engine mismatches before integrating.
Finish the rule ledger where access permits, retaining UNKNOWN for anything you
cannot verify. Do not invent a challenge API, seed flag, result schema, or quota.
The supplied exports now establish the game rules and Python API; do not mark
them unread. The separate organizers' AGENTS.md and platform policies are still
missing. Validate runtime settings against the documented 1,000-gem/2,000-round
profile, language fuel multipliers and 1,024/8-byte memories. Verify Team B wins
a complete tie. Keep fuel suspension separate from crashes and host timeouts.

Build the private runner adapter, durable queue, immutable Git ingestion, result
normalization, evaluator, feedback exporter, one-account worker supervisor,
operator commands, and systemd templates. Start with one lane. Use the official
runner and deterministic host-side summaries. Add the remaining lanes only after
the end-to-end loop works. Provide a manual external-result import path; official
submission/challenge automation stays disabled until verified and configured.

Keep the implementation small. No dashboard or distributed infrastructure is
needed. Separate bot execution from credentials. Use the exact acceptance gates
in ARENA.md. Run real-engine smoke checks when dependencies are available and
distinguish them from mocked scheduler tests. Do not spend subscription calls
just to poll, and do not enable API billing or account rotation.

Complete all implementation and tests that available access permits. If remote
deployment details or owner login are missing, deliver a concrete installable
change and precise next operator steps; do not claim deployment or tests passed.
Report files changed, tests actually run, remaining blockers, and the shortest
commands for an owner to install and start the first lane.
```

## 2. First bot bootstrap

```text
ROLE: bot_worker

Use $battlecode-strategy for the foundation task in .agent/task.json.
Follow current AGENTS.override.md when prepared, otherwise AGENTS.md.
Confirm my bot ID, owned branch/path, edit-base source hash, and engine version.
Read PLAYBOOKS.md A, BOT_REFERENCE.md, complete GameRules.md and the applicable
API export (BotAPICpp.md for C++) at bootstrap, plus the matching installed binding. If an existing playable bot
is assigned, preserve its language and establish its baseline. Otherwise create
a valid complete bot from the pinned official starter in my owned bot directory.

Design the strongest coherent objective-winning strategy you can implement within
this invocation: draft/roles, efficient economy and capture, banking, combat and
abilities, recovery/items, navigation and bounded coordination. The starter is a
starting implementation, not a strategic ceiling. Coupled multi-file upgrades are
allowed. Preserve legal actions, yielding, normal fuel and a safe fallback. Use
current SDK calls/settings, not assumptions from the older Cambridge game. State
which claims follow from rules/source and which have been measured.
Choose free reachable approach tiles, complete uncontested captures, and let
useful channels finish at the next turn start after their timer reaches zero.
Budget only 8 writable live shared bytes for the entire team. Yield before fuel
suspension with measured headroom. Do not copy malformed export examples blindly.

Use the approved bot-check wrapper. Write compact persistent notes and return
the structured result. The supervisor publishes and evaluates the candidate.
Stop after this one task. Do not publish to the official competition platform.
```

## 3. Recurring improvement job

```text
ROLE: bot_worker

Use $battlecode-strategy for exactly one task from .agent/task.json.
Follow current AGENTS.override.md when prepared, otherwise AGENTS.md.
Read my NOTES.md and the supplied latest completed feedback. Verify the feedback
belongs to the recorded candidate, opponents, maps, and engine settings.

Choose the highest-value coherent strategy upgrade using relevant PLAYBOOKS.md.
Consult BOT_REFERENCE.md and relevant source sections without rereading the whole
API every time. Re-read complete exports when their hashes change. Preserve the
documented win/tie semantics, fuel behavior and memory limits in all changes.
Read current documentation under .agent/knowledge/ and inspect supplied frozen
arena opponent sources to infer strategies and counters. Start with representative
development losses and contrasting wins; fetch further targeted evidence only
when it changes the decision. Consider alternatives internally, then record a
concise strategy hypothesis, evidence, expected gain, risks and falsifier, not a
reasoning transcript. Implement a complete coherent candidate in owned paths;
multiple coupled systems/files may change. There is no diff-size target. Run the
approved checks and save lessons, current strategy and negative evidence.

Return the worker-result schema. READY_FOR_EVAL is a proposal for evaluation, not
a claim of improvement. Return NO_CHANGE if evaluation is pending or no useful
change is justified. Return BLOCKED for missing identity, required access, or
unavailable checks. Do not wait for matches, spawn more agents, alter the evaluator,
switch accounts, or enable paid fallback. End after one experiment.
```

## 4. Resume after interruption or laptop handoff

```text
ROLE: bot_worker

Recover the task identified in .agent/task.json. First verify the supervisor's
ownership lease and expected branch tip. Read the prior checkpoint, patch, raw
task result, and evaluation state. Preserve incomplete work before changing it.

Determine whether the interrupted task needs completion, was already published,
or already has a completed evaluation. Reuse the immutable IDs and do not publish
or score duplicates. Continue the one recorded hypothesis if still valid; otherwise
explain why it is obsolete. Finish with the structured result and compact notes.
Do not reset the checkout or assume that the newest branch tip is the champion.
```

## 5. External challenge setup and import

```text
ROLE: arena_implementer

Verify the official unranked challenge workflow described in ARENA.md using the
owner's authorized current documentation/access. Do not create a match as part
of this verification task. Establish the permitted interface, rate limits,
submission selection, activation effects, replay visibility, and version metadata.

If automation is not clearly supported, finish the manual challenge/import path.
If it is supported, implement a disabled-by-default single-publisher adapter with
immutable source-to-submission mapping, rate-limit handling, and reconciliation
for uncertain remote creation. Preserve all platform restrictions.

For imported completed matches, verify our submission identity, retain raw files
and checksums, and publish compact findings to the relevant bot. Unknown opponent
versions remain unknown. Do not claim external results are controlled local tests.
```

## 6. Periodic strategy review

```text
ROLE: reviewer

Read the supplied compact cross-bot report and selected evaluation IDs. Identify
the most valuable unexplored weakness, a useful diverse opponent to retain, and
at most one promising idea to transfer between bots. Separate reliable findings
from small-sample or changing-opponent effects. Produce a short prioritized task
proposal for each owner lane; do not edit their bots or dispatch new model jobs.

The next combined bot must be a separately evaluated candidate. Do not infer that
two improvements measured independently will remain improvements when combined.
```

The supervisor should inject concrete paths, IDs, hashes, and limits into the task envelope, not continually expand these prompts with the entire match history. The same prompts apply locally and remotely; ownership and source identity must be explicit in both cases.

Each bot keeps one long-lived branch. The publisher adds a normal commit for each valid candidate; it does not create a new branch per update. The arena freezes that commit SHA for each evaluation.
