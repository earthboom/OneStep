# Sources for audio production

Research notes compiled 2026-11-24. Use papers for findings under their stated conditions, practitioner accounts for production choices worth trying, and standards and manuals for their documented scope. The procedures in this skill turn those observations into checks for the current asset. Consult current official documentation for a provider's controls, licenses, and output options when relying on them.

## Sound effects

| Source | What to apply and what to check |
| --- | --- |
| [van den Doel, Kry, and Pai, FoleyAutomatic (SIGGRAPH 2001)](https://persianney.com/kvdoelcsubc/publications/foleyautomatic.pdf) | Primary research on contact-driven sound, including impact, sliding, and rolling. Try separate excitation and resonances. Verify perceived material and motion with the current action. |
| [Perry Cook, Princeton Sound Lab physical modeling research](https://soundlab.cs.princeton.edu/research/phymod/) | Author's index and papers on physically informed percussion, modal synthesis, and stochastic events. Use the model family suited to the event, such as resonances for a strike or multiple collision events for a rattle. |
| [Andy Farnell, Designing Sound (MIT Press)](https://mitpress.mit.edu/9780262288835/designing-sound/) | Publisher overview of a procedural approach to sound. A practical starting question is which event parameters should change the rendered sound. The public overview establishes the book's scope. |
| [Lawlor and Neumann, Overwatch: The Elusive Goal: Play by Sound (GDC 2016)](https://www.gdcvault.com/play/1023010/Overwatch-The-Elusive-Goal-Play) | Developer case. The session describes a sound design goal tied to player decisions. Test whether a listener identifies the current cue against competing cues. |
| [Blizzard, Talent Tree: Sound Designer, Overwatch 2](https://overwatch.blizzard.com/en-gb/news/24226699/talent-tree-sound-designer-overwatch-2/) | Firsthand account of starting with gameplay role and character fantasy and exploring physical Foley materials. Derive the event's identity before selecting layers. |
| [Kevin Regamey, The TUNIC Audio Talk (GDC 2023)](https://www.youtube.com/watch?v=sCIK78OHrIY) | Developer talk description covers early creative direction, gameplay-informed sound decisions, effect design, and implementation. Use as a case-study entry point for a further production decision. |

## Background and adaptive music

| Source | What to apply and what to check |
| --- | --- |
| [Elizabeth Medina-Gray, Analyzing Modular Smoothness in Video Game Music (2019)](https://www.mtosmt.org/issues/mto.19.25.3/mto.19.25.3.medina.gray.html) | Research and analyses of sequential and simultaneous relationships. Compare meter, timbre, pitch, volume, and abruptness at each seam. Interpret an intentional break by its function. |
| [Austin Wintory, From JOURNEY to ERICA](https://awintory.medium.com/from-journey-to-erica-214355002896) | Composer's account of interactive scoring. Use as a source of examples for deciding which moments need a fixed sequence and which require a response to player state. |
| [Audiokinetic, Wwise Project Adventure](https://www.audiokinetic.com/download/documents/WwiseProjectAdventure_en.pdf) | Official tutorial on music segments, source/destination transitions, and optional bridge segments. Check authored cues and matching transition rules in the installed version. |
| [FMOD, Studio 2.04 Authoring Events](https://www.fmod.com/docs/2.04/studio/authoring-events.html) | Official reference for timeline regions, parameter conditions, and quantization. Verify region timing with the current event and active playback path. |
| [Epic, Quartz overview](https://dev.epicgames.com/documentation/unreal-engine/overview-of-quartz-in-unreal-engine?lang=en-US) and [MetaSounds overview](https://dev.epicgames.com/documentation/en-us/unreal-engine/metasounds-the-next-generation-sound-sources-in-unreal-engine) | Official Unreal routes for playback scheduling and sample-accurate source graph operations respectively. Test the particular add, remove, fade, and cancellation behaviors the implementation needs. |
| [Unity, AudioSource.PlayScheduled](https://docs.unity3d.com/ScriptReference/AudioSource.PlayScheduled.html) | Official DSP-time scheduling API. Give the audio path sufficient preparation time and check actual output after target import. |

## Spoken voice

| Source | What to apply and what to check |
| --- | --- |
| [Shure, Microphone Techniques for Recording](https://content-files.shure.com/Pubs/microphone-techniques-for-studio-recording/microphonetechniques-recording-guide.pdf) | Manufacturer's recording guide. Compare working distance, orientation, plosives, and proximity effect on a test line. |
| [Audacity, Noise Reduction](https://manual.audacityteam.org/man/noise_reduction.html) | Official guidance on noise profiles and processing artifacts. Use a representative noise-only selection for steady noise and audition what the effect would remove. |
| [iZotope, RX as a plug-in or standalone editor](https://www.izotope.com/community/blog/rx-as-a-plugin-vs-as-a-standalone-audio-editor) | Practitioner workflow examples for different contexts and repairs. Assess isolated clicks or residual noise in the final bed before processing an entire performance. |
| [Jean-Marc Valin, A Hybrid DSP/Deep Learning Approach to Real-Time Full-Band Speech Enhancement (2018)](https://arxiv.org/abs/1709.08243) | Research describing RNNoise's combination of estimated critical-band gains and pitch filtering. Verify artifacts and intelligibility on the actual recording. |
| [W3C, SSML 1.1](https://www.w3.org/TR/speech-synthesis11/) | Standard for pronunciation, breaks, and prosody markup. The chosen TTS provider determines which controls are available and how they render. |

## Songwriting, groove, and arrangement

| Source | What to apply and what to check |
| --- | --- |
| [Song Hawsuk, “This Damn Love”: Sexual Politics of Ballad (2017)](https://journal.kci.go.kr/musicology/archive/articleView?artiId=ART002245331) | Research on the historical Korean pop ballad and its dramatic intensification. Explore lyric, melodic contour, harmony, and the location of emotional peaks in the current brief. The historical repertoire bounds the observations. |
| [Kim Sunghyun, Climax and Final Notes in K-pop Ballads (2025)](https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART003264097) | Observational analysis of selected 2015–2024 chart-topping ballads. Compare the lead's peak with the closing gesture. The song sample limits the generalization. |
| [Witek et al., Syncopation, Body-Movement and Pleasure in Groove Music (2014)](https://doi.org/10.1371/journal.pone.0094446) | Original listener survey using funk drum breaks. Intermediate syncopation rated highly in these stimuli. Use the result to motivate a comparison of rhythmic density, with no prescribed setting for R&B or rap. |
| [Questlove, 2013 lecture and demonstrations](https://www.redbullmusicacademy.com/lectures/questlove-new-york-2013/) and [D’Angelo, 2014 conversation](https://www.redbullmusicacademy.com/lectures/dangelo/) | Firsthand accounts of groove and session collaboration. Compare the relationship between specific parts and the beat, preserving a usable pulse. These accounts describe particular artists and sessions. |
| [Ben Duinker, Segmentation, Phrasing, and Meter in Hip-Hop Music (2021)](https://doi.org/10.1093/mts/mtab003) and [Functions of Expressive Timing in Hip-Hop Flow (2022)](https://online.ucpress.edu/jpms/article-abstract/34/1/90/120447/Functions-of-Expressive-Timing-in-Hip-Hop-Flow) | Primary analyses of phrasing, meter, and timing against the beat. Mark vocal grouping and accents, then compare intentional alignment and displacement. |
| [Dennis DeSantis, Making Music (Ableton)](https://cdn-resources.ableton.com/resources/uploads/makingmusic/MakingMusic_DennisDeSantis.pdf) and [Ableton Live 12, Using Grooves](https://www.ableton.com/en/live-manual/12/using-grooves/) | Production strategies and tool-specific groove controls. Compare arrangement by subtraction and apply measured timing and velocity changes to selected parts. |

## Measurement and delivery

| Source | What to apply and what to check |
| --- | --- |
| [ITU-R BS.1770-5](https://www.itu.int/rec/R-REC-BS.1770-5-202311-I) | Normative audio programme loudness and true-peak measurement algorithms. Select the delivery target from the actual specification. |
| [EBU R 128](https://tech.ebu.ch/publications/r128) and [EBU Tech 3285](https://tech.ebu.ch/publications/tech3285) | Broadcast loudness recommendations and BWF metadata specification. Check whether the delivery requires either and whether its tools preserve the fields. |
| [Spotify for Artists, Loudness normalization](https://support.spotify.com/us/artists/article/loudness-normalization/) | Service-specific normalization behavior and delivery advice. Compare streaming preview assumptions with the intended master and destination. |
| [FFmpeg filters](https://ffmpeg.org/ffmpeg-filters.html#ebur128) and [ffprobe](https://ffmpeg.org/ffprobe.html) | Official measurement and inspection references. Probe the actual deliverable and interpret metrics in context. |

## Tools and rights

| Source | What to apply and what to check |
| --- | --- |
| [Kreuk et al., AudioGen (ICLR 2023)](https://arxiv.org/abs/2209.15352) and [Copet et al., MusicGen (NeurIPS 2023)](https://proceedings.neurips.cc/paper_files/paper/2023/hash/94b472a1842cd7c56dcb125fb2765fbd-Abstract-Conference.html) | Primary research for text-guided audio and controllable music generation. Assess event order, structure, timing, and fidelity on the actual render. Use the [AudioCraft weight license](https://github.com/facebookresearch/audiocraft/blob/main/LICENSE_weights) for that project's weights and check the terms of the exact checkpoint. |
| [ElevenLabs, Create sound effect](https://elevenlabs.io/docs/api-reference/text-to-sound-effects/convert) | Official example of generation controls for duration, format, and looping. Verify version-dependent support and inspect the resulting loop and file. |
| [Suno, Paid subscription rights](https://help.suno.com/en/articles/9601665) | Provider account of commercial-use terms. Recheck the plan, the asset's relevant dates, and the current terms before relying on rights for delivery. |
| [Freesound FAQ](https://freesound.org/help/faq/) and [U.S. Copyright Office, Sound Recordings](https://www.copyright.gov/register/sr-definition.html) | Library guidance on sound-level licenses and a U.S. primary reference distinguishing composition and recording. Verify the specific asset, use, and jurisdiction where relevant. |
