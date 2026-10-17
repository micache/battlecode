# Three owner lanes and hourly improvement

Alpha and beta keep their existing Codex subscription logins, model and high
reasoning. Gamma uses native Claude Code under `bc-gamma`, a private persistent
home and independent writable clone, and branch `bot/gamma`. No credential
caches are copied, and no API/Console key, inference proxy, paid top-up or account
failover is configured. Gamma selects the subscription's native default model
with `--effort high`; the actual model is recorded from native session events.

## Schedule and evidence

`limits.improvement_interval_seconds = 3600`: each lane gets one improvement
invocation per hour, including when its feedback has not changed. Dispatch is
oldest-served first and records its timestamp in SQLite, so restart cannot reset
the timer. Jobs are serialized by the existing global model lock. The timer is
start-to-start, with no catch-up bursts. Quota/auth/permission waits, explicit
pauses and a candidate still awaiting evaluation can delay a lane; none are
bypassed to meet a clock deadline. An invocation remains bounded to 20 minutes.

Games/evaluations run between improvement jobs, without model polling. The
handoff includes a deterministic development-only summary since the prior job:
separate immutable source revisions, wins/losses by map and side, reliability,
and up to three representative losses per source. Duplicate stage references
are deduplicated. Cached or identical deterministic reruns are not independent
evidence. Exact match/evaluation/commit IDs, canonical feedback, paged history,
replay/statistics files and bounded diagnostic retrieval remain available.
Holdout details stay reserved. A brief is a lossy index, not a substitute for
the canonical evidence or a claim that a new experiment must be stronger.

New lanes establish a three-map, both-side validity baseline against the pinned
starter; this is not promotion. Existing immutable source/engine/map matches
may be reused with their original IDs. Subsequent evaluations retain frozen
opponents and the full nine-map/readiness/promotion gates unchanged.

## Native Claude boundary

The native musl executable is installed from Anthropic's release manifest and
verified against its SHA-256. Every invocation rechecks that pin and native
`claude auth status`: only `loggedIn: true`, `authMethod: claude.ai` is accepted.
The environment is allowlisted; API/provider overrides are not inherited.

`claude -p` uses native schema output, a 30-turn/20-minute bound, high effort,
restricted mode, no project/user settings sources, no MCP or slash commands,
and only Read/Edit/Write/Glob/Grep/Bash tools. Bash requires native bubblewrap
sandboxing with no unsandboxed fallback and no allowed network destinations.
Owner credential directories are denied to tools; the CLI alone reads its
native auth cache. The trusted mailbox permits compilation/smoke checks without
exposing the host compiler, publisher credential or another owner's home.
Publication still validates actual changed paths, source identity and the
trusted exact-source check. A native permission denial parks the lane.

Only the native successful result envelope's `structured_output` is ingested,
then the existing worker-result schema and task/source identities are checked.
Quota/auth failures park the same lane; malformed output and interruptions
retain a checkpoint and require explicit recovery, never a silent model retry.
Native usage counts retain Claude's cache-token semantics; missing is unknown,
and client cost estimates are not reported as subscription billing.

Primary documentation: [native CLI](https://code.claude.com/docs/en/cli-reference),
[programmatic output](https://code.claude.com/docs/en/headless),
[Bash sandbox](https://code.claude.com/docs/en/sandboxing),
[musl setup](https://code.claude.com/docs/en/setup).

## Setup and owner-only login

Stop services before installation/configuration. Existing servers must be
upgraded, not reinstalled. On this Blaxel server, root runs:

```bash
python3 /opt/battlecode/ops/supervisor.py stop
python3 /opt/battlecode-source/ops/upgrade.py
# Once only; preserve/review the pin rather than overwriting an existing CLI:
python3 /opt/battlecode/ops/install-claude.py
python3 /opt/battlecode/ops/add-worker.py gamma --provider claude-code
python3 /opt/battlecode/ops/configure-training.py --interval-seconds 3600
python3 /opt/battlecode/ops/blaxel-host.py
python3 /opt/battlecode/ops/as-arena.py python3 /opt/battlecode/ops/bootstrap-lanes.py --bot gamma
runuser -l bc-gamma -c 'git clone --branch bot/gamma https://github.com/micache/battlecode.git /home/bc-gamma/battlecode'
```

The owner logs in using their subscription, without enabling Console/extra paid
usage. No Blaxel console is needed. From the trusted local repository terminal:

```bash
python3 ops/blaxel-claude-login.py gamma
```

This prints the native authorization URL and privately accepts the one-time
code through a hidden terminal prompt. It forwards the code to the native
process stdin over authenticated HTTPS; it does not copy credentials or put the
code in chat, command arguments or a file. `--process NAME` attaches to an
existing native login after checking its exact command and writable stdin.
If it expires, start a fresh login. Only the owner approves account access.

After successful owner login, root confirms just gamma while services are
stopped; other owner settings/logins remain unchanged:

```bash
python3 /opt/battlecode/ops/configure-owners.py --bot gamma --confirm-distinct-owner-accounts
```

Restart the managed supervisor using a new process name, as documented in
[Blaxel operations](../ops/BLAXEL.md). It includes registered lanes automatically.
After gamma's baseline is complete, explicitly resume gamma through its mailbox.
On a systemd host the generic unit is `battlecode-worker@gamma.service`; the
existing model lock still covers all providers. Status/start/pause/stop use the
same commands, substituting `gamma` where an owner-specific command is needed.

## Lossless disk maintenance

Completed matches' copied SDK/source/build working trees are archived into
`project.zip`. Every member is byte-hashed against the original. Replays,
statistics, logs, normalized outcomes, source snapshots and shared build caches
are retained. A new completion manifest records archive hashes, original
completion provenance and the original attempt identity. SQLite pointers are
updated only after verification; only then is the redundant uncompressed copy
removed. Interrupted staging/pointer/cleanup steps are restart-recoverable.
The old attempt directory becomes a relative alias to the new sealed attempt,
so existing parser/readiness references to exact raw-file paths remain valid.

To recover the working tree in a **new operator-owned scratch directory**:

```bash
unzip /srv/battlecode/matches/MATCH_ID/ATTEMPT-archived/project.zip -d ./restored-project
```

Do not extract over sealed evidence. Verify the restored file hashes against
`project-archive.json`. This is compression, not replay pruning or an off-host
backup. The disk guard still parks work if the retained evidence fills storage.
