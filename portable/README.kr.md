# 다른 게임 프로젝트에서 OneStep 사용하기

## 로컬 프로젝트

1. [OneStep-Project.zip](OneStep-Project.zip)을 별도 폴더에 풉니다.
2. 게임 프로젝트 최상위 폴더에 `onestep-strategy` 폴더와 사용할 AI의 지침 파일을 함께 복사합니다. Claude Code는 `CLAUDE.md`, Codex는 `AGENTS.md`, Gemini CLI는 `GEMINI.md`를 사용합니다. 기존 지침이 있으면 배포본의 문구를 끝에 추가합니다. 사용자 지정 지침이나 `AGENTS.override.md`를 쓰면 실제 활성 파일에 추가합니다.
3. 게임 프로젝트에서 새 AI 세션을 엽니다. “OneStep에서 `TVector::Equals` 관련 문제 기록을 찾아줘. 보간 계산은 끝났는데 컴포넌트 위치가 목표와 조금 다른 이유와 우리 게임에서 확인할 검사를 기록 ID와 함께 설명해줘”라고 요청해 적용 여부를 확인할 수 있습니다.

압축 해제와 복사에는 프로젝트 쓰기 권한이 필요합니다. 지침 파일과 전략 폴더를 함께 이동하거나 버전 관리하면 다른 PC에서도 같은 상대 경로를 씁니다.

세 기본 지침을 자동으로 병합하려면 압축을 푼 폴더에서 Python 3.8 이상으로 실행합니다. 따옴표 안은 실제 대상 폴더로 바꿉니다.

```powershell
py -3 install.py "D:\Work\내 프로젝트"
```

```sh
python3 install.py "$HOME/Work/내 프로젝트"
```

같은 버전은 다시 설치해도 UTF-8 지침을 중복 추가하지 않습니다. 기존 배포본을 교체할 때는 먼저 이전 `onestep-strategy` 폴더를 별도로 옮기고 새 버전을 설치한 다음, 자신의 수정 사항을 확인합니다. 다른 인코딩을 쓰는 지침은 편집기로 문구를 추가합니다.

## ChatGPT 프로젝트와 Gemini Gem

[OneStep-Web.txt](OneStep-Web.txt)를 ChatGPT의 프로젝트 자료 또는 Gemini Gem의 Knowledge에 올립니다. 이전 파일을 올려 둔 프로젝트에서는 새 파일로 교체합니다. 프로젝트나 Gem의 지침에 다음 문구를 넣습니다.

> 새 작업마다 OneStep-Web.txt의 agents/vegabond-agent.md와 skills/vegabond-scout/SKILL.md부터 적용한다. 게임 작업은 현재 프로젝트의 자료를 우선하고, 배포본의 게임·코드·문제 기록 색인에서 키워드로 찾아 해당 ID의 상세 본문과 근거를 확인한다. 실행하지 못한 검사는 따로 밝힌다.

## 키워드로 찾기

게임 기법과 장르 설계는 `knowledge/game/index.md`, 언리얼·C++와 도구 사용은 `knowledge/code/index.md`, 증상·원인·재발 방지는 `records/code/index.md`에서 시작합니다. 로컬에서는 `onestep-strategy/` 안의 파일이고, 웹에서는 같은 이름의 섹션입니다. 정식 API 이름, 영어·한국어 용어 또는 증상을 검색한 다음 상세 항목의 적용 범위, 검사와 Evidence를 확인합니다. 색인에 없는 표현은 본문이나 동의어로도 찾을 수 있습니다. 과거 실험의 상세 파일은 원래 프로젝트에 있으며 배포본에는 출처 식별자와 검증 범위가 있습니다.

파일을 직접 읽는 데 추가 도구는 필요 없습니다. Python 3.9 이상과 PyYAML이 있으면 게임 프로젝트 최상위 폴더에서 다음 명령으로 배포본의 지식과 문제 기록을 함께 검색할 수 있습니다.

```text
python onestep-strategy/skills/vegabond-knowledge/scripts/search.py search --project onestep-strategy --query "메모리 풀링" --portable-library
```

## 배포본 갱신

배포할 원문 목록은 `portable/game-library.txt`에서 관리합니다. 항목이 바뀌면 영문 카탈로그를 갱신한 뒤 Python과 PyYAML이 있는 환경에서 `python portable/build.py`, `python portable/test_portable.py`를 차례로 실행합니다. 생성된 ZIP과 웹용 텍스트 파일을 배포합니다.
