---
name: vegabond-fiction
description: Use when drafting, revising, critiquing, or investigating fictional manuscripts, coordinating narrative design when needed and checking story context, voice, and continuity.
---

# Vegabond Fiction

Write and revise fiction within the active operation. Reuse its brief and task profile; follow the [agent instructions](../../agents/vegabond-agent.md) for common boundaries and completion. If invoked directly, use [scout's shared setup](../vegabond-scout/SKILL.md#frame-and-classify) and its linked operation without restarting classification.

## Gather the relevant story context

Use the shared [information-needs judgment](../vegabond-scout/references/information-needs.md) to derive questions from the actual scene and edit, including relevant causal, knowledge and disclosure dependencies beyond its genre label. Keep canon, author preference, character belief and provisional invention distinct when adopting retrieved material.

Before drafting or revising a scene, request focused context through [vegabond-knowledge](../vegabond-knowledge/SKILL.md), reusing the current information brief. Identify the work and revision, chapter/scene, story time, viewpoint, involved characters and aliases, location, and intended events where known. Missing values are gaps, not invitations to invent facts.

Use the work's existing setting documents, character/relationship notes, timeline, relevant manuscript passages, and author decisions as sources. Follow the knowledge skill's scoped index-to-detail retrieval; search by work and entity names/aliases, then scene/time and relevant questions. Expand to connected characters or events only when needed for a dependency or conflict. Include supporting characters whose actions matter; narrative prominence alone does not determine relevance. Reuse valid context rather than rereading all setting files for every scene.

Return the scene-relevant facts with source locations, applicability, and gaps in the existing information brief:

| Context | Retrieve and check when relevant |
| --- | --- |
| World and place | Rules, exceptions, capabilities and costs, geography, travel, and scene constraints. |
| Characters | Identity, names/aliases, roles, goals, traits, voice, abilities, and current physical/emotional state. |
| Relationships | Who feels, believes, owes, or knows what about whom; direction, changes, and when they take effect. Do not assume mutual feelings or symmetric knowledge. |
| Timeline and disclosure | Event order, location and state at this scene, character knowledge and how it was acquired, reader-visible information, and planned reveals. |
| Voice references and corrections | Author-written or author-selected passages, explicit style choices, and relevant verified before/after corrections for this work, narrator, or character; retain source locations and exceptions. |

Use those references to keep a short voice baseline in the existing brief: what the narrator notices or omits, degree of emotional explanation, dialogue/action/description balance, diction and imagery, rhythm, and room for reader inference. Distinguish observed patterns from author-confirmed preferences. If no baseline exists, derive a provisional direction from the request and a short sample within the current work; refine it through available author feedback without adding a routine approval gate. A baseline guides choices, not identical sentence patterns in every scene.

Verify consequential summaries against their original passages. Follow explicit author decisions and declared source authority; do not resolve a disagreement merely by choosing the newest file. Distinguish established canon, provisional plans/new inventions, in-world beliefs or rumors, and unknowns. A future event or relationship must not be applied to an earlier scene, and author knowledge must not silently become character or reader knowledge. Mark conflicting sources with the affected fact and scene; investigate, or clarify material unresolved intent before dependent writing while continuing independent work.

Reuse an existing story bible rather than creating a competing copy. When authorized knowledge storage is useful, use the existing fiction domain and storage format: put the work boundary in `scope`, names/aliases in `keywords`, and relevant revision/time conditions in `context` or the body. Link original sources instead of copying entire profiles; an `active` knowledge entry is not by itself author-confirmed canon. Do not fabricate setting entries when no story material is supplied.

## Choose the design depth

Use [vegabond-fiction-design](../vegabond-fiction-design/SKILL.md) when a new work/arc, linked scenes, character motivation or change, viewpoint/disclosure, setups/payoffs, or a structural revision needs consequential narrative choices. Pass the existing brief, relevant canon/manuscript and voice baseline, constraints, and open questions. Reuse a valid design; revisit only choices affected by evidence. A clear local scene or line edit can state its purpose and preservation conditions inline without a separate design pass. Exploratory drafting can inform a provisional design; do not require a finished plot or a fixed story formula before every passage.

Design returns choices and intended effects within this workflow, not a second execution loop. A design-only request ends with that artifact rather than an unsolicited manuscript. Retrieve existing context through the section above; design must not create a competing story bible.

## Draft or revise

Establish genre, audience, realism, viewpoint, tense, narrator reliability and intended uncertainties from the request and relevant sources. Apply the work's baseline and scoped author choices, distinguishing established facts from proposed invention. Read [manuscript review and correction](references/review.md) before judging or revising prose, and apply it to the actual final text before handoff.

- **Create:** Use the design or inline scene purpose, character intent, pressure and change where relevant. Draft action, dialogue and exposition in the requested voice and viewpoint; respect deliberate ambiguity and form. Return discoveries that materially alter the intended sequence or effect to fiction-design without silently rewriting canon.
- **Revise:** Diagnose at the structural, scene, continuity or sentence level. Repair the earliest established causal problem within the requested scope, preserving facts and effective passages. If it changes linked narrative choices, update that part of the design before dependent rewriting. Use the reference's finding classification and correction loop; more explanation is not automatically improvement.
- **Research or critique only:** Ground findings in passages and distinguish textual evidence, interpretation and proposed invention. Verify the analysis without rewriting the source or promoting an interpretation to canon.

## Hand back

Return the requested text or analysis, important choices, review/correction evidence and unresolved conditions to the active operation. The review reference owns the detailed checks, uncertain judgments, style and recurrence evidence, and final rereading. Send useful findings through knowledge within the existing write scope; do not create a separate style store or new record schema. Distinguish AI review from vagabond's independent acceptance under the common instructions.
