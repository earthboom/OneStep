# Background and adaptive music

## Write for the listening window

Identify the scene's function, usual dwell time, audible foreground, and desired attention level. A BGM bed under speech can leave more rhythmic and spectral space around the voice. Start from a motif or texture that can survive repetition, then vary one or more of harmony, rhythmic density, register, or instrumentation. Check the result against dialogue and sound effects in the scene.

For a fixed-tempo loop with a constant beat unit, multiply the total number of those beats by 60 divided by BPM. For example, eight bars of 4/4 at 120 quarter notes per minute last 16 seconds, or 768,000 frames at 48 kHz. A frame contains one sample per channel. For changing tempo or meter, use the project's tempo map and confirm the exported boundaries in decoded frames. Plan how pickups and reverb tails cross the boundary. Audition multiple wraps of the export, including after target import or encoding. Use section or layer transitions where repeated structure becomes distracting.

## Author adaptive parts against a transition table

| Mechanism | Deliverable | Check |
| --- | --- | --- |
| Vertical layering | Synchronized stems with a common time origin, sample rate, and agreed loop length. Include an arrangement or routing note for allowed combinations. | Add and remove each layer while the shared transport continues. Check phase, harmony, combined peaks, and prominence of the foreground cue. |
| Horizontal resequencing | Sections with tempo, meter, entry and exit cues, harmonic relationships, and any transition segment. | Listen to every permitted direction, including a reversal. Inspect rhythmic continuity, timbre, pitch, loudness, and cut or tail at the seam. |
| Stinger or accent | A one-shot mapped to an event and an explicit immediate, beat, bar, or marker start rule. Document what happens if another cue arrives. | Trigger before and after the scheduling boundary and over a busy mix. Check both event legibility and musical delay. |

For each significant state edge, record source, destination, condition, timing rule, entry point, tail or fade, and handling of late or repeated requests. Decide when to cancel a pending change and what stop, pause, or reset means. A musical boundary can delay audible feedback, so give an urgent gameplay event its own immediate cue when needed. Use the target playback clock and test the captured output from that same path.

For example, an exploration loop can keep its pulse when an aligned percussion stem joins at the next schedulable bar. If threat clears before the join, cancel the pending addition. For a layer already playing, define its own release boundary and what happens if threat returns before that boundary. Test around the lead-time threshold, with repeated requests and rapid reversals, and through several wraps with both stems audible. Export the stems from the same time range, including any intentional leading silence. Route long tails consistently with the chosen loop contract.

Use [the adaptive music sources](sources.md#background-and-adaptive-music) for transition analysis and engine capabilities. OneStep's [Unreal timing evidence](../../../knowledge/game/K-GAME-TECH-MUSIC.md) used synthesized calibration tones and presubmitted transitions in a fixed tempo and meter. Apply its boundary and reversal checks to the current asset and verify actual sound under live input when that behavior matters.
