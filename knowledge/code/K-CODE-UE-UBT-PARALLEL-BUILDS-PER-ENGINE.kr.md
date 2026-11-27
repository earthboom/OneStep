# 여러 프로젝트 체크아웃을 동시에 빌드하려면 언리얼 엔진 트리를 하나 더 둬야 하는지 판단하기

- ID: K-CODE-UE-UBT-PARALLEL-BUILDS-PER-ENGINE
- 종류: reference
- 상태: active, 확인일 2026-11-27
- 범위: 한 컴퓨터에서 여러 프로젝트 체크아웃이나 브랜치를 동시에 빌드하는 Windows의 언리얼 엔진 소스 빌드
- 조건: Unreal Engine 5.8 소스 빌드, Windows 11
- 요약: UnrealBuildTool은 같은 UBT 실행 파일에서 시작한 빌드를 이름 있는 단일 인스턴스 뮤텍스로 하나씩만 돌린다. 그래서 엔진 트리 하나를 같이 쓰는 프로젝트 체크아웃들은 서로 줄을 선다. 엔진 트리를 따로 두면 UBT 경로가 달라 따로 빌드되지만, 디스크, 엔진 전체 빌드, 두 트리를 같은 엔진 리비전으로 맞춰 두는 비용이 든다.

## 지침

- **동작 원리.** 단일 인스턴스로 표시된 빌드 모드에서 UBT는 실행 중인 UBT 어셈블리 경로로 이름을 만든 전역 뮤텍스(`UnrealBuildTool_Mutex`에 그 경로를 붙인 이름)를 잡는다. `-WaitMutex`면 두 번째 빌드가 기다리고, 없으면 바로 실패한다. 이름에 프로젝트 경로가 들어가지 않으므로 한 엔진 트리의 모든 프로젝트 빌드가 같은 뮤텍스를 두고 다툰다.
- **결과.** 한 엔진 트리를 쓰는 체크아웃들은 CPU나 메모리가 남아도 동시에 컴파일하지 못한다. 엔진 트리를 따로 두면 UBT 경로가 달라 뮤텍스도 따로 생긴다. Live Coding 검사도 에디터 실행 파일 경로로 정해지므로(`R-CODE-UE-UBT-LIVECODING-ACROSS-CHECKOUTS` 참고) 트리를 나누면 그 막힘도 사라진다.
- **`-NoMutex`로 대신하지 않는다.** 검사는 건너뛰지만 공유 빌드 환경 타깃이 엔진 모듈을 다시 빌드하면 두 빌드가 같은 엔진 `Binaries`, `Intermediate`, 생성 헤더 위치에 쓴다. 어느 쪽도 엔진 모듈을 다시 빌드하지 않는다고 확실할 때만 쓴다.
- **두 번째 트리의 비용.** 빌드된 소스 트리는 대부분 소스가 아니라 빌드 결과물(바이너리, 중간 파일, 플러그인 빌드 결과)이다. 대상 드라이브에 기존 빌드 트리 크기만큼, 또는 거기서 실제로 빌드할 타깃만큼 공간을 잡는다. 보통 가장 큰 한 덩어리는 디버그 심볼(`.pdb`)이다. 그래서 타깃의 `DebugInfo` 모드(예: 그 트리의 `BuildConfiguration.xml`이나 `-DebugInfo=`로 지정하는 `ProjectOnly`)가 클론과 worktree 중 무엇을 고르느냐보다 필요한 용량을 훨씬 크게 바꾼다. 대신 엔진 쪽 디버깅용 심볼도 없어진다. 엔진이 Git 저장소면 다른 드라이브에 `git worktree add`로 만들어 오브젝트 저장소를 공유할 수 있다. Git은 같은 브랜치를 두 worktree에 체크아웃하지 못하므로 분리된(detached) 커밋이나 별도 로컬 브랜치를 쓴다. 새 트리도 의존성 설정과 엔진 전체 빌드가 필요하다. 빌드된 트리를 복사하면 다운로드는 줄지만 빌드 중간 파일의 절대 경로 때문에 크게 다시 빌드될 수 있다.
- **Setup 부수 효과.** `Setup.bat`은 재배포 패키지를 컴퓨터 전체에 설치하고 `UnrealVersionSelector /register`도 실행한다. 이 등록은 관리자 권한으로 `.uproject` 파일 연결을 새 트리로 바꿀지 묻는다. 이미 쓰는 트리가 있는 컴퓨터라면 `GitDependencies`와 hook 등록만 실행해 이 변경을 피할 수 있다. 나중에 에디터를 처음 열면 파일 연결은 건드리지 않고 사용자 엔진 목록에 트리가 등록된다. `Setup.bat`은 `.git\hooks`가 폴더일 때만 post-checkout, post-merge 의존성 hook을 쓴다. 그래서 `.git`이 파일인 worktree에는 hook이 없고, 갱신할 때마다 의존성을 직접 맞춰야 한다. `GitDependencies`도 `.git` 폴더를 통해서만 다운로드 캐시를 찾으므로, worktree에서는 `-cache=`나 `UE_GITDEPS`를 주지 않으면 캐시 없이 돈다.
- **계속 드는 비용.** 두 트리 모두 프로젝트가 연결한 엔진 리비전에 있어야 하고, 엔진을 올릴 때마다 양쪽에 반영하고 빌드해야 한다. 뒤처진 트리로 에셋을 저장하면 다른 엔진 버전으로 저장될 수 있다.
- **처리량 한계.** 두 번째 트리는 대기를 없앨 뿐 CPU 경쟁은 없애지 못한다. 같은 코어에서 큰 로컬 컴파일 두 개를 함께 돌리면 차례로 돌린 것과 비슷하게 걸린다. 얻는 것은 작은 증분 빌드가 긴 빌드를 기다리지 않게 되는 점이다. 둘을 함께 돌릴 때는 각 트리의 `Engine/Saved/UnrealBuildTool/BuildConfiguration.xml`에서 로컬 병렬 수를 제한하고, 진짜 제약이 전체 컴파일 능력이면 분산 실행기(원격 풀을 쓰는 UBA 등)를 우선한다.
- **체크아웃과 트리 연결.** 각 체크아웃이 쓸 트리를 명시한다. 빌드 스크립트가 읽는 엔진 경로, 프로젝트 디스크립터의 등록 엔진 연결, 그 트리로 만든 IDE 솔루션이다. 모든 체크아웃이 같이 쓰는 사용자 환경 변수 하나면 모든 체크아웃이 말없이 같은 트리로 간다.

## 적용 조건과 예외

- UE 5.8 UBT 소스로 확인했다. 다른 버전은 뮤텍스 이름이나 범위가 다를 수 있으니 의존하기 전에 소스 줄을 다시 본다.
- 설치형(미리 빌드된) 엔진도 경로별 뮤텍스는 같다. 별도 에이전트에서 컴파일하는 팀 빌드 팜에는 해당하지 않는다.
- 대기 원인이 모듈 DLL을 잡고 있는 열린 에디터나 Live Coding이면, 그 에디터가 다른 트리에서 실행될 때만 두 번째 트리가 도움이 된다.

## 점검

- 트리를 추가하기 전에 대기 원인이 UBT 뮤텍스인지 확인한다. 두 번째 빌드가 다른 UBT 인스턴스를 기다린다고 출력하거나, `-WaitMutex` 없이 뮤텍스를 못 잡고 실패하면 맞다.
- 설정한 뒤 각 체크아웃에서 동시에 빌드를 시작해 어느 쪽도 기다리지 않는지 확인한다.
- 엔진을 올린 뒤에는 빌드하거나 에셋을 저장하기 전에 두 트리의 엔진 커밋을 비교한다.

## 근거

- 엔진 소스, Unreal Engine 5.8: `Engine/Source/Programs/UnrealBuildTool/UnrealBuildTool.cs` 446행 부근: `GlobalSingleInstanceMutex.GetUniqueMutexForPath("UnrealBuildTool_Mutex", FileReference.FromString(Assembly.GetExecutingAssembly().Location))`. `-WaitMutex`면 `SingleInstanceMutex.Acquire`, 아니면 `AcquireNowOrThrow`로 잡고, `NoMutex`면 건너뛴다. 2026-11-27에 읽었고, 위의 동시 빌드 점검은 실행하지 않았다.
- 관찰, 2026-11-27: 빌드된 UE 5.8 소스 트리는 약 336 GiB였다. 그중 플러그인(빌드 결과 포함) 약 144 GiB, 바이너리 약 70 GiB, 중간 파일 약 39 GiB, 소스 약 37 GiB였고, 공유 Git 오브젝트 저장소는 약 26 GiB였다. 같은 트리에서 `.pdb` 파일이 약 154 GiB(엔진 플러그인 아래가 약 107 GiB)였다. Development 에디터 빌드는 바이너리 약 134 GiB, 중간 파일 약 58 GiB였다. `Setup.bat`이 설치한 의존성은 약 85 GiB(`Commit.gitdeps.xml` 기준 압축 다운로드 약 30 GiB), HEAD의 추적 파일은 약 2.7 GiB, 브랜치 하나의 히스토리는 압축된 오브젝트로 약 12 GiB(`git rev-list --disk-usage --objects`)였다. `DebugInfoMode` 값(`None`, `Engine`, `EnginePlugins`, `Project`, `ProjectPlugins`, `EngineOnly`, `ProjectOnly`)은 `Engine/Source/Programs/UnrealBuildTool/Configuration/Rules/TargetRules.cs`에 정의되어 있다. `ProjectOnly`로 줄어드는 용량은 측정하지 않았다. 같은 엔진 리비전을 한 브랜치만 새로 클론하고, 의존성(다운로드 31 GB)을 받고, 디버그 정보를 모두 켠 Development로 `UnrealEditor`, `ShaderCompileWorker`, `LiveCodingConsole`, `CrashReportClientEditor`, `UnrealPak`를 빌드하니 12.7 GiB의 Git 저장소를 포함해 305.7 GiB였다. UBA 원격 풀로 빌드에 32분이 걸렸다. 게임 프로젝트만 켜는 엔진 플러그인은 나중에 그 프로젝트의 에디터 타깃이 빌드하므로 여기에 포함되지 않았다. Setup 부수 효과는 5.8 `Setup.bat`, `Engine/Source/Programs/UnrealVersionSelector/Private/UnrealVersionSelector.cpp`(`RegisterCurrentEngineDirectory`, 파일 연결 확인 창과 관리자 권한 `/fileassociations`), `Engine/Source/Programs/GitDependencies/Program.cs`(`.git` 폴더를 통한 캐시 찾기)에서 읽었고, hook이 등록되지 않은 worktree에서 관찰했다.
- 관련 사고: `R-CODE-UE-UBT-LIVECODING-ACROSS-CHECKOUTS` (에디터 실행 파일 경로로 정해지는 Live Coding 뮤텍스).
