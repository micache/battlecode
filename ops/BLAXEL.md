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

An account administrator must enable a persistent volume of at least 102400 MB.
Also check the quota for an 8192 MB sandbox and the maximum/default sandbox TTL;
those creation checks have not run. Promotional credits do not automatically
raise quota tiers. See [Blaxel quotas](https://docs.blaxel.ai/Security/Quotas).

## Operator client

Run from a trusted operator computer, **not inside an owner worker**:

```bash
python3 ops/blaxel.py login --workspace banabolabs
python3 ops/blaxel.py status
# Only after the quota blocker is resolved:
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
