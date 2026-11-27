# Sound effects

## Design the cue around its event

Define the trigger, listener perspective, and what must be recognized during competing sounds. For synced action, mark the visual contact or decision frame and name the exact audio transient that should land there, such as the second clack of a latch. Set that transient's offset from the file start before trimming or applying fades. Place all versions at the same timeline position and compare the transient offset and audible sync against picture. A short UI family can share a timbral motif while direction, pitch contour, or duration distinguishes confirm, error, and cancel. Keep alert meaning recognizable in all supported variations.

| Event | Build the first pass | Check it in use |
| --- | --- | --- |
| Impact or interaction | Align a quick contact transient, material resonance or body, and optional debris or decay. Audition each layer's contribution. | The contact reads on time in-context. Check whether layered starts reinforce, smear, or cancel in mono. |
| Footsteps or Foley | Record or select multiple takes per contact surface and intensity. Keep the weight and material consistent while varying performance. | Play a walk, a run, and a surface change with the intended cadence. Check repeated choices and the transition between surfaces. |
| Wind, machinery, or ambience | Build a stable bed and place distinct events separately if repeated landmarks reveal the cycle. Author the loop or parameter boundaries explicitly. | Repeat several cycles at the intended level, then test start, stop, and state changes. Listen for seam clicks, recognizable recurrence, and phasey crossfades. |
| Designed UI, magic, or machinery | Combine shaped tones, filtered noise, and controlled transients. Use pitch motion for gesture, resonance for material, and an envelope for timing. | Test short or rapid retriggers and overlapping cues. Check whether choices remain distinguishable at low playback level. |

## Choose sources and variation

- For recorded Foley, keep a dry clean take, capture useful variation at a stable mic position, and name takes by action and surface. Compare the rhythm and weight against picture or animation before adding processing.
- For synthesis, use a short broadband excitation with one or more independently decaying resonances for a ringing contact. For scraping, use sustained irregular excitation during motion. Test whether harder contact changes attack or brightness as intended. Limit randomization to ranges that preserve recognition. [Contact modeling and procedural sound](sources.md#sound-effects)
- For a generator brief, specify event order, material, perspective, approximate duration, and the amount of tail. For example, request a close, single wooden latch closure with two contacts, a sharp tick followed by a lower clack, and a dry stop suitable under dialogue. If the generated attack timing drifts, edit it against the cue point or build controllable layers.
- If spatial treatment belongs to the runtime, audition a dry source through the target attenuation, occlusion, and room response. Encode perspective in the file when the fixed perspective is part of the deliverable. Check how stereo import, spatialization, and voice limits behave in the target engine. OneStep's [spatial audio evidence](../../../knowledge/game/K-GAME-TECH-SOUND.md) documents scoped Unreal tests for these distinct controls.

When packaging variations, keep a stable event ID and name files with meaningful surface, intensity, or variation labels. Remove unintended leading silence while preserving any intentional anticipation. For a layered one-shot, compare solo and summed playback at the required position. For a looping effect, define the loop region and whether a release tail is triggered separately.
