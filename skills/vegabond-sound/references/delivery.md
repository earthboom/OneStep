# Mix, delivery, and tools

## Choose a production path

| Requirement | Method and evidence |
| --- | --- |
| Precise timing, repeatable variation, editable score, or aligned stems | DAW timeline, MIDI with a documented instrument/render path, offline synthesis, or supported game-audio authoring. Export and compare the exact handoff files. A MIDI file needs playback instruments to become rendered audio. |
| Human performance and room character | Record available performers or Foley. Preserve dry sources and relevant edit handles when the user needs further editing. |
| Spoken script at scale | Record or use an available, permitted TTS provider that supports the language and delivery. Test exact words and difficult pronunciations before batching. |
| Generative sound or music | Check actual controls, provider access, allowed inputs, and supported exports. Use output as a candidate, then edit and measure it. Record model, settings, and asset-level provenance where needed for reuse. |
| Existing audio inspection or light repair | Use a DAW, waveform/spectral editor, or an available tool such as FFmpeg/ffprobe. Verify that the repaired output decodes and compare before and after in context. |

Use the requested provider when its capabilities, terms, and supported access fit. Keep external inputs limited to authorized content for this asset. When a OneStep task requires its restricted Suno data path, use the documented request contract in `prototypes/SunoRestricted/README.md` from the full checkout, if available. Consult [tool and rights sources](sources.md#tools-and-rights) for provider-specific controls and terms when choosing or distributing assets.

## Define the output contract

- Start with the downstream specification. For a game or video handoff with no stated spec, 48 kHz PCM WAV is a reasonable working default. Use 24-bit PCM if accepted, and use the target's required rate and bit depth for the final delivery. Preserve a source-quality master when useful. Use mono for point sources when the runtime expects it, and stereo or the requested layout when its spatial image is intentional.
- Confirm whether source sessions, dry/wet or instrumental versions, short cuts, alternate takes, loop point metadata, and editable stems are requested. For a timed loop or set of stems, record the exact frame range with an exclusive end, rate, and time origin. Embed loop markers only in a format the consumer honors, and retain the values in the handoff if the import path strips them.
- Record relevant provenance for sampled, library, generated, or performer material. Track asset/page ID, source or author, applicable license or agreement and attribution, plus any use limits. Musical composition, lyrics, recorded performance, and model/checkpoint terms can involve different rights. Check applicable conditions for the destination.

## Check the delivered artifact

1. Compare at similar perceived level. Listen for clarity and cue meaning in context, then solo for audible defects. Review at the playback devices or mono fold-down that matter to the request. For revisions, compare against the source at the same norm and identify the requested change.
2. Inspect type, duration or exact frame count, channels, sample rate, and bit depth when required. Decode the exported file and check faults such as dropouts, clipping, wrong start, extra tail, or silence. For a lossy output, check its decode and the target app's timing or gapless behavior.
3. Measure sample peaks or true peak as required and apply destination-specific loudness criteria. Integrated LUFS is a program metric that can be unhelpful or unavailable on very short cues. Match cue families by audibility and function in context. ITU-R BS.1770 defines measurement algorithms. EBU R 128 applies to its broadcast use case. Spotify's published loudness value describes playback normalization. See [measurement sources](sources.md#measurement-and-delivery).
4. For loops, repeat the decoded region through wraps and inspect timing and discontinuities. A waveform boundary measurement helps locate a click. Audition the musical handoff and overlapping tail as well. For interactive assets, capture representative gameplay or middleware output and compare to the contract for timing, audibility, and transitions.

With FFmpeg tools on PATH, use the following examples to inspect a final file. Read integrated and true-peak output with the applicable measurement scope. For a WAV whose audio time base and duration permit exact inference, derive frames from the inspected fields or count sample frames in decoded PCM.

```text
ffprobe -v error -select_streams a:0 -show_entries stream=codec_name,sample_rate,channels,channel_layout,bits_per_sample,bits_per_raw_sample,duration_ts,time_base:format=duration -of json "output.wav"
ffmpeg -hide_banner -i "output.wav" -af "ebur128=peak=true" -f null -
```

Use a handoff note proportional to the task. Give file paths, intended placement or import settings when relevant, and the checks actually performed. List any unavailable listening, runtime, or provider checks as open.
