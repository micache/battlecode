# Temporary Colab pilot

This is an explicitly owner-approved deviation from the persistent-VM deployment.
Colab PID 1 is `docker-init`; there is no running systemd manager and cgroup v2 is
read-only. **Machine-reboot persistence is unverified.** Runtime destruction can
erase `/srv`, `/opt` and all three homes, including manually established logins.
The standard systemd units and `OPERATIONS.md` remain the persistent-VM path.

The temporary adapter uses rootless Bubblewrap user, PID, network, IPC and UTS
namespaces, dropped capabilities, a read-only root/toolchain, private writable
work/output/tmp paths, CPU affinity and kernel file/CPU/process/descriptor limits.
Aggregate RSS (2 GiB), tasks (128) and writable disk (1 GiB) are sampled by a
100-ms watchdog; they are **not cgroup-hard aggregate limits** and may overshoot.
There are no owner homes, host procfs, network interfaces or credential mounts.
A static private `/proc/self/exe` link supports the pinned CLI's self-launch;
the same pinned WASI resources are mounted at its compiler resource prefix.
Neither rounds nor game fuel are increased.

Run these as the Colab administrator, in a clean clone of a committed revision:

```bash
python3.12 ops/provision.py
python3.12 ops/remote_bootstrap.py
# Install the native Codex CLI separately; owner login is NOT part of installation.
python3.12 ops/install.py --source "$PWD" --temporary-colab
python3.12 /opt/battlecode/ops/prepare-colab.py
runuser -u bc-arena -- arena init
runuser -u bc-arena -- arena starter-check
```

Inspect the two saved starter replays/statistics and real diagnostic fixtures,
then install the reviewed parser contract exactly as in `OPERATIONS.md` and run
`arena starter-check --normalize-only`. A parser-pending attempt is preserved,
not retried as if a transient engine failure occurred. Its review record lives
outside the original sealed attempt. Official uploads/challenges remain disabled.

Owners authenticate independently in their own terminal, selecting their intended
ChatGPT account in the browser for each device-code approval:

```bash
runuser -l bc-alpha -c '/usr/local/bin/codex login --device-auth'
runuser -l bc-beta -c '/usr/local/bin/codex login --device-auth'
python3.12 /opt/battlecode/ops/configure-owners.py --confirm-distinct-owner-accounts
```

Give only `bc-arena` a repository-scoped GitHub write credential. Add its public
deploy key in repository settings with write access; never copy a private key or
an owner's Codex cache. Once starter verification passes:

```bash
runuser -u bc-arena -- python3.12 /opt/battlecode/ops/bootstrap-lanes.py
python3.12 /opt/battlecode/ops/colab-supervisor.py start
runuser -u bc-arena -- arena start
# After provisional baselines finish, create independent owner clones:
runuser -l bc-alpha -c 'git -c safe.directory=/srv/battlecode/repos/source.git clone --branch bot/alpha /srv/battlecode/repos/source.git /home/bc-alpha/battlecode'
runuser -l bc-beta -c 'git -c safe.directory=/srv/battlecode/repos/source.git clone --branch bot/beta /srv/battlecode/repos/source.git /home/bc-beta/battlecode'
runuser -l bc-alpha -c 'arena-client --config /etc/battlecode/alpha.json resume'
runuser -l bc-beta -c 'arena-client --config /etc/battlecode/beta.json resume'
```

The pilot caps publication at two cycles per bot. One global model lock, one build
and one match remain enforced. Quota waits do not transfer a task between owners.
Three-map evaluations cannot automatically replace a champion; the full gate
remains required before automatic promotion.

Exact runtime commands (administrator terminal, independent of the SSH session):

```bash
# Status
python3.12 /opt/battlecode/ops/colab-supervisor.py status
runuser -u bc-arena -- arena status
runuser -u bc-arena -- arena acceptance-report

# Start/resume
python3.12 /opt/battlecode/ops/colab-supervisor.py start
runuser -u bc-arena -- arena start

# Pause new scheduling, leaving services and evidence available
runuser -u bc-arena -- arena pause

# Stop all service descendants; keep state and preserved attempts
python3.12 /opt/battlecode/ops/colab-supervisor.py stop

# Restart services; reconcile interrupted attempts under the singleton DB lock
python3.12 /opt/battlecode/ops/colab-supervisor.py restart

# Consistent backup and restore drill (new destination, service stopped for drill)
runuser -u bc-arena -- arena backup
python3.12 /opt/battlecode/ops/colab-supervisor.py stop
runuser -u bc-arena -- arena restore-drill /srv/battlecode/backups/BACKUP_ID/arena.sqlite /srv/battlecode/state/restore-drill.sqlite
```

Root-owned supervisor logs/identities are in `/run/battlecode-colab`. A subreaper
per service kills adopted match/model descendants before restarting that service.
SSH disconnect and service restart must be demonstrated with actual heartbeats
and saved attempts; neither is a machine-reboot test. Back up artifacts and the
consistent database to a selected persistent destination before ending Colab.

For a code upgrade, stop services, pull a clean committed tree, then run
`python3.12 ops/upgrade.py`. It retains the previous `/opt` tree, preserves `/srv`
and owner homes, repins infrastructure/build identity, and starts nothing.
