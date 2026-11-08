---
id: K-GAME-RESEARCH-USE
title: Retrieve applicable evidence throughout game development
summary: For game planning, architecture, implementation, debugging and optimization, turn the concrete decision or symptom into a focused knowledge query. Check source versions and conditions, decide adoption, and carry a measurable application check into the existing brief.
kind: convention
scope: OneStep game development and explicitly configured reuse of this store in another project; current project intent and authoritative design and code contracts prevail
keywords: [game-development, game-design, implementation, debugging, optimization, genre, research-retrieval, GDD, prototype, playtest, 게임개발, 게임기획, 기술선택, 구현, 디버깅, 최적화, 지식조회, 복합장르]
status: active
checked_at: '2026-11-08'
context:
  authority: Explicit user requests to collect game design and implementation knowledge and retrieve suitable techniques during future game development
  evidence_check: Retrieval convention and corpus structure; individual source checks are in each reference
  application_status: "Workflow routing plus scoped Unity experiments for CAMERA/HITSCAN/PATH/CROWD; no production-game, player or commercial validation"
---

# Retrieve applicable evidence throughout game development

## Guidance

Before game planning, architecture, implementation, debugging or optimization, identify the concrete decision, feature or observed symptom. Record relevant project/revision, engine/package versions, platform/input, intended experience, frame/resource budget, and network/state authority. For defects, preserve the reproduction and measured symptom. Unknown values remain gaps; retrieve useful evidence while resolving them.

Search the [game catalog](index.md) through [knowledge retrieval](../../skills/vegabond-knowledge/references/retrieval.md), including relevant code knowledge and problem records. Start with one to three useful details and expand for a concrete dependency, conflict or unanswered question. Use symptom and mechanism variants when a query misses; consult the [technique guide](K-GAME-TECH-GUIDE.md) as a fallback map. A top-ranked hit is a candidate, not an adoption decision. Do not read the complete collection on every task.

Use the [experience framework](K-GAME-DESIGN-FRAMEWORK.md) for concept and hybrid questions, [prototype/playtest](K-GAME-PROTOTYPE-PLAYTEST.md) for uncertain experience claims, [economy](K-GAME-ECONOMY.md) for resource interactions, and [accessibility/onboarding](K-GAME-ACCESSIBILITY-ONBOARDING.md) for interaction barriers. Select genre references by what is being designed, not only a marketing label. A cooperative roguelike may require action, cooperative pacing, run structure and resource methods at different steps.

When a query returns nothing, distinguish an unfamiliar expression from a missing required contract. Try mechanism terms, another language or a narrowly broader scope once, and use the guide for a relevant known mechanism. If an exact vendor API, private format or version guarantee still lacks evidence, name the missing contract and the dependent commitment; request the smallest authoritative document or experiment needed. A generic related hit cannot establish that exact guarantee. Complete independent, source-supported analysis while leaving that commitment conditional; no match is not proof of nonexistence.

When several techniques match, split the request into decisions before choosing. Compare the representation, required inputs, guarantee, authority, version and measured cost each candidate addresses. Different layers can need different techniques: route search does not resolve local avoidance, visible surface detail does not create collision, and visual quality does not establish competitive visibility. Adopt a combination only where each part has a role and compatible conditions; reject or defer mismatched candidates. Do not decide by rank, repeated citations or the number of matching terms.

Read candidates' Guidance, applicability, checks and Evidence. Compare the actual engine/version, data ownership, target hardware and gameplay constraints; a historical source-game implementation is not a current engine API guarantee. Mark each consequential proposal **adopt**, **conditional** or **reject**, with its reason. Inspect original sources or research a missing detail before dependent work when the summary cannot support it. Distinguish source observations, transferable synthesis and untested local assumptions.

Keep a compact application trace in the existing work brief or design: **problem/constraints → entry ID and useful section/source locator → decision and reason → intended change → check and observed result/gap**. A source citation alone is insufficient. For example, a late-jump complaint can use CONTROLLER's buffered-input window while retaining TIMESTEP's simulation contract; an expensive forest needs measured geometry/pixel/shadow costs before choosing FOLIAGE's instancing or LOD. Tie the chosen method to a small representative prototype or regression/performance check; do not report a proposed check as passed.

After implementation or investigation, return the actual outcome, rejected analogy, failed condition and useful correction to [knowledge](../../skills/vegabond-knowledge/SKILL.md). Update an existing entry when evidence improves it; keep project-specific incidents in records. Only demonstrated local results become local lessons or verified safeguards. Revisit retrieval when reproduction, platform, authority or design intent changes; preserve still-valid answers.

For large plans, connect retrieved methods to the existing hierarchy, dependent systems and acceptance checks using [large-plan coordination](../../skills/vegabond-planning/references/large-plans.md). Keep the project's own design and playtest evidence authoritative. Refresh affected retrieval after a change; preserve still-valid information rather than rereading the complete collection.

## Applicability and exceptions

This is the user's requested retrieval convention for game work. It does not require techniques in unrelated software or authorize changing other projects. A simple established local pattern can reuse a valid prior lookup and state why it still applies. Hybrid genres may contain conflicting recommendations: relate the conflict to the intended experience and test the relevant tradeoff. ARPG loot references do not cover all role-playing, industrial-management references do not cover all simulation, and one 4X example does not establish every strategy design.

For a purely mechanical spelling or formatting proposal whose supplied local input fully settles the change and preserved fields, use that input as the governing evidence. Do not initiate game-technique searches solely because the file belongs to a game. Search only if an actual contract, dependency or uncertainty could change the requested action; verify the exact diff and preserve unrelated fields.

The collection is a broad starting corpus, not an exhaustive or permanently current genre encyclopedia. Gaps such as a specific sport, fighting-game format, VR embodiment, MMO social structure or platform policy require focused research when relevant. Store entries with inspected evidence and explicit limits; a search snippet, unavailable video, or untested suggestion cannot become a verified method by repetition. Use this store in another project only within its configured or authorized source scope.

## Checks

- Does the retrieved entry match the actual decision or reproduced symptom, engine/version, hardware, authority, genre mechanics and production conditions?
- Does the brief contain an action or check informed by the evidence, rather than only a citation?
- Is adoption, conditional use or rejection explicit, with source-case results separated from new-game hypotheses and pending real tests?
- Does a rule conflict with project authority, intended ambiguity, accessibility, competitive fairness or another system?
- Is a missing source or coverage gap visible, with only dependent decisions left unresolved?

Catalog/schema validation establishes storage and discoverability, not gameplay quality, balance, usability or market success.

## Evidence

- User instructions in the current chat on 2026-11-07: collect game planning and shorts-derived technical knowledge, supplement unconfirmed implementation details, and retrieve suitable knowledge during future game development. This authorizes the scoped retrieval convention; it does not approve a particular game's design or implementation.
- The [knowledge procedure](../../skills/vegabond-knowledge/SKILL.md) governs scoped index-to-detail retrieval and evidence limits. [Scout](../../skills/vegabond-scout/SKILL.md), [planning](../../skills/vegabond-planning/SKILL.md), [code](../../skills/vegabond-code/SKILL.md) and [code design](../../skills/vegabond-code-design/SKILL.md) route game work here; the caller owns execution and verification. Entry-specific Evidence sections retain actual URLs, locators, source type and access limitations.
- Initial research produced reusable references and hypothetical application evaluations. Subsequent [Technique Lab experiments](../../prototypes/TechniqueLab/RESULTS.md) exercised CAMERA/HITSCAN/PATH in Unity 6000.0.77f1 PlayMode and three Windows Mono players, with raw measurements, failed-then-passed corrections and scoped adoption conditions. This is not a production game or player study; the remaining count was 40 at that stage; the dynamic follow-up below adds CROWD evidence. Use the actual mechanism, host and workload limits rather than transferring a benchmark number to a new game.

- Dynamic follow-up on 2026-11-08: [PATH/CROWD implementation and full-frame evidence](../../prototypes/TechniqueLab/DYNAMIC-RESULTS.md) connect deferred obstacles, local reservations, safe/unsafe comparisons and complete-frame costs to conditional adoption. Cumulative scoped engine evidence now covers four sheets, with 39 still unvalidated locally. A small controller cost did not establish the whole-frame target; missing GPU values were retained as a gap, not treated as zero.


### Latest runtime decision trace — 2026-11-08

The [opposing mixed-radius experiment](../../prototypes/TechniqueLab/TRAFFIC-RESULTS.md) combined PATH-compatible radius/goal fields with CROWD neighbour guards and explicit corridor scheduling. A collision-safe deadlock control rejected pure reactive yielding as a progress solution. The tested lane/lease method is conditional on authored holding areas, fixed circular footprints and one authority. Actual safety/completion, full-frame cost, GPU gaps and retrieval misses were returned to the same entries. Reuse the decision conditions, then validate the new game; do not copy a universal deadlock-free claim.


### Sustained service decision trace — 2026-11-08

The [unlaned stream experiment](../../prototypes/TechniqueLab/STREAM-RESULTS.md) adds per-ID release/admission/completion and unresolved-age evidence. Search PATH for time-expanded routes and CROWD for geometric conflict plus throughput/service decisions. Reject global throughput as a starvation check: latest-first admission left an old request pending while hundreds completed. Separate overload latency failure from permanent bypass. Conditional FIFO/full-route use requires controlled births, static geometry and exact planned movement; reproduce actual queue/latency and planning-bearing whole-frame costs in the target game.
