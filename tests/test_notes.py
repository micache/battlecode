"""Per-transaction history bounds and filesystem scope, no model/game calls."""
import base64
from pathlib import Path
import tempfile
import unittest

from arena.common import ArenaError
from arena.notes import apply_edits, decode_edits


def encoded(data):
    return base64.b64encode(data).decode()


class NoteEditsTests(unittest.TestCase):
    def test_bounds_apply_to_current_edits(self):
        with self.assertRaisesRegex(ArenaError, 'transaction'):
            decode_edits({f'{i}.txt':encoded(b'x') for i in range(129)})
        with self.assertRaisesRegex(ArenaError, 'edit bytes'):
            decode_edits({f'{i}.txt':encoded(b'x' * (256*1024)) for i in range(5)})
        with self.assertRaises(ArenaError):
            decode_edits({'a.txt':encoded(b'x' * (256*1024+1))})
        self.assertEqual(decode_edits({'NOTES.md':encoded(b'compact')}), {'NOTES.md':b'compact'})

    def test_rejects_unsafe_edits_and_conflicting_deletions(self):
        for notes, deleted in [({'../beta/NOTES.md':encoded(b'x')}, []),
                               ({'/tmp/escape.txt':encoded(b'x')}, []),
                               ({'payload.sh':encoded(b'x')}, []),
                               ({'a.txt':encoded(b'x')}, ['a.txt']),
                               ({}, ['a.txt','a.txt']), ({}, ['../beta.txt'])]:
            with self.subTest(notes=notes,deleted=deleted), self.assertRaises(ArenaError):
                decode_edits(notes, deleted)

    def test_apply_preserves_history_and_supports_explicit_file_directory_transition(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / 'history'
            root.mkdir()
            (root / 'keep.md').write_bytes(b'old evidence')
            (root / 'old.md').mkdir()
            (root / 'old.md/entry.txt').write_bytes(b'archived')
            apply_edits(root, {'old.md':b'new summary'}, ['old.md/entry.txt'])
            self.assertEqual((root / 'keep.md').read_bytes(), b'old evidence')
            self.assertEqual((root / 'old.md').read_bytes(), b'new summary')

    def test_inherited_symlink_cannot_redirect_a_note_write(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            root = base / 'history'
            root.mkdir()
            (root / 'escape').symlink_to(base, target_is_directory=True)
            with self.assertRaisesRegex(ArenaError, 'symlink'):
                apply_edits(root, {'escape/outside.txt':b'bad'})
            self.assertFalse((base / 'outside.txt').exists())
