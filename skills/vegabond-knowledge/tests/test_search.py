"""Consumer-level retrieval checks; expected IDs are independent of ranking code."""

import json
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import yaml


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
SCRIPT = SCRIPTS / "search.py"


class SearchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="onestep-search-", dir=os.environ.get("ONESTEP_TEST_ROOT"))
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def detail(self, ident, *, store="knowledge", domain="code", body="Contextual guidance.", **updates):
        meta = dict(id=ident, title="Resource review", summary="Inspect the applicable resource contract.",
                    kind="reference" if store == "knowledge" else "error", scope="Example project",
                    keywords=["resource"], status="active" if store == "knowledge" else "resolved",
                    checked_at=None)
        if store == "records":
            meta.update(trigger="Scheduling callback during shutdown", symptom="Callback accesses destroyed owner",
                        cause_status="confirmed", prevention="Await completion before cleanup", prevention_status="proposed")
        meta.update(updates)
        sections = ("Guidance", "Applicability and exceptions", "Checks", "Evidence") if store == "knowledge" else (
            "Expected and observed", "Cause and resolution", "Recheck and prevention", "Evidence")
        text = "---\n" + yaml.safe_dump(meta, allow_unicode=True, sort_keys=False) + "---\n\n"
        text += "\n\n".join(f"## {h}\n\n{body}" for h in sections) + "\n"
        path = self.root / store / domain / f"{ident}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        # Reading a translation would cause a decode failure.
        path.with_name(path.stem + ".kr.md").write_bytes(b"\xff\xfe")
        return path

    def cli(self, command="search", *args, expected=0):
        run = subprocess.run([sys.executable, "-B", str(SCRIPT), command, "--project", str(self.root), *args],
                             capture_output=True, text=True, encoding="utf-8", timeout=30)
        self.assertEqual(run.returncode, expected, run.stderr + run.stdout)
        self.assertTrue(run.stdout, run.stderr)
        return json.loads(run.stdout)

    def test_body_only_korean_expansion_and_line_locator(self):
        p = self.detail("K-POOL", title="Cost measurement", body="Measure allocation churn before introducing pooling.")
        self.detail("K-MEMORY", title="Memory ownership", keywords=["memory"])
        result = self.cli("search", "--query", "메모리 풀링")
        self.assertEqual(result["results"][0]["id"], "K-POOL")
        hit = result["results"][0]
        self.assertIn("pooling", hit["snippet"]["text"])
        self.assertIn("pooling", p.read_text(encoding="utf-8").splitlines()[hit["snippet"]["line"] - 1])
        self.assertIn("body", hit["matched_fields"])

    def test_both_stores_include_resolved_incidents_and_rank_specific_match(self):
        self.detail("K-RESOURCE")
        self.detail("R-SHUTDOWN", store="records")
        result = self.cli("search", "--query", "callback shutdown")
        self.assertEqual(result["results"][0]["id"], "R-SHUTDOWN")
        self.assertEqual(result["results"][0]["status"], "resolved")
        self.assertEqual(result["results"][0]["prevention_status"], "proposed")

    def test_korean_first_catalog_action_finds_english_incident(self):
        self.detail("R-BOOT", store="records", title="First build rejected future catalogs",
                    keywords=["bootstrap", "first-build", "catalog-planning"],
                    trigger="First build with root routing links to not-yet-generated catalogs")
        result = self.cli("search", "--query", "새 프로젝트 지식 카탈로그 최초 생성", "--store", "records")
        self.assertEqual(result["results"][0]["id"], "R-BOOT")

    def test_missing_yaml_keeps_structured_dependency_error(self):
        run = subprocess.run([sys.executable, "-S", "-B", str(SCRIPT), "search", "--project", str(self.root),
                              "--query", "resource"], capture_output=True, text=True, encoding="utf-8", timeout=30)
        self.assertEqual(run.returncode, 2)
        self.assertIn("PyYAML is required", json.loads(run.stdout)["error"])
        self.assertNotIn("Traceback", run.stderr)

    def test_observed_korean_paraphrases_retrieve_the_required_concept(self):
        self.detail("K-CONFIG", title="Avoid unexplained literals", keywords=["hardcoding"],
                    body="Classify embedded values before externalizing configuration.")
        self.detail("K-HIDE", title="Conceal changeable decisions", keywords=["information hiding"],
                    body="Callers should depend on a stable contract.")
        self.detail("K-KNOX", domain="fiction", title="Set up a fair solution", keywords=["fair-play"],
                    body="Give readers the relevant evidence before the revelation.")
        for query, domain, required in (
            ("숫자 값을 코드 곳곳에 직접 적어 두지 않고 바꾸기 쉽게 만들려면", "code", "K-CONFIG"),
            ("다른 파일이 내부 구현을 몰라도 쓰게 하려면", "code", "K-HIDE"),
            ("범인이 밝혀지기 전에 독자에게 판단 근거를 보여 주는 장면 구성", "fiction", "K-KNOX"),
            ("소스 여러 곳에 숫자를 고정해 놓았는데 조정하기 쉽게 바꾸고 싶어", "code", "K-CONFIG"),
            ("호출자가 내부 결정의 변화를 몰라도 되게 경계를 잡고 싶어", "code", "K-HIDE"),
            ("추리 장면에서 독자에게 실마리를 먼저 제시하고 싶어", "fiction", "K-KNOX"),
        ):
            with self.subTest(query=query):
                result = self.cli("search", "--query", query, "--domain", domain, "--limit", "3")
                self.assertIn(required, [h["id"] for h in result["results"]])
                self.assertTrue(result["inferred_concepts"])

    def test_concept_hints_require_conditions_not_single_generic_words(self):
        self.detail("K-CONFIG", keywords=["hardcoding"])
        for query in ("코드에서 숫자 값을 합산하는 방법", "CSV 숫자 값을 직접 읽는 방법",
                      "내부 구현을 자세히 설명해줘", "범인이 독자에게 편지를 보내는 장면",
                      "리소스 숫자 값을 직접 측정하는 방법", "코드에서 숫자 값을 직접 계산하는 방법",
                      "리소스 숫자 값을 고정하는 방법"):
            with self.subTest(query=query):
                result = self.cli("search", "--query", query)
                self.assertEqual(result["inferred_concepts"], [], query)

    def duplicate_candidates(self):
        body = "UObject GC determines reachability, not deterministic resource cleanup."
        self.detail("K-A-GC", title="UObject GC", keywords=["UObject", "GC"], body=body)
        for i in range(8):
            self.detail(f"K-B-COPY-{i}", title="UObject GC", keywords=["UObject", "GC"],
                        scope=f"Another project {i}", context={"engine": "another version"}, body=body)
        self.detail("K-Z-RESOURCE", title="Resource ownership", keywords=["cleanup"],
                    body="GC does not establish deterministic native resource ownership.")

    def test_identical_bodies_do_not_crowd_out_a_different_required_answer(self):
        self.duplicate_candidates()
        result = self.cli("search", "--query", "UObject GC", "--limit", "3")
        self.assertEqual(result["total_matches"], 10)
        self.assertIn("K-Z-RESOURCE", [h["id"] for h in result["results"]])
        group = result["results"][0]["similar_content"]
        self.assertEqual(group["other_matches"], 8)
        self.assertLessEqual(len(group["sample_ids"]), 3)
        self.assertTrue(group["truncated"])
        self.assertIn("scope", group["notice"])

    def test_diversity_preserves_all_candidates_and_raw_order_escape(self):
        self.duplicate_candidates()
        ids = []
        for offset in (0, 3, 6, 9):
            result = self.cli("search", "--query", "UObject GC", "--limit", "3", "--offset", str(offset))
            ids.extend(h["id"] for h in result["results"])
        self.assertEqual(len(ids), 10)
        self.assertEqual(len(set(ids)), 10)
        raw = self.cli("search", "--query", "UObject GC", "--limit", "3", "--all-variants")
        self.assertNotIn("K-Z-RESOURCE", [h["id"] for h in raw["results"]])
        exact = self.cli("search", "--query", "K-B-COPY-7", "--limit", "1")
        self.assertEqual(exact["results"][0]["id"], "K-B-COPY-7")
        self.assertEqual(exact["results"][0]["context"], {"engine": "another version"})

    def test_incoming_conflict_and_different_states_are_not_deferred_as_duplicates(self):
        for ident in ("K-A", "K-B", "K-C", "K-Z-CONFLICT", "K-Z-ENFORCED"):
            self.detail(ident, keywords=["sentinel"], body="Identical supporting text.",
                        status="enforced" if ident == "K-Z-ENFORCED" else "active")
        self.detail("K-NOTE", keywords=["other"], body="Separate counterevidence.",
                    relations={"conflicts_with": ["K-Z-CONFLICT"]})
        result = self.cli("search", "--query", "sentinel", "--limit", "3")
        self.assertEqual({h["id"] for h in result["results"]}, {"K-A", "K-Z-CONFLICT", "K-Z-ENFORCED"})
        self.assertIn("K-NOTE", [h["id"] for h in result["relations"]["related"]])

    def test_diversity_keeps_known_and_unknown_context_in_separate_groups(self):
        for ident in ("K-A-KNOWN", "K-B-KNOWN", "K-C-KNOWN"):
            self.detail(ident, keywords=["sentinel"], body="Same guidance.", context={"engine": "UE 5.8"})
        self.detail("K-Z-UNKNOWN", keywords=["sentinel"], body="Same guidance.")
        self.detail("K-OTHER", keywords=["sentinel"], body="Same guidance.", context={"engine": "UE 5.3"})
        result = self.cli("search", "--query", "sentinel", "--context", "engine=UE 5.8", "--limit", "2")
        self.assertEqual(result["total_matches"], 4)
        self.assertEqual([h["id"] for h in result["results"]], ["K-A-KNOWN", "K-Z-UNKNOWN"])
        self.assertIn("Unknown context engine", " ".join(result["results"][1]["caveats"]))

    def registered_source(self, expected=True):
        original = self.root / "originals/proof.md"
        original.parent.mkdir(parents=True, exist_ok=True)
        original.write_bytes(b"Authoritative original\n")
        data = {"sources": {"SRC-PROOF": {"project": "sample", "path": "proof.md",
                          "sha256": hashlib.sha256(original.read_bytes()).hexdigest() if expected else None}}}
        registry = self.root / "knowledge/sources.md"
        registry.parent.mkdir(parents=True, exist_ok=True)
        registry.write_text("---\n" + json.dumps(data) + "\n---\n\n## SRC-PROOF\n", encoding="utf-8")
        registry.with_name("sources.kr.md").write_bytes(b"\xff\xfe")
        self.detail("K-PROOF", body="Review retention. [Original](../sources.md#src-proof)")
        return original

    def test_search_marks_registered_originals_unchecked_without_reading_settings(self):
        self.registered_source()
        (self.root / "knowledge/sources.local.json").write_text("broken settings must not be read", encoding="utf-8")
        hit = self.cli("search", "--query", "retention")["results"][0]
        self.assertEqual(hit["source_checks"][0]["source_id"], "SRC-PROOF")
        self.assertEqual(hit["source_checks"][0]["status"], "not_checked")
        self.assertIn("not checked", " ".join(hit["caveats"]).lower())
        self.assertNotIn("observed_sha256", hit["source_checks"][0])

    def test_explicit_selected_source_check_is_fresh_even_with_warm_index(self):
        original = self.registered_source()
        args = ["--query", "retention", "--verify-sources", "--source-root", f"sample={original.parent}"]
        first = self.cli("search", *args)
        self.assertEqual(first["results"][0]["source_checks"][0]["status"], "matched")
        self.assertEqual(first["source_verification"]["checked"], 1)
        original.write_bytes(b"Changed original\n")
        second = self.cli("search", *args, expected=1)
        self.assertTrue(second["retrieval_ok"])
        self.assertFalse(second["source_verification"]["ok"])
        self.assertEqual(second["index"]["read_files"], 0)
        self.assertEqual(second["results"][0]["source_checks"][0]["status"], "mismatch")
        self.assertFalse((self.root / "knowledge/sources.local.json").exists())

    def test_source_check_distinguishes_unconfigured_from_accessible_unversioned(self):
        original = self.registered_source(expected=False)
        missing = self.cli("search", "--query", "retention", "--verify-sources", expected=1)
        self.assertEqual(missing["results"][0]["source_checks"][0]["status"], "unconfigured")
        live = self.cli("search", "--query", "retention", "--verify-sources", "--source-root", f"sample={original.parent}", expected=1)
        check = live["results"][0]["source_checks"][0]
        self.assertEqual((check["status"], check["access_status"]), ("unversioned", "available"))
        self.assertIsNone(check["expected_sha256"])

    def test_filters_keep_unknown_context_but_exclude_known_incompatibility(self):
        self.detail("K-58", keywords=["ownership"], context={"engine": "UE 5.8"})
        self.detail("K-53", keywords=["ownership"], context={"engine": "UE 5.3"})
        self.detail("K-UNKNOWN", keywords=["ownership"])
        self.detail("K-OTHER", keywords=["ownership"], domain="fiction")
        result = self.cli("search", "--query", "ownership", "--domain", "code", "--context", "engine=UE 5.8")
        self.assertEqual({h["id"] for h in result["results"]}, {"K-58", "K-UNKNOWN"})
        unknown = next(h for h in result["results"] if h["id"] == "K-UNKNOWN")
        self.assertIn("engine", " ".join(unknown["caveats"]))

    def test_superseded_default_and_explicit_state_filter(self):
        self.detail("K-OLD", status="superseded", keywords=["callback"])
        self.detail("R-OPEN", store="records", status="open")
        self.assertNotIn("K-OLD", [h["id"] for h in self.cli("search", "--query", "callback")["results"]])
        explicit = self.cli("search", "--query", "callback", "--status", "superseded")
        self.assertEqual([h["id"] for h in explicit["results"]], ["K-OLD"])

    def test_relations_cross_stores_incoming_conflicts_cycles_and_limits(self):
        self.detail("K-NEW", keywords=["cancel"], relations={"requires": ["K-BASE"], "supersedes": ["K-OLD"]})
        self.detail("K-BASE", relations={"requires": ["K-NEW"]})
        self.detail("K-OLD", status="superseded")
        self.detail("R-ISSUE", store="records", relations={"prevention": ["K-NEW"]})
        self.detail("K-CONFLICT", domain="fiction", relations={"conflicts_with": ["K-NEW"]})
        result = self.cli("related", "--id", "K-NEW", "--depth", "3")
        self.assertEqual({h["id"] for h in result["related"]}, {"K-BASE", "K-OLD", "R-ISSUE", "K-CONFLICT"})
        self.assertTrue(any(e["type"] == "conflicts_with" for e in result["edges"]))
        bounded = self.cli("related", "--id", "K-NEW", "--limit", "1")
        self.assertTrue(bounded["truncated"])

    def test_paginated_results_can_reach_late_conflicts(self):
        ids = [f"K-BASE-{i:03d}" for i in range(101)]
        self.detail("K-ROOT", relations={"requires": ids})
        for ident in ids:
            self.detail(ident)
        self.detail("K-Z-CONFLICT", relations={"conflicts_with": ["K-ROOT"]})
        first = self.cli("related", "--id", "K-ROOT", "--limit", "100")
        self.assertTrue(first["truncated"])
        last = self.cli("related", "--id", "K-ROOT", "--limit", "100", "--offset", "100")
        self.assertFalse(last["truncated"])
        self.assertIn("K-Z-CONFLICT", [h["id"] for h in last["related"]])
        page = self.cli("search", "--query", "resource", "--limit", "100", "--offset", "100")
        self.assertEqual(len(page["results"]), 3)

    def test_depth_two_pagination_preserves_cross_page_conflict_edges(self):
        self.detail("K-ROOT", relations={"requires": ["K-A"]})
        self.detail("K-A", relations={"conflicts_with": ["K-B"]})
        self.detail("K-B")
        pages = [self.cli("related", "--id", "K-ROOT", "--depth", "2", "--limit", "1", "--offset", str(i)) for i in (0, 1)]
        edges = [e for p in pages for e in p["edges"]]
        self.assertIn(dict(source="K-A", type="conflicts_with", target="K-B"), edges)

    def test_missing_relation_and_duplicate_ids_fail_without_partial_success(self):
        p = self.detail("K-ONE", relations={"requires": ["K-MISSING"]})
        result = self.cli("search", "--query", "resource", expected=2)
        self.assertFalse(result["ok"])
        self.assertIn("K-MISSING", json.dumps(result))
        p.unlink()
        self.detail("K-DUP")
        self.detail("K-DUP", domain="fiction")
        result = self.cli("search", "--query", "resource", expected=2)
        self.assertIn("duplicate", json.dumps(result).lower())

    def test_cache_refresh_update_delete_corruption_and_preserved_mtime(self):
        p = self.detail("K-ONE", keywords=["alpha"])
        first = self.cli("search", "--query", "alpha")
        self.assertEqual(first["index"]["read_files"], 1)
        self.assertEqual(self.cli("search", "--query", "alpha")["index"]["read_files"], 0)
        old = p.stat()
        p.write_text(p.read_text(encoding="utf-8").replace("alpha", "bravo"), encoding="utf-8")
        os.utime(p, ns=(old.st_atime_ns, old.st_mtime_ns))
        result = self.cli("search", "--query", "bravo", "--refresh")
        self.assertEqual([h["id"] for h in result["results"]], ["K-ONE"])
        p.unlink()
        self.assertEqual(self.cli("search", "--query", "bravo")["results"], [])
        cache = self.root / ".cache/onestep/search-v1.json"
        cache.write_text("truncated cache", encoding="utf-8")
        self.assertTrue(self.cli("search", "--query", "bravo")["ok"])

    def test_cache_malformed_json_object_is_rebuilt_not_treated_as_canonical(self):
        self.detail("K-ONE", keywords=["alpha"])
        self.cli("search", "--query", "alpha")
        cache = self.root / ".cache/onestep/search-v1.json"
        original = cache.read_text(encoding="utf-8")
        for corrupted in ([], {"not": "an index"}):
            cache.write_text(json.dumps(corrupted), encoding="utf-8")
            self.assertEqual(self.cli("search", "--query", "alpha")["index"]["read_files"], 1)
        saved = json.loads(original)
        next(iter(saved["documents"].values()))["meta"] = {}
        cache.write_text(json.dumps(saved), encoding="utf-8")
        self.assertEqual(self.cli("search", "--query", "alpha")["results"][0]["id"], "K-ONE")

    def test_scale_1000_entries_cold_warm_and_changed_file(self):
        for i in range(1000):
            self.detail(f"K-SCALE-{i:04d}", title=f"Case {i}",
                        body=f"Review sentinel-{i:04d} under its documented conditions. " + "Bounded contextual guidance. " * 30)
        cold = self.cli("search", "--query", "sentinel-0777", "--limit", "3")
        warm = self.cli("search", "--query", "sentinel-0777", "--limit", "3")
        self.assertEqual(cold["index"]["entries"], 1000)
        self.assertEqual([h["id"] for h in warm["results"]], ["K-SCALE-0777"])
        self.assertEqual(warm["index"]["read_files"], 0)
        p = self.root / "knowledge/code/K-SCALE-0777.md"
        p.write_text(p.read_text(encoding="utf-8").replace("sentinel-0777", "changed-sentinel-0777"), encoding="utf-8")
        changed = self.cli("search", "--query", "changed-sentinel-0777")
        self.assertEqual(changed["index"]["read_files"], 1)
        self.assertEqual(changed["results"][0]["id"], "K-SCALE-0777")
        print(json.dumps({"synthetic_entries": 1000, "cold_ms": cold["elapsed_ms"], "warm_ms": warm["elapsed_ms"],
                          "changed_ms": changed["elapsed_ms"], "warm_canonical_reads": warm["index"]["read_files"]}))

    def test_empty_query_bad_filter_and_missing_id_have_explicit_errors(self):
        self.cli("search", "--query", "   ", expected=2)
        self.cli("search", "--query", "x", "--context", "bad", expected=2)
        self.cli("related", "--id", "K-ABSENT", expected=2)

    def test_no_cache_does_not_write_and_unrelated_files_are_not_inputs(self):
        self.detail("K-ONE", keywords=["alpha"])
        (self.root / "knowledge/code/index.md").write_bytes(b"\xff")
        (self.root / "knowledge/code/.hidden.md").write_bytes(b"\xff")
        self.cli("search", "--query", "alpha", "--no-cache")
        self.assertFalse((self.root / ".cache").exists())

    def test_unavailable_cache_storage_and_optional_yaml_dates_do_not_block_search(self):
        self.detail("K-ONE", keywords=["alpha"], extra_date="unused")
        p = self.root / "knowledge/code/K-ONE.md"
        p.write_text(p.read_text(encoding="utf-8").replace("extra_date: unused", "extra_date: 2026-01-01"), encoding="utf-8")
        result = self.cli("search", "--query", "alpha")
        self.assertEqual(result["results"][0]["id"], "K-ONE")
        cache = self.root / ".cache/onestep/search-v1.json"
        cache.unlink()
        cache.mkdir()
        result = self.cli("search", "--query", "alpha")
        self.assertEqual(result["results"][0]["id"], "K-ONE")
        self.assertTrue(result["index"]["warning"])

    def test_exact_technical_identifier_keeps_language_suffix(self):
        for ident, language in (("K-C", "C"), ("K-CS", "C#"), ("K-CPP", "C++")):
            self.detail(ident, title=f"{language} resource contracts", keywords=[language])
        result = self.cli("search", "--query", "C++")
        self.assertEqual([h["id"] for h in result["results"]], ["K-CPP"])

    def test_unicode_separator_does_not_invent_editor_line_numbers(self):
        p = self.detail("K-ONE", body="Before\u2028sentinel-separator text.")
        hit = self.cli("search", "--query", "sentinel-separator")["results"][0]
        lines = p.read_text(encoding="utf-8").split("\n")
        self.assertIn("sentinel-separator", lines[hit["snippet"]["line"] - 1])

    def test_long_paragraph_excerpt_contains_the_actual_match(self):
        self.detail("K-ONE", body="x" * 500 + " sentinel-late is the relevant condition.")
        hit = self.cli("search", "--query", "sentinel-late")["results"][0]
        self.assertIn("sentinel-late", hit["snippet"]["text"])
        self.assertLessEqual(len(hit["snippet"]["text"]), 300)

    def test_excerpt_normalization_and_boundaries_preserve_actual_match(self):
        for scope, body, query, wanted in (
            ("composed", "e\u0301" * 400 + " sentinel-late", "sentinel-late", "sentinel-late"),
            ("boundary", "homeowner " + "x " * 300 + " ownership", "ownership", "ownership"),
        ):
            with self.subTest(scope=scope):
                self.detail("K-" + scope, body=body, keywords=["owner"], scope=scope)
                hit = self.cli("search", "--query", query, "--scope", scope)["results"][0]
                self.assertIn(wanted, hit["snippet"]["text"])

    def test_readonly_invocation_without_B_does_not_create_bytecode(self):
        self.detail("K-ONE", keywords=["alpha"])
        tool = self.root / "tool"
        tool.mkdir()
        for name in ("search.py", "catalog.py", "relations.py", "sources.py", "search_terms.json"):
            shutil.copyfile(SCRIPTS / name, tool / name)
        run = subprocess.run([sys.executable, str(tool / "search.py"), "search", "--project", str(self.root),
                              "--query", "alpha", "--no-cache"], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        self.assertFalse(list(tool.rglob("*.pyc")))
        self.assertFalse((self.root / ".cache").exists())

    def test_quality_evaluation_reports_missing_forbidden_and_unknown_coverage(self):
        self.detail("K-POOL", body="Measure pooling.")
        cases = self.root / "cases.json"
        cases.write_text(json.dumps({"cases": [
            {"name": "pool", "query": "풀링", "required": ["K-POOL"], "forbidden": [], "limit": 3},
            {"name": "negative", "query": "unknown-token", "required": [], "forbidden": ["K-POOL"], "limit": 3}
        ]}), encoding="utf-8")
        result = self.cli("evaluate", "--cases", str(cases))
        self.assertEqual(result["passed"], 2)
        self.assertEqual(result["required_recall"], 1.0)
        self.assertEqual(result["forbidden_hits"], 0)
        cases.write_text(json.dumps({"cases": [{"name": "miss", "query": "unknown-token", "required": ["K-POOL"]}]}), encoding="utf-8")
        result = self.cli("evaluate", "--cases", str(cases), expected=1)
        self.assertEqual(result["passed"], 0)
        self.assertEqual(result["required_recall"], 0.0)

    def test_catalog_checks_relations_even_when_target_is_in_another_store(self):
        self.detail("R-ONE", store="records")
        self.detail("K-ONE", relations={"derived_from": ["R-ONE"]})
        # Root routing/catalog creation is intentionally delegated to the existing helper.
        for store in ("knowledge", "records"):
            route = self.root / store / "index.md"
            route.write_text("# Domains\n\n[code](code/index.md)\n", encoding="utf-8")
            route.with_name("index.kr.md").write_bytes(b"\xff\xfe")
        run = subprocess.run([sys.executable, "-B", str(SCRIPTS / "catalog.py"), "build", "--project", str(self.root),
                              "--store", "knowledge", "--domain", "code"], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(run.returncode, 0, run.stdout)
        target = self.root / "records/code/R-ONE.md"
        target.unlink()
        run = subprocess.run([sys.executable, "-B", str(SCRIPTS / "catalog.py"), "check", "--project", str(self.root),
                              "--store", "knowledge", "--domain", "code"], capture_output=True, text=True, encoding="utf-8")
        self.assertNotEqual(run.returncode, 0)
        self.assertIn("relation", run.stdout.lower())

    def test_catalog_newline_equivalence_and_valid_yaml_relation_ids(self):
        self.detail("K-TARGET")
        self.detail("K-ONE", relations={"requires": ["K-TARGET"]})
        target = self.root / "knowledge/code/K-TARGET.md"
        target.write_text(target.read_text(encoding="utf-8").replace("id: K-TARGET", "id: 'K-TARGET' # stable ID"), encoding="utf-8")
        route = self.root / "knowledge/index.md"
        route.write_text("# Domains\n\n[code](code/index.md)\n", encoding="utf-8")
        route.with_name("index.kr.md").write_bytes(b"\xff\xfe")
        run = subprocess.run([sys.executable, "-B", str(SCRIPTS / "catalog.py"), "build", "--project", str(self.root)],
                             capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(run.returncode, 0, run.stdout)
        index = self.root / "knowledge/code/index.md"
        index.with_name("index.kr.md").write_bytes(b"\xff\xfe")
        index.write_bytes(index.read_bytes().replace(b"\n", b"\r\n"))
        run = subprocess.run([sys.executable, "-B", str(SCRIPTS / "catalog.py"), "check", "--project", str(self.root)],
                             capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(run.returncode, 0, run.stdout)


if __name__ == "__main__":
    unittest.main()
