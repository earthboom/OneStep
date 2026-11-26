---
id: "K-GAME-CONTENT-AUTHORING"
title: "Choose a source of truth and a repeatable game-content build"
summary: "Choose authoring tools around the people editing content, validate structural and game-specific rules, and regenerate delivery data from its authoritative source."
kind: "method"
scope: "Stage, balance, dialogue and packaged content in Unity, Unreal or an engine-independent pipeline"
keywords: ["content pipeline","authoring","JSON Schema","semantic validation","CSV","ScriptableObject","Data Asset","content pack","게임 데이터","콘텐츠 제작","시맨틱 검증","임포트"]
status: "active"
checked_at: "2026-11-26"
---

# Choose a source of truth and a repeatable game-content build

## Guidance

Identify who edits each dataset, which representation is authoritative, and whether its lifetime is authoring, build, session or save. Choose sheets or CSV for flat balance and localization tables and emit typed data on import. Choose versioned JSON when content is nested, needs readable diffs or must move between tools. Use ScriptableObjects or Unreal Data Assets for editor-authored references and spatial work. Keep workspace paths and direct engine references behind the importer or catalog boundary when content must also load outside that editor.

Validate the schema first, then validate unique IDs, referenced assets, condition graphs and genre rules such as a reachable exit. Report the file, object ID and field that failed. Regenerate derived assets and manifests from the edited source. For procedural content, capture seed, generator version and input configuration with the output.

## Applicability and exceptions

A single file format need not serve authoring, rendering and persistence. Use a database or event history when durable querying or reconstruction warrants it. Add a restricted script or declarative language when conditions and branching have outgrown tables. Document available operations and side effects. For optional packs, declare dependencies and supported versions in the manifest and check that unloading or omitting the pack works as intended.

## Checks

Import from a clean checkout and import the same change incrementally. Compare IDs and references, regenerate without content drift, and run the shipping catalog in a target build. Reject a well-formed file containing a duplicate ID or broken reference, and try one pack without its optional neighbors. For save and record compatibility, use [stage identity and compatibility](K-GAME-STAGE-COMPATIBILITY.md).

## Evidence

The format survey documents the JSON schema/semantic split and Unity/Unreal import paths. The management survey compares typed spreadsheets, editor assets, scripting, procedural builds, event histories and packs. Apply the choice to the target project and measure the authoring and import costs there. [Formats and pipeline](../../docs/research/2026-11-22-game-data-formats-and-pipeline.md) · [Management methods](../../docs/research/2026-11-22-game-data-management-methods.md) · [Data lifetimes](../../docs/research/2026-11-22-game-development-practices.md#1-data-lifetimes-and-change-contracts)
