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
