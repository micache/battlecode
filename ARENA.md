# Arena implementation assignment

Current owner override (18 October 2026): use pinned official CLI 2.2.5 and
release mode, with all 17 currently published maps. The earlier nine-map counts
below are historical. Full evaluation is never downgraded by a daily promotion
counter; automatic champion promotion remains a separate disabled gate.
See docs/TOOLCHAIN_225.md for migration, evidence and the ward::owner SDK gap.

19 October owner override: enable narrowly scoped unranked exploration for the
owner-selected C++ bot through the now-verified official CLI 2.2.5 commands,
using its actual shared 50/hour allowance. Upload/activation remain disabled;
no blanket policy/readiness certification is implied. Actual own submission
IDs must be independently verified, not inferred from configuration. See
docs/UNRANKED_EXPLORATION.md for source-proof and operator-online limits.
Latest selection: await the owner's prepared beta `7cab9b0f` upload, verify its
actual source, then use beta. Never upload or override another team selection.

Implement the design in README.md as a small, recoverable service. Use Python, SQLite, ordinary files, Git, systemd, and the official cambc CLI. Do not build a web dashboard, distributed broker, Kubernetes stack, vector database, custom game simulator, or LLM routing service for version one.

This document is a specification. `arena`, `arena-client`, and `bot-check` below are project commands you must implement. They are not commands supplied by cambc. Existing official CLI syntax is recorded in evidence/cli-help.txt.

## 1. Scope and first deliverable

Start by inspecting the assigned repository and host. Preserve existing work. Read RESEARCH.md, RULES_CHECKLIST.md, BOT_REFERENCE.md and both unchanged exports under sources/. The complete supplied rules/API exports were read for this revision; the separate organizers' AGENTS.md and platform policies remain unavailable. Confirm the current official CLI/SDK version, legal bot packaging, match completion/outcome schema, and effective execution budget. Record exact evidence and unresolved items in `docs/rules/verified.md`.

You may implement and test the private arena while access-dependent policy checks are pending. Do not certify contest compliance or enable official submission/challenge automation until those checks are resolved. Use current authorized documentation; do not substitute older competition rules. Ask for missing host/repository details only after preparing everything that can be done without them.

Deliver these components:

- `arena/`: configuration validation, Git ingestion, immutable build preparation, match adapter, durable scheduler, evaluation, feedback exporter, worker supervisor, and optional external-result importer.
- `ops/`: installation and rollback procedure, systemd service templates, approved rootless build/run wrapper, and operator commands.
- `schemas/`: task, worker-result, feedback, and normalized match schemas with protocol version 1.
- A pinned dependency/toolchain manifest and a frozen map-pool manifest with hashes.
- Focused tests for ingestion, attribution, recovery, evaluation, and quota handling, plus real-engine smoke evidence.

Use the provided config and result schema as starting contracts, not as an already implemented application.

## 2. Host, identities, and directories

Use a persistent CPU Linux host. Start with two concurrent matches, one concurrent compilation, and at most two coding invocations across all workers. Each account has at most one invocation. Tune from observed CPU, RSS, disk, match duration, and fuel faults; do not assume all vCPUs are available to matches during compilation.

Use distinct non-root Linux users for the arena, each account owner, and an optional official publisher. Owners authenticate directly under their own user. Restrict home directories and credentials to that user. Ordinary bot execution must not mount these homes, inherit tokens, or reach the network. A host administrator remains trusted; Unix accounts do not protect secrets from root.

Suggested arena-owned persistent paths:

| Path | Contents |
|---|---|
| `/srv/battlecode/state/arena.sqlite` | Single authoritative SQLite database |
| `/srv/battlecode/repos/` | Read-only-to-workers source mirror and pinned infrastructure |
| `/srv/battlecode/builds/<build_id>/` | Validated source snapshot, toolchain metadata, compiled artifact |
| `/srv/battlecode/matches/<job_id>/<attempt>/` | Replay, logs, statistics, normalized result |
| `/srv/battlecode/evaluations/<evaluation_id>/` | Frozen suite, aggregate metrics, promotion decision |
| `/srv/battlecode/feedback/<bot_id>/` | Atomically exported, worker-readable feedback |
| `/srv/battlecode/inbox/<worker_id>/` | Per-owner request mailbox with restricted ownership |
| `/srv/battlecode/backups/` | Consistent database backups and manifests |

Worker clones and task checkpoints live in their owners' persistent homes. Keep SQLite on local disk, enable WAL, foreign keys, a busy timeout, and explicit transactions. The arena process is the database writer. Match children and account workers return messages/files; they do not concurrently edit SQLite or promotion records.

Create one independent clone per owner. Do not share a writable checkout or a credential directory across workers. Keep trusted runtime scripts and evaluation configuration outside worker-writable paths. Restrict Git writes to registered branches where repository settings allow; also enforce path ownership in the trusted publisher and ingestion validation. Prompt instructions alone are not access controls.

## 3. Source ingestion and publication

Poll registered remote bot branches every 60 seconds, with jitter and backoff. A worker has a fixed owner, bot ID, branch, and source path. Validate names against a conservative slug grammar and reject symlinks, path traversal, oversized sources, unexpected dependencies, or changes outside its allowlist. Never construct shell commands from bot metadata; use subprocess argument arrays.

For a new candidate, record repository, branch, full Git commit SHA, bot subtree hash, parent accepted source hash, experiment ID, and infrastructure version. Fetch and materialize the exact commit before queueing. Running matches never read a moving branch or a checkout being edited.

Keep at most one evaluation running and one newer pending revision per bot. Never replace the revision of a running job. If a human pushes several revisions while offline, mark unstarted older candidates superseded and evaluate the latest; preserve their identities and any already completed results.

The non-LLM worker publisher performs publication:

1. Acquire the bot's single-writer lease and verify the expected remote branch tip.
2. Create a private attempt workspace. Start the bot subtree from the frozen development base selected by same-input development comparisons, falling back to the accepted source when evidence is insufficient. This is separate from champion promotion: never start blindly from a rejected branch tip. Retain experiment history and record both identities.
3. Invoke the coding CLI with a fixed task envelope and approved tools.
4. Validate the result, changed paths, source limits, and smoke checks. Require the returned task ID, bot ID, and base hash to match the trusted envelope. Derive changed paths from the actual working-tree diff; do not trust the model's list. Use task-specific result files so a stale result cannot be mistaken for a new one.
5. Create a normal commit with the current branch tip as parent, containing the new owned source and notes. Push without force. Record the resulting SHA and source hash.
6. On a non-fast-forward conflict, preserve the patch and pause for lease/conflict resolution. Do not silently rebase onto another writer's work.

Compare the candidate to its task's edit-base source hash, not merely to the previous branch tip. The full champion gate still compares against the accepted source. A notes-only candidate does not trigger another match suite. Credentials for Git publication belong to the trusted wrapper, not to the game sandbox.

## 4. Official engine adapter

Implement a narrow interface: `prepare_bot(snapshot, engine_lock)`, `run_match(spec)`, and `normalize_result(artifacts)`. Inspect real output before defining the parser. Preserve raw output even when normalization fails.

The reviewed current CLI 2.2.5 supports these source-project commands:

```bash
cambc init --yes /path/to/project
cambc new bot-name --lang cpp
cambc build bot-name --release --output /path/to/build/bot.wasm
cambc run bot-a bot-b --release --json --map /path/to/map.map26a --out-dir /path/to/match --statistics /path/to/match/final.json
cambc run-batch /path/to/jobs.txt --jobs 1 --timeout 300 --release --color never
cambc maps pull
cambc bundle bot-name --output /path/to/bot.zip
```

Run these from a prepared official project. The text batch manifest has four columns: bot-A project directory, bot-B project directory, map path, replay path ending in `.repl26a`; paths are relative to the manifest. A separate compiled-input JSONL mode exists, but its precise schema was not verified here. Do not invent it.

For the MVP, use a bounded process pool of `cambc run` calls with `--release --statistics PATH --json`; this gives readable final statistics to validate. Omitting `--json` in 2.2.5 produces binary statistics, and omitting `--release` selects debug behavior that differs from the platform. If batch output/replays provide the same verified outcome and fault information, add `run-batch` as an optimization. Keep concurrency owned by one layer: do not launch N batches each with N workers accidentally.

Use full-length games, normally by omitting `--rounds`, and verify the effective settings against the supplied handbook profile: 1,000 submitted gems, 2,000 maximum rounds, 1,024 draft-memory bytes and 8 live team-memory bytes. The documented base fuel is 100,000 per turn for C++/Rust, multiplied by 5 for OCaml and 25 for Python; first draft turn gets 10× and first champion play turn gets 2×. An expected profile in config is a validation target, not a measured engine snapshot. Record the actual values or mark parity unverified. Never pass one flat `--fuel 100000` to every language and assume parity.

`--rounds` is an optional stopping override, not inherently invalid; a run stopped before the authoritative ending is a truncated debug run and cannot be scored as complete. A provided round count or a process exit code alone does not establish completion. There is no documented `--seed` in the inspected public CLI. Record seed as null when unavailable. Distinct maps, sides, opponent snapshots, and explicitly versioned bot policy variants supply experimental diversity.

Fuel exhaustion suspends a bot until a later turn; it is not by itself a crash or forfeit. Preserve separate diagnostics for suspension, a genuine bot exception/trap, death of a champion, game termination, and the arena's wall timeout. A completed match with suspension still uses the engine's actual outcome. If suspension counts cannot be observed reliably, report unknown rather than treating every slow turn as a fault.

First prove that source projects and any compiled-input path behave equivalently, including language-specific execution budgets, before reusing compiled modules through a faster interface. Build identity includes source bytes, language, SDK, runner binary hash, compiler/toolchain versions, build flags, and build recipe. Reuse validated builds under this identity; never reuse based on bot name alone.

Bootstrap toolchains once with network access, then run builds and matches in dedicated, resource-bounded rootless containers with no credentials or network. Only trusted build recipes may execute. Mount source/SDK as read-only where possible, outputs separately writable, and impose CPU, memory, PID, disk, and wall-time limits. WASM is the game execution format, not a substitute for isolating compiler/build activity.

Start with a 300-second wall timeout only as a provisional protective limit. Measure complete matches and increase if valid games exceed it. A host wall timeout or process crash is not automatically a bot loss. Kill the entire job process group/container, preserve evidence, and classify the outcome.

Fetch map updates into staging; record pool ID/hash and file hashes, then activate a new suite. Never overwrite maps used by running jobs. Engine/SDK updates are explicit reviewed maintenance events: rebuild affected bots, rerun parity/smoke checks, and keep new results separate from the old version.

## 5. Durable state and idempotency

Minimum tables: `bots`, `revisions`, `builds`, `evaluations`, `match_jobs`, `match_attempts`, `workers`, and `external_matches`. Store the frozen suite and normalized metrics as versioned JSON where that keeps the schema smaller.

Suggested match states: QUEUED, RUNNING, COMPLETED, BOT_FAULT, INFRA_ERROR, TIMEOUT, CANCELLED. Worker states: IDLE, RUNNING, WAITING_EVALUATION, QUOTA_WAIT, AUTH_REQUIRED, PERMISSION_BLOCKED, PAUSED. Evaluation states include BUILD_FAILED, EVALUATING, ACCEPTED, REJECTED, INCONCLUSIVE, and SUPERSEDED. Do not compress these into a single win/loss flag.

A logical match key includes ordered bot build IDs, map hash, engine/settings hash, and any supported randomization configuration. Evaluation membership is separate. If runs are deterministic, reuse identical successful matches; repeated identical games are not independent samples. If a runner has nondeterminism without seed control, record that limitation and repetitions explicitly.

Persist RUNNING state before launching a child. Publish artifacts through a temporary directory and atomic rename, then mark completion in a transaction. Include a completion manifest with hashes so restart reconciliation can detect a finished artifact whose database transaction was interrupted. Unique constraints prevent double-counting a job or consuming a feedback batch twice.

On restart, terminate or establish the status of old service-owned process groups before requeueing orphaned work. Keep attempts separate and use only one validated terminal outcome per logical case. Retry infrastructure failures at most once automatically; repeated failures pause that adapter and surface diagnostics. A documented bot forfeit can count according to official rules, but remains a bot fault in reliability metrics.

## 6. Evaluation and champion selection

Keep immutable snapshots of a starter baseline, accepted team bots, and several past bots with different strengths. Self-play against only the newest teammate encourages narrow counters and cyclic forgetting. Do not treat a local rating as an official leaderboard rating.

For a new lane with no incumbent, establish its pinned starter or existing team bot as a provisional baseline after validity checks and a recorded initial suite. Do not require an improvement over a nonexistent incumbent. Subsequent candidates must pass the normal comparison gate.

Freeze the opponents and map suite before evaluating a candidate. Run both side assignments. For candidate-versus-incumbent comparisons, evaluate both against the same opponent versions and maps; reuse the incumbent's results only when every match identity field agrees.

Starting policy, to tune after measuring costs:

| Stage | Work | Decision |
|---|---|---|
| Smoke | Build plus one map against starter, both sides | Reject invalid builds, reproducible faults, or incomplete games |
| Screen | Three development maps × two sides × up to three distinct fixed opponents | Reject obvious regressions; otherwise continue |
| Promotion | All frozen maps × two sides × the same opponents, plus incumbent head-to-head | Accept only under the configured reliability and score gate |
| External check | Selected accepted bot versus strong official opponents | Investigate generalization; keep this evidence separate |

The currently published pool has 17 maps. With three opponents, a complete common-opponent suite is 102 candidate games, plus up to 102 reusable incumbent games; full-pool head-to-head adds 34 games. Screening cases already present in the final suite should be reused. With fewer opponents, label results provisional and report the actual coverage. Never export an old-engine or partial-map candidate as current submission-ready.

Use result score 1 for a win and 0 for a loss. Under the supplied rules there is no completed-game draw: at the round limit compare submitted gems, lifetime gold earned, champion kills, then Team B. The final fallback refers to absolute side assignment, not a relative SDK Team.ENEMY value. Trust a verified engine outcome, retain the reason where available, and test complete-tie attribution explicitly. An unexpected draw is a schema/rules discrepancy to investigate, not automatically a half point. Average sides within each map/opponent case, then apply fixed declared weights. Compare candidate and incumbent on these matched cases. Report raw counts, per-map and per-opponent results, bot faults, missing cases, and the score difference. Never let an opponent pool's changing composition masquerade as an improvement.

Initial operational promotion gate: no reproducible candidate reliability fault; at least +5 percentage points in common-opponent mean score; no decline greater than 25 percentage points on any adequately covered map; no aggregate decline on the reserved holdout maps. These are engineering thresholds, not proof of statistical significance. If evidence is mixed or incomplete, keep the incumbent and mark INCONCLUSIVE. The evaluator owns thresholds; a bot cannot edit them.

Keep the three existing reserved maps for promotion checks and expose only aggregate holdout results to the coding worker. These are public maps: holdout means reserved evaluation feedback, not secret or previously unseen terrain. Even repeated pass/fail feedback can overfit that holdout; retain that caveat and use external play as an additional check. A full evaluation must still cover every published map, with no daily counter silently reducing coverage. For statistical uncertainty, resample at the map/case level rather than pretending identical reruns or side pairs are independent. Do not promise a significant gain from a tiny suite.

Keep separate pointers for each lane champion and the team's selected official submission. Promotions are atomic compare-and-swap updates against the incumbent and suite version used by the evaluation. Do not advance an official submission automatically as a side effect of local promotion.

## 7. Feedback and efficient model use

Save raw replay bundles, stdout/stderr, final statistics, runner return code, timestamps, elapsed time, and resource measurements. Final normalized fields must be mapped from verified engine output, not guessed field names.

Export a per-evaluation `summary.json` and `summary.md` containing:

- Candidate/incumbent source and build IDs, engine/settings/pool hashes, opponent revisions, and coverage.
- Outcome table, score delta, reliability counts, and observed strategic metrics with availability flags. Prefer submitted gems, lifetime earned gold, kills, terminal reason, capture completion, bag loss, channel interruptions and fuel suspensions where actual artifacts support them. Keep gold balance separate from lifetime earned gold, and suspension separate from crashes.
- Up to three representative failures, with match ID, side, turn/round if known, relevant trace excerpts, and artifact paths.
- Promotion decision, evidence, missing information, and a short list of open questions.

Derive counts and timelines in code. If the replay format lacks a verified decoder, use final statistics and our own bounded structured bot logs first. Never fabricate per-turn damage, gem-loss, fuel, or opponent-state metrics. Add parser capability incrementally from actual fixtures.

An agent reads the compact summary first and requests only relevant replay slices. An idle worker consumes no model calls. If there is no new actionable evidence, the supervisor waits or performs predeclared non-LLM parameter experiments. It must not spend quota on repeated status questions.

## 8. Worker supervisor and handoff

Implement one small supervisor per owner. It reads a per-worker task inbox and feedback exports, holds a lock, launches the official CLI, and saves raw CLI output and the structured final result. Do not use a third-party OAuth proxy or a generic API SDK with extracted subscription tokens.

Start with a 20-minute wall limit per coding invocation and one experiment per task. Persist the patch and checkpoints on timeout. A crash, turn-limit exhaustion, or malformed final result does not publish a candidate. The next recovery task explicitly identifies that incomplete attempt.

Handle limits using provider-reported status/reset information when available. QUOTA_WAIT sleeps until the reported time plus a small jitter. If the reset is unknown, use bounded backoff, initially 30 minutes, then 1, 2, and 4 hours; do not hammer the service. AUTH_REQUIRED and PERMISSION_BLOCKED require owner/operator resolution. Disable API and paid-overage fallback. Never move a quota-blocked task to a different account's lane to evade its limit.

Implement `arena-client status`, `feedback`, `pause`, `resume`, `claim`, `release`, `publish`, and `import-external` with structured output. Local users may use them through SSH or an equivalent restricted file-transfer interface. These commands talk to the supervisor through validated mailbox requests; workers do not get write access to central evaluation state.

Handoff from server to laptop requires a confirmed pause, no active writer, and an owner lease. Copy only code and task state, not another process's live credential cache. Resume requires reconciling the branch tip and any pending candidate. Separate bot IDs are the simplest alternative when two machines must develop at once.

## 9. Official challenge integration

Ship this module disabled. First support manual import of authorized match metadata and downloaded replays, preserving the original files and checksums. The user identified the unranked chooser at `/game/matches?challenge=choose`; this is not evidence of a public automation API.

Before enabling unattended challenges, verify the current rules, authentication method, supported request interface, quotas, exact submission selection/activation effects, opponent version identity, match polling, replay access, and any visibility restrictions. Do not guess request bodies or undocumented CLI subcommands. If no supported automation route is established, keep manual challenge/import as the integration.

Use a single publisher lock. Map every official submission to our immutable bundle/source hash. Uploading and activating may be separate operations and may affect ranked play; determine this before automation. Serialize any active-submission changes with pending official challenges when the platform cannot pin a submission. Never let four workers race to change the team's active bot.

Treat remote creation as a non-idempotent operation unless the service documents otherwise. Save the request intent before sending. If the response is lost, reconcile against official match/submission history; mark UNKNOWN and stop automatic retries if identity cannot be established. Do not accidentally create duplicate challenges.

Respect Retry-After, stop on access failures, and keep one outstanding challenge initially. Do not probe private opponent code. Record version identity as unknown if the service does not expose it; do not reuse that result as a controlled fixed-opponent sample. An external loss becomes a hypothesis for local tests, not an immediate universal strategy change.

## 10. Operations and acceptance gates

Provide systemd units with explicit User and WorkingDirectory, Restart=on-failure, a nonzero RestartSec, start-rate limiting, and KillMode=control-group. Preserve state across reboot and SSH disconnect. Stop the entire job tree on shutdown. Runtime workers have no sudo and no privileged Docker socket.

Expose a text/JSON status report: active workers, quota/auth waits, Git lag, queued/running/failed matches, candidate revision, latest accepted revision, feedback age, and disk usage. Record heartbeats without calling models. Rotate service logs. Use a 10 GB initial raw-artifact budget; preserve champion evidence and representative failures, compress/prune ordinary older replays, and keep small summaries. Pause new work before the filesystem fills.

Use SQLite's consistent backup API or a clean checkpoint procedure; do not copy a live database file alone and assume WAL state is included. Keep daily backups and a copy on a separate persistent volume/provider snapshot according to the owner's chosen destination. GitHub is the code backup; it is not the replay database. Perform one restore drill.

Required evidence before calling this deployed:

1. Two official starter games finish on opposite sides; parsed outcome and replay agree. Record the real duration and final-statistics schema.
2. One candidate travels from pushed commit to exact-source build, complete evaluation, feedback, and the next coding task.
3. A deliberately crashing bot, malformed result, truncated game, and arena timeout are classified distinctly.
4. A new push during a running match does not change that match's inputs or attribution.
5. Restart during execution recovers without duplicate scoring, lost feedback, or two active writers.
6. A simulated quota response parks only that owner's lane; no account switch or API fallback occurs.
7. Another worker cannot read credential files, change evaluation thresholds, or publish on the wrong branch; bot subprocesses have no secrets/network.
8. Laptop handoff, map/engine version changes, disk-pressure pause, and backup restore work as documented.
9. Any enabled external challenge has a confirmed official ID and exact source mapping; unknown creation outcomes never auto-retry.
10. The effective language budgets, 2,000-round/1,000-gem settings and 1,024/8-byte memories match the reviewed profile or have an explicitly resolved documented update. Complete-tie Team B attribution is verified by a fixture; fuel suspension is not mislabeled as a crash. A small bot fixture checks channel completion at turn start, ranged movement/attack restrictions, capture occupancy, hidden obstruction returns, and safe approach tiles using the real engine where available.

Do not fabricate a passing integration test when a toolchain download, login, host, or platform access is unavailable. Finish the implementation and its local validation, document the precise blocker, and provide the next operator action. Report what is implemented, what actually ran, and what remains access-dependent separately.
