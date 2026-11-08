# 게임 기술 실험실

저장된 기술을 검증하는 독립 Unity 6000.0.77f1 실험이다. 재현 가능한 프로토타입·측정 하네스이며 완성 게임이나 다른 엔진·플랫폼 벤치마크가 아니다.

## 설계와 통과 기준

설치된 Unity와 Windows 빌드를 사용한다. 외부 에셋·레지스트리 패키지·네트워크·기존 게임 프로젝트 없이 네이티브 물리와 MonoBehaviour Update를 실행한다. 요약 전에 원본 표본·하드웨어·빌드 식별을 남긴다.

| 기술 | 비교와 계약 | 통과 기준 |
| --- | --- | --- |
| 카메라 | 프레임마다 10% 보간과 rate=4 지수 감쇠. 정지 목표 2초 응답은 경과 시간 기준. | 합성 30/60/144 FPS·긴 프레임, 실제 Update 요청/실측 FPS. 오차 0.0001 이하. 이동 목표·충돌 제외. |
| 히트스캔 | 카메라 조준 의도와 카메라 단독 피해 규칙 비교. 총구 경로·원점 겹침·무기 뿌리 차단. | 총구 엄폐는 차단, 개방은 명중, 내부/벽 너머 총구 우회 차단, 레이어·트리거 제외. |
| 공유 가중 경로장 | 같은 출구의 역방향 다익스트라와 개별 A* 비교. 방향 비용·0비용 순환 방지. | 알려진 비용·도달 불가·무효화·독립 비용 비교, 후속 노드를 소비하는 개체. 국소 회피 제외. |

CPU 측정은 준비 실행·반복 배치·모든 표본·중앙값/p95·작업량을 기록하고 설정·에셋·I/O를 타이머 밖에 둔다. 경로장 재계산과 캐시 조회를 구분한다. 대량 수학·물리 질의는 전체 프레임이나 GPU 비용이 아니다. 독립 실행을 반복하되 이 PC의 수치를 모바일·멀티플레이·상용 장면에 그대로 옮기지 않는다.

## 구성과 실행

- Assets/TechniqueLab: 커널 세 가지·독립 검사·런타임 하네스·장면 소비자.
- Assets/Editor: 엔진 확인·검사·빌드·Play 진입점.
- Results: 실패/통과·에디터/실행 기록과 이미지.
- Build: Git 제외 생성 실행 파일.

실제 컴파일·의미 있는 실패 후 통과·PlayMode·Windows 빌드와 실행·이미지 확인·측정·지식 반영까지 수행해야 완료다. 수식 검사만으로 엔진 실행을 대신하지 않는다.

Unity에서 Assets/TechniqueLab.unity를 열고 Play하거나 빌드 뒤 `./Run-Player.ps1 -Session interactive-check -Interactive`를 실행한다. Reset followers·Cycle cover·Toggle grid door·Quit 버튼이 있다. 문 변경은 개체를 안전한 초기 칸으로 되돌리므로 이동 중 복구·국소 회피 구현이 아니다.

[측정 결과와 재현 명령](RESULTS.kr.md)에 최종 PlayMode·독립 실행 3회·실제 UI 관찰·근거를 정리했다. [분석 스크립트](analyze_results.py)가 보고와 소스 해시를 검사한다. 약 3ms 목표로 보정한 배치에 변형별 순서를 번갈아 31표본을 기록하며 원본 배치·호출당 정규화 시간을 보관한다. 자동 PNG에는 OnGUI가 없고 실제 버튼은 따로 확인했다. Build·Library·로그는 생성 로컬 파일로 Git 제외한다.

## 동적 확장

별도 DynamicLab에서 초기화 없는 문/상자·예약 회피를 검사했다. [설계](DYNAMIC.kr.md)·[결과](DYNAMIC-RESULTS.kr.md)를 참고한다. DynamicBatch.Build와 Run-Dynamic.ps1을 사용한다.

## 양방향·반경 확장

별도 TrafficLab.unity에서 고정 혼합 반경·방향별 장·작성한 교행 차선·좁은 통로 임대를 검사했다. [설계](TRAFFIC.kr.md)·[결과](TRAFFIC-RESULTS.kr.md)에 안전/교착/충돌 비교·실제 프레임3회·한계를 기록했다. TrafficBatch.Build와 Run-Traffic.ps1의 Interactive/측정용Visible, analyze_traffic.py를 사용한다. 진입 중단은 이전 물리 장애물 변경과 별도다. 기존 장면·소스·근거를 보존한다.

## 무차선 지속 유입 확장

별도 StreamLab에서 요청별 검색·완전 시간 예약·외부 FIFO·개별 ID 응답을 검사했다. [설계](STREAM.kr.md)·[결과](STREAM-RESULTS.kr.md)의 과부하 응답 실패·기아 비교·두 지형3회 전체 프레임과 적용 조건을 읽는다. StreamBatch.Build,Run-Stream.ps1,analyze_stream.py를 쓴다. 기존 장면/소스/근거를 보존했다.
