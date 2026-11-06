---
id: K-CODE-GIT-ISOLATED-MERGE
title: 메인 체크아웃을 건드리지 않고 sparse 연결 worktree 에서 대규모 브랜치 머지 해소하기
summary: git merge-tree 로 드라이런해 충돌 목록과 단계 blob 을 얻은 뒤, 충돌 디렉터리만 cone sparse 체크아웃한 연결 worktree 에서 LFS smudge 를 끄고 실제 머지를 진행한다. 바이너리/생성물 충돌은 이력과 재생성으로 결정하고, 재생성의 EOL 전용 드리프트는 인덱스에 넣지 않는다.
kind: method
scope: 메인 작업 트리를 건드릴 수 없는(열린 에디터, 잠긴 파일, checkout 금지 규칙) 상태에서 충돌이 많은 머지를 해소해야 하는 대용량 바이너리/LFS git 저장소
keywords: [git merge, git merge-tree, git worktree, sparse-checkout, GIT_LFS_SKIP_SMUDGE, LFS pointer conflict, binary conflict, generated code, protoc, core.autocrlf, EOL drift, MERGE_MSG, cleanup=verbatim, merge commit]
status: active
checked_at: "2026-11-06"
context:
  vcs: git 2.x + git-lfs
  platform: Windows (core.autocrlf=true)
---

## Guidance

1. 드라이런 먼저: `git merge-tree --write-tree --name-only <ours> <theirs>` 는 어떤 트리도 건드리지 않고 충돌 경로를 나열하고, 전체 출력은 경로별 base/ours/theirs blob id 를 준다. 둘 다 저장한다. 이후 작업의 기준이다.
2. 연결 worktree 에 머지 브랜치를 만든다: `git worktree add -b <merge-branch> <dir> <ours>`, 그리고 `git sparse-checkout set --cone <충돌 디렉터리들>` 로 충돌이 있는 디렉터리(와 재생성 도구가 필요로 하는 것)만 실체화한다. 거기서 모든 git 명령에 `GIT_LFS_SKIP_SMUDGE=1` 을 적용해 LFS 파일은 포인터로 둔다.
3. worktree 에서 `git merge --no-ff --no-commit <theirs>` 를 실행한다. 충돌 집합이 드라이런과 같아야 하며, 다르면 멈춘다.
4. 바이너리/LFS 충돌은 기본값으로 한쪽을 고르지 말고 이력으로 결정한다: 경로를 바꾼 커밋들에서 양쪽 blob id 를 비교한다(`git log <base>..<side> -- <path>`, `git rev-parse <commit>:<path>`). 한쪽 변경이 상대편에 이미 있는 커밋과 바이트 동일하면 단순 재저장이므로 상대편의 더 나중 저장본이 이긴다. 한 에셋에 대한 서로 무관한 두 변경은 사람 결정으로 남기고 양쪽 티켓, 작성자, 날짜를 함께 나열한다.
5. 생성물(protobuf 코드, 컴파일 데이터)은 병합하지 말고 자동 병합된 소스에서 재생성한다. 생성기를 믿기 전에 각 측의 커밋 생성물을 그 측의 소스로 재생성해 줄끝 무시 동일을 요구한다.
6. `core.autocrlf=true` 에서 LF 로 쓰는 생성기는 모든 출력을 수정된 것처럼 보이게 하지만 정규화 diff 는 비어 있다. 파일별 `git diff --quiet -- <file>`(정규화)로 분류하고 EOL 전용 파일은 `git checkout -- <file>` 로 복원하며, 정규화 내용이 바뀐 파일만 스테이징한다. 입력을 정렬 없는 디렉터리 나열로 열거하는 생성기는 블록 전체를 재배치할 수도 있다: 추가/삭제 줄을 멀티셋으로 비교해 순수 재배치는 변경 없음으로 본다.
7. 머지 커밋 메시지는 `.git/worktrees/<name>/MERGE_MSG`(또는 `.git/MERGE_MSG`)에 쓴다: git 의 제목과 `# Conflicts:` 블록은 그대로 두고 경로별 해소 노트를 덧붙이며, 블록이 살아남도록 `git commit --cleanup=verbatim` 으로 커밋한다. 아직 사람 판단이 필요한 경로는 노트에 미결로 표시해 누가 그냥 커밋하지 않게 한다.
8. 커밋 전: 의도적으로 남긴 경로 외에 unmerged 없음, worktree `git status` 에 스테이징 안 된 드리프트 없음, 재생성되거나 의미 병합된 모든 산출물에 독립 검증 기록 있음.

## Applicability and exceptions

충돌 수나 크기 때문에 메인 체크아웃에서의 머지가 안전하지 않을 때 적용한다. sparse 집합에는 재생성 도구가 읽고 쓰는 모든 디렉터리가 포함돼야 하며, 아니면 도구가 부분 트리에서 돈다. 도구 실행 전에 sparse 집합을 넓힌다. `merge.lfs` 드라이버가 없으면 LFS 충돌은 포인터 줄의 텍스트 충돌로 보이며, 편집이 아니라 `git checkout --ours|--theirs -- <path>` 후 `git add` 로 해소한다. 데이터 파일의 의미 병합은 별도 방법이 있다(Unreal 로컬라이즈 파일은 K-CODE-UE-LOC-MERGE).

## Checks

- 드라이런 충돌 목록 == 실제 머지 충돌 목록.
- 한쪽으로 해소한 모든 바이너리 경로에서 인덱스 blob == 그 측 blob (`git ls-files -s`).
- 모든 재생성 출력에서 스테이징된 소스로 재생성하면 CR 무시 시 스테이징 blob 과 일치.
- worktree 의 `git status --short` 에는 의도적으로 미룬 경로의 `UU` 와 스테이징 항목의 `M `/`A ` 만 있고, 재생성 후 ` M`, `MM`, `??` 가 없음.
- 메인 체크아웃의 `git status` 가 전체 절차 동안 변하지 않음.

## Evidence

2026-11-06 UE5 게임 저장소의 37충돌 머지(양측 824/134 커밋)에서 메인 체크아웃이 Excel 로 스프레드시트를 열어 둔 상태로 사용. 드라이런과 worktree 머지가 같은 37경로를 냈다. 맵 에셋 1개는 이력으로 결정(상대편 저장본이 main 에 이미 있는 커밋과 바이트 동일, main 이 이후 재저장); protobuf 출력 4개는 재생성했고 각 측 proto 로 재생성 시 각 측 커밋 출력과 일치; 재생성 파일 216개는 줄끝만 달라 복원; 생성 C++ 2개는 정렬 없는 나열 때문에 struct 블록만 재배치. 서로 무관한 바이너리 에셋 변경 3건은 사람 결정으로 남김. 출처 프로젝트 세부는 생략.

미검증: `merge.lfs` 드라이버가 설정된 저장소, `merge-tree --write-tree`(git 2.38 추가)가 없는 git 버전.
