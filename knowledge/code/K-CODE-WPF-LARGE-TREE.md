---
id: K-CODE-WPF-LARGE-TREE
title: How to keep a WPF property tree with thousands of rows responsive
summary: Build child rows on first read, bind a row's children only while it is expanded, and show the section headers and top-level rows as one flat virtualized list. Expanders that each hold a plain ItemsControl inside a ScrollViewer create every row.
kind: lesson
scope: WPF views that show large hierarchical data (property grids, Details panels, tree-like lists) with ItemsControl templates
keywords: [WPF, virtualization, UI virtualization, VirtualizingStackPanel, CanContentScroll, ScrollUnit, VirtualizationMode, ItemsControl, Expander, ScrollViewer, lazy loading, property tree, tree view performance, 가상화, 지연 로딩]
status: active
checked_at: "2026-11-10"
context:
  framework: .NET 10 WPF
  platform: Windows desktop
---

## Guidance

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

Provenance: a standalone asset viewer's Details panel, 2026-11-10, Debug build. The largest object had 1,263 top-level rows (75,937 if fully expanded). Building rows fell from 492–864 ms to 26–58 ms. Tab-ready time fell from 7,969 ms to under the 1,000 ms budget. One full test run under heavy machine load had another view at 1,034 ms, so the Debug margin was small.

Not verified: Release timings, scrolling smoothness, memory use.
