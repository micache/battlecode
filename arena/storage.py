"""Losslessly archive completed per-match working trees, not replays or statistics.

Source snapshots and shared build caches remain separate. A verified new sealed
attempt is published before the old redundant directory is removed. Restart can
finish either side of the database-pointer update without replaying a game.
"""
import hashlib
from pathlib import Path
import shutil
import zipfile

from .common import atomic_json, file_hash, read_json, require, tree_manifest
from .engine import seal_artifacts, verify_artifacts


def remove_redundant(directory):
    def writable_retry(function, path, error):
        Path(path).parent.chmod(0o700)
        Path(path).chmod(0o700)
        function(path)
    shutil.rmtree(directory, onerror=writable_retry)


def verify_project_archive(directory):
    manifest = read_json(Path(directory) / 'project-archive.json')
    with zipfile.ZipFile(Path(directory) / 'project.zip') as archive:
        require(len(archive.namelist()) == len(set(archive.namelist())), 'duplicate archive member')
        actual = {}
        for name in archive.namelist():
            require(not Path(name).is_absolute() and '..' not in Path(name).parts, 'unsafe archive member')
            digest = hashlib.sha256()
            with archive.open(name) as member:
                for block in iter(lambda: member.read(1024 * 1024), b''):
                    digest.update(block)
            actual[name] = digest.hexdigest()
    require(actual == manifest['files'], 'project archive byte verification failed')
    return manifest


def archive_projects(arena, limit=8):
    changed = []
    for job in arena.db.all("SELECT * FROM match_jobs WHERE state='COMPLETED' AND artifact IS NOT NULL ORDER BY created"):
        if len(changed) >= limit:
            break
        old = Path(job['artifact'])
        base = arena.root / 'matches' / job['id']
        require(old.resolve().parent == base.resolve(), 'unexpected completed match path')
        if (old / 'project-archive.json').exists():
            # Crash after publishing the new pointer but before removing redundancy.
            original = read_json(old / 'project-archive.json')['previous_directory']
            require(original == Path(original).name and original != old.name, 'unsafe recovery directory')
            leftover = base / original
            if leftover.is_symlink():
                target = leftover.readlink()
                require(not target.is_absolute() and target.name == str(target) and leftover.resolve() == old.resolve(),
                        'unexpected legacy artifact alias')
                continue
            if leftover.exists():
                verify_artifacts(old, job['id'], job['attempt_count'])
                manifest = verify_project_archive(old)
                if (leftover / 'completion.json').exists():
                    require(file_hash(leftover / 'completion.json') == manifest['previous_completion_sha256'],
                            'original completion changed; preserve redundant copy')
                remove_redundant(leftover)
            # Parser/readiness records can name exact historical raw-file paths.
            # Keep their locations valid without duplicating retained bytes.
            leftover.symlink_to(old.name, target_is_directory=True)
            continue
        if not (old / 'project').is_dir():
            continue
        result = verify_artifacts(old, job['id'], job['attempt_count'])
        final = old.with_name(old.name + '-archived')
        stage = old.with_name('.archive-' + old.name)
        if not final.exists():
            if stage.exists() and not (stage / 'completion.json').exists():
                # Old sealed evidence was verified above and is still authoritative.
                # This explicit sibling contains only a regenerable partial copy.
                remove_redundant(stage)
            if stage.exists():
                verify_artifacts(stage, job['id'], job['attempt_count'])
                verify_project_archive(stage)
            else:
                size = sum(p.stat().st_size for p in old.rglob('*') if p.is_file())
                if shutil.disk_usage(arena.root).free < size + 32 * 1024**2:
                    break  # Staging must never consume the last free disk blocks.
                shutil.copytree(old, stage, ignore=lambda src, names: ['project', 'completion.json']
                                if Path(src) == old else [])
                for path in [stage, *stage.rglob('*')]:
                    path.chmod(0o750 if path.is_dir() else 0o640)
                files = tree_manifest(old / 'project')
                with zipfile.ZipFile(stage / 'project.zip', 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
                    for name in files:
                        archive.write(old / 'project' / name, name)
                atomic_json(stage / 'project-archive.json', {'files':files, 'previous_directory':old.name,
                            'previous_completion_sha256':file_hash(old / 'completion.json'),
                            'previous_completion':read_json(old / 'completion.json'),
                            'restore':'unzip project.zip -d project; verify member hashes against files in project-archive.json'})
                verify_project_archive(stage)
                seal_artifacts(stage, job['id'], job['attempt_count'], result)
            stage.rename(final)
        verify_artifacts(final, job['id'], job['attempt_count'])
        manifest = verify_project_archive(final)
        require(file_hash(old / 'completion.json') == manifest['previous_completion_sha256'], 'original completion changed')
        with arena.db.transaction():
            arena.db.execute('UPDATE match_jobs SET artifact=? WHERE id=?', (str(final), job['id']))
            arena.db.execute('UPDATE match_attempts SET artifact=? WHERE job_id=? AND number=?',
                             (str(final), job['id'], job['attempt_count']))
        remove_redundant(old)
        old.symlink_to(final.name, target_is_directory=True)
        changed.append(job['id'])
    return {'archived_projects':changed, 'replays_statistics_and_source_snapshots':'unchanged'}
