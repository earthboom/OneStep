# C++ 가이드 라우팅 평가

> 사람이 읽는 한국어 번역본이다. 실행 지침의 정본은 영문 `README.md`다.

OneStep의 C++ 작업 흐름이나 구현 가이드를 바꾼 뒤 실행한다. 독립 에이전트가 합성 프로젝트에 연결해 실제 코드를 수정하는 동안 어떤 문서를 읽는지 확인한다. 판단과 증거를 검토할 때는 [기존 블라인드 평가 방법](../../../vegabond-knowledge/tests/information-needs/evaluation.kr.md)을 따른다.

## 준비와 실행

1. OneStep 체크아웃에서 `python skills/vegabond-code/tests/cpp-routing/run.py prepare`를 실행한다. 필요하면 `--parent`로 체크아웃 밖의 쓰기 가능한 기존 디렉터리를 지정한다. 이 명령은 프로젝트 4개를 따로 만들고 각 프로젝트의 기존 지침에 `link_project.py`로 OneStep을 연결한다.
2. 독립 에이전트에게 해당 프로젝트 경로와 `request.md`의 내용만 준다. 프로젝트의 `AGENTS.md`부터 시작하고, 해당 디렉터리에서 `python read_doc.py <path>`로 마크다운을 읽으며, 실제로 실행한 검사와 제한을 보고하도록 한다. `--outline`으로 목차를, `--section "heading"`으로 특정 섹션을 읽을 수 있다. 채점 기준, 다른 사례, 이전 결과는 실행 문맥 밖에 둔다.
3. `python skills/vegabond-code/tests/cpp-routing/run.py check <run-directory>`를 실행한다. 기록된 문서 읽기를 고정된 채점 기준과 비교하고, 준비 이후 지침이나 평가 입력이 바뀌면 다시 준비하도록 한다. 출력된 검토 기준으로 패치와 실제 검증 결과를 따로 확인한다.

## 실행 가능한 검사와 증거

- 순수 C++ 사례는 수정 전후에 `check.cpp`를 C++17로 컴파일하고 실행한다. Unix 계열에서는 `c++ -std=c++17 check.cpp -o route-check`와 `./route-check`를 사용한다. MSVC 개발자 명령 프롬프트에서는 `cl /nologo /std:c++17 /EHsc check.cpp /Fe:route-check.exe`와 `route-check.exe`를 사용한다. 컴파일과 실행 종료 상태를 각각 기록한다. 소유권 사례의 제공된 검사는 호출자의 데이터 변경을 재현한다. 컴파일러를 쓸 수 있다면 수정 후 호출자 데이터의 소멸도 단언문으로 확인한다.
- Python 사례는 수정 전후에 해당 프로젝트의 `AGENTS.md`에 있는 명령을 사용한다. `.uproject`와 Unreal 코드가 수정 범위 밖인지 확인한다.
- Unreal 소유권 사례에는 소스만 들어 있다. 약한 참조, 조회 함수, 공개 API를 확인한다. 별도로 적절한 엔진 프로젝트를 준비하지 않았다면 컴파일과 실행은 미검증으로 표시한다.

실행 목록, 읽기 기록, 패치 검토, 실행 결과를 함께 보관한다. 읽기 도구는 자신이 반환한 문서 부분을 기록한다. 이 평가는 독립 문맥에서 네 사례를 표본으로 검증하며, 변경 후 다시 실행할 수 있다. 전략에 실제 문제가 확인되면 [기존 피드백 절차](../../../../feedback/README.kr.md)를 따른다.
