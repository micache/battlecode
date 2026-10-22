"""Reviewed CLI 2.2.5 readable statistics, not a second game simulator."""
import math
import re
import gzip
import hashlib
from pathlib import Path
import zlib

from .common import ArenaError, read_json, require


ENGINE_BUILD = 'd7e29ae3546357b011419c764204b7b9e2232bdb1b07868250c6b35d4c18d2a5'
ENGINE_IDENTITIES = {
    '2.2.5': ('0.0.3', ENGINE_BUILD),
    '3.0.5': ('1.0.3','fcb6c3e881c453fb7fcb1ce852ff0a6f10c9e3a199126a000df05b427f4ba41f'),
}
# Outside observations may come from a newer production engine. Reviewing its
# unchanged statistics contract is NOT qualification of our local toolchain.
EXTERNAL_ENGINES = {('0.0.3', ENGINE_BUILD),
    ('1.0.1', 'c3e9ffc8d98c106f86660c58344dc26ced9459a504e2f0d90d88b4c8594c7765'),
    ENGINE_IDENTITIES['3.0.5']}
SIDES = {'teamA': 'A', 'teamB': 'B'}


def saved_bytes(path):
    """Read raw statistics or the byte-verified lossless retained representation."""
    path = Path(path)
    if path.is_file():
        return path.read_bytes()
    proof = read_json(path.parent.parent / 'history-prune.json')['compressed_statistics']
    expected = proof['uncompressed_bytes']
    require(type(expected) is int and 0 <= expected <= 64 * 1024**2, 'invalid retained statistics bound')
    try:
        with gzip.open(str(path) + '.gz', 'rb') as stream:
            data = stream.read(expected + 1)
    except (OSError, EOFError, zlib.error) as exc:
        raise ArenaError('retained statistics compression is corrupt') from exc
    require(len(data) == expected and hashlib.sha256(data).hexdigest() == proof['uncompressed_sha256'],
            'retained statistics bytes changed')
    return data


def unsigned(value):
    # The official readable format serializes uint64 metrics as decimal strings.
    require(type(value) is int or (isinstance(value, str) and re.fullmatch(r'0|[1-9][0-9]*', value)),
            'invalid unsigned statistics value')
    value = int(value)
    require(0 <= value <= 2**64 - 1, 'statistics value outside uint64')
    return value


def read_external(stats):
    match = stats['match']
    engine = (match['engineVersion'], match['engineBuildHash'])
    require(engine in EXTERNAL_ENGINES, 'unreviewed external engine statistics')
    return read_current(stats, expected_engine=engine)


def read_current(stats, *, expected_engine=('0.0.3', ENGINE_BUILD)):
    require(stats['formatVersion'] == stats['jsonFormatVersion'] == '1.0', 'unreviewed statistics format')
    match = stats['match']
    require((match['engineVersion'], match['engineBuildHash']) == tuple(expected_engine) and
            match['metricSemanticsVersion'] == 1, 'unreviewed engine build or metric semantics')
    require(type(match['roundsStarted']) is int and 1 <= match['roundsStarted'] <= 2000 and
            type(match['roundsCompleted']) is int and
            match['roundsStarted'] - match['roundsCompleted'] in (0, 1) and
            type(match['finalRoundPartial']) is bool and
            match['finalRoundPartial'] == (match['roundsStarted'] != match['roundsCompleted']),
            'invalid final round boundary')
    require(match['outcome'] in SIDES and re.fullmatch('[a-f0-9]{64}', match['mapHash']),
            'invalid final outcome or map identity')
    seed = unsigned(match['seed'])
    require([team['team'] for team in stats['teams']] == list(SIDES), 'absolute team order changed')
    faults = stats['diagnostics']['botFaults']
    require(set(faults) == set(SIDES) and all(type(n) is int and n >= 0 for n in faults.values()),
            'invalid official botFaults counters')
    champions = stats['champions']
    require(isinstance(champions, list) and champions and
            len({c['id'] for c in champions}) == len(champions) and
            all(c['team'] in SIDES for c in champions), 'invalid champion identities')
    metrics = {
        'round': match['roundsStarted'],
        'submitted_gems': {SIDES[t['team']]: unsigned(t['submittedGems']) for t in stats['teams']},
        'bot_faults_by_side': {SIDES[t]: n for t, n in faults.items()},
        # Observed engine seed, not a user-selectable CLI --seed or independence claim.
        'observed_engine_seed': str(seed),
    }
    for name, field in (('lifetime_earned_gold','earnedGold'), ('champion_kills','kills'),
                        ('champion_deaths','deaths'), ('carried_gems','gems'),
                        ('unspent_gold','gold'), ('collected_gems','collectedGems'),
                        ('spent_gold','spentGold'), ('sale_refunds','saleRefunds')):
        metrics[name] = {side: sum(unsigned(c['metrics'][field]) for c in champions if c['team'] == team)
                         for team, side in SIDES.items()}
    for name, field in (('champion_damage_done','championDamageDone'),
                        ('champion_damage_taken','championDamageTaken'),
                        ('monster_damage_done','monsterDamageDone'),
                        ('monster_damage_taken','monsterDamageTaken')):
        values = [c['metrics'][field] for c in champions]
        require(all(type(v) in (int, float) and math.isfinite(v) and v >= 0 for v in values),
                'invalid damage metric')
        metrics[name] = {side: sum(c['metrics'][field] for c in champions if c['team'] == team)
                         for team, side in SIDES.items()}
    # Event absence is only evidence of zero when detailed capture is complete.
    suspensions = None
    if stats['diagnostics']['detailedCaptureComplete'] is True:
        for kind, name in (('fuelExhausted', 'fuel_suspensions_by_side'), ('gemLoss', 'bag_loss')):
            groups = [g for g in stats['events'] if g['kind'] == kind]
            covered = {g['owner']['id'] for g in groups if g['owner']['kind'] == 'champion'}
            require(covered == {c['id'] for c in champions}, 'incomplete event owners')
            totals = {'A': 0, 'B': 0}
            for group in groups:
                side = SIDES[group['owner']['team']]
                totals[side] += sum(unsigned(e['value']) for e in group['entries'])
            metrics[name] = totals
            if kind == 'fuelExhausted':
                suspensions = sum(totals.values())
    return sum(faults.values()), {k: {'available': True, 'value': v} for k, v in metrics.items()}, suspensions
