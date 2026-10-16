"""Saved official statistics regression; not a new real-engine run."""
from pathlib import Path
import shutil
import tempfile
import unittest

from arena.common import atomic_json, read_json
from arena.engine import normalize_result
from test_arena import ENGINE_HASH, synthetic_contract


class RealStatisticsTests(unittest.TestCase):
    def test_saved_official_schema_and_side_metrics(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            source = Path(__file__).parent / 'fixtures/cambc-216-starter-final.json'
            shutil.copyfile(source, output / 'final.json')
            atomic_json(output / 'process-result.json', {'returncode': 0, 'timeout': False})
            # Presence-only replay placeholder: this unit test does NOT validate a replay.
            (output / 'synthetic.repl26a').write_bytes(b'SYNTHETIC PLACEHOLDER')
            contract = synthetic_contract()
            contract.update(statistics_schema='cambc-216-v2', completion_mode='final_statistics_contract',
                            winner_pointer='/outcome', winner_values={'teamA': 'A', 'teamB': 'B'},
                            reason_pointer=None, metric_pointers={'round': '/round'}, fuel_suspension_patterns=[])
            result = normalize_result(output, contract, ENGINE_HASH)
            self.assertEqual(result['state'], 'COMPLETED')
            self.assertEqual(result['winner'], 'A')
            self.assertEqual(result['bot_faults'], 0)
            self.assertIsNone(result['fuel_suspensions'])
            self.assertEqual(result['metrics']['lifetime_earned_gold']['value']['A'], 5140)
            stats = read_json(output / 'final.json')
            stats['botFaults'] = [2, 0]
            atomic_json(output / 'final.json', stats)
            self.assertEqual(normalize_result(output, contract, ENGINE_HASH)['bot_faults'], 2)
            stats['schemaVersion'] = 3
            atomic_json(output / 'final.json', stats)
            self.assertEqual(normalize_result(output, contract, ENGINE_HASH)['state'], 'INFRA_ERROR')
