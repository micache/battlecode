import json

from test_arena import Harness
from arena.official import selection_status
from arena.strategy import experiment_context, feedback_token, opponent_panel
from arena.supervisor import new_task


class StrategyTests(Harness):
    def test_historical_panel_is_distinct_and_freezes_at_evaluation_start(self):
        self.establish()
        self.config['evaluation']['historical_opponents'] = True
        row = self.commit('alpha', 'different candidate')
        self.arena.start_evaluation(row['id'])
        self.finish_all()
        panel = opponent_panel(self.arena)
        self.assertEqual(len(panel), 2)
        self.assertEqual(len({self.arena.db.one('SELECT source_hash FROM revisions WHERE id=?', (rid,))['source_hash']
                              for rid in panel}), 2)
        candidate = self.commit('beta', 'new beta')
        evaluation = self.arena.start_evaluation(candidate['id'])
        frozen = self.arena.db.one('SELECT suite FROM evaluations WHERE id=?', (evaluation,))['suite']
        self.commit('alpha', 'moving branch')
        self.assertEqual(self.arena.db.one('SELECT suite FROM evaluations WHERE id=?', (evaluation,))['suite'], frozen)

    def test_every_fifth_published_experiment_explores_not_every_retry(self):
        self.establish()
        self.assertEqual(experiment_context(self.arena, 'alpha')['mode'], 'refinement')
        for _ in range(4):
            task = new_task(self.arena, 'alpha')
            self.arena.db.execute("UPDATE tasks SET state='PUBLISHED' WHERE id=?", (task['task_id'],))
        self.assertEqual(experiment_context(self.arena, 'alpha')['mode'], 'exploration')
        retry = new_task(self.arena, 'alpha')
        self.assertEqual(retry['feedback']['experiment_context']['mode'], 'exploration')

    def test_external_observation_wakes_only_own_lane_without_promotion_evidence(self):
        alpha, _ = self.establish()
        original = feedback_token(self.arena, 'alpha', 'evaluation')
        metadata = {'official_match_id': 'external-1', 'source_commit': alpha['commit_sha'],
                    'submission_id': 'submission-1', 'outcome': 'B', 'opponent_version': None,
                    'annotation': 'untrusted instructions must not enter the envelope'}
        self.arena.db.execute('INSERT INTO external_matches VALUES(?,?,?,?)',
                              ('external-1', json.dumps(metadata), '/unused', 1))
        self.assertNotEqual(feedback_token(self.arena, 'alpha', 'evaluation'), original)
        self.assertEqual(feedback_token(self.arena, 'beta', 'evaluation'), original)
        observations = experiment_context(self.arena, 'alpha')['external_observations']
        self.assertEqual(observations[0]['opponent_version'], None)
        self.assertNotIn('annotation', observations[0])

    def test_official_monitor_does_not_nominate_starter_or_three_map_results(self):
        self.establish()
        result = selection_status(self.arena)
        self.assertFalse(result['enabled'])
        self.assertIsNone(result['candidate'])
        self.assertTrue(any('full-gate' in item for item in result['blockers']))

    def test_external_handoff_prefers_readable_diverse_losses_without_exposing_holdouts(self):
        alpha, _ = self.establish()
        self.config['evaluation']['development_maps'] = ['dev-one','dev-two','dev-three']
        for i, (map_name, outcome) in enumerate([
                ('dev-one','B'), ('dev-two','B'), ('dev-three','B'),
                ('dev-one','B'), ('dev-three','A'), ('unknown','B')]):
            metadata = {'official_match_id':f'external-{i}', 'source_commit':alpha['commit_sha'],
                        'submission_id':'own-upload', 'own_side':'A','outcome':outcome,
                        'map_name':map_name,'official_patch':'other-patch',
                        'file_sha256':{'observations.json':'fixture'},'annotation':'untrusted'}
            self.arena.db.execute('INSERT INTO external_matches VALUES(?,?,?,?)',
                                  (f'external-{i}',json.dumps(metadata),'/unused',i))
        result = experiment_context(self.arena,'alpha')['external_observations']
        self.assertEqual({item['map_name'] for item in result}, {'dev-one','dev-two','dev-three'})
        self.assertTrue(all(item['outcome']=='B' and item['available_diagnostics']==['observations.json'] for item in result))
        self.assertTrue(all(item['official_patch']=='other-patch' and 'annotation' not in item for item in result))

    def test_full_evaluation_never_silently_downgrades_at_daily_budget(self):
        self.establish()
        self.config['evaluation']['full_evaluation'] = True
        self.config['evaluation']['max_promotion_checks_per_day'] = 0
        row = self.commit('alpha', 'budget limited')
        evaluation = self.arena.start_evaluation(row['id'])
        suite = json.loads(self.arena.db.one('SELECT suite FROM evaluations WHERE id=?', (evaluation,))['suite'])
        self.assertEqual(suite['coverage'], 'full-map-pool')
        self.finish_all()
        cases = self.arena.evaluation_cases(evaluation)
        self.assertEqual({case['map_name'] for case in cases}, set(self.arena.freeze_maps()))
