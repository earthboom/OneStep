"""Exercise delivery checks from an independent working project."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


class FeedbackDeliveryTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name).resolve()
        self.work = root / "working project"
        self.work.mkdir()
        checkout = root / "OneStep checkout"
        self.inbox = checkout / "feedback"
        self.inbox.mkdir(parents=True)
        self.helper = checkout / "tools" / "check_feedback.py"
        self.helper.parent.mkdir()
        shutil.copyfile(Path(__file__).with_name(self.helper.name), self.helper)
        self.report = self.inbox / "2026-11-20-example.md"
        self.translation = self.report.with_suffix(".kr.md")

    def run_check(self, filename):
        return subprocess.run(
            [sys.executable, str(self.helper), filename], cwd=self.work,
            capture_output=True, text=True,
        )

    def check_states(self, english, korean):
        result = self.run_check(self.report.name)
        present = english == korean == "present"
        self.assertEqual(result.returncode, 0 if present else 1, result.stderr)
        self.assertEqual(json.loads(result.stdout), {
            "pair_present": present,
            "files": {str(self.report): english, str(self.translation): korean},
        })

    def test_preparation_partial_delivery_and_completed_retry(self):
        for path in (self.report, self.translation):
            (self.work / path.name).write_text("fixture", encoding="utf-8")
        self.check_states("missing", "missing")
        shutil.copyfile(self.work / self.report.name, self.report)
        self.check_states("present", "missing")
        self.translation.touch()
        self.check_states("present", "empty")
        self.translation.write_text("fixture", encoding="utf-8")
        self.check_states("present", "present")

    def test_translation_only_and_directory(self):
        self.translation.write_text("fixture", encoding="utf-8")
        self.check_states("missing", "present")
        self.report.mkdir()
        self.check_states("not a regular file", "present")

    def test_rejects_nonreports_and_paths_outside_inbox(self):
        for filename in ("README.md", self.translation.name, "../" + self.report.name,
                         str(self.work / self.report.name)):
            with self.subTest(filename=filename):
                self.assertEqual(self.run_check(filename).returncode, 2)


if __name__ == "__main__":
    unittest.main()
