# 검증으로 해소할 위험에 맞춰 설계 깊이와 구현 단계 정하기

변경할 동작과 주변의 보장을 정의한다. 중간 근거에 따라 다음 결정이 달라지거나 버전 공존이 필요할 때 구현을 나눈다.

ID `K-CODE-DESIGN-DELIVERY-SCOPE` · 방법 · 활성 · 근거 확인 2026-11-24

적용 범위 — 불변식, 버전 호환, 플레이어 경험 또는 제작 가능성이 확정되지 않은 소프트웨어·게임 변경

## 지침

사용자나 호출자, 그들이 관찰할 변화, 주변에서 유지해야 할 동작과 주어진 예산을 적는다. 오판 비용이 큰 미해결 선택에 설계 시간을 쓴다. 예를 들어 중단·재시작 후 마지막으로 커밋된 체크포인트가 열려야 한다는 자극·환경·응답을 정한다. 불변식의 소유자와 결정을 뒤집을 근거를 기록한다. 중요한 약속에는 맥락과 비용, 재검토 조건을 남긴다. [Basecamp, setting boundaries](https://basecamp.com/shapeup/1.2-chapter-03) · [writing a pitch](https://basecamp.com/shapeup/1.5-chapter-06) · [Boehm, risk-driven spiral development](https://resources.sei.cmu.edu/asset_files/specialreport/2000_003_001_13655.pdf) · [SEI Quality Attribute Workshop](https://insights.sei.cmu.edu/documents/2542/2018_010_001_513488.pdf) · [Nygard, decision records](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions)

## 적용 범위와 예외

어떤 중간 결과를 확인할 수 있고 다음 결정 중 무엇이 이에 달렸는지 묻는다. 한 번의 원자적 이동을 보장해야 하면 차감, 가산, 통지와 테스트를 한 단위로 둔다. 모듈 여러 개를 바꿔도 하나의 일관된 검사가 가능하다. 반대로 형식 자체는 잘 알아도 독립 배포된 클라이언트가 공존하면 여러 단계가 필요하다. 읽는 쪽, 쓰는 쪽, 롤백 경로와 호환 지원 종료 조건을 정한다. [Parnas, information hiding](https://www.cs.lafayette.edu/~gexia/cs301/resources/parnas.html) · [DORA, small batches](https://dora.dev/capabilities/working-in-small-batches/) · [Google, self-contained changes](https://google.github.io/eng-practices/review/developer/small-cls.html) · [Sato, Parallel Change](https://martinfowler.com/bliki/ParallelChange.html)

## 확인 방법

- 두 트랙 사이에서 클립을 옮길 때 제거 직후 실패를 주입하고 한 번에 실행 취소되는 트랜잭션을 확인한다. 저장 마이그레이션은 구 → 신 → 구 → 신 순으로 이용해 이전 작성자의 영향을 드러낸다. 표시 문구는 바뀐 리소스의 연결을 따라간다. 단순 빈 상태 문구는 문자열과 표시를, 단축키가 들어 있는 메뉴는 렌더링한 키와 이전·새 키 동작을 확인한다. [Scope and delivery procedure](../../skills/vegabond-code-design/references/scope-and-delivery.md)
- 방 열두 개를 만들 때 회색 상자로 만든 분기 하나에서 초보자가 유도 없이 무엇을 골랐고 왜 그랬는지 보아 단서 설계를 검증한다. 실제 제작 경로로 완성한 방 하나를 빌드·로드해 플레이하는 검사는 제작 가능성을 다룬다. 나머지 방을 양산하기 전에 어떤 결과가 설계를 바꿀지 합의한다. 한 방의 결과만으로 나머지 열한 방을 완료하거나 검증할 수 없다. [MDA](https://users.cs.northwestern.edu/~hunicke/MDA.pdf) · [Outer Wilds GDC session](https://gdcvault.com/play/1027008/Independent-Games-Summit-Sparking-Curiosity) · [speakers' slides](https://media.gdcvault.com/GDC%2B2021/beachum_gdc_2021%281%29.pdf) · [Ismail, Prototypes & Vertical Slice](https://ltpf.ramiismail.com/prototypes-and-vertical-slice/)

## 근거

네이티브 C++ 전술 예제는 기존 빌드 스크립트와 게임플레이 소스를 유지하면서 선택 가능한 두 번째 전투 팩을 추가했다. 검증된 확장점을 사용하는 일반 변형은 한 번의 작성·플레이 단계에 담을 수 있다. 별도 검색 사례에서는 다섯 회차 P95가 모두 통과해도 일곱 응답이 개별 제한을 초과했다. 인수 기준이 바뀌면서 필요한 검사와 프로파일링 판단도 바뀌었다. [Recorded tactics workflow](../../docs/examples/cpp-gameplay-workflow/native-tactics/WORKFLOW.md) · [file comparison](../../docs/examples/cpp-gameplay-workflow/native-tactics/evidence/baseline-vs-extension.json) · [search benchmark](K-CODE-RETRIEVAL-SCALE.md)

가상 브리프를 받은 신규 검토자는 클립 트랜잭션, 버전 호환 왕복과 분기 하나의 플레이테스트를 제안했다. 단순 문구 변경에는 관련 없는 내보내기 명령까지 제안했다. 변경 리소스의 바인딩을 기준으로 범위를 좁힌 후 다른 검토자는 일반 문자열과 메뉴 접근 키에 다른 검사를 골랐다. 이 실험은 검사 계획을 평가했으며 마이그레이션 실행, 플레이어 관찰, 팀 생산성은 측정하지 않았다.
