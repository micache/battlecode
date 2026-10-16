"""Command/identity checks only; namespace enforcement is tested on the real host."""
from pathlib import Path
import tempfile
import unittest

from arena.colab_sandbox import arguments, disk_usage, process_identity, validate
from arena.common import ArenaError


class ColabTests(unittest.TestCase):
    def test_explicit_backend_and_minimal_mounts(self):
        args = arguments('/opt/battlecode-toolchain', '/tmp/project', '/tmp/output', ['/toolchain/bin/cambc', '--version'])
        for flag in ('--unshare-all', '--die-with-parent', '--clearenv', '--remount-ro', '--nproc=128:128'):
            self.assertIn(flag, args)
        self.assertNotIn('/home/bc-alpha', args)
        self.assertNotIn('/home/bc-beta', args)
        self.assertNotIn('/home/bc-arena/.ssh', args)
        with self.assertRaises(ArenaError):
            validate({}, {})

    def test_pid_identity_and_disk_accounting(self):
        import os
        self.assertEqual(process_identity(os.getpid())['uid'], os.getuid())
        self.assertIsNone(process_identity(999999999))
        with tempfile.TemporaryDirectory() as temp:
            (Path(temp) / 'one').write_bytes(b'123')
            (Path(temp) / 'link').symlink_to('one')
            self.assertEqual(disk_usage([temp]), 3)
