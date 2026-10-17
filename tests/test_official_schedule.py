"""No platform calls: durable nomination clock and bounded external evidence."""
import base64

from test_arena import Harness
from arena.common import ArenaError
from arena.official import cadence_status
from arena.operations import import_external
from arena.supervisor import handle_request


class OfficialScheduleTests(Harness):
    def test_five_hour_clock_survives_repeated_status_without_upload(self):
        candidate = {'source_hash':'a' * 64}
        first = cadence_status(self.arena, candidate, now=100000)
        self.assertEqual(first['next_check_at'], 118000)
        self.assertEqual(first['action'], 'NOMINATED_NOT_UPLOADED')
        self.assertFalse(cadence_status(self.arena, candidate, now=117999)['due'])
        self.assertTrue(cadence_status(self.arena, candidate, now=118000)['due'])
        self.assertEqual(first['uploads_performed'], 0)

    def test_any_previously_submitted_source_skips_and_waits_three_hours(self):
        candidate = {'source_hash':'a' * 64}
        self.arena.db.put('official_submission:' + candidate['source_hash'],
                          {'confirmed':True, 'submission_id':'synthetic-submission-id'})
        result = cadence_status(self.arena, candidate, now=100000)
        self.assertEqual(result['action'], 'SKIP_ALREADY_SUBMITTED')
        self.assertEqual(result['next_check_at'], 110800)
        self.assertEqual(result['uploads_performed'], 0)

    def test_uncertain_creation_never_retries_upload(self):
        self.arena.db.put('official_upload_intent', {'state':'UNKNOWN'})
        self.assertEqual(cadence_status(self.arena, {'source_hash':'a' * 64}, now=100000)['action'],
                         'BLOCKED_AMBIGUOUS_CREATION')

    def test_external_diagnostic_is_owned_bounded_and_not_a_tournament_result(self):
        self.establish()
        revision = self.arena.db.one("SELECT * FROM revisions WHERE bot_id='alpha' LIMIT 1")
        payload = {'official_match_id':'synthetic-external-id', 'submission_id':'synthetic-submit-id',
                   'source_commit':revision['commit_sha'], 'opponent_version':None,
                   'outcome':'B', 'map_name':'collision',
                   'files':{'observations.json':base64.b64encode(b'{"observed":"synthetic only"}').decode()}}
        import_external(self.arena, 'alpha', payload)
        request = {'operation':'external-slice', 'payload':{'match_id':payload['official_match_id'],
                                                          'file':'observations.json', 'limit':12}}
        result = handle_request(self.arena, 'alpha', request)
        self.assertEqual(len(result['text']), 12)
        self.assertIn('Uncontrolled', result['trust'])
        with self.assertRaises(ArenaError):
            handle_request(self.arena, 'beta', request)
        self.assertFalse(self.arena.db.one('SELECT id FROM match_jobs WHERE id=?', (payload['official_match_id'],)))

    def test_unknown_or_reserved_external_map_does_not_export_trace(self):
        self.establish()
        revision = self.arena.db.one("SELECT * FROM revisions WHERE bot_id='alpha' LIMIT 1")
        payload = {'official_match_id':'synthetic-reserved-id', 'submission_id':'synthetic-submit-id',
                   'source_commit':revision['commit_sha'], 'outcome':'B', 'map_name':'monolith',
                   'files':{'observations.json':base64.b64encode(b'secret holdout detail').decode()}}
        import_external(self.arena, 'alpha', payload)
        with self.assertRaisesRegex(ArenaError, 'development map'):
            handle_request(self.arena, 'alpha', {'operation':'external-slice',
                           'payload':{'match_id':payload['official_match_id'], 'file':'observations.json'}})
