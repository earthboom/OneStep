---
id: "K-IMAGE-BRIEF-FIDELITY"
title: "Check generated and edited images against visible brief requirements"
summary: "Set observable checks for composition, style, text and preservation before generating. Choose a repair based on the visible failure and evaluate first and final deliveries separately."
kind: "method"
scope: "Raster image generation and editing with request-specific constraints, multiple references, exact copy or protected regions"
keywords: ["image generation","brief fidelity","reference roles","image edit","imagegen","Korean type","visual validation","이미지 생성","요구 준수","참조 이미지","부분 수정","한글 타이포"]
status: "active"
checked_at: "2026-11-26"
---

# Check generated and edited images against visible brief requirements

## Guidance

Use one image workflow with generation, reference-guided generation and editing routes into the same imagegen tool. For each brief, record mandatory visible requirements, reference roles such as layout, identity and style, and which areas an edit must preserve. Add style checks that affect what the viewer can see. Photography may depend on viewpoint, light and texture. Comics may depend on a readable silhouette and line/shading hierarchy. A surreal brief may require one impossible relation to read clearly while shadows and spatial cues remain coherent.

Regenerate when framing or the interpretation is wrong. For a local issue, correct the smallest area and inspect the previously passing conditions again. Where allowed, set exact copy as editable type and verify spelling, spacing, accents and punctuation. Check output dimensions and transparency from the file. Check actual transparent background pixels as well as the presence of alpha. If output is resized, check framing and placement again. Mark any unverified mandatory condition as unresolved. [Vegabond Image](../../skills/vegabond-image/SKILL.md)

## Applicability and exceptions

For exploratory concepts use [creative exploration](K-IMAGE-CREATIVE-EXPLORATION.md). Compare subjective finish by showing matched outputs to a reviewer. A small requirements comparison cannot establish broad aesthetic preference.

## Checks

The proposed comparison fixed 12 cases. Three treatments used one lunar brief. The others covered open generation, counted objects and color binding, exact Korean poster copy such as “달 기지에 오신 것을 환영합니다!”, a 512 × 512 transparent PNG, a sketch, one character across two scenes, multiple reference roles, a background edit and a clothing-color edit. Compare two workflows and two repeats per case for 48 jobs. Match inputs, conditions and allowed calls. Blind the reviewer. Score initial delivery, final delivery and correction calls separately. Prefer a workflow with more final mandatory passes, no critical text or preservation regressions and no increase in median repair calls.

## Evidence

The OneStep comparison recorded 48 jobs across four execution contexts. One AI reviewer scored 54 blinded candidates. Initial delivered pass counts were 20/24 and 22/24 for baseline and skill. Final counts were 23/24 and 24/24, with six and two correction calls respectively and a median of zero in both. Both routes passed the exact Korean text and preservation cases. The skill route typeset the poster after generation. The hardest final case was exact top-down product framing. Model build and matched seeds were unavailable. The comparison did not run each job in a fresh chat or measure human preference. [Cases](../../output/vegabond-image-comparison/cases.md) · [Run and results](../../output/vegabond-image-comparison/results.md) · [Metrics](../../output/vegabond-image-comparison/metrics.json) · [Blind scores](../../output/vegabond-image-comparison/review-scores.json)

GenEval and T2I-CompBench++ support evaluating count, attributes and spatial relations independently. TIFA uses visual questions for visible claims. GIE-Bench evaluates edit success and preservation. PromptCharm and ControlNet illustrate iterative or spatially constrained authoring. These sources motivate review criteria and reference roles. They do not measure the OneStep workflow.

- Evaluation methods · [GenEval](https://arxiv.org/abs/2310.11513) · [T2I-CompBench++](https://arxiv.org/abs/2307.06350) · [TIFA](https://arxiv.org/abs/2303.11897) · [GIE-Bench](https://arxiv.org/abs/2505.11493)
- Reference use and edits · [PromptCharm](https://arxiv.org/abs/2403.04014) · [ControlNet](https://arxiv.org/abs/2302.05543) · [GPT Image prompting](https://developers.openai.com/api/docs/guides/image-prompting) · [Image generation limitations](https://developers.openai.com/api/docs/guides/image-generation#limitations) · [Composition sketch](https://www.adobe.com/learn/firefly/web/sketch-to-ai-generated-image) · [Separate layout and style references](https://www.adobe.com/learn/firefly/web/firefly-boards-to-photoshop-workflow) · [Porto workflow interview](https://www.creativebloq.com/3d/ai-has-amplified-my-20-years-of-experience-believes-concept-artist-daniel-porto) · [Editable type layers](https://helpx.adobe.com/photoshop/desktop/text-typography/type-layers-creation/type-layers-in-photoshop.html)
- Treatment references · [Nikon field of view](https://www.nikon.co.uk/en_GB/learn-and-explore/magazine/tips-and-tricks/what-is-focal-length-in-photography-a-guide-for-beginners) · [Animation Mentor staging](https://www.animationmentor.com/blog/tutorial-use-character-staging-to-guide-viewer-focus/) · [MoMA Surrealism](https://www.moma.org/collection/terms/surrealism/surrealist-objects-and-assemblage)
