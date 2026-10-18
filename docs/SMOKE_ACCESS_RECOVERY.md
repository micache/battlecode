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
latest task's four most recent smoke checks per lane are retained so ordinary
history pruning does not destroy evidence during a pause.

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
