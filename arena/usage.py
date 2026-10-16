"""Native CLI usage observations, not an estimate of subscription entitlement."""
import json
from pathlib import Path


def usage_summary(path):
    totals = None
    commands = output_bytes = document_reads = wrapper_calls = 0
    with Path(path).open(errors='replace') as stream:
        for line in stream:
            try:
                event = json.loads(line)
            except ValueError:
                continue
            if not isinstance(event, dict):
                continue
            if event.get('type') == 'turn.completed' and isinstance(event.get('usage'), dict):
                for key in ('input_tokens', 'cached_input_tokens', 'cache_write_input_tokens',
                            'output_tokens', 'reasoning_output_tokens'):
                    value = event['usage'].get(key)
                    if type(value) is int and value >= 0:
                        if totals is None:
                            totals = {}
                        totals[key] = totals.get(key, 0) + value
            item = event.get('item') or {}
            if not isinstance(item, dict):
                continue
            if event.get('type') == 'item.completed' and item.get('type') == 'command_execution':
                commands += 1
                command = item.get('command') or ''
                output = item.get('aggregated_output') or ''
                if not isinstance(command, str) or not isinstance(output, str):
                    continue
                output_bytes += len(output.encode())
                document_reads += int(any(name in command for name in
                                          ('sources/GameRules.md', 'sources/BotAPIPython.md', 'cambc.h')))
                wrapper_calls += int('bot-check ' in command)
    if totals and 'input_tokens' in totals and 'cached_input_tokens' in totals:
        totals['input_tokens_not_read_from_cache'] = max(0, totals['input_tokens'] - totals['cached_input_tokens'])
    return {'reported_tokens': totals, 'completed_command_events': commands,
            'command_output_bytes': output_bytes, 'documentation_command_events': document_reads,
            'wrapper_command_events': wrapper_calls,
            'limitations': 'Missing usage is unknown, not zero. Cached input and reasoning are subsets, not extra tokens. '
                          'Command categories are heuristics. Counts do not determine five-hour quota or dollars.'}
