# Code knowledge

Software implementation, systems, runtime behavior, and verification.

[Domain routing](../index.md) | [Storage and lifecycle](../../skills/vegabond-knowledge/references/storage.md)

<!-- onestep-catalog:start -->
Generated from canonical English metadata; edit detail files, not these rows.

| ID / title / kind | Summary | Scope / context | Keywords | Status / checked | Detail |
| --- | --- | --- | --- | --- | --- |
| K-CODE-UE-ENGINE-CHECKOUT / Confirm which engine source checkout is current before reading a custom Unreal engine [lesson] | An engine path environment variable can point at a stale checkout whose active source lives in a git worktree; check worktrees, branch and Build.version before drawing conclusions from engine source or history. | Projects built on a source-built or forked Unreal Engine located through an environment variable or registry association; {"engine": "Unreal Engine 5 source build", "vcs": "git with worktrees"} | Unreal Engine, custom engine, engine fork, git worktree, Build.version, EngineAssociation, engine source, stale checkout | active / 2026-11-06 | [K-CODE-UE-ENGINE-CHECKOUT](K-CODE-UE-ENGINE-CHECKOUT.md) |
| K-CODE-UE-RENDER-ORIENTATION / How to map an Unreal project's rendering setup before studying or optimizing it [method] | Classify the rendering path from renderer settings, find engine renderer changes by marker or history, and locate project render hooks by searching for view extensions, global shaders and shader files, before planning study or optimization. | Unreal Engine 5 game projects, especially ones with a custom engine and in-project rendering plugins; {"engine": "Unreal Engine 5.x", "platform": "Windows desktop"} | Unreal Engine, rendering, renderer settings, Nanite, Lumen, Virtual Shadow Maps, distance field shadows, static lighting, SceneViewExtension, ISceneViewExtension, RDG, FRDGBuilder, IMPLEMENT_GLOBAL_SHADER, usf, vertex factory, scalability, PSO | active / 2026-11-05 | [K-CODE-UE-RENDER-ORIENTATION](K-CODE-UE-RENDER-ORIENTATION.md) |
<!-- onestep-catalog:end -->
