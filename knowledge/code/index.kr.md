# 코드 지식

소프트웨어 구현, 시스템, 런타임 동작, 검증.

[도메인 라우팅](../index.md) | [저장과 수명 주기](../../skills/vegabond-knowledge/references/storage.md)

<!-- onestep-catalog:start -->
영어 원본 메타데이터에서 생성한 목록이다. 이 행이 아니라 상세 파일을 고친다.

| ID / 제목 / 종류 | 요약 | 범위 / 맥락 | 키워드 | 상태 / 확인일 | 상세 |
| --- | --- | --- | --- | --- | --- |
| K-CODE-UE-ENGINE-CHECKOUT / 커스텀 언리얼 엔진 소스를 읽기 전에 현재 쓰는 체크아웃인지 확인한다 [lesson] | 엔진 경로 환경 변수가 오래된 체크아웃을 가리키고 실제 소스는 git worktree에 있을 수 있다. 엔진 소스나 이력에서 결론을 내기 전에 worktree, 브랜치, Build.version을 확인한다. | 환경 변수나 레지스트리 연결로 소스 빌드 또는 포크 언리얼 엔진을 찾는 프로젝트; {"engine": "Unreal Engine 5 source build", "vcs": "git with worktrees"} | Unreal Engine, custom engine, engine fork, git worktree, Build.version, EngineAssociation, engine source, stale checkout | active / 2026-11-06 | [K-CODE-UE-ENGINE-CHECKOUT](K-CODE-UE-ENGINE-CHECKOUT.md) |
| K-CODE-UE-RENDER-ORIENTATION / 언리얼 프로젝트의 렌더링 구성을 공부나 최적화 전에 파악하는 방법 [method] | 렌더러 설정으로 렌더링 경로를 분류하고, 표시나 이력으로 엔진 렌더러 변경을 찾고, 뷰 익스텐션, 글로벌 셰이더, 셰이더 파일을 검색해 프로젝트 렌더 진입점을 찾은 뒤 공부나 최적화를 계획한다. | Unreal Engine 5 게임 프로젝트, 특히 커스텀 엔진과 프로젝트 내 렌더링 플러그인이 있는 경우; {"engine": "Unreal Engine 5.x", "platform": "Windows desktop"} | Unreal Engine, rendering, renderer settings, Nanite, Lumen, Virtual Shadow Maps, distance field shadows, static lighting, SceneViewExtension, ISceneViewExtension, RDG, FRDGBuilder, IMPLEMENT_GLOBAL_SHADER, usf, vertex factory, scalability, PSO | active / 2026-11-05 | [K-CODE-UE-RENDER-ORIENTATION](K-CODE-UE-RENDER-ORIENTATION.md) |
<!-- onestep-catalog:end -->
