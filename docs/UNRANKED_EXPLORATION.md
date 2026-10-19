# Outside exploration — 19 October 2026

The owner explicitly authorized using the selected v6 C++ submission and the
shared 50-per-hour unranked allowance. Current official CLI **2.2.5** now provides
`ladder`, `match-groups create/quota/show/download`, and `matches summary --json`.
The old 2.1.6 interface review no longer describes challenge availability.

The official chooser says five maps per series, no rating changes, and a shared
team hourly allowance of 50. The authenticated native quota response confirms
`limit: 50`, `used`, `resetsAt`, `ready`, the team ID, and no maximum rank gap.
The [platform terms](https://battlecode.co.uk/terms), updated 17 September,
prohibit sandbox/network circumvention, private opponent-file access, collusion
and ladder manipulation. This implementation uses official unranked commands,
honors the shared allowance and does not change ratings. No blanket event-policy,
eligibility or official-upload automation certification is asserted.

## What runs

The separate supervised `exploration` unit uses the existing native contest CLI
login under `bc-arena`. It aims for one series every 72 seconds, **up to 50 series
or 250 games per hour**, subject to the actual shared quota, readiness, disk and
backlog. It rotates the current top 25 teams, refreshes the ladder hourly, and
uses five platform-selected maps. The current CLI exposes no side-selection
option: recorded sides are authoritative; do not claim balanced external sides.
There is one creation writer and at most 50 outstanding requests. This is a
target, not a claim that all allowance has already been consumed.

Every creation has a durable intent before its CLI invocation. Unknown outcomes
block new creations; no blind retry. Existing native login is used without
reading/exporting its token files. Only the unmodified CLI container receives
that credential directory; no bot source or model-owner home is mounted. A
website/auth/access failure stops this sidecar, never the private match loop.
Uploads and activation remain disabled. A teammate's new selection is not
overwritten or silently attributed to the pinned source.

The initial outside source is alpha commit
`82a14a04f0e6b68aac8a7e879d305b1a886b857c`, source hash
`6e362fd7cce836975fa615bc8b936109235fd320def63703761366586efabc25`,
official submission `a2f2ee53-88b2-4821-b06d-ac630b9d7eae` (v6). The downloaded
own ZIP was verified, not identified merely by filename. The first native series
against #1 Intercontinental Fish is
[`f921438f-1966-4702-a037-d0eb1e0d4034`](https://2026a.battlecode.co.uk/game/match-groups/f921438f-1966-4702-a037-d0eb1e0d4034).
All five games finished with losses. Own-team browser metadata independently
confirmed v6 actually played. These results do not measure today's worker edit bases.

## Source-proof limitation — important

CLI `show --json` currently omits submission IDs. The verified replay bundles
also lack source identity. We do **not** fabricate it from configuration.
`ops/attest-official-exploration.py` reads the actual own-team group metadata
using the owner's already-approved browser on the operator machine, then sends
only finished match/source facts to the server. No browser credentials leave
this computer, and this helper makes no contest mutations.

This source-proof timer requires this operator computer to be online and its
browser login valid. While it is unavailable, the server preserves requests and
does not misattribute their results; the outstanding limit eventually pauses
new outside challenges. The private arena continues independently. Fully
operator-independent source verification would require an official CLI that
exposes submission IDs or a separately owner-authenticated server browser.
This is not claimed solved by copying cookies or extracting CLI tokens.

## Feedback and storage

Each confirmed game downloads the official replay bundle and JSON-converted raw
statistics. The latter are losslessly gzipped. A small projection includes
actual per-champion metrics and selected recorded death/gem-loss/fuel events;
it does not guess the cause of a defeat. Map aliases are reconciled by the
actual map-byte hash, not spelling (`rushbait_v2` versus `rushbait-v2`).

Imports use normal arena mailboxes; this sidecar never writes central SQLite.
All three agents receive a compact last-hour overview and three readable loss
examples at their existing hourly improvement opportunity. The exact submitted
source is included in their frozen public-source packet. They can request
bounded `external-slice` diagnostics. Sharing applies only to this owner-approved
submission, never private worker notes/credentials or unrelated imports.
Reserved holdout traces remain unavailable; outside outcomes never enter local
promotion scores and imports do not trigger extra model jobs.

Raw outside downloads have a 256 MiB oldest-first budget after successful
import, with the latest hour retained. Central outside attachments have a
128 MiB rolling budget, preserving the newest 500 games. Immutable match/source
IDs, outcomes, checksums and compact learning records remain. Retired raw files
are permanently discarded, not offloaded. Disk guards remain enabled.

## Setup / status / pause / stop

Code changes use the existing stopped-service upgrade. As server administrator:

```sh
python3 /opt/battlecode/ops/as-arena.py arena pause
# Let any active model task finish before stopping.
python3 /opt/battlecode/ops/supervisor.py stop
git -C /opt/battlecode-source pull --ff-only origin main
python3 /opt/battlecode-source/ops/upgrade.py
python3 /opt/battlecode/ops/configure-official-exploration.py
# Start the managed ops/blaxel-start.py process, then:
python3 /opt/battlecode/ops/as-arena.py arena start
```

On the operator machine, install the source-proof timer:

```sh
systemctl --user link "$PWD/ops/systemd/battlecode-exploration-attest.service"
systemctl --user link "$PWD/ops/systemd/battlecode-exploration-attest.timer"
systemctl --user enable --now battlecode-exploration-attest.timer
systemctl --user status battlecode-exploration-attest.timer
```

Inspect server `public/official-exploration.json`, `public/official-pending.json`
and `supervisor/exploration.log`. The normal arena status embeds outside status.
Pausing the arena stops outside creations; an in-progress official game cannot
be cancelled locally. Stop all units with `ops/supervisor.py stop`; stop source
attestation with `systemctl --user stop battlecode-exploration-attest.timer`.
An access/rate stop requires reviewing the saved stop and respecting Retry-After
before explicitly resuming. An unknown creation requires reconciling its real
official group ID, not deleting the intent. A new team upload requires a new
verified source/submission mapping before changing this pinned configuration.

Native contest sessions expire after seven days. Renewal remains an owner login
action; this service never switches accounts or enables paid fallback.
