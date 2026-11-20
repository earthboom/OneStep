"""Check the published stores, including provenance and required local links."""

import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[3]
SCRIPT = PROJECT / "skills/vegabond-knowledge/scripts/catalog.py"


class PublishedReferenceTests(unittest.TestCase):
    def test_published_stores_pass_strict_catalog_check(self):
        run = subprocess.run(
            [sys.executable, str(SCRIPT), "check", "--project", str(PROJECT), "--strict"],
            capture_output=True, text=True, timeout=30,
        )
        self.assertTrue(run.stdout, run.stderr)
        result = json.loads(run.stdout)
        self.assertEqual(run.returncode, 0, result)
        self.assertEqual(result["errors"], 0, result)


if __name__ == "__main__":
    unittest.main()
