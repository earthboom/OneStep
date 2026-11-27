# 피드백: link_project.py 가 Git 으로 추적되는 팀 지침 파일에 규칙 블록을 쓴다

- 날짜: 2026-11-26
- 사용한 OneStep 버전: 99cd60c (2026-11-26)
- 관련 스킬/지침: `link_project.py`, 사용자 수준 "Connect this project" 지침
- 종류: problem
- 상태: received
- 작업 맥락: `AGENTS.md` 와 `CLAUDE.md` 가 Git 으로 추적되는 팀 지침인 공용 게임 저장소. 사용자는 이미 Git 에서 제외된 개인 파일(`CLAUDE.local.md`)로 OneStep 을 불러오고 있고, 그 파일은 OneStep 설정을 `AGENTS.md`, `CLAUDE.md` 등 추적 파일에 넣지 말라고 정한다. 사용자가 프로젝트 연결을 요청했다.

## 기대와 관찰

기대: 개인용, 로컬 전용으로 OneStep 을 쓰는 프로젝트를 연결해도 추적되는 팀 파일은 그대로 두거나 로컬 전용 모드를 제공하고, `--check` 가 그 연결을 확인할 수 있다.

관찰(AI): `link_project.py <project>` 가 "5 files updated" 를 출력했다. 추적되는 `AGENTS.md` 와 `CLAUDE.md` 끝에 `onestep:checkout` 블록을 붙였고, 추적되지 않는 `GEMINI.md` 와 `.onestep/`(`checkout.local.json` 용 `.gitignore` 포함)를 만들었다. 이어서 `--check` 는 통과했다. 사용자 요청에 따라 AI 가 `AGENTS.md` 와 `CLAUDE.md` 를 되돌리고 `/.onestep/` 와 `/GEMINI.md` 를 `.git/info/exclude` 에 넣었다. 그 뒤로 `--check` 는 "Connection differs from this checkout. Rerun the same command without --check." 로 실패한다. 포인터 파일은 그대로이고 OneStep 은 개인 파일로 계속 불러와진다.

영향: 공용 저장소에서 연결하면 실수로 커밋될 수 있는 팀 지침 diff 가 남거나, 프로젝트 규칙을 지키려고 되돌리면 `--check` 로 연결을 확인할 수 없다. 오류 문구대로 다시 실행하면 원치 않는 수정이 다시 들어간다.

## 근거와 추정 원인

- `link_project.py` 145행이 `entry_files = ["AGENTS.md", "CLAUDE.md", "GEMINI.md"]` 로 고정하고, 149-153행이 각 파일에 규칙을 합치며, 165-167행은 그중 하나라도 블록이 없으면 `--check` 를 실패시킨다.
- 로컬 파일이나 Git 제외 파일을 진입 파일로 고르는 옵션이 없다(`--help` 에는 `--register` 와 `--check` 만 있다).
- 사용자 지침 "Connect this project" 는 적힌 대로 따랐다. 충돌은 지침 이탈이 아니라 프로젝트의 로컬 규칙에서 생겼다.
- 확인하지 않음: 되돌린 뒤 이 프로젝트에서 Codex 나 Gemini 세션의 동작.

## 개선 제안

로컬 전용 모드(예: `--local`)를 추가해 `CLAUDE.local.md` 나 `AGENTS.override.md` 같은 Git 제외 진입 파일에 규칙을 쓰고, 만든 파일을 `.git/info/exclude` 에 넣고, `--check` 가 그 구성을 받아들이게 한다. 또는 추적되는 진입 파일을 감지해 수정 전에 묻는다. 점검: 추적되는 `AGENTS.md`/`CLAUDE.md` 가 있는 저장소에서 로컬 모드로 연결한 뒤 `git status` 에 추적 파일 변경이 없고 `--check` 가 0 으로 끝난다.

## 검토와 검증

메인테이너가 처리하면서 채운다.
