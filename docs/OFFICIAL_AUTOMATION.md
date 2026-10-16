# Official publishing and exploration

The owner authorized automatic official submissions and unranked exploration on
16 October 2026. This supersedes the original user restriction, not the project's
policy-review and platform-interface verification gates.

The native pinned `cambc 2.1.6 login` completed successfully on the server at
2026-10-16 14:24:27 UTC. It reports a seven-day session. Its credential directory
is `/var/lib/battlecode-volume/official-auth`, mode 0700, owned by `bc-arena`.
Neither worker nor bot/build containers receive that directory. Authentication
uses the native browser approval flow; no token extraction or password sharing.

The owner subsequently supplied the current handbook's Getting Started guide.
It confirms browser-approved seven-day CLI login, `cambc submit BOT` uploading
source to the current team, equivalent source selection for bundle and submit,
and following compilation/matches/replays through the platform. It does not
describe active-submission changes, challenge automation/quotas or AI policy.
This is owner-supplied documentation, not an independently retrieved export of
the missing organizer AGENTS.md or platform policy.

## Running private training

`arena/strategy.py` selects the pinned starter plus one strong, fault-free,
distinct historical source per registered lane. This is a training heuristic,
not a comparison of local ratings across incompatible suites. Every evaluation
freezes its selected commits, sources, builds and maps before starting. Adding
another registered lane extends the panel without another supervisor.

Every fifth published experiment requests one different strategic hypothesis;
retries do not advance the cycle. Normal experiments address a reproducible
failure. Imported external match IDs, own immutable submission mappings, sides,
absolute outcomes and known/unknown opponent versions enter a bounded task
context. An import wakes only its own lane once; it never becomes a controlled
local match. Raw external annotations are not copied into instructions. Replay
analysis remains limited by available telemetry; no omniscient runtime inputs.

Full nine-map evaluations are enabled separately from automatic promotion, at
most twice per lane per rolling day. Other candidates receive development
screens instead of stalling the scheduler. All existing reliability, matched
incumbent, head-to-head, +5 percentage-point, per-map, holdout and readiness gates
remain intact. Automatic promotion is still disabled pending readiness review.

## Proposed automatic official policy: implemented as a non-mutating monitor

`arena/official.py`, exposed in `public/status.json` as `official_selection`,
requires every current lane champion to have a full accepted improvement with
three distinct fixed opponents, current infrastructure/engine identity and no
missing games, faults or unknown reliability. Champions must have the same
frozen panel before comparing their scores. The leader must exceed the next
lane by five percentage points and stay unchanged for six hours. Waiting is
stability evidence, not new independent game evidence. Any loss of eligibility
resets that timer. Uploads would be limited to one per 24 hours.

**No upload/challenge adapter is enabled or claimed implemented.** The monitor
always includes a platform-verification blocker. The pinned CLI documents
`submit BOT` and `bundle BOT --output FILE.zip`, but has no challenge command.
The official web app script returned HTTP 403; no access check was bypassed.
Uploading could affect the active ranked submission, and that effect is not
verified. Current event AI/sharing/automation rules, organizer AGENTS.md,
supported challenge requests, quotas, submission selection, polling and replay
access must be reviewed before wiring actual remote mutations.

Once a supported interface is supplied, the implementation must add a single
publisher lease, durable request intents, immutable bundle/submission mapping,
one outstanding challenge, documented rate limits and Retry-After handling.
Unknown remote creation outcomes stop and reconcile with official history;
never blindly retry. Access/auth failures stop only that adapter. No account
rotation, API billing, private opponent-code access or automatic credential
renewal is permitted. Start with one exploratory challenge, then choose a
conservative cadence within verified platform limits; no guessed quota.

## Continuous operations

The existing managed supervisor runs independently of this chat/API connection,
restarts crashed units with bounded backoff, and now restarts a scheduler with
no fresh heartbeat for 30 minutes after its startup grace. It kills descendants
before replacement. Attempts, quotas and accepted revisions persist. Disk
pressure pauses work; permissions/authentication/ambiguous writes need operator
resolution. This is continuous process supervision, not a promise that a chat
agent remains online or can autonomously repair arbitrary future bugs.

All code upgrades use stop → checkpoint → install → restart. Never replace
code or engine locks while a run is active. Physical VM reboot persistence and
full off-host replay backup remain unverified.
