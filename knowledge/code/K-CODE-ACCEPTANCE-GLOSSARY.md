---
id: K-CODE-ACCEPTANCE-GLOSSARY
title: "Consult a development glossary when a term changes an acceptance verdict"
summary: "Select the disputed term and confirm its owner, test boundary and counterexample in the governing source. Local reader trials found occasional missing criteria and no consistent time benefit from mandatory lookup."
kind: method
scope: "Development design and implementation where terms determine an observable acceptance test"
keywords: ["development glossary", "acceptance criteria", "timer boundary", "delivery receipt", "controlled reader trial", "개발 용어집", "인수 조건", "용어 정의", "피드백 접수"]
status: active
checked_at: 2026-11-25
---

# Consult a development glossary when a term changes an acceptance verdict

## Guidance

Give a term a glossary entry when two plausible meanings lead to different tests. For a disputed term, look up the matching term label, then confirm the definition in the source owning the behavior. Searching entire table rows can select unrelated entries that merely mention the same word. Keep a label-only edit local to its binding and display check. [OneStep development glossary](../../docs/development-glossary.md)

## Applicability and exceptions

For a time limit, identify the clock owner, start/end events, statistic, threshold and comparison precision. For delivery status, identify the destination and the observation that permits the state transition. Both become testable through one differing input. An identical word in a card title may leave its underlying predicate untouched.

## Checks

In the constructed 250-response example, 0.23 s before encoding, 1.76 s through receipt and 0.0104 s decoding total **2.0004 s** at the caller. Exactly 2.0 s passes an inclusive threshold. With all five round P95 values at 0.8 s, only 249/250 calls meet the individual limit. For a feedback pair, put a nonempty English file and empty Korean file in the configured inbox. The checker returns 1; refill the Korean file and recheck the same pair for code 0 before changing prepared to submitted. Maintainer review is a later decision. [Caller measurement contract](K-CODE-RETRIEVAL-SCALE.md) · [Inbox contract](../../feedback/README.md#confirm-delivery-at-handoff) · [Delivery tests](../../tools/test_check_feedback.py)

## Evidence

The following AI-reader trials used the same 11 explicit acceptance details. Scores count statements in test designs. They do not measure implementation quality or rework.

| Comparison | Observations and limits |
| --- | --- |
| Curated packet, two readers per arm | All four scored 11/11. Only treatment readers had the glossary and both cited it. The detailed request and eight common sources already supplied the evidence. No timing or live search benchmark was collected. [Frozen request, hashes, rubric and answers](https://github.com/earthboom/OneStep/blob/9f553ba95ec7209a5bf3fcc6ab16b119ebeb8317/docs/research/2026-11-25-development-glossary-trial.json) |
| Full checkout, glossary available, three readers per arm | Among 1,716 hash-identical common files, controls scored 11, 9 and 10. All three treatment readers scored 11, but only one used the glossary. Median pre-drafting lookup was 50.2 s versus 40.3 s. Two controls omitted the 48th-of-50 P95 calculation and one also omitted repair followed by recheck. The fastest treatment reader saw only the filename. Variable tool waits, self-declared stopping and unblinded scoring prevent causal attribution. [Order, timings, answers and use reports](https://github.com/earthboom/OneStep/blob/9f553ba95ec7209a5bf3fcc6ab16b119ebeb8317/docs/research/2026-11-25-development-glossary-field-trial.json) |
| Full checkout, mandatory first reading, four readers per arm | Across 1,720 common files, all four treatment readers scored 11. Controls scored 11, 11, 8 and 11. One control omitted the pre-launch start, percentile calculation and unrounded comparison. Median lookup was 40.44 s with mandatory reading and 33.09 s without. The 11.98 s median through end-token acknowledgement was included. A separate grader scored shuffled masked answers. One task and four readers per arm give limited grounds for a general timing claim. [Raw clock events and grading](https://github.com/earthboom/OneStep/blob/9f553ba95ec7209a5bf3fcc6ab16b119ebeb8317/docs/research/2026-11-25-glossary-first-measurements.json) |

To repeat a comparison, freeze the question, binary criteria, file hashes and run order. Give each reader a fresh chat, identical common sources and a declared lookup condition. Record actual glossary use, time from first lookup to sufficient evidence, and grade the written criteria separately from that time. Use the stored exclusions and packet manifests for the chosen trial. In a separate once-per-case skill check, only a disputed delivery state and a faulty threshold led to a definition read. Both label-only cases skipped it. The corrected predicate rejected 2.000001 s and accepted 2.0 s. This demonstrates conditional routing in four fixtures. [Skill hashes, access trace and fixture checks](https://github.com/earthboom/OneStep/blob/9f553ba95ec7209a5bf3fcc6ab16b119ebeb8317/docs/research/2026-11-25-conditional-glossary-routing.json)
