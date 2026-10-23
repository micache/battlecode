# 23 October liveness fix

Two infrastructure defects stopped progress without killing services:

- Every raw game in active/full evaluations was pinned. Their retained files
  exceeded the 768 MiB target; the scheduler treated that target as a hard stop.
  Consequently the evaluations could never finish and release their pins.
- An explicit creation-command HTTP 429 left an UNKNOWN intent forever. It
  correctly prevented a blind retry, but also prevented collecting identified
  games. Only heartbeat liveness was monitored, hiding the lost progress.

Rolling storage now first prunes routine raw history, then the oldest
non-representative suite files if necessary. Normalized results, evaluation
membership, source/build identities and compact lessons stay in SQLite/Git.
Parser/bootstrap/check-recovery evidence and bounded loss/win examples stay;
up to 120 recent games fit within a quarter of the history target. Worker
feedback prefers available traces and marks retired traces explicitly.
The target triggers cleanup, not a scheduling deadlock. Physical free space
below the safety floor still stops new work. No scoring gate is reduced.

Status includes progress health and last completed match time. The non-systemd
watchdog detects queued games without progress for at least 30 minutes, even
with a fresh heartbeat, and restarts the exact owned process tree. Intentional
pauses and explicit storage/access/adapter blockers are not bypassed.

Outside creation errors are saved with their intents. The existing approved
operator browser reads official own-team history, with the UI-observed
`scope=team` and `before` cursor. A fresh complete request-window history can
adopt exactly one actual, source-matching group. A closed window with no group
after an explicit HTTP 429 records NOT_CREATED and waits before a new intent.
Incomplete/stale history, multiple matches, claimed groups and non-quota
negative evidence leave UNKNOWN blocked. No creation is blindly retried.
Identified groups may still be collected while a new creation is unknown;
access/source/schema denials still stop the relevant sidecar.

Browser HTTP 429 respects Retry-After with a 60-second minimum, without
permanently wedging source proofs. Authentication/permission denials still
require review. The browser remains owner-authenticated on the operator
machine; its availability is still required for new source/history proofs.
Loss of this connection must not stop private games.

Deployment follows the normal pause, stopped-service upgrade and restart
procedure. Saved suites and queued jobs are preserved, not restarted or
relabelled. Verify advancing real games, bounded retention, outside imports
and progress health before handing off. Reboot persistence is not established
by a process restart test.

## Saved deployment observations

Runtime `ecffa1b57359a5262a23da9ad426b281fbe1322b` was installed with
services stopped. The pre-change backup and unchanged workload fingerprint
cover 18,138 jobs. Rolling maintenance retired 851 old raw game directories
(about 192 MiB); normalized results, frozen inputs and attempt counts were
unchanged. Restart recovery passed. The legacy 429 intent became NOT_CREATED
only after fresh own-team history covered its entire closed request window
with no matching group. The previously stuck five-game series then imported.

At the saved live check, 38 further private games had completed with zero bot
faults, all five service units were alive, health was WORKING and the full
40-map suites remained intact. 176 local regression tests passed. Receipts:
`evidence/blaxel/stability-{retention-repair,legacy-throttle-review,restart,live-check}-20261023.json`.
These are bounded observations, not a claim of unlimited uptime.

Creating the next outside series exposed the native CLI's seven-day contest
session expiry (`Sign in first with cambc login`). Owner renewal was requested
immediately. This explicit authentication stop is separate from the repaired
retention/429 faults and does not stop private matches or their evaluations.
