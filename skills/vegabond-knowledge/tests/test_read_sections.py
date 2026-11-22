from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
from read_sections import matching_lines


class ReadSectionsTests(unittest.TestCase):
    def test_selects_original_lines_and_nested_sections(self):
        lines = ["# Guide", "Intro", "## Approval", "Rule", "### Exceptions",
                 "Legitimate exception", "## Pricing", "Prices", "## Recovery", "Retry"]
        selected = matching_lines(lines, re.compile("approval|exceptions|recovery", re.I))
        self.assertEqual(selected, [(3, "## Approval"), (4, "Rule"), (5, "### Exceptions"),
                                    (6, "Legitimate exception"), (9, "## Recovery"), (10, "Retry")])

    def test_ignores_fenced_headings(self):
        lines = ["# Guide", "~~~md", "## Approval", "fake example", "~~~",
                 "## Recovery ###", "actual original"]
        self.assertEqual(matching_lines(lines, re.compile(r"^Recovery$")),
                         [(6, "## Recovery ###"), (7, "actual original")])
        self.assertEqual(matching_lines(lines, re.compile("Approval")), [])

    def test_document_title_matches_only_the_intro_before_subsections(self):
        lines = ["# Operations guide", "Intro", "## Approval", "Rule", "## Pricing", "Prices"]
        self.assertEqual(matching_lines(lines, re.compile("operations|approval", re.I)),
                         [(1, "# Operations guide"), (2, "Intro"), (3, "## Approval"), (4, "Rule")])

    def test_top_level_chapters_keep_their_nested_sections(self):
        lines = ["# Setup", "Intro", "## Approval", "Rule", "# Recovery", "Retry"]
        self.assertEqual(matching_lines(lines, re.compile("Setup")),
                         [(1, "# Setup"), (2, "Intro"), (3, "## Approval"), (4, "Rule")])

    def test_cli_keeps_the_document_path_and_reports_output_over_budget(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "rules.md").write_text("# Guide\n\n## Recovery\nRetry once.\n", encoding="utf-8")
            command = [sys.executable, "-X", "utf8", "-B", str(SCRIPTS / "read_sections.py"),
                       "--project", directory, "--section", "rules.md", "Recovery"]
            result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", check=True)
            self.assertIn("rules.md\n3: ## Recovery\n4: Retry once.", result.stdout)
            capped = subprocess.run([*command, "--max-chars", "10"],
                                    capture_output=True, text=True, encoding="utf-8")
            self.assertNotEqual(capped.returncode, 0)
            self.assertNotIn("Retry once", capped.stdout)
            self.assertIn("rules.md:3-4", capped.stderr)

    def test_cli_rejects_human_only_translation_before_reading(self):
        with tempfile.TemporaryDirectory() as directory:
            command = [sys.executable, "-X", "utf8", "-B", str(SCRIPTS / "read_sections.py"),
                       "--project", directory, "--section", "policy.kr.md", "policy"]
            result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("translation", result.stderr)


if __name__ == "__main__":
    unittest.main()
