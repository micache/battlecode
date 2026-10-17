# Blaxel three-owner arena

The server is **deployed**. Alpha and beta have two real Codex
publication/evaluation cycles saved; gamma's third owner login and three-map
validity baseline are complete. See [acceptance status](../docs/IMPLEMENTATION_STATUS.md)
and [saved evidence](../evidence/blaxel/). Do not rerun installation on this server.

## Installed configuration

- Workspace `banabolabs`, sandbox `battlecode-arena`, region `us-pdx-1`.
- 8,192 MB RAM / four CPU cores; 8,192 MB volume `battlecode-arena-data`.
- Alpha, beta and gamma use Codex in isolated, natively authenticated owner lanes.
  One match, build and model invocation at a time.
  Each bot receives one improvement job per hour, serialized, with accumulated
  development feedback. See [setup and safeguards](../docs/HOURLY_TRAINING.md).
- Rootless Podman, immutable local engine image, CLI/SDK 2.1.6, official C++ starter.
- Codex CLI 0.163.0, pinned executable hash; separate Linux users, private homes,
  native authentication and writable clones. Only `bc-arena` publishes source.
- All three owners explicitly select `gpt-6.1-sol`, reasoning effort `high`, in
  their private native CLI configurations. Alpha and beta have completed real
  improvement cycles; gamma's first successful improvement remains pending.
- Three-map wiring suite. Automatic promotion, official operations, model API
  billing and cross-account failover are all disabled.
- Artifact budget 3 GiB, minimum free space 1 GiB, automatic daily database
  backup, initial two-experiment cap removed after the four real pilot cycles.
  Each invocation remains bounded to 20 minutes; quota/disk gates still apply.
  Completed per-match working trees are losslessly archived; replays/statistics
  are retained. The disk guard still applies to retained evidence.

The provider's virtiofs mount ignores guest `chown`. The installation therefore
uses a 7 GiB ext4 image, `/persist/battlecode-data.ext4`, mounted nodev,nosuid at
`/var/lib/battlecode-volume`. Configuration, database, artifacts, private homes
and rootless image storage live there. UID/GID enforcement was actually checked.
Never format an existing image or mount the same ext4 image on two machines.
This is a single-host deployment, not a shared distributed filesystem.

Blaxel is not a systemd host. A managed API process runs the root supervisor with
`keepAlive=true`, no timeout, and at most five provider-level restart attempts.
Root wrappers enforce owner cgroups and drop privileges; neither owner receives
the API credential, root API access, sudo, or a privileged Docker socket. Unit
wrappers reap and kill descendants before restarting. After five rapid failures
the operator must inspect logs; this is deliberately not an endless crash loop.

## Exact commands

On the trusted operator computer, from this repository:

```bash
python3 ops/blaxel.py login --workspace banabolabs
python3 ops/blaxel.py status
python3 ops/blaxel.py limits

# FRESH installation only; never overwrite an existing server/state.
python3 ops/blaxel.py provision
python3 ops/blaxel.py run 'git clone https://github.com/micache/battlecode.git /opt/battlecode-source && bash /opt/battlecode-source/ops/blaxel-bootstrap.sh' --keep-alive --name arena-install
python3 ops/blaxel.py process arena-install

# Start independently of a terminal. After a completed stop use a new process
# name; inspect status first to avoid duplicate launches.
python3 ops/blaxel.py run 'python3 /opt/battlecode/ops/blaxel-start.py' --keep-alive --restart-on-failure --name arena-supervisor-live

# Status / scheduling start / scheduling pause / all-service stop:
python3 ops/blaxel.py run 'python3 /opt/battlecode/ops/supervisor.py status; python3 /opt/battlecode/ops/as-arena.py arena status'
python3 ops/blaxel.py run 'python3 /opt/battlecode/ops/as-arena.py arena start'
python3 ops/blaxel.py run 'python3 /opt/battlecode/ops/as-arena.py arena pause'
python3 ops/blaxel.py run 'python3 /opt/battlecode/ops/supervisor.py stop'
```

`login` reads the key without echo, saving it outside the repository, mode 0600.
`pause` finishes current synchronous scheduling work before acknowledging; it
does not kill an active model task. Pause owner lanes too before maintenance.
`stop` interrupts descendants, preserves evidence and exits successfully, so the
provider does not immediately restart it. Start again using the managed command.
Pending/unknown API responses are not permission to resubmit a write: inspect the
named process first. Never start a second supervisor to bypass a held lock.

In the Blaxel console, select **banabolabs → battlecode-arena → Terminal**.
As root, these are the manual owner actions for a fresh installation (already
completed for this pilot):

```bash
runuser -l bc-alpha -c '/usr/local/bin/codex login --device-auth'
runuser -l bc-beta -c '/usr/local/bin/codex login --device-auth'
```

Approve each in the intended owner's browser/account. Separate browser profiles
help avoid choosing the same account accidentally. Existing Colab logins were
not copied. Never paste tokens, auth files or device codes into this repository
or chat. Device authentication may require enabling the owner's ChatGPT setting.
The arena checks native login status, not credential contents.

Add this server's public key under the repository's **Settings → Deploy keys**,
with **Allow write access**:

```text
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJL8jf/OxEwhaaKvrDPoBjNx27GYMQCrGMlxLemOfU+S battlecode-arena-blaxel
```

After both owners confirm the intended distinct accounts, the operator runs:

```bash
python3 /opt/battlecode/ops/supervisor.py stop
python3 /opt/battlecode/ops/configure-owners.py --confirm-distinct-owner-accounts
```

Start the managed supervisor again from the operator computer, then in the root
terminal resume the lanes and scheduling:

```bash
runuser -l bc-alpha -c 'arena-client --config /etc/battlecode/alpha.json resume'
runuser -l bc-beta -c 'arena-client --config /etc/battlecode/beta.json resume'
python3 /opt/battlecode/ops/as-arena.py arena start
python3 /opt/battlecode/ops/as-arena.py arena acceptance-report
```

No model job is started by `configure-owners.py`. Explicit resume is required.
An authentication, permission or quota error parks the affected lane; do not
copy another account's credentials or route its task to the other account.

Console access is optional. The trusted operator can start each native owner
login through `ops/blaxel.py run ... --keep-alive --name OWNER-login`, retrieve
that named process's output with `ops/blaxel.py process OWNER-login`, and let
the intended owner approve the displayed device flow in their own browser.
Never commit temporary login codes or credential output. No Blaxel dashboard
account or transferred Codex auth cache is needed.

Change future invocations without interrupting an active job (root command):
`python3 /opt/battlecode-source/ops/set-worker-reasoning.py --model gpt-6.1-sol --effort high`.
This preserves unrelated native configuration and never opens auth caches.

## Evidence, recovery and maintenance

Root terminal commands:

```bash
python3 /opt/battlecode/ops/as-arena.py arena status
python3 /opt/battlecode/ops/as-arena.py arena backup
python3 /opt/battlecode/ops/as-arena.py arena compact
tail -n 50 /var/lib/battlecode-volume/supervisor/arena.log
tail -n 50 /var/lib/battlecode-volume/supervisor/alpha.log
tail -n 50 /var/lib/battlecode-volume/supervisor/beta.log

# Stop before code upgrade. Never replace an active engine/map lock.
python3 /opt/battlecode/ops/supervisor.py stop
git -C /opt/battlecode-source pull --ff-only
python3 /opt/battlecode-source/ops/upgrade.py

# With services stopped, optional publication cap: positive count or none.
python3 /opt/battlecode/ops/set-cycle-limit.py none
```

After upgrade start the managed supervisor again. Worker and source transactions
retain their actual input revisions. Interrupted coding attempts are checkpointed
and parked, not replayed automatically. Queued/running games reconcile sealed
completion artifacts; unknown outcomes never become invented losses.

From the operator machine, compact live status needs no console access:
`python3 ops/blaxel.py run 'python3 /opt/battlecode/ops/loop-status.py'`.
Improvement is paced once per hour per bot, including unchanged feedback, as
requested by the owner. A blocked or still-evaluating lane remains parked; no
additional model call is made merely to poll it.

Daily backups are consistent SQLite snapshots plus manifests, **not complete
off-host replay backups**. Download/copy the referenced source, replay and lock
trees to an independent destination as well. Disk pressure pauses work; no
automatic destructive pruning is configured. Private owner model logs are not
public artifacts. `ops/blaxel.py download` only accepts arena artifact prefixes.

Controlled checks (owners paused, no queued/active games):

```bash
python3 /opt/battlecode/ops/restart-check.py --unit arena
python3 /opt/battlecode/ops/restart-check.py --unit supervisor
python3 /opt/battlecode/ops/host-check.py
python3 /opt/battlecode/ops/supervisor.py stop
python3 /opt/battlecode/ops/volume-check.py
```

Process crash and volume remount drills are not proof of a physical VM reboot.
Provider archive/unarchive availability and its actual test outcome are tracked
in the acceptance status. [Archive/unarchive is private preview, not recommended
by Blaxel for production](https://docs.blaxel.ai/Sandboxes/Archive).
Do not delete/recreate this sandbox to simulate a reboot. If its root filesystem
is lost, preserve the volume and restore the recorded trusted infrastructure
revision before using existing state; bootstrap refuses to reset that state.

## Adding another owner later

Keep concurrency and promotion thresholds unchanged. Stop services and run
`python3 /opt/battlecode/ops/add-worker.py BOT_ID` as root. This registers a new
disabled identity, persistent private home and mailboxes. Publish/ingest its
initial source with `bootstrap-lanes.py` as `bc-arena`, create its own writable
clone of branch `bot/BOT_ID` using public HTTPS, and perform that owner's native
login. Attest ownership and resume only after its baseline passes. The supervisor
reads the registry; it does not require another daemon implementation. Initial
pilot acceptance still concerns exactly alpha and beta.

The earlier 100 GB volume request was rejected; the working allocation is 8 GB.
Tier 2 advertises 32,768 MB maximum RAM and 8,192 MB per volume. Effective quota
overrides are not readable by this service credential; no denial was bypassed.
The server reports no expiration, but that is not an unconditional lifetime SLA.
The previously existing `cpu-box` was never changed. Rotate the API key shared
in chat through its owner; no copy is installed on the arena or workers.

## Manual contest export and exploratory matches

The source ZIP can be prepared without a contest login or any official mutation:

```bash
python3 /opt/battlecode/ops/as-arena.py python3 /opt/battlecode-source/ops/export-candidate.py --bot alpha --commit 4922166cd44fa0bc1291cf9ccd9b05125cfcb84a
```

Exports under `/srv/battlecode/public/exports/` include a manifest recording the
exact commit, source/ZIP hashes and local evidence. Existing exports are never
overwritten. The first export is already saved; download that existing file.
This invokes official `cambc bundle`, not `submit`; it neither activates a bot
nor claims contest eligibility/production parity. A branch tip is not a selected
submission. Review the team's current AI/sharing/build rules and submission
selection effects before manually uploading through its authenticated UI.

Use the user-supplied unranked chooser only after logging into the contest.
Current challenge quotas/controls and supported automation remain unverified;
no automatic challenge endpoint is invented or enabled. Start one manual
challenge, preserve the official submission/match IDs and original replay, and
record the opponent revision as unknown if not exposed. External import stores
original files separately and now supplies bounded metadata in that lane's next
task. It never counts as frozen local promotion evidence.

The owner has since authorized guarded automatic publishing, and native official
CLI login succeeded. [Official integration status](../docs/OFFICIAL_AUTOMATION.md)
records the implemented selection monitor and remaining platform blockers.
Enable historical training and bounded full suites only with services stopped:
`python3 /opt/battlecode/ops/enable-exploration.py`. This does not enable uploads,
challenges or automatic promotion and does not change any credential.

Exploratory external games can suggest hypotheses, not reveal private opponent
source or justify live omniscient inputs. Keep a fixed regression benchmark and
a diverse history pool. Periodic strong and near-peer opponents complement
incremental local repairs; avoid tuning every iteration to a single top opponent.
