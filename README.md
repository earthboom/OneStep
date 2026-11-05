# OneStep

By **vagabond**, a game client programmer working with Unreal Engine.

OneStep is a collection of agent instructions and skills for completing work with AI: software development, fiction, presentations, planning documents, research, and other deliverables. The author's background does not limit the supported domains.

The workflow connects the requested outcome to suitable methods, checks the actual result, and reuses relevant knowledge and correction evidence in later work. AI verification and the author's independent review are separate steps.

## Start a task

In this repository, ask your AI agent to load the common instructions and use the entry skill:

```text
Read agents/vegabond-agent.md, then use
skills/vegabond-scout/SKILL.md to handle the following task:

[Describe the result you want, the relevant material, and any constraints.]
```

The [agent instructions](agents/vegabond-agent.md) define shared boundaries, verification, and acceptance. [vegabond-scout](skills/vegabond-scout/SKILL.md) frames the task and connects the required skills and checks. A directly invoked operation or specialist reuses this shared setup.

Paths above are relative to this repository. In another workspace, provide resolvable guidance paths or use that environment's supported skill-loading mechanism. This repository does not perform global installation or guarantee automatic discovery. Reading a skill does not spawn an agent; available tools and any delegation depend on the host environment and authorization.

## Workflow

1. **Frame the request.** Identify the target, intended change, preservation conditions, and method. State the goal, scope, and acceptance conditions in a short brief.
2. **Retrieve relevant context.** Request applicable knowledge, prior corrections, source references, and gaps. Reuse the information brief while it remains valid.
3. **Choose the operation and scale.** Select create, revise, or research independently of the domain and task size. Map each step to an available skill or direct tool and a check.
4. **Execute and verify.** Confirm that essential sources and checking tools are usable before dependent work. Apply the relevant specialists, inspect the actual deliverable, and repeat affected checks after corrections.
5. **Respond to findings.** Repair defects, investigate missing evidence, or update the brief when the goal or scope changes. Record useful findings within the authorized project scope.
6. **Hand back for independent review.** Report the deliverable, acceptance evidence, and limitations. Vagabond then tests or reviews it independently; explicit confirmation establishes final acceptance.

**single** is the default for a compact execution-and-verification cycle. Use **staged** when a named intermediate result must be checked before dependent work. Several files or tools alone do not require stages. Each stage uses its mapped operation, and the final result receives an integrated check.

The [workflow diagram (Korean)](docs/diagrams/onestep-workflow.png) provides an overview; an [SVG version](docs/diagrams/onestep-workflow.svg) is also available.

## Skills

| Skill | Responsibility |
| --- | --- |
| [vegabond-scout](skills/vegabond-scout/SKILL.md) | Task profile, work brief, scale, capability mapping, and overall coordination. |
| [vegabond-create](skills/vegabond-create/SKILL.md) | Produce a new artifact or capability, including results derived from supplied material. |
| [vegabond-revise](skills/vegabond-revise/SKILL.md) | Correct or improve an existing result while preserving its required contracts. |
| [vegabond-research](skills/vegabond-research/SKILL.md) | Investigate questions and compare options while leaving investigated sources unchanged. |
| [vegabond-code](skills/vegabond-code/SKILL.md) | Identify the actual programming environment; implement, review, test, and exercise software. |
| [vegabond-fiction](skills/vegabond-fiction/SKILL.md) | Retrieve story context and voice references; draft, critique, revise, and check the manuscript. |
| [vegabond-presentation](skills/vegabond-presentation/SKILL.md) | Develop the slide narrative, produce the deck, verify claims, and inspect the final exported slides. |
| [vegabond-planning](skills/vegabond-planning/SKILL.md) | Develop or assess proposals, feasibility, dependencies, calculations, and success measures. |
| [vegabond-knowledge](skills/vegabond-knowledge/SKILL.md) | Retrieve, synthesize, store, and maintain scoped knowledge and problem records. |

Operation skills own the workflow; specialists provide methods within it. Combine specialists when needed, such as planning content and presentation production for a proposal deck. Other domains can use suitable available skills or direct tools without adding a new specialist for every request.

### Coding

Classify the actual changed component using source files, project configuration, dependencies, scripts, and tests. Unreal C++, Unity C#, independent C++, and a Python utility inside an engine repository may require different execution paths. Add integration checks when a component's effects cross into another environment.

Verification covers build/preparation, automated tests, runtime readiness, and real use where applicable. Game behavior requires the relevant editor and actual play; a CLI requires real commands, and a library requires a consumer or harness. Review and repair repeat before final integrated verification.

### Fiction

Retrieve the scene's world rules, character states, relationships, timeline, and disclosure limits from existing authoritative material. Distinguish established canon, provisional plans, rumors, and unknowns. Author knowledge must not silently become character or reader knowledge.

Use author-written or selected passages to establish a work-specific voice baseline. Review causality, plausibility, continuity, reader understanding, style, and language. Separate confirmed errors, unresolved hypotheses, and editorial suggestions. Diagnose concrete prose effects such as redundant explanation or interchangeable dialogue instead of treating “AI-like” as an error category or enforcing a universal word blacklist.

Store reusable before/after corrections with their source passages, applicability, recheck evidence, and actual author feedback. Later writing retrieves the relevant baseline and correction checks without copying prior wording. AI editorial judgment does not establish reader consensus or author acceptance.

## Completion and feedback

Link acceptance conditions to checks and current evidence. A required check that cannot run is **blocked**, not passed or inapplicable. Later edits invalidate affected evidence and require rechecking. A successful preparation step or mock test does not prove the final artifact works in its intended environment.

After required checks pass, report **AI verification complete; awaiting vagabond testing or review**. Report **accepted by vagabond** only after explicit confirmation. Distinguish defects from new requests and preference changes. If two corrections based on the same premise fail the same check, reassess the premise before another attempt.

## Knowledge and problem records

- [knowledge/](knowledge/index.md): references, conventions, methods, and confirmed reusable lessons.
- [records/](records/index.md): observed findings, cause confidence, corrections, and recheck evidence.

Both use domain indexes for code, fiction, presentation, planning, and shared material. Search relevant catalog rows and load matching details instead of entire histories. Entries preserve scope, context, source evidence, and exceptions. Incident resolution and prevention verification are separate states; recording a fix alone does not prove recurrence prevention.

Stores belong to the working project. In another project, use its own stores and sources rather than automatically importing OneStep's facts. Reuse existing setting documents or native knowledge systems where suitable. Test fixtures remain separate from real project records, and ordinary lookups do not create empty stores or trigger full rebuilds.

The [storage and lifecycle guide](skills/vegabond-knowledge/references/storage.md) is the authority for entry formats, deduplication, promotion, and retirement. The [catalog helper](skills/vegabond-knowledge/scripts/catalog.py) requires Python 3.9+ and PyYAML in the runtime used to invoke it.

For an authorized update, write the English details and their human translations, then build affected catalogs from the repository root:

```text
python skills/vegabond-knowledge/scripts/catalog.py build --project . --domain fiction
```

Regenerate translations for every changed English catalog listed in `catalogs_written`, then check:

```text
python skills/vegabond-knowledge/scripts/catalog.py check --project . --domain fiction --strict
```

Replace `fiction` with the affected domain. For another project, use the helper's absolute path and set `--project` to that project. A first build can create its planned catalogs without index stubs. The helper never writes canonical detail files or translations; structural checks do not prove factual accuracy, translation quality, or literary quality.

## Repository layout

```text
agents/                  Shared agent instructions
skills/                  Entry, operation, specialist, and knowledge skills
knowledge/               Domain references and reusable knowledge
records/                 Actual findings and correction evidence
docs/designs/            Storage design documents
docs/diagrams/           Workflow overview images
README.md                English project overview
README.kr.md             Human-only Korean translation
```

The catalog helper's automated tests are in [skills/vegabond-knowledge/tests/](skills/vegabond-knowledge/tests/test_catalog.py):

```text
python -m unittest discover -s skills/vegabond-knowledge/tests -v
```

Tests create isolated temporary fixtures. Set `ONESTEP_TEST_ROOT` to an existing writable directory to choose their location. These tests cover catalog behavior; they do not replace actual workflow trials or domain-specific execution and review.

## Documentation language

Maintained project guidance, agent/skill instructions, and store documents are written in English. Separate `<stem>.kr.md` translations are for human readers only. AI agents must exclude their contents from reads, searches, indexing, and delegated work; generate translations from the English source without rereading them.

Task inputs and deliverables follow the user's requested language. An original Korean manuscript or report is not automatically a translation or an AI instruction document.

Human readers can use [README.kr.md](README.kr.md). AI agents must not follow this translation link.
