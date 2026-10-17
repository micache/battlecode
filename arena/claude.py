"""Narrow native Claude Code subscription adapter; no inference SDK or API keys."""
import json
import os
from pathlib import Path
import subprocess

from .common import atomic_json, clean_environment, file_hash, read_json, require


def environment():
    env = clean_environment(True)
    env.update(USE_BUILTIN_RIPGREP='0', DISABLE_AUTOUPDATER='1')
    return env


def verify_subscription(config):
    binary = config['claude_executable']
    require(file_hash(binary) == config['claude_sha256'], 'Claude binary changed; review the pin')
    env = environment()
    status = subprocess.run([binary, '--setting-sources', '', 'auth', 'status'],
                            capture_output=True, env=env, timeout=30)
    try:
        value = json.loads(status.stdout)
    except ValueError:
        value = {}
    require(status.returncode == 0 and value.get('authMethod') == 'claude.ai' and
            value.get('loggedIn') is True, 'AUTH_REQUIRED: native Claude subscription login required; API/Console forbidden')
    return env


def settings(config, attempt):
    attempt = Path(attempt).resolve()
    home = Path(os.path.expanduser('~')).resolve()
    bot = config['bot_id']
    inbox = str(Path(config['root']) / 'inbox' / bot)
    secrets = sorted({str(base / name) for base in (home, Path(os.path.expanduser('~')))
                      for name in ('.claude', '.claude.json', '.codex', '.ssh')})
    denied_writes = [str(path) for path in attempt.iterdir() if path.name not in ('bots', 'experiments', '.agent')]
    for parent in ('bots', 'experiments'):
        denied_writes += [str(p) for p in (attempt / parent).iterdir() if p.name != bot]
    # Native file tools and sandboxed Bash share secret denials. No shell network,
    # custom hooks/plugins/MCP, unsandboxed retries or delegated model sessions.
    return {'permissions': {'defaultMode':'default', 'allow':['Read', 'Glob', 'Grep', 'Bash',
                f'Edit(/{attempt}/bots/{bot}/src/**)', f'Edit(/{attempt}/experiments/{bot}/**)'],
                'deny':[f'Read(/{path}/**)' for path in secrets] +
                       [f'Read(/{path})' for path in secrets] +
                       ['Bash(git push *)', 'Bash(git commit *)']},
            'sandbox': {'enabled':True, 'failIfUnavailable':True, 'allowUnsandboxedCommands':False,
                        'autoAllowBashIfSandboxed':True, 'excludedCommands':[],
                        'enableWeakerNestedSandbox':False, 'enableWeakerNetworkIsolation':False,
                        'filesystem': {'allowWrite':[inbox], 'denyRead':secrets,
                                       'denyWrite':denied_writes},
                        'network': {'allowedDomains':[], 'allowAllUnixSockets':False,
                                    'allowLocalBinding':False}}}


def command(config, attempt, prompt):
    schema = read_json(Path(config['infrastructure']) / 'schemas/worker-result.schema.json')
    task = read_json(Path(config['root']) / 'tasks' / config['bot_id'] / (Path(attempt).name + '.json'))
    sdk = task.get('feedback', {}).get('handoff', {}).get('sdk', {}).get('cpp_header')
    args = [config['claude_executable'], '-p', '--output-format', 'stream-json', '--verbose',
            '--json-schema', json.dumps(schema), '--max-turns', '30', '--effort', 'high',
            '--restricted', '--setting-sources', '', '--settings', json.dumps(settings(config, attempt)),
            '--permission-mode', 'default', '--permission-prompts', 'none', '--disable-slash-commands',
            '--strict-mcp-config', '--mcp-config', '{"mcpServers":{}}',
            '--tools', 'Read,Edit,Write,Glob,Grep,Bash']
    if sdk:
        args += ['--add-dir', str(Path(sdk).parent)]
    if config.get('model'):
        args += ['--model', config['model']]
    return args + [prompt]


def events(path):
    with Path(path).open(errors='replace') as stream:
        for line in stream:
            try:
                event = json.loads(line)
            except ValueError:
                continue
            if isinstance(event, dict):
                yield event


def finish(directory, process, final):
    """Trust the native result envelope, never JSON embedded in model prose."""
    failure = {'state':'PAUSED', 'detail':'Claude invocation incomplete/malformed; checkpoint retained'}
    if process['timeout']:
        return dict(failure, detail='Claude wall timeout; checkpoint retained; explicit recovery required')
    result = None
    for event in events(Path(directory) / 'stdout.log'):
        if event.get('type') == 'rate_limit_event' and isinstance(event.get('rate_limit_info'), dict):
            info = event['rate_limit_info']
            if info.get('status') == 'rejected':
                reset = info.get('resetsAt')
                return {'state':'QUOTA_WAIT', 'reset_at':reset if type(reset) in (int, float) else None,
                        'detail':'Claude native quota response; same owner lane parked'}
        if event.get('type') == 'assistant':
            code = event.get('error')
            if code == 'rate_limit':
                return {'state':'QUOTA_WAIT', 'reset_at':None, 'detail':'Claude native rate limit; no account failover'}
            if code == 'authentication_failed':
                return {'state':'AUTH_REQUIRED', 'detail':'Claude owner must log in manually'}
        if event.get('type') == 'result':
            result = event
    if result and result.get('permission_denials'):
        return {'state':'PERMISSION_BLOCKED', 'detail':'Claude native tool permission denied; policy unchanged'}
    if process['returncode'] or not result or result.get('is_error') or result.get('subtype') != 'success':
        return failure
    require(isinstance(result.get('structured_output'), dict), 'Claude native structured output missing')
    atomic_json(final, result['structured_output'], 0o600)
    return None


def usage_summary(path):
    result = None
    models = set()
    for event in events(path):
        if event.get('type') == 'system' and isinstance(event.get('model'), str):
            models.add(event['model'])
        if event.get('type') == 'result':
            result = event
    raw = result.get('usage', {}) if result else {}
    tokens = {key: raw[key] for key in ('input_tokens', 'output_tokens', 'cache_read_input_tokens',
                                       'cache_creation_input_tokens') if type(raw.get(key)) is int and raw[key] >= 0}
    return {'reported_tokens':tokens or None, 'models':sorted(models),
            'limitations':'Native result usage only; Claude input/cache categories retain provider semantics. '
                         'No conversion to subscription entitlement or billed dollars. Missing is unknown.'}
