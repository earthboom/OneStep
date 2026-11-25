# Finding acceptance criteria across the full OneStep repository

All six independent readers chose the same core acceptance criteria. The readers with access to the glossary supplied all 11 details in each of three runs. Readers without it supplied 11, 9 and 10. Evidence lookup took a median of 40.3 seconds with the glossary available and 50.2 seconds without it. Only one reader actually used the glossary. These runs establish a difference between the observed groups, with insufficient evidence to attribute it to the glossary.

## Task and design

Every reader received the same short request, without a source shortlist or worked examples.

> 3만 건 세션 검색의 개별 응답 2초 목표와 피드백 접수 표시를 검증할 인수 테스트 기준을 잡아줘.

We created two snapshots of the working tree and verified the SHA-256 of all 1,716 common files. Both included tracked and nonignored untracked project files, the normal skill references to the project glossary, and the original code, reports and tests. We excluded Git metadata, local caches and all three outputs of the previous glossary trial. The treatment snapshot added only the English and Korean glossary files. The portable exports in the control did not contain an embedded copy of the glossary.

Each run used a new reader with no inherited chat. Readers chose where to search and cited their evidence. Before the first run we fixed the order and 11 binary criteria. The same machine's monotonic clock measured each interval from immediately before the first repository lookup until the reader declared it had enough evidence, before drafting. This includes reasoning and tool waits. The six search intervals did not overlap. Opposite orders were represented in the three adjacent pairs. The rubric and results were outside the assigned repositories.

| Pair | Search order | Without glossary, seconds and score | With glossary, seconds and score | Glossary actually used |
| --- | --- | --- | --- | --- |
| 1 | Without, with | 43.0 · 11/11 | 29.4 · 11/11 | No |
| 2 | With, without | 100.9 · 9/11 | 42.0 · 11/11 | No |
| 3 | Without, with | 50.2 · 10/11 | 40.3 · 11/11 | Yes |

## What changed in the tests

All six included launch time in each session's first request, started later timers before request encoding and stopped after decoding the full reply. All used the latest gate of 250/250 unrounded caller times at or below two seconds, with matching result IDs and order. They distinguished a local prepared feedback pair from a verified, nonempty English/Korean pair in the designated inbox. All kept delivery separate from reviewer acceptance.

Two control answers mentioned P95 but omitted its exact calculation, the 48th sorted value among 50 in each round. One of these also gave both partial and complete feedback states without specifying the transition test that repairs the partial delivery and rechecks the same report before changing its status. Both omissions matter when another developer implements the tests. The 11 criteria score explicit coverage, not the number of design errors.

The fastest reader, at 29.4 seconds, reported seeing only the glossary filename. The other nonuser in the treatment group reported no use. Both supported their criteria with original sources. The one actual glossary user read it, cited it together with original sources, and took 40.3 seconds. The 100.9-second control run illustrates the spread. One task, three readers per condition, variable tool latency, self-declared stopping points and unblinded manual grading limit the interpretation. Keep the pilot optional. These data do not justify a mandatory glossary lookup or a speed guarantee. [Full request, rubric, timings, reader answers and use reports](2026-11-25-development-glossary-field-trial.json)
