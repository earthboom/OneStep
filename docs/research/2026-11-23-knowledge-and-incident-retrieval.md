# OneStep에서 다음 작업자가 지식과 과거 결함을 다시 찾는 방법

2026-11-23 · 적용 대상은 `vegabond-knowledge`와 그 검색 도우미다. 검색 전에는 다음 작업자가 아는 정보가 제한적이다. 작업 전에는 하려는 동작과 제약을 알고, 실패 직후에는 증상과 오류 문구를 알고, 이전 검토를 이어갈 때는 문서 ID를 안다. 이 세 상황을 분리해 저장 방식과 검색기를 점검했다.

## 조사에서 채택한 방법

| 근거 | OneStep에 적용한 판단 |
| --- | --- |
| KCS는 문의자가 문제를 처음 표현한 말과 환경을 보존하고, 이미 존재하지만 찾기 어려웠던 문서를 실제 문의 표현으로 보강한다. [Consortium for Service Innovation 실무 지침](https://library.serviceinnovation.org/KCS/KCS_v6/KCS_v6_Practices_Guide/030/030/010/020) | 문제 기록의 `symptom`에는 사용자가 관찰한 표현을, `trigger`에는 작업 전에 검색할 동작을 남긴다. 같은 원리·범위의 사례를 새로 복제하기 전에 기존 상세에 누락된 표현과 검사를 추가한다. |
| Sun 등의 중복 버그 보고 연구는 제목·설명과 제품·구성요소·버전을 결합해 Mozilla, Eclipse, OpenOffice에서 관련 보고서의 순위를 평가했다. [ASE 논문 원문](https://cs.uwaterloo.ca/~cnsun/public/publication/ase11/ase11.pdf) | 검색 단계에서는 후보를 넓게 찾고 채택 단계에서 환경과 원인을 대조한다. 증상이 비슷해도 환경이 다르면 이전 수정의 전용을 보류한다. 논문의 학습 가중치나 중복 판정 점수를 이 저장소에 그대로 이식할 근거는 없다. |
| Google 개발자 대상 조사와 로그 분석에서 API 사용법, 동작 원리, 실패 원인, 코드 위치는 흔한 검색 목적이었다. [Sadowski·Stolee·Elbaum의 현장 연구](https://research.google/pubs/how-developers-search-for-code-a-case-study/) | 식별자를 이미 아는 질문에는 철자·구두점·전체 ID를 보존한다. `R-CODE-UE-MUSIC-STOP` 안의 일반어 `music` 때문에 다른 문서가 먼저 나오는 실패를 재현해 수정했다. |
| Google SRE의 회고 절차는 영향·조치·후속 검토를 연결하고, 사건이 누적된 뒤 구조화된 기록에서 경향을 분석한다. [Google SRE 사고 대응 경험](https://sre.google/resources/practices-and-processes/incident-management-guide/) | 과거 결함을 찾으면 `cause_status`, `prevention_status`, 실제 재검증 근거를 확인한다. 해결된 사건도 검색 대상에 남긴다. 예를 들어 잘못된 이름 인덱스를 찾은 뒤에는 숫자처럼 보이는 속성 이름을 정상 디코딩으로 오판하는지와 정상 입력을 함께 검사할 수 있다. |
| BEIR는 18개 데이터셋에서 어휘 검색이 강한 기준선이 될 수 있고 재순위화에 효과와 연산 비용이 함께 있음을 보였다. MIRACL은 한국어를 포함한 다국어 질의와 관련성 판정을 제공한다. [BEIR 논문](https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/hash/65b9eea6e1cc6bb9f0cd2a47751a186f-Abstract-round2.html) · [MIRACL 논문](https://aclanthology.org/2023.tacl-1.63/) · [언어별 자료 구성](https://project-miracl.github.io/) | OneStep에서는 한국어 질문, 영문 기술명, 사건 ID, 증상이 비슷한 오답을 따로 평가한다. 공개 벤치마크는 후보 기법을 고르는 근거이며, 프로젝트의 짧은 재발 방지 기록에서 얻을 적중률은 로컬 사례로 측정해야 한다. |
| Stanford CS224U의 공개 강의는 역색인과 순위 평가를 구분하고 첫 정답 순위와 재현율을 각각 설명한다. 영상의 공개 챕터 기준으로 7:25는 역색인, 20:01은 Success·MRR, 21:13은 Precision·Recall이다. [Stanford Online 강의](https://www.youtube.com/watch?v=e8zKKDMAze8) | 필수 자료 중 첫 번째가 얼마나 위에 있는지와 여러 필수 자료를 모두 회수했는지를 따로 보고한다. 빈 결과여야 하는 질의는 별도 평가한다. 현행 평가는 모든 검색 결과의 정밀도를 측정하지 않는다. |

## 적용 사례

**한국어 문장에 섞인 식별자.** 원래 `RenderDocPlugin`은 찾을 수 있었지만 `RenderDocPlugin을`은 결과가 없었다. `UAsset.GetNameReference에서`도 자료가 있는 상태에서 실패했다. 검색 시 자주 쓰는 조사의 경계만 처리하고, 본문에 조사가 붙은 경우에도 실제 원문 줄을 가리킨다. `Widget::FlushExtra`를 `Widget::Flush`로 잘못 찾거나 `RenderDocPlugin용`에서 임의로 어미를 잘라 내지 않는 대조 사례를 검사했다. 전체 ID만 주어진 경우에는 그 안의 주제어 확장보다 ID 일치를 우선한다.

**기록은 있는데 그 표현이 없는 경우.** 기존 경로 탐색 평가에서 `packed priority PriorityKey ties state distance`의 정답 문서는 6위였고 요구 범위는 상위 3개였다. 해당 문서는 압축 키가 정렬 순서를 보존해야 한다고 설명하고 있었다. 여기에 동일 거리, 마지막 동점 기준, 필드 상한에서 원래 튜플과 압축 키의 정렬 결과를 대조하는 검사를 추가하자 1위가 됐다. 문서를 보강한 뒤에는 이전 검색기로도 기존 평가가 모두 통과했다. 순위 개선이 문서와 알고리즘 중 어디서 왔는지 분리할 수 있었던 사례다. [보강한 경로 탐색 지식](../../knowledge/game/K-GAME-TECH-PATH.md)

**질문이 여러 개인 작업.** 같은 프로젝트·저장소·필터로 후진 카메라와 중복 중단 문제를 함께 조사한다면 `--query`를 두 번 전달한다. 문서는 한 번 불러오고 결과·빈 결과·관련 기록·출처 확인은 질문별로 반환한다. 다른 환경 조건이 필요한 질문은 별도로 실행한다. 검색 내부에서도 정규식 검사 전에 실제 문자열이 있는지 확인하고 반복 사용하는 경계 패턴을 제한된 개수만 재사용한다. 검색 점수와 자료의 사실성은 별도로 판단한다. [검색 명령과 결과 형식](../../skills/vegabond-knowledge/references/retrieval.md#separate-questions-in-one-call)

**찾은 뒤의 판단.** 같은 명령에서 `UAsset.GetNameReference에서`는 파서 사건을 1위로 반환했고 해당 사건의 예방 상태는 `verified`였다. `R-FIC-N2-DIALOGUE-20261106의`는 소설 대화 사건을 1위로 반환했지만 예방 상태는 `proposed`였다. 전자는 검증 환경이 현재 작업과 일치하는지 확인해 검사를 재사용하고, 후자는 제안된 검사를 이번 원고에서 먼저 시험하는 것이 맞다. 첫 검색 결과를 그대로 규칙으로 승격하면 두 기록의 가장 중요한 차이가 사라진다.

## 다른 접근을 선택할 조건

- **SQLite FTS5**는 지속되는 역색인과 열별 가중치가 필요한 비교 후보이다. Markdown이 정본이면 추가·수정·삭제의 동기화와 색인 재구축도 검증해야 한다. 특히 기본 토크나이저가 기술명 구두점과 한국어 조사를 어떻게 처리하는지 같은 사례로 먼저 확인한다. 현행 전체 문서 로딩이 병목일 때 검토한다. [SQLite FTS5 공식 문서](https://sqlite.org/fts5.html) · [프로젝트의 규모별 측정 기준](../../skills/vegabond-knowledge/references/search-scale.md)
- **한국어 형태 분석과 어휘·의미 혼합 검색**은 이번 경계 처리로 회수되지 않는 실제 바꿔쓰기 질문이 반복될 때 비교한다. 한국어 분석기의 복합어 분해나 품사 제거는 의미 있는 접두사를 잃을 수 있어 사용자 사전과 인접 오답도 함께 시험한다. 후보 회수 후 원문과 적용 범위를 확인하는 절차는 유지한다. [Elastic Nori 품사 필터 문서](https://www.elastic.co/docs/reference/elasticsearch/plugins/analysis-nori-speech) · [MIRACL](https://aclanthology.org/2023.tacl-1.63/)

## 검증 범위

Windows 11, Python 3.12.3에서 실제 지식·문제 기록 172건을 사용했다. 기존 도우미는 커밋 `ca13c55`의 검색 코드다. 기존 7개 사례 파일의 218개 질문, 새 회귀 사례 5개, 구현 조정에 사용하지 않은 추가 대조 3개를 구분했다. 추가 대조는 소설 사건 ID, 게임 지식 ID, 존재하지 않는 긴 플러그인 이름이다. 새 사례 수가 적어 임의의 한국어 질문에 일반화할 수 없다.

| 평가 | 변경 전 | 검색기·문서 반영 후 |
| --- | ---: | ---: |
| 기존 218개 사례 통과 | 217/218 | 218/218 |
| 기존 사례에서 필수 ID 회수 | 208/209 | 209/209 |
| 기존 사례에서 첫 필수 ID의 평균 역순위 | 0.9326 | 0.9379 |
| 신규 회귀 5개 통과 | 1/5 | 5/5 |
| 별도 대조 3개 통과 | 1/3 | 3/3 |

속도를 비교할 때는 보강된 동일 문서 집합으로 두 버전을 각각 예열한 뒤 실행 순서를 번갈아 바꿨다. 이미 메모리에 있는 문서를 대상으로 기존 218개 질의를 네 차례 일괄 평가한 중앙값은 **16.25초 → 1.98초**였다. 이 수치에는 프로세스 시작, 디스크에서 문서 로드, 외부 원본 검증이 포함되지 않는다. 코퍼스 전체를 훑는 방식은 그대로이며 자료가 대폭 늘어날 때의 지연은 별도 측정 대상이다.

기존 평가 묶음은 공통 23개, 게임 적용 11개·확장 25개·네이티브 150개, TechniqueLab의 Dynamic·Traffic·Stream 각 3개다. 별도 대조 질의는 `R-FIC-N2-DIALOGUE-20261106의`, `K-GAME-TECH-WATER로`, `RenderDocPluginExtended를`였다. 앞의 두 질의에는 해당 ID를 1위로, 마지막 질의에는 빈 결과를 기대했다. 최종 문서 해시 목록의 SHA-256은 `a825aa20ba5320fbef86d3be103bb31546a9e8a2cf8fffffceeb13a72bd90d42`다. 검증된 지식 도우미 테스트는 92개, 배포본 테스트는 5개다.

실제 명령 시간은 전체 테스트가 끝난 후 별도로 측정했다. `--store records --limit 3 --no-cache`로 `reverse camera framing`, `duplicate stop fade`, `work brief`를 조회했다. 세 방식의 실행 순서를 순환해 각 세 번 측정했고, 질문별 상위 결과 ID 목록이 매번 일치했는지도 확인했다. Python 시작과 정본 읽기를 포함한 세 질문 전체의 중앙값은 이전 도우미 개별 실행 **9.17초**, 개선 도우미 개별 실행 **5.33초**, 개선 도우미 묶음 실행 **2.43초**였다. 범위는 각각 5.69–10.18초, 5.04–6.47초, 2.04–2.92초였다. 파일시스템 캐시는 비우지 않았으며 세 번의 측정으로 꼬리 지연을 추정할 수는 없다.

공통 회귀 사례는 아래 명령으로 재실행한다. 기존 평가 파일에는 상황별 필수·금지 ID와 순위 제한이 들어 있다. 이번 실제 질의와 오답 대조는 같은 파일에 추가했다.

```powershell
python skills/vegabond-knowledge/scripts/search.py evaluate --project . --cases skills/vegabond-knowledge/tests/retrieval_cases.json --no-cache
python skills/vegabond-knowledge/scripts/search.py search --project . --store records --query "UAsset.GetNameReference에서" --query "R-FIC-N2-DIALOGUE-20261106의" --limit 1 --no-cache
```

같은 문제를 다르게 표현한 질문의 순위와 3만 건에서의 개별 검색 시간은 [후속 규모 실험](2026-11-23-korean-retrieval-at-30000.md)에 기록했다.
