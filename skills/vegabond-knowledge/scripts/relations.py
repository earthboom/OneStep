"""Optional ID relationships shared by catalog validation and retrieval."""

import re


RELATION_TYPES = {"requires", "derived_from", "prevention", "supersedes", "conflicts_with"}
ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")


def validate_relations(meta):
    relations = meta.get("relations", {})
    if not isinstance(relations, dict):
        return ["relations must be a mapping of relation types to nonempty ID lists"]
    errors = []
    for kind, targets in relations.items():
        if kind not in RELATION_TYPES:
            errors.append(f"unknown relation type: {kind}")
        if not isinstance(targets, list) or not targets or any(
                not isinstance(t, str) or not ID.fullmatch(t) for t in targets):
            errors.append(f"{kind}: expected a nonempty list of entry IDs")
        elif len({t.casefold() for t in targets}) != len(targets):
            errors.append(f"{kind}: duplicate target ID")
        elif meta["id"].casefold() in {t.casefold() for t in targets}:
            errors.append(f"{kind}: self-reference is not useful")
    return errors


def relation_edges(documents):
    """Resolve declared edges; missing or ambiguous identities are errors."""
    by_id = {}
    for doc in documents:
        key = doc["meta"]["id"].casefold()
        if key in by_id:
            raise ValueError(f"duplicate ID: {doc['meta']['id']}")
        by_id[key] = doc
    edges = []
    for doc in documents:
        meta = doc["meta"]
        errors = validate_relations(meta)
        if errors:
            raise ValueError(f"{meta['id']}: " + "; ".join(errors))
        for kind, targets in meta.get("relations", {}).items():
            for target in targets:
                if target.casefold() not in by_id:
                    raise ValueError(f"{meta['id']}: missing relation target {target}")
                edges.append(dict(source=meta["id"], type=kind, target=by_id[target.casefold()]["meta"]["id"]))
    return by_id, edges
