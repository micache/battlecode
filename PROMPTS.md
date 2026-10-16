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

Perform the bootstrap task in .agent/task.json. Follow AGENTS.md.
Confirm my bot ID, owned branch/path, accepted source hash, and engine version.
Read PLAYBOOKS.md A, BOT_REFERENCE.md and the complete supplied GameRules.md and
BotAPIPython.md at bootstrap, plus the matching installed language binding. If an existing playable bot
is assigned, preserve its language and establish its baseline. Otherwise create
a valid complete bot from the pinned official starter in my owned bot directory.

First prioritize correct draft handling, legal actions, yielding, bounded fuel,
basic navigation, camp farming, gem submission, and a safe fallback. Use current
SDK calls and settings. Do not copy assumptions from the older Cambridge game.
Do not optimize several systems before a measured baseline exists.
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

Perform exactly one improvement task from .agent/task.json under AGENTS.md.
Read my NOTES.md and the supplied latest completed feedback. Verify the feedback
belongs to the recorded candidate, opponents, maps, and engine settings.

Select one high-value failure pattern and use the matching PLAYBOOKS.md procedure.
Consult BOT_REFERENCE.md and relevant source sections without rereading the whole
API every time. Re-read complete exports when their hashes change. Preserve the
documented win/tie semantics, fuel behavior and memory limits in all changes.
Inspect only the relevant code and at most three representative replay/log slices.
State a falsifiable hypothesis, make the smallest useful change in my owned paths,
run the approved checks, and save what you learned, including negative evidence.

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
