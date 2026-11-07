---
id: K-CODE-READABILITY
title: Review readability through a concrete maintenance question
summary: Judge readability by whether a reader can explain behavior and safely locate a likely change. Treat size, naming and comment metrics as prompts for inspection rather than universal acceptance thresholds.
kind: reference
scope: Source-code review and maintenance; language and team conventions must be checked locally
keywords: [readability, maintainability, code review, comprehension, naming, comments, cognitive load, 가독성, 유지보수성, 이름짓기, 주석]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: Primary English guidance and selected full-text research sections inspected online
  application_status: Proposed review checks; no implementation or reader study performed in OneStep
---

# Review readability through a concrete maintenance question

## Guidance

Use a plausible maintenance task to judge a passage: explain its result, identify its assumptions, and locate the decision that would change for a new requirement. Readability concerns the reader's successful understanding. A shorter expression can conceal state changes; a longer explanation can remove an otherwise necessary investigation.

Proposed practice: make domain distinctions visible in names and control flow. Choose names that distinguish nearby concepts, state units when confusion is plausible, and keep a name's meaning consistent across its scope. Introduce an intermediate value when it gives a significant condition or calculation a useful meaning. Remove indirection when following it adds no useful concept or independent responsibility.

Use comments for information the code cannot communicate economically: a constraint's origin, a surprising tradeoff, or a compatibility reason. Check that the explanation remains true after a change. A comment that merely repeats an operation adds another statement to maintain. Neither comment count nor identifier length establishes understanding.

## Applicability and exceptions

Apply this review to code that someone must inspect or modify. The relevant reader may need domain training; an unfamiliar algorithm is not automatically poorly written. Generated output, mathematical notation, performance-sensitive loops and framework conventions can justify different presentation choices. Check their generating source, explanation or measured constraints instead of mechanically expanding everything.

Do not derive universal function lengths, naming lengths or formatting thresholds from a readability model. Correlation with defect indicators does not establish that editing a metric causes fewer defects.

## Checks

These are proposed checks, not demonstrated safeguards:

- Trace one normal path and one important exceptional path; state the resulting values and side effects.
- Locate the rule for one plausible change. Record any hidden assumption, misleading name or unnecessary cross-file jump that blocked the explanation.
- Compare a candidate revision using that same question. Accept extra lines or a retained comment when they reduce the actual ambiguity.

## Evidence

Source observations, checked 2026-11-07:

- [Google Engineering Practices](https://google.github.io/eng-practices/review/reviewer/looking-for.html), “Complexity,” “Naming,” and “Comments”: review guidance prioritizes understandable code and useful explanation. English, undated living organizational guidance; relevant sections accessible, not an experiment.
- [Buse and Weimer, Learning a Metric for Code Readability](https://web.eecs.umich.edu/~weimerw/p/weimer-tse2010-readability-preprint.pdf), 2010 author-hosted English preprint, sections 2, 5–7: Java-snippet ratings yield predictive associations; the model is descriptive, with participant limitations. Selected full-text sections were accessible; this does not establish a universal metric or causal intervention.
