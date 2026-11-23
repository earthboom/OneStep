"""Project-local lexical retrieval, ID traversal and repeatable quality evaluation.

Markdown is authoritative. The disposable cache never reads human translations,
external originals, or generated catalogs. No network, model, or vector service.
"""

from __future__ import annotations

import argparse
from collections import Counter, deque
from functools import lru_cache
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
import time
import unicodedata
from urllib.parse import unquote, urlsplit

# A read-only CLI must not create local/dependency bytecode on first import.
sys.dont_write_bytecode = True

from catalog import Catalogs, human_file, yaml, LINK, visible_markdown
from relations import relation_edges, validate_relations
try:
    import sqlite3
except ImportError:
    sqlite3 = None
SEARCH_ERRORS = (OSError, UnicodeError, ValueError, KeyError, TypeError) + ((sqlite3.DatabaseError,) if sqlite3 else ())
if yaml is not None:
    from sources import SourceRegistry, SourceError, parse_roots


CACHE = Path(".cache/onestep/search-v1.json")
HERE = Path(__file__).resolve().parent
WEIGHTS = {"id": 18, "title": 10, "keywords": 9, "trigger": 9, "symptom": 9,
           "summary": 6, "prevention": 6, "scope": 3, "context": 2, "body": 1}
TOKEN = re.compile(r"[\w]+(?:(?:[./-][\w]+)|(?:::[\w]+))*(?:\+\+|#)?", re.UNICODE)
# Technical names in Korean questions often carry a postposition without a space.
PARTICLE_WORDS = "에서 에게 으로 부터 까지 처럼 보다 은 는 이 가 을 를 과 와 에 의 로 도 만".split()
PARTICLES = "(?:" + "|".join(PARTICLE_WORDS) + ")"
ATTACHED_PARTICLE = re.compile(r"(?<=[a-z0-9_+#])" + PARTICLES + r"(?!\w)")
SEARCH_META = set(WEIGHTS) - {"body"} | {"status", "checked_at", "kind", "relations", "cause_status", "prevention_status"}


def normalized(value):
    return unicodedata.normalize("NFKC", str(value)).casefold()


@lru_cache(maxsize=1024)
def term_pattern(term):
    if re.search(r"[가-힣]", term):
        # Korean particles/endings may follow a term, but a suffix inside an
        # unrelated compound is not a match (어미 must not match 종결어미).
        ending = ""
    elif term.isascii() and term and (term[-1].isalnum() or term[-1] in "_+#"):
        ending = r"(?=" + PARTICLES + r"?(?!\w))"
    else:
        ending = r"(?!\w)"
    return re.compile(r"(?<!\w)" + re.escape(term) + ending)


def term_match(text, term):
    if term not in text:
        return None
    return term_pattern(term).search(text)


def contains(text, term):
    return term_match(text, term) is not None


def analyze_query(query):
    text = ATTACHED_PARTICLE.sub("", normalized(query).strip())
    if not text:
        raise ValueError("query must not be empty")
    config = json.loads((HERE / "search_terms.json").read_text(encoding="utf-8"))
    groups, covered, inferred, hinted = [], set(), [], set()
    for rule in config.get("concepts", []):
        # Require a word start while allowing Korean particles/endings afterward.
        matches = [[fragment for fragment in alternatives
                    if re.search(r"(?<!\w)" + re.escape(normalized(fragment)), text)]
                   for alternatives in rule["all"]]
        if matches and all(matches):
            inferred.append(dict(id=rule["id"], matched_fragments=matches, expanded_terms=rule["expand"]))
            hinted.update(normalized(term) for term in rule["expand"])
    tokens = TOKEN.findall(text)
    for aliases in config["groups"]:
        aliases = [normalized(a) for a in aliases]
        found = [a for a in aliases if contains(text, a)]
        if found or hinted.intersection(aliases):
            groups.append(aliases)
            for token in tokens:
                if any(contains(token, a) or contains(a, token) for a in found):
                    covered.add(token)
    stop = set(config["stopwords"])
    groups.extend([t] for t in dict.fromkeys(tokens) if t not in covered and t not in stop)
    if not groups:
        raise ValueError("query has no searchable terms")
    return groups, inferred


def query_groups(query):
    return analyze_query(query)[0]


def safe_path(project, path):
    if (not path.resolve().is_relative_to(project) or path.is_symlink()
            or getattr(path, "is_junction", lambda: False)()):
        raise ValueError(f"linked or outside-project path: {path}")


def canonical_files(project):
    def walk(folder, prefix, store, domain=None):
        directories, details = [], []
        with os.scandir(folder) as stream:
            for entry in stream:
                name = entry.name
                if name.startswith("."):
                    continue
                directory = entry.is_dir(follow_symlinks=False)
                lower = name.lower()
                detail = domain and lower.endswith(".md") and not (
                    lower.endswith(".kr.md") or lower in {"index.md", "archive.md"})
                # An excluded file is never read. Linked directories must still
                # fail closed even when their name does not resemble a detail.
                if not directory and not detail:
                    if ((hasattr(entry, "is_junction") and entry.is_junction())
                            or (entry.is_symlink() and entry.is_dir())):
                        raise ValueError(f"linked or outside-project path: {entry.path}")
                    continue
                info = entry.stat(follow_symlinks=False)
                if entry.is_symlink() or getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT:
                    raise ValueError(f"linked or outside-project path: {entry.path}")
                relative = prefix + "/" + name
                if directory:
                    directories.append((entry.path, relative, domain or name))
                else:
                    details.append((relative, (store, domain, [info.st_mtime_ns, info.st_size])))
        # Preserve manifest order while sorting only canonical paths. DirEntry
        # objects and excluded translations can be released during enumeration.
        yield from sorted(details)
        for path, relative, child_domain in sorted(directories):
            yield from walk(path, relative, store, child_domain)

    for store in ("knowledge", "records"):
        base = project / store
        if not base.exists():
            continue
        safe_path(project, base)
        yield from walk(base, store, store)


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
                or not isinstance(doc.get("sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", doc["sha256"])
                or not isinstance(doc.get("body_sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", doc["body_sha256"])):
            return {}
    return docs


def canonical_document(checker, project, relative, location):
    store, domain, stamp = location
    path = project / relative
    entry = checker.entry(path, store)
    if entry is None or (entry["meta"] is None and not entry["legacy"]):
        raise ValueError(f"invalid canonical entry: {relative}; " + json.dumps(checker.messages[-4:]))
    meta = entry["meta"] or dict(id="legacy:" + relative, title=path.stem, summary="Unstructured legacy entry",
                                 keywords=[], scope="unknown", status="unknown", checked_at=None, kind="unknown")
    meta = {k: v for k, v in meta.items() if k in SEARCH_META}
    return dict(meta=meta, body=entry["body"], body_line=entry["body_line"], sha256=entry["sha256"],
                body_sha256=hashlib.sha256(entry["body"].encode("utf-8")).hexdigest(),
                stamp=stamp, path=relative, store=store, domain=domain)


def changed_documents(checker, project, files, changed):
    if len(changed) < 1000:
        for path in changed:
            yield canonical_document(checker, project, path, files[path])
        return

    from concurrent.futures import ThreadPoolExecutor

    def read_batch(paths):
        local = Catalogs(project, checker.command, checker.strict, require_translations=checker.require_translations)
        docs = [canonical_document(local, project, path, files[path]) for path in paths]
        # Some validation errors (e.g. a missing translation) accompany a parsed entry.
        errors = [m for m in local.messages if m["level"] == "error"]
        if errors:
            raise ValueError("canonical validation failed: " + json.dumps(errors[:5]))
        return docs

    # Overlap filesystem waits. One writer consumes at most one window of
    # batches in canonical order and validates IDs and relations across them.
    workers, batch_size = 8, 32
    window = workers * batch_size
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for start in range(0, len(changed), window):
            batches = (changed[i:i + batch_size] for i in range(start, min(start + window, len(changed)), batch_size))
            for batch in pool.map(read_batch, batches):
                yield from batch


def load_index(project, *, no_cache=False, refresh=False, portable_library=False):
    """Stat unchanged files; parse/hash changed files. --refresh bypasses stamps."""
    started = time.perf_counter()
    if portable_library:
        no_cache = True
    project = project.resolve()
    cache_path = project / CACHE
    files = dict(canonical_files(project))
    cached = {}
    cache_warning = None
    checker = Catalogs(project, "check", require_translations=not portable_library)
    database = cache_path.with_name("search-v2.sqlite3")
    large_cache = not no_cache and (len(files) >= 1000 or database.is_file())
    if large_cache and sqlite3 is None:
        cache_warning = "SQLite unavailable; using document scan"
    if large_cache and sqlite3 is not None:
        from search_index import open_index
        for path in (project / ".cache", database.parent, database,
                     *(database.with_name(database.name + ext) for ext in ("-journal", "-wal", "-shm"))):
            safe_path(project, path)
        try:
            database.parent.mkdir(parents=True, exist_ok=True)
            documents, reads, count = open_index(database, files, checker, project, refresh, changed_documents,
                                                 search_fields, lambda: dict(canonical_files(project)))
            return documents, dict(entries=count, read_files=reads, cached_files=count-reads,
                                   elapsed_ms=round((time.perf_counter()-started)*1000, 3),
                                   backend="sqlite", warning=None)
        except (OSError, sqlite3.DatabaseError) as exc:
            cache_warning = f"SQLite index unavailable; using document scan: {exc}"
            checker = Catalogs(project, "check", require_translations=not portable_library)
    signature = hashlib.sha256(b"".join((HERE / n).read_bytes() for n in (
        "search.py", "catalog.py", "relations.py", "sources.py", "search_terms.json"))).hexdigest()
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
    for relative, location in files.items():
        stamp = location[2]
        previous = cached.get(relative)
        if previous and previous["stamp"] == stamp and not refresh:
            docs[relative] = previous
            continue
        read_files += 1
        docs[relative] = canonical_document(checker, project, relative, location)
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
                    # Encode one row at a time. The streaming JSON encoder's
                    # per-token writes dominate cache replacement at scale.
                    header = json.dumps({"signature": signature, "project": str(project)})
                    stream.write(header[:-1] + ',"documents":{')
                    for i, (key, doc) in enumerate(docs.items()):
                        if i:
                            stream.write(",")
                        stream.write(json.dumps(key) + ":" + json.dumps(doc, ensure_ascii=False, separators=(",", ":")))
                    stream.write("}}")
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


def search_fields(doc):
    fields = {name: normalized(flatten(doc["meta"].get(name))) for name in WEIGHTS if name != "body"}
    fields["body"] = normalized(doc["body"])
    return fields


def lexical_score(points, covered, total):
    return round(points + 30 * covered / total, 3)


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
    for name in ("context", "cause_status", "prevention_status", "prevention"):
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
    hits = result.get("results", []) + result.get("related", [])
    if result.get("relations"):
        hits += result["relations"]["related"]
    by_id = (documents.by_ids([h["id"] for h in hits]) if hasattr(documents, "by_ids") else
             {d["meta"]["id"].casefold(): d for d in documents})
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


def diversify_hits(hits, by_id, protected, enabled):
    """Round-robin exact-body variants without discarding partial matches.

    No candidates disappear. Evidence states and explicit conflicts/replacements
    have separate groups; differing scope/context remains visible on each entry.
    """
    diversity = dict(enabled=enabled, groups=len(hits), variant_matches=0,
                     policy="Exact-body groups take turns; every candidate remains pageable. Scores and coverage retain their lexical meaning.")
    hashes = {doc.get("body_sha256") for doc in by_id.values()}
    if None not in hashes and len(hashes) == len(hits):
        return hits, diversity
    families = {}
    for hit in hits:
        doc = by_id[hit["id"]]
        meta = doc["meta"]
        identity = (("id", hit["id"].casefold()) if hit["id"].casefold() in protected else
                    ("body", doc.get("body_sha256") or hashlib.sha256(doc["body"].encode("utf-8")).hexdigest()))
        evidence = json.dumps({key: meta.get(key) for key in (
            "kind", "status", "checked_at", "cause_status", "prevention_status", "prevention", "relations")}, sort_keys=True)
        key = (identity, doc["store"], doc["domain"], evidence, tuple(hit["caveats"]))
        families.setdefault(key, []).append(hit)
    for members in families.values():
        # Constant-size samples avoid quadratic work on large duplicate groups.
        sample = [h["id"] for h in members[:4]]
        if len(members) > 1:
            for hit in members:
                ids = [ident for ident in sample if ident != hit["id"]][:3]
                hit["similar_content"] = dict(
                    other_matches=len(members) - 1, sample_ids=ids,
                    truncated=len(members) - 1 > len(ids),
                    notice="Identical body, not interchangeable evidence: scope/context may differ. Inspect variants by ID or --all-variants.")
    queue = deque(deque(members) for members in families.values())
    ordered = []
    while queue:
        members = queue.popleft()
        ordered.append(members.popleft())
        if members:
            queue.append(members)
    diversity.update(groups=len(families), variant_matches=len(hits) - len(families))
    return (ordered if enabled else hits), diversity


def hit_snippet(doc, hit):
    for line_offset, line in enumerate(doc["body"].split("\n")):
        text = normalized(line)
        if any(contains(text, term) for term in hit["matched_terms"]):
            return dict(line=doc["body_line"] + line_offset, text=excerpt(line, hit["matched_terms"]))
    return dict(line=1, text=f"Metadata match: {', '.join(hit['matched_fields'])}; {doc['meta']['summary']}"[:300])


def search(documents, query, *, domains=(), store="both", statuses=(), scope=None, context=None,
           include_superseded=False, limit=5, offset=0, diversify=True):
    literal = ATTACHED_PARTICLE.sub("", normalized(query).strip())
    indexed = hasattr(documents, "candidates")
    known = documents.has_id(literal) if indexed else any(normalized(d["meta"]["id"]) == literal for d in documents)
    if known:
        # A known-item lookup may contain an alias such as "music" inside its ID.
        groups, inferred = [[literal]], []
    else:
        groups, inferred = analyze_query(query)
    hinted = {normalized(term) for rule in inferred for term in rule["expanded_terms"]}
    importance = [2 if any(" " in a and (a in hinted or contains(literal, a)) for a in aliases)
                  else 1 for aliases in groups]
    terms = tuple(dict.fromkeys(term for aliases in groups for term in aliases))
    results, by_id, protected = [], {}, set()
    indexed_page = None
    if indexed:
        protected = documents.protected_ids()
        if not (context or scope or domains) and store == "both":
            indexed_page = documents.word_page(groups, WEIGHTS, PARTICLE_WORDS, lexical_score, statuses,
                                               include_superseded, limit, offset)
        candidates = indexed_page[0] if indexed_page is not None else documents.candidates(terms, domains, store)
    else:
        candidates = documents
        for doc in documents:
            for kind in ("conflicts_with", "supersedes"):
                targets = doc["meta"].get("relations", {}).get(kind, [])
                if targets:
                    protected.update(ident.casefold() for ident in [doc["meta"]["id"], *targets])
    for doc in candidates:
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
        fields = search_fields(doc)
        # Reject absent literals before the per-field boundary checks. All
        # scoring still happens inside the original, separately weighted fields.
        text = "\n".join(fields.values())
        present = {term for term in terms if term in text}
        if not present:
            continue
        matched_fields, matched_terms, score, matched_groups, covered_weight = set(), set(), 0, 0, 0
        for aliases, weight in zip(groups, importance):
            aliases = [term for term in aliases if term in present]
            if not aliases:
                continue
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
        if meta["status"] == "unknown":
            caveats.append("Legacy metadata is unknown; inspect the original before applying")
        hit = compact(doc, caveats)
        hit.update(score=lexical_score(score, covered_weight, sum(importance)),
                   matched_fields=sorted(matched_fields), matched_terms=sorted(matched_terms),
                   query_coverage=f"{matched_groups}/{len(groups)}")
        results.append(hit)
        by_id[meta["id"]] = doc
    results.sort(key=lambda h: (-h["score"], len(h["caveats"]), h["id"].casefold()))
    results, diversity = diversify_hits(results, by_id, protected, diversify)
    if indexed_page is None:
        total, page = len(results), results[offset:offset + limit]
    else:
        total, page = indexed_page[1], results
        diversity["groups"] = total  # word_page has established that every body is distinct.
    for hit in page:
        hit["snippet"] = hit_snippet(by_id[hit["id"]], hit)
    return dict(results=page, total_matches=total, offset=offset, diversity=diversity,
                truncated=total > offset + limit,
                expanded_terms=groups, inferred_concepts=inferred,
                gap=None if total else "No lexical match under these filters; try alternate terms or a broader scope. Absence is not proved.")


def related(documents, ids, *, depth=1, limit=10, offset=0):
    indexed = hasattr(documents, "by_ids")
    by_id, edges = (documents.by_ids(ids), []) if indexed else relation_edges(documents)
    roots = set()
    for ident in ids:
        if ident.casefold() not in by_id:
            raise ValueError(f"unknown entry ID: {ident}")
        roots.add(by_id[ident.casefold()]["meta"]["id"])
    visited, frontier, used_edges = set(roots), set(roots), []
    for _ in range(depth):
        following = set()
        if indexed:
            edges = documents.edges_for(frontier)
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
    if indexed:
        by_id = documents.by_ids(page)
    return dict(related=[compact(by_id[i.casefold()], ["Relation candidate; verify scope and source before applying"])
                         for i in page],
                edges=[e for e in used_edges if e["source"] in chosen or e["target"] in chosen
                       or (e["source"] in roots and e["target"] in roots)],
                total_related=len(ids), offset=offset, truncated=len(ids) > offset + limit)


def evaluate(documents, cases):
    if not isinstance(cases, list) or not cases:
        raise ValueError("evaluation requires a nonempty cases list")
    outcomes, required_total, found_total, forbidden_total = [], 0, 0, 0
    reciprocal_ranks = []
    for case in cases:
        started = time.perf_counter()
        result = search(documents, case["query"], domains=case.get("domains", ()), store=case.get("store", "both"),
                        statuses=case.get("statuses", ()), scope=case.get("scope"), context=case.get("context", {}),
                        include_superseded=case.get("include_superseded", False), limit=case.get("limit", 5))
        ranked = [h["id"] for h in result["results"]]
        actual = set(ranked)
        required = set(case.get("required", ()))
        forbidden = set(case.get("forbidden", ()))
        missing, bad = sorted(required - actual), sorted(forbidden & actual)
        first_rank = next((i for i, ident in enumerate(ranked, 1) if ident in required), None)
        if required:
            reciprocal_ranks.append(1 / first_rank if first_rank else 0)
        unexpected_matches = bool(case.get("expect_empty") and result["total_matches"])
        required_total += len(required)
        found_total += len(required & actual)
        forbidden_total += len(bad)
        outcomes.append(dict(name=case["name"], passed=not (missing or bad or unexpected_matches),
                             missing=missing, forbidden_hits=bad, unexpected_matches=unexpected_matches,
                             returned=ranked, first_required_rank=first_rank,
                             snippets_characters=sum(len(h["snippet"]["text"]) for h in result["results"]),
                             elapsed_ms=round((time.perf_counter() - started) * 1000, 3)))
    return dict(cases=outcomes, passed=sum(c["passed"] for c in outcomes), total=len(outcomes),
                required_recall=round(found_total / required_total, 4) if required_total else None,
                mean_reciprocal_rank=(round(sum(reciprocal_ranks) / len(reciprocal_ranks), 4)
                                      if reciprocal_ranks else None),
                forbidden_hits=forbidden_total,
                limitation="Recall covers only declared required IDs; forbidden-hit checks are not a general precision estimate.")


def lookup(documents, args, query, filters, roots):
    if args.command == "related":
        result = related(documents, args.id, depth=args.depth, limit=args.limit, offset=args.offset)
    else:
        result = search(documents, query, domains=args.domain, store=args.store, statuses=args.status,
                        scope=args.scope, context=filters, include_superseded=args.include_superseded,
                        limit=args.limit, offset=args.offset, diversify=not args.all_variants)
        ids = [h["id"] for h in result["results"]]
        result["relations"] = related(documents, ids, depth=args.depth, limit=args.limit) if ids else None
    verification = annotate_sources(args.project, documents, result, verify=args.verify_sources, roots=roots)
    result["source_verification"] = verification
    result["retrieval_ok"] = True
    if verification["statuses"].get("invalid", 0):
        return result, 2
    return result, int(verification["ok"] is False)


def add_lookup_options(parser):
    parser.add_argument("--query", action="append", help="Repeat for separate questions sharing the same filters and index load.")
    parser.add_argument("--domain", action="append", default=[])
    parser.add_argument("--store", choices=("knowledge", "records", "both"), default="both")
    parser.add_argument("--status", action="append", default=[])
    parser.add_argument("--scope")
    parser.add_argument("--context", action="append", default=[])
    parser.add_argument("--include-superseded", action="store_true")
    parser.add_argument("--depth", type=int, default=1)
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--no-cache", action="store_true")
    parser.add_argument("--portable-library", action="store_true",
                        help="Search a distributed English reference library without translation files or a search cache.")
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--verify-sources", action="store_true", help="Check linked registered originals for returned hits")
    parser.add_argument("--source-root", action="append", default=[], help="Authorized project=absolute-path for this call")
    parser.add_argument("--all-variants", action="store_true", help="Search in raw lexical order without exact-body diversification")


def execute(args):
    documents = None
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
        if args.all_variants and args.command != "search":
            raise ValueError("--all-variants applies only to search")
        if args.command == "evaluate" and (args.verify_sources or args.source_root):
            raise ValueError("Source checks apply to search/related, not ranking evaluation")
        if args.source_root and not args.verify_sources:
            raise ValueError("--source-root requires --verify-sources")
        roots = parse_roots(args.source_root)
        filters = context_filters(args.context)
        started = time.perf_counter()
        documents, stats = load_index(args.project, no_cache=args.no_cache, refresh=args.refresh,
                                      portable_library=args.portable_library)
        if args.command == "evaluate":
            if human_file(args.cases):
                raise ValueError("human translations are not evaluation inputs")
            result = evaluate(documents, json.loads(args.cases.read_text(encoding="utf-8"))["cases"])
            exit_code = int(result["passed"] != result["total"])
        elif args.command == "search" and len(args.query) > 1:
            results, exit_code = [], 0
            for query in args.query:
                entry, code = lookup(documents, args, query, filters, roots)
                results.append(dict(query=query, ok=code == 0, **entry))
                exit_code = max(exit_code, code)
            result = dict(queries=results)
        else:
            query = args.query[0] if args.command == "search" else None
            result, exit_code = lookup(documents, args, query, filters, roots)
        return dict(ok=exit_code == 0, command=args.command, index=stats,
                    elapsed_ms=round((time.perf_counter() - started) * 1000, 3), **result), exit_code
    except SEARCH_ERRORS as exc:
        return dict(ok=False, error=str(exc)), 2
    finally:
        if hasattr(documents, "close"):
            documents.close()


class RequestParser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)


def search_session(defaults):
    """One UTF-8 input line per search; release its read snapshot before replying."""
    parser = RequestParser(add_help=False, allow_abbrev=False)
    add_lookup_options(parser)
    for raw in sys.stdin.buffer:
        try:
            line = raw.decode("utf-8").strip()
            if not line:
                raise ValueError("empty search request")
            if line.startswith("["):
                options = json.loads(line)
                if not isinstance(options, list) or not all(isinstance(arg, str) for arg in options):
                    raise ValueError("expected an array of search option strings")
            else:
                options = ["--query=" + line]
            args = parser.parse_args(options, namespace=argparse.Namespace(**vars(defaults)))
            args.command = "search"
            response, _ = execute(args)
        except (UnicodeError, ValueError) as exc:
            response = dict(ok=False, error=str(exc))
        print(json.dumps(response, ensure_ascii=True, separators=(",", ":")), flush=True)
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__, epilog="session reads one search at a time from standard input.")
    parser.add_argument("command", choices=("search", "related", "evaluate", "session"))
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--id", action="append", default=[])
    parser.add_argument("--cases", type=Path)
    add_lookup_options(parser)
    args = parser.parse_args()
    if args.command == "session":
        if args.query or args.id or args.cases or not args.project.is_dir():
            parser.error("session requires an existing project and reads its queries from standard input")
        args.project = args.project.resolve()
        return search_session(args)
    response, code = execute(args)
    print(json.dumps(response, ensure_ascii=True, indent=2))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
