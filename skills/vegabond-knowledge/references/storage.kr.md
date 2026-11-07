# 저장과 수명주기

## 위치와 분야

아래 경로는 작업 프로젝트 기준이다. 범위별 조회와 출처 추적을 지원하는 기존 체계가 있으면 재사용하고, 없으면 다음 구조를 쓴다.

```text
knowledge/index.md              # 분야 경로 안내만
knowledge/<domain>/index.md     # 검색 가능한 지식 요약
knowledge/<domain>/<id>.md      # 재사용할 주제·교훈 하나
records/index.md                # 분야 경로 안내만
records/<domain>/index.md       # 검색 가능한 문제 요약
records/<domain>/<id>.md        # 문제·수정·재검사 이력
```

초기 분야는 code·fiction·presentation·planning·shared이며 전체 목록이 아니다. 창작·수정·조사나 확장자가 아닌 대상 주제로 분류하고 실제 내용이 요구하면 분야를 추가한다. 언어·엔진·장르·형식·컴포넌트·작품 ID·작업 하위 유형은 더 깊은 폴더보다 메타데이터에 먼저 둔다.

여러 분야 항목은 주 위치 하나를 정하고 다른 관련 색인에서 연결한다. shared는 근거 있는 공통 적용성에만 쓰고 잡다한 기본 목적지로 쓰지 않는다. 프로젝트 사건과 정본은 그 프로젝트에 두며 근거가 뒷받침할 때만 일반 방법을 공용 지침으로 승격한다.

lessons와 knowledge를 병렬로 만들지 않는다. 기존 교훈 체계가 있으면 재사용하거나 허용된 범위에서 ID·근거를 보존하여 이전한다.

유지하는 저장 문서에는 색인·지식 상세·문제 상세·보관 문서가 포함된다. 영어 문서를 생성·변경할 때마다 영어로부터 `<stem>.kr.md`를 만들고 번역은 읽지 않는다. 기록이라는 이유로 번역 규칙에서 제외하지 않는다. 인계 전 영어 링크·상태 일관성과 번역 쌍 존재를 확인하되 번역 내용은 열지 않는다.

## 항목 헤더와 본문

기본 Markdown 저장소는 독립 재사용할 주제·검사 하나를 상세 하나로 관리하고 다음 YAML 필드를 둔다.

| 필드 | 규칙 |
| --- | --- |
| id | 프로젝트 고유의 안정 ID. 문자·숫자·점·밑줄·하이픈을 사용하고 비교는 대소문자 무시. |
| title | 구체적인 질문·방법·대상. |
| summary | 핵심 적용 조건을 포함한 유용한 요점 1~2문장. |
| kind | 지식은 reference·method·convention·lesson, 기록은 error·suggestion·hypothesis. |
| scope | 프로젝트·컴포넌트·작품과 적용 경계 문자열. |
| keywords | 유용한 영어 개념·동의어·정확한 식별자의 비어 있지 않은 목록. |
| status | 지식은 active·enforced·superseded, 기록은 open·resolved·superseded. |
| checked_at | 실제 근거 확인 날짜 YYYY-MM-DD 또는 미상 null. 편집일로 자동 채우지 않음. |

선택 context는 관련 버전·엔진·형식·장르·시점 등 문자열 또는 문자열의 평면 매핑이다. 버전과 YAML 예약어는 따옴표로 감싼다. 무관한 빈 필드는 만들지 않는다. 항목 메타데이터는 스킬 검색용 frontmatter가 아니며 사람용 번역은 검색 입력이 되지 않는다.

선택 relations는 requires·derived_from·prevention·supersedes·conflicts_with를 다른 저장소·분야의 기존 ID까지 포함하는 비어 있지 않은 목록에 연결한다. 실제 조회에 도움이 되는 관계만 추가한다. [관계 의미와 탐색](retrieval.md#follow-meaningful-relationships)을 따른다. 도구는 형식·대상 ID를 검증하지만 간선은 인과·독립 근거·호환성·검증된 예방을 증명하지 않는다. 본문 출처 링크와 과거 날짜를 보존하며 간선 추가를 새 조사로 취급하지 않는다.

헤더 형식 예시:

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

이는 실제 항목이 아닌 형식 예시다. 뒤에 비어 있지 않은 H2 네 절을 둔다.

- 지식: Guidance, Applicability and exceptions, Checks, Evidence.
- 기록: Expected and observed, Cause and resolution, Recheck and prevention, Evidence.

유용한 행동을 짧게 설명하고 예외·출처 사실·방법·관행·편집 판단을 구분한다. 원본 위치와 검증 맥락을 인용한다. 문제 기록은 원인 확신도·수정 또는 제안·해결 및 재검사 근거·예방 연결을 유지한다. 미상 원인은 미상으로 남긴다. enforced는 입증된 예방 장치가 필요하며 저장만으로 강제 적용이 증명되지 않는다.

이슈·보고서·테스트·구절·화면·로그는 복제보다 원본 참조를 쓴다. 유용하면 같은 원인의 작은 발견을 묶는다. 프로젝트 원본은 그 사실의 권위이고 상세는 항목 메타데이터의 정본이며 카탈로그 행은 파생 투영이다.

### 문제 조회 필드

새 기록이나 정규화한 records 상세는 다음 다섯 필드를 모두 둔다. knowledge 상세에 추가로 요구하는 필드는 아니다.

| 필드 | 규칙 |
| --- | --- |
| trigger | 발생 조건·행동의 짧은 설명 또는 미상 null. 증상 발생 전 조회에 사용. |
| symptom | 구분 가능한 관찰 실패의 비어 있지 않은 설명. 제안·가설은 미확정 결함을 단정하지 않고 관찰된 우려를 설명. |
| cause_status | unknown·suspected·confirmed. Cause and resolution의 근거 필요. 결함이 확정되어도 원인은 미상일 수 있음. |
| prevention | 핵심 조건을 포함한 구체적 행동·검사 또는 미확립 null. 상세 절차·예외·근거는 Recheck and prevention에 둠. |
| prevention_status | none·proposed·verified·invalidated. none은 prevention null, 나머지는 행동 필요. verified는 실제 checked_at과 본문 입증 근거도 필요. |

유용한 카탈로그 행이 되도록 짧게 쓰고 로그·모든 예시를 반복하지 않는다. keywords에는 동의어·정확한 식별자를 두고 모든 문구를 중복하지 않는다. summary는 헤더 복제가 아닌 발견과 핵심 조건이다. 적용성을 바꾸는 버전·정본·형식은 scope/context에 명시한다.

실제 사건이 아닌 기록 예시:

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

resolved는 사건의 상태다. verified는 해당 맥락에서 구체 점검이 원래 실패나 통제된 동등 실패를 탐지했음을 입증한 뒤에만 쓴다. 수정된 결과물만으로는 부족하다. 편집 작업은 결함을 탐지한 문서화된 검토도 유효하지만 자동 강제 검사라고 표현하지 않는다. 수정 결과와 예방 점검의 날짜·결과를 Recheck and prevention에 나누어 기록한다. checked_at은 최신 실제 중요 근거 확인일이며 꾸민 예방 날짜가 아니다. 날짜·헤더만으로 실행이 입증되지 않으므로 전문가는 근거를 읽는다.

네 본문 절을 유지한다. Expected and observed는 원래 계약·관찰·발생 조건·위치, Cause and resolution은 진단 확신도·근거·수정·미상, Recheck and prevention은 수정 결과 검사와 미래 예방의 상태·조건·예외를 분리해 기록한다. Evidence는 원본 판본·보고서를 연결한다. 제안·가설은 기록했다고 오류가 되지 않는다.

### 이전 구조화 기록

공통 헤더만 있고 다섯 필드가 전혀 없는 기록은 읽을 수 있다. 도구는 legacy_record_fields 경고와 함께 원본을 유지하고 새 차원을 unrecorded로 투영한다. strict는 이를 오류로 처리한다. 일부 필드만 추가한 것은 오류이며 레거시 예외가 아니다. 새 기록·편집 기록은 모두 다섯 필드를 쓴다. 도구는 과거 파일의 편집 여부를 추정할 수 없으므로 작성 규칙도 스킬이 관리한다. 허용된 유지보수에서만 ID·경로·근거·미상을 보존하여 정규화하고 제목·옛 카탈로그 행에서 값을 추측하지 않는다.

## 카탈로그 갱신과 검증

[catalog.py](../scripts/catalog.py)는 기존 Python 3.9+ 및 PyYAML 환경을 사용하고 설치하지 않는다. 다음은 OneStep 체크아웃 기준이다. 다른 프로젝트는 도구 절대 경로와 해당 작업 프로젝트의 project 값을 쓴다.

```text
python skills/vegabond-knowledge/scripts/catalog.py build --project . --domain fiction
python skills/vegabond-knowledge/scripts/catalog.py check --project . --domain fiction
```

store knowledge·records 또는 기본 both로 저장소를 고르고 domain을 반복해 영향 분야를 고른다. 분야를 생략하면 프로젝트 전체 중복 ID 검사를 포함한 명시적 전체 유지보수다. 필터 실행은 선택 상세와 명시 관련 참조만 검증한다. 일반 조회는 한정된 검색을 사용하며 매 요청마다 재생성하지 않는다.

도구는 관리 마커 안에 **ID·제목·종류 | 요약 | 범위·맥락 | 키워드 | 상태·확인일 | 상세**의 6열 행을 만든다. 문제 기록의 요약에는 trigger·symptom, 상태에는 원인 확신도·예방 상태·짧은 예방 행동도 표시한다. 일반 지식 행은 그대로다. 해결된 사건은 활성 목록에서 찾을 수 있게 하고 superseded만 보관 목록으로 이동한다. 마커 밖 프로젝트 안내를 보존하고 관련 분야는 주 상세를 연결하되 복제하지 않는다. 루트 색인은 분야 변경 때 유지하는 작은 경로 안내다.

저장 순서는 정본 상세·번역 작성 → build → catalogs_written의 영어 경로 번역 재생성 → check다. build는 준비 단계여서 번역·경로 안내 누락을 경고로 처리한다. check는 최신 카탈로그·유효 메타데이터와 상태·고유 ID·필수 절·로컬 참조·안내·번역 쌍을 요구한다. 중복 YAML 키와 잘못된 구조 헤더는 오류다. 메타데이터·참조 오류는 쓰기 전에 중단하고 변경 카탈로그는 각각 원자 교체한다. 파일시스템 실패로 일부만 갱신될 수 있으므로 다시 검사하고 범위 안에서 복구한다. 도구는 상세 정본이나 번역을 쓰지 않는다.

프로젝트 밖 링크와 절 앵커 정확성은 별도 검증한다. 카탈로그 도구는 명시 관련 정본과 내부 출처 등록부 메타데이터를 읽고, 나머지 로컬 참조는 내용을 열지 않고 존재를 확인한다. 번역은 존재만 검사하며 의미·최신성을 판단하지 않는다. 변경 번역은 영어로부터 다시 만들고 열지 않는다. 진단은 처음 20개와 총수·오류 수를 제공하므로 큰 결과는 분야를 좁혀 조사한다.

### 이동 가능한 출처 참조

작업 프로젝트 밖 출처는 [출처 등록부](../../../knowledge/sources.md)에서 안정 ID와 기계 위치를 분리한다. sources YAML의 각 SRC ID는 소문자 project, 슬래시로 구분한 프로젝트 상대 정본 path, 기존 소문자 해시 또는 null인 sha256만 가진다. 각 ID는 일반 Markdown 링크를 위한 H2를 둔다. 구절·절 위치와 근거 맥락은 참조 항목에 남긴다. 알려진 지문을 보존하며 누락 판본을 추정하거나 과거 근거 날짜를 갱신하거나 변경 가능한 현재 파일로 과거 원고를 인증하지 않는다.

기록 해시가 있는 ID는 그 내용 판본을 식별한다. 다른 근거 판본은 기존 인용을 다른 내용으로 돌리지 말고 새 ID를 만든다. 같은 판본의 위치 변경은 가능하면 로컬 루트만 바꾼다.

영구 루트는 Git 제외된 knowledge/sources.local.json에만 저장한다. 예: `{"novel0": "D:/Writing/Novel_0"}`. 또는 허용된 임시 루트를 `--root project=absolute-path`로 주면 해당 프로젝트의 영구 매핑보다 이번 호출에서만 우선하며 아무것도 쓰지 않는다. 루트를 묻기 전에 사용자가 확인한 작업 경로나 알려진 프로젝트 메타데이터를 재사용한다. 예시는 기본 위치가 아니다. 루트를 꾸미거나 무관한 프로젝트를 검색하거나 연결 복구를 위해 출처 라이브러리를 복제하지 않는다. 다른 프로젝트도 영구 설정은 Git에서 제외한다.

등록 링크를 따른 뒤 현재 주장에 필요한 ID만 [출처 도구](../scripts/sources.py)로 확인한다.

```text
python skills/vegabond-knowledge/scripts/sources.py resolve --project . --id SRC-NOVEL0-ATTAINMENT
python skills/vegabond-knowledge/scripts/sources.py resolve --project . --id SRC-NOVEL0-BODY-MOTION --id SRC-NOVEL0-SPATIAL-BLOCKING --root novel0=C:/Projects/Novel_0
```

명령은 선택 원본의 바이트를 읽어 SHA-256을 비교하므로 허용된 출처 범위에서만 실행한다. 내용 출력, 번역 읽기, 설정·항목 쓰기, 관찰 해시 자동 승격은 하지 않는다. 경로 순회와 설정 루트 밖으로 해석되는 경로를 거부한다. 해시 일치는 내용 동일성만 확인하며 진위·적용성·품질·사용자 수락은 증명하지 않는다. 필요한 원본 구간은 직접 확인한다.

다른 ID를 여러 개 확인하려면 id를 반복한다. 단일 ID는 기존 결과 객체 형태를 유지한다. 배치는 requested_ids·completed·results를 반환하고 입력 순서대로 잘못된 ID·접근 불가 ID까지 결과 하나씩을 제공한다. 완료를 주장하기 전에 입력 ID·수와 결과를 대조한다. 대소문자를 무시한 중복 ID나 중복 루트 지정은 오류이며 조용히 버리지 않는다. root는 다른 프로젝트에만 반복한다.

종료 0은 모두 matched, 1은 unconfigured·missing·unavailable·mismatch·unversioned가 하나 이상, 2는 잘못된 등록부·ID·설정·경로다. 유효 배치의 잘못된 ID는 다른 결과를 버리지 않지만 등록부처럼 공통 입력이 잘못되면 확인을 진행하지 못한다. 결과별 access_status와 identity_status를 나눈다. available은 바이트 읽기 성공, unversioned는 기대 해시 없음이다. 무버전·불일치 파일 모두 접근은 가능할 수 있다. 접근 가능한 무버전 원본은 범위가 명확한 현재 읽기를 뒷받침할 수 있지만 과거 동일성을 인증하지 못한다. 필수 접근·동일성 공백은 그것에 의존한 검사만 막고 독립 작업은 계속한다. 조회 중 과거 null 해시·날짜를 채우지 않는다. 기계의 접근 가능성은 사건 해결·예방 상태가 아니다.

카탈로그 build/check는 등록 ID 링크와 등록부 번역 존재를 확인하고 source_unverified를 알리며 로컬 설정·외부 원본은 읽지 않는다. 등록 링크만으로 외부 근거가 검증되지 않는다. 미등록 ID·잘못된 등록부는 쓰기를 중단한다. 일반 조회는 필요한 ID만 확인하고 모든 출처를 훑지 않는다. 등록부 수정은 번역도 함께 만들되 번역을 읽지 않는다. 현행 Novel_0 참조는 이 등록부를 사용하며 다른 외부 참조는 기존 경고를 유지한다.

레거시 본문 항목은 기존 카탈로그 행·조건을 미검증 Legacy entries로 유지하고 색인 없는 파일은 메타데이터 미상 포인터를 둔다. ID·날짜·규칙·상태를 추정하지 않는다. 허용된 유지보수 때 경로·ID·근거를 보존하여 이전하고 재생성한다. 기본은 경고이고 strict는 정규화된 범위의 레거시를 오류로 본다. 새 항목·수정 항목은 주변이 레거시여도 헤더를 사용한다. 엄격 검사는 과거 근거나 무관한 파일 전체를 고칠 권한이 아니다.

## 기록·통합·승격

저장 전 [조회 도구](retrieval.md)로 양쪽 저장소에서 제안 질문·별칭·근본 원인을 찾고 가까운 항목·관계를 읽는다. 유사도는 후보를 제안할 뿐 자동 병합 권한이 아니다.

앞으로 지원할 결정·행동·검사와 적용 조건을 먼저 정한다. 재사용은 같은 조건의 다른 작업에 유용하다는 뜻이며 보편성은 아니다. 가장 작은 적절한 목적지를 고른다.

- **지식:** 쓸 원칙·방법·이유·검사·예외. 제목·요약은 특정 작업 이력보다 재사용 질문·행동을 중심으로 쓴다.
- **문제 기록:** 발생 조건·증상·원인 확신도·수정·재검사를 구분할 최소 근거만 유지하고 일반 지식에 연결한다.
- **기존 원본·작업 이력:** 고유 프로젝트 사실·정본·작가 선호·일회성 진행은 권위 있는 원본에 둔다. 반복 조회에 이득이 있을 때만 범위 있는 참조·관행을 추가하고 전체 프로필·명세를 복제하지 않는다. 재사용·추적 가치가 없으면 작업 결과에 두고, 후속 추적이 필요한 미해결 문제는 기록한다.

같은 원칙·질문·원인을 먼저 찾아 새 프로젝트 전용 복제보다 기존 항목의 조건·예외·근거·재발을 보강한다. 지식 하나가 조건이 다른 여러 사건을 연결할 수 있다. 원인·발생 조건이 같은 예방을 뒷받침할 때만 사건을 묶으며 같은 증상만으로는 부족하다. 불확실한 일치는 진단을 합치지 않고 연결한다. 중요한 이견을 보존하고 최신이라는 이유로 덮어쓰지 않는다. 문제→예방, 교훈→원래 근거 연결을 유지한다.

설명을 일반화하더라도 근거 경계를 지우지 않는다. 버전·수명·장르·시점·독자 등 핵심 조건은 scope·context·본문·출처에 남긴다. 재현·검색 식별자는 유지하고 부수적 이름·긴 로그는 원본에 둔다. 실제 확인 조건과 원리에 근거한 확장 추론, 미시험 범위를 구분한다. 한 번의 성공은 한정 교훈이며 다른 환경 검증이 아니다. 정본·선호를 보편화하거나 제안 예방을 표현 일반화만으로 승격하지 않는다. 일반화는 프로젝트 간 이동 권한이나 자동 shared 분류가 아니다.

재발 이력은 날짜 또는 미상, 위치·버전, 근거 링크, 수정·재검사, 이전 예방의 결과만 짧게 남긴다. 미실행·실행했으나 불충분·조건 변화로 무효화를 구분하고 미상 결과를 꾸미지 않는다. 반증으로 예방이 무효화되면 invalidated로 표시하고 과거 입증 맥락을 유지하며 대체를 조사한다. 점검 누락이 점검 자체를 반증하지는 않는다. 조건·해결이 다르면 별도 사건으로 분리하고 긴 로그는 원본에 둔다.

반복성·재사용 가능성·유용한 예방이 뒷받침하는 확정적이고 중요한 교훈만 승격한다. 사건은 records, 추린 재사용 내용은 knowledge에 두고 복제 대신 양방향 링크를 만든다. 전문가는 진단·분야 검사를 제공하며 이 스킬은 정리만 하고 원인 확정·결과물 인증을 만들어내지 않는다.

가능하면 구조·타입·검증·린트·회귀 검사로 재발을 예방한다. 원래 실패나 통제된 동등 사례를 탐지한 근거를 유지한다. 판단이 필요한 작업은 조건부 검토 항목과 이유를 기록한다. 저장만으로 예방이 성립하지 않는다.

## 출처를 잃지 않고 폐기

평소 사용 중 중복을 합치고 낡은 적용성을 고친다. 대체할 항목은 정본 상태와 이유·대체 ID를 기록하고 재생성하면 해당 분야 archive로 이동한다. 필요할 때만 보관 목록을 만들고 재활성화하면 되돌린다. 상세 경로·근거는 유지하며 생성 행을 직접 편집하지 않는다. 기존 체계는 자체 보관 방식을 쓴다. 오래됐다는 이유만으로 유용한 지식을 폐기하지 않는다.

출처·버전·정본·예방이 바뀌면 영향 항목과 무효화된 요약을 재확인한다. 한정 검색이 반복해서 무관한 자료를 많이 반환하면 실제 프로젝트 영역으로 색인을 나누고 작은 경로 안내를 남긴다. 관찰된 조회 마찰에 따라 확장하며 매 작업마다 전체 이력을 읽지 않는다.

## 최초 카탈로그 생성

새 저장소·분야는 유효 상세와 번역을 작성하고 루트 안내·번역을 만든다. 루트는 이번 생성이 만들 카탈로그를 미리 가리켜도 되며 빈 색인이나 별도 초기화 명령은 필요 없다. 일반 build→번역→check를 사용한다. 도구는 선택 출력 계획을 모두 세운 뒤 파일 존재를 확인하여 이번 생성 계획 안의 누락 카탈로그만 허용한다. 다른 누락 파일·미선택 누락 카탈로그는 쓰기를 막는다. check는 첫 실행에도 읽기 전용이며 실제 카탈로그가 있어야 한다.
