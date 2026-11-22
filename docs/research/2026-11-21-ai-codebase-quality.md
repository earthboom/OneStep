# AI에 코드 변경을 맡기면서 기존 품질을 지키는 방법

2026-11-21 · OneStep 적용을 위한 조사 · 기존 코드베이스 공통, C++와 Unreal Engine 적용 예시 포함

**변경 계약을 먼저 정하고, 기존 동작과 새 요구를 각각 실행으로 확인하며, 구조는 후속 변경으로 평가한다.** 작업을 맡긴 사람이 매번 상세 지시를 작성할 필요는 없다. 에이전트가 요청과 저장소에서 계약을 찾아 기존 작업 브리프에 짧게 적고, 그에 맞는 증거를 남기는 흐름을 제안한다. OneStep의 현재 검증 절차를 사용하면서 반복적으로 발생하는 회귀에 실행 가능한 검사부터 붙이는 방식이다.

| 지킬 것 | 판정에 쓸 증거 |
| --- | --- |
| **기존 동작과 호환성** | 기존 공개 진입점을 이용해 대표 입력과 실패 경로를 실행한다. 사용 중인 API, 저장 파일, 에셋, 네트워크 계약을 바꿀 때는 실제 구버전 호출자나 고정된 구버전 데이터도 사용한다. |
| **구조와 확장성** | 책임·상태 소유자·허용 의존 방향을 확인한다. 새 콘텐츠나 정책 하나를 더하는 후속 작업에서 변경이 어디까지 퍼지고 무엇을 이해해야 하는지 본다. |
| **운영 품질** | 해당 작업에 성능·수명·실패 복구 요구가 있으면 동일 조건의 기준값, 실제 실행 대상, 실패 후 관찰 상태를 확인한다. 고비용 검사는 해당 위험이 있는 경로에 집중한다. |

## 1. AI 도입과 품질에 관한 실증 근거

| 자료와 근거 유형 | 확인된 내용과 적용 범위 |
| --- | --- |
| **METR, 2025·2026 · 무작위 실험과 후속 조사** | 숙련 오픈소스 개발자 16명이 익숙한 저장소에서 진행한 246개 과제에서 2025년 초 AI 사용 조건은 평균 19% 더 오래 걸렸다. 2026년 글은 후속 실험의 표본 선택과 병렬 작업 시간 측정 문제가 커 현재 효과를 신뢰성 있게 추정하기 어렵다고 설명한다. 우리 작업의 속도는 리뷰와 재작업을 포함해 직접 재는 편이 타당하다. [원 실험](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) · [후속 실험 설계](https://metr.org/blog/2026-02-24-uplift-update/) |
| **Borg 외, Echoes of AI, 2026 · 사전등록 2단계 실험** | 참가자 151명, 95%가 전문 개발자였다. Java 웹 앱의 기능을 AI 사용 여부에 따라 구현한 뒤 다른 개발자가 AI 없이 이어서 작업했다. 무작위 배정된 후속 단계에서 시간과 코드 품질의 유의한 차이를 발견하지 못했다. 실험의 범위는 해당 기능과 후속 과제이며, 반복적인 에이전트 작업의 누적 효과는 별도 질문이다. [학술지 원문](https://link.springer.com/article/10.1007/s10664-026-10889-1) |
| **DORA, 2025 · 팀 설문과 인터뷰** | 약 5,000명의 설문을 포함한 조사에서 AI 활용은 처리량과 양의 관계, 배포 안정성과 음의 관계를 보였다. 조직 수준의 관찰 자료이므로 도입 효과를 인과로 해석하기 어렵다. 처리량과 안정성을 별도 지표로 둘 이유를 준다. [DORA 보고서](https://dora.dev/research/2025/dora-report/) · [연구팀 발표](https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report) |
| **Ogenrwot·Businge, 2026 · GitHub 관찰 연구** | 병합된 에이전트 PR 24,014건과 사람 PR 5,081건의 커밋 수, 수정 파일 폭, 삭제 규모 등에 차이가 있었다. 병합된 PR과 그 변경 특성을 관찰한 결과다. 리뷰에서는 설명과 실제 변경 범위를 함께 읽고, 작업 종류에 따라 범위가 넓어진 이유를 확인할 수 있다. [MSR 논문](https://arxiv.org/abs/2601.17581) |
| **Gloaguen 외, 2026 · 저장소 지침 비교, 프리프린트** | 생성한 지침과 개발자가 커밋한 지침을 평가했다. 평가한 작업에서는 `AGENTS.md` 같은 파일이 일반적으로 성공률을 높이지 못했고 추론 비용은 평균 20% 넘게 늘었다. 에이전트는 지시 자체를 잘 따르는 경향을 보였다. OneStep에는 찾기 어려운 규칙과 실행 방법으로 연결하는 짧은 진입점이 합리적인 출발점이다. [논문 v3](https://arxiv.org/abs/2602.11988) |
| **SWE-CI 및 SlopCodeBench, 2026 · 반복 변경 벤치마크, 프리프린트** | SWE-CI는 실제 저장소 이력에서 얻은 100개 과제의 지속적 통합을 따라간다. SlopCodeBench v2는 36개 문제와 196개 체크포인트에서 에이전트가 자기 코드를 이어서 확장하게 했다. 연구진이 정의한 구조 악화 지표는 궤적의 77%에서 상승했다. 명시적 품질 지침은 초기 지표를 개선했으나 이후 악화율의 차이는 관찰되지 않았다. 이 비율은 해당 벤치마크에서의 관찰이며, OneStep에는 첫 결과물과 다음 작업을 함께 평가하는 방법을 적용할 수 있다. [SWE-CI](https://arxiv.org/abs/2603.03823) · [SlopCodeBench v2](https://arxiv.org/abs/2603.24755v2) |
| **Needle in the Repo, 2026 · 구조 제약을 포함한 평가** | 23개 모델·도구 조합에서 전체 483개 평가 결과 중 64개가 기능 테스트를 모두 통과하고도 평가에 명시된 구조 조건에서 실패했다. 예를 들어 소유권 이전 함수가 받는 쪽 모듈의 검증까지 떠맡았다. 통제된 문제의 결과지만, 기능 테스트와 소유권·의존 방향 검사를 함께 둘 이유를 구체적으로 보여준다. [ASE 논문 §4–5](https://cs.ucr.edu/~qzhang/nitr-ase26.pdf) |
| **OpenAI, SWE-bench Verified 감사, 2026 · 평가 제작자의 재검토** | 모델이 여러 실행에서 일관되게 해결하지 못한 138개 과제를 다시 읽었다. 그중 59.4%에서 테스트 설계나 문제 설명에 중대한 문제를 찾았다. 선택된 실패 표본에 해당하는 비율이다. 누락된 지시나 내부 구현 이름을 강제하는 테스트가 실패하면 제품 계약을 먼저 대조해야 한다. [감사 결과와 사례](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/) |

개발자의 보조 도구 사용, 에이전트의 연속 작업, 팀 단위 도입은 개입과 결과 지표가 서로 다르다. 이 조사에서 적용할 결론은 **대표 과제에서 기존 품질을 지켰는지와 운영 비용을 따로 기록한다**는 것이다. 현재 공개 근거만으로 OneStep의 장기 효과 크기는 추정할 수 없다.

## 2. AI 없이도 검증된 방법과 적용 한계

| 방법 | 원 자료와 OneStep 적용 |
| --- | --- |
| **캡슐화와 실제 호환성 계약** | Parnas는 변경될 설계 결정을 모듈 안에 숨기는 분해를 제안했다. Hyrum Wright의 API 운영 경험은 호출자가 문서에 없는 관찰 가능한 동작에도 의존할 수 있음을 지적한다. 안정적 진입점은 보존하되 정렬·이벤트 순서·실패 코드처럼 기존 호출자가 쓰는 동작을 조사한다. 발견한 우연한 동작을 공식 계약에 넣을지는 실제 의존과 호환성 비용을 보고 정한다. [Parnas 원 논문](https://doi.org/10.1145/361598.361623) · [Hyrum’s Law](https://www.hyrumslaw.com/) |
| **행동 특성화와 단계적 리팩터링** | Feathers의 특성화 테스트는 기존 코드가 실제로 하는 일을 잡아 둔다. 그중 지원할 행동은 호출자·요구로 확인한다. Fowler의 리팩터링 경계는 관찰 가능한 행동을 어느 인터페이스에서 보존할지 정하는 데 유용하다. 작은 준비 리팩터링과 의도적 동작 변경을 구별해 리뷰하면 기대값 변화의 이유가 드러난다. Microsoft 현장 연구는 개발자가 말하는 리팩터링의 동기·위험과 코드 지표를 함께 조사했다. [Feathers 인터뷰](https://techleadjournal.dev/episodes/195/) · [Fowler](https://martinfowler.com/bliki/RefactoringBoundary.html) · [Kim 외, FSE 현장 연구](https://thomas-zimmermann.com/publications/files/kim-fse-2012.pdf) |
| **공개 경계와 실제 의존을 통한 테스트** | Google의 테스트 문서는 결과와 공개 계약을 검사하고, 필요한 경로에서 실제 의존 또는 충실한 대역을 쓰는 기준을 준다. 정상·실패·경계 사례의 기대값은 사양, 별도 계산, 구버전 산출물이나 고정 데이터로 정한다. 결정적 경로는 기준판과 후보판에 동일 입력을 주고 의미 있는 출력을 비교한다. 양쪽이 공유하는 오류를 잡을 독립 사례도 둔다. [테스트와 변경](https://abseil.io/resources/swe-book/html/ch12.html) · [테스트 대역의 충실도](https://testing.googleblog.com/2024/02/increase-test-fidelity-by-avoiding-mocks.html) |
| **테스트가 실제 결함을 잡는지 확인** | Inozemtseva와 Holmes의 Java 실험에서는 테스트 수를 통제했을 때 커버리지와 변이 결함 탐지력 사이의 상관이 낮거나 중간 수준이었다. 커버리지는 빠진 경로를 찾는 데 사용한다. Google의 실무 연구는 리뷰 중 바뀐 코드에 변이를 제한하고 가치가 낮은 변이를 거른다. OneStep에서는 혼자 수행한 작업에서도 독립 기대값을 먼저 고정하고, 중요한 계약 한두 개에 의도적 결함을 넣어 기대한 이유로 실패하는지 볼 수 있다. [ICSE 커버리지 논문](https://cs.uwaterloo.ca/~rtholmes/papers/icse_2014_inozemtseva.pdf) · [Google 변이 테스트 연구](https://research.google/pubs/practical-mutation-testing-at-scale-a-view-from-google/) |
| **불변식과 경계 입력 생성** | QuickCheck의 원 논문은 입력 생성과 속성 판정을 구분한다. 중복 요청은 한 번만 반영되고 취소한 작업은 상태를 쓰지 않는다는 식으로 외부에서 확인할 불변식을 둔다. 시드와 축소된 실패 입력을 기록하며 긴 시간차, 빈 상태, 오래된 ID처럼 드문 입력의 생성 비중을 확인한다. [QuickCheck 원 논문](https://www.cs.tufts.edu/comp/150FP/archive/john-hughes/quick.pdf) |
| **작은 리뷰 단위와 구조 검사** | Google의 리뷰 실무는 리뷰 가능한 단위가 이해와 후속 수정을 돕는 이유를 설명한다. Microsoft의 코드 리뷰 현장 연구는 결함 탐지 외에 변경 이해와 지식 이전을 관찰했다. 진화적 아키텍처의 fitness function은 의존 방향처럼 명시 가능한 구조 조건을 자동 검사로 만든다. 성숙한 코드에 넣을 때는 기존 위반을 기준으로 기록한 뒤 새 위반부터 막고, 구조 선택은 구체적인 다음 변경으로 평가한다. [Google 리뷰](https://abseil.io/resources/swe-book/html/ch08.html) · [Bacchelli·Bird 논문](https://www.ifi.uzh.ch/dam/jcr%3A4d711d23-ce10-4069-8214-eae91797e44b/icse2013.pdf) · [Building Evolutionary Architectures](https://evolutionaryarchitecture.com/precis.html) |
| **빠른 피드백과 전체 적합성** | Meta의 테스트 선택 사례는 변경과 실패의 과거 자료로 CI에서 돌릴 테스트를 좁히는 방법이다. OneStep에서는 영향 경로를 빨리 돌리고, 공유 기반 변경이나 중요한 합류에는 프로젝트가 지원하는 넓은 검사로 보완한다. 선택 근거와 실제 실행 수를 남긴다. [Meta 엔지니어링](https://engineering.fb.com/2018/11/21/developer-tools/predictive-test-selection/) · [Google 회귀 테스트 선택 연구](https://research.google/pubs/regression-test-selection-at-scale-4/) |
| **양쪽 버전이 공존하는 마이그레이션** | `expand → migrate → contract`는 새 계약을 먼저 추가하고 소비자를 옮긴 뒤 구 계약을 걷는다. Branch by Abstraction은 큰 구현 교체를 작은 단계로 진행하는 방법이다. 실제 배포가 있는 경우 카나리의 비교 집단·지표·중단 기준도 쓸 수 있다. 저장 포맷 변경은 기능 스위치를 꺼도 이미 기록된 데이터가 남으므로 롤백 후 실제 읽기·쓰기까지 확인한다. [Parallel Change](https://martinfowler.com/bliki/ParallelChange.html) · [Branch by Abstraction](https://martinfowler.com/bliki/BranchByAbstraction.html) · [Google SRE 카나리](https://sre.google/workbook/canarying-releases/) |

## 3. 팀 운영 사례와 영상

| 자료 | 적용해 볼 부분과 자료의 범위 |
| --- | --- |
| **OpenAI · Harness engineering** | 짧은 진입 문서에서 저장소 안의 자세한 자료로 연결하고, 허용 의존 방향을 린트와 구조 테스트로 검사했다. 검사 메시지에 고치는 방법을 담았다. 새 제품을 만든 팀의 사례이므로 기존 저장소에서는 현재 경계부터 확인하고 한 규칙씩 적용한다. [팀 회고](https://openai.com/index/harness-engineering/) |
| **Anthropic · Effective harnesses for long-running agents** | 세션마다 작은 단위를 완료하고 진행 상태를 다음 세션에 넘겼다. 구현과 단위 테스트 뒤에도 놓친 동작을 실제 사용자 경로에서 발견했다. 웹 앱에서의 운영 사례다. 게임에서는 대상 실행 파일과 런치 모드를 고정하고 다음 세션에서 재실행할 수 있도록 명령을 남긴다. [팀 회고](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents) |
| **OpenAI · Performance Factory** | 운영 지표의 기준선을 두고 비교군으로 원인을 가린다. 다른 에이전트 작업에서 진단에 반례를 대고, 엔지니어가 패치를 리뷰하며 배포 후 회복을 다시 측정한다. 자체 운영 환경 사례이며 소형 프로젝트에는 같은 입력과 빌드로 전후 재현·비교하는 부분부터 적용할 수 있다. [팀 회고](https://openai.com/index/how-openai-performance-factory-keeps-chatgpt-fast/) |
| **Michael Feathers · Tech Lead Journal 195** | 레거시 코드에 테스트를 댈 수 있는 경계와 현재 동작을 기록하는 이유부터 보고, `43:42`의 AI 테스트 도우미 논의로 이어서 본다. 실무자 견해를 담은 인터뷰다. [영상](https://www.youtube.com/watch?v=mwVRHDD0tEk) · [제작자 전사](https://techleadjournal.dev/episodes/195/) |
| **Rebecca Parsons, Neal Ford, James Lewis · GOTO 2023** | 어떤 구조 특성이 프로젝트에 중요한지 먼저 고르고 지속적으로 판정하는 부분을 본다. 컴파일·런타임·팀 경계에 어떤 불변식을 둘지 판단하는 데 연결된다. [영상](https://www.youtube.com/watch?v=m2ZlX1je3as) · [주최자 전사](https://gotopia.tech/episodes/232/building-evolutionary-architectures) |
| **Titus Winters · CppCon 2017** | API와 ABI 호환성, 같은 소스에서 다시 빌드하는 팀과 이미 배포된 바이너리를 지원하는 팀의 조건 차이를 살펴본다. 프로젝트가 실제로 약속하는 호환성 범위를 정할 때 유용하다. [영상](https://www.youtube.com/watch?v=tISy7EJQPzI) · [공식 발표 자료](https://github.com/CppCon/CppCon2017/blob/master/Keynotes/C%2B%2B%20as%20a%20%27Live%20at%20Head%27%20Language/C%2B%2B%20as%20a%20%27Live%20at%20Head%27%20Language%20-%20Titus%20Winters%20-%20CppCon%202017.pdf) |
| **Pete Hodgson · KubeCon 2024** | 시스템 교체를 점진적으로 바꾸는 패턴 발표다. 기존·신규 경로가 공존하는 시기와 되돌리기 기준을 설계할 때 참고한다. [영상](https://www.youtube.com/watch?v=oOHnDhPH3YQ) · [발표자 슬라이드](https://speakerdeck.com/phodgson/migratory-patterns-kubecon-salt-lake-city-2024) |

영상 항목은 주최자·발표자의 소개, 전사 또는 슬라이드를 기준으로 안내했다. 연구 수치와 실제 효과는 위의 원 논문과 운영 보고서를 근거로 삼았다.

## 4. OneStep에서 한 작업을 맡겼을 때의 흐름

기존 OneStep은 설계에서 요구·보존 조건과 판단 근거를 연결하고, 구현에서 기준 실행·독립 기대값·테스트 변경 검토·실사용 확인을 요구한다. 저장소의 유지보수 지식도 코드 크기와 복잡도를 여러 관찰 중 일부로 사용하고, 대표 변경 과제로 검증하라고 안내한다. 따라서 첫 적용은 **현재 흐름에서 어떤 증거를 고정하고 어떤 경계를 자동으로 막을지** 결정하는 일이다. [설계 검토](../../skills/vegabond-code-design/references/review.md) · [코드 검증](../../skills/vegabond-code/references/verification.md) · [유지보수 근거](../../knowledge/code/K-CODE-MAINTAINABILITY-EVIDENCE.md) · [에이전트 지침 점검](../../knowledge/code/K-CODE-AGENT-INSTRUCTION-AUDIT.md)

1. **작업과 보존 계약을 잡는다.** 기준 리비전, 바꿀 행동 한 문장, 계속 성립해야 할 계약, 대표 호출자·상태 소유자·외부 데이터, 성공을 확인할 실행을 기존 브리프에 적는다. 과거 관찰로만 확인한 동작과 지원을 약속한 동작의 근거를 기록한다. 차이가 결과를 바꾸는 경우 현재 호출자나 요구를 조사한다.
2. **기준 실행을 확보한다.** 버그 작업은 고치기 전에 결함을 의도한 이유로 재현하고 주변 사례의 정상 동작도 기록한다. 리팩터링은 보존 계약이 기준판에서 통과해야 한다. 의도적 행동 변경은 바뀌는 기대값의 근거와 보존할 주변 기대값을 정한다. 기준판의 기존 실패, 새 실패, 환경 실패를 판정할 수 있게 실제 대상과 실행 수를 기록한다.
3. **변경을 소유자 주변에 모은다.** 공개 경계로 드러낼 계약과 모듈이 내부에서 관리할 상태를 정한다. 단계적으로 옮겨야 한다면 각 단계에 보존 조건을 둔다. 구현에서 발견한 새 의존성, 호환성 변경, 실패 시 부작용은 브리프와 검증 범위에 반영한다.
4. **후보판의 제품과 테스트를 함께 검토한다.** 같은 공개 진입점과 조건에서 보존 사례를 재실행한다. 추가한 테스트의 기대값을 요구나 고정 자료와 대조한다. 바뀐 assertion, fixture, skip, 필터, lint 억제, 설정을 함께 읽고 이유를 확인한다. 중요한 보호 장치는 의도적으로 고장 낸 후보를 잡는지, 다른 유효한 구현도 허용하는지 확인한다. 다른 검토자나 별도 검토 세션도 같은 계약과 직접 실행한 결과를 사용한다.
5. **결과를 다시 확인할 수 있게 남긴다.** 실행한 명령·리비전·대상·환경·결과, 허용한 호환성 변화와 남은 미검증을 전달한다. 배포나 지속 데이터가 관련된 경우 복구 후 상태까지 검증한다. 다음 에이전트가 같은 결론을 도출할 수 있도록 증거에 연결한다.

| 작업 위험 | 추가할 증거 |
| --- | --- |
| 좁은 국소 수정 | 관련 기존 테스트와 재현 경로. 검증된 범위에 맞춰 간단히 기록한다. |
| 공유 경계·콘텐츠 확장·소유권 이동 | 이전 호출자와 새 호출자, 정상·실패 경로, 의존 방향, 제거 가능한 선택 콘텐츠의 단독 실행. 실제 다음 변경을 하나 수행해 편집 범위와 이해 비용을 본다. |
| 저장·API·ABI·멀티플레이·비동기 수명·프레임 예산 | 해당되는 구버전 데이터나 혼합 버전, 중단·재시도·종료 순서, 실제 런타임과 빌드 구성. 성능 계약은 동일 입력·플랫폼·빌드·워밍업에서 반복 측정하며 프로젝트의 예산과 변동 폭을 사용한다. |

문서는 진입점·예외·판단 근거를 담는다. 실행 명령, 지원 대상, 허용 의존 방향처럼 기계적으로 판정할 수 있는 조건은 재현 가능한 로컬 검사에 둔다. 같은 검사가 반복 사용에서 결함을 잘 잡고 정상 변경을 허용하면 대상 프로젝트의 CI에 연결할 수 있다. CI 검사 결과의 의미나 테스트 기준 자체를 바꾸는 diff에는 리뷰가 필요하다. GitHub를 쓰는 프로젝트는 저장소 조건에 맞으면 필요한 검사와 리뷰를 규칙으로 지정할 수 있다. [GitHub Rulesets 문서](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)

예를 들어 기존 게임에 새 조우 팩을 추가한다면 작업 브리프에 기존 팩·기본 게임의 실행 계약, 팩 로더와 런타임 상태의 소유자, 새 팩이 의존할 수 있는 등록 경계, 각 팩이 단독으로 로드되는 실행 명령을 남긴다. 테스트가 요구하는 기대값은 게임 규칙과 고정 입력에서 계산한다. 완료 판단에는 동작 결과와 변경 파일이 모두 들어간다. 다음 팩을 같은 경로로 추가해 로더나 기존 팩까지 편집해야 하는지 확인한다.

## 5. C++와 Unreal에서 확인하는 방법

| 검증 대상 | 독립 C++ | Unreal C++ |
| --- | --- | --- |
| 기능과 실패 | 실제 공개 API·CLI에 고정 입력을 주고 반환·상태·부작용을 비교한다. 수명 오류나 데이터 경합의 의심 경로에는 플랫폼이 지원하는 Sanitizer를 해당 입력으로 함께 실행한다. [AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html) · [ThreadSanitizer](https://clang.llvm.org/docs/ThreadSanitizer.html) | 엔진 독립 규칙은 작은 테스트로 확인한다. 월드, 타이머, 종료, 복제, 쿠킹에 의존하는 동작은 해당 엔진 대상과 실행 모드까지 검증한다. [Epic Automation Test Framework](https://dev.epicgames.com/documentation/en-us/unreal-engine/automation-test-framework-in-unreal-engine) |
| 의존성과 캡슐화 | `#include`·CMake 타깃 링크 그래프·런타임 등록의 범위를 확인한다. 공개 헤더와 등록 지점에서 상태 소유자와 변경 범위가 드러나는지 보고, 선택 기능을 물리적으로 뺀 빌드나 실행으로 숨은 연결을 찾는다. [CMake Graphviz 옵션](https://cmake.org/cmake/help/latest/manual/cmake.1.html#cmdoption-cmake-graphviz) | `Build.cs`의 공개·비공개 의존성, 에셋 참조, 런타임 로드·활성화 순서를 각각 확인한다. 에디터 동작과 패키지 동작이 모두 계약에 해당하면 두 대상에서 실행한다. [Epic Modules](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-modules) · [Reference Viewer](https://dev.epicgames.com/documentation/en-us/unreal-engine/reference-viewer-in-unreal-engine) |
| 저장·실패 복구 예 | 예전에 생성한 저장 파일을 현재 버전에서 로드하고 실패를 유도한 뒤 기존 파일을 다시 읽는다. 동시 저장·중복 재시도의 계약이 있으면 각 경로의 최종 상태를 확인한다. | 타이머나 저장 콜백이 살아 있는 상태에서 월드 종료나 맵 전환을 거친다. 이전 월드 소유자가 종료 뒤 기록을 남기는지, 다음 월드에 이전 상태가 들어가는지 관찰한다. |

OneStep에는 이미 작은 직접 증거가 있다. **Crossing Tactics**는 의도적으로 넣은 콘텐츠 간 숨은 의존을 B 단독 테스트로 잡았다. **Pulse Arena**는 실제 Unreal Game 월드를 새로 열어 서로 다른 파일 인벤토리와 쿨다운을 검사했고, 결과를 변조한 여섯 사례를 검증기가 거부했다. 이 증거는 문서에 기록된 실행 범위를 뒷받침한다. 기존의 장기 유지 코드, 멀티플레이와 패키징, 후속 변경 비용은 따로 평가할 항목이다. 과거 Unreal 기록에도 잘못된 시간과 값 조합을 허용한 검증기를 고친 사례가 남아 있다. [두 예시와 증거](../examples/cpp-gameplay-workflow/README.md) · [Pulse Arena 실행 범위](../examples/cpp-gameplay-workflow/unreal-action/README.md) · [Unreal 검증기 보정 기록](../../records/code/R-CODE-UE-EVIDENCE-PROXY.md)

## 6. 효과를 확인하는 첫 파일럿

**기존 절차와 기존 절차에 자동 검사 한두 개를 더한 방식을 비교한다.** 새 기능 데모보다 기존 계약과 과거 변경 이력이 있는 코드를 대상으로 한다. 국소 버그, 구조 변경 뒤 콘텐츠 확장, 호환성이나 수명 문제를 포함한 변경에서 시작한다. 같은 기준 리비전과 요구를 별도 작업 복사본에 주고 모델·도구·시간 예산·리뷰 기준을 맞춘다. 가능하면 과제별 실행 순서를 교차하고, 최종 판정은 양쪽에 동일한 독립 체크를 사용한다.

| 관찰 시점 | 수집할 자료 |
| --- | --- |
| 첫 변경 직후 | 기준판과 비교한 기존 계약 실패, 새 요구 충족, 금지한 의존성 추가, 테스트나 검증 설정 완화, 실제 실행 환경과 미검증. |
| 후속 변경 두 차례 | 소유자를 찾아 계약을 이해하는 시간, 영향받은 모듈과 등록 지점, 리뷰가 요청한 재작업, 알려진 고장 패치의 탐지 여부. 정상적인 다른 구현도 검사해 과도한 차단을 센다. |
| 작업 전체 | 생성에서 리뷰·재작업까지 걸린 시간, 도구·CI 비용, 환경 실패로 인한 대기, 불필요한 차단과 실제 결함의 수. |

첫 후보는 **새로 생기는 금지 의존성 검사**와 **실제 진입점의 보존 테스트 하나**다. 확장 작업에서는 기존 팩·새 팩·둘 다·둘 다 없음의 실행과 함께 새 팩이 기존 팩을 은밀히 요구하는 고장 버전을 사용한다. 다음 두 변경에서 보호 장치가 의미 있는 회귀를 잡고 비용을 감당할 수 있으면 적용 범위를 넓힌다. 작은 파일럿의 결과는 과제별로 기록하며, 지표가 나빠진 원인을 코드·요구·테스트·환경으로 추적한다. 이번 조사의 OneStep 적용안은 이 파일럿에서 검증할 가설이다.
