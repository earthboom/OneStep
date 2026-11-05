"""Behavior checks for catalog writes, retrieval data, and preservation boundaries."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import yaml


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "catalog.py"


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix="onestep-catalog-", dir=os.environ.get("ONESTEP_TEST_ROOT")))
        self.domain("knowledge", "fiction")

    def put(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def pair(self, path):
        # Deliberately unreadable as UTF-8: successful indexing must not load it.
        path.with_name(path.stem + ".kr.md").write_bytes(b"\xff\xfe")

    def domain(self, store, domain):
        route = self.root / store / "index.md"
        old = route.read_text(encoding="utf-8") if route.exists() else "# Domains\n\n"
        route = self.put(f"{store}/index.md", old + f"[{domain}]({domain}/index.md)\n")
        self.pair(route)
        index = self.put(f"{store}/{domain}/index.md", f"# {domain}\n\nKeep this project note.\n")
        self.pair(index)

    def detail(self, ident="K-1", domain="fiction", store="knowledge", **changes):
        meta = {"id": ident, "title": "Check viewpoint access", "summary": "For limited narration, check private claims.",
                "kind": "method" if store == "knowledge" else "error", "scope": "story-A", "keywords": ["viewpoint", "POV"],
                "status": "active" if store == "knowledge" else "open", "checked_at": None}
        meta.update(changes)
        sections = ("Guidance", "Applicability and exceptions", "Checks", "Evidence") if store == "knowledge" else (
            "Expected and observed", "Cause and resolution", "Recheck and prevention", "Evidence")
        body = "\n\n".join(f"## {heading}\n\nContextual content." for heading in sections)
        path = self.put(f"{store}/{domain}/{ident}.md", "---\n" + yaml.safe_dump(meta, sort_keys=False) + "---\n\n" + body + "\n")
        self.pair(path)
        return path

    def run_cli(self, command, *extra):
        result = subprocess.run([sys.executable, str(SCRIPT), command, "--project", str(self.root), *extra],
                                text=True, capture_output=True, timeout=15)
        self.assertTrue(result.stdout, result.stderr)
        return result.returncode, json.loads(result.stdout)

    def index(self, domain="fiction", store="knowledge", name="index.md"):
        return (self.root / store / domain / name).read_text(encoding="utf-8")

    def record(self, ident="R-1", domain="fiction", **changes):
        meta = {"trigger": "Drafting limited narration", "symptom": "Private decision asserted without access",
                "cause_status": "confirmed", "prevention": "Trace each private assertion to available evidence",
                "prevention_status": "proposed"}
        meta.update(changes)
        return self.detail(ident, domain=domain, store="records", **meta)

    def test_bootstrap_builds_multiple_stores_without_index_stubs(self):
        self.domain("knowledge", "code")
        self.domain("records", "code")
        self.domain("records", "fiction")
        entries = [self.detail("K-fiction"), self.detail("K-code", domain="code"),
                   self.record("R-fiction"), self.record("R-code", domain="code")]
        original = {p: p.read_bytes() for p in entries}
        indexes = [self.root / store / domain / "index.md"
                   for store in ("knowledge", "records") for domain in ("code", "fiction")]
        for index in indexes:
            index.unlink()
        code, result = self.run_cli("check", "--strict")
        self.assertEqual(code, 1)
        self.assertEqual(result["catalogs_written"], [])
        self.assertFalse(any(index.exists() for index in indexes))
        code, result = self.run_cli("build")
        self.assertEqual(code, 0, result["diagnostics"])
        self.assertEqual(set(result["catalogs_written"]), {p.relative_to(self.root).as_posix() for p in indexes})
        self.assertEqual(self.run_cli("check", "--strict")[0], 0)
        self.assertEqual(self.run_cli("build")[1]["catalogs_written"], [])
        self.assertEqual({p: p.read_bytes() for p in entries}, original)

    def test_bootstrap_still_rejects_unplanned_missing_files(self):
        self.detail()
        index = self.root / "knowledge/fiction/index.md"
        index.unlink()
        routing = self.root / "knowledge/index.md"
        original = routing.read_text(encoding="utf-8")
        for href in ("missing-proof.txt", "missing-domain/index.md", "fiction/archive.md"):
            with self.subTest(href=href):
                routing.write_text(original + f"\n[Missing]({href})\n", encoding="utf-8")
                code, result = self.run_cli("build")
                self.assertEqual(code, 1)
                self.assertIn("broken_reference", [d["code"] for d in result["diagnostics"]])
                self.assertEqual(result["catalogs_written"], [])
                self.assertFalse(index.exists())

    def test_bootstrap_does_not_exempt_unselected_catalogs(self):
        self.domain("knowledge", "code")
        self.detail("K-fiction")
        self.detail("K-code", domain="code")
        indexes = [self.root / "knowledge" / domain / "index.md" for domain in ("code", "fiction")]
        for index in indexes:
            index.unlink()
        code, result = self.run_cli("build", "--domain", "fiction")
        self.assertEqual(code, 1)
        self.assertEqual(result["catalogs_written"], [])
        self.assertFalse(any(index.exists() for index in indexes))
        self.assertEqual(self.run_cli("build")[0], 0)
        self.assertEqual(self.run_cli("check", "--strict")[0], 0)

    def test_bootstrap_resolves_planned_archive_and_detail_links(self):
        self.domain("knowledge", "code")
        source = self.detail("K-fiction")
        self.detail("K-retired", domain="code", status="superseded")
        source.write_text(source.read_text(encoding="utf-8") +
                          "\n[Code catalog](../code/index.md)\n[Prior guidance](../code/archive.md)\n", encoding="utf-8")
        for domain in ("code", "fiction"):
            (self.root / "knowledge" / domain / "index.md").unlink()
        code, result = self.run_cli("build")
        self.assertEqual(code, 0, result["diagnostics"])
        self.assertIn("knowledge/code/archive.md", result["catalogs_written"])
        archive = self.root / "knowledge/code/archive.md"
        self.assertIn("K-retired", archive.read_text(encoding="utf-8"))
        self.pair(archive)
        self.assertEqual(self.run_cli("check", "--strict")[0], 0)

    def test_record_signals_are_searchable_and_refresh_independently(self):
        self.domain("records", "fiction")
        entry = self.record(status="resolved")
        original = entry.read_bytes()
        self.assertEqual(self.run_cli("build")[0], 0)
        index = self.index(store="records")
        for signal in ("Drafting limited narration", "Private decision asserted without access",
                       "Trace each private assertion to available evidence", "confirmed", "proposed"):
            self.assertIn(signal, index)
        self.assertIn("resolved / unknown", index)
        self.assertNotIn("verified", index)
        self.assertEqual(entry.read_bytes(), original)
        entry.write_text(entry.read_text(encoding="utf-8").replace("prevention_status: proposed", "prevention_status: invalidated"), encoding="utf-8")
        self.assertEqual(self.run_cli("check")[0], 1)
        self.assertEqual(self.run_cli("build")[0], 0)
        self.assertIn("invalidated", self.index(store="records"))
        self.assertEqual(self.run_cli("check")[0], 0)

    def test_unknown_record_conditions_are_not_inferred(self):
        self.domain("records", "fiction")
        entry = self.record(trigger=None, cause_status="unknown", prevention=None, prevention_status="none")
        original = entry.read_bytes()
        self.assertEqual(self.run_cli("build")[0], 0)
        index = self.index(store="records")
        self.assertIn("Trigger: unknown", index)
        self.assertIn("Prevention [none]", index)
        self.assertIn("Cause: unknown", index)
        self.assertEqual(entry.read_bytes(), original)

    def test_invalid_record_signals_stop_writes(self):
        self.domain("records", "fiction")
        for changes in ({"trigger": []}, {"trigger": " "}, {"symptom": None}, {"symptom": ""},
                        {"cause_status": "proven"}, {"cause_status": []}, {"prevention": []},
                        {"prevention_status": "enforced"}, {"prevention_status": []},
                        {"prevention_status": "none"}, {"prevention": None},
                        {"prevention_status": "verified", "checked_at": None}):
            with self.subTest(changes=changes):
                self.record(**changes)
                code, result = self.run_cli("build")
                self.assertEqual(code, 1)
                self.assertEqual(result["catalogs_written"], [])
                self.assertIn("invalid_record_fields", [d["code"] for d in result["diagnostics"]])

    def test_partial_record_header_is_not_silently_legacy(self):
        self.domain("records", "fiction")
        self.detail("R-1", store="records", trigger="Drafting limited narration")
        code, result = self.run_cli("build")
        self.assertEqual(code, 1)
        self.assertIn("missing_record_fields", [d["code"] for d in result["diagnostics"]])
        self.assertEqual(result["catalogs_written"], [])

    def test_old_structured_records_preserve_metadata_with_migration_warning(self):
        self.domain("records", "fiction")
        entry = self.detail("R-old", store="records", status="resolved")
        original = entry.read_bytes()
        code, result = self.run_cli("build")
        self.assertEqual(code, 0)
        self.assertIn("legacy_record_fields", [d["code"] for d in result["diagnostics"]])
        self.assertIn("unrecorded", self.index(store="records"))
        self.assertIn("resolved / unknown", self.index(store="records"))
        self.assertEqual(self.run_cli("check")[0], 0)
        self.assertEqual(self.run_cli("check", "--strict")[0], 1)
        self.assertEqual(entry.read_bytes(), original)

    def test_record_catalog_lookup_across_domains(self):
        cases = [
            ("code", "R-CODE", "Computing a ratio with empty input", "division by zero", "Run zero-input regression", "suspected", "proposed", None),
            ("fiction", "R-FIC", "Drafting limited narration", "inaccessible private thought", "Trace information access", "confirmed", "proposed", None),
            ("presentation", "R-SLIDE", "Exporting a slide deck", "text clipped in final PDF", "Render every final slide", "confirmed", "verified", "2026-11-05"),
            ("planning", "R-PLAN", "Allocating a shared specialist", "weekly capacity exceeded", "Compare per-person weekly allocation", "unknown", "invalidated", None),
        ]
        for domain, ident, trigger, symptom, action, cause, state, checked in cases:
            self.domain("records", domain)
            self.record(ident, domain=domain, trigger=trigger, symptom=symptom, prevention=action,
                        cause_status=cause, prevention_status=state, checked_at=checked, scope=f"project-{domain}; revision-B")
        self.assertEqual(self.run_cli("build")[0], 0)
        for domain, ident, trigger, symptom, action, cause, state, checked in cases:
            catalog = self.index(domain, store="records")
            for query in (trigger, symptom):
                matches = [row for row in catalog.splitlines() if query in row]
                self.assertEqual(len(matches), 1)
                self.assertIn(ident, matches[0])
                self.assertIn(action, matches[0])
                self.assertIn(f"project-{domain}; revision-B", matches[0])
                self.assertIn(f"Prevention [{state}]", matches[0])
        self.assertEqual(self.run_cli("check", "--strict")[0], 0)

    def test_projection_staleness_and_read_only_check(self):
        entry = self.detail(summary="Apply the current source", context={"viewpoint": "limited"})
        before = entry.read_bytes()
        self.assertEqual(self.run_cli("build")[0], 0)
        first = self.index()
        self.assertIn("Apply the current source", first)
        self.assertIn('"viewpoint": "limited"', first)
        self.assertIn("Keep this project note.", first)
        self.assertEqual(self.run_cli("check")[0], 0)
        entry.write_text(entry.read_text(encoding="utf-8").replace("Apply the current source", "Use revised source"), encoding="utf-8")
        changed = entry.read_bytes()
        code, result = self.run_cli("check")
        self.assertEqual(code, 1)
        self.assertIn("stale_catalog", [d["code"] for d in result["diagnostics"]])
        self.assertEqual(self.index(), first)
        self.assertEqual(entry.read_bytes(), changed)
        self.assertNotEqual(before, changed)
        self.assertEqual(self.run_cli("build")[0], 0)
        self.assertIn("Use revised source", self.index())
        self.assertEqual(self.run_cli("build")[1]["catalogs_written"], [])

    def test_archival_reactivation_and_stable_detail(self):
        old = self.detail("K-old", status="superseded")
        self.detail("K-current")
        before = old.read_bytes()
        self.assertEqual(self.run_cli("build")[0], 0)
        self.assertNotIn("[K-old]", self.index())
        archive = self.root / "knowledge/fiction/archive.md"
        self.assertIn("[K-old]", archive.read_text(encoding="utf-8"))
        self.assertEqual(old.read_bytes(), before)
        self.pair(archive)
        self.assertEqual(self.run_cli("check")[0], 0)
        old.write_text(old.read_text(encoding="utf-8").replace("status: superseded", "status: active"), encoding="utf-8")
        self.assertEqual(self.run_cli("build")[0], 0)
        self.assertIn("[K-old]", self.index())
        self.assertNotIn("[K-old]", archive.read_text(encoding="utf-8"))

    def test_legacy_metadata_preserved_without_inference(self):
        old = self.put("knowledge/fiction/old.md", "# Old topic\n\nA prose-only entry with no verified date.\n")
        self.pair(old)
        index = self.put("knowledge/fiction/index.md", "# Fiction\n\n| ID | Scope | Trigger | Status | Detail |\n| --- | --- | --- | --- | --- |\n| L-original | unusual-symptom | story-Z | active | [old](old.md) |\n")
        original = old.read_bytes()
        code, result = self.run_cli("build")
        self.assertEqual(code, 0)
        self.assertEqual(result["legacy_entries"], 1)
        self.assertIn("unusual-symptom", self.index())
        self.assertIn("unverified metadata", self.index())
        self.assertEqual(old.read_bytes(), original)
        self.assertEqual(self.run_cli("build")[1]["catalogs_written"], [])
        self.assertEqual(self.run_cli("check")[0], 0)
        self.assertEqual(self.run_cli("check", "--strict")[0], 1)

    def test_related_domain_reference_has_one_primary_entry(self):
        self.domain("knowledge", "presentation")
        self.detail("K-story")
        index = self.put("knowledge/presentation/index.md", "# Presentation\n\n| ID | Detail |\n| --- | --- |\n| K-story | [story](../fiction/K-story.md) |\n")
        self.assertEqual(self.run_cli("build")[0], 0)
        self.assertIn("../fiction/K-story.md", self.index("presentation"))
        self.assertEqual(self.run_cli("check")[0], 0)
        self.assertFalse((index.parent / "K-story.md").exists())

    def test_duplicate_ids_stop_all_catalog_writes(self):
        self.detail("K-1")
        self.detail("K-2", id="K-1")
        before = self.index()
        code, result = self.run_cli("build")
        self.assertEqual(code, 1)
        self.assertIn("duplicate_id", [d["code"] for d in result["diagnostics"]])
        self.assertEqual(self.index(), before)

    def test_invalid_metadata_is_diagnostic_not_crash(self):
        for changes in [{"keywords": None}, {"context": ["bad"]}, {"checked_at": "yesterday"}, {"status": "done"}]:
            with self.subTest(changes=changes):
                self.detail(**changes)
                code, result = self.run_cli("build")
                self.assertEqual(code, 1)
                self.assertGreater(result["errors"], 0)
                self.assertEqual(result["catalogs_written"], [])

    def test_body_schema_and_reference_failures_stop_writes(self):
        entry = self.detail()
        entry.write_text(entry.read_text(encoding="utf-8").replace("## Checks", "## Not checks") + "\n[proof](missing.log)\n", encoding="utf-8")
        code, result = self.run_cli("build")
        self.assertEqual(code, 1)
        kinds = [d["code"] for d in result["diagnostics"]]
        self.assertIn("missing_section", kinds)
        self.assertIn("broken_reference", kinds)
        self.assertEqual(result["catalogs_written"], [])

    def test_preserved_catalog_notes_and_routing_links_are_checked(self):
        self.detail()
        self.assertEqual(self.run_cli("build")[0], 0)
        for relative in ("knowledge/fiction/index.md", "knowledge/index.md"):
            with self.subTest(relative=relative):
                path = self.root / relative
                original = path.read_text(encoding="utf-8")
                changed = "[Missing evidence](missing-proof.txt)\n\n" + original
                path.write_text(changed, encoding="utf-8")
                try:
                    code, result = self.run_cli("check", "--strict")
                    self.assertEqual(code, 1)
                    self.assertIn("broken_reference", [d["code"] for d in result["diagnostics"]])
                    code, result = self.run_cli("build")
                    self.assertEqual(code, 1)
                    self.assertEqual(result["catalogs_written"], [])
                    self.assertEqual(path.read_text(encoding="utf-8"), changed)
                finally:
                    path.write_text(original, encoding="utf-8")

    def test_translations_are_existence_only_and_build_is_preparation(self):
        entry = self.detail()
        entry.with_name(entry.stem + ".kr.md").unlink()
        self.assertEqual(self.run_cli("build")[0], 0)
        code, result = self.run_cli("check")
        self.assertEqual(code, 1)
        self.assertIn("missing_translation", [d["code"] for d in result["diagnostics"]])
        self.pair(entry)
        self.assertEqual(self.run_cli("check")[0], 0)

    def test_record_states_and_unknown_check_date(self):
        self.domain("records", "fiction")
        self.detail("R-1", store="records", status="open", kind="hypothesis")
        self.assertEqual(self.run_cli("build")[0], 0)
        self.assertIn("open / unknown", self.index(store="records"))
        self.assertEqual(self.run_cli("check")[0], 0)

    def test_selected_domain_does_not_load_unrelated_invalid_entry(self):
        self.domain("knowledge", "code")
        self.detail()
        self.put("knowledge/code/bad.md", "---\ninvalid: [\n---\n")
        self.assertEqual(self.run_cli("build", "--domain", "fiction")[0], 0)
        self.assertEqual(self.run_cli("check", "--domain", "fiction")[0], 0)

    def test_missing_fields_and_duplicate_header_keys(self):
        entry = self.detail()
        text = entry.read_text(encoding="utf-8")
        entry.write_text(text.replace("summary: For limited narration, check private claims.\n", ""), encoding="utf-8")
        self.assertEqual(self.run_cli("build")[0], 1)
        entry.write_text(text.replace("status: active", "status: active\nstatus: superseded"), encoding="utf-8")
        code, result = self.run_cli("build")
        self.assertEqual(code, 1)
        self.assertIn("invalid_header", [d["code"] for d in result["diagnostics"]])

    def test_markdown_examples_are_not_live_references(self):
        entry = self.detail()
        body = entry.read_text(encoding="utf-8")
        entry.write_text(body + "\n```markdown\n[example](not-a-real-source.md)\n```\n\n`[inline](also-not-a-source.md)`\n", encoding="utf-8")
        self.assertEqual(self.run_cli("build")[0], 0)

    def test_angle_wrapped_reference_and_external_url_do_not_crash(self):
        entry = self.detail()
        self.put("sources/proof (draft).txt", "Evidence from a controlled check.\n")
        entry.write_text(entry.read_text(encoding="utf-8") + '\n[proof](<../../sources/proof (draft).txt>)\n[external](http://[)\n', encoding="utf-8")
        self.assertEqual(self.run_cli("build")[0], 0)


if __name__ == "__main__":
    unittest.main()
