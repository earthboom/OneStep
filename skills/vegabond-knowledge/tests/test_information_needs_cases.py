"""Fixture integrity only; semantic request-to-application judgment is separate."""

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


HERE = Path(__file__).parent / "information-needs"
spec = importlib.util.spec_from_file_location("prepare_information_cases", HERE / "prepare.py")
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)


class InformationCaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="onestep-needs-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.cases = json.loads((HERE / "cases.json").read_text(encoding="utf-8"))["cases"]

    def test_prepared_projects_use_actual_catalog_and_search_without_answer_key(self):
        from catalog import Catalogs
        from search import load_index, search
        for case in self.cases:
            with self.subTest(case=case["id"]):
                project = self.root / case["id"]
                fixture.prepare(project, case)
                result = Catalogs(project, "check", True).run(("knowledge", "records"), [])
                self.assertTrue(result["ok"], result)
                docs, _ = load_index(project, no_cache=True)
                self.assertEqual({d["meta"]["id"] for d in docs}, {e["id"] for e in case["entries"]})
                self.assertFalse((project / "rubric.json").exists())
                self.assertFalse((project / "cases.json").exists())
                self.assertEqual(search(docs, "nonexistent-query")["results"], [])

    def test_preparation_never_overwrites_existing_project(self):
        project = self.root / "case"
        fixture.prepare(project, self.cases[0])
        original = (project / "request.md").read_bytes()
        with self.assertRaises(ValueError):
            fixture.prepare(project, self.cases[0])
        self.assertEqual((project / "request.md").read_bytes(), original)

    def test_fixture_paths_cannot_escape_project(self):
        with self.assertRaises(ValueError):
            fixture.inside(self.root, "../outside.md")

    def test_rubric_covers_inputs_but_is_not_a_semantic_automated_test(self):
        rubric = json.loads((HERE / "rubric.json").read_text(encoding="utf-8"))["cases"]
        self.assertEqual(set(rubric), {c["id"] for c in self.cases})
        for case in self.cases:
            self.assertNotIn("required", case)
            self.assertNotIn("query", case)
            self.assertTrue(rubric[case["id"]]["essential_questions"])
            self.assertTrue(rubric[case["id"]]["critical_failures"])


if __name__ == "__main__":
    unittest.main()
