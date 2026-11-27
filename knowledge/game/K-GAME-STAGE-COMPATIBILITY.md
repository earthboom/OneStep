---
id: "K-GAME-STAGE-COMPATIBILITY"
title: "Keep stage identity stable as content and progression change"
summary: "Separate stage definitions, discovery, progression, runtime state and saved results. Test stage additions and retirement against previous saves and the shipping entry path."
kind: "method"
scope: "Games that add, reorder, revise or remove stages, campaigns, or optional packs"
keywords: ["StageId","stage catalog","progression","save migration","retired content","replay","스테이지 추가","진행도","저장 호환성","리플레이"]
status: "active"
checked_at: "2026-11-26"
---

# Keep stage identity stable as content and progression change

## Guidance

Give every stage a stable StageId independent of display order, name or asset path. The definition owns editable content and references. The catalog owns lookup and distribution. Progression decides availability and unlocks. The runner creates a fresh session and publishes its outcome. The save layer owns committed completion, rewards and records keyed by stable ID. Keep mutable play state out of shared definitions.

Add a stage by creating a definition, validating genre-specific requirements, registering it and following the actual listing → unlock → enter → retry or exit → finish flow. Confirm the result is committed once. Reordering or renaming preserves IDs. Retiring a stage requires an explicit history display, replacement or migration rule. Preserve replay context when supported by recording the stage and content versions and, where applicable, the generator, seed and input sequence.

## Applicability and exceptions

Choose record and replay compatibility separately from save compatibility when collision or timing changes invalidate old results. A valid old completion can survive even if its replay cannot run. Keep an archived fixture from a supported released build to test migration and missing-pack behavior. Use [save technology guidance](K-GAME-TECH-SAVE.md) for platform-specific persistence.

## Checks

Move an existing stage within the catalog and confirm its completion, then enter and finish a new stage from a real menu with the old save. Try a blocked puzzle move, a skipped racing checkpoint or a tactics layout with an invalid spawn as appropriate. Test retry and a second entry, followed by reading a migrated save again. Check the shipping build for missing assets, optional packs and the expected policy for retired IDs. [Verification scope](K-GAME-REGRESSION-SCOPE.md)

## Evidence

The stage framework covers state owners, genre-specific units and production checks. The format and management reports document versioned stage content, saves, procedural generation and content packs. Example stages are proposals to verify in the target project. [Stage framework](K-GAME-STAGE-AUTHORING.md) · [Format and save changes](K-GAME-CONTENT-FORMATS.md) · [Management methods](K-GAME-CONTENT-PRODUCTION.md)
