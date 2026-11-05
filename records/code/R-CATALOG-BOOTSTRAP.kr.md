# 첫 생성에서 자신의 미생성 색인 링크를 거부한 문제

사람용 번역본입니다. AI는 읽거나 검색하지 않습니다. 영문 R-CATALOG-BOOTSTRAP.md가 기준입니다.

| 항목 | 값 |
| --- | --- |
| ID | R-CATALOG-BOOTSTRAP |
| 요약 | 생성될 색인이 생기기 전에 루트 링크를 검사해 첫 build가 차단됐습니다. 선택된 모든 색인을 계획한 뒤 파일 존재를 검사하고 build에서만 해당 생성 대상 경로를 허용하도록 수정했습니다. |
| 유형·범위 | error; OneStep의 vegabond-knowledge catalog.py build/check |
| 검색어 | bootstrap, first-build, broken_reference, domain-index, catalog-planning |
| 상태·확인일 | resolved; 2026-11-05 |
| 발생 조건 | 올바른 분야 상세 문서와 아직 생성되지 않은 분야 색인을 가리키는 루트 경로가 있는 첫 build |
| 증상 | 미래 index.md 대상에 broken_reference를 보고하고 색인을 하나도 쓰지 않음 |
| 원인 확신 | confirmed |
| 예방 | 생성 계획·링크 검사 변경 시 여러 저장소·보관 색인·선택 밖 색인·실제 누락 파일에 대한 초기 생성 회귀 테스트 실행 |
| 예방 상태 | verified |

## 기대와 관찰

첫 build는 루트 링크가 분야 색인을 미리 가리켜도 올바른 상세에서 색인을 생성해야 합니다. 통합 시험과 수정 전 회귀 검사에서 종료 코드 1, broken_reference, 생성 파일 없음이 확인됐습니다. 색인 제목 파일을 미리 만들면 우회할 수 있었지만 필요하지 않아야 합니다.

## 원인과 해결

입력을 읽는 동안 모든 생성 대상이 정해지기 전에 파일 존재를 검사했습니다. 이제 로컬 참조를 수집하고 모든 선택된 색인을 계획한 뒤 대상을 검사합니다. build는 실제 생성 계획과 일치하는 해석된 경로만 미존재 상태로 허용하며 check는 누락을 허용하지 않습니다. 다른 깨진 참조는 계속 쓰기를 막습니다. 초기화 명령·폴더·빈 파일을 추가할 필요가 없습니다.

## 재검증과 예방

2026-11-05에 새 초기 생성 테스트 세 개가 수정 전 실패하고 수정 후 통과했습니다. 일반 누락 파일의 거부 테스트는 전후 모두 통과했습니다. 최종 전체 테스트 24개가 통과했습니다. 네 초기 생성 테스트는 두 저장소·여러 분야의 첫 생성, 생성 전 읽기 전용 검사, 재생성 시 무변경, 상세 원본 보존, 생성할 보관 색인·상세의 참조, 실제 누락 파일·선택 밖 색인을 포함합니다.

이는 이 도구의 해당 동작에 대한 실행 근거이며 CI 강제나 다른 지식 시스템의 호환성은 주장하지 않습니다. build의 생성 대상 예외를 바꿀 때도 실패해야 하는 사례를 유지합니다.

## 근거

- [회귀 테스트](../../skills/vegabond-knowledge/tests/test_catalog.py): test_bootstrap_builds_multiple_stores_without_index_stubs, test_bootstrap_still_rejects_unplanned_missing_files, test_bootstrap_does_not_exempt_unselected_catalogs, test_bootstrap_resolves_planned_archive_and_detail_links.
- [도구](../../skills/vegabond-knowledge/scripts/catalog.py): links에서 수집하고 run의 모든 분야 계획 뒤 검사합니다.
- [저장 절차](../../skills/vegabond-knowledge/references/storage.md#first-catalog-build): 상세·경로 작성, build, 변경 색인 번역, check.
