import collections
import json
from pathlib import Path
import time

from .common import atomic_bytes, atomic_json, identity, read_json, require


def summarize(cases, gate, holdouts, full=False):
    """One observation per ordered logical game; case means weight maps/opponents equally."""
    grouped = collections.defaultdict(list)
    missing, faults, unknown_reliability, failures = [], [], [], []
    wins = losses = 0
    for case in cases:
        result = case.get("result")
        if not result or result["state"] != "COMPLETED" or not result["completed"]:
            missing.append(case["job_id"])
            if result and result["state"] == "BOT_FAULT":
                faults.append(case["job_id"])
            continue
        if result.get("bot_faults") is None:
            unknown_reliability.append(case["job_id"])
        elif result["bot_faults"]:
            faults.append(case["job_id"])
        won = result["winner"] == case["candidate_side"]
        if case["role"] == "candidate":
            wins += int(won)
            losses += int(not won)
            if not won and case["map_name"] not in holdouts:
                failures.append({"match_id": case["job_id"], "side": case["candidate_side"],
                                 "map": case["map_name"], "artifact": case.get("artifact"),
                                 "round": None, "trace": None})
        grouped[(case["role"], case["map_name"], case["opponent"])].append(
            (case["candidate_side"], int(won)))
    means = {}
    for key, values in grouped.items():
        if {v[0] for v in values} == {"A", "B"} and len(values) == 2:
            means[key] = sum(v[1] for v in values) / 2
    paired = [(key, score, means[("incumbent", key[1], key[2])])
              for key, score in means.items() if key[0] == "candidate"
              and ("incumbent", key[1], key[2]) in means]
    delta = sum(a - b for _, a, b in paired) / len(paired) if paired else None
    maps = {}
    for name in sorted({key[1] for key, _, _ in paired}):
        rows = [(a, b) for key, a, b in paired if key[1] == name]
        maps[name] = {"candidate": sum(a for a, _ in rows) / len(rows),
                      "incumbent": sum(b for _, b in rows) / len(rows), "pairs": len(rows)}
    holdout_rows = [(a, b) for key, a, b in paired if key[1] in holdouts]
    per_opponent = {}
    for opponent in sorted({key[2] for key, _, _ in paired}):
        rows = [(a, b) for key, a, b in paired if key[2] == opponent]
        per_opponent[opponent] = {"candidate": sum(a for a, _ in rows) / len(rows),
                                  "incumbent": sum(b for _, b in rows) / len(rows), "pairs": len(rows)}
    holdout_delta = sum(a - b for a, b in holdout_rows) / len(holdout_rows) if holdout_rows else None
    decision = "INCONCLUSIVE"
    if faults:
        decision = "REJECTED"
    elif full and not missing and not unknown_reliability and paired:
        if (delta + 1e-12 >= gate["minimum_gain"] and
                all(v["candidate"] - v["incumbent"] >= -gate["maximum_map_drop"] - 1e-12 for v in maps.values())
                and holdout_delta is not None and holdout_delta >= -1e-12):
            decision = "ACCEPTED"
        else:
            decision = "REJECTED"
    return {"decision": decision, "wins": wins, "losses": losses,
            "common_opponent_delta": delta, "per_map": maps, "holdout_delta": holdout_delta,
            "missing": sorted(set(missing)), "fault_matches": sorted(set(faults)),
            "unknown_reliability": sorted(set(unknown_reliability)),
            "representative_failures": failures[:3], "case_count": len(cases),
            "paired_cases": len(paired), "per_opponent": per_opponent,
            "metrics_not_available": ["bag_loss", "capture_completion",
                                                                    "channel_interruptions", "per_turn_damage"]}


def export_feedback(db, config, evaluation):
    metrics = json.loads(evaluation["metrics"])
    suite = json.loads(evaluation["suite"])
    revision = db.one("SELECT * FROM revisions WHERE id=?", (evaluation["revision_id"],))
    incumbent = db.one("SELECT * FROM revisions WHERE id=?", (evaluation["incumbent_id"],))
    holdouts = set(config["evaluation"]["holdout_maps"])
    metrics["per_map"] = {key: value for key, value in metrics["per_map"].items() if key not in holdouts}
    # Holdout match IDs cannot be used as a back door to per-map reserved feedback.
    reserved_jobs = {row["job_id"] for row in db.all("SELECT job_id,map_name FROM evaluation_cases WHERE evaluation_id=?",
                                                   (evaluation["id"],)) if row["map_name"] in holdouts}
    for field in ("missing", "fault_matches", "unknown_reliability"):
        metrics[f"holdout_{field}_count"] = len(set(metrics[field]) & reserved_jobs)
        metrics[field] = [job for job in metrics[field] if job not in reserved_jobs]
    summary = {"protocol_version": 1, "evaluation_id": evaluation["id"], "bot_id": evaluation["bot_id"],
               "candidate": {"revision_id": revision["id"], "commit": revision["commit_sha"],
                             "source_hash": revision["source_hash"], "build_id": suite.get("candidate_build")},
               "incumbent": ({"revision_id": incumbent["id"], "commit": incumbent["commit_sha"],
                              "source_hash": incumbent["source_hash"], "build_id": suite.get("incumbent_build")} if incumbent else None),
               "suite_hash": evaluation["suite_hash"], "engine_lock_hash": suite["engine_lock_hash"],
               "settings_hash": identity(suite.get("effective_profile")), "map_pool_hash": identity(suite["maps"]),
               "opponents": suite["opponents"], "coverage": suite["coverage"],
               "decision": evaluation["state"], "metrics": metrics, "created": evaluation["finished"] or evaluation["created"],
               "next_action": "One bounded hypothesis from development feedback; holdout detail reserved."}
    directory = Path(config["root"]) / "evaluations" / evaluation["id"]
    directory.mkdir(parents=True, exist_ok=True)
    atomic_json(directory / "summary.json", summary)
    markdown = (f"Evaluation {evaluation['id']} — {evaluation['state']}\n\n"
                f"Candidate `{revision['commit_sha']}` / source `{revision['source_hash']}`.\n\n"
                f"Wins/losses: {metrics['wins']}/{metrics['losses']}; common-opponent delta: "
                f"{metrics['common_opponent_delta']}; missing: {len(metrics['missing'])}.\n\n"
                f"Coverage: {suite['coverage']}. Holdout delta: {metrics['holdout_delta']}.\n\n"
                "See summary.json for immutable opponents, failures and availability flags.\n")
    atomic_bytes(directory / "summary.md", markdown.encode())
    feedback = Path(config["root"]) / "feedback" / evaluation["bot_id"]
    feedback.mkdir(parents=True, exist_ok=True)
    # Per-evaluation files first, latest pointer last. A crash can always re-export safely.
    atomic_json(feedback / f"{evaluation['id']}.json", summary)
    atomic_bytes(feedback / f"{evaluation['id']}.md", markdown.encode())
    atomic_json(feedback / "latest.json", {"evaluation_id": evaluation["id"], "summary": summary})
    return summary
