# 저장과 수명 관리

## 위치와 분야

경로는 작업 프로젝트 기준입니다. 범위별 검색과 출처 추적이 가능한 기존 체계가 있으면 재사용하고, 없으면 다음 구조를 사용합니다.

```text
knowledge/index.md              # 분야 안내만
knowledge/<domain>/index.md     # 검색 가능한 지식 요약
knowledge/<domain>/<id>.md      # 재사용할 주제·점검 하나
records/index.md                # 분야 안내만
records/<domain>/index.md       # 검색 가능한 문제 요약
records/<domain>/<id>.md        # 문제·수정·재점검 이력
```

초기 분야는 code, fiction, presentation, planning, shared이며 완결된 목록이 아닙니다. 작업 방식·확장자보다 주제로 분류하고 실제 필요에 따라 추가합니다. 언어·엔진·장르·형식·구성요소·작품·작업 유형은 깊은 폴더 전에 메타데이터로 표현합니다.

여러 분야의 자료는 주 저장 위치 하나와 관련 색인 링크를 사용합니다. shared는 분야 간 적용 근거가 있을 때만 쓰고 잡동사니 저장소로 쓰지 않습니다. 프로젝트 사건과 설정은 해당 프로젝트에 두며 일반 방법의 공유 승격에는 그 범위의 근거가 필요합니다. lessons와 knowledge를 병행하지 말고 기존 교훈 체계를 재사용하거나 허용된 범위에서 ID·근거를 보존하여 이전합니다.

색인·지식·문제·보관 문서를 새로 쓰거나 바꾸면 영문에서 사용자 번역본을 작성·갱신하고 기존 번역 내용은 읽지 않습니다. 기록도 같은 규칙을 따릅니다. 인계 전 영문 링크·상태와 번역 쌍 존재를 확인하되 번역 내용은 열람하지 않습니다.

## 항목 헤더와 본문

독립적으로 재사용할 주제·점검 하나를 상세 문서 하나로 작성하고 YAML 헤더를 둡니다.

| 필드 | 규칙 |
| --- | --- |
| id | 프로젝트 고유의 안정적인 ID. 영문자·숫자·점·밑줄·하이픈. 비교는 대소문자를 구분하지 않음. |
| title | 구체적인 질문·방법·주제. |
| summary | 활용할 요점과 필수 조건을 한두 문장으로 표현. |
| kind | 지식: reference, method, convention, lesson. 기록: error, suggestion, hypothesis. |
| scope | 프로젝트·구성요소·작품과 적용 경계를 문자열로 표현. |
| keywords | 유용한 영문 개념·동의어·정확한 기술 식별자의 비어 있지 않은 목록. |
| status | 지식: active, enforced, superseded. 기록: open, resolved, superseded. |
| checked_at | 실제 근거 확인일 YYYY-MM-DD 또는 미확인 null. 수정 날짜로 자동 채우지 않음. |

선택 context는 버전·엔진·형식·장르·시점 등의 조건을 문자열 또는 문자열 값의 평평한 매핑으로 표현합니다. 버전·예약어는 따옴표로 감싸고 무관한 빈 필드는 두지 않습니다. 헤더는 스킬 검색 메타데이터가 아니며 번역본에 검색용 프런트매터를 복제하지 않습니다.

선택 relations는 requires, derived_from, prevention, supersedes, conflicts_with를 기존 항목 ID의 비어 있지 않은 목록에 연결하며 다른 저장소·분야도 가능합니다. 실제 검색에 도움이 될 때만 추가하고 [관계 의미와 탐색](retrieval.md#follow-meaningful-relationships)을 따릅니다. 도구는 형식·대상 ID만 검증합니다. 간선은 인과·독립 근거·호환·예방 검증을 입증하지 않습니다. 본문 근거 링크와 과거 날짜를 보존하고 관계 추가를 새 출처 조사로 취급하지 않습니다.

형식 예시이며 실제 항목이 아닙니다.

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

본문 H2 네 개를 비어 있지 않게 둡니다. 지식은 Guidance, Applicability and exceptions, Checks, Evidence이며 기록은 Expected and observed, Cause and resolution, Recheck and prevention, Evidence입니다.

유용한 행동은 짧게 쓰고 예외를 설명합니다. 출처 사실·방법·관례·편집 판단을 구분하고 위치·검증 맥락을 포함해 원본을 인용합니다. 문제에는 원인 확신도, 수정·제안, 해결·재점검 근거와 예방 연결을 남깁니다. 모르는 원인은 모르는 상태로 둡니다. enforced에는 입증된 방지책이 필요하며 교훈 저장만으로 강제가 입증되지는 않습니다.

원래 문제·보고서·테스트·문단·화면·로그는 복제하지 말고 참조합니다. 사소한 동일 원인 발견은 필요에 따라 묶습니다. 사실의 권위는 프로젝트 원본, 항목 메타데이터는 상세 문서가 소유하며 카탈로그는 생성된 표현입니다.

### 문제 검색 필드

새로 쓰거나 정규화한 records에는 다섯 필드를 모두 사용합니다. knowledge의 추가 요건은 아닙니다.

| 필드 | 규칙 |
| --- | --- |
| trigger | 발생 조건·행동. 미확인은 null. 증상이 생기기 전 검색에 사용. |
| symptom | 구별 가능한 관찰 증상을 비어 있지 않게 표현. 제안·가설은 미확인 결함을 단정하지 않음. |
| cause_status | unknown, suspected, confirmed. 본문에서 근거 제시. 확인된 결함도 원인은 모를 수 있음. |
| prevention | 필수 조건이 있는 구체적 행동·점검 또는 미확립 null. 상세 단계·예외·근거는 본문에 둠. |
| prevention_status | none, proposed, verified, invalidated. none은 null prevention, 다른 상태는 행동 필요. verified는 실제 checked_at과 본문 입증도 필요. |

검색 행으로 유용하도록 짧게 쓰고 로그·모든 예시를 반복하지 않습니다. keywords는 동의어·식별자에 쓰며 문구 전체를 복제하지 않습니다. summary는 발견과 필수 조건을 요약하고 적용을 바꾸는 버전·설정·형식 차이는 scope/context에 둡니다.

기록 형식 예시이며 실제 사건이 아닙니다.

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

resolved는 사건이지 예방 상태가 아닙니다. 정해진 조건에서 점검이 원래 실패나 통제된 동등 사례를 탐지한 뒤에만 verified로 둡니다. 수정 결과물만으로는 부족합니다. 편집은 자동 강제로 가장하지 않으면서 결함을 탐지한 문서화된 검수를 근거로 사용할 수 있습니다. 수정·방지책 확인 날짜·결과는 본문에 따로 남깁니다. checked_at은 최근 실제 중요한 근거 확인일이며 지어낸 예방 날짜가 아닙니다. 헤더·날짜만으로 실증이 입증되지 않으므로 전문 스킬이 근거를 확인합니다.

기대·관찰 절에는 원래 규약·실제 발견·조건·위치, 원인·해결 절에는 확신도·근거·수정·미확인점, 재점검·예방 절에는 수정 결과와 미래 방지책의 상태·적용·예외를 분리하여 둡니다. 근거 절은 원래 결과물·버전·보고서를 연결합니다. 제안·가설은 기록했다는 이유로 오류가 되지 않습니다.

### 기존 구조화 기록

공통 헤더만 있는 기록은 계속 읽을 수 있습니다. 도구는 legacy_record_fields 경고를 내며 원본을 바꾸지 않고 새 정보는 unrecorded로 표시합니다. strict는 이전 공백을 오류로 취급합니다. 일부 필드만 추가한 것은 기존 형식 예외가 아닙니다. 새로 쓰거나 수정하는 기록은 다섯 필드를 모두 써야 합니다. 도구가 편집 이력을 알 수 없으므로 스킬에도 규칙이 필요합니다. 정규화는 허용된 유지관리에서만 하고 ID·경로·근거·미확인점을 보존합니다. 제목·이전 행에서 값을 추정하지 않습니다.

## 카탈로그 갱신과 검증

[catalog.py](../scripts/catalog.py)는 Python 3.9+와 기존 런타임의 PyYAML을 쓰며 설치하지 않습니다. OneStep 체크아웃에서 다음과 같이 실행합니다. 다른 작업 프로젝트는 도구 절대경로와 해당 project 값을 사용합니다.

```text
python skills/vegabond-knowledge/scripts/catalog.py build --project . --domain fiction
python skills/vegabond-knowledge/scripts/catalog.py check --project . --domain fiction
```

store는 knowledge, records 또는 기본 both이고 domain은 반복합니다. 분야 생략은 프로젝트 전체 중복 ID 검사까지 포함한 명시적 유지관리입니다. 범위 지정은 선택 문서·명시적 관련 항목만 확인합니다. 일반 조회에서는 전체 재생성하지 않습니다.

도구는 관리 표식 안에 ID/제목/종류, 요약, 범위/맥락, 검색어, 상태/확인일, 상세의 여섯 열을 생성합니다. 문제는 요약에 조건·증상, 상태에 원인 확신도·예방 상태·짧은 행동도 표시하며 지식 행은 유지합니다. 해결 사건은 검색 가능하게 두고 superseded만 보관합니다. 표식 밖 메모를 보존하고 관련 분야는 주 문서 하나를 연결합니다. 루트는 분야 변경 시 이 스킬이 관리하는 작은 안내로 유지합니다.

상세·번역 작성 → build → catalogs_written에 나온 카탈로그 번역 재작성 → check 순서입니다. 준비 단계 build는 번역·안내 누락을 경고로 두어 영문을 먼저 만듭니다. check는 최신성, 메타데이터·상태, 고유 ID, 필수 절, 참조, 안내·번역 쌍을 확인합니다. 중복 YAML 키·잘못된 헤더는 오류입니다. 메타데이터·참조 오류는 쓰기 전에 중단하고 파일별 원자 교체를 사용합니다. 파일 시스템 오류로 일부만 갱신될 수 있으므로 허용 범위에서 재검사·수정합니다. 도구는 상세·번역을 쓰지 않습니다.

프로젝트 밖 링크·일반 절 앵커는 별도 확인합니다. 카탈로그는 명시적 관련 기준 항목·내부 출처 메타데이터를 읽고 다른 로컬 대상은 내용 없이 존재만 확인합니다. 번역 의미·최신성은 확인하지 않습니다. 영문에서 번역하고 다시 열지 않습니다. 진단은 앞 20개와 전체·오류 수를 출력하므로 큰 결과는 분야를 좁힙니다.

### 위치와 분리한 출처 참조

[출처 목록](../../../knowledge/sources.md)은 과거 식별 정보와 위치를 구분합니다. sources는 SRC-... ID마다 project, path, sha256만 둡니다. 해시는 기존 소문자 값 또는 null입니다. OneStep에서는 project와 path를 모두 null로 두고 다른 프로젝트의 실제 위치·연결을 추가하지 않습니다. 실제 소비 프로젝트에서 명시적으로 허용된 경우에만 소문자 프로젝트 ID와 슬래시를 쓰는 내부 상대경로를 연결합니다. 둘은 함께 지정하거나 함께 null이어야 합니다. ID마다 H2를 두어 일반 링크로 연결하고 문단·절 위치·근거 맥락은 참조 항목에 유지합니다. 알려진 해시는 보존하며 누락 버전·과거 확인일을 추정하거나 현재 원고로 과거를 인증하지 않습니다.

해시가 기록된 ID는 그 내용 시점을 식별합니다. 다른 근거 버전은 새 ID를 사용하여 과거 인용을 바꾸지 않습니다. 같은 내용의 이동은 가능하면 로컬 루트만 바꿉니다.

실제 소비 프로젝트의 영구 루트는 그 프로젝트의 Git 제외 knowledge/sources.local.json에만 둡니다. 허용된 임시 루트는 --root project=absolute-path로 주며 이번 호출에서 영구 매핑보다 우선하고 파일을 쓰지 않습니다. 기본 프로젝트 ID·위치는 없습니다. 루트가 필요하면 사용자 확인 경로나 알려진 메타데이터를 먼저 재사용합니다. OneStep에 연결을 만들거나 로컬 설정을 커밋하거나 루트를 지어내거나 무관한 프로젝트를 찾거나 원본 전체를 복제하지 않습니다. 소비 프로젝트는 자체 영구 설정을 Git에서 제외합니다.

주장에 필요한 ID만 [출처 도구](../scripts/sources.py)로 해석합니다.

```text
python <source-helper-path> resolve --project <working-project> --id <registered-source-ID>
python <source-helper-path> resolve --project <working-project> --id <source-ID-1> --id <source-ID-2> --root <project-ID>=<authorized-absolute-path>
```

선택한 원본을 바이트로 읽어 해시를 비교하므로 허용된 범위에서만 실행합니다. 내용 출력·번역 읽기·설정과 항목 쓰기·관찰 해시 자동 승격은 하지 않습니다. 루트 밖 경로 이탈을 거부합니다. 해시 일치는 내용 동일성만 보여 주며 사실·적용·출처 품질·작가 수락은 입증하지 않습니다. 필요한 원본 절도 확인합니다.

id를 반복하여 여러 출처를 확인할 수 있습니다. 단일 형식은 유지하고 일괄 결과는 requested_ids, completed와 입력 순서의 results를 반환합니다. 잘못된·접근 불가 ID도 빠뜨리지 않습니다. 입력 ID·개수와 결과를 대조합니다. 대소문자만 다른 중복 ID나 같은 프로젝트의 중복 루트는 오류이며 root 반복은 서로 다른 프로젝트에만 씁니다.

모두 matched면 코드 0, 하나라도 unbound·unconfigured·missing·unavailable·mismatch·unversioned면 1, 잘못된 목록·ID·설정·경로는 2입니다. 정상 목록의 잘못된 ID 하나는 다른 결과를 없애지 않지만 잘못된 공유 입력은 해석을 막습니다. unbound는 이력만 있는 상태로 기기 설정을 읽거나 외부 프로젝트를 찾기 전에 반환하며 설정 요청이 아닙니다. access_status와 identity_status를 구분합니다. available은 바이트를 읽었다는 뜻이고 unversioned는 기대 해시가 없다는 뜻입니다. 불일치·해시 미기록 파일도 현재 읽기는 가능하나 과거 동일성을 인증하지 못합니다. 정보 요약에 한계를 유지하고 필요한 원본 문제는 종속 점검만 차단하며 독립 작업은 계속합니다. 조회 중 과거 null 해시·날짜를 바꾸지 않고 기기 상태를 사건 해결·예방 상태와 섞지 않습니다.

카탈로그는 ID·번역 존재를 확인하고 이력에는 source_unbound, 별도 확인이 필요한 연결에는 source_unverified를 냅니다. 설정·원문은 읽지 않으며 등록만으로 검증되지 않습니다. 미등록 ID·잘못된 목록은 쓰기를 막습니다. 조회는 필요한 ID만 해석합니다. 목록·번역을 함께 갱신하되 번역은 다시 읽지 않습니다. 다른 외부 참조는 기존 경고를 유지합니다.

기존 산문은 계속 사용합니다. 기존 행·조건은 미검증 Legacy entries에 보존하고 색인 없는 파일에는 메타데이터 미확인 안내를 둡니다. ID·날짜·규칙·상태를 추론하지 않습니다. 허용된 유지관리에서 경로·ID·근거를 보존하여 이전·재생성합니다. 기본 실행은 경고, strict는 이미 정규화한 범위의 기존 자료를 오류로 봅니다. 주변이 기존 형식이어도 새로 쓰거나 바꾸는 항목은 헤더를 씁니다. strict는 무관한 이력까지 다시 쓸 권한이 아닙니다.

## 저장·통합·승격

저장 전에 [검색 절차](retrieval.md)로 두 저장소에서 질문·별칭·원인을 조회하고 가까운 후보와 관계를 확인하여 갱신·별도 사건·새 지식을 결정합니다. 유사성은 후보 제안이며 자동 통합 권한이 아닙니다.

미래의 어떤 결정·행동·점검과 조건을 돕는지 정합니다. 재사용은 같은 조건의 다른 작업에 유용하다는 뜻이며 보편성을 뜻하지 않습니다. 가장 작은 목적지를 고릅니다.

- 지식: 원리·방법·이유·점검·예외를 두고 제목·요약은 연대기보다 재사용 질문·행동으로 씁니다.
- 문제: 조건·증상·원인 확신도·수정·재점검을 구별할 최소 근거를 두고 공통 절차는 연결합니다.
- 원본·작업 이력: 고유 사실·설정·작가 취향·일회성 진행은 원래 권위에 둡니다. 반복 조회에 이득이 있을 때만 전체 명세 복제 없이 범위별 참고·관례를 추가합니다. 재사용·추적 가치가 없으면 작업 보고에 두되 후속 추적이 필요한 문제는 기록합니다.

같은 원리·질문·원인을 먼저 검색하고 복제보다 기존 조건·예외·근거·재발을 갱신합니다. 지식 하나에서 여러 사건을 연결할 수 있습니다. 원인·조건이 같은 예방을 뒷받침할 때만 합칩니다. 같은 증상만으로 합치지 않고 불확실한 일치는 연결합니다. 중요한 불일치를 유지하고 최신이라는 이유로 덮어쓰지 않습니다. 문제에서 예방, 교훈에서 원래 근거로 연결을 보존합니다.

일반화해도 근거 경계는 유지합니다. 버전·수명·장르·시점·독자 조건은 기존 scope/context·본문·출처에 둡니다. 재현·검색 식별자를 보존하고 부수적 이름·긴 로그는 제외합니다. 실제 확인과 넓은 적용 추론을 구분하고 미검증 범위를 명시합니다. 한 성공으로 다른 환경을 검증했다고 주장하지 않습니다. 설정·취향을 보편화하거나 문구 일반화만으로 제안 예방을 승격하지 않습니다. 일반화가 프로젝트 간 이동 권한이나 shared 분류를 주지 않습니다. 기존 스키마·저장소를 씁니다.

재발 이력은 날짜 또는 미확인, 위치·버전, 근거 링크, 수정·재점검과 기존 방지책 결과로 짧게 유지합니다. 미실행·실행했지만 불충분·조건 변화 무효화를 구분하고 모르는 결과를 지어내지 않습니다. 반대 근거가 예방 주장을 무효화하면 invalidated로 두고 이전 입증 맥락을 보존하며 대안을 조사합니다. 누락만으로 점검이 반증되지는 않습니다. 조건·해결이 다르면 별도 사건을 두고 긴 로그는 원래 위치에 둡니다.

확인되고 중요한 교훈만 반복·예상 재사용·유용한 방지책 필요에 따라 승격합니다. 사건은 records, 정제된 내용은 knowledge에 상호 연결하고 서술을 복제하지 않습니다. 전문 스킬이 진단·분야 점검을 제공하고 지식 스킬은 정리하며 원인·결과를 임의 인증하지 않습니다. 구조·타입·검증·린트·회귀 점검을 우선하고 원래 실패나 통제된 동등 사례 탐지 근거를 보존합니다. 판단 작업은 구체적 조건부 검수와 이유를 남깁니다. 저장만으로 예방이 입증되지 않습니다.

## 출처를 보존하는 퇴역

일상 사용 중 중복·낡은 조건을 고칩니다. 대체 항목은 상태·이유·대안을 기록하고 재생성하면 필요할 때만 archive.md를 만들어 행을 옮깁니다. 재활성화하면 돌아옵니다. 상세 경로·근거를 안정적으로 유지하고 생성 행을 직접 편집하지 않습니다. 기존 체계는 자체 방식을 사용하며 오래되었다는 이유로 지식을 무효화하지 않습니다.

원본·버전·설정·방지책 변경 시 영향 항목을 재확인하고 무효화된 요약을 갱신합니다. 제한 검색에서 무관한 결과가 반복되면 실제 영역별로 나누고 작은 안내를 유지합니다. 관찰된 불편에 따라 확장하며 작업마다 전체 이력을 읽지 않습니다.

## 첫 카탈로그 생성

새 저장소·분야에는 유효한 상세·번역본을 쓰고 루트 안내·번역을 갱신합니다. 이번 build가 만들 카탈로그를 미리 링크해도 되며 빈 색인·특별 초기화는 필요하지 않습니다. 일반 build·번역·check 순서를 따릅니다. 모든 계획 후 존재를 검사하여 계획에 속한 누락 카탈로그만 허용합니다. 다른 누락 파일·선택하지 않은 카탈로그는 쓰기를 막습니다. check는 읽기 전용이며 첫 실행에도 카탈로그를 요구합니다.
