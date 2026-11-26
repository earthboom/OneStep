---
id: K-GAME-EFFECT-EVENT-PLAYBACK
title: "Does a 2D effect show the right event at its actual time and place?"
summary: "Drive one-shots from confirmed events, choose an attachment or a world position, and inspect exported actor and effect tracks alone and together to diagnose missing cues."
kind: method
scope: "2D cels, particle texture sheets and flipbooks attached to characters or emitted into world space"
keywords: ["2D effects","landing dust","event timing","one-shot","world space","local coordinates","exposure","draw order","SpriteFrames","GPUParticles2D","Texture Sheet Animation","착지 먼지","이펙트","월드 좌표","노출 시간","그리기 순서","가림","플립북"]
status: active
checked_at: '2026-11-23'
---

# Does a 2D effect show the right event at its actual time and place?

## Guidance

Choose the trigger, anchor, lifetime and draw order for each effect. A charge follows the hand, a released object takes its starting point once, and an arrival pulse waits for confirmed reception. Ground dust stays at confirmed contact even after the actor moves. Record actor and effect on one timeline with independent exposures. An actor may hold the compressed pose across two dust cels. Godot SpriteFrames represents relative duration; at 10 FPS and normal speed, a 1.2 hold lasts 120 ms. Unity Texture Sheet Animation can use lifetime, speed or FPS, so changing particle lifetime can shift a cel tied to normalized life. [Godot SpriteFrames duration](https://docs.godotengine.org/en/stable/classes/class_spriteframes.html#class-spriteframes-method-get-frame-duration) · [Godot GPUParticles2D coordinates and one-shot restart](https://docs.godotengine.org/en/stable/classes/class_gpuparticles2d.html) · [Unity Texture Sheet Animation time modes](https://docs.unity3d.com/6000.0/Documentation/Manual/PartSysTexSheetAnimModule.html)

Sketch the first and last important shapes, then author the ambiguous interval where a hand passes behind a prop or water breaks into droplets. Stage anticipation and recovery within the game's action budget. Stagger births and deaths across a sustained flame, and use force direction and changing negative spaces to convey material. For a warning, compare its apparent boundary with the affected area and its visual priority with nearby actions. [Paper, Figure 1 and §4](https://studios.disneyresearch.com/wp-content/uploads/2019/03/BetweenIT-An-Interactive-Tool-for-Tight-Inbetweening-Paper.pdf) · [Authors’ abstract, paper and demonstration](https://www.cse.iitb.ac.in/~paragc/publication/2016-icvgip-01/) · [Paper](https://arxiv.org/abs/2405.17933) · [Authors’ demonstration](https://doubiiu.github.io/projects/ToonCrafter/) · [Official GDC video](https://www.youtube.com/watch?v=Mw0h9WmBlsw) · [Slides on anticipation, timing and gameplay](https://media.gdcvault.com/GDC2014/Presentations/Cartwright_Muriel_Animation_Bootcamp_Fluid.pdf) · [Keyser and Graf interview](https://www.toonboom.com/jason-keyser-and-chris-graf-on-the-secrets-behind-the-magic-of-2d-fx) · [Timing and rough motion studies](https://www.vfxapprentice.com/blog/the-soul-of-effects-what-is-timing-in-vfx) · [Riot development examples](https://www.leagueoflegends.com/en-us/news/dev/clarity-in-league/) · [Riot art education videos and materials](https://www.riotgames.com/en/artedu/visual-effects) · [GDC VFX slides](https://media.gdcvault.com/gdc2017/Presentations/Chamberlin_Keyser_ArtisticPrinciplesVFX.pdf)

## Applicability and exceptions

Authored clips can schedule a known contact in a preview. Variable jump height, cancellation or missed contact requires the corresponding game-state event. Vector in-betweening and video interpolation research informed the sketch decisions; the results do not measure engine latency, pixel-alpha quality or player perception.

## Checks

- Replay exported actor alone, effect alone and the composite at target speed on light and dark surfaces. Step across contact and expiry; move actor and camera independently. Check a missed event, mid-cycle cancel, repeated trigger, and tail cleanup. On a loop inspect the seam for a duplicated hold.
- If the effect appears in isolation, test occlusion before retiming it. Split near and far lobes across the actor if necessary. For a halo inspect edge RGB and straight versus premultiplied alpha. Neighboring colors suggest atlas padding/sampling. For additive light that vanishes on a bright surface, test an alpha-blended core. [Godot CanvasItem blend modes](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/canvas_item_shader.html) · [Aseprite CLI](https://www.aseprite.org/docs/cli/)
- Ask an unfamiliar viewer what happened, where and in which direction at normal speed. With overlapping effects, inspect warning visibility, repeated flashes and target-device frame time. Preserve the cue if a lower-intensity version is needed. [Xbox Accessibility Guideline 118](https://learn.microsoft.com/en-us/gaming/accessibility/xbox-accessibility-guidelines/118)

## Evidence

In a decoded dock-landing preview, event timing was correct, but the boots hid most of the dust onset. Moving just the near lobe to the front increased the visible portion from 23 to 46 of 71 opaque pixels. On this clip contact was at 120 ms and dust cleared at 420 ms. These are measured mask exposure and authored timings in six states on two backgrounds. Human detection, smoothness, engine input latency and target performance were outside the test. [Drawing and export record](../../output/2d-character-test/landing-effects-01/example.md) · [Pivots, cel times and layers](../../output/2d-character-test/landing-effects-01/timing.json) · [Production guide](../../skills/vegabond-image/references/2d-effects-and-motion.md)
