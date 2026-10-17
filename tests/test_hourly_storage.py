"""Focused scheduler/archive checks; no model calls or real games."""
import json
from pathlib import Path
from unittest.mock import patch
import zipfile

from test_arena import Harness
from arena.common import tree_manifest
from arena.engine import seal_artifacts, verify_artifacts
from arena.supervisor import dispatch_tasks, handle_request
from arena.storage import archive_projects, verify_project_archive
from arena.memory import training_window
from arena.service import Arena


class HourlyTests(Harness):
    def test_hourly_runs_even_on_unchanged_feedback_but_never_bursts(self):
        self.establish()
        self.config['limits']['improvement_interval_seconds'] = 3600
        self.config['workers']['alpha'].update(enabled=True, owner_confirmed=True)
        self.arena.db.execute("UPDATE workers SET state='IDLE',paused=0 WHERE id='alpha'")
        with patch('arena.supervisor.time.time', return_value=2000000000):
            dispatch_tasks(self.arena)
            first = self.arena.db.one("SELECT * FROM workers WHERE id='alpha'")['task_id']
            handle_request(self.arena, 'alpha', {'operation':'worker-finished',
                           'payload':{'task_id':first, 'state':'NO_CHANGE'}})
        self.arena.db.connection.close()
        self.arena = Arena(self.config, self.engine)  # A restart retains the hourly timer.
        with patch('arena.supervisor.time.time', return_value=2000003599):
            dispatch_tasks(self.arena)
            self.assertEqual(self.arena.db.one('SELECT count(*) AS n FROM tasks')['n'], 1)
        with patch('arena.supervisor.time.time', return_value=2000003600):
            dispatch_tasks(self.arena)
            self.assertEqual(self.arena.db.one('SELECT count(*) AS n FROM tasks')['n'], 2)
            self.assertNotEqual(self.arena.db.one("SELECT task_id FROM workers WHERE id='alpha'")['task_id'], first)
            dispatch_tasks(self.arena)
            self.assertEqual(self.arena.db.one('SELECT count(*) AS n FROM tasks')['n'], 2)

    def test_training_window_separates_sources_and_excludes_holdouts(self):
        self.establish()
        window = training_window(self.arena, 'alpha')
        self.assertTrue(window['source_groups'])
        for group in window['source_groups']:
            self.assertEqual(group['completed'], group['wins'] + group['losses'])
            self.assertFalse(any(name.split('/')[0] in self.config['evaluation']['holdout_maps']
                                 for name in group['by_map_side']))


class ArchiveTests(Harness):
    def test_completed_worktree_is_byte_recoverable_and_replay_unchanged(self):
        self.establish()
        job = self.arena.db.one("SELECT * FROM match_jobs WHERE state='COMPLETED' LIMIT 1")
        old = Path(job['artifact'])
        old.chmod(0o750)
        project = old / 'project'
        project.mkdir()
        (project / 'source.cpp').write_bytes(b'int main() {}\n')
        (project / 'build.wasm').write_bytes(bytes(range(256)) * 1000)
        artifacts = old / 'artifacts'
        artifacts.mkdir(exist_ok=True)
        replay = artifacts / 'saved.repl26a'
        replay.write_bytes(b'original replay')
        expected = tree_manifest(project)
        seal_artifacts(old, job['id'], job['attempt_count'], json.loads(job['result']))
        changed = archive_projects(self.arena)
        self.assertIn(job['id'], changed['archived_projects'])
        new = Path(self.arena.db.one('SELECT artifact FROM match_jobs WHERE id=?', (job['id'],))['artifact'])
        self.assertTrue(old.is_symlink())
        self.assertEqual(old.resolve(), new.resolve())
        self.assertEqual((old / 'artifacts/saved.repl26a').read_bytes(), b'original replay')
        self.assertEqual((new / 'artifacts/saved.repl26a').read_bytes(), b'original replay')
        self.assertEqual(verify_project_archive(new)['files'], expected)
        self.assertEqual(verify_artifacts(new, job['id'], job['attempt_count']), json.loads(job['result']))
        restored = self.path / 'restore-project'
        with zipfile.ZipFile(new / 'project.zip') as archive:
            archive.extractall(restored)
        self.assertEqual(tree_manifest(restored), expected)
        self.assertFalse(archive_projects(self.arena)['archived_projects'])

    def test_crash_after_database_pointer_recovers_verified_redundancy(self):
        self.establish()
        job = self.arena.db.one("SELECT * FROM match_jobs WHERE state='COMPLETED' LIMIT 1")
        old = Path(job['artifact'])
        old.chmod(0o750)
        (old / 'project').mkdir()
        (old / 'project/source').write_bytes(b'safe')
        seal_artifacts(old, job['id'], job['attempt_count'], json.loads(job['result']))
        with patch('arena.storage.remove_redundant', side_effect=OSError('synthetic crash')):
            with self.assertRaises(OSError):
                archive_projects(self.arena)
        self.assertTrue(old.exists())
        archive_projects(self.arena)
        self.assertTrue(old.is_symlink())
