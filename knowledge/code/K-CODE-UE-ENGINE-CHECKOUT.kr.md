# 사용 중인 언리얼 엔진 소스 체크아웃 확인하기

항목 `K-CODE-UE-ENGINE-CHECKOUT` · 상태 활성 · 확인일 2026-11-06

검색어 Unreal Engine, custom engine, engine fork, git worktree, Build.version, EngineAssociation, engine source, stale checkout

## 지침

환경 변수가 가리키는 경로에서 `git worktree list`를 실행해 같은 저장소의 작업 트리와 브랜치를 확인한다. `Engine/Build/Build.version`의 주·부 버전, 현재 커밋·상태, 빌드 또는 실행 스크립트가 실제로 선택한 UnrealEditor.exe를 대조한다. .uproject의 `EngineAssociation`이 GUID이면 현재 사용자의 등록 경로도 해석한 뒤 엔진 이력이나 수정 사항을 조사한다.

## 적용 범위와 예외

Windows에서 경로나 등록 GUID로 선택하는 소스 빌드·포크에 적용한다. 여러 클론과 연결 작업 트리가 공존할 수 있다. 런처 설치본에는 같은 방식으로 볼 Git 이력이 없다.

## 점검

Build.version, 실행 파일, 요구한 커밋을 확인한다. 브랜치 이름, 짧은 이력 또는 많은 스테이징 삭제만으로 판단하지 않는다. 얕은 클론일 수도 있다. GUID가 HKCU의 Software/Epic Games/Unreal Engine/Builds에 없으면 그 위치에서 연결을 확인할 수 없다. 등록 스크립트가 같은 경로의 다른 GUID를 제거하는 경우 그 GUID를 쓰는 로컬 프로젝트를 먼저 확인한다. 필요하면 기존 GUID를 유지하고 새 연결만 더하는 방법을 검토한다. 수정 검색은 대상 모듈이나 `git log -- <paths>`로 제한한다.

## 근거

2026-11-05~06 Windows UE 5.8 사례에서는 불완전한 체크아웃과 필요한 에디터를 보유한 연결 작업 트리가 달랐고 프로젝트 연결과 사용자 등록도 일치하지 않았다. 경로 점검으로 이력 해석을 바로잡았다. 재등록부터 실제 실행까지는 재검증하지 않았다. [Git worktree manual](https://git-scm.com/docs/git-worktree)
