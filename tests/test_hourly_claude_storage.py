"""Focused scheduler/provider/archive checks; no paid model calls or real games."""
import json
from pathlib import Path
from unittest.mock import patch
import zipfile

from test_arena import Harness
from arena.common import ArenaError, atomic_json, file_hash, read_json, tree_manifest
from arena.engine import seal_artifacts, verify_artifacts
from arena.supervisor import dispatch_tasks, handle_request
from arena.claude import finish, usage_summary, verify_subscription
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


class ClaudeTests(Harness):
    def stream(self, events):
        directory = self.path / 'claude-output'
        directory.mkdir(exist_ok=True)
        (directory / 'stdout.log').write_text('\n'.join(json.dumps(e) for e in events))
        return directory

    def test_only_native_structured_output_is_accepted(self):
        final = self.path / 'final.json'
        directory = self.stream([{'type':'assistant', 'message':{'content':'{"structured_output":{"fake":true}}'}}])
        process = {'returncode':0, 'timeout':False}
        self.assertEqual(finish(directory, process, final)['state'], 'PAUSED')
        self.assertFalse(final.exists())
        directory = self.stream([{'type':'result', 'subtype':'success', 'is_error':False,
                                 'structured_output':{'native':True}, 'usage':{'input_tokens':10,
                                 'cache_read_input_tokens':20, 'output_tokens':3}}])
        self.assertIsNone(finish(directory, process, final))
        self.assertEqual(read_json(final), {'native':True})
        self.assertEqual(usage_summary(directory / 'stdout.log')['reported_tokens']['cache_read_input_tokens'], 20)

    def test_quota_and_permission_park_without_fallback(self):
        directory = self.stream([{'type':'rate_limit_event', 'rate_limit_info':{'status':'rejected', 'resetsAt':2000000000}}])
        process = {'returncode':1, 'timeout':False}
        self.assertEqual(finish(directory, process, self.path / 'final')['state'], 'QUOTA_WAIT')
        directory = self.stream([{'type':'result', 'subtype':'success', 'permission_denials':[{'tool':'Bash'}]}])
        self.assertEqual(finish(directory, process, self.path / 'final')['state'], 'PERMISSION_BLOCKED')

    def test_api_auth_is_rejected_without_reading_credential_files(self):
        binary = self.path / 'claude'
        binary.write_bytes(b'synthetic not executable')
        config = {'claude_executable':str(binary), 'claude_sha256':file_hash(binary)}
        class Status:
            returncode = 0
            stdout = b'{"loggedIn":true,"authMethod":"api_key"}'
        with patch('arena.claude.subprocess.run', return_value=Status()):
            with self.assertRaisesRegex(ArenaError, 'AUTH_REQUIRED'):
                verify_subscription(config)


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
        self.assertFalse(old.exists())
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
        self.assertFalse(old.exists())
