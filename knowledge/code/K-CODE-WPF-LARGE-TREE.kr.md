# 많은 행을 표시하는 WPF 속성 트리의 응답성 개선

항목 `K-CODE-WPF-LARGE-TREE` · 상태 활성 · 확인일 2026-11-10

검색어 WPF, virtualization, UI virtualization, VirtualizingStackPanel, CanContentScroll, ScrollUnit, VirtualizationMode, ItemsControl, Expander, ScrollViewer, lazy loading, property tree, tree view performance, 가상화, 지연 로딩, VirtualizationMode.Recycling, IReadOnlyList<T>, ItemsSource, DataTemplate, data virtualization, container recycling

## 지침

UI 가상화는 보이는 범위의 컨테이너만 만든다. 데이터 가상화와 지연 생성은 배경 데이터의 생성 시점을 조절한다. VirtualizationMode.Recycling은 스크롤 시 컨테이너를 재사용하므로 항목별 상태는 바인딩된 항목에 둔다.

자식 목록의 Count는 계산할 수 있게 하고 IReadOnlyList<T>의 첫 인덱스 접근이나 열거 시 실제 행을 만든다. DataTemplate에서 자식 ItemsControl을 접고 ItemsSource를 비워 두었다가 토글을 펼칠 때만 바인딩한다. 섹션·안내·최상위 행을 하나의 리스트로 평탄화하고, ScrollViewer의 CanContentScroll=True 및 VirtualizingStackPanel을 사용한다. VirtualizingPanel.IsVirtualizing과 픽셀 ScrollUnit을 확인한다. 헤더의 IsExpanded로 목록을 재구성하고 중첩 값 요약은 표시 폭에서 작업을 중단해 타입 이름으로 대체한다.

## 적용 범위와 예외

바깥 ScrollViewer가 크기 제한 없이 측정하거나 패널이 가상화하지 않으면 모든 행이 만들어질 수 있다. 펼친 자식 목록은 길이를 제한하거나 같은 목록으로 평탄화한다. 가상화된 TreeView와는 비교하지 않았다.

## 점검

가장 큰 대표 데이터로 할당부터 디스패처 안정화와 UpdateLayout 완료까지 측정한다. 준비 시간과 생성된 행·컨테이너 수를 함께 비교한다.

## 근거

2026-11-10 Windows .NET 10 WPF Debug 에셋 검사 뷰에서 행 생성 및 사용 가능 시점이 앞당겨졌다. 머신이 바쁜 실행에서는 다른 뷰의 여유가 적었다. Release, 스크롤 부드러움과 메모리는 측정하지 않았다. [Microsoft, Optimizing performance for WPF controls](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/optimizing-performance-controls)
