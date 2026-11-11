# 코드 문제 기록

소프트웨어 구현, 시스템, 실행 동작과 검증에 관한 기록입니다.

[분야 안내](../index.kr.md) | [저장과 수명 관리](../../skills/vegabond-knowledge/references/storage.kr.md)

영문 원본 메타데이터에서 생성한 사용자용 번역입니다. 변경은 상세 원본에 반영합니다.

| ID / 제목 / 종류 | 요약 / 발생 조건 / 증상 | 범위 / 맥락 | 검색어 | 상태 / 확인일 / 원인 / 예방 | 상세 |
| --- | --- | --- | --- | --- | --- |
| R-CATALOG-BOOTSTRAP / 첫 빌드가 생성 예정 색인 참조를 거절함 [오류] | 색인 생성 전에 루트 링크를 검사해 생성 예정 색인까지 누락으로 판단했습니다. 선택한 출력을 계획한 뒤 참조를 검사하고 해당 출력만 예외로 허용합니다. 발생 조건: 유효한 상세와 생성 예정 색인을 가리키는 루트 링크가 있는 첫 빌드. 증상: broken_reference 오류로 색인을 쓰지 못함. | OneStep; vegabond-knowledge catalog.py build와 check | bootstrap, first-build, broken_reference, domain-index, catalog-planning | 해결 / 2026-11-05; 원인 확정; 예방 검증됨: 여러 저장소, 계획된 보관 색인, 미선택 색인과 실제 누락 파일에 대한 회귀 검사 | [상세](R-CATALOG-BOOTSTRAP.kr.md) |
| R-CODE-SUNO-CONTEXT-BOUNDARY / Suno 연결에서 채팅·메모리 제외 [개선 제안] | 사용자가 플러그인 문맥 공유를 거절했습니다. 채팅·메모리 입력이 없는 전용 클라이언트가 검토된 가사·스타일만 허용하는 검사와 함께 연결에 성공했습니다. 발생 조건: 가사와 음악 지시문만 허용하는 Suno 연결. 증상: 플러그인 안내의 관련 대화·메모리 공유가 요구 조건과 맞지 않음. 실제 유출은 관찰되지 않음. | 수정되지 않은 OneStep 전용 클라이언트와 검토한 입력; Windows, Node.js 22.19.0, PowerShell 7, 공식 MCP 클라이언트 2.4.0 | Suno, MCP, privacy, memory, chat-history, exact-content, allowlist, egress, approved-payload, DPAPI | 해결 / 2026-11-10; 원인 확정; 예방 검증됨: 검토한 lyrics/style 파일과 정확히 일치하는 전용 경로를 사용하고 변경 후 소스 해시·차단 검사를 확인 | [상세](R-CODE-SUNO-CONTEXT-BOUNDARY.kr.md) |
| R-CODE-SUNO-MCP-AUTH / Suno MCP 서버 등록 후 인증 확인 [오류] | 초기에는 AI 앱 연결 자격을 거절했습니다. 사용자 승인 메일 수신 보고 후 전용 제한 클라이언트의 인증·도구 조회·자격 증명 재사용에 성공했습니다. 실제 곡 생성은 미검증입니다. 발생 조건: 공식 HTTP 서버 등록 후 첫 OAuth 로그인. 증상: 로그인과 명시적 권한 승인 뒤 Account Linking Error 및 AI 앱 연결 불가 표시. | Windows Codex CLI의 Suno MCP 베타; 관찰된 연결에 한정; codex-cli 0.163.0 | Suno, MCP, OAuth, invalid_scope, 인증, 음악 생성, 연결 | 해결 / 2026-11-10; 원인 추정; 예방 제안: 제공자 베타 자격, 동의, 인증 완료, 실제 도구와 음원 생성을 각각 확인 | [상세](R-CODE-SUNO-MCP-AUTH.kr.md) |
