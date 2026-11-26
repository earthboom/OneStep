# AI가 코드를 바꾼 뒤 기존 계약과 후속 변경 비용 확인하기

K-CODE-AI-CHANGE-QUALITY · 방법 · 적용 중 · 근거 확인 2026-11-21

AI 작업 전에 공개 동작과 의존 관계를 기록한다. 첫 패치와 두 번의 후속 변경에서 의도한 변화, 기존 계약, 검토 비용을 각각 측정한다.

적용 범위 — 기존 저장소의 변경. C++와 Unreal을 포함하며 실험 결과는 조사한 과제, 도구, 참여자 범위에 한정된다.

## 적용 방법

기준 리비전, 바꿀 동작, 지원하는 공개 계약, 대표 호출자, 상태 소유자, 실패 시 부수 효과를 기록한다. 특성화 테스트는 관찰한 동작을 보여 준다. 우연히 생긴 동작까지 유지할지는 호출부와 요구사항에서 확인한다. 버그는 실패 재현과 인접한 성공 사례를, 리팩터링은 변경 전 통과 결과를 확보한다. 새 동작의 예상 결과는 독립적으로 구한다.

프로덕션 코드와 테스트를 함께 검토한다. 건너뛴 사례, 기대값·픽스처·필터·허용 오차·경고 억제 변경을 살핀다. 평소 진입점에 고정 입력을 넣고 사양이나 별도 계산으로 구한 결과를 비교한다. 고의로 계약을 어긴 후보가 제대로 실패하고 다른 정상 구현도 통과하는지 확인한다. 커버리지는 실행되지 않은 경로를 찾는 데 쓴다. 생성 입력은 시드, 축소된 반례, 드문 입력의 발생 빈도를 남긴다.

평소에는 영향받는 검사를 먼저 실행한다. 공유 의존성, 호환성, 수명, 성능이 걸리면 범위를 넓힌다. 선택 팩은 단독·조합 실행을 확인한다. 계약을 단계적으로 교체할 때는 새 계약을 추가하고 소비자를 옮긴 후 이전 계약을 제거한다. 기능을 꺼도 이미 쓴 데이터는 새 형식일 수 있으므로 롤백 후 읽기와 쓰기를 검증한다.

## 적용 조건과 예외

배포 안정성, 처리량, 후속 작업량, 검토와 재작업을 포함한 총비용을 구분한다. METR의 2025년 초 실험에서 숙련자 16명은 익숙한 저장소의 과제 246개를 AI 조건에서 평균 19% 더 오래 수행했다. 후속 조사에서는 표본 선택과 병렬 작업의 시간 측정이 추정을 어렵게 했다. Borg 등의 Java 실험은 151명이 참여했고 무작위 후속 단계에서는 유의한 차이가 없었다. DORA 설문 약 5,000명의 결과는 상관관계이며, 병합된 PR 연구에는 거절된 변경이 빠진다.

SlopCodeBench의 구조 지표는 실험 경로의 77%에서 악화했다. Needle in the Repo는 기능 테스트를 모두 통과했지만 구조 조건을 위반한 결과가 483건 중 64건이었다. SWE-bench의 59.4%는 반복 실패 과제 138개를 골라 재검토한 수치다. 저장소 지침 실험에서는 추론 비용이 평균 20% 넘게 늘었다. 연구마다 참여 집단과 결과 지표가 달라 다른 팀의 효과 크기를 바로 추정할 수 없다.

## 확인 방법

평소 절차에 의존 방향 검사 하나와 공개 경로 보존 검사 하나를 추가한 조건을 비교한다. 기준 버전·요구사항·모델·작업 예산·최종 독립 검사를 맞추고 가능하면 수행 순서를 교차한다. 다음 두 번의 변경에서도 소유자를 찾은 시간, 손댄 파일·등록점, 정상 변경 차단, 놓친 결함, 리뷰·재작업을 기록한다. 명령·대상·건수·환경·미확인 범위를 남긴다. C++에서는 CMake와 공개 헤더, 선택 기능 제외 빌드를, Unreal에서는 에셋 참조와 실제 월드·쿠킹·패키지·복제 경로 중 해당 범위를 확인한다.

## 근거

11월 21일 검토는 통제 실험, 관찰 연구, 프리프린트, 벤치마크 감사, 팀 회고를 구분했다. Crossing Tactics에서는 숨은 팩 의존성을 검출했고, Pulse Arena에서는 실제 Game 월드를 다시 열어 확인하고 변조한 결과 6개를 거부했다. 장기 유지보수와 모든 패키지·네트워크 구성까지 평가한 사례는 아니다. 위 비교는 제안된 실험이다.

[실행 사례](../../docs/examples/cpp-gameplay-workflow/README.md) · [검증기 수정 기록](../../records/code/R-CODE-UE-EVIDENCE-PROXY.md) · [유지보수성 판단](K-CODE-MAINTAINABILITY-EVIDENCE.md) · [지침 검토](K-CODE-AGENT-INSTRUCTION-AUDIT.md) · [동작 검사](K-CODE-CHANGE-TESTS.md)

- [METR, 2025 and 2026 — Original experiment](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) · [METR, 2025 and 2026 — Follow-up design](https://metr.org/blog/2026-02-24-uplift-update/) · [Borg et al., Echoes of AI, 2026 — Journal article](https://link.springer.com/article/10.1007/s10664-026-10889-1) · [DORA report](https://dora.dev/research/2025/dora-report/) · [Research team announcement](https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report)
- [Ogenrwot and Businge, 2026 — MSR paper](https://arxiv.org/abs/2601.17581) · [Gloaguen et al., 2026 — Paper v3](https://arxiv.org/abs/2602.11988) · [SWE-CI](https://arxiv.org/abs/2603.03823) · [SlopCodeBench v2](https://arxiv.org/abs/2603.24755v2) · [Needle in the Repo, 2026 — ASE paper, §§4–5](https://cs.ucr.edu/~qzhang/nitr-ase26.pdf)
- [Audit findings and examples](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/)
- [Parnas's original paper](https://doi.org/10.1145/361598.361623) · [Hyrum’s Law](https://www.hyrumslaw.com/) · [Feathers interview](https://techleadjournal.dev/episodes/195/) · [Fowler](https://martinfowler.com/bliki/RefactoringBoundary.html) · [Kim et al., FSE field study](https://thomas-zimmermann.com/publications/files/kim-fse-2012.pdf)
- [Tests and change](https://abseil.io/resources/swe-book/html/ch12.html) · [Test-double fidelity](https://testing.googleblog.com/2024/02/increase-test-fidelity-by-avoiding-mocks.html) · [ICSE coverage paper](https://cs.uwaterloo.ca/~rtholmes/papers/icse_2014_inozemtseva.pdf) · [Google mutation testing study](https://research.google/pubs/practical-mutation-testing-at-scale-a-view-from-google/) · [Invariants and boundary input generation — Original QuickCheck paper](https://www.cs.tufts.edu/comp/150FP/archive/john-hughes/quick.pdf)
- [Google code review](https://abseil.io/resources/swe-book/html/ch08.html) · [Bacchelli and Bird paper](https://www.ifi.uzh.ch/dam/jcr%3A4d711d23-ce10-4069-8214-eae91797e44b/icse2013.pdf) · [Building Evolutionary Architectures](https://evolutionaryarchitecture.com/precis.html) · [Meta Engineering](https://engineering.fb.com/2018/11/21/developer-tools/predictive-test-selection/) · [Google regression test selection study](https://research.google/pubs/regression-test-selection-at-scale-4/)
- [Parallel Change](https://martinfowler.com/bliki/ParallelChange.html) · [Branch by Abstraction](https://martinfowler.com/bliki/BranchByAbstraction.html) · [Google SRE on canaries](https://sre.google/workbook/canarying-releases/)
- [OpenAI — Team retrospective](https://openai.com/index/harness-engineering/) · [Anthropic — Team retrospective](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents) · [OpenAI — Team retrospective](https://openai.com/index/how-openai-performance-factory-keeps-chatgpt-fast/) · [Michael Feathers — Video](https://www.youtube.com/watch?v=mwVRHDD0tEk) · [Rebecca Parsons, Neal Ford, James Lewis — Video](https://www.youtube.com/watch?v=m2ZlX1je3as)
- [Organizer's transcript](https://gotopia.tech/episodes/232/building-evolutionary-architectures) · [Titus Winters — Video](https://www.youtube.com/watch?v=tISy7EJQPzI) · [Titus Winters — Official slides](https://github.com/CppCon/CppCon2017/blob/master/Keynotes/C%2B%2B%20as%20a%20%27Live%20at%20Head%27%20Language/C%2B%2B%20as%20a%20%27Live%20at%20Head%27%20Language%20-%20Titus%20Winters%20-%20CppCon%202017.pdf) · [Pete Hodgson — Video](https://www.youtube.com/watch?v=oOHnDhPH3YQ) · [Speaker's slides](https://speakerdeck.com/phodgson/migratory-patterns-kubecon-salt-lake-city-2024)
- [GitHub Rulesets documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
- [AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html) · [ThreadSanitizer](https://clang.llvm.org/docs/ThreadSanitizer.html) · [Epic Automation Test Framework](https://dev.epicgames.com/documentation/en-us/unreal-engine/automation-test-framework-in-unreal-engine) · [CMake Graphviz options](https://cmake.org/cmake/help/latest/manual/cmake.1.html#cmdoption-cmake-graphviz) · [Epic Modules](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-modules)
- [Reference Viewer](https://dev.epicgames.com/documentation/en-us/unreal-engine/reference-viewer-in-unreal-engine)

## AI 슬롭이 의심되는 코드 변경을 판단하는 법 · 2026-11-26 조사

AI 슬롭이라는 말을 검토자가 확인할 수 있는 질문으로 바꾼다. 지원하던 동작이 깨졌는가? 불필요한 의존성이 생겼는가? 다음 담당자가 같은 규칙을 바꾸기 위해 무엇을 다시 알아내야 하는가? 작성자나 줄 수만으로는 답할 수 없다.

| 발견 | 자료가 보여 주는 범위 | OneStep에 적용할 판단 |
| --- | --- | --- |
| 기능 테스트를 통과하고도 구조적 계약을 깰 수 있다. | Needle in the Repo에서는 평가 결과 483건 중 64건이 기능 테스트를 통과하고 지정한 구조 제약에 실패했다. SlopCodeBench v2는 36개 문제와 196개 체크포인트로 반복 변경을 평가했고, 작업 궤적 77%에서 구조 악화 지표가 올랐다. 두 연구 모두 지정한 제약과 대리 지표를 측정했다. [저장소 변경 연구](https://cs.ucr.edu/~qzhang/nitr-ase26.pdf) · [반복 수정 벤치마크](https://arxiv.org/abs/2603.24755v2) | 독립 설치를 약속한 기능은 단독으로 실행한다. 두 호출자가 같은 규칙을 써야 한다면 한 번의 규칙 변경이 양쪽에 반영되는지 본다. 새 추상화는 지금 필요한 호출자나 계약으로 정당화한다. [Fowler의 YAGNI](https://martinfowler.com/bliki/Yagni.html) |
| 유지보수 비용이 언제나 높아지는 것은 아니다. | Borg 등의 사전등록 2단계 연구에는 151명이 참여했다. 다른 개발자가 AI 없이 Java 코드를 확장한 단계에서, 원래 코드를 작성할 때 AI를 썼는지에 따른 시간·품질 차이는 유의하지 않았다. 한 번의 후속 작업으로 장기간 누적 효과를 판단하기는 어렵다. [Echoes of AI](https://link.springer.com/article/10.1007/s10664-026-10889-1) | 비슷한 후속 변경에서 수정 시간과 리뷰어의 부담을 함께 비교한다. 적절히 단순한 구현에 구조가 적다는 이유로 감점하지 않는다. |
| 틀린 기대값도 설명이 붙으면 그럴듯하다. | Python 개발자 86명의 생성 단언문 판별 연구에서 올바른 단언의 판별 정확도는 74%, 틀린 단언은 49%였고 자연어 설명의 전반적 이점은 없었다. 별도의 개발자 52명 Trio 학습 실험에서는 AI 사용 집단의 직후 이해도가 낮았다. 전자는 단언문 판별, 후자는 단기 학습을 측정했다. [단언문 연구](https://arxiv.org/abs/2607.08885) · [Trio 실험과 한계](https://www.anthropic.com/research/AI-assistance-coding-skills) | 합격 여부가 갈리는 분기에서는 생성된 기대값을 보기 전에 호출자나 제품 결정으로 답을 정한다. 결함 버전은 잡으면서 다른 올바른 구현은 통과시키는 입력을 찾는다. |
| 그럴듯한 API 이름이나 패키지도 실제 계약을 확인해야 한다. | Spracklen 등은 16개 모델이 생성한 Python·JavaScript 코드 57만 6천 개를 조사해 존재하지 않는 패키지 추천을 확인했다. 이 비율을 Unreal이나 OneStep에 그대로 적용할 수 없다. [USENIX 논문·강연](https://www.usenix.org/conference/usenixsecurity25/presentation/spracklen) | 새 의존성은 패키지 정체, 설치·고정 버전, 실제로 필요한 연산을 확인한다. 엔진 API는 설치된 선언이나 해당 버전의 공식 문서와 대조하고 관련 빌드·실행 경로로 확인한다. |
| 작성자가 줄인 시간이 리뷰어에게 넘어갈 수 있다. | LLVM의 기여 지침과 Google의 작은 변경 검토 지침은 팀의 운영 경험이다. Tufano 등의 11월 24일 사전논문은 선택한 커밋·대화·인터뷰에서 개발자가 AI에 귀속한 품질 문제 87가지 유형을 분류했다. 모든 변경 중 발생률을 뜻하지 않는다. [LLVM 정책](https://llvm.org/docs/AIToolPolicy.html) · [Google 검토 지침](https://google.github.io/eng-practices/review/developer/small-cls.html) · [실제 사례 분류](https://arxiv.org/abs/2611.32676) | 바뀐 결정, 계약의 소유자 또는 호출자, 다시 확인할 관찰 결과를 함께 넘긴다. 동작 변경을 가리는 독립적인 정리는 분리한다. |

**책·강연·실무 기록.** 마이클 페더스는 기존 동작을 관찰하는 특성화 테스트와 새 요구의 기대값을 구분한다. 인터뷰 30분 6초부터는 AI가 남기는 레거시를 다룬다. 포드·파슨스·루이스는 아키텍처 제약을 실행 가능한 검사로 표현하는 방법을 설명한다. 영상은 제작자가 제공한 대담록과 장 구분으로 내용을 확인했다. 『Software Engineering at Google』 12장은 구현 세부사항에 덜 결합된 테스트를, 사이먼 윌리슨의 실무 기록은 실제 UI나 CLI로 주장을 확인하는 방법을 제시한다. [페더스 유튜브 30:06](https://www.youtube.com/watch?v=mwVRHDD0tEk&t=1806s) · [대담록](https://techleadjournal.dev/episodes/195/) · [GOTO 대담 및 원문](https://gotopia.tech/episodes/232/building-evolutionary-architectures) · [책 12장](https://abseil.io/resources/swe-book/html/ch12.html) · [실제 진입점 검사 사례](https://simonwillison.net/guides/agentic-engineering-patterns/agentic-manual-testing/)

**OneStep 시범 적용안.** [개발 설계 인계](../../skills/vegabond-code-design/SKILL.md)와 [코드 검증 절차](../../skills/vegabond-code/references/verification.md)를 사용한다. 공유 규칙·공개 계약·의존성이 바뀔 때만 조용히 깨질 수 있는 동작과 그 결함을 드러낼 관찰을 한 문장에 적는다. 문구만 고치는 요청은 기존 직접 검사로 끝낸다. 양쪽 조건 모두 기존 테스트를 유지하고, 독립적으로 도출한 반례와 올바른 대안 구현 하나를 최종 평가용으로 남긴다. 같은 시작 리비전·과제·모델 예산에서 별도 맥락으로 기존 지침과 조건부 지침을 비교한다. 놓친 계약 위반, 올바른 구현의 오거절, 리뷰·재작업 시간, 후속 변경 두 건의 비용을 기록한다. 여러 비교에서 결함 누락이 줄고 오거절이나 검토 비용이 이득을 상쇄하지 않을 때 기본 절차로 채택한다. 저장소 공통 지침의 분량에도 비용이 든다. [저장소 지침 실험](https://arxiv.org/abs/2602.11988)

**프로젝트 검증 · 2026-11-26.** 임시 폴더에서 Visual Studio 2022 Professional로 [Crossing Tactics 예제](../../docs/examples/cpp-gameplay-workflow/native-tactics/README.md)를 빌드하고 `python -B verify.py --fault`를 실행했다. 정상판은 팩 없음·A만·B만·둘 다의 네 배치를 통과했다. B가 A에 의존하도록 결함을 넣자 두 팩이 함께 있을 때는 여전히 통과했지만, B 단독 실행에서 카탈로그 누락과 선택 거절이 확인됐다. 이 예제에서 해당 검사가 결함을 구별함을 확인했다. AI 작업 방식이나 리뷰 비용 비교는 아직 수행하지 않았다.

## 개발 설계·구현 조건부 시범 적용, 2026-11-26

이전 대화를 모르는 AI 두 개에 같은 Python 예약 앱, 계약, 영어 스킬을 제공했다. 설계·구현 스킬의 시범 문구만 달랐다. 각 작업자는 오타를 고치고, 같은 미완성 변경을 수정 전에 리뷰한 뒤 수리했다. 이어서 후속 요청을 하나씩 받아 자기 결과물을 변경했다. 리뷰는 구현자가 전달받은 코드에서 결함을 찾은 시간이다. 같은 Windows 호스트의 단조 시계로 단계별 추론·셸·테스트를 포함한 경과 시간을 쟀다. 세션 준비, 요청 사이의 대기, 독립 채점은 측정 구간 밖에 있다. 요청 원문 (로컬 검증 파일 `skills/vegabond-code-design/tests/change-quality/cases.json`) · 최초 계약 (로컬 검증 파일 `skills/vegabond-code-design/tests/change-quality/fixture/CONTRACT.txt`)

| 관측 항목 | 기존 절차 | 조건부 절차 |
| --- | ---: | ---: |
| 리뷰에서 놓친 결함 / 준비한 3건 | 0건 | 0건 |
| 정상 대안 오거부 / 1건 | 1건 | 0건 |
| 리뷰 / 수리 및 검증 | 64.9초 / 20.9초 | 58.4초 / 20.2초 |
| 후속 1. 자정을 넘는 예약 | 48.6초 | 27.5초 |
| 후속 2. 픽업과 일시 중지 | 45.4초 | 51.4초 |
| 오타 수정, 최초 스킬 읽기 포함 | 80.1초 | 72.3초 |

양쪽 모두 빈 영업시간에 기본값을 적용하는 오류, 마감 시각의 예약 허용, 피드의 장소 설정 누락을 잡았다. 각 절차가 제출한 결과는 독립 검사에서 최초 9개, 후속 1에서 15개, 후속 2에서 50개를 모두 통과했다. 채점 후 추가 수리는 양쪽 모두 0건이었다. 기존 절차의 테스트는 데스크 모듈을 제거한 상태에서도 피드가 작동해야 한다고 요구했다. 계약은 데스크가 닫혀 있어도 피드를 조회할 수 있다고 규정하고, 이 앱은 두 모듈을 함께 배포한다. 설치된 데스크 함수를 재사용하는 대안은 공개 동작 검사를 모두 통과했으며 조건부 절차의 테스트도 이를 허용했다. 향후 단독 설치를 지원한다면 모듈 제거 검사에도 근거가 생긴다.

두 후속 변경 모두 각 절차에서 실행 코드 한 파일씩을 건드렸다. 합계는 기존 94.0초·조건부 78.9초였고, 추가한 테스트 줄 수는 각각 20줄·30줄이었다. 오타 수정은 양쪽 모두 바로 처리해 한 파일 한 줄만 바뀌었다. 이번 한 쌍의 결과는 선택적으로 적용할 근거다. 결함 누락이나 소요 시간이 일반적으로 줄어드는지는 다른 작업에서 반복 측정해야 한다. 저장소 루트에서 `python skills/vegabond-code-design/tests/change-quality/evaluate.py`로 결과를 재검증할 수 있다. 시간·리뷰·독립 채점 원자료 (로컬 검증 파일 `skills/vegabond-code-design/tests/change-quality/results.json`) · 단계별 제출 변경 (로컬 검증 파일 `skills/vegabond-code-design/tests/change-quality/submissions.json`)

## OneStep 실제 저장소 비교, 2026-11-26

**판단은 구체적인 의문이 남는 변경에 한해 조건부 검사를 유지하는 것이다.** 설계 인계에는 기대 결과를 정하는 호출자와 차이를 볼 수 있는 사례를 남긴다. 기존 테스트가 의심되는 오동작도 통과시키거나 허용된 구현을 거부할 가능성이 있을 때 추가 대안을 실행한다. 기존 공개 경로 검사로 판별이 끝나면 그 증거를 재사용한다. 앞선 예약 앱에서는 정상 대안 오거부를 줄였지만, 이번 실험에서는 모든 공유 규칙·의존성 변경에 별도 검사를 실행할 만큼의 이점이 관찰되지 않았다.

이전 대화를 공유하지 않은 AI 8개에 OneStep 커밋 `99cd60c`의 실제 운영 스크립트를 제공했다. 두 과제를 절차별로 두 번씩 수행했다. 각 쌍은 같은 미완성 패치와 요청을 리뷰·수리한 다음 자기 제출본에 같은 후속 요청을 적용했다. 결함은 측정용으로 넣었고 변경은 격리된 복사본에만 적용했다. 포터블 설치기에는 읽기 전용 검사와 어댑터 한 개 선택을 순서대로 추가했다. 지식 문서 판독기에는 표준 라이브러리만 사용하는 프로젝트 기준 JSON 선택자 입력을 추가하고, 후속 변경으로 BOM과 빈 배열을 지원했다. 설치기는 실제 배포 ZIP에서, 판독기는 기존 테스트 6개와 공개 CLI에서 추가로 검증했다. 과제와 시작 코드 (로컬 검증 파일 `skills/vegabond-code-design/tests/repository-change-quality/material.py`) · 실험 조건과 스킬 차이 (로컬 검증 파일 `skills/vegabond-code-design/tests/repository-change-quality/protocol.json`)

| 과제와 반복 | 기존 리뷰 / 재작업 / 후속 변경(초) | 조건부 리뷰 / 재작업 / 후속 변경(초) |
| --- | ---: | ---: |
| 설치기 1차 | 103.4 / 95.2 / 76.5 | 131.5 / 83.1 / 99.1 |
| 설치기 2차 | 130.6 / 118.3 / 96.7 | 99.5 / 115.9 / 156.1 |
| 문서 판독기 1차 | 100.2 / 130.9 / 121.0 | 97.1 / 106.3 / 123.1 |
| 문서 판독기 2차 | 78.0 / 120.6 / 99.7 | 104.6 / 129.0 / 196.6 |
| 원자료 기준 합계 | 412.2 / 465.0 / 393.9 | 432.8 / 434.4 / 574.9 |

수정 전에 저장한 리뷰를 비교한 결과, 각 절차가 다섯 가지 결함 원인을 두 번씩 모두 지적했다. 설치기는 공유 전략 누락을 허용하거나 정상 CRLF 파일을 거부했다. 판독기는 YAML 의존성과 문법을 사용했고, 파일의 기준 디렉터리가 잘못됐으며, 잘못된 선택자 값을 문자열로 바꿔 허용했다. 각 절차가 작성한 테스트는 결함을 하나씩 되살린 10건을 전부 거부했고, 고정한 정상 대안과 상대 작업자의 검증된 구현을 합한 8건을 전부 허용했다. 제출본은 절차별로 독립 검사 최초 42건·후속 60건을 모두 통과했다. 채점 후 추가 수리는 0건이었다. 리뷰·시간·제출 변경 (로컬 검증 파일 `skills/vegabond-code-design/tests/repository-change-quality/submissions.json`) · 실행별 채점 (로컬 검증 파일 `skills/vegabond-code-design/tests/repository-change-quality/results.json`)

리뷰와 최초 수리·검증 합계는 기존 877.2초, 조건부 867.2초였다. 후속 변경은 네 쌍 모두 조건부 절차에서 길어졌으며 합계 차이는 181.0초(46.0%)였다. 네 후속 요청의 실행 코드 변경량은 기존 23줄 추가·14줄 삭제, 조건부 23줄 추가·12줄 삭제였다. 전체 계측 시간은 1,271.1초에서 1,442.0초로 늘었다. Windows와 Python 3.12.3을 사용한 공유 호스트에서 두 과제를 반복한 결과다. 작업자와 실행 부하가 달라 시간 차이 전부를 스킬의 효과로 귀속할 수 없다. 측정 범위는 AI 경과 시간과 준비한 공개 동작 검사까지다. 실험 폴더의 `replay.py`와 `challenges.py`로 계약·교차 검사와 결함별 검사를 다시 실행할 수 있다. 계약·교차 재검증 (로컬 검증 파일 `skills/vegabond-code-design/tests/repository-change-quality/replay.py`) · 결함별 재검증 (로컬 검증 파일 `skills/vegabond-code-design/tests/repository-change-quality/challenges.py`)

## 기존 테스트로 판별이 끝나는 시점, 2026-11-26

설계는 호출자가 기대하는 결과와 이를 단언하는 기존 공개 경로 테스트를 인계한다. 구현은 해당 테스트를 변경한 코드에 실행한다. 테스트가 통과하고 단언이 예상 결함을 잡으면서 동등한 정상 구현도 허용하면 그 검증을 마친다. 판정에 의문이 남을 때만 이를 가릴 최소 대안을 검사한다. [설계 스킬](../../skills/vegabond-code-design/SKILL.md) · [구현 스킬](../../skills/vegabond-code/SKILL.md)

이전 대화를 공유하지 않은 AI 8개가 앞선 설치기·문서 판독기 후속 변경을 다시 수행했다. 각 쌍의 시작 코드, 테스트, 요청, 주의할 사례, 선택적으로 쓸 수 있는 대안 실행 도구는 같았다. 비교군에는 직전 조건부 스킬을 제공했다. 각 과제에 기존 단언이 충분한 경우와 결함을 통과시키는 경우를 하나씩 준비했다. 독립적으로 확인한 약점은 설치기에서 ‘선택한 파일은 최신이고 공유 전략이 없음’을 검사하지 않는 경우, 판독기에서 표준 출력의 공백을 지우고 빈 문자열과 비교하는 경우였다. 비교 조건과 스킬 문구 (로컬 검증 파일 `skills/vegabond-code-design/tests/repository-change-quality/followup_protocol.json`) · 입력 생성 (로컬 검증 파일 `skills/vegabond-code-design/tests/repository-change-quality/followup_inputs.py`)

| 후속 변경 경과 시간 | 직전 조건부 기준 | 새 종료 기준 |
| --- | ---: | ---: |
| 설치기, 기존 단언 충분 | 112.7초 | 93.3초 |
| 문서 판독기, 기존 단언 충분 | 125.6초 | 121.7초 |
| 설치기, 경계 사례 누락 | 205.7초 | 241.4초 |
| 문서 판독기, 약한 단언 | 164.4초 | 113.2초 |
| 합계 | 608.5초 | 569.5초 |

새 기준은 단언이 충분한 두 작업을 테스트 수정과 대안 실행 없이 끝냈다. 불분명한 두 작업에서는 단언을 보강해 결함 대안을 거부했다. 설치기에서는 단언 보강 전후로 같은 대안을 한 번씩 실행했다. 직전 기준도 두 약점을 보완했지만, 충분한 조건 한 건에서 대안을 더 실행했다. 전체 대안 실행 횟수는 양쪽 모두 3회였다. 각 절차는 공개 계약 검사 60건을 모두 통과했고, 최종 테스트는 기준 정상 구현을 4/4회 허용하고 결함 구현을 4/4회 거부했다. 새 기준의 합계는 39.0초(6.4%) 짧았고, 설치기 경계 사례 보완은 35.6초 길었다. 같은 호스트에서 과제·조건별 한 쌍씩 관찰한 AI 경과 시간이다. 앞선 실험과는 시작 테스트와 작업자 맥락이 달라 이번에 재실행한 직전 기준을 비교 대상으로 삼았다. 실행별 결과 (로컬 검증 파일 `skills/vegabond-code-design/tests/repository-change-quality/followup-results.json`) · 시간 기록과 제출 변경 (로컬 검증 파일 `skills/vegabond-code-design/tests/repository-change-quality/followup-submissions.json`) · 재검증 스크립트 (로컬 검증 파일 `skills/vegabond-code-design/tests/repository-change-quality/followup_replay.py`)
