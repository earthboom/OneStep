---
id: K-CODE-WPF-LARGE-TREE
title: 행이 수천 개인 WPF 프로퍼티 트리를 빠르게 유지하는 방법
summary: 하위 행은 처음 읽을 때 만들고, 행의 하위 목록은 펼쳐져 있을 때만 바인딩하며, 구역 머리글과 최상위 행은 평평한 가상화 목록 하나로 보여 줍니다. ScrollViewer 안에서 Expander마다 일반 ItemsControl을 두면 모든 행이 만들어집니다.
kind: lesson
scope: ItemsControl 템플릿으로 큰 계층 데이터(프로퍼티 그리드, Details 패널, 트리형 목록)를 보여 주는 WPF 뷰
keywords: [WPF, virtualization, UI virtualization, VirtualizingStackPanel, CanContentScroll, ScrollUnit, VirtualizationMode, ItemsControl, Expander, ScrollViewer, lazy loading, property tree, tree view performance, 가상화, 지연 로딩]
status: active
checked_at: "2026-11-10"
context:
  framework: .NET 10 WPF
  platform: Windows 데스크톱
---

## 지침

1. **지연 하위 행:** 각 행의 하위 목록은 하위 행을 만들지 않고도 `Count`를 알려 주게 합니다(처음 색인하거나 열거할 때 만드는 `IReadOnlyList<T>`). 펼침 화살표에는 개수만 필요합니다.
2. **펼칠 때 바인딩:** 행의 `DataTemplate`에서 하위 `ItemsControl`은 `ItemsSource` 없이 접어 둡니다. 토글의 `IsChecked` 트리거가 `ItemsSource`와 `Visibility`를 설정합니다. 그러면 접힌 행은 하위 컨테이너를 만들지 않습니다.
3. **가상화 목록 하나:** 뷰 모델에서 구역 머리글, 안내문, 최상위 행을 한 목록으로 펴고, 이를 하나의 `ItemsControl`로 보여 줍니다. 그 템플릿에는 `CanContentScroll="True"`인 `ScrollViewer`를, 패널에는 `VirtualizingStackPanel`(`VirtualizingPanel.IsVirtualizing`, `ScrollUnit="Pixel"`)을 둡니다. 구역마다 `Expander`를 두는 대신, 목록을 다시 만드는 `IsExpanded` 속성을 가진 머리글 항목을 씁니다.
4. **값싼 행 텍스트:** 중첩된 값의 한 줄 요약은 표시 너비를 넘으면 만들기를 멈추고 타입 이름으로 대신합니다.

## 적용 범위와 예외

`ItemsControl`을 바깥 `ScrollViewer`로 감싸거나 가상화 패널 없이 쓰면 모든 항목을 측정하므로 가상화가 조용히 작동하지 않습니다. 펼친 행 안의 하위 목록은 여전히 가상화되지 않으므로 길이를 제한하거나 그것도 펴야 합니다. 가상화를 켠 `TreeView`는 대안이지만 비교하지 않았습니다.

## 확인 방법

- 실제로 가장 큰 데이터로, 데이터 할당부터 레이아웃 완료(디스패처가 안정된 뒤 `UpdateLayout`)까지 시간을 예산과 비교해 잽니다.
- 경과 시간뿐 아니라 만들어진 행이나 컨테이너 수도 전후로 셉니다.

## 근거

출처: 독립 실행형 에셋 뷰어의 Details 패널, 2026-11-10, Debug 빌드. 가장 큰 객체는 최상위 행이 1,263개(전부 펼치면 75,937개)였습니다. 행 생성은 492–864 ms에서 26–58 ms로, 탭 준비 시간은 7,969 ms에서 1,000 ms 예산 안으로 줄었습니다. 기기 부하가 높은 전체 테스트 실행 한 번에서는 다른 뷰가 1,034 ms여서 Debug 여유는 작았습니다.

검증하지 않음: Release 시간, 스크롤 부드러움, 메모리 사용량.
