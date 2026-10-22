"""Bounded on-server history: discard oldest raw files, keep learning records.

The sole arena writer owns this maintenance. Source commits, normalized results,
evaluation summaries and feedback are never removed. Raw removal is journaled
before deletion so a restart cannot mistake it for an unexplained missing game.
"""
import json
import gzip
import hashlib
from pathlib import Path
import re
import shutil
import time

from .common import atomic_json, file_hash, identity, read_json, require
from .engine import seal_artifacts, verify_artifacts
from .storage import remove_redundant


def size(directory):
    return sum(p.stat().st_size for p in Path(directory).rglob('*') if not p.is_symlink() and p.is_file())


def checked_root(arena, job_id):
    require(isinstance(job_id, str) and re.fullmatch('[a-f0-9]{64}', job_id), 'invalid match directory identity')
    base = arena.root / 'matches'
    target = base / job_id
    require(not target.is_symlink() and target.resolve().parent == base.resolve(), 'unsafe match history target')
    return target


def finish_compaction(arena, job):
    current = Path(job['artifact'])
    marker = read_json(current / 'history-prune.json')
    previous = marker['previous_directory']
    require(previous == Path(previous).name and previous != current.name, 'unsafe previous history path')
    root = checked_root(arena, job['id'])
    require(current.resolve().parent == root.resolve(), 'unsafe compact history path')
    old = root / previous
    if old.is_symlink():
        require(old.resolve() == current.resolve(), 'history alias changed')
        return
    verify_artifacts(current, job['id'], job['attempt_count'])
    if old.exists():
        require(file_hash(old / 'completion.json') == marker['previous_completion_sha256'], 'old history changed')
        remove_redundant(old)
    old.symlink_to(current.name, target_is_directory=True)


def compact_project(arena, job):
    """Remove redundant per-game build trees, retaining replay/stats/log bytes."""
    old = Path(job['artifact'])
    root = checked_root(arena, job['id'])
    require(old.resolve().parent == root.resolve(), 'unexpected match artifact path')
    if (old / 'history-prune.json').exists():
        finish_compaction(arena, job)
        return 0
    removed = [name for name in ('project', 'project.zip') if (old / name).exists()]
    if not removed:
        return 0
    result = verify_artifacts(old, job['id'], job['attempt_count'])
    removed_bytes = sum(size(old / n) if (old / n).is_dir() else (old / n).stat().st_size for n in removed)
    final = old.with_name(old.name + '-retained')
    stage = old.with_name('.history-' + old.name)
    original_hash = file_hash(old / 'completion.json')
    if not final.exists():
        if stage.exists():
            remove_redundant(stage)  # Old sealed copy above remains authoritative.
        shutil.copytree(old, stage, ignore=lambda src, names:
                        ['project', 'project.zip', 'completion.json'] if Path(src)==old else [])
        compressed = None
        stats = stage / 'artifacts/final.json'
        original_stats = old / 'artifacts/final.json'
        parser = Path(arena.config['parser_contract'])
        fixture = read_json(parser).get('fixture_path') if parser.exists() else None
        bootstrap = json.loads(job['spec']).get('verification_repetition')
        if (stats.is_file() and 128 * 1024 <= stats.stat().st_size <= 64 * 1024**2 and
                not bootstrap and (not fixture or Path(fixture).resolve() != original_stats.resolve())):
            original_size, digest = stats.stat().st_size, file_hash(stats)
            packed = stats.with_name('final.json.gz')
            with stats.open('rb') as source, packed.open('xb') as target:
                with gzip.GzipFile(fileobj=target, mode='wb', mtime=0) as stream:
                    shutil.copyfileobj(source, stream)
            with gzip.open(packed, 'rb') as stream:
                require(hashlib.sha256(stream.read(original_size + 1)).hexdigest() == digest,
                        'statistics compression changed evidence')
            compressed = {'uncompressed_sha256':digest, 'uncompressed_bytes':original_size,
                          'stored_file':'artifacts/final.json.gz', 'compression':'gzip'}
            stats.unlink()  # Only the verified staging copy; sealed original still exists.
            removed_bytes += original_size - packed.stat().st_size
        atomic_json(stage / 'history-prune.json', {
            'policy':'rolling-v1', 'previous_directory':old.name,
            'previous_completion_sha256':original_hash, 'previous_completion':read_json(old / 'completion.json'),
            'removed_names':removed, 'removed_bytes':removed_bytes, 'at':time.time(),
            'compressed_statistics':compressed,
            'recovery':'Redundant per-match worktree discarded, not offloaded. Source/SDK/build identities retained; '
                       'Replay/log bytes are unchanged. Large statistics may be losslessly gzipped with '
                       'their original content hash retained. Original worktree is not recoverable here.'})
        seal_artifacts(stage, job['id'], job['attempt_count'], result)
        stage.rename(final)
    verify_artifacts(final, job['id'], job['attempt_count'])
    require(read_json(final / 'history-prune.json')['previous_completion_sha256'] == original_hash,
            'interrupted history compaction differs')
    removed_bytes = read_json(final / 'history-prune.json')['removed_bytes']
    with arena.db.transaction():
        arena.db.execute('UPDATE match_jobs SET artifact=? WHERE id=?', (str(final),job['id']))
        arena.db.execute('UPDATE match_attempts SET artifact=? WHERE job_id=? AND number=?',
                         (str(final),job['id'],job['attempt_count']))
    finish_compaction(arena, dict(job, artifact=str(final)))
    return removed_bytes


def protected_jobs(arena):
    db = arena.db
    engine=arena.adapter().lock_hash
    protected, evaluations = set(), set()
    evaluations.update(r['id'] for r in db.all("SELECT id FROM evaluations WHERE state='EVALUATING' "
                                              "OR revision_id IN (SELECT accepted_revision FROM bots)"))
    for bot in arena.config['workers']:
        # Keep current feedback, best full-suite evidence, and a bounded set of
        # representative failures. Old scores/lessons stay in SQLite regardless.
        rows = db.all('SELECT id,suite,metrics FROM evaluations WHERE bot_id=? AND finished IS NOT NULL '
                      'ORDER BY created DESC', (bot,))
        rows=[r for r in rows if json.loads(r['suite'])['engine_lock_hash']==engine]
        if rows:
            evaluations.add(rows[0]['id'])
        full = next((r for r in rows if json.loads(r['suite'])['coverage'] in ('full-nine-map','full-map-pool')), None)
        if full:
            evaluations.add(full['id'])
        for row in rows[:8]:
            metrics = json.loads(row['metrics']) if row['metrics'] else {}
            protected.update(r['match_id'] for r in metrics.get('representative_failures', []))
        task = db.one('SELECT id,envelope FROM tasks WHERE bot_id=? ORDER BY created DESC LIMIT 1', (bot,))
        if task:
            envelope = json.loads(task['envelope'])
            # Keep recovery evidence through the handoff to the next task,
            # not just until that task is dispatched. Still bounded: at most
            # four checks from the current and immediate prior task per lane.
            for task_id in (task['id'], envelope.get('prior_task_id')):
                if not task_id or not db.one('SELECT id FROM tasks WHERE id=? AND bot_id=?', (task_id,bot)):
                    continue
                for check in db.all('SELECT value FROM meta WHERE key LIKE ? '
                                    "ORDER BY json_extract(value,'$.finished') DESC LIMIT 4",
                                    (f"check:{task_id}:%",)):
                    protected.update(json.loads(check['value']).get('matches', []))
            rid = envelope.get('development_selection', {}).get('revision_id')
            row = db.one('SELECT id FROM evaluations WHERE revision_id=? AND finished IS NOT NULL ORDER BY created DESC LIMIT 1', (rid,))
            if row:
                evaluations.add(row['id'])
    exports = sorted((arena.root/'public/exports').glob('*/manifest.json'),
                     key=lambda p:p.stat().st_mtime,reverse=True)
    for manifest in exports[:2]:
        value = read_json(manifest)
        if value.get('evaluation_id'):
            evaluations.add(value['evaluation_id'])
    for eid in evaluations:
        protected.update(r['job_id'] for r in db.all('SELECT job_id FROM evaluation_cases WHERE evaluation_id=?', (eid,)))
    for row in db.all('SELECT id,spec FROM match_jobs'):
        if json.loads(row['spec']).get('verification_repetition'):
            protected.add(row['id'])
    paths = []
    contract = Path(arena.config['parser_contract'])
    if contract.is_file():
        paths.append(read_json(contract).get('fixture_path'))
    paths.append(arena.adapter().lock.get('profile_evidence', {}).get('path'))
    readiness = db.get('readiness', {})
    paths.extend(v.get('path') for v in readiness.get('checks', {}).values() if isinstance(v,dict))
    for path in paths:
        if path:
            try:
                relative = Path(path).absolute().relative_to((arena.root / 'matches').absolute())
            except ValueError:
                continue
            if relative.parts and re.fullmatch('[a-f0-9]{64}', relative.parts[0]):
                protected.add(relative.parts[0])
    return protected


def finish_retirement(arena, record):
    directory = checked_root(arena, record['job_id'])
    if directory.exists():
        remove_redundant(directory)
    arena.db.execute("UPDATE artifact_retirements SET state='DELETED' WHERE job_id=?", (record['job_id'],))


def prune_build_cache(arena):
    """LRU of rebuildable compiler caches; queued/frozen inputs are pinned."""
    root = arena.root/'builds'
    root.mkdir(exist_ok=True)
    for stage in root.glob('.retired-*'):
        if re.fullmatch(r'\.retired-[a-f0-9]{64}',stage.name) and stage.is_dir() and not stage.is_symlink():
            remove_redundant(stage)
    pinned = set()
    # Future stages use the suite's frozen inputs, not only today's queued
    # games. In particular development-base builds may not have a case yet.
    for row in arena.db.all("SELECT suite FROM evaluations WHERE state='EVALUATING'"):
        suite = json.loads(row['suite'])
        pinned.update(suite.get(k) for k in ('candidate_build','incumbent_build','development_build'))
        pinned.update(item.get('build_id') for item in suite.get('opponents', {}).values())
    rows = arena.db.all("SELECT spec FROM match_jobs WHERE state IN ('QUEUED','RUNNING') OR id IN "
                        "(SELECT c.job_id FROM evaluation_cases c JOIN evaluations e ON e.id=c.evaluation_id "
                        "WHERE e.state='EVALUATING')")
    for row in rows:
        spec = json.loads(row['spec'])
        pinned.update(spec.get(k) for k in ('a_build','b_build'))
    candidates = [p for p in root.iterdir() if re.fullmatch('[a-f0-9]{64}',p.name) and
                  not p.is_symlink() and p.is_dir() and (p/'build.json').is_file()]
    candidates.sort(key=lambda p:((p/'build.json').stat().st_mtime,p.name),reverse=True)
    pinned.update(p.name for p in candidates[:12])
    removed, reclaimed = [], 0
    for directory in reversed(candidates):
        if directory.name in pinned:
            continue
        require(read_json(directory/'build.json')['build_id']==directory.name, 'unexpected build cache identity')
        reclaimed += size(directory)
        stage = root/('.retired-'+directory.name)
        directory.rename(stage)  # Invalidated atomically; a crash cannot reuse half a cache.
        remove_redundant(stage)
        removed.append(directory.name)
    return removed,reclaimed


def retire(arena, job):
    root = checked_root(arena, job['id'])
    require(job['state']=='COMPLETED' and job['artifact'], 'only completed stored history can retire')
    require(Path(job['artifact']).resolve().parent == root.resolve(), 'artifact outside match root')
    verify_artifacts(job['artifact'], job['id'], job['attempt_count'])
    record = {'job_id':job['id'], 'artifact':job['artifact'], 'bytes':size(root), 'at':time.time(),
              'completion_sha256':file_hash(Path(job['artifact']) / 'completion.json'),
              'normalized_result_sha256':identity(json.loads(job['result'])),
              'reason':'Oldest routine raw history removed under bounded rolling retention; '
                       'source commits, normalized result and evaluation/feedback records retained.',
              'recoverable':False}
    with arena.db.transaction():
        arena.db.execute("INSERT INTO artifact_retirements VALUES(?,?,'DELETING')", (job['id'],json.dumps(record)))
        arena.db.execute('UPDATE match_jobs SET artifact=NULL WHERE id=?', (job['id'],))
    finish_retirement(arena, record)
    return record


def maintain_external(arena):
    """Old outside attachments roll away; source/match IDs and compact outcomes stay in SQLite."""
    policy = arena.config.get('official_exploration', {})
    if not policy.get('enabled'):
        return
    rows = arena.db.all('SELECT * FROM external_matches ORDER BY created DESC,official_id DESC')
    base = arena.root / 'external'
    total = size(base) if base.exists() else 0
    budget = policy.get('feedback_budget_bytes', 128 * 1024**2)
    for index, row in reversed(list(enumerate(rows))):
        metadata = json.loads(row['metadata'])
        pending = metadata.get('raw_retired', {}).get('state') == 'DELETING'
        if not pending and (index < 500 or total <= budget or metadata.get('raw_retired')):
            continue
        directory = Path(row['artifact'])
        require(not directory.is_symlink() and directory == base / identity(row['official_id']),
                'unsafe outside-history retirement path')
        if not pending:
            require(all((directory / name).is_file() and file_hash(directory / name) == digest
                        for name,digest in metadata['file_sha256'].items()), 'outside history changed')
            metadata['raw_retired'] = {'state':'DELETING', 'at':time.time(), 'bytes':size(directory),
                'reason':'Oldest outside attachments retired; newest 500, match/source mapping and outcomes retained.',
                'recoverable':False}
            arena.db.execute('UPDATE external_matches SET metadata=? WHERE official_id=?',
                             (json.dumps(metadata), row['official_id']))
        if directory.exists():
            remove_redundant(directory)
        total -= metadata['raw_retired']['bytes']
        metadata['raw_retired']['state'] = 'DELETED'
        arena.db.execute('UPDATE external_matches SET metadata=? WHERE official_id=?',
                         (json.dumps(metadata), row['official_id']))


def prune_publications(arena, keep=3):
    """Completed push checkouts are reproducible; intents and Git history stay."""
    from .gitstore import git
    retired, reclaimed = [], 0
    for bot in arena.config['workers']:
        rows=arena.db.all("SELECT id,published_commit FROM tasks WHERE bot_id=? AND state='PUBLISHED' "
                          "AND published_commit IS NOT NULL ORDER BY created DESC",(bot,))
        for row in rows[keep:]:
            directory=arena.root/'publication'/row['id']
            if not directory.is_dir() or directory.is_symlink():continue
            marker=directory/'retired-checkout.json'
            if not marker.exists():
                if not (directory/'.git').is_dir():continue
                intent=read_json(directory/'publication-intent.json')
                require(intent['task_id']==row['id'] and intent['commit']==row['published_commit'],
                        'published checkpoint identity differs')
                git(arena.config['mirror'],'cat-file','-e',row['published_commit']+'^{commit}')
                require(git(directory,'rev-parse','HEAD')==row['published_commit'],'published checkout changed')
                if git(directory,'status','--porcelain','--untracked-files=all') != '?? publication-intent.json':
                    continue  # Never discard unknown edits or a partial transaction.
                atomic_json(marker,{'task_id':row['id'],'commit':row['published_commit'],
                    'at':time.time(),'bytes':size(directory),'state':'DELETING',
                    'recovery':'Recreate checkout from preserved mirror/GitHub commit; push intent retained.'})
            record=read_json(marker)
            if record['state']=='DELETED':continue
            for child in directory.iterdir():
                if child.name in ('publication-intent.json','retired-checkout.json'):continue
                require(not child.is_symlink(),'unexpected published checkpoint symlink')
                if child.is_dir():remove_redundant(child)
                else:child.unlink()
            record['state']='DELETED';atomic_json(marker,record)
            retired.append(row['id']);reclaimed+=record['bytes']
    return retired,reclaimed


def maintain(arena, compaction_limit=8, deletion_limit=128):
    if not arena.config['limits'].get('rolling_history', False):
        return {'enabled':False}
    maintain_external(arena)
    for row in arena.db.all("SELECT record FROM artifact_retirements WHERE state='DELETING'"):
        finish_retirement(arena, json.loads(row['record']))
    publications,reclaimed = prune_publications(arena)
    removed_builds,build_bytes = prune_build_cache(arena)
    reclaimed += build_bytes
    compacted = []
    for job in arena.db.all("SELECT * FROM match_jobs WHERE state='COMPLETED' AND artifact IS NOT NULL ORDER BY created DESC,id DESC"):
        path = Path(job['artifact'])
        if (path / 'history-prune.json').exists():
            finish_compaction(arena, job)
        elif (path / 'project').exists() or (path / 'project.zip').exists():
            if len(compacted) < compaction_limit:
                reclaimed += compact_project(arena, job)
                compacted.append(job['id'])
    reserve = arena.config['limits']['minimum_free_bytes']
    budget = arena.config['limits']['artifact_budget_bytes']
    total, free = size(arena.root / 'matches'), shutil.disk_usage(arena.root).free
    deleting = free < reserve + 256*1024**2 or total >= budget
    records = []
    if deleting:
        protected = protected_jobs(arena)
        recent = arena.db.all("SELECT id FROM match_jobs WHERE state='COMPLETED' AND artifact IS NOT NULL "
                              'ORDER BY created DESC,id DESC LIMIT 120')
        protected.update(r['id'] for r in recent)
        for job in arena.db.all("SELECT * FROM match_jobs WHERE state='COMPLETED' AND artifact IS NOT NULL ORDER BY created,id"):
            if job['id'] in protected:
                continue
            record = retire(arena, job)
            records.append(record)
            reclaimed += record['bytes']
            total -= record['bytes']
            free = shutil.disk_usage(arena.root).free
            if (free >= reserve + 768*1024**2 and total < budget * .75) or len(records) >= deletion_limit:
                break
    report = {'enabled':True,'at':time.time(),'compacted_projects':compacted,
              'retired_build_caches':removed_builds,
              'retired_publication_checkouts':publications,
              'retired_matches':[r['job_id'] for r in records], 'reclaimed_bytes':reclaimed,
              'total_reclaimed_bytes':arena.db.get('rolling_history',{}).get('total_reclaimed_bytes',0)+reclaimed,
              'free_bytes':shutil.disk_usage(arena.root).free,'artifact_bytes':total,
              'total_retired_matches':arena.db.one("SELECT count(*) AS n FROM artifact_retirements WHERE state='DELETED'")['n'],
              'policy':'oldest routine raw matches first; newest 120, active/accepted/latest evaluations, '
                       'bounded failures and parser/bootstrap evidence protected; no offloading',
              'raw_retirement_is_permanent':True}
    arena.db.put('rolling_history', report)
    return report
