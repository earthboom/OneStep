---
id: K-CODE-DESIGN-DELIVERY-SCOPE
title: "Choose design depth and delivery stages from the risk each check resolves"
summary: "Describe the changed behavior and neighboring guarantee, then stage delivery where evidence can change the next decision or compatibility requires coexistence."
kind: method
scope: "Software and game changes with unsettled invariants, compatibility windows or player and production assumptions"
keywords: ["design depth", "delivery stages", "scope", "vertical slice", "parallel change", "small batches", "설계 깊이", "작업 분할", "단계별 구현", "범위 설정", "호환 기간"]
status: active
checked_at: 2026-11-24
---

# Choose design depth and delivery stages from the risk each check resolves

## Guidance

Describe the user or caller, the change they can observe, an adjacent guarantee and any supplied budget. Spend design effort on an unresolved choice with a costly consequence. Express it as a stimulus, environment and expected response, such as opening the last committed checkpoint after interruption and restart. Record who owns the invariant and what evidence could reverse the choice. Significant commitments merit a brief account of their context, cost and reopening condition. [Basecamp, setting boundaries](https://basecamp.com/shapeup/1.2-chapter-03) · [writing a pitch](https://basecamp.com/shapeup/1.5-chapter-06) · [Boehm, risk-driven spiral development](https://resources.sei.cmu.edu/asset_files/specialreport/2000_003_001_13655.pdf) · [SEI Quality Attribute Workshop](https://insights.sei.cmu.edu/documents/2542/2018_010_001_513488.pdf) · [Nygard, decision records](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions)

## Applicability and exceptions

Ask what intermediate result can be checked and which later decision depends on it. Keep debit, credit, notification and tests in one unit when they enforce one atomic transfer. A change can span modules and still have one coherent check. A well-understood format change can require several units when independently deployed clients coexist. Identify the readers, writers, rollback path and condition for retiring compatibility. [Parnas, information hiding](https://www.cs.lafayette.edu/~gexia/cs301/resources/parnas.html) · [DORA, small batches](https://dora.dev/capabilities/working-in-small-batches/) · [Google, self-contained changes](https://google.github.io/eng-practices/review/developer/small-cls.html) · [Sato, Parallel Change](https://martinfowler.com/bliki/ParallelChange.html)

## Checks

- Move a clip across two tracks, inject failure after removal and verify one undoable transaction. In a save migration, exercise old → new → old → new so the older writer's effect is visible. For a label edit follow the edited resource. A plain empty-state string needs a text and display check. A menu mnemonic warrants checking the rendered key and its old and new bindings. [Scope and delivery procedure](../../skills/vegabond-code-design/references/scope-and-delivery.md)
- For twelve planned rooms, an uncoached first-time player's choice and explanation at one greybox junction can challenge a cue. An authored room built, loaded and played through the production pipeline answers a different feasibility question. Agree on what outcome would change the design before repeating production across the remaining rooms. One room does not complete or validate the other eleven. [MDA](https://users.cs.northwestern.edu/~hunicke/MDA.pdf) · [Outer Wilds GDC session](https://gdcvault.com/play/1027008/Independent-Games-Summit-Sparking-Curiosity) · [speakers' slides](https://media.gdcvault.com/GDC%2B2021/beachum_gdc_2021%281%29.pdf) · [Ismail, Prototypes & Vertical Slice](https://ltpf.ramiismail.com/prototypes-and-vertical-slice/)

## Evidence

The native C++ tactics fixture added a second optional encounter pack while retaining the baseline build script and gameplay source. This supports one author-and-play cycle for an ordinary variant using that extension point. In a separate search example, all five per-round P95 values passed while seven individual responses exceeded the limit. A change to acceptance required a different test and profiling decision. [Recorded tactics workflow](../../docs/examples/cpp-gameplay-workflow/native-tactics/WORKFLOW.md) · [file comparison](../../docs/examples/cpp-gameplay-workflow/native-tactics/evidence/baseline-vs-extension.json) · [search benchmark](K-CODE-RETRIEVAL-SCALE.md)

In a forward trial a fresh reader proposed the clip transaction, compatibility round trip and one-junction playtest on hypothetical briefs. Its label-only plan also exercised an unrelated export command. After the binding check was clarified, another reader selected different checks for the plain string and menu mnemonic. These were proposed design checks, with no execution of a migration, player observation or measurement of team productivity.
