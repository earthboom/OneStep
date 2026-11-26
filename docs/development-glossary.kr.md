# OneStep 개발 용어집 (시범)

OneStep 자체 개발과 테스트에 적용한다. 동작은 연결된 원본 계약에서 정의하며 계약이 바뀌면 해당 항목을 다시 확인한다.

| 용어와 범위 | 테스트에서의 의미 | 필요한 이유와 근거 |
| --- | --- | --- |
| 개별 검색 응답 시간 · 준비된 색인의 세션 벤치마크 | 호출자에서 질문 하나를 잰다. 각 회차 첫 질문은 인터프리터 실행부터, 이후 질문은 인코딩 전부터 시작한다. 전체 JSON 응답을 받아 디코딩한 뒤 끝낸다. 최초 색인 구축 시간은 별도 측정한다. | 내부 도구 시간과 호출자 P95가 달랐다. 일찍 멈추면 시작·전송·디코딩 중 초과를 놓친다. [측정 지식](../knowledge/code/K-CODE-RETRIEVAL-SCALE.kr.md) · [세션 타이머](../skills/vegabond-knowledge/tests/benchmark_scale.py) |
| 2초 이내 · 질문 50개를 5회 수행 | 기존 P95 기준은 **각 회차**에서 빠른 순서로 48번째 값이다. 이후의 **모든 응답** 기준은 반올림 전 호출자 시간 각각이 2초 이하인지 확인한다. 하나라도 초과하면 실패한다. 결과를 보고할 때 어느 기준인지 밝힌다. | 이전 실행에서는 다섯 회차의 P95가 통과했지만 250건 중 7건이 초과했다. 이후 요구가 강화됐다. [이전 측정](https://github.com/earthboom/OneStep/blob/9f553ba95ec7209a5bf3fcc6ab16b119ebeb8317/docs/research/2026-11-23-search-session-measurements.json) · [모든 응답 검사](https://github.com/earthboom/OneStep/blob/9f553ba95ec7209a5bf3fcc6ab16b119ebeb8317/docs/research/2026-11-23-search-tail-measurements.json) |
| 피드백 접수·제출 · 개발 도구의 전달 상태 | 지정한 체크아웃 접수함에 같은 사안의 영문·한국어 파일이 모두 도착해야 한다. 작업 프로젝트에 두 파일이 있으면 준비 상태를 보고할 수 있다. 검토자의 수용은 별도 결정이다. | 세션에서 보고했지만 목적지에 파일이 없던 사례가 있었다. 실제 목적지를 확인하고 일부만 도착한 상태와 재시도를 검사한다. [접수 규칙](../feedback/README.kr.md) · [문제 기록](../feedback/2026-11-20-feedback-lines-not-submitted.kr.md) · [실행 검사](../tools/test_check_feedback.py) |
