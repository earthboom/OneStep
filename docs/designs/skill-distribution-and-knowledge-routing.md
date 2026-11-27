# Keep distributed skills current and retrieve evidence in the right domain

Design proposal for OneStep · 2026-11-25

## Starting evidence and scope

A read-only comparison covered all 35 canonical English skill entry points and immediate skill reference files in this working tree. In both shipped formats the image entry point, `2d-game-characters.md` and `style-and-review.md` are stale. The references `2d-effects-and-motion.md` and `stationery-characters.md` are missing. The builder already collects these paths. The verifier starts from what is in the ZIP and compares only selected skills against the checkout, so the same omission in ZIP and web can pass. [Build inputs](../../portable/build.py) · [Distribution tests](../../portable/test_portable.py)

Both the planning and presentation knowledge catalogs currently contain zero structured entries. Searching the whole working store for `기획안 목표 성과지표` returns K-FIC-CRAFT-SCENE first. For `발표 슬라이드 청중 정보 밀도` it returns K-GAME-TECH-VOLUME first. Each query with its own domain returns zero matches. The lexical search helper already accepts multiple domains and reports empty results. Existing specialist guidance already asks for knowledge, project sources and focused research. The prior image trials found project identity rules and vendor evidence via direct and Scout entry. [Planning catalog](../../knowledge/planning/index.md) · [Presentation catalog](../../knowledge/presentation/index.md) · [Retrieval contract](../../skills/vegabond-knowledge/references/retrieval.md)

## Unit A — verify and rebuild the distributions

1. Extend the existing distributed-file test to derive the **expected set from the source tree**, independently of the builder's output. Enumerate canonical `skills/vegabond-*/SKILL.md` and `skills/vegabond-*/references/*.md`, excluding human translations. Compare this set with ZIP members and web section names under the same namespace. Reject missing, duplicate and obsolete paths. Compare the complete contents per path, allowing the LF/CRLF convention and the web section separator. Keep the existing checks for other release surfaces, deliberate content transformations, the curated game library and local-data exclusions.
2. Run the new check on the two **existing** outputs before rebuilding and confirm that it names all five current differences for each format. Rebuild both from one source snapshot using the existing builder, review the complete release diff and rerun the same check. An image-specific whitelist would miss the next specialist or reference. Comparing ZIP to web alone misses a shared omission. Treat ZIP and web as one release unit.
3. Verify the shipped entry points as consumers. After local install and relocation, follow the image entry to the stationery and motion references. Resolve those same topics in the web document by section name. Both destinations must contain the source guidance. In disposable fixtures, remove one reference from both formats, leave one stale web section, and introduce a duplicate section. Each case must fail for the relevant path. The unchanged install, relocation and curated-library tests must still pass. A failure blocks releasing the generated pair.

The proposed change is in [the existing packaging tests](../../portable/test_portable.py) and the generated ZIP/web outputs. The builder needs a change only if the independent comparison still fails after a normal rebuild. No new manifest service or build system is needed.

## Unit B — close the two observed knowledge gaps

| Future decision | Proposed home and evidence boundary | Acceptance example |
| --- | --- | --- |
| Which measure would show that a proposal achieved its intended outcome? | A planning entry on beneficiary, intended change, baseline, target, period, data source and the difference between an output and an outcome. Start with the [planning review](../../skills/vegabond-planning/references/review.md) and verify a reusable method against an original source before capture. | A workshop attendance count alone cannot establish that participants completed the target task more often. Expose the missing baseline or follow-up observation. |
| What information does this audience need on a decision slide? | A presentation entry on the audience's decision, its supporting claim, the comparison and legibility at the intended display size. Start from the [presentation skill](../../skills/vegabond-presentation/SKILL.md). Treat measured performance and audience comprehension as separate evidence. | For a purchase decision, keep the recommendation, comparable figures and decision-changing caveat together. Put supporting detail in notes or an appendix when appropriate. A universal line count would not settle this case. |

Use the current knowledge procedure to look for equivalent entries first, save or update each English detail and Korean companion, regenerate only affected catalogs and check them. Give entries Korean search terms drawn from the actual questions and links to original evidence. The synthetic project values from the audit belong to those fixtures. This design does not promote them to global policy. The portable library has a separate game-focused allowlist.

## Unit C — verify lookup and escalation through the normal entry points

When the work profile identifies the domain, the specialist reuses the information brief or asks knowledge with that domain. If a task spans domains, pass the relevant domains together, for example planning and game for a combat economy decision. Read a candidate's scope and evidence before adopting it. If no usable entry answers the question, inspect governing project sources, including project-specific guides and approved specifications. If consequential evidence is still missing, hand the focused question to research and return its source, conditions or remaining gap to the calling operation. A missing vendor measurement stays open until the vendor evidence supports a value. Simple text refinements continue directly.

| Trial | Pass condition |
| --- | --- |
| Two observed Korean questions, unfiltered and with the intended domain | Each proposed entry is first for its own question in the real store. Add these as named regressions and exercise a Korean paraphrase per topic. Inspect the selected passage and its effect on the result. |
| Empty-domain fixture containing a plausible hit in an unrelated domain | Filtered lookup returns zero. The consumer identifies the gap and uses an authoritative source or records the unresolved dependency. A matching word in the other domain cannot establish the conclusion. |
| Cross-domain game plan and one local wording edit | The plan can use both supported domains; the text-only edit finishes without initiating research. |
| Image brief needing project identity and supplier-specific constraints, direct and via Scout | Both routes use the actual project identity and the correct vendor specification. With the latter withheld, neither supplies an invented number. A generic image-knowledge entry is unnecessary for a vendor-specific fact. |
| A presentation claim requiring an external primary source | Direct invocation and Scout both use the project context and substantiate the claim with the primary source through the research step. File lookup and a correct-looking number alone are insufficient. |

Rerun the current [retrieval regression set](../../skills/vegabond-knowledge/tests/retrieval_cases.json) with its existing required and forbidden IDs. Keep the normal unfiltered CLI contract and result schema. If one of the two known questions still misses after capture, inspect the actual matched fields and Korean expression, refine that entry and retest. Consider general ranking changes only for a reproduced failure that content and domain selection cannot resolve. If a specialist demonstrably bypasses this path, change that caller or its shared handoff and repeat the direct and Scout trials.

Unit A and the two knowledge captures address independent failures. Validate A before publishing new distributions. Validate B before interpreting the end-to-end results in C. The design is ready to implement; the proposed packaging failures, content checks and behavioral trials remain implementation acceptance criteria.

## Implementation and acceptance results · 2026-11-25

The independent source check reproduced three stale files and two omissions per format before the rebuild. After rebuilding, all 35 canonical skill documents matched each distribution. The seven portable tests passed, including the shared-omission, stale-section and duplicate-section fixture and navigation to both image references after installation and relocation. The builder also picked up seven existing game detail updates, their index and the current ZIP search helper (line endings only). The curated library membership stayed the same.

The two domain entries and their catalogs passed strict validation. At first the planning paraphrase returned an unrelated code entry globally and nothing within planning. The helper kept the Korean inflections in the query; adding natural expressions for the beneficiary's change and the effect being observed to the entry resolved both cases. The final [real-store evaluation](../../skills/vegabond-knowledge/tests/retrieval_cases.json) passed 37/37 with zero forbidden hits. Both original questions and both paraphrases ranked first in global and scoped lookup. A separate temporary-project test verified that a plausible game hit produces an explicit gap when scoped to empty planning.

| Read-only task | Decision observed in the trial |
| --- | --- |
| Planning, workshop proposal | The performer applied K-PLAN-OUTCOME-INDICATOR to replace attendance as the success criterion with independent completion of the same kind of task before and after training. It specified the denominator, missing participants and data collection. The follow-up time was a proposal and the target was left open. |
| Procurement slide, direct and via Scout | Both read the project caption specification and consulted the W3C primary source. With the supplied 3.9:1 for 14 pt regular text, both recommended holding release and retesting after adjustment against 4.5:1. The direct performer also documented using K-PRES-DECISION-SLIDE; the Scout performer documented using the project entry. The delivered result was slide copy. |
| Sticker brief, direct and via Scout | Initial direct runs produced correct copy but did not report using the shared procedure. After linking the conditional route from the image entry, fresh performers used the stored character identity and checked the current sheet: 19 mm display-width check and 2.7 mm finished cut-line separation, including interior cuts. With that sheet withheld, fresh performers on both routes consulted research, retained the design rules and left the manufacturing dimension open. |
| Game plan and local spacing edit | The mixed-domain trial applied both economy and capacity entries, recalculated 3,000 versus 6,000 coins/hour under the stated zero-downtime assumption and kept actual demand open. The text-only control inserted one space without looking up domain knowledge or initiating research. |

The trials used separate AI contexts and synthetic project inputs. They establish the observed decisions in these requests. They do not establish physical print quality, audience comprehension or game balance. To rerun the automated checks from the repository root:

```text
python -m unittest portable.test_portable
python skills/vegabond-knowledge/scripts/search.py evaluate --project . --cases skills/vegabond-knowledge/tests/retrieval_cases.json --no-cache
python skills/vegabond-knowledge/scripts/catalog.py check --project . --store knowledge --domain planning --domain presentation --strict
python -m unittest discover -s skills/vegabond-knowledge/tests
```

## Research material migrated to knowledge

Use this crosswalk to find a decision by its former report name. The entries carry the applicable guidance, sources and checks. The [pre-migration revision](https://github.com/earthboom/OneStep/tree/558f90b3a61a4f16a69edc269698d991ef80725f/docs/research) retains the original narrative and translations. The [retrieval measurements](https://github.com/earthboom/OneStep/tree/9f553ba95ec7209a5bf3fcc6ab16b119ebeb8317/docs/research) and [glossary trials](https://github.com/earthboom/OneStep/tree/9f553ba95ec7209a5bf3fcc6ab16b119ebeb8317/docs/research) are available in that revision.

| Former report | Knowledge entries |
| --- | --- |
| `2026-11-21-ai-codebase-quality` | [K-CODE-AI-CHANGE-QUALITY](../../knowledge/code/K-CODE-AI-CHANGE-QUALITY.md) |
| `2026-11-21-cpp-game-framework` | [K-CODE-CPP-GAMEPLAY-FRAMEWORK](../../knowledge/code/K-CODE-CPP-GAMEPLAY-FRAMEWORK.md) |
| `2026-11-22-game-data-formats-and-pipeline` | [K-GAME-CONTENT-FORMATS](../../knowledge/game/K-GAME-CONTENT-FORMATS.md) |
| `2026-11-22-game-data-management-methods` | [K-GAME-CONTENT-PRODUCTION](../../knowledge/game/K-GAME-CONTENT-PRODUCTION.md) |
| `2026-11-22-game-development-practices` | [K-GAME-NPC-SIMULATION](../../knowledge/game/K-GAME-NPC-SIMULATION.md) · [K-GAME-RUNTIME-RESOURCE-BUDGET](../../knowledge/game/K-GAME-RUNTIME-RESOURCE-BUDGET.md) · [K-GAME-CONTENT-FORMATS](../../knowledge/game/K-GAME-CONTENT-FORMATS.md) |
| `2026-11-22-gameplay-regression-verification` | [K-GAME-GAMEPLAY-REGRESSION](../../knowledge/game/K-GAME-GAMEPLAY-REGRESSION.md) |
| `2026-11-22-image-generation-skill-plan` | [K-IMAGE-BRIEF-ACCEPTANCE](../../knowledge/image/K-IMAGE-BRIEF-ACCEPTANCE.md) |
| `2026-11-22-stage-content-framework` | [K-GAME-STAGE-AUTHORING](../../knowledge/game/K-GAME-STAGE-AUTHORING.md) |
| `2026-11-22-unity-csharp-game-framework` | [K-CODE-UNITY-GAMEPLAY-FRAMEWORK](../../knowledge/code/K-CODE-UNITY-GAMEPLAY-FRAMEWORK.md) |
| `2026-11-23-2d-character-art-and-sprites` | [K-GAME-SPRITE-PRODUCTION](../../knowledge/game/K-GAME-SPRITE-PRODUCTION.md) |
| `2026-11-23-2d-effects-and-motion` | [K-GAME-EFFECT-EVENT-PLAYBACK](../../knowledge/game/K-GAME-EFFECT-EVENT-PLAYBACK.md) |
| `2026-11-23-2d-sprites-animation-and-stage-dialogue` | [K-GAME-SPRITE-PRODUCTION](../../knowledge/game/K-GAME-SPRITE-PRODUCTION.md) · [K-GAME-STAGE-DIALOGUE](../../knowledge/game/K-GAME-STAGE-DIALOGUE.md) |
| `2026-11-23-game-feel-and-impact-feedback` | [K-GAME-IMPACT-FEEDBACK](../../knowledge/game/K-GAME-IMPACT-FEEDBACK.md) |
| `2026-11-23-knowledge-and-incident-retrieval` | [K-SHARED-INCIDENT-RETRIEVAL](../../knowledge/shared/K-SHARED-INCIDENT-RETRIEVAL.md) |
| `2026-11-23-korean-retrieval-at-30000` | [K-CODE-RETRIEVAL-SCALE](../../knowledge/code/K-CODE-RETRIEVAL-SCALE.md) |
| `2026-11-24-development-design-and-delivery` | [K-CODE-DESIGN-DELIVERY-SCOPE](../../knowledge/code/K-CODE-DESIGN-DELIVERY-SCOPE.md) |
| `2026-11-25-design-review-and-cross-check` | [K-CODE-ACTIVE-DESIGN-REVIEW](../../knowledge/code/K-CODE-ACTIVE-DESIGN-REVIEW.md) · [K-CODE-DESIGN-VALIDATION-EVIDENCE](../../knowledge/code/K-CODE-DESIGN-VALIDATION-EVIDENCE.md) |
| `2026-11-25-development-glossary-field` | [K-CODE-ACCEPTANCE-GLOSSARY](../../knowledge/code/K-CODE-ACCEPTANCE-GLOSSARY.md) |
| `2026-11-25-development-glossary-pilot` | [K-CODE-ACCEPTANCE-GLOSSARY](../../knowledge/code/K-CODE-ACCEPTANCE-GLOSSARY.md) |
| `2026-11-25-glossary-first` | [K-CODE-ACCEPTANCE-GLOSSARY](../../knowledge/code/K-CODE-ACCEPTANCE-GLOSSARY.md) |
| `2026-11-25-stationery-character-image-generation` | [K-IMAGE-STATIONERY-MASCOT](../../knowledge/image/K-IMAGE-STATIONERY-MASCOT.md) |
| `2026-11-24-2d-props-bursts-and-particles` | [K-GAME-PROP-BURST-PARTICLE-SPRITES](../../knowledge/game/K-GAME-PROP-BURST-PARTICLE-SPRITES.md) |
| `2026-11-24-game-ui-image-production` | [K-GAME-UI-ART-PRODUCTION](../../knowledge/game/K-GAME-UI-ART-PRODUCTION.md) |
