# Quota efficiency: high reasoning, less repeated work

17 October update: improvements now follow a one-hour per-bot schedule, not a
fresh-feedback trigger. Matches continue between invocations; development
results are compressed by immutable source/map/side, with exact evidence kept.
See [Claude and hourly operation](CLAUDE_AND_HOURLY.md) for the third lane and
the unchanged quota, evaluation and promotion guards.

Both lanes retain `gpt-6.1-sol` with high reasoning. Subscription-only native
authentication, account isolation, one concurrent model job, quota waits and the
full promotion gate remain unchanged. No paid overage, API fallback, account
rotation, extra model reviewer or automatic model downgrade is introduced.

OpenAI documents that task complexity, context, reasoning, tools and caching all
affect allowance use; prompt size alone is not a quota estimate. See
[current Codex pricing/limits](https://learn.chatgpt.com/docs/pricing).
Treat the owner's reported five-hour window as a constraint, not five hours of
continuous inference or a published fixed token budget. The account dashboard
and provider reset responses remain authoritative; weekly/shared usage can also
matter. Never turn token counts into an invented remaining allowance or dollars.

## Observed bottlenecks

Native logs from alpha task `task-1dc3b256a0de46648114a0975812d515` report:

| Observation | Count |
|---|---:|
| Input tokens across the invocation | 4,939,868 |
| Of those, cached input | 4,741,888 |
| Input not read from cache | 197,980 |
| Output tokens | 14,180 |
| Reported reasoning output | 4,149 |
| Completed command events | 34 |
| Command output bytes | 605,166 |

This was a first/unrecorded-documentation-manifest iteration, including a full
rules/API/SDK review; it is not a steady-state benchmark or proof the review was
unnecessary. Earlier routine invocations also repeatedly dumped all playbooks,
research and compact references, often tens of kilobytes before reading code.
Large tool output enlarges later context too. Cached input is not free, and
the categories above must not be added as if all were disjoint.

The worker produced a smoke-passed candidate, but publication rejected C++
reference files under the allowed experiment directory. Beta subsequently hit
the same artifact allowlist bug. Losing a valid candidate to a wrapper failure
and asking another model to recreate it is avoidable quota waste.

## Changes

1. Trusted preparation writes `.agent/brief.md`: exact identities, compact latest
   measurements, two representative development losses, four recent experiment
   decisions, documentation status and approved commands. This is the initial
   read instead of a roughly 27 KB envelope. The complete immutable envelope,
   eight-entry history, old task pages, metrics, checks and checkpoints remain
   available on demand; no evidence is discarded to shorten the brief.
2. Unchanged routine lanes consult only the relevant playbook and API sections.
   Bootstrap/changed rules, exports and SDK still require the complete review.
   A fresh conversation is not itself a new bot bootstrap. SDK/API ambiguities
   still justify targeted investigation; scope and permission checks remain.
3. High reasoning is directed at a causal failure pattern, expected strategic
   impact and a falsifiable prediction. One focused change, useful regression
   checks and one normal `bot-check`; rerun only after a source correction.
   Do not generate source backups, copied SDKs, bulk replay exports or verbose
   narration when Git, snapshots and checkpoints already preserve the evidence.
4. Experiment C++/header regression/reference fixtures can be published as data.
   Generated Python bytecode remains private, not published. The build service
   never executes experiment files. The source/path/size validation remains.
5. Operator-only recovery can publish a preserved, previously smoke-passed native
   candidate after this exact pre-push artifact bug, with fresh trusted checks
   and **zero new model invocations**. It refuses auth/quota failures, changed
   source baselines, branch conflicts and existing/ambiguous publication intents.
6. Every future native invocation records the CLI's actual `turn.completed`
   usage and completed-command output counts. Historical logs can be backfilled
   while stopped. Missing usage stays unknown. See the official
   [JSON event documentation](https://learn.chatgpt.com/docs/non-interactive-mode).

## Measure useful output, not activity

Run `python3 /opt/battlecode/ops/usage-report.py` on the server. It reads SQLite
without a second writer and groups observations by lane and efficiency profile
over the last five hours. That reporting window is not a claim about the
provider's exact quota-reset window. Compare completed valid candidates,
reported uncached-input/output counts, blocked jobs and eventual full-suite
results. More commits or shorter prompts alone do not establish stronger bots.

No before/after reduction in consumed subscription quota or strategic strength
is claimed before comparable post-change runs exist. A smaller rendered brief
can be measured immediately; total savings depend on what the model actually
reads, tool calls and subsequent reasoning. Keep necessary evidence accessible,
inspect traces for repeat waste, and tune from observations instead of imposing
an arbitrary hard token cutoff in the middle of a useful experiment.

## Safe deployment/recovery

Pause new scheduling, let the current bounded invocation finish, then stop the
supervisor before installing. Preserve incomplete attempts if draining fails.
With all services stopped, root may run:

```bash
python3 /opt/battlecode/ops/recover-worker-history.py
python3 /opt/battlecode/ops/recover-publication.py --bot alpha --task-id TASK_ID
```

The recovery helper runs capture under the bot owner and central writes under
`bc-arena`; it never invokes Codex or reads credential caches. After recovery,
restart the managed supervisor and start scheduling. A pending evaluation must
finish before any new improvement task for that lane. Original native results
and transcripts remain unchanged; operator recovery is recorded separately.
