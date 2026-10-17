"""Two-phase offload of redundant match worktrees; live evidence stays online.

The operator downloads and verifies a batch before acknowledging it. Only then
does the sole arena writer replace each attempt with a newly sealed compact
copy. Its original seal and the local archive address remain in the new seal.
No missing bytes are silently accepted by verify_artifacts.
"""
import io
import json
from pathlib import Path
import re
import shutil
import tarfile
import time

from .common import atomic_json, canonical, file_hash, identity, read_json, require
from .engine import seal_artifacts, verify_artifacts
from .storage import remove_redundant


MAX_BATCH_BYTES = 48 * 1024**2


def checked_id(value):
    require(isinstance(value, str) and re.fullmatch('[a-f0-9]{64}', value), 'invalid archive ID')
    return value


def base_path(arena):
    directory = arena.root / 'public/offload'
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def prepare(arena, keep_recent=20):
    """At most one durable pending batch; preparing never deletes source bytes."""
    pending = arena.db.get('offload_pending')
    if pending:
        require(file_hash(pending['archive_path']) == pending['archive_sha256'], 'pending batch changed')
        return pending
    root = base_path(arena)
    # A crash after the receipt transaction can leave only this redundant tar.
    for row in arena.db.all("SELECT value FROM meta WHERE key LIKE 'offload_receipt:%'"):
        batch = json.loads(row['value'])['batch_id']
        for suffix in ('.tar', '.tar.xz'):
            (root / (checked_id(batch) + suffix)).unlink(missing_ok=True)
    jobs = arena.db.all("SELECT * FROM match_jobs WHERE state='COMPLETED' AND artifact IS NOT NULL "
                        'ORDER BY created DESC,id DESC')
    entries, total = [], 0
    for job in reversed(jobs[keep_recent:] if keep_recent else jobs):
        directory = Path(job['artifact'])
        if (directory / 'project-offload.json').exists() or not (directory / 'project.zip').is_file():
            continue
        require(directory.resolve().parent == (arena.root / 'matches' / job['id']).resolve(), 'unsafe artifact directory')
        require(not (directory / 'project.zip').is_symlink(), 'unsafe project archive')
        size = sum((directory / n).stat().st_size for n in ('project.zip', 'project-archive.json', 'completion.json'))
        if size > MAX_BATCH_BYTES - 1024**2:
            continue
        if total + size > MAX_BATCH_BYTES - 1024**2 or len(entries) == 16:
            break
        verify_artifacts(directory, job['id'], job['attempt_count'])
        entry = {'job_id':job['id'], 'attempt':job['attempt_count'], 'directory':directory.name,
                 'files':{name: {'sha256':file_hash(directory / name), 'size':(directory / name).stat().st_size}
                          for name in ('project.zip', 'project-archive.json', 'completion.json')}}
        entries.append(entry)
        total += size
    if not entries:
        return {'batch_id':None, 'entries':[], 'retained_recent_matches':keep_recent}
    batch = identity(entries)
    target = root / (batch + '.tar.xz')
    manifest = {'protocol_version':1, 'batch_id':batch, 'entries':entries}
    if not target.exists():
        stage = target.with_suffix('.pending')
        stage.unlink(missing_ok=True)  # Sole-writer, regenerable interrupted batch; originals still exist.
        # ZIP members repeat SDK/cache bytes across games. A multi-MiB XZ
        # dictionary deduplicates these across the batch, unlike ZIP's window.
        with tarfile.open(stage, 'x:xz', preset=6) as archive:
            data = canonical(manifest)
            info = tarfile.TarInfo('manifest.json')
            info.size, info.mode = len(data), 0o600
            archive.addfile(info, io.BytesIO(data))
            for entry in entries:
                directory = arena.root / 'matches' / entry['job_id'] / entry['directory']
                for name in entry['files']:
                    archive.add(directory / name, arcname=entry['job_id'] + '/' + name, recursive=False)
        stage.rename(target)
    require(target.stat().st_size <= MAX_BATCH_BYTES, 'batch exceeds download bound')
    report = dict(manifest, archive_path=str(target), archive_sha256=file_hash(target),
                  archive_size=target.stat().st_size, project_bytes=sum(e['files']['project.zip']['size'] for e in entries))
    atomic_json(root / (batch + '.json'), report)
    arena.db.put('offload_pending', report)
    return report


def finish_cleanup(arena, job):
    """Reconcile a pointer committed before old-byte cleanup or alias creation."""
    current = Path(job['artifact'])
    marker = read_json(current / 'project-offload.json')
    previous = marker['previous_directory']
    require(previous == Path(previous).name and previous != current.name, 'unsafe previous artifact directory')
    old = current.parent / previous
    require(current.resolve().parent == (arena.root / 'matches' / job['id']).resolve(), 'unsafe offloaded artifact')
    if old.is_symlink():
        require(old.resolve() == current.resolve(), 'legacy artifact alias changed')
        return
    verify_artifacts(current, job['id'], job['attempt_count'])
    if old.exists():
        require(file_hash(old / 'completion.json') == marker['original_completion_sha256'] and
                file_hash(old / 'project.zip') == marker['project_sha256'], 'original changed; preserve it')
        remove_redundant(old)
    old.symlink_to(current.name, target_is_directory=True)


def acknowledge(arena, receipt):
    batch = checked_id(receipt['batch_id'])
    prior = arena.db.get('offload_receipt:' + batch)
    if prior:
        require(prior['archive_sha256'] == receipt['archive_sha256'] and
                prior['archive_root'] == receipt['archive_root'], 'conflicting archive receipt')
        return prior
    pending = arena.db.get('offload_pending')
    require(pending and pending['batch_id'] == batch and
            pending['archive_sha256'] == receipt['archive_sha256'], 'receipt does not match pending bytes')
    require(receipt.get('verified') is True and receipt.get('fsynced') is True, 'verified durable local copy required')
    destination = receipt.get('archive_root')
    require(isinstance(destination, str) and Path(destination).is_absolute() and len(destination) <= 1000,
            'absolute operator archive address required')
    for entry in pending['entries']:
        job = arena.db.one('SELECT * FROM match_jobs WHERE id=?', (entry['job_id'],))
        require(job and job['state'] == 'COMPLETED' and job['attempt_count'] == entry['attempt'], 'match identity changed')
        old = Path(job['artifact'])
        if (old / 'project-offload.json').exists():
            require(read_json(old / 'project-offload.json')['batch_id'] == batch, 'different offload already recorded')
            finish_cleanup(arena, job)
            continue
        require(old.name == entry['directory'] and
                old.resolve().parent == (arena.root / 'matches' / job['id']).resolve(), 'artifact pointer changed')
        result = verify_artifacts(old, job['id'], entry['attempt'])
        for name, expected in entry['files'].items():
            require(file_hash(old / name) == expected['sha256'], 'source bytes changed before acknowledgement')
        final = old.with_name(old.name + '-offloaded')
        stage = old.with_name('.offload-' + old.name)
        if not final.exists():
            if stage.exists():
                remove_redundant(stage)  # Original verified above; only regenerable staging is replaced.
            require(shutil.disk_usage(arena.root).free > 32 * 1024**2, 'insufficient safe staging space')
            shutil.copytree(old, stage, ignore=lambda src,names: ['project.zip', 'completion.json'] if Path(src)==old else [])
            atomic_json(stage / 'project-offload.json', {
                'batch_id':batch, 'archive_root':destination, 'archive_relative_path':'batches/' + Path(pending['archive_path']).name,
                'archive_sha256':pending['archive_sha256'], 'project_sha256':entry['files']['project.zip']['sha256'],
                'original_completion_sha256':entry['files']['completion.json']['sha256'],
                'original_completion':read_json(old / 'completion.json'), 'previous_directory':old.name,
                'verified_local_copy_at':time.time(), 'retained_online':'all replays, statistics, diagnostic logs and result provenance'})
            seal_artifacts(stage, job['id'], entry['attempt'], result)
            stage.rename(final)
        verify_artifacts(final, job['id'], entry['attempt'])
        require(read_json(final / 'project-offload.json')['batch_id'] == batch, 'offload staging identity mismatch')
        with arena.db.transaction():
            arena.db.execute('UPDATE match_jobs SET artifact=? WHERE id=?', (str(final), job['id']))
            arena.db.execute('UPDATE match_attempts SET artifact=? WHERE job_id=? AND number=?',
                             (str(final), job['id'], entry['attempt']))
        job['artifact'] = str(final)
        finish_cleanup(arena, job)
    done = dict(receipt, project_bytes=pending['project_bytes'], matches=len(pending['entries']), acknowledged_at=time.time())
    atomic_json(base_path(arena) / (batch + '-receipt.json'), done)
    with arena.db.transaction():
        arena.db.put('offload_receipt:' + batch, done)
        arena.db.put('offload_last_completed', done)
        arena.db.put('offload_pending', None)
    Path(pending['archive_path']).unlink(missing_ok=True)
    return done
