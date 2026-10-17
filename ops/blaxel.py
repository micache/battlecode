#!/usr/bin/env python3
"""Small operator client. Credentials stay on the operator machine, never in a VM.

The client intentionally has no resource deletion or billing-enablement command.
Creation is name-based, checked first, and never retried after an ambiguous POST.
"""
import argparse
import getpass
import json
import os
from pathlib import Path
import re
import stat
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.blaxel.ai/v0"
CREDENTIALS = Path.home() / ".config/battlecode/blaxel.json"
NAME = "battlecode-arena"
VOLUME = "battlecode-arena-data"
REGION = "us-pdx-1"


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # The default urllib redirect handler can forward Authorization.
        raise RuntimeError("Blaxel endpoint redirected; refusing to forward credentials")


class APIError(RuntimeError):
    def __init__(self, code, message):
        self.code = code
        super().__init__(f"Blaxel HTTP {code}: {message}")


def contains_spec(actual, expected):
    """Server-populated defaults may be extra; requested values may never drift."""
    if isinstance(expected, dict):
        return isinstance(actual, dict) and all(contains_spec(actual.get(k, False if k == 'readOnly' else None), v)
                                                for k, v in expected.items())
    if isinstance(expected, list):
        return isinstance(actual, list) and len(actual) == len(expected) and all(
            contains_spec(a, e) for a, e in zip(actual, expected))
    return type(actual) is type(expected) and actual == expected


class Client:
    def __init__(self, key, workspace):
        self.key, self.workspace = key, workspace

    def request(self, method, path, body=None, base=API, raw=False):
        # Never forward an administrator credential to an arbitrary returned URL.
        host = urllib.parse.urlparse(base)
        if host.scheme != "https" or not (host.hostname == "api.blaxel.ai" or
                (host.hostname and host.hostname.endswith(".bl.run"))):
            raise RuntimeError("untrusted Blaxel endpoint")
        headers = {"Authorization": "Bearer " + self.key,
                   "X-Blaxel-Workspace": self.workspace, "Blaxel-Version": "2026-04-28",
                   "Content-Type": "application/octet-stream" if isinstance(body, bytes) else "application/json",
                   "Accept": "application/octet-stream" if raw else "application/json"}
        req = urllib.request.Request(base.rstrip("/") + path, headers=headers, method=method,
                                     data=body if isinstance(body, bytes) else json.dumps(body).encode() if body is not None else None)
        try:
            with urllib.request.build_opener(NoRedirect).open(req, timeout=70) as response:
                content = response.read(64 * 1024**2 + 1)
                if len(content) > 64 * 1024**2:
                    raise RuntimeError('operator response exceeds 64 MiB; use a bounded archive')
                return content if raw else json.loads(content) if content else {}
        except urllib.error.HTTPError as exc:
            message = exc.read().decode(errors="replace").replace(self.key, "[REDACTED]")
            raise APIError(exc.code, message[:2000]) from None
        except (OSError, ValueError) as exc:
            raise RuntimeError(f"{method} {path} outcome unknown; inspect before any retry: {type(exc).__name__}") from None

    def get(self, path):
        return self.request("GET", path)

    def ensure(self, collection, name, spec):
        try:
            existing = self.get(f"/{collection}/{name}")
        except APIError as exc:
            if exc.code != 404:
                raise
        else:
            if existing.get("metadata", {}).get("labels", {}).get("managed-by") != "battlecode-arena":
                raise RuntimeError(f"refusing to adopt unregistered existing {collection}/{name}")
            if not contains_spec(existing.get('spec', {}), spec):
                raise RuntimeError(f"existing {collection}/{name} differs from requested specification; inspect it")
            return existing
        return self.request("POST", f"/{collection}", {
            "metadata": {"name": name, "labels": {"managed-by": "battlecode-arena"}}, "spec": spec})

    def endpoint(self):
        box = self.get(f"/sandboxes/{NAME}")
        if box.get("status") != "DEPLOYED":
            raise RuntimeError(f"arena not deployed: {box.get('status')}")
        endpoint = box.get("metadata", {}).get("url")
        if not endpoint:
            raise RuntimeError("sandbox has no API endpoint")
        return endpoint


def summary(resource):
    return {key: resource[key] for key in ("metadata", "spec", "status", "state", "nodeGeneration", "expiresIn", "events")
            if key in resource and key != "spec"} | {
                "spec": {k: v for k, v in resource.get("spec", {}).items() if k != "runtime"},
                "runtime": {k: v for k, v in resource.get("spec", {}).get("runtime", {}).items() if k != "envs"}}


def plan_report(client):
    """Read advertised plan/tier limits, NOT inaccessible effective quota overrides."""
    workspace = client.get("/workspaces/" + urllib.parse.quote(client.workspace, safe=""))
    account_id = workspace.get("accountId")
    if not isinstance(account_id, str) or not re.fullmatch(r"[a-zA-Z0-9-]+", account_id):
        raise RuntimeError("workspace did not return a valid account ID")
    account = client.get(f"/accounts/{account_id}")
    subscription = account.get("spec", {}).get("subscription", {})
    plan, tier = subscription.get("plan"), subscription.get("tier")
    definitions = client.get(f"/accounts/{account_id}/plan").get("plans", {})
    tier_limits = definitions.get("tiers", {}).get(tier, {}).get("limits")
    plan_limits = definitions.get(plan, {}).get("limits")
    if not isinstance(tier_limits, dict) or not isinstance(plan_limits, dict):
        raise RuntimeError("missing plan/tier definitions; do not guess resource limits")
    selected = ("memory", "volume_max_size", "volume_total_max_size", "volumes", "sandboxes",
                "sandbox_enforced_ttl", "sandbox_ttl", "image_total_max_size")
    return {"workspace": client.workspace, "plan": plan, "tier": tier,
            "source": "GET /accounts/{accountId}/plan; active subscription from GET /accounts/{accountId}",
            "effective_quota_overrides_verified": False,
            "size_unit": "MiB (console label); API fields are integer MB",
            "tier_limits": {k: tier_limits.get(k) for k in selected},
            "plan_limits": {k: plan_limits.get(k) for k in selected},
            "warning": "Advertised limits only, not allocation proof. Service accounts cannot read account quotas. "
                       "TTL policy may differ between plan, tier and effective overrides; verify on the created sandbox."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["login", "status", "limits", "provision", "run", "process", "logs", "download"])
    parser.add_argument("argument", nargs="?")
    parser.add_argument("--workspace", default=os.environ.get("BL_WORKSPACE", "banabolabs"))
    parser.add_argument("--keep-alive", action="store_true")
    parser.add_argument("--name")
    parser.add_argument("--restart-on-failure", action="store_true")
    parser.add_argument("--output", help="new local file for an arena artifact download")
    args = parser.parse_args()
    if args.command == "login":
        key = getpass.getpass("Blaxel API key (stored locally, mode 0600): ")
        client = Client(key, args.workspace)
        client.get("/sandboxes")  # Verify first, never overwrite with an invalid key.
        CREDENTIALS.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        fd = os.open(CREDENTIALS, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_NOFOLLOW, 0o600)
        with os.fdopen(fd, "w") as handle:
            os.fchmod(handle.fileno(), 0o600)
            json.dump({"key": key, "workspace": args.workspace}, handle)
        print("Verified. Operator credential saved outside the repository; not installed on workers.")
        return 0
    key = os.environ.get("BL_API_KEY")
    if not key:
        info = CREDENTIALS.stat()
        if info.st_uid != os.geteuid() or stat.S_IMODE(info.st_mode) != 0o600 or CREDENTIALS.is_symlink():
            raise RuntimeError("operator credential file must be owned by this user, regular, mode 0600")
        credentials = json.loads(CREDENTIALS.read_text())
        key = credentials["key"]
        args.workspace = credentials["workspace"]
    client = Client(key, args.workspace)
    if args.command == "limits":
        result = plan_report(client)
    elif args.command == "status":
        result = {}
        for collection in ("sandboxes", "volumes"):
            rows = client.get(f"/{collection}?limit=200")
            result[collection] = [summary(r) for r in (rows["data"] if isinstance(rows, dict) else rows)
                                  if r["metadata"]["name"] in (NAME, VOLUME)]
    elif args.command == "provision":
        volume = client.ensure("volumes", VOLUME, {"region": REGION, "size": 8192})
        print(json.dumps({"volume": summary(volume)}, indent=2), flush=True)
        box = client.ensure("sandboxes", NAME, {
            "region": REGION, "runtime": {"image": "blaxel/docker-in-sandbox:latest", "memory": 8192,
                "extraArgs": {"iptables": "enabled"}, "terminationGracePeriodSeconds": 30,
                "envs": [{"name": "BL_SANDBOX_API_ISOLATION", "value": "true"},
                         {"name": "SANDBOX_DISABLE_PROCESS_LOGGING", "value": "true"}]},
            "volumes": [{"name": VOLUME, "mountPath": "/persist", "readOnly": False}]})
        result = {"sandbox": summary(box)}
    else:
        endpoint = client.endpoint()
        if args.command == 'download':
            remote = Path(args.argument or '')
            allowed = ('/srv/battlecode/matches/', '/srv/battlecode/acceptance/', '/srv/battlecode/public/', '/srv/battlecode/backups/')
            if not args.output or '..' in remote.parts or not str(remote).startswith(allowed):
                parser.error('download requires an explicit arena artifact path and --output; owner homes are excluded')
            content = client.request('GET', '/filesystem/' + urllib.parse.quote(str(remote), safe=''), base=endpoint, raw=True)
            target = Path(args.output)
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open('xb') as stream:
                stream.write(content)
                stream.flush()
                os.fsync(stream.fileno())
            import hashlib
            result = {'downloaded': str(target), 'bytes': len(content), 'sha256': hashlib.sha256(content).hexdigest()}
        elif args.command == "run":
            if not args.argument:
                parser.error("run requires a command string")
            body = {"command": args.argument, "waitForCompletion": not args.keep_alive,
                    "keepAlive": args.keep_alive, "timeout": 0 if args.keep_alive else 60}
            if args.restart_on_failure:
                body.update(restartOnFailure=True, maxRestarts=5)
            if args.name:
                if not re.fullmatch(r"[a-z0-9-]+", args.name):
                    parser.error("invalid process name")
                body["name"] = args.name
            result = client.request("POST", "/process", body, endpoint)
        else:
            if not args.argument or not re.fullmatch(r"[a-zA-Z0-9-]+", args.argument):
                parser.error("valid process name or ID required")
            path = f"/process/{args.argument}" + ("/logs" if args.command == "logs" else "")
            result = client.request("GET", path, base=endpoint)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (RuntimeError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
