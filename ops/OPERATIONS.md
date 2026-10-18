The pilot has exactly two independent owners, `bc-alpha` and `bc-beta`, with branches `bot/alpha` and `bot/beta`. One scheduler serializes matches and builds; a shared kernel lock limits Codex to one invocation. Workers start disabled and paused. The arena user alone holds GitHub write access. Workers clone its read-only mirror, submit source through their own mailboxes, and cannot write the mirror, database, rules, thresholds or service files. Neither worker needs GitHub credentials.

For the deployed Blaxel pilot, use [BLAXEL.md](BLAXEL.md) and the [current status](../docs/IMPLEMENTATION_STATUS.md). The commands below target a standard systemd VM, not Blaxel. Historical synthetic validation remains in `evidence/local-validation.json`; real server evidence is in `evidence/blaxel/`.

Install on the selected server as an administrator, after committing/pushing the implementation to the assigned repository. `/srv/battlecode` must be persistent local storage. A normal Colab runtime may lack systemd and may disappear when its allocation ends; the installer checks systemd and requires an explicit persistent-volume acknowledgement. A service cannot survive destruction of the underlying VM.

```bash
git clone https://github.com/micache/battlecode
cd battlecode
python3 -m unittest discover -s tests -v
sudo apt-get update
sudo apt-get install -y python3 git podman uidmap slirp4netns fuse-overlayfs
sudo bash ops/install.sh --ack-persistent-volume
```

The install script creates all three users with mode-0700 homes, private owner groups and independent config paths. It does not authenticate anyone, start services or overwrite an existing installation. Inspect `/etc/subuid` and `/etc/subgid` for non-overlapping ranges allocated to `bc-arena`; `useradd` normally creates these. A missing allocation is an administrator blocker, not grounds for privileged containers. Verify rootless Podman with `bash ops/as-arena.sh podman info`.

Bootstrap the trusted toolchain with network access once. No owner credential is available inside this image. Wheel and binary hashes are checked, the SDK and official C++ starter are generated, and the starter must compile during image construction. The resulting image ID, SDK/template hash, compiler package versions and recipe hash are recorded in the runtime lock. The bootstrap base tag is resolved once into that immutable local image; builds and games use `--pull=never --network=none`.

```bash
bash ops/as-arena.sh bash /opt/battlecode/ops/prepare-engine.sh
bash ops/as-arena.sh arena init
bash ops/as-arena.sh arena starter-check
```

The last command saves two full starter games, reversing the named verification assignment. Identical starter games are explicitly marked as deterministic repetitions. It omits round, fuel and seed overrides. A first run without a reviewed parser intentionally cannot score. Inspect the real files under `/srv/battlecode/matches/<match-id>/<attempt>/artifacts/` as `bc-arena`: `final.json`, stdout/stderr and `.repl26a`. Use the official visualizer to compare each replay outcome with the statistics.

Create `/etc/battlecode/parser.json` as administrator only after that inspection. It contains protocol version 1, the pinned `engine_sha256`, `reviewed_by`, `fixture_path` (the saved `final.json`), its `fixture_sha256`, `replay_agreement_verified: true`, `winner_pointer` (JSON Pointer), and `winner_values` mapping the *observed* raw values to absolute `A`/`B`. Completion uses either `completion_mode: "field_equals"` with observed `complete_pointer`/`complete_value`, or `completion_mode: "final_statistics_contract"` after verifying the CLI emits statistics only for completed games. Optional `reason_pointer` and `metric_pointers` must refer to observed fields. Only add `bot_fault_patterns`, `truncated_patterns` and `fuel_suspension_patterns` demonstrated by saved fixtures. `fault_detection_verified` stays false until a deliberately crashing fixture is distinguished from death and fuel suspension. No guessed engine field names ship in this implementation.

```bash
bash ops/as-arena.sh arena starter-check --normalize-only
```

Both games must be complete, replay agreement reviewed and fault detection verified before `starter_verified` becomes true. Normalization review is stored separately from the original sealed raw artifact. If a full game exceeds 300 seconds, preserve the timeout evidence, measure the valid duration and deliberately raise `limits.match_timeout_seconds`; never convert a timeout into a loss or increase fuel.

Only now configure the arena user's GitHub access manually, preferably an SSH key or credential helper scoped to this repository. Do not put tokens in a remote URL, config file, image or worker home. Competition login is unnecessary; official uploads and challenges remain disabled. Then publish the initial lanes and establish the two baselines:

```bash
bash ops/as-arena.sh python3 /opt/battlecode/ops/bootstrap-lanes.py
sudo systemctl enable --now battlecode-arena.service battlecode-backup.timer
bash ops/as-arena.sh arena start
bash ops/as-arena.sh arena status
```

The bootstrap publisher preserves existing branches instead of overwriting them. For a newly created lane it adds the official starter and notes in a normal commit parented by the pinned infrastructure revision. It preserves an independent arena-owned Git commit of the official starter as a fixed opponent, so existing lane bots need not be replaced. Initial baselines use three maps and both sides. They need validity, not an improvement over a nonexistent incumbent. Subsequent three-map candidates remain provisional; they cannot replace an incumbent.

Each owner now logs in manually under their own Linux user. Install the unmodified official Codex CLI following its current installation instructions, verify the binary/version, and perform subscription login. Commands below are repeated independently for beta. Use the owner's actual CLI path if it differs from the initial config. The arena never reads the owner's auth cache.

```bash
sudo -iu bc-alpha
codex --version
codex login --device-auth
codex login status
chmod 700 ~/.codex
git clone --branch bot/alpha /srv/battlecode/repos/source.git ~/battlecode
sha256sum "$(command -v codex)"
exit
```

As administrator, record that owner's executable path and SHA-256 in `/etc/battlecode/alpha.json`, and their chosen model if desired. Confirm the current native login reports ChatGPT rather than API authentication; the wrapper checks this again before each invocation. In `/etc/battlecode/arena.json`, set only that owner's `enabled` and `owner_confirmed` flags to true. No credential files are copied between users. No API keys, API helpers, third-party providers, paid fallback or quota failover are supported.

```bash
sudoedit /etc/battlecode/alpha.json
sudoedit /etc/battlecode/arena.json
sudo systemctl restart battlecode-arena.service
sudo systemctl enable --now battlecode-worker@alpha.service
sudo -iu bc-alpha arena-client --config /etc/battlecode/alpha.json resume
```

Enable beta through the same steps after alpha's end-to-end loop works. Starting both worker services is safe: task dispatch and the common lock permit only one active Codex job. Each CLI call has its own 20-minute limit, task-specific final file, private raw log, patch, untracked source/notes checkpoint and immutable trusted envelope. The wrapper starts source from the accepted snapshot even when the branch tip contains a rejected experiment. Only exact-source trusted smoke checks authorize central publication. The central publisher records a normal commit before pushing, never force-pushes, and retains its intent if a push is ambiguous.

Routine commands, as administrator unless an owner command is shown:

```bash
# Status, including auth/quota waits, source tips, queue counts, heartbeat and disk use.
bash ops/as-arena.sh arena status
bash ops/as-arena.sh arena acceptance-report
sudo systemctl status battlecode-arena.service battlecode-worker@alpha.service battlecode-worker@beta.service
sudo journalctl -u battlecode-arena.service -u battlecode-worker@alpha.service -u battlecode-worker@beta.service --since today

# Start/resume scheduling (the service must be running).
sudo systemctl start battlecode-arena.service battlecode-worker@alpha.service battlecode-worker@beta.service
bash ops/as-arena.sh arena start

# Pause new scheduling. Already running work completes before acknowledgement.
bash ops/as-arena.sh arena pause
sudo -iu bc-alpha arena-client --config /etc/battlecode/alpha.json pause
sudo -iu bc-beta arena-client --config /etc/battlecode/beta.json pause

# Stop all descendants and persist interrupted attempts for restart reconciliation.
sudo systemctl stop battlecode-worker@alpha.service battlecode-worker@beta.service battlecode-arena.service

# Restart; systemd kills old cgroups before the single writer reconciles artifacts/attempts.
sudo systemctl start battlecode-arena.service battlecode-worker@alpha.service battlecode-worker@beta.service
```

Global start/pause, backup and compaction use an administrator-only control mailbox; only the daemon writes SQLite. A command queued during a long match may report pending after 60 seconds. Inspect status instead of submitting duplicate requests. Stopped-service setup commands (`ingest`, `register-toolchain`, `verify-readiness`) acquire the same service lock and refuse a second writer. Scheduler infrastructure failures get at most one automatic retry, then the adapter pauses; use `arena adapter-resume` only after resolving the reported cause.

Owner status and evidence commands:

```bash
arena-client --config /etc/battlecode/alpha.json status
arena-client --config /etc/battlecode/alpha.json feedback
arena-client --config /etc/battlecode/alpha.json slice --match-id MATCH_ID --file stderr.log --offset 0
```

Quota responses park only that lane until the provider reset plus jitter. An unknown reset uses 30 minutes, one hour, two hours, then four hours. Independent beta work may run; an alpha task is never transferred to beta. Authentication and permission failures require the owner/operator to fix the underlying condition and resume. A missing/malformed final result, timeout or ambiguous publication preserves work and pauses instead of committing.

For laptop handoff, first pause the owner lane and confirm `active_writer: false`, then claim its lease:

```bash
arena-client --config /etc/battlecode/alpha.json pause
arena-client --config /etc/battlecode/alpha.json claim --owner alpha-laptop
```

Claim returns a trusted manual task and creates its private server attempt. Copy only the owned source/notes and task state to the laptop. Keep the server credential cache on the server. Copy the edited files and structured final result back into that attempt. Publish with `arena-client --config /etc/battlecode/alpha.json publish --attempt /home/bc-alpha/attempts/TASK_ID --owner alpha-laptop`; the normal exact-source checks, ownership validation and central publisher still apply. Release after publication or a no-change handoff, then wait for any pending evaluation before resuming:

```bash
arena-client --config /etc/battlecode/alpha.json release --owner alpha-laptop
arena-client --config /etc/battlecode/alpha.json resume
```

Before automatic promotion, retain the full gate: all currently published frozen maps (17 as of 18 October), both sides, three distinct fixed source opponents (including starter/history), common-opponent incumbent comparison, and incumbent head-to-head. Gain must be at least 0.05, no covered-map decline greater than 0.25, no holdout aggregate decline, and verified reliability. Full evaluation is not downgraded by a daily counter. Holdout game files are arena-private; workers get aggregate holdout feedback and development-only slices. See docs/TOOLCHAIN_225.md for the current release-mode migration.

Save actual runtime settings evidence with all `arena.engine.PROFILE` values. Register a new engine lock with `arena register-toolchain --image-id IMAGE_SHA256 --template /srv/battlecode/repos/official-template --compiler-record /srv/battlecode/locks/compiler-record.json --profile-record PROFILE_RECORD.json`; the profile record contains `effective_profile` and `evidence: {path, sha256}`. This changes build identities: rebuild and repeat starter verification. Then provide `arena verify-readiness EVIDENCE.json` with that lock hash, profile, and hashed saved artifacts for each required check listed in `arena/operations.py`. Set `automatic_promotion` true and a new suite version only after those checks and three distinct opponent revisions are registered. Engine/map changes require explicit staging, pins, rebuilds and new evaluation identities; do not overwrite active files. Official automation remains false regardless of local readiness.

Retention and backups:

```bash
bash ops/as-arena.sh arena backup
bash ops/as-arena.sh arena compact
```

The daily timer requests a consistent SQLite backup with manifest hashes. The owner must select a separate persistent backup destination and copy the database, manifest and referenced artifact/source/lock trees there. Database backups alone do not include replays. New work pauses at the 10 GiB artifact budget or below 2 GiB free. Compaction compresses ordinary replays older than 14 days, retaining champion, running-suite, starter and representative-failure evidence. Verified compressed bytes replace only the exact old attempt; `gzip -dk` restores each replay. An interrupted compaction retains its staging/original copies and requires inspection. No automatic destructive pruning is performed. Configure host journald retention as administrator; private worker logs remain under their owner.

Restore drill, with the service stopped and a new destination path:

```bash
bash ops/as-arena.sh arena restore-drill /srv/battlecode/backups/BACKUP_ID/arena.sqlite /srv/battlecode/state/restore-drill.sqlite
```

Inspect the restored tables, manifest checksums and artifact references before considering activation. To roll back code, stop all three services, preserve `/srv/battlecode` and owner homes, install the previous pinned infrastructure tree under `/opt/battlecode` after moving the current tree to a named backup, restore its config/units, and run `systemctl daemon-reload`. Do not downgrade a database across an incompatible schema; this version uses protocol/schema 1. Restore the matching database/locks/artifacts as a set if needed. Keep both copies until the recovery drill passes.

For a manual authorized external match, copy its downloaded replay as that owner to `/srv/battlecode/external-inbox/alpha/NAME.repl26a`. Metadata JSON must include the actual `official_match_id`, own `submission_id`, known ingested `source_commit`, explicit outcome `A`/`B`/`UNKNOWN`, `opponent_version` (null when unknown), and `staged_replay: "NAME.repl26a"`. Then run `arena-client --config /etc/battlecode/alpha.json import-external --metadata metadata.json`. Original bytes/checksums are retained separately; these results never enter controlled local scores. There is no submission or challenge creation code.

Acceptance on the real server must retain two published/evaluated task cycles per bot with actual commit and match IDs in `arena acceptance-report`. Additionally record systemd heartbeats across a real SSH disconnect, restart during a running game (one validated outcome, distinct interrupted attempt), simulated quota isolation, host credential/network denials, engine mechanic fixtures, and a restore drill. A unit definition or a synthetic test is not evidence that an SSH disconnect or reboot succeeded. See `docs/IMPLEMENTATION_STATUS.md` for the currently pending items.
