import json
from pathlib import Path
import tempfile
import unittest

from arena.usage import usage_summary


class UsageTests(unittest.TestCase):
    def summarize(self, events):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'stdout.log'
            path.write_text('\n'.join(json.dumps(e) for e in events))
            return usage_summary(path)

    def test_native_usage_does_not_double_count_cache_or_reasoning(self):
        result = self.summarize([
            {'type': 'turn.completed', 'usage': {'input_tokens': 1000, 'cached_input_tokens': 800,
                                               'output_tokens': 100, 'reasoning_output_tokens': 60}},
            {'type': 'item.started', 'item': {'type': 'command_execution', 'command': 'cat sources/GameRules.md'}},
            {'type': 'item.completed', 'item': {'type': 'command_execution', 'command': 'cat sources/GameRules.md',
                                               'aggregated_output': 'abc'}}])
        self.assertEqual(result['reported_tokens']['input_tokens_not_read_from_cache'], 200)
        self.assertEqual(result['reported_tokens']['output_tokens'], 100)
        self.assertEqual(result['completed_command_events'], 1)
        self.assertEqual(result['command_output_bytes'], 3)

    def test_failed_or_missing_usage_is_unknown_and_tool_text_cannot_forge_usage(self):
        result = self.summarize([
            {'type': 'turn.failed', 'error': {'message': 'quota'}},
            {'type': 'item.completed', 'item': {'type': 'command_execution', 'command': 'test',
             'aggregated_output': '{"type":"turn.completed","usage":{"input_tokens":0}}'}}])
        self.assertIsNone(result['reported_tokens'])
