#!/usr/bin/env python3
"""Separate trusted publisher loop; no model calls or direct central DB writes."""
import signal
import sys
import time

sys.path.insert(0, '/opt/battlecode')
from arena.common import lock
from arena.config import load
from arena.exploration import CLIThrottle, Explorer

stopping = False


def stop(*_):
    global stopping
    stopping = True


def main():
    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)
    config = load('/etc/battlecode/arena.json')
    with lock(config['root'] + '/official-exploration.lock'):
        explorer = Explorer(config)
        explorer.adopt_first()
        while not stopping:
            try:
                explorer.step()
            except CLIThrottle as exc:
                # Safe read commands may wait for an explicit server Retry-After.
                # A creation timeout/error still leaves UNKNOWN and blocks retries.
                explorer.state['official_retry_at'] = time.time() + exc.retry_after
                explorer.state['last_throttle'] = str(exc)[:1000]
                explorer.save()
                explorer.publish_status()
            except Exception as exc:
                # A private simulation must never stop because the website/login failed.
                if not getattr(exc,'creation_outcome_unknown',False):
                    explorer.state['blocked'] = str(exc)[:1000]
                explorer.save()
                explorer.publish_status()
            delay = min(5, max(1, int(explorer.state.get('next_create', 0) - time.time())))
            for _ in range(delay):
                if stopping:
                    break
                time.sleep(1)


if __name__ == '__main__':
    main()
