---
id: K-FIC-RESEARCH-PLAUSIBILITY
title: Select evidence for narrative plausibility and the limits of AI judgment
summary: Ten newly inspected papers distinguish perceived realism, intentional action, state and knowledge tracking, and the reliability limits of automated critics. Use their task-specific findings to support an auditable review, without treating a benchmark score as accuracy on Korean novels.
kind: reference
scope: Selected theory and AI studies 2008-2026, checked 2026-11-17; Korean fiction application; purposive research map, not systematic review or validated literary instrument
keywords: [plausibility, verisimilitude, believability, consistency, rationality, contradiction, 핍진성, 개연성, 논리, 합리성, 모순, 판단논문, AI평가연구]
status: active
checked_at: '2026-11-17'
relations:
  derived_from: [K-FIC-RESEARCH-CAUSALITY, K-FIC-RESEARCH-CHARACTER]
context:
  evidence: Publisher and author abstracts plus selected full-text sections; individual access depths in the V01-V10 ledger
  application: Editorial review procedure and constructed probes; no human validation or universal AI accuracy claim
---

# Select evidence for narrative plausibility and the limits of AI judgment

## Guidance

Use [the plausibility review method](K-FIC-PLAUSIBILITY-REVIEW.md) within existing manuscript/design review. These are working distinctions for this project, not interchangeable dictionary definitions or a claim of scholarly consensus about Korean terminology:

| Question | Working distinction | Evidence route |
| --- | --- | --- |
| Could the presented statements jointly hold? | Logical/internal consistency requires the same entity, time, world and assertion level. | V03, V06 |
| What makes the event possible and connected? | Causal plausibility concerns enabling conditions and consequences, beyond mere temporal succession. | Existing [P01](K-FIC-RESEARCH-GUIDE.md#p01), V02-V03 |
| Why would this person choose it? | Motivation and instrumental fit concern the actor's goals, beliefs, information, pressure and cost; they are distinct from morality, success or omniscient optimization. | V02, V04; editorial extension |
| Why accept the impossible premise? | Perceived realism separates fictionality, external reality and coherence within the narrative. Fantasy need not reproduce everyday physics. | V01 |
| Can the critic establish its judgment? | Evaluation reliability concerns evidence and error detection in a specified task, not fluent confidence. | V05-V10 |

### Consequential use

Inspect the work's rules, viewpoint and disclosure first. Extract the disputed state or action with its source; test a relevant precondition or conflicting claim; consider a text-supported alternative; report a demonstrated error, uncertainty, or no demonstrated error. Missing narration alone does not prove an impossible transition. A genre label alone does not authorize arbitrary exceptions to established rules.

The source studies support different pieces, not a single verified novel critic. V06 offers promising evidence-grounded contradiction detection; V05 exposes unreliable book-summary raters. Their outcomes concern different tasks, models and diagnostic material, so neither cancels the other. V07-V08's agreement measures do not establish contradiction detection in fiction. V09 concerns intrinsic reasoning correction, not every possible benefit of revision. V10 motivates checking distant passages rather than assuming that placing a whole book in context guarantees inspection.

## Applicability and exceptions

Preserve motivated error, deception, deliberate uncertainty, irrationality, evolving traits and unusual form. A law can be broken without immediate punishment; a trait is a tendency rather than an exceptionless proposition; an unresolved object in an excerpt is not automatically an abandoned plot. These are safeguards against over-literal transfer of benchmark categories, not excuses to invent unseen support.

No paper here validates the proposed review for Korean literary fiction or proves a particular novel's appeal. The ten sources are a purposive selection; models, languages, prompts and targets vary. Existing P01 is reused at its previously recorded access depth and is not counted as a newly checked paper. Simon's 1955 rational-choice article was located, but its informative full text was unavailable in this lookup; it is not counted or used as inspected support. Korean-language searches did not yield an additional primary item inspected deeply enough for this ledger.

## Checks

- Is the claim about world consistency, causality, character choice, external fact or reader response?
- Does the evidence concern that question, rather than a neighboring benchmark?
- Are direct text, defeasible inference, character belief and author choice distinguished?
- Are benchmark language, model/date, controlled errors and access depth attached to transferred claims?
- Is an AI finding independently checkable in the actual text without accepting the AI's authority?

## Evidence

Checked 2026-11-17 through primary publication pages, author-hosted material and author preprints. V labels are local to this ledger. Source-derived observations below are distinguished from the review procedure's editorial synthesis. No datasets, model weights, published novels or papers were downloaded into the store.

### V01

[Busselle & Bilandzic (2008), Fictionality and Perceived Realism in Experiencing Stories](https://onlinelibrary.wiley.com/doi/10.1111/j.1468-2885.2008.00322.x). DOI: 10.1111/j.1468-2885.2008.00322.x. Publisher author abstract inspected. This theoretical mental-model account separates fictionality, external realism and narrative realism. It informs the premise-versus-coherence distinction. Repository PDF timed out; full argument and cited experiments were not audited. It does not supply an automatic score or a universal fantasy exemption.

### V02

[Riedl & Young (2010), Narrative Planning: Balancing Plot and Character](https://faculty.cc.gatech.edu/~riedl/pubs/jair.pdf). JAIR 39:217-267; DOI: 10.1613/jair.2989. Author-hosted PDF inspected: abstract, §2.2.2, §4 and plan-completeness definitions. IPOCL represents action preconditions and recognizable character intentions. The paper reports better intention comprehension than conventional planning in its evaluation; that evaluation was not independently reproduced here. Formal generation with supplied operators/goals does not prove arbitrary prose can be parsed or judged correctly.

### V03

[Storks et al. (2021), Tiered Reasoning for Intuitive Physics](https://aclanthology.org/2021.findings-emnlp.422/). DOI: 10.18653/v1/2021.findings-emnlp.422. ACL abstract and PDF §2.2, §4.1 inspected. TRIP separates choosing a plausible story, identifying conflicting sentences and verifying relevant physical preconditions/effects. A correct label can lack supporting state evidence. Its short English everyday physical narratives are not a complete model of emotion, social norms, fantasy or novel quality.

### V04

[Kim et al. (2023), FANToM](https://aclanthology.org/2023.emnlp-main.890/). DOI: 10.18653/v1/2023.emnlp-main.890. ACL abstract and PDF introduction/Figure 1 inspected. Information-asymmetric conversations distinguish full facts from what a participant can access. Multiple related question types expose brittle apparent success. This motivates a character-information check; the benchmark does not establish a real mind, reader empathy or accuracy on every fictional perspective.

### V05

[Kim et al. (2024), FABLES: Evaluating faithfulness and content selection in book-length summarization](https://arxiv.org/abs/2404.01261). COLM 2024; author version v2, 2024-09-30. Abstract and HTML §4/conclusion inspected. Human annotations cover 3,158 summary claims from 26 books; automatic-verifier experiments use a smaller subset. Tested raters struggled with unfaithful claims, even with book text. Summary faithfulness differs from an author's deliberate invention; use this as a critic-reliability caution, not a ban on AI review.

### V06

[Li et al. (2026), Lost in Stories: Consistency Bugs in Long Story Generation by LLMs](https://aclanthology.org/2026.findings-acl.410/). DOI: 10.18653/v1/2026.findings-acl.410. ACL PDF abstract, §2.2-2.3, §6 and Appendix A.2 inspected. ConStory-Checker extracts spans, pairs contradictions and reports quoted evidence/locations. Its diagnostic validation uses planted inconsistencies. §6 explicitly limits transfer beyond English/Western conventions and acknowledges intentional ambiguity/delayed disclosure are not distinguished from errors. Human comparisons use two writers under the reported workload; no universal superiority claim is adopted.

### V07

[Liu et al. (2023), G-Eval](https://aclanthology.org/2023.emnlp-main.153/). DOI: 10.18653/v1/2023.emnlp-main.153. ACL author abstract inspected. Criterion-driven structured evaluation is tested on summarization/dialogue; GPT-4's reported summarization Spearman correlation is 0.514. The authors flag possible preference for LLM text. Correlation is not 51.4% accuracy and does not validate this project's literary rubric, current models or whole-novel judgments.

### V08

[Zheng et al. (2023), Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena](https://papers.nips.cc/paper_files/paper/2023/hash/91f18a1287b398d378ef22505bf41832-Abstract-Datasets_and_Benchmarks.html). NeurIPS 2023 Datasets and Benchmarks. Proceedings author abstract inspected. Reports useful human-preference agreement alongside position, verbosity, self-enhancement and reasoning limitations. For consequential variant comparisons, blind labels/order and demand evidence rather than trusting eloquence. Chat preference agreement is not calibrated probability that a narrative inconsistency finding is true.

### V09

[Huang et al. (ICLR 2024), Large Language Models Cannot Self-Correct Reasoning Yet](https://arxiv.org/abs/2310.01798). Author version v2, 2024-03-14; abstract inspected. Intrinsic self-correction without external feedback can struggle or degrade reasoning in the studied settings. The title is not adopted as a timeless impossibility claim. A second AI pass is not independent ground truth; a useful correction adds checkable textual evidence or other appropriate feedback. OpenReview's current page required browser verification.

### V10

[Liu et al. (2024), Lost in the Middle](https://aclanthology.org/2024.tacl-1.9/). DOI: 10.1162/tacl_a_00638. TACL author abstract inspected. Multi-document QA and key-value retrieval reveal sensitivity to relevant information's position. For long-manuscript review, retain locators and check separated dependencies. This is a workflow inference, not a tested fiction-review intervention or a claim that every later long-context model has identical limitations.
