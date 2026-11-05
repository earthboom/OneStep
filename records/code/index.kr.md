# 코딩 문제 기록

소프트웨어 구현, 시스템, 실행 동작과 검증.

[분야 경로](../index.md) | [저장과 수명주기](../../skills/vegabond-knowledge/references/storage.md)

<!-- onestep-catalog:start -->
영문 원본 메타데이터에서 생성합니다. 이 행 대신 상세 문서를 수정합니다.

| ID / 제목 / 유형 | 요약 / 발생 조건 / 증상 | 범위 / 맥락 | 검색어 | 상태 / 확인일 / 원인 / 예방 | 상세 |
| --- | --- | --- | --- | --- | --- |
| R-CATALOG-BOOTSTRAP / 첫 생성에서 자신의 미생성 색인 참조를 거부함 [error] | 색인 생성 전에 루트 링크를 검사했습니다. 선택된 모든 색인을 계획한 뒤 존재 여부를 검사하고 build에서만 해당 생성 대상을 허용합니다.; 발생 조건: 올바른 분야 상세와 미생성 분야 색인을 가리키는 루트 경로가 있는 첫 build; 증상: 미래 index.md 대상에 broken_reference를 보고하고 색인을 쓰지 않음 | OneStep; vegabond-knowledge catalog.py build and check | bootstrap, first-build, broken_reference, domain-index, catalog-planning | resolved / 2026-11-05; 원인: confirmed; 예방 [verified]: 생성 계획·참조 검사 변경 시 여러 저장소·생성할 보관 색인·선택 밖 색인·실제 누락 파일의 초기 생성 회귀 테스트 실행 | [R-CATALOG-BOOTSTRAP](R-CATALOG-BOOTSTRAP.md) |
<!-- onestep-catalog:end -->
