---
id: K-CODE-WPF-LARGE-TREE
title: How to keep a WPF property tree with thousands of rows responsive
summary: Build child rows on first read, bind a row's children only while it is expanded, and show the section headers and top-level rows as one flat virtualized list. Expanders that each hold a plain ItemsControl inside a ScrollViewer create every row.
kind: lesson
scope: WPF views that show large hierarchical data (property grids, Details panels, tree-like lists) with ItemsControl templates
keywords: [WPF, virtualization, UI virtualization, VirtualizingStackPanel, CanContentScroll, ScrollUnit, VirtualizationMode, ItemsControl, Expander, ScrollViewer, lazy loading, property tree, tree view performance, 가상화, 지연 로딩, "VirtualizationMode.Recycling", "IReadOnlyList<T>", "ItemsSource", "DataTemplate", "data virtualization", "container recycling"]
status: active
checked_at: "2026-11-10"
context:
  framework: .NET 10 WPF
  platform: Windows desktop
---

## Guidance

UI virtualization creates visual containers only as items enter the visible range. Data virtualization and lazy construction determine when backing objects exist. Container recycling (`VirtualizationMode.Recycling`) can reuse a visual while scrolling; keep per-item state in the bound item.

1. **Lazy children:** give each row a child list that reports `Count` without building its children (an `IReadOnlyList<T>` that builds on first index or enumeration). An expand arrow needs only the count.
2. **Bind children on expand:** in the row's `DataTemplate`, leave the child `ItemsControl` collapsed with no `ItemsSource`; a trigger on the toggle's `IsChecked` sets `ItemsSource` and `Visibility`. A collapsed row then creates no child containers.
3. **One virtualized list:** flatten the section headers, notices and top-level rows into one list in the view model and show it in a single `ItemsControl` whose template has a `ScrollViewer` with `CanContentScroll="True"` and whose panel is a `VirtualizingStackPanel` (`VirtualizingPanel.IsVirtualizing`, `ScrollUnit="Pixel"`). Use a header item with an `IsExpanded` property that rebuilds the list, instead of an `Expander` per section.
4. **Cheap row text:** stop building a one-line summary of a nested value once it exceeds the display width, and fall back to a type name.

## Applicability and exceptions

An outer `ScrollViewer` around `ItemsControl`s, or an `ItemsControl` without a virtualizing panel, measures every item, so virtualization silently does nothing. Nested child lists in expanded rows are still not virtualized; cap their length or flatten them too. A `TreeView` with virtualization enabled is an alternative that was not compared.

## Checks

- Time the view from data assignment to layout complete (`UpdateLayout` after the dispatcher settles) on the largest real data set, against a budget.
- Count created rows or containers before and after, not only elapsed time.

## Evidence

A Windows .NET 10 WPF asset-inspection view (Debug, 2026-11-10) built rows faster and became usable sooner after deferred row construction and a single virtualized host. A heavily loaded run showed little margin in another view. Release latency, scrolling and memory were not measured. Microsoft describes conditions that disable virtualization and the difference between container recycling and data virtualization. [Microsoft, Optimizing performance for WPF controls](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/optimizing-performance-controls)
