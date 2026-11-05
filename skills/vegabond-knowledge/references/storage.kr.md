# 저장과 수명주기

사람용 번역본입니다. AI는 읽거나 검색하지 않습니다. 영문 storage.md가 기준입니다.

## 위치와 분야

작업 프로젝트의 기존 시스템이 범위별 검색·출처 추적에 적합하면 재사용합니다. 없으면 다음 구조를 씁니다.

```text
knowledge/index.md             # 분야 경로
knowledge/<domain>/index.md    # 검색용 지식 요약
knowledge/<domain>/<id>.md     # 재사용 주제·교훈 하나
records/index.md               # 분야 경로
records/<domain>/index.md      # 검색용 문제 요약
records/<domain>/<id>.md        # 문제·수정·재검증 이력
```

초기 code·fiction·presentation·planning·shared는 전체 목록이 아닙니다. 작업 동작·확장자가 아닌 대상 분야로 분류하고 실제 내용이 필요할 때 분야를 추가합니다. 언어·엔진·장르·형식·컴포넌트·작품 ID·세부 작업은 폴더보다 먼저 메타데이터에 담습니다.

복합 분야는 기본 위치 하나에 두고 다른 색인에서 연결합니다. shared는 근거가 있는 공통 적용에만 씁니다. 사건·설정은 해당 프로젝트에 유지하고 일반 방법의 공유 승격도 근거가 범위를 뒷받침할 때만 합니다. lessons/와 knowledge/를 병렬로 만들지 않습니다. 기존 시스템은 재사용하거나 허용 범위에서 ID·근거를 유지하며 이관합니다.

색인·상세·보관 문서까지 새·변경 영문마다 <stem>.kr.md 번역을 영문에서 생성합니다. 번역은 다시 읽지 않으며 기록도 예외가 아닙니다. 전달 전 영문 링크·상태와 번역 존재를 확인하되 번역 내용은 불러오지 않습니다.

## 공통 헤더와 본문

독립적으로 재사용할 주제·점검 하나를 상세 하나로 작성합니다.

| 필드 | 규칙 |
| --- | --- |
| id | 프로젝트 고유의 안정된 ID. 영문자·숫자·점·밑줄·하이픈. 대소문자 구분 없이 비교합니다. |
| title | 구체적인 질문·방법·대상. |
| summary | 활용할 내용과 핵심 조건을 한두 문장으로 표현합니다. |
| kind | 지식: reference·method·convention·lesson. 기록: error·suggestion·hypothesis. |
| scope | 프로젝트·컴포넌트·작품과 적용 경계의 문자열. |
| keywords | 영문 개념·동의어·정확한 식별자의 비어 있지 않은 목록. |
| status | 지식: active·enforced·superseded. 기록: open·resolved·superseded. |
| checked_at | 실제 근거 확인일 YYYY-MM-DD 또는 null. 편집일로 자동 입력하지 않습니다. |

선택 context는 문자열 또는 문자열 값만 갖는 평면 사전입니다. 필요한 버전·엔진·형식·장르·시점 등을 담고 버전·YAML 예약어에 따옴표를 씁니다. 무관한 빈 필드는 만들지 않습니다. 헤더는 데이터이며 스킬 발견용이 아닙니다. 번역도 발견 입력으로 삼지 않습니다.

다음은 형식 예시이며 실제 항목이 아닙니다.

```yaml
---
id: K-FIC-001
title: Check information access in limited viewpoint
summary: Under limited narration, check each claim against the focal character's information access before line polishing.
kind: method
scope: naru-novel; Seorin-limited narration
keywords: [viewpoint, POV, character-knowledge]
status: active
checked_at: null
context:
  viewpoint: third-person limited
---
```

내용이 있는 H2 구획 네 개를 사용합니다.

- 지식: Guidance(지침), Applicability and exceptions(조건·예외), Checks(점검), Evidence(근거).
- 기록: Expected and observed(기대·관찰), Cause and resolution(원인·해결), Recheck and prevention(재검증·예방), Evidence(근거).

행동을 짧게 쓰고 예외를 설명합니다. 사실·방법·관례·편집 판단을 구분하고 원본 위치·검증 맥락을 인용합니다. 기록은 원인 확신·수정 또는 제안·해결·재검증·예방 연결을 남기며 모르는 원인은 그대로 둡니다. enforced는 입증된 방지 장치가 필요합니다. 원래 이슈·보고서·테스트·문장·이미지·로그를 복사하지 않고 참조합니다. 같은 원인의 작은 발견은 묶을 수 있습니다. 프로젝트 원본은 사실, 상세는 메타데이터의 기준이며 색인은 파생 결과입니다.

### 문제 검색용 필드

새·정규화 records/ 상세에는 다섯 필드 모두 필요하며 knowledge/에는 추가 요구하지 않습니다.

| 필드 | 규칙 |
| --- | --- |
| trigger | 짧은 발생 조건·작업 또는 미확인 시 null. 증상 발생 전 검색용입니다. |
| symptom | 관찰 현상과 구별되는 특징의 비어 있지 않은 설명. 제안·가설은 미확인 결함을 단정하지 않습니다. |
| cause_status | unknown·suspected·confirmed. 원인·해결 구획이 뒷받침합니다. 결함이 확실해도 원인은 모를 수 있습니다. |
| prevention | 핵심 조건을 포함한 행동·점검 또는 미수립 시 null. 상세 절차·예외·근거는 본문에 둡니다. |
| prevention_status | none·proposed·verified·invalidated. none은 null 예방책을 요구하고 나머지는 행동이 필요합니다. verified는 실제 checked_at과 본문 근거도 필요합니다. |

색인에 유용하도록 짧게 쓰고 로그·모든 예시를 반복하지 않습니다. keywords는 동의어·식별자를 담고 summary는 발견과 핵심 조건을 요약합니다. 버전·설정·형식 차이는 범위·맥락에 명시합니다.

다음은 기록 형식 예시이며 실제 사건이 아닙니다.

```yaml
---
id: R-FIC-EXAMPLE
title: Inaccessible private decision in limited narration
summary: A focal character asserted a private decision without an information source; revision restored uncertainty.
kind: error
scope: story-alpha; chapter-3
keywords: [viewpoint, POV, information-access, private-thought]
status: resolved
checked_at: null
context:
  canon: revision-B
trigger: Drafting third-person limited narration
symptom: Focal character states another character's private decision without access
cause_status: confirmed
prevention: Trace each private-knowledge assertion to a source available to the focal character
prevention_status: proposed
---
```

resolved는 사건 해결이지 예방 상태가 아닙니다. 명시한 점검이 원래 실패나 통제된 동등 사례를 해당 맥락에서 실제 탐지했을 때만 verified입니다. 결과물을 고친 사실만으로 부족합니다. 편집에서도 결함을 탐지한 문서화된 검수는 근거가 되지만 자동 강제로 표현하지 않습니다. 수정 확인과 예방 확인의 날짜·결과를 본문에서 나눕니다. checked_at은 최근 실제 중요 근거 확인일이며 예방 날짜를 꾸미지 않습니다. 헤더·날짜만으로 입증하지 못하므로 전문 스킬이 근거를 확인합니다.

네 본문 구획을 유지합니다. 기대·관찰에는 계약·발견·조건·위치, 원인·해결에는 확신·근거·수정·미확인을 적습니다. 재검증·예방은 수정 결과와 향후 예방을 나누어 상태·조건·예외를 남기고 근거는 원본 결과물·버전·보고서에 연결합니다. 제안·가설은 기록했다고 오류로 바뀌지 않습니다.

### 이전 구조 기록

다섯 필드가 모두 없는 공통 헤더 기록도 읽을 수 있습니다. legacy_record_fields 경고를 내고 원본을 보존하며 새 정보는 unrecorded로 표시합니다. --strict에서는 오류입니다. 일부만 추가하면 기존 형식 예외가 아닌 오류입니다. 새·수정 기록에는 모두 필요하지만 도구가 편집 이력을 알 수 없으므로 작성 절차도 지켜야 합니다. 허용 유지 관리에서만 ID·경로·근거·미확인을 보존하며 정규화하고 제목·과거 색인으로 추정하지 않습니다.

## 색인 생성과 검사

[catalog.py](../scripts/catalog.py)는 기존 Python 3.9 이상과 PyYAML을 쓰며 설치하지 않습니다. 다음은 OneStep 폴더 기준이며 다른 프로젝트는 도구 절대 경로와 해당 --project를 씁니다.

```text
python skills/vegabond-knowledge/scripts/catalog.py build --project . --domain fiction
python skills/vegabond-knowledge/scripts/catalog.py check --project . --domain fiction
```

--store knowledge·records 또는 기본 both로 선택하고 영향 분야마다 --domain을 반복합니다. 분야 생략은 전체 ID 중복을 포함한 명시적 전체 유지 관리입니다. 분야 지정은 선택 상세·명시적 관련 참조만 검사합니다. 일반 검색은 제한된 행을 찾으며 매번 재생성하지 않습니다.

관리 표식 안에 식별, 요약, 범위·맥락, 검색어, 상태·확인일, 상세의 여섯 열을 생성합니다. 기록의 요약은 조건·증상, 상태는 원인 확신·예방 상태·행동도 표시합니다. 지식 행은 그대로이며 해결 사건도 현재 색인에서 찾고 superseded만 보관합니다. 표식 밖 메모와 단일 기본 상세를 보존하며 루트는 작은 분야 경로입니다.

상세·번역 작성 → build → catalogs_written에 있는 영문 색인들의 번역 생성 → check 순서입니다. build는 준비라 번역·경로 누락을 경고로 처리합니다. check는 최신 색인·메타데이터·상태·ID 고유성·본문 구획·로컬 파일 참조·경로·번역 존재를 요구합니다. YAML 중복 키·잘못된 헤더는 오류이며 메타데이터·참조 오류는 쓰기를 막습니다. 파일별 원자 교체지만 파일 시스템 실패로 일부만 바뀔 수 있어 검사·복구합니다. 도구는 상세·번역을 쓰지 않습니다.

외부 링크·구획 앵커 정확성은 별도 확인합니다. 참조 내용을 읽지 않고 로컬 파일 대상만 확인합니다. 번역은 의미·최신성이 아닌 존재만 확인하며 영문에서 생성하고 다시 열지 않습니다. 진단은 처음 20개와 전체·오류 수로 제한하므로 많으면 분야를 좁힙니다.

산문형 기존 행·조건은 미확인 Legacy entries에 보존하고 색인 밖 파일은 미확인 링크로 표시합니다. ID·날짜·규칙·상태를 추정하지 않습니다. 허용 유지 관리에서 경로·ID·근거를 보존하며 이관합니다. 기본 경고이며 정규화 범위는 --strict로 오류 처리합니다. 주변이 과거 형식이어도 새·수정 항목은 새 헤더를 씁니다. 엄격 검사는 무관한 파일·역사 근거를 다시 쓸 권한이 아닙니다.

## 수집·통합·승격

쓰기 전 같은 주제·원인을 찾아 중복 대신 기존 항목에 조건·근거·재발을 더합니다. 원인·조건이 같은 예방책을 뒷받침할 때만 합칩니다. 증상만 같으면 부족하며 불확실한 사례는 연결합니다. 중요한 이견과 문제·예방·교훈·원래 근거의 연결을 유지하고 최신이라는 이유로 덮어쓰지 않습니다.

재발은 날짜 또는 미확인, 위치·버전, 근거 링크, 수정·재검증 결과, 기존 예방 결과를 짧게 남깁니다. 실행 누락·실행했으나 부족·조건 변화로 무효를 구분하며 모르면 그대로 둡니다. 반대 근거가 예방 주장을 무효화하면 invalidated로 표시하고 과거 맥락을 남긴 채 대체안을 조사합니다. 누락했다고 점검 자체가 틀린 것은 아닙니다. 다른 해결이 필요한 조건은 별도 사건이며 긴 로그는 원본에 둡니다.

재발·재사용 가능성·유용한 방지 장치가 정당화할 때만 확인된 중요한 교훈을 승격합니다. 사건은 records/, 정제 내용은 knowledge/에 두고 복사 대신 양방향 연결합니다. 진단·분야 점검은 전문 스킬이 제공하고 이 스킬은 정리하며 원인을 꾸미거나 인증하지 않습니다. 구조·타입·검증·린트·회귀 점검을 우선하고 원래 실패·동등 사례 탐지 근거를 보존합니다. 판단 작업은 구체적인 조건부 검수·이유를 남깁니다. 저장은 예방 입증이 아닙니다.

## 출처를 보존하며 폐기

중복·낡은 조건을 정리합니다. 대체하려면 원본 status와 이유·대체 대상을 기록하고 재생성하면 필요 시 만드는 archive.md로 이동합니다. 재활성화하면 현재 색인으로 돌아옵니다. 상세 경로·근거는 유지하고 생성 행은 수동 편집하지 않습니다. 기존 시스템은 자체 방식을 사용하며 나이만으로 유용한 지식을 폐기하지 않습니다.

출처·버전·설정·예방 장치가 바뀌면 관련 항목·무효화된 요약을 갱신합니다. 무관한 검색 결과가 반복해 많으면 실제 영역별로 해당 색인을 나누고 작은 경로를 유지합니다. 실제 불편이 있을 때만 확장하며 무관한 작업 후 전체 이력을 다시 읽지 않습니다.

## 첫 색인 생성

새 저장소·분야에서는 분야 폴더에 올바른 상세 문서와 사람용 번역을 작성하고, 루트 경로 문서와 그 번역을 생성·갱신합니다. 루트 링크는 이번 build가 만들 분야 색인을 미리 가리킬 수 있습니다. 빈 색인 파일이나 별도 초기화 명령은 필요하지 않습니다. 기존 build → 변경 색인 번역 → check 순서로 진행합니다. 도구는 선택된 모든 색인의 생성 계획을 정한 뒤 로컬 파일 존재를 검사하며, 실제 이번 계획에 들어 있는 미생성 색인만 허용합니다. 다른 누락 파일과 선택되지 않은 미생성 색인은 계속 쓰기를 차단합니다. check는 첫 실행에서도 색인의 존재를 요구하며 파일을 생성·수정하지 않습니다.
