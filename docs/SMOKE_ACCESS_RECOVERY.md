# Own-smoke evidence access and recovery

The slice authorization gate originally knew only evaluation and continuous
training membership. `bot-check` returns smoke match IDs before those matches
belong to an evaluation, so legitimate own-smoke requests were rejected. Beta
and gamma obeyed their permission-denial instructions and preserved BLOCKED
results instead of publishing checked candidates.

The gate now also recognizes arena-written `check:TASK:SOURCE` reports joined
to the lane's trusted task and exact match/source identity. This includes old
reports without a schema migration. Development-map restrictions, holdout
denial, bounded file allowlists and cross-lane privacy remain enforced. The
current and immediate prior tasks' four most recent smoke checks per lane are
retained so ordinary pruning does not destroy evidence during a pause or the
handoff to the recovery task.

An adjacent publication race is fixed: ingestion now links a trusted published
commit to its approved task and edit-base hash before any evaluation can start.
Previously a fast Git poll could start a legacy three-map screen before the
worker-finished message attached the six-map workflow task. Old scores are not
relabeled or treated as if missing cases had run.

Stop services before installation. After upgrading, run the narrowly scoped
recovery as the arena user while scheduling remains paused:

```bash
python3 /opt/battlecode/ops/as-arena.py python3 /opt/battlecode/ops/resolve-smoke-pauses.py --bot beta --bot gamma
```

This verifies final statistics and both bot logs for each side of the most
recent passed check. Only the known smoke-access blocker is resumable. The
original BLOCKED result, source, notes, and checkpoint are not overwritten or
published automatically. A trusted finding directs the next task to inspect
that preserved work and recheck before proposing it. Authentication, quota,
other permissions, leases and pending evaluations are not bypassed. The
operator receipt makes repeated recovery idempotent for that task.

Restart the managed supervisor and send `arena start` to resume the continuous
loop. Hourly per-lane model spacing and the single global model slot are
unchanged; games continue between model jobs.

## Live verification, 18 October 2026

Runtime `13ad10e00bd1fe44b2c5e3f0cc276e607932c717` is installed. All 114
automated orchestration checks passed. Twelve reads of the previously blocked
smoke statistics/log files succeeded, as did requests through both owners'
normal clients. Beta recovered the exact preserved source, passed a new check,
read both smoke logs, and published `d2d57274232ca7cead5bacf650d6f51fd5b3bc3d`.
Its full nine-map evaluation is running; no win-rate claim is made yet.

At the recorded snapshot gamma's recovery task was RUNNING, alpha and beta
were WAITING_EVALUATION, and the continuous loop had completed 5,430 games
(up from 5,420 before the final restart). All four service units had zero
unexpected restarts, no lane was paused, and about 3.34 GB remained free.
Both lanes' prior smoke files were still available and protected across the
handoff. See the [exact live record](../evidence/blaxel/smoke-access-recovery-20261018.json).
No owner login was needed. Physical provider reboot persistence is still
unverified; this record demonstrates controlled service restarts, not a reboot.
