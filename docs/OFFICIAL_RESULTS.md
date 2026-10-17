# Official loss feedback — 17 October 2026

The owner approved a separate local contest-browser login and reading their
team's history. No password/token is exported. Normal browser cookies are used
by Playwright; the arena server receives neither browser credentials nor private
opponent diagnostics. No submission, activation or challenge was performed.

## Actual collected evidence

The uploaded v3 archive, submission
`185d5f06-459c-440d-a386-3ccd51f55b2f`, is byte-for-byte identical to
`artifacts/submissions/beta-02ab89d1.zip`:

- Commit: `02ab89d1e111f8c75f726004ee54346f5e7e4d8a`.
- Source hash: `5ce83774dbb2ba2a893c9cf2c4a7d24919420b4f5a27ddbda77b8d106ae3a7b0`.
- ZIP hash: `e22bb00e433f622d2b6238d0957199f7a7a9786c6367d13b0f8d4cdbc7ed50dd`.
- All ten owner-provided IDs are five-map series: 50 completed games, 12 wins
  and 38 losses. All fifty original game archives are downloaded.
- All 30 completed v3 series available in the collected snapshot are downloaded:
  **150 games, 57 wins / 93 losses; nine series wins / 21 losses**. This is
  uncontrolled ranked evidence, not a fixed-opponent benchmark. Two error series
  are excluded rather than scored as strategic losses.
- The complete paginated history metadata snapshot contains 242 series across
  three own-team submissions. Older Python v1/v2 sources are preserved locally
  but have no registered arena-commit mapping and are not attributed to beta.
- Collection stopped on an actual HTTP 429 while downloading older v2 history.
  Forty-eight series bundles were saved across versions; older history download
  is **partial**, not complete. No automatic collector timer is enabled.

The [official match overview](https://2026a.battlecode.co.uk/game/match-groups/9c808ab1-204b-4a41-bc28-089463a0c1d9)
exposes outcomes, drafts, gem scores, rounds and own-team diagnostics. Opponent
source revisions/diagnostics remain private. Raw bundles contain per-game
replays, own stdout/debug/fuel data. No verified decoder for the binary replay
or fuel format is claimed. The submitted source logs little strategic detail;
shared-round messages are not authoritative current-round measurements.

Official metadata identifies patch
`0.0.3:d7e29ae3546357b011419c764204b7b9e2232bdb1b07868250c6b35d4c18d2a5:1`,
whereas the pinned local CLI embeds engine 0.0.1. Some official maps are absent
from the frozen nine-map suite. External feedback flags these discrepancies;
it cannot establish local/production parity or silently update a scored suite.
The source ZIP is an older candidate, not the latest bot branch tip.

## Feedback and storage

All 150 mapped games were imported through beta's normal owner mailbox, not a
second database writer. Each import retains the official individual game ID,
series ID, absolute own/winning sides, old source/ZIP identity, patch, compact
observations, original metadata and exact raw-archive/member SHA-256 references.
Compact stdout reports explicitly distinguish extracted literal messages from
undecoded binary timeline markers. Original bundles stay locally available.

The existing three-example handoff now prioritizes readable development-map
losses across different maps. Unknown/holdout detailed traces remain reserved;
unknown opponent versions stay unknown. Imports do not trigger extra model
calls: beta consumes this evidence at its next normal hourly improvement task.
External observations never count toward local promotion scores.

Private local storage, outside Git:

```text
~/.local/share/battlecode-contest-browser/      owner-approved browser profile
~/.local/share/battlecode-contest-downloads/
  history-complete.json                       bounded paginated snapshot
  submissions/                               original own-team ZIPs + hashes
  groups/GROUP/                              metadata + original bundles
  mapped-SUBMISSION.json                      exact source mapping and totals
  imports/                                   durable API/mailbox receipts
  collection-stop.json                       access/rate stop; review required
```

Local commands (no contest mutations):

```bash
# Prepare/reconcile the exact already-imported source mapping; reruns reuse IDs.
python3 ops/import-contest-evidence.py \
  --manifest artifacts/submissions/beta-02ab89d1-manifest.json \
  --submission-id 185d5f06-459c-440d-a386-3ccd51f55b2f --apply

# Only AFTER reviewing the saved rate/access stop and the platform allowance:
python3 ops/contest-collect.py --resume-after-review --max-new-bundles 10
```

The second command is deliberately not scheduled or run automatically after a
429. It uses only previously observed own-team read/download interfaces, caches
finished archives, and stops on 401/403/429. Pending download jobs and named
remote import intents remain available for reconciliation. A changed attachment
for an already-imported official ID requires explicit evidence reconciliation,
not overwriting that immutable record.
