# GC 도달 가능성, 자원 정리와 메모리 증가 진단 구분하기

항목 `K-CODE-GC-LIFETIMES` · 상태 활성 · 확인일 2026-11-07

검색어 garbage collection, GC, reachability, retention, memory leak, fragmentation, allocation churn, IDisposable, UObject, TObjectPtr, 메모리 관리, 가비지 컬렉션, 메모리 누수, 객체 보존, UPROPERTY, TStrongObjectPtr, TWeakObjectPtr, TSoftObjectPtr

## 지침

객체가 도달 가능한지, 여전히 필요한지, 외부 자원을 지금 닫아야 하는지 구분한다. .NET GC는 루트에서 도달하지 못하는 관리 객체의 메모리를 수거할 수 있다. 아직 참조된 캐시 항목이 쓸모없어졌는지는 알 수 없다. IDisposable의 Dispose 계약은 소유한 자원을 명시적으로 정리한다. Dispose 후에도 관리 객체 자체는 도달 가능할 수 있다.

UE에서 UObject를 가리키는 TObjectPtr 멤버는 UPROPERTY로 반영되고 소유자가 도달 가능할 때 강한 참조 경로를 제공한다. TStrongObjectPtr은 반영된 필드 밖에서도 객체를 살려 둔다. TWeakObjectPtr은 로드된 객체를 붙잡지 않으므로 사용 전 유효성을 확인한다. TSoftObjectPtr은 경로로 에셋을 식별하고 자동 로드하거나 메모리에 붙잡아 두지 않는다.

## 적용 범위와 예외

CLR과 UE의 각 계약에 적용한다. 수거 가능 시점, 실제 수거, 프로세스 메모리 감소는 다르다. 네이티브·GPU 메모리, 할당자 캐시와 엔진 하위 시스템은 별도 계상한다.

## 점검

같은 부하를 재현해 안정 상태를 비교하고 소유권을 잃은 할당, 불필요한 강한 참조, 단편화, 임시 할당 빈도를 구분한다. 관리 힙·프로세스·핸들 수, 타입과 루트 경로를 본다. .NET은 dumpheap·gcroot 등을 사용할 수 있다. 캐시·구독·작업 캡처, Unreal의 반영된 강한 참조와 외부 자원의 해제를 살핀다.

## 근거

2026-11-07 Microsoft Learn과 UE 5.8 객체 포인터 표 및 강한 참조 설명을 확인한 문헌 기록이다. .NET 누수 진단 예제는 .NET Core 3.1 이상을 대상으로 하며 도구 출력이 다를 수 있다. 로컬 프로세스·힙 덤프나 자원 정리 실험은 없었다. [Microsoft GC](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/fundamentals) · [Dispose](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-dispose) · [Leak diagnostics](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/debug-memory-leak) · [Epic object pointers](https://dev.epicgames.com/documentation/en-us/unreal-engine/object-pointers-in-unreal-engine?application_version=5.8)
