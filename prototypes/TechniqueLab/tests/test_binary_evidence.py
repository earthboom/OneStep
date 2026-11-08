"""Binary provenance dimensions are separate from retained-data arithmetic."""
import hashlib
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from analysis_evidence import add_expected, verify_binaries


class BinaryEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=os.environ.get('ONESTEP_TEST_ROOT'))
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.expected = {'Build/player.exe': hashlib.sha256(b'original').hexdigest().upper()}

    def test_missing_is_explicit_and_only_allowed_in_offline_mode(self):
        result = verify_binaries(self.root, self.expected)
        self.assertTrue(result['acceptable'])
        self.assertFalse(result['complete'])
        self.assertEqual(result['checks'][0]['status'], 'missing')
        self.assertFalse(verify_binaries(self.root, self.expected, require=True)['acceptable'])

    def test_matched_then_corrupted_binary_changes_result_without_cached_success(self):
        player = self.root/'Build/player.exe'
        player.parent.mkdir()
        player.write_bytes(b'original')
        self.assertTrue(verify_binaries(self.root, self.expected, require=True)['complete'])
        player.write_bytes(b'changed')
        result = verify_binaries(self.root, self.expected)
        self.assertFalse(result['acceptable'])
        self.assertEqual(result['checks'][0]['status'], 'mismatch')

    def test_unreadable_present_binary_is_not_treated_as_optional_missing(self):
        with patch.object(Path, 'open', side_effect=PermissionError('test unavailable')):
            result = verify_binaries(self.root, self.expected)
        self.assertFalse(result['acceptable'])
        self.assertEqual(result['checks'][0]['status'], 'unavailable')

    def test_expected_hashes_must_agree_across_runs(self):
        expected = {}
        add_expected(expected, 'Build/player.exe', 'a'*64)
        add_expected(expected, 'Build/player.exe', 'A'*64)
        with self.assertRaisesRegex(ValueError, 'Conflicting'):
            add_expected(expected, 'Build/player.exe', 'b'*64)

    def test_invalid_paths_and_hashes_do_not_become_missing_successes(self):
        for path in ('../outside', '/absolute', 'C:/absolute', 'Build/../../outside', 'Build\\player.exe'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                verify_binaries(self.root, {path: 'a'*64})
        with self.assertRaises(ValueError):
            add_expected({}, 'Build/player.exe', 'not-a-sha')


if __name__ == '__main__':
    unittest.main()
