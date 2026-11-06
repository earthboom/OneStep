---
id: K-CODE-UE-LOC-MERGE
title: Merge conflicting Unreal localization manifest and archive files semantically and recompile locres with a parity proof
summary: Flatten Game.manifest and each Game.archive to (namespace path, key) entries, three-way merge the entries, write the result in the kept side's own format, then recompile Game.locres with the GatherText commandlet only after proving that the same engine reproduces the kept side's committed locres byte for byte.
kind: method
scope: Unreal Engine projects whose Content/Localization/<target>/ manifest, archive and locres files conflict in a git merge between two long-lived branches
keywords: [Unreal Engine, localization, Game.manifest, Game.archive, Game.locres, Game.po, GatherText, GenerateTextLocalizationResource, Game_Compile.ini, UTF-16LE, three-way merge, semantic merge, locres parity]
status: active
checked_at: "2026-11-06"
context:
  engine: Unreal Engine 5.3 project data compiled with a 5.8 source build
  platform: Windows desktop
  format: manifest and archive are UTF-16LE BOM JSON with tab indentation and LF
---

## Guidance

1. Extract the three stages of every conflicted manifest and archive with `git show <base>:<path>`, `git show <ours>:<path>` and `git show <theirs>:<path>` into a scratch tree. Do not resolve them as text: the files are large JSON trees and git's line merge produces duplicate or broken namespaces.
2. Parse each file as UTF-16LE JSON after the 2-byte BOM. Flatten to a map keyed by (tuple of nested `Namespace` values, `Key`). In the manifest the value is the `Source` object plus the key's other fields; in an archive it is the child entry without `Key`.
3. Three-way merge the maps: equal on both sides keeps; changed on one side only takes that side (add, modify or delete); changed differently on both sides is a conflict to list for a person, kept as ours meanwhile.
4. Apply the merged map as a delta onto a deep copy of the kept side's tree. Insert new entries in the order the tree already uses (detect whether children are sorted by source text and keys by key before inserting) and remove empty `Children` or `Subnamespaces` arrays. Flatten the result again and assert it equals the merged map.
5. Serialize with the kept side's format: BOM, `json.dumps(ensure_ascii=False, indent='\t')`, LF, and a trailing newline if the kept side has one. Prove the serializer first: parse and re-serialize each input and compare bytes. A side that differs only by a missing trailing newline is still safe to merge.
6. Recompile every `Game.locres` instead of choosing a side. Make a dummy project: a minimal `.uproject`, the project's `Config/Localization/<target>_Compile.ini`, and `Content/Localization/<target>/` holding the merged manifest and archives. Run `UnrealEditor-Cmd.exe <dummy>.uproject -run=GatherText -config=Config/Localization/<target>_Compile.ini -unattended -nullrhi -nosplash -NoShaderCompile`.
7. Prove parity before trusting the output: compile the kept side's committed manifest and archives first and require byte identity with its committed locres for every culture. Only then compile the merged inputs and stage those locres.
8. Treat `Game.po` as a derived export, not a source: it can lag the archive by many entries and git merges it as text. Compare it against the merged archive only to detect merge mistakes, never to decide translations.

## Applicability and exceptions

Applies when both branches touched the same localization target and the archives are JSON (the default UE format). An engine of a later minor version compiled the locres identically here, but that must be re-proven per engine build and per project with the parity step. A plugin listed in the dummy project's engine that fails to load (here `NNEDenoiser` in a source build without its shader module) must be disabled in the `.uproject` `Plugins` array, otherwise the commandlet exits before compiling. If the project's custom engine is available, prefer it for the compile. The method does not handle entries that both sides changed differently; those stay a human decision.

## Checks

- Round trip: `serialize(parse(file)) == file` for the kept side; report any other side's difference and confirm it is only the trailing newline.
- Entry counts: merged entries == kept side entries + the other side's additions - deletions, identical across the manifest and every culture archive.
- Parity: compiled locres of the kept side's committed inputs == committed locres, all cultures, before compiling the merge.
- Content: parse or byte-search the merged locres for every key the other side added and for every key the kept side added since the merge base; both sets must be present. ASCII keys and translations are stored as 1-byte ANSI strings inside locres, so search them as ASCII bytes, and non-ASCII text as UTF-16LE.
- `.po` cross-check: entries present in the `.po` but absent from the archive on all three sides are pre-existing staleness, not merge loss.

## Evidence

Observed in a UE 5.3 game project merge of a hotfix branch into main on 2026-11-06: 1 manifest and 10 culture archives conflicted; flattening gave 14364 base, 14557 ours and 14378 theirs entries; the other side added 14 keys and modified up to 875 manifest entries (source metadata) and 4 to 37 translations per culture; zero both-sides conflicts. The committed locres were reproduced byte for byte by a 5.8 source-build `UnrealEditor-Cmd.exe` through a dummy project after disabling one plugin, and the merged locres contained all 14 added keys and all 193 keys the kept side had added. The `.po` files lagged the archives by 1245 entries on every side. Originating project: a studio UE5 game; its paths and keys are omitted.

Not verified: engines other than that 5.8 build, archives in the legacy non-JSON format, and merges where both sides change the same key.
