# Blaxel deployment status

Deployment is **not complete**. The authorized first creation request was rejected
with HTTP 403: `Volume size 102400MB exceeds maximum allowed size`.
Read-only reconciliation confirmed no `battlecode-arena` sandbox and no
`battlecode-arena-data` volume exist. The pre-existing `cpu-box` is untouched.
No failed request was retried or silently replaced with ephemeral storage.

Planned resources: one 8192 MB sandbox (four CPU cores), one 102400 MB persistent
volume, region `us-pdx-1`. Initial lanes are alpha and beta, with match/build/Codex
concurrency 1/1/1. No public application ports, model gateway, billing fallback,
or official competition mutations. Infrastructure credits do not replace the
owners' Codex subscription quotas.

## Limits discovered without contacting an administrator

The active subscription endpoint reports `plan=free`, `tier=tier_2`. The account's
plan-definition endpoint returns these Tier 2 limits:

| Resource | Advertised limit |
| --- | --- |
| RAM per sandbox | 32768 MB (32 GiB using the console's units) |
| Persistent volume size | 8192 MB (8 GiB) per volume |
| Total volume storage | 204800 MB (200 GiB) |
| Volume count | 400 |
| Sandbox count | 200 |

This is plan-definition evidence, **not verified effective account overrides or
proof of a successful allocation**. The effective-quota endpoint explicitly
rejects service accounts (`you can't retrieve account quotas from a service
account`). That permission denial was not retried or bypassed. The supported
account/plan reads succeeded. The existing `cpu-box` has 32768 MB memory; it was
inspected read-only and left unchanged.

TTL is unresolved: the tier definition sets `sandbox_enforced_ttl=0`, while the
free-plan definition sets it to 1; both list `sandbox_ttl=30`. The existing box
has no reported expiration. Verify the newly created arena's effective expiration
instead of claiming an unconditional no-expiry guarantee from these definitions.

The earlier 100 GB volume choice is not a hard arena requirement. An 8 GB volume
may support this pilot with the immutable toolchain in the runtime image and
bounded persistent build/artifact retention. This requires a deployment-specific
disk budget and measured headroom; the current 10 GB artifact budget is too large
for an 8 GB volume and must not be carried over unchanged. Blaxel currently allows
only one persistent volume per sandbox, so the account's 200 GB aggregate allowance
cannot simply be combined as multiple mounts on one host. No additional resources
were created during this read-only investigation.

An administrator is needed only if verified practical requirements exceed the
existing limits or the effective lifetime policy prevents stable recovery.
Promotional credits do not automatically raise tiers. See
[Blaxel quotas](https://docs.blaxel.ai/Security/Quotas) and
[volume attachment constraints](https://docs.blaxel.ai/Sandboxes/Volumes).

## Operator client

Run from a trusted operator computer, **not inside an owner worker**:

```bash
python3 ops/blaxel.py login --workspace banabolabs
python3 ops/blaxel.py limits
python3 ops/blaxel.py status
# WARNING: current provision still requests the original 100 GB disk.
# Adapt its size AND arena retention budget before using the 8 GB plan limit.
# Otherwise, only run after a quota increase:
python3 ops/blaxel.py provision
```

`login` reads the key without echoing and stores it outside the repository in
`~/.config/battlecode/blaxel.json`, owned by the operator, mode 0600. Alternatively
use `BL_API_KEY` and `BL_WORKSPACE` from an existing secret manager. Never put the
key in a shell command, repository, Docker image, or worker environment. The key
shared in chat should be rotated by its owner; rerun `login` with the replacement.

`provision` is resource creation only, **not a completed arena installer**. The
remaining work includes the persistent multi-user installation, protected local
sandbox API, verified hard container limits, pinned runtime image, startup and
restart supervision, engine/parser acceptance, account logins, publication key,
and real improvement cycles. Standard VM systemd units remain in `ops/systemd`;
Blaxel's sandbox API is PID 1, so installing those units alone is insufficient.

The client checks exact resource names before creation, refuses to adopt foreign
resources, refuses credential-bearing redirects/untrusted endpoints, and does not
retry ambiguous writes. It contains no deletion, quota-change, or billing command.
After an interrupted creation, inspect `status` before deciding whether to retry.
