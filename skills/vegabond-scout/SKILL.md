---
name: vegabond-scout
description: Use when starting substantive creation, revision, multi-step work, or research in any domain, including software, fiction, presentations, and planning, or when the user explicitly requests vegabond-scout.
---

# Vegabond Scout

Choose an operation and scale for vagabond's intended outcome, then coordinate execution through the linked operation skill. Scout owns the work brief, capability mapping, and overall progress.

## Frame and classify

Read the [English agent instructions](../../agents/vegabond-agent.md) if not already loaded. Inspect the request, relevant context, and source material for the intended result, audience, format, language, constraints, and acceptance conditions. Ask only when missing intent materially changes the work.

Identify the operation separately from domain, medium, and tools. The author's background and the examples here do not limit eligibility. Original inputs and outputs follow the requested language. Never read, search, or load *.kr.md human-only translations; exclude them from retrieval and any authorized delegated work.

Build one lightweight task profile by answering four questions:

1. **Target:** What material, artifact, behavior, or question is involved, and what result is requested? Include relevant domain, medium/format, and execution context.
2. **Intended change:** What should be added, corrected, transformed, improved, or established? Describe the specific gap between the current state and the requested outcome.
3. **Preservation conditions:** What must remain intact, such as meaning, behavior, voice, facts, format, or source material? Use the request and context; clarify material conflicts or uncertainty.
4. **Method:** What way of working can close that gap while preserving those conditions, and what capabilities and checks does it require? Choose from the actual problem and acceptance conditions rather than a domain label or file extension.

Use open descriptions; a task can involve several domains and methods. A novel-based pitch deck can need narrative analysis, slide production, and visual inspection together. Search can support any operation. Keep the profile in the brief and step mapping, without a separate file or a fixed catalog of task subtypes. Reuse it in the operation skills and refine only missing details or assumptions changed by evidence.

Apply the shared [information-needs judgment](references/information-needs.md) to derive questions from decisions, preservation conditions and actual inputs. Request a focused brief from [knowledge](../vegabond-knowledge/SKILL.md); carry evidence, applicability, checks and gaps forward. The executing specialist then checks for missing questions after source inspection, reusing valid answers and adding only needs exposed by the work. Revisit affected judgments before consequential reliance and at handoff.

| Operation skill | Choose when |
| --- | --- |
| [vegabond-create](../vegabond-create/SKILL.md) | Producing a new artifact or capability, including one derived from existing sources. |
| [vegabond-revise](../vegabond-revise/SKILL.md) | Improving or correcting an existing artifact or behavior. |
| [vegabond-research](../vegabond-research/SKILL.md) | Answering a question or comparing options while leaving investigated sources unchanged. |

Select the primary operation from the requested outcome. Supporting research does not make a chapter or deck request research-only. A software feature uses create; a software defect uses revise with reproduction and root-cause investigation. Mixed work may combine operations in its steps.

Choose scale independently:

- **single:** a compact task that fits one execution-and-verification cycle; use this by default.
- **staged:** a named intermediate result must be checked before dependent work because of dependencies, costly unresolved assumptions, or scope that makes final-only verification inadequate. Use an appropriate operation at each milestone, then check the integrated result.

Several tools, files, ordinary steps, or long waiting times alone do not require staged work. Risk can require stronger checks without changing scale. If no concrete checkpoint is needed, start single; reassess and update the brief when new dependencies or uncertainty emerge. A full novel can be create + staged; editing one chapter can be revise + single.

## Give a short work brief

Before execution, state these in a few lines in the conversation:

- **Goal and deliverable:** what the user will receive, with audience, format, and language when relevant.
- **Operation and scale:** the choices and a short reason.
- **Scope:** the target, intended change, preservation conditions, and meaningful exclusions.
- **Done:** link each acceptance condition to its check; attach the result and evidence as work proceeds. One or two inline lines suffice for a small task; use the existing brief or step mapping, not a separate tracking file.

For staged work, give one sentence explaining the boundary: "Check A before B, because if A is wrong, C would need rework." Name the actual intermediate result, dependent work, and consequence; use its check in the step mapping below.

Proceed within existing authorization without a routine approval checkpoint. Reuse the brief on follow-ups; update it when the goal, scope, or evidence changes. No separate brief file is required.

## Connect steps to skills and checks

For each planned step, identify the needed capability, an available skill or direct tool, and the expected result with its check. For single work, keep the mapping inline; for staged work, use a short list or this table:

| Step | Available skill or direct tool | Expected result and check |
| --- | --- | --- |
| Describe the step. | Use an advertised name, or name the direct tool. | State what it produces and the evidence that checks it. |

Use these local specialists when their methods are needed:

| Specialist | Relevant work |
| --- | --- |
| [vegabond-code](../vegabond-code/SKILL.md) | Software implementation, defects, system design, refactoring, and code investigation. |
| [vegabond-fiction](../vegabond-fiction/SKILL.md) | Fiction development, drafting, critique, and continuity. |
| [vegabond-presentation](../vegabond-presentation/SKILL.md) | Slide narrative, deck production, and content or visual revision. |
| [vegabond-planning](../vegabond-planning/SKILL.md) | Planning/proposal content, feasibility, and success measures; not task scheduling alone. |

The operation owns the workflow; a selected specialist supplies its domain execution, verification, and correction methods. Apply those methods within the operation's steps rather than running a second independent workflow. For research or feedback-only work, use checks that substantiate the findings and correct the analysis without changing investigated sources; production checks apply when producing or changing the corresponding artifact. Combine specialists only where needed, such as planning content and presentation production for a proposal deck. This is an initial set, not a closed list of supported work. Load only the relevant specialists; they can use available environment- or format-specific skills and tools through the same mapping.

Inspect the current skill catalog and use actual names and paths. Read each selected skill when its step needs it. Do not assume a plugin is installed. If no specialist fits, use capable direct tools and briefly note the fallback. Do not create or install skills or delegate merely to satisfy the mapping. Missing required capability is a blocker, not a passed check.

Before substantial production or dependent work, confirm that the essential sources, access, tools, and execution or inspection environment for the planned checks are usable. Use a small relevant probe when availability is uncertain; do not run the entire final check suite at setup. A tool listing alone does not prove readiness. Carry any gap into the brief and follow the agent instructions' blocker handling. This readiness check does not replace verification of the final artifact.

Read the linked operation skill needed for each step; do not load all three by default. Pass the existing brief, four-part profile, source material, and acceptance conditions. The operation skill turns the chosen method into its execution procedure and selects specialists through this shared capability mapping. Update the profile and mapping when evidence changes instead of repeating classification. Reading a skill does not spawn another agent.

For direct invocation of an operation skill, use these shared framing, brief, and mapping sections to fill missing context, then continue in that skill without routing back through scout. It follows the linked agent instructions for common verification and acceptance. Scout consumes the returned result, evidence, and open issues to coordinate dependent steps and the final handoff.

## Execute and hand back

Follow the agent instructions' completion-evidence contract for the actual medium. Execute each step and inspect its result; for staged work, pass the milestone's checks before dependent work. Route failures and feedback using the [shared return-point rules](../../agents/vegabond-agent.md#respond-to-failures-and-feedback), updating only the affected brief, steps, and checks.

At each staged checkpoint, give a one-line update: intermediate result; check and evidence; passed, failed, or blocked; next action. Advance dependent work only after the required checks pass; an update does not request routine user approval.

Continue with the next step's mapped operation and specialist, which may differ from the previous step. Reuse valid context rather than restarting classification. Before final handoff, confirm that each acceptance condition has current evidence or an explicit unresolved status, and check the integrated result.

Report the result, acceptance evidence, and uncertainty. Distinguish drafts, completed AI verification, and vagabond's explicit acceptance. AI checks precede vagabond's independent testing or review.
