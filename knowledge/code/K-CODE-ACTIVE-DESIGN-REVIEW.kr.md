# 소비자가 직접 설계를 사용해 교차 검토하기

요청을 근거로 독립적으로 예상 결과를 낸 뒤 소비자가 설계를 따라 호출 순서를 써 본다. 처음으로 예측이 갈린 지점을 고친 뒤 같은 사례를 다시 확인한다.

ID `K-CODE-ACTIVE-DESIGN-REVIEW` · 방법 · 활성 · 근거 확인 2026-11-25

적용 범위 — 그럴듯한 해석 차이나 누락된 계약이 인수 판정에 영향을 주는 설계 검토와 인계

## 지침

검토자에게 원래 요청과 기준 계약을 먼저 준다. 보통 입력 하나와, 그럴듯한 두 해석에서 관찰 가능한 결과가 달라지는 사례 하나를 요청한다. 그다음 설계를 주고 호출 순서나 의사 코드를 작성하게 한다. 필수 정보를 추측해야 하는 첫 단계를 적는다. 제품 결정은 담당자에게, 기술 질문은 해당 계약이나 실험에 근거해 푼다.

## 적용 범위와 예외

공유 API, 소유권 변경, 영속성과 장애 복구에 적합하다. 명확한 표시 전용 편집은 직접 확인할 수 있다. 출처를 바탕으로 한 검토 방법이며 검토자 합의 자체로 실제 구현 동작이 입증되지는 않는다.

## 확인 방법

작업 폴더에는 피드백 파일이 있지만 지정 수신함에는 영문 파일만 있는 경우를 보자. 전달 상태를 먼저 예측하고 호출자가 확인하는 경로를 추적한 뒤, 빠진 파일을 복구해 같은 검사를 되풀이한다. 예상 전이, 근거와 구현을 기다려야 하는 검사를 인계한다. [OneStep inbox contract](../../feedback/README.md)

제한을 바꿀 때는 0.8초 호출 49건과 2.0004초 호출 한 건을 준다. 회차 P95 0.8초는 통과하나 모든 응답 조건은 실패한다. 호출자가 잰 반올림 전 시간을 어디서 비교하는지 소비자가 짚게 한다. 표시 전용 변경은 제목과 바인딩을 확인한다. 검토 결과에는 요구, 보존할 동작, 판별 입력, 보장 지점, 근거, 미해결 검사의 담당자를 남긴다. 수정한 뒤 같은 입력과 기존 호출자를 다시 확인한다. [Caller benchmark](K-CODE-RETRIEVAL-SCALE.md) · [When glossary lookup changes acceptance](K-CODE-ACCEPTANCE-GLOSSARY.md) · [Review procedure](../../skills/vegabond-code-design/references/review.md)

## 근거

NASA §4.4는 요구사항 부합과 의도한 용도 적합성을 구별한다. ARID §2.2는 사용할 사람이 설계를 직접 적용한다. Porter 등의 실험은 대학원생 48명이 3인 16개 팀으로 명세 두 개를 검토했다. 시나리오 읽기는 더 많은 결함을 발견했지만 수집 회의의 이득은 손실로 상쇄됐다. Huang 등은 해당 추론 과제에서 외부 피드백 없는 LLM 자기 수정이 답을 악화시킬 수 있음을 보였다. 독립 예측과 원문 근거를 AI 검토에 쓰는 것은 이 결과의 적용이다. 이 프로젝트에서의 효과를 비교하려면 근거 있는 결함, 근거 없는 지적, 경과 시간과 재검사 시 재발을 기록해야 한다. [NASA handbook](https://www.nasa.gov/reference/4-4-design-solution-definition/) · [ARID report](https://www.sei.cmu.edu/documents/1962/2000_004_001_13685.pdf) · [Porter et al.](https://www.cs.umd.edu/~basili/publications/technical/T101.pdf) · [Huang et al.](https://arxiv.org/abs/2310.01798)

검토 깊이와 독자를 정할 때는 문서 작성 비용과 영향을 받는 팀의 역할에 대한 저자의 경험을 참고한다. [Malte Ubl, Design Docs at Google](https://www.industrialempathy.com/posts/design-docs-at-google/)

### 구현 전에 게임 설계 검수 지적을 판단하는 법 (2026-11-26 조사)

OneStep에는 이미 호출자가 기대하는 결과를 추적하고, 상태 전이의 반례를 찾고, 검증되지 않은 플레이 경험을 플레이테스트로 넘기는 절차가 있다. 이번 제안은 지적을 발견한 다음 취할 행동에 관한 것이다. 기대 결과의 출처, 판정을 가르는 실제 도달 가능한 상황, 남은 의문을 해소할 사람이나 증거를 확인한다. 처리 방향이 달라질 때만 이 질문을 쓴다. 플레이어에게 미칠 영향과 그 판단을 뒷받침하는 증거의 강도는 별도로 본다. [현재 설계 검수](../../skills/vegabond-code-design/references/review.md) · [기존 플레이테스트 방법](../game/K-GAME-PROTOTYPE-PLAYTEST.md)

| 지적 | 판단 근거와 행동 |
| --- | --- |
| 설계 결함 | 합의한 제약, 실제로 가능한 사건 순서, 그때 위반되는 관찰 결과를 제시한다. 설계가 이미 막는 상황인지 확인하고 해당 결정을 수정한 뒤 같은 사례를 다시 대입한다. |
| 기획 결정 누락 | 기준 문서와 양립하는 두 결과가 플레이어에게 어떤 차이를 만드는지 보인다. 결정권자에게 그 상황 하나를 묻는다. 엔진의 동작처럼 기술로 답할 문제는 선언이나 작은 실험으로 해결한다. |
| 개선 후보 | 현 설계도 선택지에 남긴다. 대안 하나가 구체적으로 개선할 목표, 비용, 잃을 수 있는 것을 비교하고 어떤 관찰이 나오면 선택을 바꿀지 적는다. |
| 플레이 경험 가설 | 관찰했거나 예상하는 행동, 이를 설명하는 경쟁 가설, 둘을 구별할 최소 플레이테스트를 적는다. 패배율 하나로 신호를 못 봤는지 위험을 알고 감수했는지 판정할 수 없다. |
| 해소된 우려 | 출처를 확인했더니 이미 허용되거나 결정된 동작이면 지적을 닫는다. 기존 관찰로 판별되면 거기서 끝낸다. |

**저장소 사례.** Crossing Tactics의 선택형 팩은 다른 팩 파일이 없어도 작동해야 한다. Bulwark 등록에 Harrier 존재를 요구하는 설계는 Bulwark만 둔 구성에서 약속을 위반한다. 반면 방어한 플레이어가 살아남아야 반격한다는 점은 이미 규칙에 있다. 동시 사망을 상상할 수 있다는 이유만으로 이 규칙을 거부하면 오판이다. 가령 *새 독 효과*로 양쪽이 동시에 죽을 수 있고 승패 규칙이 비었다면 그때 기획자에게 묻는다. 공통 전투 조우 기반 클래스를 추가하자는 제안에는 이 구조가 도울 실제 변형이 필요하다. 저장된 비교 기록에서는 Bulwark 추가 시 실행 코드가 그대로였다. 초보자가 이 조우에서 반격을 스스로 배우는지는 개입 없는 첫 플레이와 플레이어가 기대한 결과에 대한 질문으로 확인한다. 기존 문서와 저장된 변경 기록을 읽어 적용한 예이며, 독 효과는 가정이다. [원 요청](../../docs/examples/cpp-gameplay-workflow/native-tactics/request.md) · [전투 규칙](../../docs/examples/cpp-gameplay-workflow/native-tactics/README.md) · [확장 시 변경 기록](../../docs/examples/cpp-gameplay-workflow/native-tactics/evidence/baseline-vs-extension.json)

**자료별 발견과 적용 범위**

- Letier와 van Lamsweerde는 목표와 환경 가정에서 목표 달성을 방해하는 상황을 도출하는 방법을 정리했다. 실제로 가능한 가장 짧은 위반 순서를 찾는 데 쓸 수 있다. NASA 의사결정 핸드북은 필수 조건과 선호 조건을 구분하고, 결정권자와 결과의 크기에 맞는 분석 깊이를 정한다. 취향 차이로 구현을 막는 오류를 줄이는 데 적용할 만하다. 두 자료의 원래 영역은 요구공학과 시스템공학이다. [장애 요인 분석](https://discovery.ucl.ac.uk/id/eprint/10204032/1/Obstacle-analysis-retrospective.pdf) · [NASA 핸드북 §6.8](https://www.nasa.gov/reference/6-8-decision-analysis/)
- Desurvire 등의 연구는 초기 프로토타입 하나에서 전문가의 원칙 기반 검수와 실제 플레이 관찰을 비교했다. 전자는 전체 지적 수가 많았고, 후자는 검수에서 놓친 지루함·속도·용어 문제를 드러냈다. Tracy Fullerton의 책 《Game Design Workshop》 5판은 경험 목표, 프로토타입, 플레이테스트, 수정을 연결한다. 책은 출판사 소개와 목차를 확인했다. [비교 연구의 결과와 결론](https://www.eng.auburn.edu/~sealscd/COMP7970/notes/Playtesting/usingheuristics.pdf) · [책](https://www.routledge.com/Game-Design-Workshop-A-Playcentric-Approach-to-Creating-Innovative-Games-Fifth-Edition/Fullerton/p/book/9781032607009)
- Valve의 Mike Ambinder는 GDC 강연에서 행동 관찰, 플레이어 진술, 계측의 쓰임을 비교했다. 사망 집중 지도는 위치를 보여주지만 집계하면 맥락이 사라진다. Steve Bromley는 목표를 보고 다른 곳을 탐색한 플레이어를 목표를 못 본 사람으로 오해할 수 있다고 설명한다. 행동이 끝난 뒤 유도하지 않는 질문을 할 이유다. Maddy Thorson은 《Celeste》에서 시간·위치 판정을 의도적으로 너그럽게 둔 사례를 공개했다. 늦은 점프 허용은 의도된 설계일 수 있다. 해당 작품과 팀의 경험이며, 강연 내용은 공개 세션 소개와 슬라이드로 확인했다. [GDC 강연](https://gdcvault.com/play/1566/Valve-s-Approach-to-Playtesting) · [발표 자료](https://cdn.fastly.steamstatic.com/apps/valve/2009/GDC2009_ValvesApproachToPlaytesting.pdf) · [PlayStation 진행 경험](https://www.stevebromley.com/blog/2015/01/06/some-things-ive-learned-about-moderating-playtesting-sessions/) · [Celeste 설계자 기록](https://www.maddymakesgames.com/articles/celeste_and_forgiveness/)
- CHI PLAY 2024의 인디 게임 실무자 13명 면담 연구에서는 적절한 플레이어 모집과 결과 처리에 부담이 있었다. 실제 결정을 바꿀 수 있는 규모의 관찰부터 택할 근거다. Hämäläinen 등은 GPT-3로 게임을 예술로 경험한 듯한 설득력 있는 설문 응답을 만들 수 있었지만, 합성 응답은 연구 기획과 예행연습에 사용하고 결론은 실제 데이터로 검증하라고 했다. 관찰 대상은 설문 응답이었다. [인디 개발자 면담](https://eprints.whiterose.ac.uk/id/eprint/216480/7/CHI_PLAY_24_Indie_Playtesting_final_.pdf) · [합성 플레이어 응답 연구](https://acris.aalto.fi/ws/portalfiles/portal/106452436/SCI_H_m_l_inen_etal_CHI_2023.pdf)
- Huang 등은 추론 과제에서 외부 피드백 없는 자기수정의 한계를 확인했다. Gou 등의 CRITIC은 질의응답·프로그램 합성·유해성 감소 과제에서 도구 피드백을 받아 개선된 결과를 보고했다. OneStep에 옮길 부분은 새 계약 근거, 실행 기록, 플레이 관찰이 생겼을 때 논란 있는 판정을 다시 검토하는 것이다. 두 연구는 게임 설계 검수 정확도를 측정하지 않았다. [자기수정 연구](https://arxiv.org/abs/2310.01798) · [도구 피드백 연구](https://arxiv.org/abs/2305.11738)
- Zheng 등은 AI가 대화 응답을 채점할 때 제시 순서와 답변 길이의 영향을 확인했다. Shankar 등의 EvalGen 연구에서는 전문가 9명이 실제 출력을 채점하며 자신의 기준을 구체화했다. 현지 검증에서는 기획자가 기준을 확정하고 미공개 사례를 남겨 둔다. 기준이 바뀌면 버전을 남기고 양 절차를 같은 기준으로 재채점한다. 다른 AI의 동의에는 기획 결정권이 없다. [MT-Bench 연구](https://arxiv.org/abs/2306.05685) · [EvalGen 논문](https://people.eecs.berkeley.edu/~bjoern/papers/shankar-validators-uist2024.pdf) · [ACM 학회 발표](https://www.youtube.com/watch?v=pkJJNgMYUyM)

**도입 판단용 비교 설계.** 같은 미공개 게임 기획과 기준 문서를 새 맥락의 AI에 주고 기존 검수와 제안 문구를 비교한다. 실제 결함, 의도적으로 특이하지만 정상인 설계, 이미 정한 결정과 실제 누락, 비용이 큰 선택적 개선, 경험 가설을 섞는다. 계약 한 문장만 바꾸면 판정이 뒤집혀야 하는 쌍도 넣는다. 기획자가 출력을 보기 전에 허용되는 판정·행동을 정하고 절차 이름을 가려 채점한다. 준비한 결함 중 발견·누락 수, 결함이라고 지적한 것 중 근거가 맞는 비율, 정상 설계를 막은 수, 불필요한 질문, 플레이어 증거 없는 경험 단정, 검수와 후속 재작업 시간을 본다. 같은 원인의 중복 지적은 한 번만 센다. 사전에 합의한 오거부·비용 허용 범위 안에서 중요한 결함 누락이 줄어들 때 스킬에 반영한다. 현재 근거는 도입 제안까지이며, 이전 후속 변경 측정 (로컬 검증 파일 `skills/vegabond-code-design/tests/repository-change-quality/followup-results.json`)은 구현 검증에 대한 결과다.

**2026-11-26 시범 적용 결과: 현재 설계 스킬 유지.** 이전 맥락을 공유하지 않는 AI 8개가 같은 8항목 가상 게임 설계를 두 버전의 계약으로 검수했다. 계약마다 기존·후보 절차를 두 쌍씩 비교했다. 이동권을 ‘첫 시도’에 쓰는지 ‘첫 유효 입력’에 쓰는지 한 문장을 바꾸면 다리와 나룻배 중 수정해야 할 쪽이 뒤집힌다. 검수 의견을 먼저 저장하고 동일한 동시 승패 결정을 전달한 뒤 실제로 설계안을 다시 작성하게 했다. 별도 AI 채점자 2개가 절차 이름을 가린 혼합 제출물을 사전 정답으로 판정했다. 사용자가 요청한 실험 우선 원칙에 따라 진행했으며, 게임의 정답과 기획자 답변은 가상 명세에 고정했다. 사전 기준 (로컬 검증 파일 `skills/vegabond-code-design/tests/game-design-judgment/protocol.json`) · 후보 문구 (로컬 검증 파일 `skills/vegabond-code-design/tests/game-design-judgment/proposal.txt`)

양쪽 모두 절차당 중요 결함 12/12건을 발견했다. 각 검수에 저장 복구 후 중복 보상, 잘못된 이동권 소모 시점, 지원 설정에서 사라지는 경로 안내가 하나씩 있었다. 정상 설계 차단, 근거 없는 결함 지적, 불필요한 기획 질문, 근거 없는 플레이어 반응 단정, 수정본의 중대한 누락은 양쪽 모두 0건이었다. 두 절차 모두 네 번 모두 이동권 계약에 맞게 판정을 바꿨고, 동시 승패는 기획 결정으로, 초보자 이해도는 플레이 관찰로 넘겼으며 구조 변경을 선택 사항으로 처리했다. 기존 절차의 검수와 설계 재작업은 150.6초와 119.4초, 후보 절차는 170.8초와 129.4초였다. 합산 AI 경과 시간은 270.0초에서 300.2초로 11.2% 늘었다. 시간 증가가 허용 범위 15% 안이었지만 필수 조건인 중요 결함 누락 감소가 없었다. 자료는 판단 사례로 보존한다. 현재 절차가 만점을 받은 이번 사례에서는 복잡한 실제 기획의 정확도나 플레이어 반응까지 판단할 수 없다. 실험 폴더에서 `python judge.py verify`로 원문 해시와 시간·점수 집계를 재검증할 수 있다. 채점 결과와 근거 (로컬 검증 파일 `skills/vegabond-code-design/tests/game-design-judgment/results.json`) · 검수 원문·수정본·시간 (로컬 검증 파일 `skills/vegabond-code-design/tests/game-design-judgment/submissions.json`)
