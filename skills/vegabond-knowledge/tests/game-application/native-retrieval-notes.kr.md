# 네이티브 기법의 지식 검색 회귀 검사

게임 참조 경로 148개와 컴포넌트 끝점 정밀도 및 잘못된 전환 검사의 문제 기록 경로 2개를 포함한 150개 사례로 공유 지식의 검색을 확인합니다. 각 사례는 기대한 ID가 지정한 순위 안에 드는지를 평가합니다.

```text
python skills/vegabond-knowledge/scripts/search.py evaluate --project . --cases skills/vegabond-knowledge/tests/game-application/native-retrieval-cases.json --refresh
```

기법 채택 여부와 런타임 동작은 따로 검증합니다. [전환 검증 기록](../../../../records/code/R-CODE-UE-EVIDENCE-PROXY.kr.md)과 [컴포넌트 정밀도 기록](../../../../records/code/R-CODE-UE-TRANSFORM-TOLERANCE.kr.md)은 재사용할 관찰과 그 근거 범위를 설명합니다. 실행별 상세 측정치는 원본 프로젝트에서 관리합니다.
