# 네이티브 에디터 자동화로 실제 PIE 검증하기

항목 `K-CODE-UE-PIE-VERIFICATION` · 상태 활성 · 확인일 2026-11-11

검색어 Play In Editor,PIE,UnrealEd,FEditorLoadMap,FStartPIECommand,FEndPlayMapCommand,UWorld::WorldType,EWorldType::PIE,Target.bBuildEditor,latent automation command,rendered viewport,orthographic camera,snapshot lifetime,backpressure,에디터 자동화,플레이 월드

## 지침

설치한 엔진의 `AutomationEditorCommon.h`에서 에디터 자동화 명령을 확인한다. UE 5.8.3의 `FEditorLoadMap`은 테스트 맵을 열고, `FStartPIECommand(false)`는 Play In Editor(PIE)를 요청하며, `FEndPlayMapCommand`는 종료를 요청한다. 잠복 명령은 여러 프레임에 걸칠 수 있으므로 플레이 월드 생성과 대상 작업 완료를 기다린다. `Target.bBuildEditor`일 때만 `UnrealEd` 모듈에 의존하고 대상에 맞는 에디터·자동화 컴파일 조건을 적용한다.

대상 월드의 `UWorld::WorldType`이 `EWorldType::PIE`인지 확인한다. `-game`으로 실행한 독립 프로세스는 게임 월드다. 실제 로드된 에디터 모듈과 소스·설정·테스트 실행기를 검증하려는 빌드와 대조한다. 자동화 결과와 실제 소비자의 실행 결과가 모두 성공해야 한다. 렌더링을 검증하려면 렌더링 백엔드와 요구한 뷰포트 및 캡처된 화면이 필요하다. 고정 시간 영상과 일반 패키지 실행의 프레임 시간은 구분한다.

## 적용 범위와 예외

과거 실행은 Windows/D3D11의 UE 5.8.3에서 네이티브 C++ 에디터 자동화 및 따로 쿠킹한 Development Game을 검증했다. 다른 프로젝트에서 명령 시그니처, 월드 생성, 카메라, 종료와 에셋을 확인한다. 네트워크 PIE, 다른 그래픽 백엔드, 시뮬레이션 도중 자동 저장에는 별도 검사가 필요하다.

## 점검

- 독립 게임 월드, 잘못된 소비자, 오래된 결과, 미완료 작업, 중첩된 실패, 뷰포트 누락이나 크기 불일치를 거부한다. 실행 코드가 사용한 렌더 플래그와 모드를 확인한다. 표시 이름·정책·추적 실행기를 일부러 바꾸면 해당 증거는 실패해야 한다.
- 충돌 컴포넌트와 시각 메시의 월드 변환을 모두 확인하고 해당 화면 좌표의 실제 픽셀을 본다. 직교 카메라의 뷰 원점·근원면 자동 조정이 구도를 바꿀 수 있다. HUD 가림까지 포함해 투영 위치와 캡처를 비교하고, 객체 제거 전 최초·중간·최종 상태를 검사한다.
- 서비스 동작을 검증할 때 원래 요청 ID, 도착, 입장, 거절, 완료 및 가장 오래 기다린 항목을 개별 기록에서 복원한다. 같은 시뮬레이션 시점에 두 구현의 설정과 결과를 대조한다.
- 스냅샷에서는 값의 타입, 이스케이프, 정밀도, 요구된 멤버·배열 순서, 누락·중복을 확인한다. 쓰기 전에 원본을 바꾸거나 파괴한다. 백그라운드 작업 전에 메타데이터와 문자열을 포함한 입력을 완전히 분리하고 살아 있는 `UObject`와 월드는 게임 스레드에서 다룬다. 입력 용량·소유권, 거부 후 재시도, FIFO 완료, 쓰기 실패, 대기 작업을 둔 종료를 시험한다. 평소 폴링과 종료 시 비우기는 대기 동작이 다를 수 있다. 임시 파일 이름 변경만으로 비정상 종료 후 내구성을 입증할 수 없다.

## 근거

과거 보고서는 실제 PIE와 패키지 실행에서 독립 게임 월드, 위치가 어긋난 시각 메시, 잘못 적용된 실행 설정을 검출하고 출력 동등성과 종료 시 수락한 저장의 완료를 확인했다. 일부 데이터만 소유한 스냅샷은 여전히 월드에 접근했다. 이후 전체 입력을 소유하는 경로를 원본 폐기 후 검증했다. 이번 검토에서는 에디터나 성능·게임플레이 실험을 다시 실행하지 않았다.

- [Epic, EWorldType::Type](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/EWorldType__Type?application_version=5.8) · `UnrealEd/Public/Tests/AutomationEditorCommon.h` (UE 5.8.3)
- [PIE automation](../sources.md#src-ue-lab-editor-gate-results-md) · [Orthographic framing](../sources.md#src-ue-lab-traffic-results-md) · [Mesh transforms](../sources.md#src-ue-lab-stream-results-md) · [Queue and policy identity](../sources.md#src-ue-lab-admission-results-md)
- [Viewport and trace settings](../sources.md#src-ue-lab-hitch-results-md) · [Planner comparison](../sources.md#src-ue-lab-planner-results-md) · [Snapshot parity](../sources.md#src-ue-lab-snapshot-results-md) · [Worker completion](../sources.md#src-ue-lab-async-save-results-md)
