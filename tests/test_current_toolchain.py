"""Real saved current-format regression plus synthetic scheduling coverage."""
import copy
import json
from pathlib import Path
import tempfile
from unittest.mock import patch

from arena.common import ArenaError, atomic_json, read_json
from arena.engine import normalize_result
from arena.statistics import read_current,ENGINE_IDENTITIES
from test_arena import Harness, ENGINE_HASH, synthetic_contract
from arena.memory import training_window
from arena.training import roster


FIXTURE = Path(__file__).parent / 'fixtures/cambc-225-starter-projection.json'


class CurrentToolchainTests(Harness):
    def test_305_actual_statistics_require_the_matching_local_contract(self):
        stats=read_json(FIXTURE.with_name('cambc-305-starter-projection.json'))
        faults,metrics,suspensions=read_current(stats,expected_engine=ENGINE_IDENTITIES['3.0.5'])
        self.assertEqual(faults,0)
        self.assertEqual(metrics['submitted_gems']['value'],{'A':373,'B':637})
        with self.assertRaises(ArenaError):read_current(stats)
        with tempfile.TemporaryDirectory() as temp:
            output=Path(temp);atomic_json(output/'final.json',stats)
            atomic_json(output/'process-result.json',{'returncode':0,'timeout':False})
            (output/'placeholder.repl26a').write_bytes(b'SYNTHETIC replay presence only')
            contract=synthetic_contract()
            contract.update(statistics_schema='cambc-305-json-v1',completion_mode='final_statistics_contract',
                winner_pointer='/match/outcome',winner_values={'teamA':'A','teamB':'B'},reason_pointer=None)
            self.assertEqual(normalize_result(output,contract,ENGINE_HASH)['state'],'COMPLETED')
            contract['statistics_schema']='cambc-225-json-v1'
            self.assertEqual(normalize_result(output,contract,ENGINE_HASH)['state'],'INFRA_ERROR')

    def test_current_forty_map_suite_freezes_every_map_on_both_sides(self):
        self.establish()
        manifest=read_json(FIXTURE.parent.parent.parent/'evidence/map-pool-305.json')
        self.config['evaluation'].update(full_evaluation=True,
            screen_maps=['00collision','00corners','00elkring'],
            development_maps=[m['name'] for m in manifest['maps'] if m['role']=='development'],
            holdout_maps=[m['name'] for m in manifest['maps'] if m['role']=='holdout'])
        for m in manifest['maps']:(self.maps/(m['name']+'.map26a')).write_text('SYNTHETIC MAP '+m['name'])
        from arena.common import file_hash
        atomic_json(self.path/'maps.json',{'maps':[{'name':m['name'],
            'sha256':file_hash(self.maps/(m['name']+'.map26a'))} for m in manifest['maps']]})
        row=self.commit('alpha','forty-map contender');eid=self.arena.start_evaluation(row['id'])
        self.finish_all()
        cells={(c['map_name'],c['candidate_side']) for c in self.arena.evaluation_cases(eid) if c['role']=='candidate'}
        self.assertEqual(cells,{(m['name'],side) for m in manifest['maps'] for side in ('A','B')})
        self.assertEqual(len(cells),80)

    def test_current_saved_official_statistics_and_unknown_versions_fail_closed(self):
        stats = read_json(FIXTURE)
        faults, metrics, suspensions = read_current(stats)
        self.assertEqual((faults, suspensions), (0, 0))
        self.assertEqual(metrics['submitted_gems']['value'], {'A':1012, 'B':550})
        self.assertEqual(metrics['lifetime_earned_gold']['value'], {'A':4950, 'B':4140})
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            atomic_json(output / 'final.json', stats)
            atomic_json(output / 'process-result.json', {'returncode':0,'timeout':False})
            (output / 'placeholder.repl26a').write_bytes(b'SYNTHETIC replay presence only')
            contract = synthetic_contract()
            contract.update(statistics_schema='cambc-225-json-v1', completion_mode='final_statistics_contract',
                            winner_pointer='/match/outcome', winner_values={'teamA':'A','teamB':'B'},
                            reason_pointer=None, metric_pointers={'round':'/match/roundsStarted'},
                            fuel_suspension_patterns=[])
            result = normalize_result(output, contract, ENGINE_HASH)
            self.assertEqual(result['state'], 'COMPLETED')
            self.assertEqual(result['winner'], 'A')
            self.assertEqual(result['fuel_suspensions'], 0)
            for field, value in [('engineBuildHash','0'*64), ('engineVersion','0.0.4'),
                                 ('metricSemanticsVersion',2), ('roundsStarted',2001)]:
                bad = copy.deepcopy(stats)
                bad['match'][field] = value
                atomic_json(output / 'final.json', bad)
                self.assertEqual(normalize_result(output, contract, ENGINE_HASH)['state'], 'INFRA_ERROR')

    def test_incomplete_diagnostics_are_not_zero_suspensions(self):
        stats = read_json(FIXTURE)
        stats['diagnostics']['detailedCaptureComplete'] = False
        _, metrics, suspensions = read_current(stats)
        self.assertIsNone(suspensions)
        self.assertNotIn('bag_loss', metrics)
        stats['champions'][0]['metrics']['earnedGold'] = '-1'
        with self.assertRaises(ArenaError):
            read_current(stats)

    def test_full_published_seventeen_map_suite_includes_every_map_on_both_sides(self):
        self.establish()
        manifest = read_json(Path(__file__).parent.parent / 'evidence/map-pool-225.json')
        self.config['evaluation'].update(full_evaluation=True, max_promotion_checks_per_day=0,
            development_maps=[m['name'] for m in manifest['maps']
                              if m['name'] not in self.config['evaluation']['holdout_maps']])
        for name in self.config['evaluation']['development_maps']:
            (self.maps / (name + '.map26a')).write_text('SYNTHETIC MAP: ' + name)
        from arena.common import file_hash
        atomic_json(self.path / 'maps.json', {'maps':[
            {'name':p.stem, 'sha256':file_hash(p)} for p in sorted(self.maps.glob('*.map26a'))]})
        candidate = self.commit('alpha', 'current complete contender')
        eid = self.arena.start_evaluation(candidate['id'])
        self.finish_all()
        cases = [c for c in self.arena.evaluation_cases(eid) if c['role']=='candidate']
        self.assertEqual(len(cases), 34)
        self.assertEqual({(c['map_name'],c['candidate_side']) for c in cases},
                         {(m['name'],side) for m in manifest['maps'] for side in ('A','B')})
        self.assertFalse(self.config['evaluation']['automatic_promotion'])

    def test_feedback_windows_separate_the_same_source_on_different_engines(self):
        self.establish()
        old = training_window(self.arena, 'alpha')['source_groups']
        self.assertEqual(len(old), 1)
        old_hash = self.engine.lock_hash
        self.engine.lock_hash = 'a' * 64
        candidate = self.arena.db.one("SELECT accepted_revision FROM bots WHERE id='alpha'")['accepted_revision']
        self.arena.db.execute("UPDATE revisions SET state='PENDING' WHERE id=?", (candidate,))
        self.arena.start_evaluation(candidate)
        self.finish_all()
        groups = training_window(self.arena, 'alpha')['source_groups']
        self.assertEqual({g['engine_lock_hash'] for g in groups}, {old_hash, 'a'*64})
        self.assertEqual(len({g['source_hash'] for g in groups}), 1)

    def test_old_engine_results_cannot_select_a_current_training_roster(self):
        self.establish()
        for worker in self.config['workers'].values():
            worker.update(enabled=True, owner_confirmed=True)
        self.assertEqual(set(roster(self.arena)), {'alpha','beta'})
        self.engine.lock_hash = 'a' * 64
        self.assertEqual(roster(self.arena), {})

    def test_evaluation_restart_keeps_original_builds_instead_of_rebuilding_new_inputs(self):
        self.establish()
        self.config['evaluation']['full_evaluation'] = True
        candidate = self.commit('alpha','frozen complete contender')
        eid = self.arena.start_evaluation(candidate['id'])
        frozen = self.arena.db.one('SELECT suite FROM evaluations WHERE id=?',(eid,))['suite']
        self.config['infrastructure_commit'] = 'a'*40
        with patch.object(self.arena,'build',side_effect=AssertionError('must use frozen builds')):
            self.finish_all()
        self.assertEqual(self.arena.db.one('SELECT suite FROM evaluations WHERE id=?',(eid,))['suite'],frozen)
        self.assertEqual(len({c['map_name'] for c in self.arena.evaluation_cases(eid)}),9)
