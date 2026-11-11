# 코드 문제 기록

소프트웨어 구현·실행·검증의 원인, 수정과 재검사 기록이다.

| 기록 | 요점 | 상태 / 예방 |
| --- | --- | --- |
| [첫 카탈로그 생성 순서 오류](R-CATALOG-BOOTSTRAP.kr.md) | 생성할 색인을 미리 계획한 뒤 파일 존재를 검사해 정상 참조와 실제 누락을 구분한다. | resolved / verified |
| [Suno 연결에서 채팅·메모리 제외](R-CODE-SUNO-CONTEXT-BOUNDARY.kr.md) | 사용자가 거부한 컨텍스트 공유 대신 검토한 가사/스타일만 전송하는 제한된 클라이언트를 검증했다. | resolved / verified |
| [Suno 등록과 실제 인증 구분](R-CODE-SUNO-MCP-AUTH.kr.md) | 초기 인증 실패 뒤 베타 승인·OAuth·도구 조회·자격 재사용을 확인했다. 실제 곡 생성은 미검증이다. | resolved / proposed |
| [자체 일관성만 검사한 네이티브 자료 누락](R-CODE-UE-EVIDENCE-PROXY.kr.md) | 실제시간 연결과 독립 이벤트값 검사를 추가해 위조된 동일값·절반 시간·0초를 거부한다. | resolved / verified |
| [정책 끝점과 컴포넌트 정밀도 구분](R-CODE-UE-TRANSFORM-TOLERANCE.kr.md) | 1e-4cm 이내 이동 생략을 확인하고 정책값·시간·실제위치의 서로 다른 검사를 유지한다. | resolved / verified |
