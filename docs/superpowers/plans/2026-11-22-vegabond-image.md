# Vegabond Image Implementation Plan

**Goal** — Add the OneStep image specialist and measure request fidelity against stock Codex `imagegen` on real images.

**Spec** — [Image brief and acceptance criteria](../../../knowledge/image/K-IMAGE-BRIEF-ACCEPTANCE.md)

**Architecture** — Scout selects the specialist. `vegabond-image` owns acceptance criteria, visual direction, and diagnosis. The built-in `imagegen` skill supplies the raster execution path in both benchmark arms. Store benchmark inputs, outputs and scores under `output/vegabond-image-comparison/`.

1. Freeze 12 user-facing cases, shared references, acceptance checks and budget before scoring. Run a built-in generation probe on the open-ended case before authoring the new skill. Record the returned image or exact tool failure.
2. Add `skills/vegabond-image/SKILL.md`, a Korean translation without discovery metadata, and optional style and review examples. Add a specialist row to both Scout and README versions. Validate frontmatter, link targets, and routing. Preserve existing workspace changes.
3. Run both workflows with the same cases and references twice. Record first and final outputs, actual prompts, and correction calls. Use isolated generation contexts where supported. Score anonymized output against frozen checks. Mark missing results separately from generated failures. Report completed pairs, denominators, fidelity and repair calls, and preserve the artifacts for review.
