# 하위 .gitignore 의 부정 규칙이 다시 포함시킨 경로를 로컬에서만 Git 에서 빼기

ID: K-CODE-GIT-LOCAL-IGNORE-PRECEDENCE
종류: reference
상태: active, 확인일 2026-11-25
범위: 커밋된 .gitignore 가 디렉터리(예: 공용 도구나 스킬 폴더)를 다시 포함시키는데, 한 사용자가 그 안의 개인 하위 폴더를 커밋에서 빼야 하는 Git 작업 트리
조건: git 2.45.1.windows.1, Windows

요약: `$GIT_DIR/info/exclude` 의 패턴은 작업 트리 안 `.gitignore` 의 `!dir/**` 같은 부정 규칙에 져서, 그 경로는 추적되지 않은 파일로 계속 보인다. 로컬 제외 줄은 부정 규칙이 있는 같은 `.gitignore` 의 부정 줄 뒤에 넣고, `git check-ignore -v` 로 확인할 때는 종료 코드가 아니라 출력된 패턴을 읽는다.

## 지침

Git 은 여러 곳의 무시 패턴을 정해진 우선순위로 읽는다. 작업 트리 안 `.gitignore` 가 `$GIT_DIR/info/exclude` 보다 우선하고, `info/exclude` 가 `core.excludesFile` 보다 우선한다. 같은 수준에서는 마지막에 맞은 패턴이 이기고, 더 아래 폴더의 `.gitignore` 가 위 폴더의 것보다 우선한다.

그래서 커밋된 `.gitignore` 에 `*`, `!skills/`, `!skills/**` 가 있으면 `info/exclude` 에 `sub/skills/mine/` 을 넣어도 효과가 없다. 부정 규칙이 그 경로를 다시 포함시킨다. 개인 폴더를 로컬에만 두려면:

1. 부정 규칙이 있는 같은 `.gitignore` 에서 부정 줄 뒤에 제외 줄(예: `skills/mine/`)을 넣는다.
2. 이 `.gitignore` 수정도 작업 트리 변경이다. 커밋하지 않고 두거나, 팀이 그 규칙을 커밋하기를 원하는지 묻는다. `git update-index --skip-worktree` 로 `git status` 에서 숨길 수 있지만, 그 파일의 이후 상류 변경도 함께 숨긴다.
3. 그 파일을 고치기 곤란하면 우선순위와 싸우지 말고 개인 폴더를 다시 포함되는 디렉터리 밖(예: 사용자 수준 도구 디렉터리)에 둔다.

## 적용 범위와 예외

추적되지 않은 경로에 적용된다. 이미 추적 중인 파일은 무시 규칙과 상관없이 계속 추적되므로 `git rm --cached` 나 다른 방법이 필요하다. 부모 디렉터리가 제외된 파일은 부정 규칙으로 다시 포함시킬 수 없어서, `!dir/**` 는 `dir/` 자체가 다시 포함될 때(`!skills/` 처럼)만 동작한다. 연결된 워크트리들은 `info/exclude` 를 공유하지만 작업 트리 안 `.gitignore` 는 각자 따로 가지므로, 커밋하지 않은 규칙은 필요한 워크트리마다 넣어야 한다.

## 점검

- `git check-ignore -v <경로>` 를 돌려 출력된 출처와 패턴을 읽는다. 종료 코드 0 은 어떤 패턴이 맞았다는 뜻일 뿐이다. `!` 패턴에 맞았다면 그 경로는 무시되지 않는다.
- `git status --short --untracked-files=all <디렉터리>` 에 개인 파일이 더 이상 나오지 않는다.

## 근거

Git 문서 gitignore 의 "Pattern format" 절과 우선순위 목록(https://git-scm.com/docs/gitignore). 2026-11-25 git 2.45.1.windows.1 임시 저장소 재현: `sub/.gitignore` 에 `*`, `!.gitignore`, `!skills/`, `!skills/**` 를 두고 `.git/info/exclude` 에 `sub/skills/mine/` 을 넣었을 때 `git check-ignore -v` 는 `sub/.gitignore:4:!skills/**`(종료 코드 0)를 보고했고 `git status` 에 `sub/skills/mine/SKILL.md` 가 계속 나왔다. `sub/.gitignore` 에 `skills/mine/` 을 덧붙인 뒤에는 `check-ignore` 가 그 줄을 보고했고 파일이 `git status` 에서 사라졌다. 실제 프로젝트의 개인 스킬 폴더에서도 같은 결과를 봤다. 추적 중인 파일, `skip-worktree`, 다른 Git 버전은 시험하지 않았다.
