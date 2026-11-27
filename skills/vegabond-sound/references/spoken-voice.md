# Spoken voice

## Prepare the script and performance

Keep one stable line ID per utterance for localization, retakes, and integration. Record the exact text, intended listener, speaking objective, delivery or intensity, timing constraint, and pronunciation notes when important. Separate line text from direction and pronunciation hints. Flag names, numbers, units, abbreviations, and mixed-script phrases that can be read multiple ways.

For Korean lines, confirm speech level and character relationship, then read the phrase naturally at speed. Inspect the intended reading of 받침 and liaison, Sino-Korean versus native Korean numbers, and mixed Korean and foreign proper names. Use a supplied pronunciation or ask for one where a name's correct reading materially affects delivery. Preserve locked wording and keep any TTS spelling variants in a separate rendering field.

## Record, synthesize, or repair

- **Recording and ADR.** Choose a quiet position and capture a short room-tone bed with the same mic and gain. Keep mic geometry and pop protection consistent. Record a test line and the loudest expected delivery before committing. For ADR, compare phrase onset, visible closures, breaths, and intention against picture. Keep the original or an edit-safe copy for pickups.
- **TTS.** Confirm the language, controls, output format, and permitted use of the selected provider. Use an eligible stock voice when the brief leaves the voice open. For an identifiable real voice, check its license or documented permission and apply relevant disclosure requirements. Use speaking direction, line context, and supported pronunciation markup or dictionaries where useful. Check an ordinary line and a difficult line before generating a batch. Listen to each exact line for omissions, substitutions, pronunciation, natural pauses, inconsistent character, and unwanted generated material. [Speech sources](sources.md#spoken-voice)
- **Editing.** Select and align takes first. Use clip gain and short fades to join them with matching room tone. Repair isolated plosives, mouth clicks, or hum where they distract. Compare conservative denoise against the untreated take at similar playback level, especially consonants, breaths, and endings. Use de-essing or dynamics for an audible problem, and shape intelligibility against the actual music and effects.

For a batch, hand off files with stable IDs and only the requested variants. Include matching room tone or edit handles when the downstream editor needs them. Listen both solo and in the scene at normal speed, especially the starts and ends of short lines, stressed syllables, and names. A transcript comparison can locate omissions. Human or tool-assisted listening is needed to establish intelligibility, emotion, and naturalness.
