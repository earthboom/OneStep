# OneStep

언리얼 엔진으로 게임 클라이언트를 개발하는 **vagabond**의 프로젝트입니다.

OneStep은 소프트웨어 개발, 소설, 발표자료, 기획서, 조사 등 다양한 결과물을 AI와 함께 완성하기 위한 에이전트 지침과 스킬 모음입니다. 저자의 배경이 지원 분야를 제한하지는 않습니다.

요청한 결과에 적합한 수행 방법을 연결하고 실제 산출물을 검증하며, 관련 지식과 수정 근거를 다음 작업에서 재사용합니다. AI 검증과 저자의 독립 검토는 별개 단계입니다.

## 작업 시작

이 저장소에서는 AI 에이전트에 공통 지침을 읽고 진입 스킬을 사용하도록 요청합니다.

```text
Read agents/vegabond-agent.md, then use
skills/vegabond-scout/SKILL.md to handle the following task:

[Describe the result you want, the relevant material, and any constraints.]
```

[에이전트 지침](agents/vegabond-agent.kr.md)은 공통 경계, 검증, 수용 기준을 정합니다. [vegabond-scout](skills/vegabond-scout/SKILL.kr.md)는 작업 특성을 파악하고 필요한 스킬과 검사를 연결합니다. 작업 스킬이나 전문 스킬을 직접 호출해도 같은 공통 설정을 재사용합니다.

위 경로는 이 저장소 기준입니다. 다른 작업 공간에서는 실제로 찾을 수 있는 지침 경로를 제공하거나 해당 환경이 지원하는 스킬 로딩 방식을 사용합니다. 이 저장소가 전역 설치나 자동 검색을 수행·보장하지는 않습니다. 스킬을 읽는 것이 에이전트 생성은 아니며, 사용 가능한 도구와 위임은 실행 환경과 허가에 따릅니다.

## 작업 흐름

1. **요청 파악.** 대상, 원하는 변화, 유지할 조건, 수행 방법을 파악하고 목표·범위·수용 조건을 짧은 작업 요약으로 밝힙니다.
2. **관련 맥락 검색.** 적용할 지식, 이전 수정 사례, 출처 참조, 공백을 요청하고 정보 요약이 유효한 동안 재사용합니다.
3. **작업 방식과 규모 선택.** 분야와 작업 크기와 별개로 create, revise, research를 선택하고 각 단계에 사용 가능한 스킬이나 도구와 검사를 연결합니다.
4. **실행과 검증.** 의존 작업 전에 필수 출처와 검사 도구를 사용할 수 있는지 확인하고, 관련 전문 스킬을 적용해 실제 산출물을 확인하며 수정 후 영향받는 검사를 반복합니다.
5. **발견에 대응.** 결함을 수정하거나 부족한 근거를 조사하거나 목표·범위가 바뀌면 작업 요약을 갱신합니다. 유용한 발견은 허가된 프로젝트 범위 안에 기록합니다.
6. **독립 검토를 위한 전달.** 산출물, 수용 조건별 근거, 한계를 보고합니다. vagabond가 별도로 테스트하거나 검토하고 명시적으로 확인하면 최종 수용이 성립합니다.

**single**은 한 번의 실행·검증 주기로 처리할 수 있는 작업의 기본값입니다. 의존 작업 전에 이름 붙일 수 있는 중간 결과를 검사해야 하면 **staged**를 사용합니다. 파일이나 도구가 여러 개라는 이유만으로 단계를 나누지 않습니다. 각 단계는 연결된 작업 스킬을 사용하고 최종 결과는 통합 검증합니다.

[작업 흐름도](docs/diagrams/onestep-workflow.png)에서 개요를 볼 수 있으며 [SVG 버전](docs/diagrams/onestep-workflow.svg)도 있습니다.

## 스킬

| 스킬 | 역할 |
| --- | --- |
| [vegabond-scout](skills/vegabond-scout/SKILL.kr.md) | 작업 특성, 작업 요약, 규모, 수행 능력 연결, 전체 조정. |
| [vegabond-create](skills/vegabond-create/SKILL.kr.md) | 제공된 자료에서 파생된 결과를 포함해 새로운 산출물이나 기능 생성. |
| [vegabond-revise](skills/vegabond-revise/SKILL.kr.md) | 유지해야 할 조건을 지키면서 기존 결과나 동작을 수정·개선. |
| [vegabond-research](skills/vegabond-research/SKILL.kr.md) | 조사 원본을 변경하지 않고 질문을 조사하고 대안 비교. |
| [vegabond-code](skills/vegabond-code/SKILL.kr.md) | 실제 프로그래밍 환경 파악, 소프트웨어 구현·검수·테스트·실행. |
| [vegabond-code-design](skills/vegabond-code-design/SKILL.kr.md) | 필요할 때 소프트웨어 구조, 소유권, 인터페이스, 검증 가능한 설계 결정. |
| [vegabond-fiction](skills/vegabond-fiction/SKILL.kr.md) | 작품 맥락과 문체 기준 검색, 집필·비평·수정·원고 검사. |
| [vegabond-fiction-design](skills/vegabond-fiction-design/SKILL.kr.md) | 필요할 때 스무 서사 요소를 범위가 명확한 선택, 의도한 효과, 검사에 연결. |
| [vegabond-presentation](skills/vegabond-presentation/SKILL.kr.md) | 발표 흐름 구성, 자료 제작, 주장 검증, 최종 내보낸 슬라이드의 시각 검토. |
| [vegabond-planning](skills/vegabond-planning/SKILL.kr.md) | 제안서, 실현 가능성, 의존성, 계산, 성공 지표의 작성·평가. |
| [vegabond-knowledge](skills/vegabond-knowledge/SKILL.kr.md) | 적용 범위가 있는 지식과 문제 기록의 검색·취합·저장·관리. |

작업 스킬은 흐름을 담당하고 전문 스킬은 그 안에서 수행 방법을 제공합니다. 기획 제안서 발표처럼 필요하면 기획과 발표자료 전문 스킬을 함께 사용합니다. 다른 분야도 요청마다 새 전문 스킬을 만들지 않고 적합한 스킬이나 직접 도구로 처리할 수 있습니다.

### 코딩

소스, 프로젝트 설정, 의존성, 스크립트, 테스트를 근거로 실제 변경하는 구성요소를 분류합니다. 언리얼 C++, 유니티 C#, 독립 C++, 엔진 저장소 안의 Python 도구는 서로 다른 실행 경로가 필요할 수 있습니다. 영향이 다른 환경으로 이어지면 통합 검사를 추가합니다.

Code는 중요한 구조 결정에 [code-design](skills/vegabond-code-design/SKILL.kr.md)을 호출하고 반환된 방향을 현재 작업 안에서 재사용합니다. 기존 방식을 따르는 작은 수정은 조건을 간단히 밝혀 진행할 수 있습니다. 설계만 요청했다면 설계에서 끝냅니다. [검증 참조](skills/vegabond-code/references/verification.kr.md)에 상세 소프트웨어 검사, 수정 규칙, 이어가기 상태를 두며 코드 변경이나 결과 판정 전에 읽습니다.

필요에 따라 빌드·준비, 자동 테스트, 실행 환경 준비, 실제 사용을 검증합니다. 게임 동작에는 관련 에디터와 실제 플레이가 필요하며 CLI는 실제 명령, 라이브러리는 사용 코드나 하네스로 확인합니다. 최종 통합 검증 전에 검수·수정을 반복합니다.

### 소설

기존의 권위 있는 자료에서 장면에 필요한 세계 규칙, 인물 상태, 관계, 시간선, 공개 범위를 가져옵니다. 확정 설정, 임시 계획, 소문, 미상을 구분합니다. 작가가 아는 정보가 인물이나 독자의 지식으로 조용히 넘어가지 않도록 합니다.

Fiction은 중요한 서사 선택에 [fiction-design](skills/vegabond-fiction-design/SKILL.kr.md)을 호출하고 결과를 현재 작업 안에서 재사용합니다. 설계는 이야기 논리, 인물, 서사 추진, 표현, 작품의 방향·결말에 걸친 스무 요소를 고려합니다. 국소 작업에는 관련 요소를 선택하며 장면마다 스무 장치를 강제하지 않습니다. 상세 판단, 문체, 수정, 반복 방지 절차는 [원고 검수](skills/vegabond-fiction/references/review.kr.md)에 둡니다. 설계만 요청하면 설계를 만들고, 의도한 독자 효과와 실제 독자 반응을 구분합니다.

작가가 쓰거나 선택한 문장으로 작품별 문체 기준을 정합니다. 인과, 개연성, 일관성, 독자의 이해, 문체, 언어를 검토합니다. 확정 오류, 미해결 가설, 편집 제안을 구분합니다. AI 같다는 느낌을 오류 종류로 삼거나 보편 금칙어 목록을 강제하는 대신 중복 설명, 인물 간 바꿔 써도 구별되지 않는 대사 같은 구체적인 문장 효과를 진단합니다.

재사용할 수정 전후 사례는 원문, 적용 조건, 재검증 근거, 실제 작가 피드백과 함께 저장합니다. 다음 집필에서는 관련 기준과 수정 검사를 가져오되 이전 표현을 복사하지 않습니다. AI의 편집 판단이 독자 합의나 작가 수용을 입증하지는 않습니다.

## 완료와 피드백

수용 조건에 검사와 현재 근거를 연결합니다. 필요한 검사를 실행할 수 없으면 **차단**이며 통과나 해당 없음이 아닙니다. 이후 수정이 영향을 주면 근거가 무효가 되므로 다시 확인합니다. 준비 단계나 모의 테스트의 성공이 실제 환경에서 최종 산출물이 동작함을 입증하지는 않습니다.

필요한 검사가 통과하면 **AI verification complete; awaiting vagabond testing or review**로 보고합니다. 명시적인 확인 후에만 **accepted by vagabond**로 보고합니다. 결함과 새로운 요청·선호 변경을 구분합니다. 같은 전제의 두 번 수정이 같은 검사에서 실패하면 다시 시도하기 전에 전제와 관찰 방법을 재평가합니다.

### 다른 프로젝트의 사용 후기

OneStep을 사용하는 프로젝트는 [피드백 안내](feedback/README.kr.md)와 [제출 양식](feedback/template.kr.md)을 통해 전략의 문제, 유용한 동작, 개선 제안을 남길 수 있습니다. 제출에는 알고 있는 OneStep 체크아웃과 허가된 접근이 필요하며, 자동 설치나 동기화가 아닙니다. 피드백은 판단할 때까지 임시 접수함에 둡니다. 개선을 적용하고 검증하며 필요한 사용자 확인도 마친 뒤에는 기존 테스트·지침·변경 보고서에 필요한 근거만 남기고 후기와 번역본을 삭제합니다. 일반 프로젝트 결함은 해당 프로젝트의 문제 기록에 둡니다.

## 지식과 문제 기록

- [knowledge/](knowledge/index.kr.md): 참조 자료, 관례, 수행 방법, 검증된 재사용 교훈.
- [records/](records/index.kr.md): 관찰한 문제, 원인 확신도, 수정, 재검증 근거.

두 저장소 모두 코드, 소설, 발표자료, 기획, 공통 분야 색인을 사용합니다. 전체 이력 대신 관련 카탈로그 행을 검색하고 일치하는 상세 문서를 읽습니다. 항목은 적용 범위, 맥락, 출처 근거, 예외를 유지합니다. 사건 해결과 예방 검증은 별개 상태이며 수정을 기록했다는 사실만으로 재발 방지를 입증하지는 않습니다.

저장소는 작업 프로젝트에 속합니다. 다른 프로젝트에서는 OneStep의 사실을 자동으로 가져오지 말고 해당 프로젝트의 저장소와 출처를 사용합니다. 적합하다면 기존 설정 문서나 원래 지식 체계를 재사용합니다. 테스트 자료는 실제 프로젝트 기록과 분리하고 일반 검색 때문에 빈 저장소를 만들거나 전체 재생성을 실행하지 않습니다.

[저장·수명주기 안내](skills/vegabond-knowledge/references/storage.kr.md)가 항목 형식, 중복 제거, 승격, 폐기의 기준입니다. [카탈로그 도우미](skills/vegabond-knowledge/scripts/catalog.py)는 실행 환경에 Python 3.9 이상과 PyYAML이 필요합니다.

허가된 갱신에서는 영문 상세와 사용자 번역본을 작성한 뒤 저장소 루트에서 영향받는 카탈로그를 생성합니다.

```text
python skills/vegabond-knowledge/scripts/catalog.py build --project . --domain fiction
```

`catalogs_written`에 나온 변경된 영문 카탈로그의 번역본을 다시 생성한 뒤 검사합니다.

```text
python skills/vegabond-knowledge/scripts/catalog.py check --project . --domain fiction --strict
```

`fiction`은 영향받는 분야로 바꿉니다. 다른 프로젝트에서는 도우미의 절대 경로를 사용하고 `--project`를 해당 프로젝트로 지정합니다. 최초 생성은 색인 빈 파일 없이 예정된 카탈로그를 만들 수 있습니다. 도우미는 기준 상세 문서나 번역본을 쓰지 않으며 구조 검사는 사실 정확성, 번역 품질, 문학적 품질을 입증하지 않습니다.

## 저장소 구성

```text
agents/                  공통 에이전트 지침
skills/                  진입·작업·전문·지식 스킬
knowledge/               분야별 참조와 재사용 지식
records/                 실제 발견과 수정 근거
feedback/                임시 전략 후기, 안내, 양식
docs/designs/            저장 구조 설계 문서
docs/diagrams/           작업 흐름 개요 이미지
README.md                영문 프로젝트 개요
README.kr.md             사용자용 한국어 번역
```

카탈로그 도우미의 자동 테스트는 [skills/vegabond-knowledge/tests/](skills/vegabond-knowledge/tests/test_catalog.py)에 있습니다.

```text
python -m unittest discover -s skills/vegabond-knowledge/tests -v
```

테스트는 분리된 임시 자료를 만듭니다. 위치를 선택하려면 `ONESTEP_TEST_ROOT`를 이미 존재하는 쓰기 가능한 폴더로 지정합니다. 이 테스트는 카탈로그 동작을 다루며 실제 작업 흐름 실험이나 분야별 실행·검토를 대체하지 않습니다.

## 문서 언어

유지관리하는 프로젝트 안내, 에이전트·스킬 지침, 저장소 문서는 영문으로 작성합니다. 별도 `<stem>.kr.md` 번역본은 사람만 읽습니다. AI는 읽기, 검색, 색인, 위임 작업에서 번역본 내용을 제외하고 영문 원본에서 생성하되 번역본을 다시 읽지 않습니다.

작업 입력과 산출물은 사용자가 요청한 언어를 따릅니다. 한국어 원고나 보고서 원본이 자동으로 번역본이나 AI 지침 문서가 되지는 않습니다.

사람은 [README.kr.md](README.kr.md)를 읽을 수 있습니다. AI 에이전트는 이 번역본 링크를 따라가지 않습니다.
