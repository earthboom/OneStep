---
id: K-GAME-STAGE-DIALOGUE
title: "Who selects, interrupts and commits a stage conversation across locales and saves?"
summary: "Bind stable line IDs to text, voice and portraits. Let stage placement select eligible conversations, a session own temporary controls, and persistent game state apply quest outcomes once."
kind: reference
scope: "Stage-based games with reactive lines, interactive dialogue or scripted scenes; proposed integration and regression checks"
keywords: ["stage dialogue","conversation","dialogue session","LineId","storylet","interruption","resume","localization","voice-over","Yarn Spinner","ink","FText","String Table","SignalEmitter","Sequencer Event Track","스테이지 대사","대화 세션","대사 ID","대화 중단","재개","재방문","보상 중복","현지화","자막"]
status: active
checked_at: '2026-11-23'
---

# Who selects, interrupts and commits a stage conversation across locales and saves?

## Guidance

Choose the authoring form around edits writers actually make. A table works for unrelated greetings. Use a script or graph when authors need to follow choices and reconverging branches. On revisits, conditional storylets need prerequisites, priority, repeat limits and a fallback. A dialogue-led game can put scenes, voice and transitions in a script. [Unreal data-driven gameplay](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-driven-gameplay-elements-in-unreal-engine) · [Yarn Spinner localization](https://docs.yarnspinner.dev/3.1/yarn-spinner-for-unity/assets-and-localization/inbuilt-localisation) · [Writing with ink](https://github.com/inkle/ink/blob/master/Documentation/WritingWithInk.md) · [Yarn Dialogue Runner](https://docs.yarnspinner.dev/components/dialogue-runner) · [Emily Short on Storylets](https://emshort.blog/2019/11/29/storylets-you-want-them/) · [Valve talk on dynamic dialogue](https://www.gdcvault.com/play/1015528/Do-Say-The-Right-Thing) · [Ren’Py dialogue and narration](https://www.renpy.org/doc/html/dialogue.html) · [Ren’Py voice](https://www.renpy.org/doc/html/voice.html)

Give each line a stable `LineId`, speaker, source text, owning node and translation context. Link portrait/expression keys, subtitle segments and takes to that ID. Mark revised text for translation or recording review. When splitting a line or changing its meaning, define what becomes of the old translation, takes and saved progress. Yarn tags, Unity Localization String Tables and Unreal `FText`/String Tables support related parts of this mapping; verify asset localization and voice packaging in the target build. [Yarn Spinner tags and metadata](https://docs.yarnspinner.dev/write-yarn-scripts/advanced-scripting/tags-metadata) · [Unity Localization String Tables](https://docs.unity3d.com/Packages/com.unity.localization%401.5/manual/StringTables.html) · [Unreal text localization](https://dev.epicgames.com/documentation/en-us/unreal-engine/text-localization-in-unreal-engine) · [Yarn Spinner voice-over and localization sample](https://docs.yarnspinner.dev/yarn-spinner-for-unity/samples/sample-guide-voice-over-and-localisation) · [Yarn Spinner and Unity](https://docs.yarnspinner.dev/3.1/yarn-spinner-for-unity/yarn-spinner-in-unity-scenes) · [Asset localization](https://dev.epicgames.com/documentation/en-us/unreal-engine/asset-localization-in-unreal-engine) · [Dialogue Wave API](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/UDialogueWave?application_version=5.8)

| Owner | Decision |
| --- | --- |
| Conversation definition | Lines, choices, branches and commands that the story can request. |
| Stage placement | Which conversation binds to a stable actor role and which approach, interaction or objective event makes it eligible here. |
| Dialogue session | Current line and choice, input focus, camera and voice lifetimes, priority, queueing, skip, interrupt and resume policy. |
| World state and save | Quest eligibility, one-time results, when a line counts as seen or heard, and supported resume points across versions. |
| Presentation | Display the selected line, speaker, expression, gesture, voice and subtitle. Notify the session of reveal, skip or choice. |

Let a reaction play during movement, give an explicit choice input focus, and use a timeline when a scene has fixed beats. When the player controls reading pace or branching, advance from the session's line/choice events. Request a progression change from its owner and cue the scene after confirmation. Unity Timeline `SignalEmitter` and Unreal Sequencer Event Track can bridge the authored beat to a command. Decide how that command behaves during skip, scrub or loop. [Running ink, state, and external functions](https://github.com/inkle/ink/blob/master/Documentation/RunningYourInk.md) · [Unity Timeline Signal Emitter](https://docs.unity3d.com/Packages/com.unity.timeline%401.8/api/UnityEngine.Timeline.SignalEmitter.html) · [Unreal Sequencer Event Track](https://dev.epicgames.com/documentation/en-us/unreal-engine/cinematic-event-track-in-unreal-engine)

## Applicability and exceptions

An offscreen reactive line can yield to an urgent cue; an essential instruction may need replay or a retained transcript. A bubble works for a short spatial reaction, while a fixed box with portraits can carry longer localized choices. Test anticipation of meaningfully different outcomes with players. An 88-participant text-adventure experiment supports this question within that context. Production accounts describe tools and interruption costs in particular games; the integration below is a proposed test. [Ren’Py side images](https://www.renpy.org/doc/html/side_image.html) · [Authors' paper](https://users.soe.ucsc.edu/~michaelm/publications/mateas-aiide2005.pdf) · [Research paper](https://cdn.aaai.org/ojs/12716/12716-52-16233-1-2-20201228.pdf) · [Greg Kasavin and Darren Korb talk](https://gdcvault.com/play/1027149/Breathing-Life-into-Greek-Myth) · [Developer talk](https://www.gdcvault.com/play/1024415/Do-You-Copy-Dialog-System) · [Sean Krankel talk](https://www.gdcvault.com/play/1024270/Building-Game-Mechanics-to-Elevate) · [Itay Keren's GDC talk on side-scrolling cameras](https://www.gdcvault.com/play/1022244/Scroll-Back-The-Theory-and) · [GDC talk on Celeste level layout and story](https://www.gdcvault.com/play/1024307/The-Gamer-s-Brain-How)

## Checks

1. Play approach → greeting → interact → choose → show result → restore control. Trigger a competing cue, walk away at a choice, remove a speaker, skip mid-voice and re-enter with an old save. Log the selection condition, priority and reason for ending. Confirm input, camera, subtitles and audio cleanup on each exit. Preview, retries and replay must produce the intended number of persistent rewards.
2. Check duplicate IDs, dangling branches, absent voice/portrait/translation and prior flags after editing shared dialogue. Revisit two existing stages. Verify line replacement, silent-line advance, mouth shape and camera restoration with actual reading and recording durations.
3. Pseudolocalize early and inspect the actual localized build for glyphs, Korean/Japanese/Chinese wrapping, supported right-to-left layout, substitutions, contrast and overlapping subtitle order. Test long text in edge-of-screen bubbles and nearby or absent speakers. [Xbox subtitle and caption guidelines](https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/104) · [Unicode line breaking algorithm](https://www.unicode.org/reports/tr14/)

## Evidence

The Firewatch production talk describes interruption and resumption, Hades documents voice production at scale, and ink documents persisted story state and external functions. These inform ownership and tests; no two-stage playtest, localization build or save migration was performed for this design. For animation source and reimport checks see [character sprite production](K-GAME-SPRITE-PRODUCTION.md). For narrative choice design see [narrative adventure](K-GAME-NARRATIVE-ADVENTURE.md). [Running ink, state, and external functions](https://github.com/inkle/ink/blob/master/Documentation/RunningYourInk.md) · [Greg Kasavin and Darren Korb talk](https://gdcvault.com/play/1027149/Breathing-Life-into-Greek-Myth) · [Developer talk](https://www.gdcvault.com/play/1024415/Do-You-Copy-Dialog-System)
