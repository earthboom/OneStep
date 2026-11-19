# 언리얼 작업의 공유 DDC와 원격 컴파일 사용 여부 확인하기

항목 `K-CODE-UE-LOCAL-ONLY-WORK` · 상태 활성 · 확인일 2026-11-06

----------

## 지침

DDC(Derived Data Cache)는 재생성 가능한 엔진·에셋 파생 데이터를 보관한다. 파일시스템 공유 저장소를 체크아웃 한 곳에서만 끌 때는 프로젝트가 쓰는 저장소 이름과 Config/UserEngine.ini의 [DerivedDataCacheStores], Shared=(Type=FileSystem, Path=None)을 확인한다. 사용자 재정의 파일을 .git/info/exclude로 제외한다.

UnrealBuildTool은 사용자 BuildConfiguration.xml을 읽는다. UBA(Unreal Build Accelerator)는 Horde를 통해 C++ 컴파일 작업을 원격 실행할 수 있다. 출력의 RemoteExecutor·Horde 설정과 실제 실행 위치를 확인한다. Incredibuild의 XGE 셰이더 컨트롤러는 별도 경로이므로 UBA가 비활성이라는 메시지만으로 로컬 작업이라고 결론 내릴 수 없다.

## 적용 범위와 예외

UE 5.8 Windows 소스 빌드의 관찰이다. 다른 버전·설치는 실제 선택된 백엔드와 실행기를 확인한다. 사용자 ini 레이어는 체크아웃 단위지만 로컬 ZenServer와 엔진 DDC는 같은 PC의 다른 프로젝트와 공유될 수 있다. 호스트 로컬과 프로젝트 간 격리를 구분한다.

## 점검

LogDerivedDataCache 범주에서 해당 저장소가 비활성인지 확인한다. git check-ignore -v, git status로 재정의 파일을 확인한다. 빌드 전에 원격 실행기 설정을 점검하고 이후 실제 원격 작업 기록을 확인한다. 컨트롤러 선택과 원격 작업 실행은 각각 다르게 보고한다.

## 근거

2026-11-06 UE 5.8 Windows에서 파일시스템 공유 DDC가 꺼졌지만 C++ 작업은 원격 실행됐고 에디터는 XGE 셰이더 컨트롤러를 골랐다. 실제 원격 셰이더 작업과 단일 빌드의 UBA 로컬 전용 구성은 미확인이다. [Epic, Horde and Unreal Build Accelerator](https://dev.epicgames.com/documentation/en-us/unreal-engine/horde-unreal-build-accelerator-and-remote-compilation-tutorial-for-unreal-engine?application_version=5.8)

검색어 Unreal Engine, DDC, Derived Data Cache, shared DDC, UserEngine.ini, UnrealBuildTool, UBA, Horde, Incredibuild, XGE, distributed compile, local only, Unreal Build Accelerator, LogDerivedDataCache, BuildConfiguration.xml, bAllowUBAExecutor
