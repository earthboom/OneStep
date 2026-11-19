---
id: K-FIC-CRAFT-RELATION-MAP
title: Draw readable character relationship maps with evidence and time for AI reuse
summary: Use a small labeled map for people and linked structured records for AI, with stable character IDs,
  directed relation types, scene phases and source passages. Separate co-occurrence, speech, belief, allegation,
  proposal and accepted agreement; a missing edge is unknown rather than false.
kind: method
scope: Fiction design and manuscript-grounded relationship annotation for human and machine reading
keywords:
- character-network
- relationship-map
- directed-graph
- evidence
- coreference
- information-access
- 캐릭터관계도
- 캐릭터 관계도
- 인물관계도
- 관계도
- 관계망
- 관계도그리기
- 관계시각화
- 방향성
- 정보차이
- 시점변화
- 근거구절
- AI이해
status: active
checked_at: '2026-11-17'
relations:
  derived_from:
  - K-FIC-CRAFT-RELATIONSHIPS
  - K-FIC-PLAUSIBILITY-REVIEW
context:
  evidence: Six papers and two W3C documents inspected at the depths listed below; procedures are editorial adaptations
---

# Draw readable character relationship maps with evidence and time for AI reuse

## Guidance

### Select a relation before drawing a line

Character-network research distinguishes identifying characters, defining interactions and analyzing the resulting network [M01, M02]. A conversation edge, repeated co-occurrence and a trust judgment answer different questions. State what an edge means before selecting a layout. Information propagation also needs the content, direction and access path, rather than just shared presence [M03].

For a writer-facing map, start with the current question: who needs whom, who knows which fact, what obligation changed, or what made cooperation possible? Use [directional relationship design](K-FIC-CRAFT-RELATIONSHIPS.md) for the underlying dramatic choices. The map represents that reasoning; it cannot establish motives by itself.

### Maintain linked human and machine views

This is an editorial procedure adapted from the sources, not a published, experimentally validated writing method.

1. **Identify entities.** Assign stable IDs even to unnamed people, organizations and relevant groups. Keep display names and aliases separate. Resolve Korean omitted subjects, titles, kinship terms, dialogue first person and pronouns in context; do not make every `그` an alias for the same man or every `나` the narrator. Literary coreference is a distinct annotation problem [M04]; extraction errors can affect a network downstream [M05].
2. **Record typed, directed relations.** Store `from_id`, `to_id`, `predicate`, short label, phase, assertion status and evidence IDs. A toward B need not equal B toward A. Separate social affiliation, practical dependency, emotion, communication and knowledge. A numerical weight must name its measured basis; dialogue frequency does not measure love or trust.
3. **Represent shared events explicitly.** For a three-party bargain, connect participants and their separate conditions to an agreement event. Preserve offers, refusals, approved conditions and performed actions as separate states. This adapts the n-ary-relation pattern [M07]; it avoids implying three unconditional friendships through a triangle.
4. **Keep source and time.** Link every consequential claim to a manuscript version/hash, exact quote and locator. Name speaker, observer or document when relevant. Distinguish story-time validity from when the reader learns a secret if these differ. For the worked example, four sequential scene phases suffice. Provenance concepts [M08] inspire these fields; provenance is not proof of truth.
5. **Render selected views.** Put only the active cast and relations needed for one question on a node-link diagram. Label arrows with a concrete verb or condition, keep character placement/labels stable across comparable snapshots, and use line style plus words rather than color alone. Add a separate background view and change timeline rather than crowding all relations together. When density makes tracing difficult, try an adjacency table/matrix or a chapter/scene filter. Graph-versus-matrix readability depends on the task and graph [M06]; there is no universal character-count cutoff.
6. **Check both representations.** Read the actual map at its intended display size, then answer source-grounded questions from the records. Check direction, phase, attribution and uncertainty against the manuscript. A beautiful drawing cannot validate its underlying claims; valid JSON cannot establish visual clarity.
7. **Synchronize after revision.** Change the source-grounded records, revalidate passages and regenerate selected views. If someone edits a canvas independently, reconcile it before AI reuse. A source hash mismatch means the annotations require review, not that offsets should silently be shifted.

### Minimal portable records

For a small work, plain JSON plus the manuscript is sufficient. A graph database or retrieval framework is not required by these sources or this example.

| Record | Minimum useful content |
| --- | --- |
| Entity | Stable ID, kind, display name, contextual mentions/aliases; avoid inventing names or biographies |
| Relation | ID, source and target IDs, type, phase/time, status, exact supporting passages; belief-holder if a belief |
| Event | ID, participants/roles, separate condition and approval links, proposed/approved/performed state |
| Information access | Character, proposition, phase, knows/believes/heard/explicitly unread/unknown, supporting source |
| Evidence | Source path and revision/hash, quote, offset convention or line locator, speaker/document/observer |
| View | Purpose, selected IDs, phase, labels and drawing source; omitted relations remain in the underlying record |

Do not convert an absent edge into hostility, an unrecorded fact into ignorance, a report's accusation into guilt, or a cooperative action into settled trust. Keep author-planned future facts separate from what the manuscript establishes and from what each character or reader can access. If an inference is useful, retain its basis and alternative reading.

### Reuse during drafting

For drafting, first retrieve this method and the current work's map. Ask a scoped question such as: “At the opening, what can the narrator know, and which agreement has each participant accepted? Cite relation and evidence IDs.” Read the cited passages before applying the answer to a new scene. Retrieve another phase only if the scene or disclosure order allows it.

## Applicability and exceptions

The method is intended to make assumptions and evidence inspectable for humans and AI. It has not established improved LLM comprehension, extraction accuracy, Korean-reader comprehension or literary enjoyment. The cited NLP studies concern their own corpora and extraction tasks, mostly English; Korean ellipsis and address terms require local checks. Graph centrality does not establish narrative importance, moral value or point of view.

Draft planning may deliberately contain undecided or contradictory options. Mark these as alternatives rather than silently treating all as canon. Unreliable narration, mistaken beliefs, secrets, role changes and parallel timelines require explicit attribution and time scope. A large cast may need multiple views; the small example is not a universal layout template.

This example is manually annotated, not an automatic extraction system, RDF/OWL ontology or PROV-O implementation. No precision/recall improvement or independent evaluation is claimed. The canonical manuscript remains authoritative; the JSON is a derived editorial annotation. Its Mermaid and SVG are selected projections, not a complete world model.

## Checks

- Can each visible line be translated into a typed relation/event with a source and direction?
- Does each consequential relation have a phase and passage? Does the source hash still match?
- Are proposed, refused, approved and performed states distinct? Is inspection permission being mistaken for publication consent?
- Can an inference, an accusation and a narrated observation be told apart without relying on color?
- Are dialogue first person and ambiguous pronouns resolved locally? Is an unnamed person still findable by ID?
- Can the AI answer “who knows what at this phase?” without importing a later revelation?
- Do the rendered views agree with the record and preserve important limits? Can a person read the labels without line crossings or clipped text at the intended size?
- For future automated extraction, evaluate entity/coreference errors, typed/directed edges, time/status and evidence fidelity separately against reviewed passages. A JSON parser pass alone answers none of those accuracy questions.

## Evidence

Checked 2026-11-17. Six papers plus two W3C documents; not eight experiments or eight full-text readings. Only the access depths below are claimed. Source findings and the proposed writing procedure are distinct.

| ID | Primary source and inspected portion | Usable point and limit |
| --- | --- | --- |
| M01 | Labatut & Bost, 2019, [Extraction and Analysis of Fictional Character Networks: A Survey](https://arxiv.org/abs/1907.02704). ACM Computing Surveys 52(5):89, DOI 10.1145/3344548. Author arXiv v5 revised 2022-03-31; abstract inspected. | Extraction and interpretation depend on medium and analysis goal. Survey, not a validated recipe for writing or AI comprehension. HAL full text was inaccessible. |
| M02 | Elson, Dames & McKeown, 2010, [Extracting Social Networks from Literary Fiction](https://aclanthology.org/P10-1015/). ACL; PDF abstract and introduction inspected. | Character identification and attributed conversation support a conversation network. Such an edge does not automatically denote affection or trust. |
| M03 | Sims & Bamman, 2020, [Measuring Information Propagation in Literary Social Networks](https://aclanthology.org/2020.emnlp-main.47/). EMNLP, DOI 10.18653/v1/2020.emnlp-main.47. Abstract and PDF introduction inspected. | Information passing between characters is a specific modeling task. Their pipeline and corpus findings do not certify this hand-authored map. |
| M04 | Bamman, Lewke & Mansoor, 2020, [An Annotated Dataset of Coreference in English Literature](https://aclanthology.org/2020.lrec-1.6/). LREC; landing abstract and PDF opening inspected; PDF title is A Dataset of Literary Coreference. | Contextual identity/coreference deserves separate attention. English sampled passages from 100 works do not validate Korean pronoun resolution. |
| M05 | Amalvy, Labatut & Dufour, 2025, [The Role of Natural Language Processing Tasks in Automatic Literary Character Network Construction](https://aclanthology.org/2025.coling-main.566/). COLING, pp. 8462–8473. Abstract and PDF opening inspected. | The paper tests downstream effects of extraction errors in co-occurrence networks. Findings about tested LLM recall do not mean every LLM or every relation-extraction method is inferior. |
| M06 | Ghoniem, Fekete & Castagliola, 2005, [On the Readability of Graphs Using Node-Link and Matrix-Based Representations](https://journals.sagepub.com/doi/10.1057/palgrave.ivs.9500092). Information Visualization 4:114–135, DOI 10.1057/palgrave.ivs.9500092. Publisher abstract inspected; author PDF timed out. | Controlled comparison across generic graph-reading tasks; representation choice depends on graph and task. Not a Korean literary-map reader study or universal numeric threshold. |
| M07 | W3C, 2006-04-12, [Defining N-ary Relations on the Semantic Web](https://www.w3.org/TR/swbp-n-aryRelations/). Abstract and Pattern 1 / use case 3 inspected. | An informative Working Group Note about relation instances and multiple participants; not a Recommendation or empirical paper. The event record is an adaptation, not a compliant ontology. |
| M08 | W3C, 2013-04-30, [PROV-O](https://www.w3.org/TR/prov-o/). Introduction, role and qualified-association example inspected. | Recommendation distinguishing provenance entities, activities, agents and roles. Borrowing this distinction does not prove a claim true or implement the standard. |

They assess this saved representation, not future model or reader performance.
