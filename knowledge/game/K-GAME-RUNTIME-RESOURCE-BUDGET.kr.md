# 긴 프레임의 원인을 찾아 스폰·풀링·스트리밍 선택하기

K-GAME-RUNTIME-RESOURCE-BUDGET · 방법 · 적용 중 · 근거 확인 2026-11-22

반복 가능한 동선에서 CPU·GPU·I/O·활성화 시간을 구분한다. 측정한 비용, 수명, 재사용 빈도, 실패 동작에 따라 자원 전략을 선택한다.

적용 범위 — 지원 기기의 프레임 시간, 최초 진입, 상주 메모리, 콘텐츠 스트리밍.

## 적용 방법

기기·빌드·해상도·품질·카메라·동선을 고정한다. 첫 방문, 워밍업, 안정 구간을 나눈다. CPU·GPU가 겹쳐 일하는 구간과 대기를 타임라인에서 본다. 해상도를 낮춰 픽셀 비용을, 제출 시간을 보고 드로 콜과 상태 변경을, 패스별로 그림자·스키닝·파티클 비용을 분리한다. 첫 진입에서는 I/O·압축 해제·업로드·PSO 컴파일을 따로 본다. 중앙값·p95/p99와 예산 초과 빈도·지속 시간을 비교한다.

배칭·인스턴싱은 제출 횟수를 줄이면서 메모리, 셰이더 제약, 컬링 단위를 바꿀 수 있다. 오클루전 쿼리 자체의 대기·검사 비용을 잰다. 빠른 이동에서 LOD/HLOD 윤곽과 전환을 확인한다. GPU 기반 렌더링은 GPU로 옮긴 일과 메모리도 측정한다. 패스를 제거했다면 화면에서 무엇이 사라졌는지 본다.

빈도·지연이 허용되면 필요할 때 스폰한다. 생성 비용이 크고 자주 반복되는 객체는 풀 용량과 소진 시 정책을 정하고 재사용 시 타이머·콜백·체력·물리 상태를 초기화한다. 계산 결과 캐시는 입력·버전·공간 범위를 키로 삼는다. 무효화가 확실한 고정 작업은 미리 굽는다. 이동 동선으로 수요를 예측할 수 있으면 스트리밍한다. 선행 로드 거리는 이동 속도 × 준비 시간 + 여유 거리로 시작하고 활성화를 여러 프레임에 나누며 오래된 요청을 취소·해제한다.

## 적용 조건과 예외

다운로드된 파일도 압축 해제·업로드·활성화가 남을 수 있다. 풀은 객체를, 캐시는 다시 구하는 비용이 큰 결과를 보관한다. 셰이더 컴파일은 별도 비용이다. ARC의 순차 스캔 내성은 저장장치 캐시 연구에서 나온 결과이므로 한 번만 지나는 동선과 반복 방문을 비교한다. 플레이에 영향을 주는 절차적 지형은 생성기 버전과 변경 이력을 보존해야 할 수 있다.

## 확인 방법

동일 기기에서 마을→숲→교전→마을 동선을 반복한다. 골목·탁 트인 숲·군중·야간을 따로 캡처한다. 순간 이동, 경로 역전, 동시 대량 스폰, 이전 콜백 도착 전 객체 재사용을 시험한다. 준비 지연, 최대·상주 메모리, 프레임별 활성화, 화면 전환, 캐시 무효화와 복귀 상태를 확인한다. 저장장치 속도·메모리 압력·카메라 이동에 따라 결과가 달라진다.

## 근거

11월 22일 개발 관행 조사는 메시·컬링 원 논문, 실제 엔진과 스트리밍 발표, 프로파일러 문서, 캐시 연구를 비교했다. 발표 자료는 공개된 세션 설명과 슬라이드 범위다. 마을 동선은 실험 제안이다.

[성능 측정](../code/K-CODE-PERFORMANCE-MEASUREMENT.md) · [시뮬레이션 정밀도](K-GAME-NPC-SIMULATION.md)

- [Unity profiling](https://unity.com/how-to/best-practices-for-profiling-game-performance) · [Unreal profiling](https://dev.epicgames.com/documentation/en-us/unreal-engine/introduction-to-performance-profiling-and-configuration-in-unreal-engine) · [Unreal Fest frame timing video](https://www.youtube.com/watch?v=dKSHw_8vz3I) · [Unity rendering captures](https://docs.unity.com/en-us/engine/6000.3/manual/analysis/graphics-performance-profiling/profile-rendering) · [Unreal dynamic resolution](https://dev.epicgames.com/documentation/en-us/unreal-engine/dynamic-resolution-in-unreal-engine)
- [Unreal PSO Precaching](https://dev.epicgames.com/documentation/unreal-engine/pso-precaching-for-unreal-engine) · [Unity PSO warm-up](https://docs.unity.com/en-us/engine/6000.3/manual/materials-and-shaders/shaders/shader-troubleshooting/shader-reduce-stalling/shader-prevent-stutter/shader-pso-trace-warming/shader-pso-introduction) · [Unity draw call optimization](https://docs.unity.com/en-us/engine/6000.3/manual/analysis/graphics-performance-profiling/reduce-draw-calls/optimizing-draw-calls-choose-method) · [Unity URP GPU culling](https://docs.unity.com/en-us/engine/6000.3/manual/analysis/graphics-performance-profiling/in-urp/gpu-culling) · [Unreal visibility and occlusion](https://dev.epicgames.com/documentation/en-us/unreal-engine/visibility-and-occlusion-culling-in-unreal-engine)
- [Hoppe, SIGGRAPH 1996 — Paper](https://www.cs.jhu.edu/~misha/ReadingSeminar/Papers/Hoppe96.pdf) · [Bittner et al., 2004 — Paper](https://www.cg.tuwien.ac.at/research/publications/2004/Bittner-2004-CHC/Bittner-2004-CHC-Paper.pdf) · [Haar and Aaltonen, SIGGRAPH 2015 — Slides](https://advances.realtimerendering.com/s2015/aaltonenhaar_siggraph2015_combined_final_footer_220dpi.pdf) · [Karis et al., SIGGRAPH 2021 — Talk video](https://www.youtube.com/watch?v=eviSykqSUUw) · [SIGGRAPH materials](https://advances.realtimerendering.com/s2021/Karis_Nanite_SIGGRAPH_Advances_2021_final.pdf)
- [Epic technical documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/nanite-technical-details) · [O’Donnell — GDC talk](https://www.gdcvault.com/play/1024612/) · [Joshua Simmons — GDC talk](https://www.gdcvault.com/play/1034412/Upgrading-the-Snowdrop-Engine-for) · [Development team's technical introduction](https://www.massive.se/article/crafting-pandoras-breathtaking-landscape-with-snowdrop/)
- [Nystrom, Object Pool](https://gameprogrammingpatterns.com/object-pool.html) · [Dirty Flag](https://gameprogrammingpatterns.com/dirty-flag.html) · [Unity pooling guidance](https://docs.unity.com/en-us/engine/6000.3/manual/analysis/performance-memory/managed-memory/optimizing-code-managed-memory/reusable-code) · [Elan Ruskin — GDC talk](https://www.gdcvault.com/play/1022268/Streaming-in-Sunset-Overdrive) · [Elan Ruskin — Slides](https://media.gdcvault.com/gdc2015/presentations/Ruskin_Elan_SunsetOverdriveStreaming.pdf)
- [Chad Barb — Video](https://www.youtube.com/watch?v=4BuvKotqpWo) · [Chad Barb — Slides](https://media.gdcvault.com/gdc2017/Presentations/Barb_Chad_EfficientTextureStreaming.pdf) · [Innes McKendrick — GDC talk](https://www.gdcvault.com/play/1024265/Continuous-World-Generation-in-Noby) · [Megiddo and Modha, FAST 2003 — Paper](https://www.usenix.org/legacy/publications/library/proceedings/fast03/tech/full_papers/megiddo/megiddo.pdf) · [World Partition](https://dev.epicgames.com/documentation/en-us/unreal-engine/world-partition-in-unreal-engine)
- [Addressables memory 2.7](https://docs.unity3d.com/Packages/com.unity.addressables@2.7/manual/MemoryManagement.html) · [DirectStorage](https://learn.microsoft.com/en-us/xbox/gdk/docs/features/console/storage/directstorage/directstorage-overview?view=gdk-2604)
