# Active training: alpha, beta and gamma

18 October engine update: official CLI 2.2.5 / engine 0.0.3, release mode,
17 published maps: 14 development and the existing three reserved maps.
Full qualification uses every map with no daily downgrade. Three-bot continuous
self-play now has 84 games per round (three pairs × two sides × 14 maps).
Old/new engine feedback is separated. The six-map counts below are historical.
See [the current-game transition](TOOLCHAIN_225.md).

18 October storage policy: [rolling local history](ROLLING_HISTORY.md) replaces
the laptop offloader. Old routine raw history expires automatically while source,
compact results and important evaluation evidence remain. The offload sections
below describe the earlier configuration, not the current dependency.

17 October strategy update: all lanes now use the same competitive strategy
skill, current readable rule/API packet and frozen arena opponent sources.
Training edits continue from a measured development base, separately from the
protected champion. New-workflow comparisons include that base on all six
development maps. See [the improvement workflow](IMPROVEMENT_WORKFLOW.md) and
[live deployment evidence](../evidence/blaxel/competitive-workflow-20261017.json).

Gamma was initially requested as Claude Code, then corrected by the owner to
**Codex** before any model task or Claude login completed. All three active
lanes use native ChatGPT subscription login, `gpt-6.1-sol`, high reasoning,
independent Linux users/homes/clones, and persistent `bot/<id>` branches.
The unused Claude sign-in was stopped. No credentials were copied or pooled.
The cancelled Claude-only adapter/install helpers were removed from the active
implementation; their earlier commits remain in Git if ever needed for review.

## One improvement per bot per hour

`limits.improvement_interval_seconds = 3600`. Every bot gets an improvement job
each hour, even when feedback is unchanged. The existing global model slot
serializes these jobs; oldest-served goes first. The durable start timestamp
prevents duplicate calls after restart, and there are no catch-up bursts.

Games run continuously between coding jobs when `limits.continuous_matches`
is enabled. Each handoff includes a compact development summary
since the prior job, grouped by source revision, map and side, with reliability
counts and representative losses. Canonical feedback, commit/evaluation/match
IDs, replays, statistics, historical notes, check reports and diagnostic slices
remain available. Duplicate stage references are deduplicated; deterministic
reruns and cached views are not independent strategic evidence. Holdout detail
remains reserved. Each invocation makes one bounded experiment and stops.

Explicit pauses, authentication/quota/permission waits, and a candidate still
awaiting evaluation can delay the next job. No work is transferred to another
account and no paid fallback is enabled to meet a clock deadline. Each model
invocation keeps its 20-minute wall limit. The full promotion gate is unchanged.

## Continuous self-play is separate from hourly coding

An implementation gap was found on 17 October: the original scheduler ran only
candidate evaluations and then left the game queue empty. Earlier wording about
games between jobs did not establish continuous play. The new low-priority
producer keeps **one frozen round-robin** queued, independent of model cadence
and the daily promotion-check cap. With three bots this is 36 full games:
three pairs × both sides × six development maps. After it finishes, another
round starts without a model call. Evaluations and smoke checks take priority.

Each lane contributes its latest completed reliability-valid evaluated source,
not a mutable checkout or an unevaluated branch tip. These are training
candidates, not automatically accepted champions. The engine, maps, commits,
source/build hashes and pairings remain frozen within a round. New revisions
enter the next round. Adding an enabled registered lane extends the round-robin.

All games retain normal sealed replays, statistics and logs. The next hourly
handoff includes a bounded, lane-scoped summary with exact source and opponent
commits, map/side cells, available final metrics and up to three loss references.
Workers use the normal `arena-client ... slice` command for those diagnostics.
Only development maps are played; no reserved-map trace access is added.

There is no public seed flag. Identical-input runs therefore remain **repeated
executions, not independent evidence**. Feedback reports physical completions
and repeat counts separately; its win/loss cells deduplicate identical inputs
within the time window and flag differing repeated outcomes. Training matches
never enter promotion evaluation cases or certify a submission. Repeats still
produce useful runtime/reliability evidence, not extra proof of strategic gain.

Global pause, engine-adapter pause and disk guards stop new gameplay. A coding CLI
quota/login wait or owner-model pause does not stop already compiled bots from
playing. To disable a lane in future training rounds, disable its registration;
to pause new play use global pause; to interrupt an active game use full service
stop. In-progress attempts remain recoverable rather than becoming invented losses.

Enable on this existing deployment only while services are stopped:

```bash
python3 /opt/battlecode/ops/configure-training.py --interval-seconds 3600 --continuous-matches
```

Disable with `--no-continuous-matches`; restart afterward. Existing training
queue entries park without deletion and resume if re-enabled. The status snapshot
includes `continuous_training` with its frozen roster, round and game counts.
Concurrency stays one match, one build and one model invocation. The full
nine-map promotion gate and official upload/challenge restrictions are unchanged.

### Real deployment evidence

Infrastructure `707a137c0a451f615cef589f5ffe174f5aa9e434` was installed with all
services stopped, then enabled with `--continuous-matches` and restarted under
the managed supervisor. [The live observation](../evidence/blaxel/continuous-self-play-live-20261017.json)
records a complete 36-game round and automatic creation/execution of the next
round while all three coding workers remained IDLE and the task count stayed 49.
The model clocks were not reset or forced. Exact match IDs, pairings and frozen
commit/build/map identities are preserved in that report.

[The feedback/artifact check](../evidence/blaxel/continuous-self-play-feedback-20261017.json)
verifies three real completed replay/statistics artifact sets and confirms that
each worker's prospective brief includes self-play. These are previews of the
normal next-hourly-task inputs, not extra dispatched model jobs. The sampled
complete briefs were about 10–12 KB, including existing history and external
feedback, rather than raw game transcripts. Restart/publication/priority/pause/
repeat-count behavior also passed focused synthetic tests; they are not claimed
as additional real-engine games. Ninety local tests passed before deployment.

## Adding a Codex lane

Root stops the services before setup; do not reinstall the server:

```bash
python3 /opt/battlecode/ops/supervisor.py stop
# Once, for a fresh identity; alpha/beta/gamma already exist on this server:
python3 /opt/battlecode/ops/add-worker.py NEW_BOT
python3 /opt/battlecode/ops/blaxel-host.py
python3 /opt/battlecode/ops/as-arena.py python3 /opt/battlecode/ops/bootstrap-lanes.py --bot NEW_BOT
runuser -l bc-NEW_BOT -c 'git clone --branch bot/NEW_BOT https://github.com/micache/battlecode.git /home/bc-NEW_BOT/battlecode'
runuser -l bc-NEW_BOT -c '/usr/local/bin/codex login --device-auth'
```

The owner opens the native device-login URL and enters its short-lived code
using the intended account. Do not share passwords, access tokens or auth files.
The operator can expose the native login instructions through the existing
Blaxel process API; console/SSH access is not required. The owner alone approves
the account access. After native login, pin the model/reasoning in that owner's
private configuration and confirm only the new lane:

```bash
python3 /opt/battlecode/ops/configure-owners.py --bot NEW_BOT --confirm-distinct-owner-accounts
python3 /opt/battlecode/ops/configure-training.py --interval-seconds 3600
```

All registered Codex lanes can be pinned to the owner's requested settings with
`python3 /opt/battlecode/ops/set-worker-reasoning.py --model gpt-6.1-sol --effort high`.
This requires native owner directories to exist and does not touch auth files.
The native wrapper rechecks subscription login and its executable pin per job.

Restart using the managed keep-alive command in [Blaxel operations](../ops/BLAXEL.md).
After the baseline completes, resume the owner through its mailbox:

```bash
runuser -l bc-NEW_BOT -c 'arena-client --config /etc/battlecode/NEW_BOT.json resume'
```

New lanes use the official C++ starter and a three-map, both-side validity
baseline. They do not receive champion promotion from this wiring check. On
systemd hosts use `battlecode-worker@NEW_BOT.service`; the same global model
lock applies. Existing accepted baselines, frozen opponent revisions, full
nine-map evaluation, readiness and promotion thresholds are not weakened.

## Retained evidence and disk recovery

Completed per-match working trees are losslessly archived into `project.zip`,
with every member hash verified against its original. Replays, statistics,
logs, normalized outcomes, source snapshots and shared build caches are kept.
The new completion manifest retains original manifest provenance. Database
pointers move only after verification; redundant uncompressed working trees
are then removed. Old attempt paths remain relative aliases, preserving exact
parser/readiness raw-file references. Interrupted staging/publication/cleanup
are recoverable without rerunning a game.

Restore a working tree into a **new scratch directory**, not sealed evidence:

```bash
unzip /srv/battlecode/matches/MATCH_ID/ATTEMPT-archived/project.zip -d ./restored-project
```

Check file hashes against `project-archive.json`. Compression is not an off-host
backup or unlimited storage: the disk guard still parks work when necessary.
Physical VM reboot persistence remains unverified; managed process recovery
and survival of operator-client disconnection are separate observations.

## Official publishing and outside exploration

The official monitor checks the eligible best version every five hours,
deduplicates by previously confirmed submitted source, and waits three hours
after a duplicate. Actual uploads/challenges/results collection remain blocked
until the official policy/interface checks are resolved. Outside match imports
and bounded diagnostic feedback are implemented; no external games or automatic
uploads are claimed without saved real evidence. See [official operations](OFFICIAL_AUTOMATION.md).

Do not install a different `bwrap` on this running Codex-only host without a
controlled native sandbox check: Codex selects it ahead of its bundled helper.
The temporary Claude setup's distribution package caused private-parent mount
failures and was removed. The pinned native Codex helper again passed the exact
task/mailbox access and protected-write-denial checks for beta and gamma; no
directory permissions or sandbox boundaries were relaxed.
