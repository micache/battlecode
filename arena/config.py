from pathlib import Path
import re

from .common import identity, read_json, require, slug


def load(path):
    config = read_json(path)
    require(config.get("protocol_version") == 1, "unsupported configuration")
    require(config["repository_url"] in ("https://github.com/micache/battlecode", "git@github.com:micache/battlecode.git"),
            "repository must match assignment; never embed a token in a URL")
    workers = config["workers"]
    require({"alpha", "beta"} <= set(workers), "alpha and beta must remain registered")
    require(len({w["linux_user"] for w in workers.values()}) == len(workers), "owner users must differ")
    for bot, worker in workers.items():
        slug(bot)
        slug(worker["linux_user"])
        require(worker["branch"] == f"bot/{bot}", "branch/identity conflict")
        require(Path(worker["clone"]).is_absolute(), "absolute clone required")
        require(worker.get('provider', 'codex') == 'codex', 'only native Codex workers are configured')
    require(len({w["clone"] for w in workers.values()}) == len(workers), "writable clones must differ")
    require(config["limits"]["matches"] == config["limits"]["builds"] ==
            config["limits"]["codex_jobs"] == 1, "pilot concurrency must be 1/1/1")
    interval = config['limits'].get('improvement_interval_seconds', 3600)
    require(type(interval) is int and interval >= 0, 'nonnegative improvement interval required')
    require(type(config['limits'].get('continuous_matches', False)) is bool, 'continuous_matches must be boolean')
    require(type(config['limits'].get('rolling_history', False)) is bool, 'rolling_history must be boolean')
    policy = config.get('official_schedule', {})
    require(type(policy.get('check_interval_seconds', 18000)) is int and
            policy.get('check_interval_seconds', 18000) >= 18000 and
            type(policy.get('unchanged_recheck_seconds', 10800)) is int and
            policy.get('unchanged_recheck_seconds', 10800) >= 10800, 'invalid official check cadence')
    require(config['official'].get('upload') is False and config['official'].get('activation') is False and
            type(config['official'].get('challenges')) is bool, 'uploads and activation remain disabled')
    if config['official']['challenges']:
        outside = config.get('official_exploration', {})
        require(config['engine']['version'] == '2.2.5' and outside.get('enabled') is True and
                outside.get('owner_authorized') is True and outside.get('interface') == 'cambc-225-match-groups' and
                outside.get('bot_id') in workers and
                re.fullmatch('[a-f0-9]{40}', outside.get('source_commit', '')) and
                re.fullmatch('[a-f0-9]{64}', outside.get('source_hash', '')) and
                outside.get('interval_seconds', 0) >= 72,
                'owner-approved pinned-source native CLI outside-play configuration required')
    require(config["billing"] == {"subscription_only": True, "api_fallback": False,
                                  "cross_account_failover": False}, "subscription isolation required")
    require(config["engine"]["version"] in ("2.1.6", "2.2.5"), "review engine update before use")
    require(config["evaluation"]["minimum_gain"] >= 0.05 and
            config["evaluation"]["maximum_map_drop"] <= 0.25, "weakened promotion gate")
    development, holdouts = (config['evaluation'][k] for k in ('development_maps', 'holdout_maps'))
    require(len(development) >= 6 and len(holdouts) >= 3 and
            len(development + holdouts) == len(set(development + holdouts)),
            "complete published map pool and at least three reserved holdouts required")
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
