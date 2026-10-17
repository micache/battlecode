# Local worktree archive relay

17 October live checkpoint: [45 acknowledged batches](../evidence/blaxel/local-offload-20261017.json)
moved 2,067,458,640 redundant project bytes from 540 distinct matches into
508,631,444 local archive bytes. All those acknowledgements followed verified,
fsynced local copies. The enabled timer completed successfully and
`loginctl show-user micache -p Linger` reported `Linger=yes`. Subsequent timer
cycles continue the backlog; these counts are a historical checkpoint.

The server's large `project.zip` files contain redundant full per-match working
directories. The local relay moves those bytes to this operator computer;
**all replays, statistics, bot/runner diagnostic logs, normalized results,
source snapshots, notes and feedback remain on the server**. Workers require no
local-machine connection to read gameplay evidence. The newest 20 completed
matches retain their working-directory archives online too.

Archives live outside Git at
`/home/micache/.local/share/battlecode-arena-archive`, mode 0700. Every batch
has its original completion manifests and project-member hashes. Batches use
XZ-compressed TAR to compress repeated SDK/cache bytes across project ZIPs;
the relay also accepts earlier uncompressed TAR batches after restart. The client
checks transport SHA-256, manifest attribution and every inner ZIP member,
fsyncs the archive and receipt, then sends an acknowledgement through the
trusted operator mailbox. Worker mailboxes cannot acknowledge offloads.

Only the sole arena writer can replace the attempt with a newly sealed compact
copy. That copy preserves the original completion manifest, local archive
address/checksum, normalized result, and all online gameplay artifacts. Legacy
paths remain aliases. No verifier is changed to pretend that missing raw bytes
are present. Pending transfers, partial acknowledgements and cleanup are
reconciled after restart. Corruption or ambiguous API outcomes preserve source
bytes and stop the relay for inspection.

## Operations on this computer

The systemd **user** timer runs every five minutes after the previous invocation:

```bash
systemctl --user status battlecode-offload.timer battlecode-offload.service
journalctl --user -u battlecode-offload.service -n 30 --no-pager
systemctl --user start battlecode-offload.service
systemctl --user stop battlecode-offload.timer
systemctl --user start battlecode-offload.timer
python3 ops/offload-local.py --max-batches 100
```

The relay holds a local single-writer lock, uses the existing operator API key
outside the repository, and never starts model jobs or reads owner credentials.
It requires a running remote supervisor, including when scheduling is paused.
The remote side accepts offload messages through its operator control mailbox.

For a new operator installation, link the supplied units with `systemctl --user
link "$PWD/ops/systemd/battlecode-offload.service"
"$PWD/ops/systemd/battlecode-offload.timer"`, then enable the timer. Keeping user
services running after logout requires `loginctl enable-linger micache`; if
policy denies it, an administrator must run that command. Do not claim logout
persistence merely because an interactive relay succeeded.

This computer must remain powered on and connected. If unavailable, the server
continues with available headroom and eventually parks at its existing disk
guard. This is not unlimited storage or an off-site replicated backup. The
relay maintains a 2 GiB local free-space reserve. Other server data (especially
build caches and owner CLI histories) can still grow and need separate capacity
management. Neither quota waits nor safety thresholds are bypassed.

## Restoring an archived worktree

Find the batch in a match's `project-offload.json` or the local `receipts/`
index. Verify the batch against the receipt's `plan` with
`verify_batch` from `ops/offload-local.py`. The TAR contains
`MATCH_ID/project.zip`, `MATCH_ID/project-archive.json` and
`MATCH_ID/completion.json`. Extract into a **new scratch directory**, then unzip
`project.zip` there and check every member against `project-archive.json`.
Never restore over sealed server evidence or a live worker checkout. Archive
files can contain untrusted bot source; do not execute them on this machine.

Runtime change rollout remains stop → install committed code → restart. A
successful transfer is not a claim that official-match logs were downloaded;
that requires a real match/submission identity and authorized replay access.
