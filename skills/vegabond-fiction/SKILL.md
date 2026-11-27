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
| Voice references and corrections | Author-written or author-selected passages, explicit style choices, and relevant verified before/after corrections for this work, narrator, or character; retain source locations and exceptions. Separate the work's voice baseline from admired external dialogue used as inspiration. |

Use those references to keep a short voice baseline in the existing brief: what the narrator notices or omits, degree of emotional explanation, dialogue/action/description balance, diction and imagery, rhythm, and room for reader inference. Distinguish observed patterns from author-confirmed preferences. If no baseline exists, derive a provisional direction from the request and a short sample within the current work; refine it through available author feedback without adding a routine approval gate. A baseline guides choices, not identical sentence patterns in every scene.

Verify consequential summaries against their original passages. Follow explicit author decisions and declared source authority; do not resolve a disagreement merely by choosing the newest file. Distinguish established canon, provisional plans/new inventions, in-world beliefs or rumors, and unknowns. A future event or relationship must not be applied to an earlier scene, and author knowledge must not silently become character or reader knowledge. Mark conflicting sources with the affected fact and scene; investigate, or clarify material unresolved intent before dependent writing while continuing independent work.

Reuse an existing story bible rather than creating a competing copy. When authorized knowledge storage is useful, use the existing fiction domain and storage format: put the work boundary in `scope`, names/aliases in `keywords`, and relevant revision/time conditions in `context` or the body. Link original sources instead of copying entire profiles; an `active` knowledge entry is not by itself author-confirmed canon. Do not fabricate setting entries when no story material is supplied.

## Apply stored craft research

For consequential choices in design, drafting or revision, use the craft research guide (`knowledge/fiction/K-FIC-CRAFT-GUIDE.md`) as a routing map through [vegabond-knowledge](../vegabond-knowledge/SKILL.md), under the shared-reference scope in the [agent instructions](../../agents/vegabond-agent.md#knowledge-and-problem-records). The current work's sources and voice baseline supply the context; the guide supplies methods to consider, not story facts.

1. **Frame the decision.** Name the actual issue or desired effect and its work/arc/scene scope. Include genre, atmosphere, character aims and relationships, viewpoint, and preservation conditions when relevant. A request about a relationship turn needs different evidence from one about sentence rhythm.
2. **Retrieve selectively.** Use the guide's decision map and the knowledge [natural-language lookup procedure](../vegabond-knowledge/references/retrieval.md#recover-a-natural-language-lookup) to inspect the relevant details, sources, application conditions, exceptions and checks. Separate a multi-part request into the consequential craft decisions; inspect whether each need is answered rather than treating a successful search or its top three hits as complete coverage. For Korean expression, route to the Korean guide (`knowledge/fiction/K-FIC-KO-EXPRESSION-GUIDE.md`); for research and critique, use the research map (`knowledge/fiction/K-FIC-RESEARCH-GUIDE.md`) and evaluation (`knowledge/fiction/K-FIC-EVALUATION.md`). If the raw request misses, use focused terms or the guide's named detail and keep any unresolved gap visible. Reuse a valid information brief across design and drafting. Expand for a real dependency or gap; do not read the whole collection or reopen all external sources by default. Recheck original evidence when a material claim or changed source requires it.
3. **Adapt or decline.** Connect a useful method to a concrete choice in this work, explaining any adjustment to genre, mood, character voice or scene function. Keep source-supported claims separate from editorial procedures and intended effects. Note consequential adoption, conditional use or rejection with its reference ID in the existing brief. An inapplicable model may be declined; act counts, conflict, transformation, hard magic or a particular prose style are not universal requirements.
4. **Apply and check the result.** Use the relevant checks on the actual outline, scene, paragraph or revision. Pass adopted reference IDs, applicability decisions and planned checks to [fiction-design](../vegabond-fiction-design/SKILL.md) when structural choices need it, and carry the same brief back into drafting. Follow [the craft-application review](references/review.md#applied-craft-methods) before handoff. Adjust the method or revisit the design when the result conflicts with established facts or the intended experience; a completed checklist or source citation is not proof of reader effect.

Keep this work proportional to the decision, within the existing brief and review process. Do not add a separate report, repeated full-store lookup or a mandatory method to every scene.

## Adapt selected dialogue references

Before drafting or revising dialogue, connect the scene's needs to selected quotation references through [vegabond-knowledge](../vegabond-knowledge/SKILL.md). Use the working project's relevant collection and the author-selected shared collection enabled by the [agent instructions](../../agents/vegabond-agent.md#knowledge-and-problem-records). Keep the following work in the existing scene brief; no separate worksheet or permanent usage log is required.

1. **Establish the scene's need.** Identify the speaker, listener, relationship, immediate aim, dramatic function, and intended emotional effect. Set the target genre, atmosphere, and expressive density from the actual work and its voice baseline before choosing an admired line.
2. **Retrieve by function and feeling.** Search for relevant tensions, such as affection and coercion, an alliance's internal insecurity and outward threat, or brief intimacy with beauty. Search source names or genre when useful, but do not select by genre label alone. Read the relevant interpretation, application conditions, and caveats. Reuse valid retrieval; if no candidate fits, proceed without applying one. Do not create a scene merely to accommodate a quotation or require memorable speeches in every scene.
3. **Extract the mechanism in plain language.** Set aside the source's wording and identify what it does: the relationship or choice it reveals, the emotion or unresolved tension it holds, the observer's stance, and the image or rhythm that carries the effect. Select the parts this scene needs. Treat stored interpretations as readings, not canonical intent or a doctrine the new story must endorse. Note consequential adoption, adjustment, or rejection with the reference ID in the existing brief.
4. **Compose from the new story.** Choose images and words grounded in the speaker's experience, work, culture, available knowledge, and present surroundings. Shape register, metaphor density, pauses, and directness to that character, listener, scene pressure, and the work's atmosphere. Genre is context, not a fixed menu of props or archaic diction. Recreate the useful dramatic mechanism through new expression; replacing nouns or synonyms while retaining a source's distinctive image sequence or sentence movement is insufficient adaptation.
5. **Review in context.** Read the new dialogue with the surrounding action and the listener's response, then compare it with the source using [the adapted-dialogue checks](references/review.md#adapted-dialogue). Keep wording that earns its place through this scene and this voice; rewrite or discard an application that remains recognizable as an imported line or disrupts the scene. Preserve source wording in reference records, without inserting those quotations into an adapted manuscript by default.

## Choose the design depth

Use [vegabond-fiction-design](../vegabond-fiction-design/SKILL.md) when a new work/arc, linked scenes, character motivation or change, viewpoint/disclosure, setups/payoffs, or a structural revision needs consequential narrative choices. Pass the existing brief, relevant canon/manuscript and voice baseline, constraints, and open questions. Reuse a valid design; revisit only choices affected by evidence. A clear local scene or line edit can state its purpose and preservation conditions inline without a separate design pass. Exploratory drafting can inform a provisional design; do not require a finished plot or a fixed story formula before every passage.

Design returns choices and intended effects within this workflow, not a second execution loop. A design-only request ends with that artifact rather than an unsolicited manuscript. Retrieve existing context through the section above; design must not create a competing story bible.

## Draft or revise

Establish genre, audience, realism, viewpoint, tense, narrator reliability and intended uncertainties from the request and relevant sources. Apply the work's baseline and scoped author choices, distinguishing established facts from proposed invention. Read [manuscript review and correction](references/review.md) before judging or revising prose, and apply it to the actual final text before handoff.

- **Create:** Use the design or inline scene purpose, character intent, pressure and change where relevant. Draft action, dialogue and exposition in the requested voice and viewpoint; respect deliberate ambiguity and form. Return discoveries that materially alter the intended sequence or effect to fiction-design without silently rewriting canon.
- **Revise:** Diagnose at the structural, scene, continuity or sentence level. Repair the earliest established causal problem within the requested scope, preserving facts and effective passages. If it changes linked narrative choices, update that part of the design before dependent rewriting. Use the reference's finding classification and correction loop; more explanation is not automatically improvement.
- **Research or critique only:** Ground findings in passages and distinguish textual evidence, interpretation and proposed invention. Verify the analysis without rewriting the source or promoting an interpretation to canon.

### Show character through the scene

When the passage should reveal a character, reuse the [designed choice](../vegabond-fiction-design/SKILL.md#design-choices-that-reveal-character) or identify it inline for a local passage. Choose the cue that fits the scene and its viewpoint: what the person does first or leaves undone, what response they seek in dialogue, or what they notice and how they interpret it in narration. A direct statement can also serve the voice or pace. Check whether nearby explanation adds something the cue leaves open.

If speech is meant to distinguish characters, decide what each wants from this listener and how they try to get it. Use the work's voice references to choose words, rhythm, directness, or silence. In Korean, check address terms, endings, and degree of certainty against the relationship, who else is present, and what prompts any shift. Read how the listener responds. Apply the [characterization review](references/review.md#review-characterization) to the written passage.

## Hand back

Return the requested text or analysis, important choices, review/correction evidence and unresolved conditions to the active operation. The review reference owns the detailed checks, uncertain judgments, style and recurrence evidence, and final rereading. Send useful findings through knowledge within the existing write scope; do not create a separate style store or new record schema. Distinguish AI review from vagabond's independent acceptance under the common instructions.

## Shared review checkpoints

Apply [the shared review checkpoints](../vegabond-review/SKILL.md#review-checkpoints). Review new or changed narrative choices with fiction-design criteria before dependent drafting; reuse a still-valid design review. Before handoff, use fiction criteria on the actual final prose and incorporate the manuscript review above into the same pass. Carry canon, knowledge/problem IDs and evidence forward; return structural defects to design and recheck only affected passages and dependencies.
