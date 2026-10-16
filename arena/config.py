from pathlib import Path
import re

from .common import identity, read_json, require, slug


def load(path):
    config = read_json(path)
    require(config.get("protocol_version") == 1, "unsupported configuration")
    require(config["repository_url"] in ("https://github.com/micache/battlecode", "git@github.com:micache/battlecode.git"),
            "repository must match assignment; never embed a token in a URL")
    workers = config["workers"]
    require(set(workers) == {"alpha", "beta"}, "pilot requires exactly alpha and beta")
    require(len({w["linux_user"] for w in workers.values()}) == 2, "owner users must differ")
    for bot, worker in workers.items():
        slug(bot)
        slug(worker["linux_user"])
        require(worker["branch"] == f"bot/{bot}", "branch/identity conflict")
        require(Path(worker["clone"]).is_absolute(), "absolute clone required")
    require(len({w["clone"] for w in workers.values()}) == 2, "writable clones must differ")
    require(config["limits"]["matches"] == config["limits"]["builds"] ==
            config["limits"]["codex_jobs"] == 1, "pilot concurrency must be 1/1/1")
    require(config["official"] == {"upload": False, "activation": False, "challenges": False},
            "official mutations disabled for this pilot")
    require(config["billing"] == {"subscription_only": True, "api_fallback": False,
                                  "cross_account_failover": False}, "subscription isolation required")
    require(config["engine"]["version"] == "2.1.6", "review engine update before use")
    require(config["evaluation"]["minimum_gain"] >= 0.05 and
            config["evaluation"]["maximum_map_drop"] <= 0.25, "weakened promotion gate")
    require(len(config["evaluation"]["development_maps"]) == 6 and
            len(config["evaluation"]["holdout_maps"]) == 3, "full nine-map gate required")
    require(set(config["evaluation"]["screen_maps"]) <= set(config["evaluation"]["development_maps"]),
            "screen maps must be development maps")
    require(len(config["evaluation"]["screen_maps"]) == 3 and
            not set(config["evaluation"]["development_maps"]) & set(config["evaluation"]["holdout_maps"]),
            "three wiring maps and disjoint holdouts required")
    for key in ("root", "mirror", "maps", "engine_lock", "parser_contract", "infrastructure"):
        require(Path(config[key]).is_absolute(), f"absolute {key} required")
    require(re.fullmatch(r"[a-f0-9]{40}", config["infrastructure_commit"] or ""),
            "pin infrastructure commit before setup")
    config["config_hash"] = identity(config)
    return config
