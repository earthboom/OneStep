# OneStep agent instructions

OneStep is authored by vagabond, whose background includes Unreal Engine game client programming. That background does not limit the project. Support work in any domain by identifying the requested outcome and deliverable, not by maintaining a closed list of industries, engines, or file types. Start small and expand only when real use demonstrates a need.

## Document boundary

- Author maintained project guidance, agent instructions, and skill instructions in English, with separate Korean translations named <stem>.kr.md.
- English guidance is canonical. Never read, load, or search the contents of *.kr.md files, including during reviews, indexing, and delegated work. Exclude them before content retrieval; for example, rg -g '!*.kr.md'.
- Translations are human-only, never instruction entry points or reference inputs. Generate them from the English guidance without rereading them. Do not duplicate skill-discovery frontmatter in translations.
- Task inputs and deliverables follow the user's requested language. A Korean manuscript, presentation, or plan is not automatically a translation or an instruction document. Do not append .kr.md to an original artifact merely because it is Korean.
- These rules do not restrict the language of conversation with the user.

## Entry skill

Paths here are relative to the repository root. For a new substantive task, read skills/vegabond-scout/SKILL.md if not already loaded for this task. Continue the selected procedure on follow-up turns; reassess when the goal or evidence changes.

Scout owns classification, scale, the work brief, capability mapping, and overall coordination. The create, revise, and research operation skills own their workflows and reuse that shared setup. Selected specialists supply domain execution, verification, and correction methods within those workflows. Do not create additional specialist skills, install tools, or delegate merely because routing is possible.

## Knowledge and problem records

OneStep's shared guidance and stores must not contain another project's physical locations or active source connections. Keep that setup in the actual working project. Historical source identities, fingerprints, scoped knowledge and incident evidence may be retained here without location bindings; their presence does not authorize searching for or connecting the original project.

Use [vegabond-knowledge](../skills/vegabond-knowledge/SKILL.md) for a focused information request once the task profile is known. Reuse the returned sources, applicability conditions, checks, and gaps in the work brief and execution. Operations and specialists can refine that request when new needs arise; reuse the existing information brief instead of repeating the same lookup. The specialist applies the knowledge and verifies the deliverable. Supply findings, corrections, and reusable lessons back to this skill for authorized storage and maintenance. It owns the common storage and retrieval procedure across domains.

## Completion evidence for any deliverable

Before producing or changing a result, identify its purpose, audience, requested format and language, source material, constraints, acceptance conditions, and how the AI will check the actual final result. Resolve missing intent that materially changes the work; do not add routine permission checkpoints.

The AI produces the result, checks it directly against the acceptance conditions, and reports evidence and limitations before vagabond's independent testing or review. Domain-specific execution, verification, and correction procedures live in the specialists linked from [scout's capability mapping](../skills/vegabond-scout/SKILL.md#connect-steps-to-skills-and-checks). Evidence gathering and source boundaries for research live in the research operation skill.

For other deliverables, choose observable checks based on purpose, medium, and failure modes. Use automation where it provides meaningful evidence; use direct reading, visual inspection, or real use where those are needed. Do not force build, editor, gameplay, slide, or manuscript checks onto unrelated work.

A check is not applicable only when the deliverable genuinely does not require it; explain why and what covers acceptance instead. Missing tools, tests, access, or time make an applicable check blocked, not inapplicable. Apply this distinction to all required build, test, reading, rendering, and use checks.

Evidence must describe the final artifact, not a proxy or a confident summary. Rerun checks invalidated by later edits. Do not weaken acceptance conditions to pass. If a required check cannot run, establish the capability within authorized scope or report the exact blocker and unverified conditions. Do not transfer a missing AI check to vagabond as a substitute.

After the required AI checks pass, report **AI verification complete; awaiting vagabond testing or review**, with acceptance results, evidence locations, and limitations. Vagabond then tests or reviews independently. Report **accepted by vagabond** only after explicit confirmation. Reopen the work if that review finds a problem, then repeat affected AI checks before handing it back.

## Respond to failures and feedback

Use the same diagnosis for AI findings and vagabond's review. Choose the return point from the evidence:

- **Artifact defect:** correct the result with the relevant specialist and rerun the original failure check and affected checks. For research or feedback-only work, correct the analysis without editing investigated sources.
- **Evidence gap:** request focused knowledge or research before deciding on a correction. Keep unsupported conclusions uncertain.
- **Changed or mistaken goal, premise, or scope:** have scout update the existing brief and affected step mapping. Distinguish a missed original requirement from a new request or preference; do not record a preference change as a defect. Clarify only material unresolved intent, and never redefine a valid acceptance condition merely to pass.
- **Unavailable required capability:** establish it within authorized scope or report the blocker and unverified conditions. Continue independent useful work, but do not advance work that depends on the blocked check.

If two corrections based on the same premise fail the same check, examine that premise and the observation method before another correction. Resume with new evidence or a revised diagnosis; if progress still requires unavailable capability or a user decision, report that specific blocker rather than repeating unsupported attempts. This is a reassessment trigger, not a fixed attempt limit or a reason to weaken checks.

Send material findings from either AI or user review, their corrections, and recheck evidence through vegabond-knowledge under the existing storage rules. Keep findings distinct from requests and preferences; update scoped conventions only when supported by the user's intent. After changes, repeat invalidated AI checks before returning the result for independent review.
