"""Disposable SQLite candidate index. Markdown parsing and ranking belong to search.py."""
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import unicodedata


WORDS = re.compile(r"\w+")
# Bump when the schema, projected search fields, or word encoding changes.
FORMAT = b"onestep-candidate-index-v2"
FIELDS = ("id", "title", "keywords", "trigger", "symptom", "summary", "prevention", "scope", "context", "body")
INSERT_WORDS = f"INSERT INTO words(rowid,{','.join(FIELDS)}) VALUES({','.join(['?'] * (1 + len(FIELDS)))})"
SCHEMA = (
    "CREATE TABLE state(signature TEXT, manifest TEXT)",
    "CREATE TABLE docs(n INTEGER PRIMARY KEY, path TEXT UNIQUE, id TEXT, folded TEXT UNIQUE, "
    "norm_id TEXT, domain TEXT, store TEXT, status TEXT, body_hash TEXT, mtime INTEGER, size INTEGER, data TEXT)",
    "CREATE INDEX normalized_ids ON docs(norm_id)",
    f"CREATE VIRTUAL TABLE words USING fts5({','.join(FIELDS)}, tokenize='ascii', detail=column)",
    "CREATE TABLE edges(source TEXT, kind TEXT, target TEXT)",
    "CREATE INDEX outgoing ON edges(source)",
    "CREATE INDEX incoming ON edges(target)",
)


def fingerprint(files):
    digest = hashlib.sha256()
    for path, (_, _, (mtime, size)) in files.items():
        digest.update(f"{path}\0{mtime}\0{size}\0".encode("utf-8"))
    return digest.hexdigest()


class IndexedDocuments:
    def __init__(self, connection):
        self.db = connection

    def __iter__(self):
        return (json.loads(row[0]) for row in self.db.execute("SELECT data FROM docs ORDER BY n"))

    def __len__(self):
        return self.db.execute("SELECT count(*) FROM docs").fetchone()[0]

    def has_id(self, literal):
        return self.db.execute("SELECT 1 FROM docs WHERE norm_id=?", (literal,)).fetchone() is not None

    def candidates(self, terms, domains, store):
        # A literal boundary match necessarily contains each complete internal
        # word and at least a prefix of its final word (including Korean endings).
        # Encoding Python-normalized words prevents FTS tokenizer differences.
        anchors = set()
        for term in terms:
            matches = list(WORDS.finditer(term))
            if not matches:
                anchors.clear()  # A punctuation-only literal requires the full eligible set.
                break
            # Several necessary words distinguish a compound ID from documents
            # that merely mention its topic. Alternatives remain disjunctive.
            required = []
            for match in sorted(matches, key=lambda m: len(m.group()), reverse=True)[:3]:
                encoded = match.group().encode().hex()
                prefix = encoded[:64]
                partial = len(encoded) > len(prefix) or match.end() == len(term)
                required.append(prefix + ("*" if partial else ""))
            anchors.add(" AND ".join(required))
        clauses, params = [], []
        if anchors:
            # Split large disjunctions to keep MATCH expressions bounded.
            choices = sorted(anchors)
            groups = [" OR ".join(choices[i:i+64]) for i in range(0, len(choices), 64)]
            clauses.append("n IN (SELECT words.rowid FROM json_each(?) CROSS JOIN words WHERE words MATCH json_each.value)")
            params.append(json.dumps(groups))
        if domains:
            clauses.append("domain IN (SELECT value FROM json_each(?))")
            params.append(json.dumps(list(domains)))
        if store != "both":
            clauses.append("store=?")
            params.append(store)
        where = " WHERE " + " AND ".join(clauses) if clauses else ""
        return (json.loads(row[0]) for row in self.db.execute("SELECT data FROM docs" + where, params))

    def by_ids(self, ids):
        keys = json.dumps([i.casefold() for i in ids])
        return {k: json.loads(data) for k, data in self.db.execute(
            "SELECT folded,data FROM docs WHERE folded IN (SELECT value FROM json_each(?))", (keys,))}

    def word_page(self, groups, weights, particles, lexical_score, statuses, include_superseded, limit, offset):
        """Rank broad single-word searches using field postings; load only the requested page."""
        terms = {term for aliases in groups for term in aliases}
        if len(terms) > 64 or not all(WORDS.fullmatch(term) and len(term.encode()) <= 32 for term in terms):
            return None
        # Small candidate sets are cheaper to score directly. Prefixes give a
        # safe upper bound even for Korean endings and attached postpositions.
        broad = " OR ".join(term.encode().hex() + "*" for term in terms)
        if not self.db.execute("SELECT 1 FROM words WHERE words MATCH ? LIMIT 1 OFFSET 128", (broad,)).fetchone():
            return None
        totals = {}
        for aliases in groups:
            choices = set()
            for term in aliases:
                token = term.encode().hex()
                if re.search("[가-힣]", term):
                    choices.add(token + "*")
                else:
                    choices.add(token)
                    if term.isascii():
                        choices.update(token + suffix.encode().hex() for suffix in particles)
            expression = " OR ".join(sorted(choices))
            best = {}
            for field, weight in weights.items():
                rows = self.db.execute("SELECT rowid FROM words WHERE words MATCH ?",
                                       (f"{field}:({expression})",))
                for (number,) in rows:
                    best[number] = max(best.get(number, 0), weight)
            for number, weight in best.items():
                points, coverage = totals.get(number, (0, 0))
                totals[number] = points + weight, coverage + 1

        ranking, bodies = [], set()
        rows = self.db.execute("SELECT n,folded,status,body_hash FROM docs WHERE n IN "
                               "(SELECT value FROM json_each(?))", (json.dumps(list(totals)),))
        for number, key, status, body_hash in rows:
            if statuses and status not in statuses:
                continue
            if not statuses and status == "superseded" and not include_superseded:
                continue
            # A duplicate requires the full evidence-aware round-robin, even
            # with --all-variants (which still reports related copies).
            if body_hash in bodies or not body_hash:
                return None
            bodies.add(body_hash)
            points, coverage = totals[number]
            ranking.append((-lexical_score(points, coverage, len(groups)), status == "unknown", key))
        ranking.sort()
        return self.by_ids([key for _, _, key in ranking[offset:offset + limit]]).values(), len(ranking)

    def protected_ids(self):
        return {k for row in self.db.execute(
            "SELECT source,target FROM edges WHERE kind IN ('conflicts_with','supersedes')") for k in row}

    def close(self):
        self.db.close()

    def edges_for(self, ids):
        keys = json.dumps([i.casefold() for i in ids])
        rows = self.db.execute(
            "SELECT s.id,e.kind,t.id FROM edges e JOIN docs s ON s.folded=e.source "
            "JOIN docs t ON t.folded=e.target WHERE e.source IN (SELECT value FROM json_each(?)) "
            "OR e.target IN (SELECT value FROM json_each(?)) ORDER BY s.n,e.rowid", (keys, keys))
        return [dict(source=s, type=k, target=t) for s, k, t in rows]


def open_index(path, files, checker, project, refresh, parse_changed, fields_for, scan):
    here = Path(__file__).parent
    signature = hashlib.sha256(FORMAT + str(project).encode() + b"".join(
        (here / name).read_bytes() for name in ("catalog.py", "relations.py", "sources.py")
    )).hexdigest()
    db = sqlite3.connect(path, isolation_level=None, timeout=15)
    try:
        def state():
            if not db.execute("SELECT 1 FROM sqlite_master WHERE name='state'").fetchone():
                return None
            return db.execute("SELECT signature,manifest FROM state").fetchone()

        db.execute("BEGIN")
        current = (signature, fingerprint(files))
        if not refresh and state() == current:
            db.execute("SELECT n FROM docs, words, edges LIMIT 0")
            return IndexedDocuments(db), 0, len(files)
        db.rollback()
        db.execute("BEGIN IMMEDIATE")
        # A writer may have committed while this process waited for the lock.
        files = scan()
        current = (signature, fingerprint(files))
        saved = state()
        if not saved or saved[0] != signature:
            for name in ("state", "docs", "words", "edges"):
                db.execute("DROP TABLE IF EXISTS " + name)
            for statement in SCHEMA:
                db.execute(statement)
        old = {p: (n, k, [mtime, size]) for p, n, k, mtime, size in db.execute(
            "SELECT path,n,folded,mtime,size FROM docs")}
        changed = [p for p, loc in files.items() if refresh or p not in old or loc[2] != old[p][2]]
        for p in (old.keys() - files.keys()) | (old.keys() & set(changed)):
            n, key, _ = old[p]
            db.execute("DELETE FROM words WHERE rowid=?", (n,))
            db.execute("DELETE FROM edges WHERE source=?", (key,))
            db.execute("DELETE FROM docs WHERE n=?", (n,))
        for doc in parse_changed(checker, project, files, changed):
            p = doc["path"]
            meta = doc["meta"]
            ident = meta["id"]
            key = ident.casefold()
            try:
                n = db.execute("INSERT INTO docs(path,id,folded,norm_id,domain,store,status,body_hash,mtime,size,data) "
                               "VALUES(?,?,?,?,?,?,?,?,?,?,?)", (p, ident, key, unicodedata.normalize("NFKC", ident).casefold(),
                               doc["domain"], doc["store"], meta["status"], doc["body_sha256"],
                               *doc["stamp"], json.dumps(doc, ensure_ascii=False))).lastrowid
            except sqlite3.IntegrityError as exc:
                raise ValueError(f"duplicate ID: {ident}") from exc
            fields = fields_for(doc)
            tokens = [" ".join(w.encode().hex() for w in set(WORDS.findall(fields[field]))) for field in FIELDS]
            db.execute(INSERT_WORDS, (n, *tokens))
            db.executemany("INSERT INTO edges VALUES(?,?,?)", (
                (key, kind, target.casefold()) for kind, targets in meta.get("relations", {}).items() for target in targets))
        errors = [m for m in checker.messages if m["level"] == "error"]
        if errors:
            raise ValueError("canonical validation failed: " + json.dumps(errors[:5]))
        missing = db.execute("SELECT source,target FROM edges LEFT JOIN docs ON folded=target WHERE n IS NULL LIMIT 1").fetchone()
        if missing:
            raise ValueError(f"{missing[0]}: missing relation target {missing[1]}")
        db.execute("DELETE FROM state")
        db.execute("INSERT INTO state VALUES(?,?)", current)
        db.commit()
        db.execute("BEGIN")
        state()  # Pin a read snapshot across ranking, traversal and source notices.
        return IndexedDocuments(db), len(changed), len(files)
    except BaseException:
        db.close()
        raise
