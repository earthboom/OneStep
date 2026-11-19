# 여러 프로젝트에서 OneStep 폴더 하나 참조하기

## 다른 프로젝트 세션에서 말로 연결하기

OneStep을 clone한 뒤 해당 폴더에서 PC마다 한 번 `py -3 link_project.py --register`를 실행합니다. macOS·Linux에서는 `python3 link_project.py --register`를 씁니다. Codex·Claude Code·Gemini CLI의 개인 지침에 이 PC의 체크아웃 위치와 요청 처리 방법이 등록됩니다. 이후 원하는 프로젝트에서 **새 로컬 세션**을 열고 평소처럼 요청하세요.

- **“이 프로젝트를 OneStep에 연결하고 전투 시스템을 검토해줘.”** 에이전트가 현재 프로젝트를 연결하고 `--check`로 확인한 뒤 같은 세션에서 검토를 시작합니다. 다음 세션도 연결을 이어받습니다.
- **“이번 검토에만 OneStep 써줘.”** 에이전트가 공유 지침과 Scout를 읽어 현재 작업에 적용합니다. 프로젝트 설정은 바뀌지 않습니다.

`--register --check`로 개인 지침 등록을 확인할 수 있습니다. 체크아웃을 옮기면 새 위치에서 등록 명령을 다시 실행합니다. 이미 열려 있던 세션에서는 OneStep의 전체 경로와 원하는 작업을 함께 알려주면 바로 시작할 수 있습니다. 웹 채팅은 아래의 자료 연결 방식을 사용합니다.

PC마다 편한 폴더에 OneStep을 한 번 복제합니다. 게임·소설·문서 프로젝트마다 연결 명령을 한 번 실행합니다. 다음은 두 폴더의 상위 폴더에서 실행하는 Windows 예시입니다.

```powershell
git clone https://github.com/earthboom/OneStep.git OneStep
py -3 OneStep/link_project.py "내 게임"
py -3 OneStep/link_project.py "내 소설"
py -3 OneStep/link_project.py "내 게임" --check
```

macOS·Linux에서는 `py -3` 대신 `python3`를 씁니다. 대상 프로젝트는 이미 존재하는 폴더여야 하며, 다른 드라이브의 절대 경로도 지정할 수 있습니다. 연결 도구는 Python 3.8 이상과 표준 라이브러리를 사용합니다. 연결한 뒤 작업 프로젝트에서 새 AI 세션을 열고, OneStep 폴더를 읽을 수 있는지 확인합니다.

**자동 참조가 시작되는 지점**은 대상 프로젝트의 `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`입니다. 연결 명령이 기존 지침을 보존하면서 OneStep 블록을 추가하고, 내용이 있는 `AGENTS.override.md`에도 반영합니다. 도구의 지침 파일명을 직접 바꾼 경우에는 같은 블록을 그 파일에 추가합니다. 이전 ZIP의 기본 지침은 자동 전환합니다. 직접 수정해 둔 ZIP 지침은 새 블록과 충돌하는 경로를 편집기로 정리합니다.

새 작업을 받으면 AI는 공유 폴더에서 공통 지침과 Scout를 읽고 필요한 스킬을 선택합니다. 게임 작업에서는 현재 프로젝트 자료를 먼저 보고, 공유 폴더의 게임·코드 지식과 문제 기록을 조회합니다. 예를 들어 “보간이 끝났는데 컴포넌트 위치가 목표와 조금 달라. TVector::Equals 관련 문제 기록 ID와 이유를 찾아줘”라고 요청해 보세요. 읽은 파일과 답변에 `R-CODE-UE-TRANSFORM-TOLERANCE`가 있는지 확인할 수 있습니다. 작업 결과물과 프로젝트 고유 데이터는 해당 프로젝트에서 관리합니다.

**다른 PC**에서는 작업 프로젝트의 시작 지침 파일과 `.onestep/.gitignore`를 Git으로 공유합니다. PC별 경로인 `.onestep/checkout.local.json`은 Git에서 제외합니다. 작업 프로젝트 바로 옆에 `OneStep`이라는 이름으로 복제하면 시작 지침이 `../OneStep`을 찾습니다. 다른 위치에 받거나 OneStep 폴더를 옮겼다면 그 체크아웃에서 연결 명령을 다시 실행합니다. `--check`는 파일을 수정하지 않고 연결 상태를 검사합니다.

**갱신**할 때는 상위 폴더에서 `git -C OneStep pull --ff-only`를 한 번 실행합니다. 연결된 프로젝트들은 다음 새 세션에서 같은 폴더의 갱신본을 읽습니다. 현재 PC에서는 커밋 전 로컬 수정도 보이며, 다른 PC는 원격 저장소에 올라간 커밋을 받습니다.

**웹 채팅**에는 서비스가 읽을 수 있는 자료를 연결합니다. GitHub 접근을 지원하는 ChatGPT 환경에서는 저장소를 허용하고 프로젝트 지침에 이 저장소의 `agents/vegabond-agent.md`와 `skills/vegabond-scout/SKILL.md`를 읽도록 지정할 수 있습니다. ChatGPT 프로젝트나 Gemini Gem에 `portable/OneStep-Web.txt`를 올리는 경우에는 업데이트할 때 파일을 교체합니다. [웹 설정](../portable/README.kr.md) · [ChatGPT의 GitHub 접근 안내](https://help.openai.com/en/articles/11145903-connecting-github-to-chatgpt)
