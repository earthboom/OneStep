---
id: K-IMAGE-BRIEF-ACCEPTANCE
title: "How can a generated image or local edit be checked against the brief?"
summary: "Translate mandatory counts, attributes, positions, wording and edit boundaries into observable checks. Inspect the delivered file and choose the smallest repair that addresses a failed condition."
kind: method
scope: "Raster generation, image editing and matched workflow comparisons"
keywords: ["image generation","image editing","attribute binding","composition","preservation","exact text","alpha transparency","이미지 생성","부분 편집","원본 보존","정확한 한글 문구","구도","개체 수"]
status: active
checked_at: '2026-11-25'
---

# How can a generated image or local edit be checked against the brief?

## Guidance

Separate a brief's mandatory features from preferences. Ask “Are both lights attached to the entrance?”, “Which side of the frame contains the rover?” and “Is any background figure also a robot?” Specify whether left means screen-left or the subject's left. Judge what happens in the scene independently of the rendering medium. A floating building can be photographed with internally consistent shadows. For a photo, check perspective, shadows and materials. For a comic, shrink to panel size and check silhouettes and focal order. For an impossible scene, check the visual cue that makes the intended exception legible. [GenEval](https://arxiv.org/abs/2310.11513) · [T2I-CompBench++](https://arxiv.org/abs/2307.06350) · [TIFA](https://arxiv.org/abs/2303.11897) · [Nikon on field of view and focal length](https://www.nikon.co.uk/en_GB/learn-and-explore/magazine/tips-and-tricks/what-is-focal-length-in-photography-a-guide-for-beginners) · [Animation Mentor staging demonstration](https://www.animationmentor.com/blog/tutorial-use-character-staging-to-guide-viewer-focus/) · [MoMA on Surrealism](https://www.moma.org/collection/terms/surrealism/surrealist-objects-and-assemblage)

Assign each reference a job, such as subject identity, camera/layout, pose or rendering. When placement matters, supply a blocking sketch. For an edit, identify both the requested change and details that must survive, then place the source and delivery side by side. Offer distinct treatments when the brief leaves that choice open. [GIE-Bench](https://arxiv.org/abs/2505.11493) · [PromptCharm](https://arxiv.org/abs/2403.04014) · [ControlNet](https://arxiv.org/abs/2302.05543) · [Composition sketch video and transcript](https://www.adobe.com/learn/firefly/web/sketch-to-ai-generated-image) · [Porto interview](https://www.creativebloq.com/3d/ai-has-amplified-my-20-years-of-experience-believes-concept-artist-daniel-porto) · [Skateboard production video and transcript](https://www.adobe.com/learn/firefly/web/firefly-boards-to-photoshop-workflow)

## Applicability and exceptions

Scale the checks to the brief. A mask, pose-control strength or fixed seed depends on the selected generator. The papers provide evaluation dimensions and examples from particular systems. Aesthetic preference requires separate judgment. [Prompt guide](https://developers.openai.com/api/docs/guides/image-prompting) · [Generation documentation](https://developers.openai.com/api/docs/guides/image-generation#limitations)

## Checks

1. For every mandatory check, record met, failed or unverified. Enlarge lettering, compare spaces, punctuation and line breaks with the supplied copy, and decode the exported dimensions, format and alpha. Inspect transparent areas and edges over contrasting backgrounds after resizing or cropping.
2. For a wrong view or framing, change the camera cues or sketch and regenerate. For a local defect, edit the last accepted image and inspect adjacent features again. When the deliverable permits layout, reserve space, typeset exact text and inspect the export. On a depicted surface, check perspective and texture. [Photoshop type layers](https://helpx.adobe.com/photoshop/desktop/text-typography/type-layers-creation/type-layers-in-photoshop.html)
3. To compare workflows, fix briefs, references, budgets and checks before generating. Blind the reviewer to the route. Score first delivery and accepted repair separately, count calls including discarded attempts and retain failures by condition.

## Evidence

In a 12-brief, two-repeat comparison with the same image tool, baseline and guided routes passed all conditions on 20/24 and 22/24 first deliveries, then 23/24 and 24/24 final deliveries. A subsequent focused revision reached 24/24 first deliveries across the repeated suite while edit calls increased from two to five. The first-delivery measure includes planned sizing or typesetting. The small suite, AI reviewer and unavailable seed/build limit generalization. [Fixed cases](../../output/vegabond-image-comparison/cases.md) · [Initial comparison](../../output/vegabond-image-comparison/results.md) · [Regression](../../output/vegabond-image-comparison/full-regression/results.md) · [Image workflow](../../skills/vegabond-image/SKILL.md)
