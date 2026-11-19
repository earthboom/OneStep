# 큰 바이너리 충돌을 희소 연결 작업 트리에서 해결하기

항목 `K-CODE-GIT-ISOLATED-MERGE` · 상태 활성 · 확인일 2026-11-06

검색어 git merge, git merge-tree, git worktree, sparse-checkout, GIT_LFS_SKIP_SMUDGE, LFS pointer conflict, binary conflict, generated code, protoc, core.autocrlf, EOL drift, MERGE_MSG, cleanup=verbatim, merge commit

## 지침

git merge-tree --write-tree --name-only <ours> <theirs>로 충돌 목록을 미리 구하고 전체 출력에서 공통 조상·양쪽 블롭을 확인한다. 기본 작업 트리와 인덱스에는 변경이 없다. git worktree add -b로 별도 작업 트리를 만들고 git sparse-checkout set --cone에 충돌과 재생성에 필요한 디렉터리를 포함한다. GIT_LFS_SKIP_SMUDGE=1로 LFS 객체는 포인터로 둔다.

별도 트리에서 git merge --no-ff --no-commit 후 충돌 목록을 대조한다. 바이너리는 git log와 git rev-parse로 양측 블롭과 후속 변경 의도를 살핀다. 독립적인 양쪽 편집은 사람에게 남긴다. protobuf 등 생성물은 각 커밋 원본에서 재생성해 기존 출력과 동등한지 확인한 뒤 병합 원본에서 다시 만든다. core.autocrlf=true 환경에서는 정규화된 diff로 단순 개행 차이를 확인해 해당 파일만 되돌린다. 순서만 바뀐 경우 언어나 생성기 계약에서 순서가 무관한지도 확인한다. 병합 메시지에 원래 제목과 충돌 목록, 파일별 판단을 남긴다. git commit --cleanup=verbatim은 # Conflicts 행을 보존한다. 사람의 판단이 필요한 충돌은 실제로 해결하기 전 커밋하지 않는다.

## 적용 범위와 예외

대용량 바이너리·LFS가 있고 편집기가 열린 기본 작업 트리를 유지해야 하는 경우다. 희소 범위에 필요한 모든 생성기 입력이 있어야 한다. merge.lfs 드라이버가 없으면 포인터 충돌에서 선택한 쪽을 체크아웃하고 스테이징한다. 현지화 데이터는 [의미 단위 병합 방법](K-CODE-UE-LOC-MERGE.md)을 참조한다.

## 점검

예측·실제 충돌 목록, 선택한 바이너리와 인덱스 블롭, 생성 결과와 스테이징된 원본의 일치를 확인한다. 보류 중에는 해결하지 않은 경로를 명확히 하고 커밋 전에는 미병합 경로가 없어야 한다. 작업 트리의 비의도 변경과 기본 체크아웃 상태도 확인한다.

## 근거

2026-11-06 Windows UE5 게임 저장소에서 미리보기와 실제 충돌 집합이 일치했다. 이력 및 재생성으로 바이너리와 개행·순서 차이를 구분했고, 독립된 양쪽 바이너리 변경은 사람의 결정으로 남겼다. 커스텀 LFS 드라이버와 Git 2.38 미만은 미검증이다. [Git, merge-tree](https://git-scm.com/docs/git-merge-tree/2.45.0.html) · [Git, worktree](https://git-scm.com/docs/git-worktree)
