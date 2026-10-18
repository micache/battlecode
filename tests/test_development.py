"""Synthetic outcomes validate continuation; they are not strategy evidence."""
import json

from test_arena import Harness
from arena.development import select_base
from arena.supervisor import new_task
from arena.common import read_json, validate_schema
from test_arena import PROJECT


class DevelopmentTests(Harness):
    def evaluate(self, policy, win_maps=None, fault=False):
        row = self.commit('alpha', policy)
        original = self.engine.run_match
        def outcome(spec, output):
            result = original(spec, output)
            if row['source_hash'] in (spec['a_source_hash'], spec['b_source_hash']):
                if win_maps is None or spec['map_name'] in win_maps:
                    result['winner'] = 'A' if spec['a_source_hash'] == row['source_hash'] else 'B'
                result['bot_faults'] = 1 if fault else 0
            return result
        self.engine.run_match = outcome
        eid = self.arena.start_evaluation(row['id'])
        self.finish_all()
        self.engine.run_match = original
        return row, eid

    def test_improved_development_source_continues_without_champion_promotion(self):
        accepted, _ = self.establish()
        strong, _ = self.evaluate('complete strong policy')
        chosen, decision = select_base(self.arena, 'alpha')
        self.assertEqual(chosen['id'], strong['id'])
        self.assertEqual(decision['advances'][-1]['matched_delta'], .5)
        self.assertEqual(self.arena.db.one("SELECT accepted_revision FROM bots WHERE id='alpha'")['accepted_revision'],
                         accepted['id'])
        task = new_task(self.arena, 'alpha')
        self.assertEqual(task['base_source_hash'], strong['source_hash'])
        self.assertEqual(task['edit_commit'], strong['commit_sha'])
        self.assertEqual(task['accepted_commit'], accepted['commit_sha'])
        self.assertEqual(task['feedback']['handoff']['edit_start']['source_hash'], strong['source_hash'])
        self.assertFalse(self.config['evaluation']['automatic_promotion'])

    def test_ties_regressions_and_faults_do_not_displace_development_base(self):
        self.establish()
        strong, _ = self.evaluate('strong')
        frozen = new_task(self.arena, 'alpha')
        self.evaluate('same wins')
        self.evaluate('weak', win_maps=[])
        self.evaluate('faulty apparent winner', fault=True)
        self.assertEqual(select_base(self.arena, 'alpha')[0]['id'], strong['id'])
        self.assertEqual(frozen['edit_commit'], strong['commit_sha'])

    def test_insufficient_both_side_coverage_is_not_a_training_advance(self):
        accepted, _ = self.establish()
        strong, eid = self.evaluate('incomplete historical record')
        self.arena.db.execute("DELETE FROM evaluation_cases WHERE evaluation_id=? AND role='candidate' "
                              "AND candidate_side='B' AND map_name=?", (eid, self.config['evaluation']['screen_maps'][0]))
        self.assertEqual(select_base(self.arena, 'alpha')[0]['id'], accepted['id'])

    def test_changed_settings_or_engine_cannot_masquerade_as_gain(self):
        accepted, _ = self.establish()
        strong, eid = self.evaluate('different setting')
        for row in self.arena.db.all("SELECT j.id,j.spec FROM match_jobs j JOIN evaluation_cases c ON c.job_id=j.id "
                                     "WHERE c.evaluation_id=? AND c.role='candidate'", (eid,)):
            spec = json.loads(row['spec']); spec['settings_hash'] = 'different'
            self.arena.db.execute('UPDATE match_jobs SET spec=? WHERE id=?', (json.dumps(spec), row['id']))
        self.assertEqual(select_base(self.arena, 'alpha')[0]['id'], accepted['id'])
        self.engine.lock_hash = 'changed-engine'
        self.assertEqual(select_base(self.arena, 'alpha')[0]['id'], accepted['id'])

    def test_holdout_wins_do_not_choose_edit_base_and_selection_repeats_exactly(self):
        accepted, _ = self.establish()
        self.config['evaluation']['full_evaluation'] = True
        self.evaluate('holdout specialist', win_maps=self.config['evaluation']['holdout_maps'])
        first, audit = select_base(self.arena, 'alpha')
        self.assertEqual(first['id'], accepted['id'])
        self.assertEqual(select_base(self.arena, 'alpha'), (first, audit))

    def test_first_shared_workflow_is_foundation_then_uses_experiment_mode(self):
        self.establish()
        first = new_task(self.arena, 'alpha')
        self.assertEqual(first['strategy']['phase'], 'foundation')
        self.arena.db.execute("UPDATE tasks SET state='PUBLISHED' WHERE id=?", (first['task_id'],))
        second = new_task(self.arena, 'alpha')
        self.assertEqual(second['strategy']['phase'], 'refinement')

    def test_new_candidate_and_frozen_development_base_get_same_six_map_panel(self):
        accepted, _ = self.establish()
        base, _ = self.evaluate('strong development source')
        task = new_task(self.arena, 'alpha')
        self.assertEqual(task['development_selection']['revision_id'], base['id'])
        candidate = self.commit('alpha', 'next coherent strategy')
        self.arena.db.execute('UPDATE revisions SET experiment_id=? WHERE id=?', (task['task_id'], candidate['id']))
        eid = self.arena.start_evaluation(candidate['id'])
        self.finish_all()
        rows = self.arena.evaluation_cases(eid)
        own = {(r['map_name'], r['opponent'], r['candidate_side']) for r in rows if r['role']=='candidate'}
        previous = {(r['map_name'], r['opponent'], r['candidate_side']) for r in rows if r['role']=='development-base'}
        self.assertEqual(own, previous)
        self.assertEqual({r[0] for r in own}, set(self.config['evaluation']['development_maps']))
        suite = json.loads(self.arena.db.one('SELECT suite FROM evaluations WHERE id=?', (eid,))['suite'])
        self.assertEqual(suite['development_incumbent_id'], base['id'])
        self.assertEqual(suite['coverage'], 'development-map-pool')
        summary = read_json(self.root / 'feedback/alpha/latest.json')['summary']
        validate_schema(summary, read_json(PROJECT / 'schemas/feedback.schema.json'))
        self.assertEqual(summary['metrics']['development_comparison']['source_hash'], base['source_hash'])
        self.assertEqual(summary['metrics']['development_comparison']['paired_cases'], 6)
        self.assertEqual(self.arena.db.one("SELECT accepted_revision FROM bots WHERE id='alpha'")['accepted_revision'],
                         accepted['id'])
