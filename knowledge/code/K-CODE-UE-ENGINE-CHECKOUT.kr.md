---
id: K-CODE-UE-ENGINE-CHECKOUT
title: 커스텀 언리얼 엔진 소스를 읽기 전에 현재 쓰는 체크아웃인지 확인한다
summary: 엔진 경로 환경 변수가 오래된 체크아웃을 가리키고 실제 소스는 git worktree에 있을 수 있다. 엔진 소스나 이력에서 결론을 내기 전에 worktree, 브랜치, Build.version을 확인한다.
kind: lesson
scope: 환경 변수나 레지스트리 연결로 소스 빌드 또는 포크 언리얼 엔진을 찾는 프로젝트
keywords: [Unreal Engine, custom engine, engine fork, git worktree, Build.version, EngineAssociation, engine source, stale checkout]
status: active
checked_at: "2026-11-06"
context:
  engine: Unreal Engine 5 source build
  vcs: git with worktrees
---

## 지침

엔진 소스, 엔진 이력, 엔진 수정 표시를 읽기 전에 프로젝트가 실제로 쓰는 엔진 버전이 어느 체크아웃에 있는지 확인한다.

1. 환경 변수가 가리키는 경로에서 `git worktree list`를 실행한다. 릴리스 브랜치가 다른 worktree에 있을 수 있다.
2. `Engine/Build/Build.version`이 있는지, 그 메이저와 마이너 버전이 프로젝트가 밝힌 버전과 같은지 확인한다.
3. `git status`와 브랜치를 확인한다. 이력이 아주 짧거나 스테이징된 삭제가 대량인 기본 브랜치는 엔진 소스가 아니다.
4. 프로젝트가 레지스트리 GUID(`.uproject`의 `EngineAssociation`)로 엔진을 지정하면, 환경 변수를 빌드 입력으로 가정하기 전에 GUID를 경로로 풀어 본다.

그다음에 엔진에서 수정 표시나 렌더러 변경을 검색한다.

## 적용 범위와 예외

경로나 레지스트리 연결로 커스텀 엔진을 찾는 모든 프로젝트에 해당한다. 런처로 설치한 엔진은 잘못 읽을 git 이력이 없으므로 해당하지 않는다. worktree 구성은 원인 중 하나이며, 릴리스별 엔진 클론 여러 개가 나란히 있는 경우도 같은 문제를 만든다.

## 점검

- `git worktree list`에 경로가 둘 이상 나오면 읽기 전에 어느 쪽이 릴리스 브랜치인지 정한다.
- `Engine/Build/Build.version`이 없으면 쓸 수 있는 엔진 트리가 아니다.
- 현재 브랜치의 커밋 수가 엔진치고 터무니없이 적으면(수십만이 아니라 수십) 잘못된 브랜치다.
- 수정 표시 검색(예: `*_ENGINE_MODIFIED` 매크로)은 특정 모듈 디렉터리로 좁히거나 `git log -- <경로>`를 쓴다. Windows에서 `Engine/Source` 전체 재귀 grep은 5분을 넘겼다.

## 근거

Windows의 UE 5.8 게임 프로젝트에서 한 번 관찰했다(2026-11-05, 2026-11-06 재확인). 엔진 환경 변수가 기본 브랜치 체크아웃을 가리켰고, 커밋 22개, 스테이징된 삭제 약 148,000개, `Build.version` 없음 상태였다. `git worktree list`를 보니 릴리스 브랜치가 옆 worktree에 있었고 거기에 `Build.version` 5.8과 스튜디오의 엔진 수정이 있었다. 처음 읽은 엔진 이력은 오래된 체크아웃에서 나온 것이었고 worktree 확인 뒤 바로잡았다.

검증하지 않은 것: 레지스트리 `EngineAssociation` GUID가 두 경로 중 어디로 풀리는지, 빌드 스크립트가 환경 변수와 레지스트리 중 무엇을 쓰는지.
