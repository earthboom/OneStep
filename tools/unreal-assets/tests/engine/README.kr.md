# 엔진으로 저장한 에셋 검증

테스트 전용 프로젝트에서 실제 언리얼 에디터로 uncooked 에셋을 만든 뒤 **별도의 프로세스에서 저장하지 않고 다시 로드**해 `oracle.json`을 작성합니다. `../verify_engine_assets.py`가 독립적인 엔진 관찰과 파서를 비교합니다. 보조 모듈은 파서에 연결되지 않으며 파서 실행 의존성도 아닙니다.

검증 대상은 내용이 있는 튜토리얼 애니메이션, 이를 참조하는 몽타주, 캔버스·텍스트 자식이 있는 컴파일한 위젯, 세 soft 참조와 기본값이 아닌 규칙을 가진 PrimaryAssetLabel, 두 행의 DataTable입니다. 확인한 엔진에서 애니메이션은 원본 프레임 188개입니다. 실제 엔진으로 작성한 제어 사례이며 실무 프로젝트 전체를 포괄하는 검사는 아닙니다.

**새로운 격리 폴더**, 개발 헤더·라이브러리가 있는 Windows UE 5.8 에디터, 내장 튜토리얼 애니메이션 콘텐츠가 필요합니다. 보조 모듈은 Python이 보호 속성으로 거부하는 실제 값을 확인합니다. 격리된 `/Game/ReaderChecks/` 위젯만 구성하고 native 속성을 텍스트로 내보냅니다. 엔진 소스·에셋은 편집하지 않습니다. 최초 컴파일은 엔진 개발 캐시를 많이 생성할 수 있습니다. 검증한 UE 5.8 소스 빌드를 기준으로 하며 다른 빌드에서는 API 조정이 필요할 수 있습니다. 필요한 콘텐츠·빌드 기능이 없으면 명시적으로 실패해야 합니다.

OneStep 루트에서 실행하는 PowerShell 예시입니다. 엔진 위치 자리표시자는 실제 설치 위치로 바꿉니다.

```powershell
$taskEngine = '<engine directory>'
$taskFixture = Join-Path (Get-Location) '.cache/onestep/native-reader-check'
if (Test-Path -LiteralPath $taskFixture) { throw 'Use a new empty fixture directory' }
Copy-Item -LiteralPath 'tools/unreal-assets/tests/engine' -Destination $taskFixture -Recurse
$taskEditor = Join-Path $taskEngine 'Engine/Binaries/Win64/UnrealEditor-Cmd.exe'
$taskBuilder = Join-Path $taskEngine 'Engine/Build/BatchFiles/Build.bat'
& $taskBuilder AssetCheckEditor Win64 Development "-Project=$taskFixture/AssetCheck.uproject" -WaitMutex -UsePrecompiled -NoHotReloadFromIDE -NoUBA -NoXGE -NoFASTBuild -NoSNDBS -MaxParallelActions=4
if ($LASTEXITCODE -ne 0) { throw 'Fixture helper build failed' }
[Environment]::SetEnvironmentVariable('UE-LocalDataCachePath', "$taskFixture/DDC")
& $taskEditor "$taskFixture/AssetCheck.uproject" -run=pythonscript "-script=$taskFixture/create_assets.py" -unattended -nullrhi -nosound -nop4 -ddc=NoShared "-abslog=$taskFixture/create.log"
if ($LASTEXITCODE -ne 0) { throw 'Fixture creation failed' }
& $taskEditor "$taskFixture/AssetCheck.uproject" -run=pythonscript "-script=$taskFixture/read_assets.py" -unattended -nullrhi -nosound -nop4 -ddc=NoShared "-abslog=$taskFixture/read.log"
if ($LASTEXITCODE -ne 0) { throw 'Independent native observation failed' }
python -B tools/unreal-assets/tests/verify_engine_assets.py --project $taskFixture --output "$taskFixture/evidence"
```

먼저 주 사용 안내에 따라 파서 Release CLI를 빌드합니다. 검증기의 종료 코드가 0이 아니면 실패입니다. 에디터 성공 종료만 믿지 말고 `creation.json`·`oracle.json`·`evidence/results.json`의 값·입력 지문·부분 해석 상태를 확인합니다. 프로젝트 에셋을 얻기 위한 네트워크를 사용하지 않습니다. 설치된 엔진 콘텐츠에서 애니메이션을 복제하며 원본은 유지합니다. 생성 바이너리는 로컬 Git 제외 파일이며 저장소에 배포하지 않습니다.

`oracle.json`이 생기면 생성 스크립트는 에셋을 다시 만들지 않습니다. 기존 파일에는 native **읽기**와 파서 검증만 반복하거나, 다른 사례는 새 폴더에서 생성합니다. 보고서 출력은 원본 `Content` 밖이어야 합니다. native 읽기와 CLI 검증은 각각 전후 패키지 해시를 비교합니다. 이 검사는 저장된 구조·속성·참조를 대상으로 하며 애니메이션 재생·압축 트랙 해독·몽타주 런타임 상태·위젯 화면을 검사하지 않습니다.
