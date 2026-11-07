"""Portable source identity and absence behavior through the actual CLI."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "sources.py"
CATALOG = SCRIPT.with_name("catalog.py")


class SourceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="onestep-sources-", dir=os.environ.get("ONESTEP_TEST_ROOT"))
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.project = self.base / "consumer"
        self.content = "Synthetic research evidence, not an original project document.\n".encode()
        self.digest = hashlib.sha256(self.content).hexdigest()
        self.sources = {"SRC-RESEARCH": {"project": "sample", "path": "research/근거.md", "sha256": self.digest},
                        "SRC-BEFORE": {"project": "sample", "path": "before.md", "sha256": None}}
        self.registry()

    def put(self, path, content):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content if isinstance(content, bytes) else content.encode("utf-8"))
        return path

    def registry(self):
        # JSON is a YAML subset; fixtures exercise the same Markdown metadata contract.
        body = "---\n" + json.dumps({"sources": self.sources}, ensure_ascii=False) + "\n---\n"
        body += "\n".join("\n## " + ident for ident in self.sources)
        self.put(self.project / "knowledge/sources.md", body)
        self.put(self.project / "knowledge/sources.kr.md", b"\xff\xfe")

    def configure(self, root):
        return self.put(self.project / "knowledge/sources.local.json", json.dumps({"sample": str(root)}))

    def cli(self, ident="SRC-RESEARCH"):
        run = subprocess.run([sys.executable, "-X", "utf8", str(SCRIPT), "resolve", "--project", str(self.project), "--id", ident],
                             capture_output=True, text=True, encoding="utf-8", timeout=15)
        self.assertTrue(run.stdout, run.stderr)
        return run.returncode, json.loads(run.stdout)

    def batch(self, ids, *extra):
        args = [sys.executable, "-B", "-X", "utf8", str(SCRIPT), "resolve", "--project", str(self.project)]
        for ident in ids:
            args += ["--id", ident]
        run = subprocess.run(args + list(extra), capture_output=True, text=True, encoding="utf-8", timeout=15)
        self.assertTrue(run.stdout, run.stderr)
        return run.returncode, json.loads(run.stdout)

    def test_multiple_ids_report_every_result_and_separate_access_from_identity(self):
        root = self.base / "originals"
        self.put(root / "research/근거.md", self.content)
        self.put(root / "before.md", "Current unversioned text")
        registry = (self.project / "knowledge/sources.md").read_bytes()
        code, result = self.batch(["SRC-RESEARCH", "SRC-BEFORE"], "--root", f"sample={root}")
        self.assertEqual(code, 1, result)
        self.assertEqual(result["requested_ids"], ["SRC-RESEARCH", "SRC-BEFORE"])
        self.assertEqual([x["source_id"] for x in result["results"]], result["requested_ids"])
        self.assertEqual([x["status"] for x in result["results"]], ["matched", "unversioned"])
        self.assertEqual([x["access_status"] for x in result["results"]], ["available", "available"])
        self.assertFalse(result["ok"])
        self.assertEqual(result["completed"], 2)
        self.assertFalse((self.project / "knowledge/sources.local.json").exists())
        self.assertEqual((self.project / "knowledge/sources.md").read_bytes(), registry)

    def test_invalid_middle_id_does_not_hide_other_results(self):
        root = self.base / "originals"
        self.put(root / "research/근거.md", self.content)
        self.put(root / "before.md", "Unversioned")
        ids = ["SRC-RESEARCH", "SRC-UNKNOWN", "SRC-BEFORE"]
        code, result = self.batch(ids, "--root", f"sample={root}")
        self.assertEqual(code, 2, result)
        self.assertEqual([x["source_id"] for x in result["results"]], ids)
        self.assertEqual([x["status"] for x in result["results"]], ["matched", "invalid", "unversioned"])
        self.assertEqual(result["completed"], 3)

    def test_single_id_keeps_shape_and_explicit_root_overrides_unused_settings(self):
        root = self.base / "authorized originals"
        self.put(root / "research/근거.md", self.content)
        settings = self.put(self.project / "knowledge/sources.local.json", "not json")
        code, result = self.batch(["SRC-RESEARCH"], "--root", f"sample={root}")
        self.assertEqual((code, result["source_id"], result["status"]), (0, "SRC-RESEARCH", "matched"))
        self.assertEqual(result["root_source"], "argument")
        self.assertEqual(result["access_status"], "available")
        self.assertEqual(result["identity_status"], "matched")
        self.assertNotIn("results", result)
        self.assertEqual(settings.read_text(encoding="utf-8"), "not json")

    def test_duplicate_ids_and_conflicting_roots_are_explicitly_invalid(self):
        code, result = self.batch(["SRC-RESEARCH", "src-research"])
        self.assertEqual((code, result["status"]), (2, "invalid"))
        self.assertIn("duplicate", result["message"].lower())
        code, result = self.batch(["SRC-RESEARCH"], "--root", "sample=relative")
        self.assertEqual((code, result["status"]), (2, "invalid"))
        code, result = self.batch(["SRC-RESEARCH"], "--root", f"sample={self.base}", "--root", f"sample={self.project}")
        self.assertEqual((code, result["status"]), (2, "invalid"))

    def test_relocation_changes_only_machine_root_and_preserves_evidence(self):
        original = (self.project / "knowledge/sources.md").read_bytes()
        root_a = self.base / "original source"
        file = self.put(root_a / "research/근거.md", self.content)
        self.configure(root_a)
        code, result = self.cli()
        self.assertEqual(code, 0, result)
        self.assertEqual(result["status"], "matched")
        self.assertEqual(result["observed_sha256"], self.digest)
        root_b = self.base / "다른 위치"
        root_a.rename(root_b)
        self.configure(root_b)
        code, result = self.cli()
        self.assertEqual(code, 0, result)
        self.assertEqual(Path(result["path"]), (root_b / "research/근거.md").resolve())
        self.assertEqual(result["source_id"], "SRC-RESEARCH")
        self.assertEqual((self.project / "knowledge/sources.md").read_bytes(), original)
        self.assertEqual((root_b / "research/근거.md").read_bytes(), self.content)

    def test_unconfigured_and_missing_are_distinct_and_never_ok(self):
        code, result = self.cli()
        self.assertEqual((code, result["status"], result["ok"]), (1, "unconfigured", False))
        self.configure(self.base / "absent root")
        code, result = self.cli()
        self.assertEqual((code, result["status"], result["ok"]), (1, "missing", False))
        self.assertFalse((self.base / "absent root").exists())

    def test_changed_research_hash_does_not_match(self):
        source = self.base / "source"
        self.put(source / "research/근거.md", self.content + b"changed")
        self.configure(source)
        code, result = self.cli()
        self.assertEqual((code, result["status"], result["ok"]), (1, "mismatch", False))

    def test_existing_unversioned_manuscript_cannot_prove_historical_identity(self):
        source = self.base / "source"
        self.put(source / "before.md", "Synthetic prior manuscript.")
        self.configure(source)
        code, result = self.cli("SRC-BEFORE")
        self.assertEqual((code, result["status"], result["ok"]), (1, "unversioned", False))
        self.assertEqual(result["expected_sha256"], None)
        self.assertTrue(result["observed_sha256"])

    def test_unknown_source_is_invalid_even_without_a_local_config(self):
        code, result = self.cli("SRC-NO-SUCH-SOURCE")
        self.assertEqual((code, result["status"]), (2, "invalid"))

    def test_invalid_local_config_is_not_treated_as_absence(self):
        for text in ("not json", '{"sample": "relative/path"}', '{"sample": "a", "sample": "b"}'):
            with self.subTest(text=text):
                self.put(self.project / "knowledge/sources.local.json", text)
                code, result = self.cli()
                self.assertEqual((code, result["status"]), (2, "invalid"))

    def test_registry_rejects_escape_translation_absolute_paths_and_bad_hash(self):
        for path in ("../outside.md", "proof.kr.md", "C:/elsewhere/proof.md", "/proof.md", "folder\\proof.md"):
            with self.subTest(path=path):
                self.sources["SRC-RESEARCH"]["path"] = path
                self.registry()
                self.assertEqual(self.cli()[0], 2)
        self.sources["SRC-RESEARCH"]["path"] = "proof.md"
        self.sources["SRC-RESEARCH"]["sha256"] = "invalid"
        self.registry()
        self.assertEqual(self.cli()[0], 2)

    def test_duplicate_registry_ids_are_invalid(self):
        self.put(self.project / "knowledge/sources.md", "---\nsources:\n  SRC-X: {}\n  SRC-X: {}\n---\n## SRC-X\n")
        self.assertEqual(self.cli("SRC-X")[0], 2)

    def test_resolved_symlink_cannot_escape_configured_root(self):
        source = self.base / "source"
        source.mkdir()
        outside = self.base / "outside"
        self.put(outside / "proof.md", self.content)
        self.sources["SRC-RESEARCH"]["path"] = "escape/proof.md"
        self.registry()
        try:
            (source / "escape").symlink_to(outside, target_is_directory=True)
        except OSError as exc:
            if os.name != "nt" or exc.winerror != 1314:
                raise
            # Windows junctions exercise the same resolved-root escape without symlink privilege.
            run = subprocess.run(["cmd", "/c", "mklink", "/J", str(source / "escape"), str(outside)], capture_output=True)
            self.assertEqual(run.returncode, 0, run.stderr)
        self.configure(source)
        code, result = self.cli()
        self.assertEqual((code, result["status"]), (2, "invalid"))


if __name__ == "__main__":
    unittest.main()
