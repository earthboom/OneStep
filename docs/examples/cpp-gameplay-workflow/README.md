# C++ gameplay workflow examples

These two staged examples apply the [C++ project guidelines](../../../skills/vegabond-code/references/cpp-project-guidelines.md) and the [gameplay framework design procedure](../../../skills/vegabond-code-design/references/gameplay-framework.md). Each starts with one optional encounter, adds a second, and verifies the actual game entry point with neither pack, each pack alone, and both packs. Each extension adds one authored content file.

| Example | What the checks exercise |
| --- | --- |
| [Crossing Tactics](native-tactics/README.md) | C++17 command validation, player and enemy turn order, and a deliberately broken sibling dependency caught by the B-only test. |
| [Pulse Arena](unreal-action/README.md) | Unreal Engine 5.8.3 gameplay input, world-time cooldowns, and physically distinct startup content inventories. |

The examples include source, rerun instructions, and selected observations. Recorded read traces use repository-relative paths for shared guidance and `fixture/` for the isolated example's instructions. Rebuilding locally creates the executable or Unreal module needed to rerun the checks. The [C++ gameplay framework knowledge](../../../knowledge/code/K-CODE-CPP-GAMEPLAY-FRAMEWORK.md) provides the architectural background.
