# 빌드를 다시 만들지 않고 보관된 증거 재분석하기

네 분석기는 동일한 읽기 전용 계약을 사용한다. 새 체크아웃에는 소스·프로세스 명세·원시 결과와 gzip 보관 파일이 있지만 Unity 빌드는 Git에서 제외된다. 과거 실행 파일을 재생성하지 않아도 재분석할 수 있어야 한다. 이 절차는 Unity를 실행하거나 실험을 반복하지 않는다.

```powershell
python -B ./analyze_results.py
python -B ./analyze_dynamic.py
python -B ./analyze_traffic.py
python -B ./analyze_stream.py
```

Python 3.9 이상에서 assertion을 활성화해 실행한다. 기존 소스 해시·실행 식별자·동작 검사·음성 대조군·보관 어셈블리 검사·측정 계산은 계속 필수다. 보고서가 없거나 손상되었거나 기록된 소스가 바뀌면 실패한다. 다른 SDK·게임플레이·다른 장비의 성능까지 입증하지 않는다.

## 서로 다른 검증 결과

출력 첫 JSON의 `analysis_ok: true`는 보관 자료와 소스 검사가 통과한 뒤에만 나온다. `binary_verification`은 별도 차원이며 경로별 예상·관측 SHA-256과 상태를 담는다.

| 상태 | 의미 | 기본 종료 | `--require-binaries` 사용 |
| --- | --- | --- | --- |
| `matched` | 파일이 기록된 해시와 일치 | 다른 검사도 통과하면 0 | 모든 지정 파일이 일치하면 0 |
| `missing` | 선택한 루트에 기록된 바이너리가 없음 | 0, `complete: false` | 1 |
| `mismatch` | 존재하는 파일의 해시가 다름 | 1 | 1 |
| `unavailable` | 읽을 수 없거나 실제 경로가 루트 밖으로 나감 | 1 | 1 |

`acceptable`은 바이너리 정책 통과 여부이고 `complete`는 모든 지정 파일이 일치해야 참이다. 빌드가 없을 때 종료 0은 오프라인 분석 통과를 뜻하며 과거 바이너리 확인 완료를 뜻하지 않는다. 잘못된 인수나 기존 출력 경로는 종료 2다. 원시 자료 assertion·입출력 실패는 성공 요약 없이 0이 아닌 값으로 끝난다.

바이너리 범위는 기존 대상 그대로다. 원본 실험은 플레이어 EXE, Dynamic은 관리 어셈블리, Traffic·Stream은 EXE와 관리 어셈블리다. `complete: true`도 이 경로와 명세의 일치만 뜻하며 전체 Unity 빌드·원격 실행의 신뢰성·렌더링·현재 엔진 동작을 인증하지 않는다. 실행 명세끼리 지정 바이너리 해시도 일치해야 한다. Stream의 보관된 UI 파일럿 어셈블리는 별도의 필수 역사 검사로 유지된다.

## 선택적 바이너리 검사와 결과 저장

```powershell
python -B ./analyze_traffic.py --require-binaries
python -B ./analyze_stream.py --binary-root C:/Archives/TechniqueLab --require-binaries
python -B ./analyze_stream.py --output C:/Reports/stream-analysis-new.json
```

대체 루트도 `StreamBuild/...`처럼 같은 상대 경로 구조를 사용한다. 소스나 원시 자료의 입력 위치는 바뀌지 않는다. 실제 보관 바이너리를 사용한다. 재빌드는 식별자를 바꿀 수 있어 과거 바이너리 일치 검사를 대신하지 못한다. 기본 모드도 존재하는 잘못된 바이너리를 건너뛰지 않고 실패시킨다.

기본 실행은 요약·증거 파일을 쓰지 않는다. `--output`은 부모 폴더가 존재하는 **새** 경로에 전체 JSON을 독점 생성한다. `Results/**/summary.json`을 포함한 기존 파일은 덮어쓸 수 없다. 이전의 자동 요약 덮어쓰기는 이 계약으로 대체한다. Traffic·Stream은 첫 JSON 뒤에 읽기 쉬운 측정 행을 출력하며 선택적 출력 파일에는 전체 JSON만 담는다. 엄격 검사 실패도 `analysis_ok: true`와 `binary_verification.acceptable: false`를 함께 저장할 수 있으므로 두 차원과 종료 코드를 모두 확인한다.

## 회귀 검사

```powershell
python -B -m unittest discover -s tests
```

통합 검사는 추적 중인 소스·결과를 임시 트리에 복사하고 생성 빌드는 넣지 않는다. 네 분석기, 엄격 모드 누락 실패, 소스·보고서 변경 실패, 존재하는 잘못된 바이너리, 출력 보호와 과거 측정 필드의 정확한 일치를 검사한다. 단위 검사는 정상 바이너리·통과 후 손상·접근 불가·명세 해시 불일치를 다룬다. 필요하면 `ONESTEP_TEST_ROOT`를 쓰기 가능한 임시 상위 폴더로 설정한다. 분석·출처 검증 시험이며 새 엔진 실행은 아니다.
