"""Project-local lexical retrieval, ID traversal and repeatable quality evaluation.

Markdown is authoritative. The disposable cache never reads human translations,
external originals, or generated catalogs. No network, model, or vector service.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import time
import unicodedata
from urllib.parse import unquote, urlsplit

# A read-only CLI must not create local/dependency bytecode on first import.
sys.dont_write_bytecode = True

from catalog import Catalogs, human_file, yaml, LINK, visible_markdown
from relations import relation_edges, validate_relations
if yaml is not None:
    from sources import SourceRegistry, SourceError, parse_roots


CACHE = Path(".cache/onestep/search-v1.json")
HERE = Path(__file__).resolve().parent
WEIGHTS = {"id": 18, "title": 10, "keywords": 9, "trigger": 9, "symptom": 9,
           "summary": 6, "prevention": 6, "scope": 3, "context": 2, "body": 1}
TOKEN = re.compile(r"[\w]+(?:(?:[./-][\w]+)|(?:::[\w]+))*(?:\+\+|#)?", re.UNICODE)
SEARCH_META = set(WEIGHTS) - {"body"} | {"status", "checked_at", "kind", "relations", "cause_status", "prevention_status"}


def normalized(value):
    return unicodedata.normalize("NFKC", str(value)).casefold()


def term_match(text, term):
    if re.search(r"[가-힣]", term):
        return re.search(re.escape(term), text)
    return re.search(r"(?<!\w)" + re.escape(term) + r"(?!\w)", text)


def contains(text, term):
    return term_match(text, term) is not None


def query_groups(query):
    text = normalized(query).strip()
    if not text:
        raise ValueError("query must not be empty")
    config = json.loads((HERE / "search_terms.json").read_text(encoding="utf-8"))
    groups, covered = [], set()
    tokens = TOKEN.findall(text)
    for aliases in config["groups"]:
        aliases = [normalized(a) for a in aliases]
        found = [a for a in aliases if contains(text, a)]
        if found:
            groups.append(aliases)
            for token in tokens:
                if any(contains(token, a) or contains(a, token) for a in found):
                    covered.add(token)
    stop = set(config["stopwords"])
    groups.extend([t] for t in dict.fromkeys(tokens) if t not in covered and t not in stop)
    if not groups:
        raise ValueError("query has no searchable terms")
    return groups


def safe_path(project, path):
    if (not path.resolve().is_relative_to(project) or path.is_symlink()
            or getattr(path, "is_junction", lambda: False)()):
        raise ValueError(f"linked or outside-project path: {path}")


def canonical_files(project):
    for store in ("knowledge", "records"):
        base = project / store
        if not base.exists():
            continue
        safe_path(project, base)
        for current, dirs, names in os.walk(base, followlinks=False):
            current = Path(current)
            kept = []
            for name in sorted(dirs):
                if name.startswith("."):
                    continue
                path = current / name
                safe_path(project, path)
                kept.append(name)
            dirs[:] = kept
            if current == base:
                continue  # source registry and routing files are not entries
            for name in sorted(names):
                path = current / name
                if (name.startswith(".") or path.suffix.lower() != ".md" or human_file(path)
                        or name.lower() in {"index.md", "archive.md"}):
                    continue
                safe_path(project, path)
                yield path, store, path.relative_to(base).parts[0]


def usable_cache(saved, project, signature):
    """Reject malformed disposable snapshots before treating any row as a hit."""
    if not isinstance(saved, dict) or saved.get("signature") != signature or saved.get("project") != str(project):
        return {}
    docs = saved.get("documents")
    if not isinstance(docs, dict):
        return {}
    for path, doc in docs.items():
        if not isinstance(doc, dict) or not isinstance(doc.get("meta"), dict):
            return {}
        meta = doc["meta"]
        if any(not isinstance(meta.get(k), str) for k in ("id", "title", "summary", "scope", "status", "kind")):
            return {}
        if "checked_at" not in meta or not isinstance(meta.get("keywords"), list) or validate_relations(meta):
            return {}
        if (doc.get("path") != path or doc.get("store") not in {"knowledge", "records"}
                or not isinstance(doc.get("domain"), str) or not isinstance(doc.get("body"), str)
                or not isinstance(doc.get("body_line"), int) or doc["body_line"] < 1
                or not isinstance(doc.get("stamp"), list) or len(doc["stamp"]) != 2
                or any(not isinstance(v, int) for v in doc["stamp"])
                or not isinstance(doc.get("sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", doc["sha256"])):
            return {}
    return docs


def load_index(project, *, no_cache=False, refresh=False):
    """Stat unchanged files; parse/hash changed files. --refresh bypasses stamps."""
    started = time.perf_counter()
    project = project.resolve()
    cache_path = project / CACHE
    signature = hashlib.sha256(b"".join((HERE / n).read_bytes() for n in (
        "search.py", "catalog.py", "relations.py", "sources.py", "search_terms.json"))).hexdigest()
    cached = {}
    cache_warning = None
    if not no_cache and cache_path.exists():
        for ancestor in (project / ".cache", cache_path.parent, cache_path):
            safe_path(project, ancestor)
        try:
            saved = json.loads(cache_path.read_text(encoding="utf-8"))
            cached = usable_cache(saved, project, signature)
        except (ValueError, KeyError, TypeError, UnicodeError):
            cached = {}  # a damaged disposable cache is rebuilt from originals
        except OSError as exc:
            cache_warning = f"Cache unavailable; results use canonical content: {exc}"
    docs, read_files = {}, 0
    checker = Catalogs(project, "check")
    for path, store, domain in canonical_files(project):
        relative = path.relative_to(project).as_posix()
        stat = path.stat()
        stamp = [stat.st_mtime_ns, stat.st_size]
        previous = cached.get(relative)
        if previous and previous["stamp"] == stamp and not refresh:
            docs[relative] = previous
            continue
        entry = checker.entry(path, store)
        read_files += 1
        if entry is None or (entry["meta"] is None and not entry["legacy"]):
            raise ValueError(f"invalid canonical entry: {relative}; " + json.dumps(checker.messages[-4:]))
        # Catalog parsing retains the exact body and original digest for retrieval.
        meta = entry["meta"] or dict(id="legacy:" + relative, title=path.stem, summary="Unstructured legacy entry",
                                     keywords=[], scope="unknown", status="unknown", checked_at=None, kind="unknown")
        meta = {k: v for k, v in meta.items() if k in SEARCH_META}
        docs[relative] = dict(meta=meta, body=entry["body"], body_line=entry["body_line"], sha256=entry["sha256"],
                              stamp=stamp, path=relative, store=store, domain=domain)
    errors = [m for m in checker.messages if m["level"] == "error"]
    if errors:
        raise ValueError("canonical validation failed: " + json.dumps(errors[:5]))
    documents = list(docs.values())
    relation_edges(documents)
    if not no_cache and (read_files or set(cached) != set(docs) or not cache_path.exists()):
        try:
            for ancestor in (project / ".cache", cache_path.parent, cache_path):
                safe_path(project, ancestor)
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            temporary = None
            try:
                with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=cache_path.parent,
                                                 prefix=".search-", suffix=".tmp", delete=False) as stream:
                    temporary = Path(stream.name)
                    json.dump(dict(signature=signature, project=str(project), documents=docs), stream, ensure_ascii=False)
                os.replace(temporary, cache_path)
            finally:
                if temporary is not None and temporary.exists():
                    temporary.unlink()
        except OSError as exc:
            cache_warning = f"Cache unavailable; results use canonical content: {exc}"
    return documents, dict(entries=len(documents), read_files=read_files, cached_files=len(documents) - read_files,
                           elapsed_ms=round((time.perf_counter() - started) * 1000, 3), warning=cache_warning)


def flatten(value):
    if isinstance(value, dict):
        return " ".join(f"{k} {v}" for k, v in value.items())
    if isinstance(value, list):
        return " ".join(map(str, value))
    return "" if value is None else str(value)


def excerpt(line, terms, budget=300):
    """Keep a literal source window around a hit, rather than a paragraph prefix."""
    text = normalized(line)
    positions = [match.start() for t in terms if (match := term_match(text, t)) is not None]
    target = min(positions, default=0)
    low, high = 0, len(line)
    while low < high:
        middle = (low + high) // 2
        if len(normalized(line[:middle])) <= target:
            low = middle + 1
        else:
            high = middle
    raw_offset = max(0, low - 1)
    start = max(0, raw_offset - 60)
    prefix = "…" if start else ""
    take = budget - len(prefix) - 1
    end = start + take
    return prefix + line[start:end] + ("…" if end < len(line) else "")


def compact(doc, caveats=()):
    meta = doc["meta"]
    result = {k: meta.get(k) for k in ("id", "title", "summary", "scope", "status", "checked_at", "kind")}
    result.update(path=doc["path"], store=doc["store"], domain=doc["domain"], sha256=doc["sha256"], caveats=list(caveats))
    for name in ("cause_status", "prevention_status", "prevention"):
        if name in meta:
            result[name] = meta[name]
    return result


def registered_ids(project, doc):
    """Only actual links to this project's registry are source requests."""
    ids = []
    for href in LINK.findall(visible_markdown(doc["body"])):
        href = href.strip()
        href = href[1:href.find(">")] if href.startswith("<") else re.split(r"\s+[\"']", href, maxsplit=1)[0]
        parsed = urlsplit(href)
        if parsed.scheme or not parsed.fragment:
            continue
        target = (project / doc["path"]).parent / unquote(parsed.path)
        if target.resolve() == project / "knowledge/sources.md":
            ident = unquote(parsed.fragment).upper()
            if ident not in ids:
                ids.append(ident)
    return ids


def annotate_sources(project, documents, result, *, verify=False, roots=None):
    """Describe returned references; open only explicitly requested originals.

    Results are never cached: an unchanged entry cannot hide a changed original.
    """
    project = project.resolve()
    by_id = {d["meta"]["id"].casefold(): d for d in documents}
    hits = result.get("results", []) + result.get("related", [])
    if result.get("relations"):
        hits += result["relations"]["related"]
    registry, registry_error, outcomes = None, None, {}
    for hit in hits:
        ids = registered_ids(project, by_id[hit["id"].casefold()])
        hit["evidence_notice"] = "checked_at is a recorded evidence date; sha256 identifies the entry, not live original-source verification. Other Evidence still needs review."
        checks = []
        for ident in ids:
            if ident not in outcomes:
                try:
                    if registry is None and registry_error is None:
                        try:
                            registry = SourceRegistry(project)
                        except SourceError as exc:
                            registry_error = str(exc)
                    if registry_error is not None:
                        raise SourceError(registry_error)
                    outcomes[ident] = registry.resolve(ident, roots) if verify else registry.describe(ident)
                except SourceError as exc:
                    outcomes[ident] = dict(ok=False, source_id=ident, status="invalid", access_status="not_checked",
                                           identity_status="not_checked", message=str(exc))
            checks.append(outcomes[ident])
        hit["source_checks"] = checks
        if checks:
            states = ", ".join(f"{r['source_id']}: {r['status']}" for r in checks)
            if not verify:
                hit["caveats"].append("Registered originals not checked; access and identity remain unverified. " + states)
            elif any(not r["ok"] for r in checks):
                hit["caveats"].append("Original-source verification is incomplete. " + states)
    values = list(outcomes.values())
    return dict(requested=verify, source_ids=list(outcomes), completed=len(values) if verify else 0,
                checked=sum(r["access_status"] == "available" for r in values),
                ok=all(r["ok"] for r in values) if verify and values else None,
                statuses=dict(Counter(r["status"] for r in values)),
                scope="Returned linked registry IDs only; no automatic web verification or historical-date updates.")


def context_filters(values):
    filters = {}
    for value in values:
        key, sep, desired = value.partition("=")
        if not sep or not key.strip() or not desired.strip():
            raise ValueError("context filter must be key=value")
        key = key.strip()
        if key in filters and filters[key] != desired.strip():
            raise ValueError(f"conflicting context filter: {key}")
        filters[key] = desired.strip()
    return filters


def search(documents, query, *, domains=(), store="both", statuses=(), scope=None, context=None,
           include_superseded=False, limit=5, offset=0):
    groups = query_groups(query)
    importance = [2 if any(" " in a and contains(normalized(query), a) for a in aliases) else 1 for aliases in groups]
    results = []
    for doc in documents:
        meta = doc["meta"]
        if domains and doc["domain"] not in domains:
            continue
        if store != "both" and doc["store"] != store:
            continue
        if statuses and meta["status"] not in statuses:
            continue
        if not statuses and not include_superseded and meta["status"] == "superseded":
            continue
        if scope and normalized(scope) not in normalized(meta["scope"]):
            continue
        caveats, incompatible = [], False
        actual = meta.get("context", {})
        for key, desired in (context or {}).items():
            if not isinstance(actual, dict) or key not in actual:
                caveats.append(f"Unknown context {key}; applicability needs checking")
            elif normalized(actual[key]) != normalized(desired):
                incompatible = True
        if incompatible:
            continue
        fields = {name: normalized(flatten(meta.get(name))) for name in WEIGHTS if name != "body"}
        fields["body"] = normalized(doc["body"])
        matched_fields, matched_terms, score, matched_groups, covered_weight = set(), set(), 0, 0, 0
        for aliases, weight in zip(groups, importance):
            weights = []
            for field, content in fields.items():
                found = [a for a in aliases if contains(content, a)]
                if found:
                    matched_fields.add(field)
                    matched_terms.update(found)
                    weights.append(WEIGHTS[field])
            if weights:
                matched_groups += 1
                covered_weight += weight
                score += max(weights) * weight
        if not matched_groups:
            continue
        # Coverage dominates repeated boilerplate; timestamps are not relevance.
        score += 30 * covered_weight / sum(importance)
        if meta["status"] == "unknown":
            caveats.append("Legacy metadata is unknown; inspect the original before applying")
        hit = compact(doc, caveats)
        snippet = None
        for line_offset, line in enumerate(doc["body"].split("\n")):
            if any(contains(normalized(line), t) for t in matched_terms):
                snippet = dict(line=doc["body_line"] + line_offset, text=excerpt(line, matched_terms))
                break
        if snippet is None:
            snippet = dict(line=1, text=f"Metadata match: {', '.join(sorted(matched_fields))}; {meta['summary']}"[:300])
        hit.update(score=round(score, 3), matched_fields=sorted(matched_fields), matched_terms=sorted(matched_terms),
                   query_coverage=f"{matched_groups}/{len(groups)}", snippet=snippet)
        results.append(hit)
    results.sort(key=lambda h: (-h["score"], len(h["caveats"]), h["id"].casefold()))
    return dict(results=results[offset:offset + limit], total_matches=len(results), offset=offset,
                truncated=len(results) > offset + limit,
                expanded_terms=groups,
                gap=None if results else "No lexical match under these filters; try alternate terms or a broader scope. Absence is not proved.")


def related(documents, ids, *, depth=1, limit=10, offset=0):
    by_id, edges = relation_edges(documents)
    roots = set()
    for ident in ids:
        if ident.casefold() not in by_id:
            raise ValueError(f"unknown entry ID: {ident}")
        roots.add(by_id[ident.casefold()]["meta"]["id"])
    visited, frontier, used_edges = set(roots), set(roots), []
    for _ in range(depth):
        following = set()
        for edge in edges:
            if edge["source"] in frontier or edge["target"] in frontier:
                if edge not in used_edges:
                    used_edges.append(edge)
                following.update((edge["source"], edge["target"]))
        frontier = following - visited
        visited.update(frontier)
        if not frontier:
            break
    ids = sorted(visited - roots)
    page = ids[offset:offset + limit]
    chosen = set(page)
    return dict(related=[compact(by_id[i.casefold()], ["Relation candidate; verify scope and source before applying"])
                         for i in page],
                edges=[e for e in used_edges if e["source"] in chosen or e["target"] in chosen
                       or (e["source"] in roots and e["target"] in roots)],
                total_related=len(ids), offset=offset, truncated=len(ids) > offset + limit)


def evaluate(documents, cases):
    if not isinstance(cases, list) or not cases:
        raise ValueError("evaluation requires a nonempty cases list")
    outcomes, required_total, found_total, forbidden_total = [], 0, 0, 0
    for case in cases:
        started = time.perf_counter()
        result = search(documents, case["query"], domains=case.get("domains", ()), store=case.get("store", "both"),
                        statuses=case.get("statuses", ()), scope=case.get("scope"), context=case.get("context", {}),
                        include_superseded=case.get("include_superseded", False), limit=case.get("limit", 5))
        actual = {h["id"] for h in result["results"]}
        required = set(case.get("required", ()))
        forbidden = set(case.get("forbidden", ()))
        missing, bad = sorted(required - actual), sorted(forbidden & actual)
        required_total += len(required)
        found_total += len(required & actual)
        forbidden_total += len(bad)
        outcomes.append(dict(name=case["name"], passed=not missing and not bad, missing=missing, forbidden_hits=bad,
                             returned=[h["id"] for h in result["results"]],
                             snippets_characters=sum(len(h["snippet"]["text"]) for h in result["results"]),
                             elapsed_ms=round((time.perf_counter() - started) * 1000, 3)))
    return dict(cases=outcomes, passed=sum(c["passed"] for c in outcomes), total=len(outcomes),
                required_recall=round(found_total / required_total, 4) if required_total else None,
                forbidden_hits=forbidden_total,
                limitation="Recall covers only declared required IDs; forbidden-hit checks are not a general precision estimate.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("search", "related", "evaluate"))
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--query")
    parser.add_argument("--domain", action="append", default=[])
    parser.add_argument("--store", choices=("knowledge", "records", "both"), default="both")
    parser.add_argument("--status", action="append", default=[])
    parser.add_argument("--scope")
    parser.add_argument("--context", action="append", default=[])
    parser.add_argument("--include-superseded", action="store_true")
    parser.add_argument("--id", action="append", default=[])
    parser.add_argument("--depth", type=int, default=1)
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--no-cache", action="store_true")
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--cases", type=Path)
    parser.add_argument("--verify-sources", action="store_true", help="Check linked registered originals for returned hits")
    parser.add_argument("--source-root", action="append", default=[], help="Authorized project=absolute-path for this call")
    args = parser.parse_args()
    try:
        if yaml is None:
            raise ValueError("PyYAML is required; use the existing catalog runtime")
        if not args.project.is_dir():
            raise ValueError("--project must be an existing directory")
        if not 1 <= args.limit <= 100 or not 0 <= args.depth <= 3:
            raise ValueError("limit must be 1..100 and depth 0..3")
        if args.offset < 0:
            raise ValueError("offset must be nonnegative")
        if args.command == "search" and args.query is None:
            raise ValueError("search requires --query")
        if args.command == "related" and not args.id:
            raise ValueError("related requires --id")
        if args.command == "evaluate" and args.cases is None:
            raise ValueError("evaluate requires --cases")
        if args.command == "evaluate" and (args.verify_sources or args.source_root):
            raise ValueError("Source checks apply to search/related, not ranking evaluation")
        if args.source_root and not args.verify_sources:
            raise ValueError("--source-root requires --verify-sources")
        roots = parse_roots(args.source_root)
        filters = context_filters(args.context)
        started = time.perf_counter()
        documents, stats = load_index(args.project, no_cache=args.no_cache, refresh=args.refresh)
        if args.command == "search":
            result = search(documents, args.query, domains=args.domain, store=args.store, statuses=args.status,
                            scope=args.scope, context=filters, include_superseded=args.include_superseded,
                            limit=args.limit, offset=args.offset)
            ids = [h["id"] for h in result["results"]]
            result["relations"] = related(documents, ids, depth=args.depth, limit=args.limit) if ids else None
        elif args.command == "related":
            result = related(documents, args.id, depth=args.depth, limit=args.limit, offset=args.offset)
        else:
            if human_file(args.cases):
                raise ValueError("human translations are not evaluation inputs")
            result = evaluate(documents, json.loads(args.cases.read_text(encoding="utf-8"))["cases"])
        passed = args.command != "evaluate" or result["passed"] == result["total"]
        invalid_source = False
        if args.command != "evaluate":
            verification = annotate_sources(args.project, documents, result, verify=args.verify_sources, roots=roots)
            result["source_verification"] = verification
            result["retrieval_ok"] = True
            invalid_source = verification["statuses"].get("invalid", 0) > 0
            passed = not invalid_source and verification["ok"] is not False
        print(json.dumps(dict(ok=passed, command=args.command, index=stats,
                              elapsed_ms=round((time.perf_counter() - started) * 1000, 3), **result), ensure_ascii=True, indent=2))
        return 2 if invalid_source else (0 if passed else 1)
    except (OSError, UnicodeError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps(dict(ok=False, error=str(exc)), ensure_ascii=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
