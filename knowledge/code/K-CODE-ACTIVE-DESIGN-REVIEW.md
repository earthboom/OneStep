---
id: K-CODE-ACTIVE-DESIGN-REVIEW
title: "Cross-check a software design by asking a consumer to use it"
summary: "Derive an expected outcome from the request independently, then have a consumer trace calls through the proposed design. Replay the first divergence after revision."
kind: method
scope: "Software design review and handoff when a plausible interpretation or missing contract changes acceptance"
keywords: ["design review","independent review","active design review","ARID","acceptance criteria","cross-check","설계 검수","설계 리뷰","설계 검증","교차검토","교차검증","크로스체크","인수인계","설계 완성도","요구사항 누락","구현 착수","개발 설계를 구현에 넘기기 전에","동료 검토","설계 인계","호출 절차"]
status: active
checked_at: 2026-11-25
---

# Cross-check a software design by asking a consumer to use it

## Guidance

Give a reviewer the original request and governing contract first. Ask for one ordinary input and one case where two plausible interpretations give different observable outcomes. Then give the reviewer the design and ask them to write the caller's sequence or pseudocode. Record the first step where a required fact must be guessed. Resolve a product choice with its owner and a technical question with the relevant contract or experiment.

## Applicability and exceptions

Useful for shared APIs, changes of ownership, persistence and failure recovery. A clear display-only edit can be checked directly. This is a source-based method. Agreement between reviewers does not establish implementation behavior.

## Checks

Example: feedback files exist in the working directory, but the configured inbox contains only the English file. Derive the expected delivery state, trace which path the caller checks, then repair the missing file and repeat the same check. Hand off the expected transition, its evidence, and any check that must wait for implementation. [OneStep inbox contract](../../feedback/README.md)

For a risky transition, move a failure to just before and after it. Hand off the requirement and preservation condition, distinguishing case, enforcement point, evidence and remaining check with its owner. For glossary routing, ask whether a competing meaning would change the verdict before adding a definition. The linked conditional routing trial is project data. A separate review-method pilot could compare substantiated and unsupported findings, elapsed review time and recurrence on replay. [Review procedure](../../skills/vegabond-code-design/references/review.md) · [Conditional glossary trial](../../docs/research/2026-11-25-conditional-glossary-routing.json)

## Evidence

NASA §4.4 distinguishes requirements conformance and suitability for intended use from later end-product verification. ARID §2.2 has intended consumers exercise the design by writing code or pseudocode. Porter and colleagues used two specifications with 48 graduate students in 16 three-person groups. Scenario-based reading found more defects than ad hoc or checklist reading, while collection-meeting gains were offset by losses in that experiment. Huang and colleagues found that intrinsic LLM correction without outside feedback could fail or degrade results on their reasoning tasks. The experiments did not measure AI design review or multi-agent review in OneStep. [NASA handbook](https://www.nasa.gov/reference/4-4-design-solution-definition/) · [ARID report](https://www.sei.cmu.edu/documents/1962/2000_004_001_13685.pdf) · [Porter et al.](https://www.cs.umd.edu/~basili/publications/technical/T101.pdf) · [Huang et al.](https://arxiv.org/abs/2310.01798)

For review depth and who should read a design, compare the author's account of the cost of a design document and the role of affected teams. [Malte Ubl, Design Docs at Google](https://www.industrialempathy.com/posts/design-docs-at-google/)
