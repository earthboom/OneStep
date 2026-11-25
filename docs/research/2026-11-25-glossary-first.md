# Reading the development glossary before looking for test evidence

Four independent readers opened the glossary first and four searched without it. All four glossary-first answers covered the 11 predefined acceptance criteria. Three control answers also covered all 11. One covered eight. Median evidence lookup took 40.44 seconds with mandatory reading and 33.09 seconds without it, an observed difference of 7.35 seconds.

## Request and results

> 3만 건 세션 검색의 개별 응답 2초 목표와 피드백 접수 표시를 검증할 인수 테스트 기준을 잡아줘.

| Pair | Order | Glossary first, total seconds | Of which, through read acknowledgement | Without glossary, total seconds | Criteria covered, first / without |
| --- | --- | ---: | ---: | ---: | --- |
| 1 | First, without | 41.63 | 13.67 | 39.36 | 11/11 · 11/11 |
| 2 | Without, first | 39.25 | 10.57 | 30.67 | 11/11 · 11/11 |
| 3 | Without, first | 42.63 | 8.74 | 31.03 | 11/11 · 8/11 |
| 4 | First, without | 25.76 | 13.39 | 35.15 | 11/11 · 11/11 |

All eight readers chose the same two main gates. Every one of the 250 caller responses must meet the two-second limit. Feedback becomes submitted after the matching English and Korean files are confirmed in the designated inbox. All eight also distinguished delivery from maintainer review and covered the partial-delivery retry.

The control answer in pair 3 omitted three search details. It measured from “프로세스 시작부터” without specifying that the caller starts the clock immediately **before** launching the process. It reported P95 without specifying the 48th sorted value of each round of 50. It correctly used an inclusive two-second limit but left out comparison using the **unrounded** elapsed time. The other seven answers covered the three details. This is a coverage score on written test designs.

## Procedure and limits

We froze the request, 11 binary criteria and run order before collection. Each reader had a fresh chat and one full working-tree snapshot. The two snapshots had 1,720 hash-identical files in common. Only the treatment contained the two glossary language files. Readers consulted English canonical sources. Both snapshots excluded Git internals, caches and six previous trial artifacts. Both kept the usual skill references. No source shortlist was supplied. A fresh grader received the frozen rubric and eight shuffled answers with glossary names masked, without run IDs, conditions or timings.

The same host's monotonic timer started before the first lookup. In the glossary-first condition that command opened and displayed the complete English glossary. The reader had to return a token printed after its last line before looking elsewhere. The median interval to acknowledgement was 11.98 seconds, already included in total lookup. It includes tool round trips and reading. The timer stopped when the reader declared the evidence sufficient, before drafting. Scheduled waits before start were excluded. The eight search intervals did not overlap.

Mandatory reading took longer in three pairs. All three omissions occurred in one answer and the other three control readers achieved full coverage. These data support selectively consulting the glossary when the exact timer, percentile or threshold affects acceptance. A single task with four readers per condition provides little basis for a universal reading rule. [Per-reader answers, grading reasons and raw clock events](2026-11-25-glossary-first-measurements.json)
