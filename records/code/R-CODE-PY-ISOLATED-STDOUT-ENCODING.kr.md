# R-CODE-PY-ISOLATED-STDOUT-ENCODING

사람이 읽는 번역본이다. 기준 문서는 영어 원문 `R-CODE-PY-ISOLATED-STDOUT-ENCODING.md`다.

- **제목:** 격리 모드로 실행한 파이썬 스크립트에서 PYTHONIOENCODING 이 듣지 않음
- **요약:** `python -I` 에서는 인터프리터가 `PYTHON*` 환경 변수를 무시한다. 그래서 표준 출력이 Windows 콘솔 코드 페이지에 머물고, 그 코드 페이지에 없는 글자에서 UnicodeEncodeError 가 난다. 명령줄 옵션 `-X utf8` 로 UTF-8 을 고르거나, 결과를 UTF-8 파일로 쓴다.
- **종류:** error
- **범위:** 콘솔 코드 페이지가 UTF-8 이 아닌 Windows 의 CPython, `-I` 또는 `-E` 로 시작한 스크립트
- **상태:** resolved
- **확인 날짜:** 2026-11-24
- **환경:** Windows 11, 콘솔 코드 페이지 949, Python 3.12.3
- **발생 조건:** `python -I` 로 시작한 스크립트에서 ASCII 가 아닌 글자를 출력할 때. 예를 들어 내려받은 데이터나 신뢰할 수 없는 데이터를 격리 모드로 읽을 때
- **증상:** 명령 앞에 `PYTHONIOENCODING=utf-8` 을 붙였는데도 `UnicodeEncodeError: 'cp949' codec can't encode character` 가 나거나, 받은 출력의 글자가 깨짐
- **원인 확신도:** confirmed
- **예방:** `-I` 나 `-E` 를 쓸 때는 출력 인코딩을 명령줄(`-X utf8`)에서 고르거나, 인코딩을 UTF-8 로 명시해 연 파일에 결과를 쓴다. `PYTHON*` 환경 변수에 기대지 않는다
- **예방 상태:** verified

## 기대와 관찰

한글과 긴 줄표가 든 JSON 을 요약하는 스크립트를, 데이터 폴더의 코드를 불러오지 않도록 `python -I` 로 실행했다. 명령 앞에 `PYTHONIOENCODING=utf-8` 을 붙이면 `print` 가 UTF-8 로 내보낼 것으로 기대했다. 실제로는 받은 출력이 깨졌고 스크립트가 `UnicodeEncodeError: 'cp949' codec can't encode character '—'` 로 멈췄다. 환경 변수를 붙인 뒤에도 같은 오류가 나서 실행을 한 번 더 버렸다.

## 원인과 해결

격리 모드(`-I`)는 `-E` 를 포함한다. `-E` 는 `PYTHONIOENCODING`, `PYTHONUTF8` 을 포함한 모든 `PYTHON*` 환경 변수를 무시하게 한다. 그래서 표준 출력이 콘솔 코드 페이지 인코딩을 그대로 썼다. 해당 PC 에서 확인했다. `PYTHONIOENCODING=utf-8 python -I -c "import sys; print(sys.stdout.encoding, sys.flags.ignore_environment)"` 가 `cp949 1` 을 출력했다.

작업에서 쓴 해결: 스크립트가 요약을 `encoding='utf-8'` 로 연 파일에 쓰고, 그 파일을 나중에 읽었다. 격리 모드에서도 명령줄 옵션은 그대로 적용되므로 `-X utf8` 이 직접적인 대안이다.

## 재확인과 예방

2026-11-24 에 한글을 넣은 `python -I -X utf8 -c "import sys; print(sys.stdout.encoding); print('— ...')"` 가 `utf-8` 과 기대한 UTF-8 바이트를 오류 없이 출력했다(`od -c` 로 확인). 파일로 쓰는 방식도 같은 세션에서 읽을 수 있는 UTF-8 요약을 만들었다.

격리 옵션이 필요하고 출력에 콘솔 코드 페이지 밖의 글자가 있을 때 적용한다. `-I` 나 `-E` 가 없으면 환경 변수가 문서대로 동작하므로 이 기록은 해당하지 않는다. 스크립트 안에서 `sys.stdout.reconfigure(encoding='utf-8')` 를 부르는 것도 가능해 보이지만 여기서 실행해 보지는 않았다.

## 근거

- 세션 관찰, 2026-11-24, 콘솔 코드 페이지 949 인 Windows 11 의 Python 3.12.3: 위에 적은 실패 실행, `cp949 1` 확인, `-X utf8` 통과 실행.
- [파이썬 명령줄 문서, -I 옵션](https://docs.python.org/3/using/cmdline.html#cmdoption-I): 격리 모드는 `-E` 를 포함한다. [-E 옵션](https://docs.python.org/3/using/cmdline.html#cmdoption-E): 모든 `PYTHON*` 환경 변수를 무시한다. [-X utf8 옵션](https://docs.python.org/3/using/cmdline.html#cmdoption-X): UTF-8 모드를 켠다. 이 세션에서 문서 페이지를 다시 받아 보지는 않았고, 확인한 근거는 로컬 실행 결과다.
