import json
from pathlib import Path
from unittest.mock import patch

from test_arena import Harness
from arena.common import ArenaError, atomic_json, tree_manifest
from arena.engine import BuildError
from arena.memory import task_history
from arena.protocol import encode_source
from arena.supervisor import handle_request, new_task


class MemoryTests(Harness):
    def result(self, task, outcome='BLOCKED'):
        return {'protocol_version': 1, 'task_id': task['task_id'], 'bot_id': task['bot_id'],
                'base_source_hash': task['base_source_hash'], 'outcome': outcome,
                'hypothesis': 'Prior hypothesis must not be forgotten', 'changed_paths': [],
                'evidence': [], 'tests': [], 'blocked_reason': 'Compiler failure' if outcome == 'BLOCKED' else None,
                'next_action': 'Inspect the exact-source check before retrying'}

    def test_blocked_and_no_change_results_survive_fresh_tasks(self):
        self.establish()
        for outcome, state in [('BLOCKED', 'PAUSED'), ('NO_CHANGE', 'NO_CHANGE')]:
            task = new_task(self.arena, 'alpha')
            handle_request(self.arena, 'alpha', {'operation': 'worker-finished', 'payload': {
                'task_id': task['task_id'], 'state': state, 'worker_result': self.result(task, outcome)}})
            next_task = new_task(self.arena, 'alpha')
            history = next_task['feedback']['handoff']['recent_history']['entries']
            entry = next(e for e in history if e['id'] == task['task_id'])
            self.assertEqual(entry['worker_result']['hypothesis'], 'Prior hypothesis must not be forgotten')
            self.assertEqual(entry['worker_result']['outcome'], outcome)

    def test_history_is_paged_and_lane_scoped(self):
        self.establish()
        ids = [new_task(self.arena, 'alpha')['task_id'] for _ in range(10)]
        page = task_history(self.arena, 'alpha')
        self.assertEqual(len(page['entries']), 8)
        self.assertEqual(page['next_offset'], 8)
        self.assertEqual(len(task_history(self.arena, 'alpha', 8)['entries']), 2)
        with self.assertRaisesRegex(ArenaError, 'this lane'):
            task_history(self.arena, 'beta', task_id=ids[0])

    def test_exact_source_is_not_confused_with_latest_candidate(self):
        alpha, _ = self.establish()
        revision = self.commit('alpha', 'unaccepted historical source')
        self.arena.start_evaluation(revision['id'])
        self.finish_all()
        task = new_task(self.arena, 'alpha')
        handoff = task['feedback']['handoff']
        self.assertEqual(task['input_revision'], revision['commit_sha'])
        self.assertEqual(handoff['edit_start']['commit'], alpha['commit_sha'])
        self.assertEqual(handoff['edit_start']['source_file_sha256'], tree_manifest(Path(alpha['snapshot']) / 'src'))
        self.assertFalse(handoff['last_evaluated_source_is_edit_start'])
        self.assertIn('sources/GameRules.md', handoff['documentation_sha256'])

    def test_build_failure_has_bounded_readable_diagnostics(self):
        alpha, _ = self.establish()
        task = new_task(self.arena, 'alpha')
        output = self.path / 'compiler-output'
        output.mkdir()
        (output / 'stderr.log').write_text('x' * 9000 + '\nerror: no matching function')
        failure = BuildError(output, {'returncode': 1, 'timeout': False}, 'side-a')
        with patch.object(self.engine, 'prepare_bot', side_effect=failure):
            report = handle_request(self.arena, 'alpha', {'operation': 'check', 'payload': {
                'task_id': task['task_id'], 'source': encode_source(Path(alpha['snapshot']) / 'src')}})
        self.assertEqual(report['state'], 'FAILED')
        self.assertNotIn('report_path', report)
        self.assertIn('error: no matching function', report['diagnostics']['stderr.log'])
        self.assertLessEqual(len(report['diagnostics']['stderr.log'].encode()), 8192)
        retrieved = handle_request(self.arena, 'alpha', {'operation': 'check-report', 'payload': {
            'task_id': task['task_id'], 'source_hash': report['source_hash']}})
        self.assertEqual(retrieved['diagnostics'], report['diagnostics'])
        with self.assertRaisesRegex(ArenaError, 'identity'):
            handle_request(self.arena, 'beta', {'operation': 'check-report', 'payload': {
                'task_id': task['task_id'], 'source_hash': report['source_hash']}})

    def test_historical_holdout_details_never_exported(self):
        self.establish()
        task = new_task(self.arena, 'alpha')
        revision = self.commit('alpha', 'fake candidate')
        self.arena.db.execute('UPDATE revisions SET experiment_id=? WHERE id=?', (task['task_id'], revision['id']))
        eid = self.arena.start_evaluation(revision['id'])
        self.finish_all()
        evaluation = self.arena.db.one('SELECT metrics FROM evaluations WHERE id=?', (eid,))
        metrics = json.loads(evaluation['metrics'])
        metrics.update(per_map={'monolith': {'secret': 100}}, representative_failures=[{'match_id': 'hidden-job'}])
        self.arena.db.execute('UPDATE evaluations SET metrics=? WHERE id=?', (json.dumps(metrics), eid))
        history = json.dumps(task_history(self.arena, 'alpha', task_id=task['task_id'], detailed=True))
        self.assertNotIn('hidden-job', history)
        self.assertNotIn('monolith', history)
