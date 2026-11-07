# 가비지 컬렉션·자원 정리·메모리 진단을 구분한다

- ID: K-CODE-GC-LIFETIMES
- 요약: GC는 회수 조건을 만족하는 도달 불가 관리 객체를 회수합니다. 유용한 수명·신속한 정리는 별도 설계하며 도달 가능성·할당·단편화 근거로 증가 원인을 진단합니다.
- 종류: 참고 지식 / 상태: 활성 / 근거 확인일: 2026-11-07
- 범위: .NET 관리 메모리 진단과 Unreal UObject 참조. 모든 GC에 대한 보장이 아닌 출처별 기전입니다.
- 검색어: garbage collection, GC, reachability, retention, memory leak, fragmentation, allocation churn, IDisposable, UObject, TObjectPtr, 메모리 관리, 가비지 컬렉션, 메모리 누수, 객체 보존
- 확인 및 적용 맥락: 2026-11-07 Microsoft Learn·Epic 문서를 확인했으며 Epic은 UE 5.8을 제공했습니다. 실제 프로세스·덤프·프로파일러·정리 검사는 수행하지 않았습니다.

## 지침

도달 가능한지, 아직 필요한지, 외부 자원을 지금 닫아야 하는지를 구분합니다. .NET GC는 루트에서 도달 불가 객체를 찾아 수집 때 적격 관리 메모리를 회수합니다. 도달 가능한 캐시 항목의 불필요함을 추론하거나 모든 메모리·네이티브 핸들을 해제하지는 않습니다.

소유한 disposable 자원은 문서의 해제 계약을 따릅니다. Dispose의 정리는 관리 객체 저장공간 회수와 다릅니다. 해제한 객체도 도달 가능할 수 있으며 소유권에 따라 포함 객체의 연쇄 해제 여부를 정합니다. 파일·소켓의 신속한 닫기는 GC 시점 대신 명시적 자원 프로토콜이 필요합니다.

Unreal은 실제 UObject 참조 종류를 확인합니다. Epic 표는 강한·약한·소프트 참조를 구분합니다. TObjectPtr는 UPROPERTY로 표시됐을 때 GC 안전하며 TStrongObjectPtr는 리플렉션 필드 밖에서도 GC에 영향을 줍니다. 포인터 모양만으로 엔진이 추적하는 도달 가능성이 입증되지는 않습니다.

## 적용 조건과 예외

.NET 설명은 CLR 관리 객체에, Epic 설명은 해당 엔진 버전에 적용합니다. 네이티브 할당·GPU·할당자 캐시·엔진 하위 시스템은 별도 집계가 필요합니다. GC 대상이라는 사실은 즉시 회수나 프로세스 메모리 즉시 감소를 약속하지 않습니다. 런타임마다 정책이 다르며 .NET 알고리즘을 Unreal 보장으로 옮기지 않습니다.

## 점검

다음은 제안 진단 순서입니다.

- 고정 부하로 안정된 기준선을 비교합니다. 소유권을 잃은 미해제 할당, 도달 가능하지만 불필요한 보유, 단편화, 빠른 임시 할당을 구분합니다. 증가만으로 원인이 정해지지 않습니다.
- 관리 힙·할당률·수집 동작·프로세스 및 네이티브 메모리를 비교합니다. 주요 타입·루트 경로를 조사합니다. Microsoft 예는 카운터·덤프·dumpheap·gcroot를 사용합니다.
- 보유 문제는 캐시 한도·구독·작업 캡처를, 자원 고갈은 활성 핸들 수·해제를 따로 확인합니다. Unreal은 리플렉션 추적·의도하지 않은 강한 참조를 확인합니다.

## 근거

2026-11-07 확인한 출처입니다.

- [Microsoft GC 기본](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/fundamentals): Memory release, Unmanaged resources, 단편화 설명.
- [Microsoft Dispose 구현](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-dispose): 도입·Cascade dispose calls·Dispose와 관리 저장공간 해제의 구분.
- [Microsoft 누수 진단](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/debug-memory-leak): 관리 메모리 조사·코어 덤프 분석. .NET Core 3.1 이후 대상이며 도구 출력은 다를 수 있습니다.
- [Epic 객체 포인터](https://dev.epicgames.com/documentation/en-us/unreal-engine/object-pointers-in-unreal-engine): 표 각주·TObjectPtr·TStrongObjectPtr, UE 5.8.

Microsoft 페이지에 권한 안내가 있었지만 해당 본문은 읽을 수 있었습니다. 로컬 측정은 하지 않았으며 제안 점검으로 진단이나 예방 검증이 확립되지는 않았습니다.
