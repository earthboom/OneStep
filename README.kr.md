# OneStep

저자 **vagabond**는 언리얼 엔진으로 게임을 개발하는 클라이언트 프로그래머입니다.

OneStep은 소프트웨어 개발, 소설, 발표자료, 기획서, 조사 등 다양한 작업을 AI와 함께 완성하기 위한 에이전트 지침과 스킬 모음입니다. 저자의 배경이 지원 분야를 제한하지 않습니다. 요청한 결과에 맞는 방법을 연결하고 실제 결과를 점검하며 관련 지식과 수정 근거를 이후 작업에서 재사용합니다. AI 검증과 저자의 독립 검토는 별도 단계입니다.

## 작업 시작

이 저장소에서 AI에게 공통 지침과 시작 스킬을 읽도록 요청합니다.

```text
Read agents/vegabond-agent.md, then use
skills/vegabond-scout/SKILL.md to handle the following task:

[원하는 결과, 관련 자료, 제약을 설명합니다.]
```

[에이전트 지침](agents/vegabond-agent.md)은 공통 경계·검증·수락을, [scout](skills/vegabond-scout/SKILL.md)은 작업 이해와 스킬·점검 연결을 담당합니다. 직접 호출한 작업·전문 스킬도 공통 준비를 재사용합니다.

경로는 저장소 기준입니다. 다른 작업 공간에서는 찾을 수 있는 지침 경로나 해당 환경의 스킬 로딩 방식을 사용합니다. 전역 설치나 자동 탐색을 보장하지 않습니다. 스킬을 읽는다고 에이전트가 생성되지 않으며 도구·위임은 실행 환경과 권한에 따릅니다.

## 작업 흐름

1. **요청 이해:** 대상, 원하는 변화, 보존 조건, 방법을 파악하고 목표·범위·완료 조건을 짧게 정리합니다.
2. **맥락 조회:** 적용 지식, 이전 수정, 출처, 빈틈을 요청하고 유효한 정보 요약을 재사용합니다.
3. **방식·규모 선택:** 분야·규모와 독립적으로 create, revise, research를 선택하고 단계마다 스킬 또는 도구와 점검을 연결합니다.
4. **수행·검증:** 의존 작업 전에 필수 출처·점검 도구의 준비를 확인합니다. 전문 방법으로 실제 결과를 검사하고 수정 후 영향받는 검증을 반복합니다.
5. **발견 대응:** 결함 수정, 부족한 근거 조사, 목표·범위 변화에 따른 요약 갱신을 수행합니다. 유용한 발견은 허용된 프로젝트 범위에 기록합니다.
6. **독립 검토:** 결과, 완료 근거, 한계를 반환합니다. vagabond의 별도 테스트·검토와 명시적 확인으로 최종 수락합니다.

**single**은 간결한 수행·검증 작업의 기본값입니다. 의존 작업 전에 이름 붙인 중간 결과를 확인해야 하면 **staged**를 사용합니다. 파일·도구 수만으로 단계를 늘리지 않습니다. 각 단계는 연결된 작업 스킬을 사용하고 최종 결과를 통합 점검합니다.

[작업 흐름 그림](docs/diagrams/onestep-workflow.png)과 [SVG](docs/diagrams/onestep-workflow.svg)를 참고할 수 있습니다.

## 스킬

| 스킬 | 책임 |
| --- | --- |
| [vegabond-scout](skills/vegabond-scout/SKILL.md) | 작업 프로필·요약·규모·역량 연결·전체 조율. |
| [vegabond-create](skills/vegabond-create/SKILL.md) | 제공 자료에서 파생한 결과를 포함하여 새 결과물·기능 제작. |
| [vegabond-revise](skills/vegabond-revise/SKILL.md) | 필요한 계약을 보존하며 기존 결과 수정·개선. |
| [vegabond-research](skills/vegabond-research/SKILL.md) | 조사 대상 출처를 유지하며 질문 조사·대안 비교. |
| [vegabond-code](skills/vegabond-code/SKILL.md) | 실제 환경 식별, 소프트웨어 구현·검수·테스트·실행. |
| [vegabond-code-design](skills/vegabond-code-design/SKILL.md) | 필요한 구조·소유권·인터페이스와 검증 가능한 설계 결정 확정. |
| [vegabond-fiction](skills/vegabond-fiction/SKILL.md) | 작품 맥락·문체 참조 조회, 집필·비평·수정·원고 점검. |
| [vegabond-fiction-design](skills/vegabond-fiction-design/SKILL.md) | 설계가 필요할 때 20개 서사 요소를 범위에 맞는 선택·효과·점검에 연결. |
| [vegabond-presentation](skills/vegabond-presentation/SKILL.md) | 발표 흐름, 자료 제작, 주장 검증, 최종 출력 점검. |
| [vegabond-planning](skills/vegabond-planning/SKILL.md) | 제안·실현 가능성·의존성·계산·성공 지표 개발·평가. |
| [vegabond-knowledge](skills/vegabond-knowledge/SKILL.md) | 범위가 정해진 지식·문제 기록 조회·취합·저장·관리. |

작업 스킬이 흐름을 소유하고 전문 스킬이 수행 방법을 제공합니다. 기획 내용과 발표 제작처럼 필요한 전문 스킬을 결합합니다. 다른 분야는 요청마다 새 전문 스킬을 추가하지 않고 적합한 기존 스킬이나 도구를 사용할 수 있습니다.

### 코딩

소스·설정·의존성·스크립트·테스트로 실제 변경 대상을 분류합니다. 언리얼 C++, 유니티 C#, 독립 C++, 엔진 저장소 안의 Python 도구는 실행 경로가 다를 수 있습니다. 영향이 다른 환경에 도달하면 통합 점검을 추가합니다.

중요한 구조 선택은 [code-design](skills/vegabond-code-design/SKILL.md)에 맡기고 결과를 현재 작업에서 재사용합니다. 기존 패턴의 작은 수정은 조건만 확인하고 진행할 수 있습니다. 설계만 요청받으면 설계로 끝냅니다. 상세 점검·수정·재개 상태는 [검증 참조 문서](skills/vegabond-code/references/verification.md)에 있으며 코드 변경·판정 전에 읽습니다.

검증은 해당되는 빌드·준비, 자동 테스트, 실행 준비, 실제 사용을 포함합니다. 게임은 에디터·실제 플레이, CLI는 실제 명령, 라이브러리는 사용 주체나 검증 환경이 필요합니다. 최종 통합 검증 전에 검수·수정을 반복합니다.

### 소설

기존 기준 자료에서 장면의 세계 규칙, 인물 상태, 관계, 시간, 공개 범위를 조회합니다. 정본, 임시 계획, 소문, 미확인을 구별하며 저자 지식이 인물·독자 지식으로 조용히 바뀌지 않게 합니다.

중요한 서사 선택은 [fiction-design](skills/vegabond-fiction-design/SKILL.md)에 맡기고 결과를 현재 작업에서 재사용합니다. 설계는 이야기 논리, 인물, 서사 동력, 전달, 작품 방향·결말의 20개 요소를 검토합니다. 국소 작업은 관련 요소를 선택하고 모든 장면에 20개 장치를 강요하지 않습니다. 상세 판단·문체·수정·재발 절차는 [원고 검수](skills/vegabond-fiction/references/review.md)에 둡니다. 설계만 요청받으면 설계를 제공하며 의도한 독자 효과와 실제 반응을 구별합니다.

저자 작성·선택 구절로 작품별 문체 기준을 정합니다. 인과성·핍진성·연속성·독자 이해·문체·언어를 검토하고 오류·가설·제안을 구별합니다. AI 같은 느낌 자체를 오류로 삼거나 보편적 금지어 목록을 강제하지 않고 중복 설명·구분 없는 대화 같은 구체적인 효과를 진단합니다.

재사용할 전후 수정은 원출처, 적용 조건, 재검증, 실제 저자 피드백과 함께 저장합니다. 이후 집필은 표현을 복사하지 않고 기준·점검을 조회합니다. AI 판단만으로 독자 합의나 저자 수락이 성립하지 않습니다.

## 완료와 피드백

완료 조건을 현재 점검·근거에 연결합니다. 실행할 수 없는 필수 점검은 **차단**이며 통과나 해당 없음이 아닙니다. 이후 편집으로 무효화된 근거는 다시 확인합니다. 준비나 모의 테스트 성공만으로 실제 환경의 최종 결과가 작동한다고 볼 수 없습니다.

필수 점검 뒤 **AI verification complete; awaiting vagabond testing or review**라고 보고합니다. 명시적 확인 뒤에만 **accepted by vagabond**라고 합니다. 결함과 새 요청·선호를 구분합니다. 같은 전제의 수정 두 번이 같은 점검에서 실패하면 다음 시도 전에 전제를 재검토합니다.

## 지식과 문제 기록

- [knowledge/](knowledge/index.md): 참조, 관례, 방법, 확인된 재사용 교훈.
- [records/](records/index.md): 관찰한 발견, 원인 확신도, 수정, 재검증 근거.

코딩·소설·발표자료·기획서·공통 분야의 관련 색인 행과 상세를 조회하며 전체 이력을 읽지 않습니다. 범위·맥락·출처·예외를 보존합니다. 사건 해결과 예방 검증은 별개이며 수정 기록만으로 재발 방지가 입증되지 않습니다.

저장소는 작업 프로젝트에 속합니다. 다른 프로젝트는 자체 저장소와 출처를 쓰고 OneStep 사실을 자동으로 가져오지 않습니다. 적합한 기존 설정 문서나 지식 체계는 재사용합니다. 시험 자료는 실제 기록과 분리합니다. 일반 조회를 이유로 빈 저장소를 만들거나 전체 재생성을 하지 않습니다.

[저장 지침](skills/vegabond-knowledge/references/storage.md)은 형식·통합·승격·정리의 기준입니다. [색인 도우미](skills/vegabond-knowledge/scripts/catalog.py)는 실행 환경의 Python 3.9 이상과 PyYAML을 사용합니다.

허용된 갱신은 영문 상세와 번역본을 쓴 뒤 영향받는 색인을 만듭니다.

```text
python skills/vegabond-knowledge/scripts/catalog.py build --project . --domain fiction
```

`catalogs_written`의 바뀐 영문 색인마다 번역을 다시 생성하고 점검합니다.

```text
python skills/vegabond-knowledge/scripts/catalog.py check --project . --domain fiction --strict
```

fiction 대신 해당 분야를 사용합니다. 다른 프로젝트는 도우미의 절대 경로와 해당 프로젝트의 `--project`를 사용합니다. 첫 build는 임시 색인 없이 계획된 색인을 만들 수 있습니다. 도우미는 상세·번역을 작성하지 않으며 구조 검증으로 사실성·번역·문학적 품질이 입증되지는 않습니다.

## 저장소 구조

```text
agents/                  공통 에이전트 지침
skills/                  시작·작업·전문·지식 스킬
knowledge/               분야별 참조·재사용 지식
records/                 실제 발견·수정 근거
docs/designs/            저장 설계 문서
docs/diagrams/           작업 흐름 이미지
README.md                영문 개요
README.kr.md             사용자용 한국어 번역
```

도우미의 자동 테스트는 [tests/](skills/vegabond-knowledge/tests/test_catalog.py)에 있습니다.

```text
python -m unittest discover -s skills/vegabond-knowledge/tests -v
```

테스트는 격리된 임시 자료를 만듭니다. 기존 쓰기 가능 디렉터리를 `ONESTEP_TEST_ROOT`로 지정해 위치를 고를 수 있습니다. 이는 색인 테스트이며 실제 작업 흐름이나 분야별 실행·검토를 대신하지 않습니다.

## 문서 언어

프로젝트 지침, 에이전트·스킬 지침, 저장 문서는 영문으로 작성합니다. `<stem>.kr.md`는 사용자 전용 번역입니다. AI는 읽기·검색·색인·위임에서 내용을 제외하고 영문에서 생성한 뒤 다시 읽지 않습니다.

작업 입력과 결과물은 요청 언어를 따릅니다. 원래 한국어 원고나 보고서가 자동으로 번역·AI 지침이 되지 않습니다. 영문 기준은 [README.md](README.md)입니다.
