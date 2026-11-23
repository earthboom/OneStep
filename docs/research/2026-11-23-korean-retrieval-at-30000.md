# Retrieving knowledge and incidents with Korean paraphrases across 30,000 records

## Which questions counted as correct?

We added 29,828 synthetic documents to the 172 canonical records from the same date. There were 14,914 synthetic knowledge records and 14,914 synthetic incident records. Across 12 topics, including camera clipping through walls, reverse-parking warnings, music loudness measurement, and worker restarts, we generated documents with distinct part numbers and body text. Both stores go through actual Markdown and metadata validation. Empty files represented Korean translations for existence checks. The production stores and original evidence received no evaluation documents.

We fixed the expected answers and result counts before changing the search implementation. For each of three topics we wrote three Korean questions and checked whether the target document appeared in the top three in an unrestricted search with no store or domain specified. The other five covered an exact technical name, an incident ID, two synthetic documents with similar topics but different causes, and a nonexistent identifier. For neighboring questions we specified both the document to find and the incident to exclude from the top results. [Questions, expected answers, and counterexamples](../../skills/vegabond-knowledge/tests/scale_korean_cases.json)

Before the change, the Korean inputs “뒤로 달리면 시점이 주인공을 앞질러요” (when I run backward, the camera overtakes the character) and “뒷걸음치자 화면이 몸체 앞쪽으로 넘어간다” (when I stepped backward, the view moved in front of the body) both returned nothing. The query “배경음 멈춤을 연달아 눌렀더니 다음 재생이 늦어진다” (pressing background-music stop repeatedly delays the next playback) returned results but missed the duplicate-stop incident. The query “후진할 때 카메라가 캐릭터보다 앞으로 튀어나와요” (when reversing, the camera jumps ahead of the character) ranked the correct result third in the small store, then lost it from the top three when similar documents were introduced.

When reversing, viewpoint, and overtaking appear together, the search looks for position-correction terminology for a fixed-direction camera. When audio, stop, repetition, and playing again appear together, it looks for duplicate-stop terms. When internal representation, caller, and independence of change appear together, it looks for information hiding. Compound terms recovered by these combinations receive the same weight as explicitly entered compound terms. The results expose the terms used for expansion. No rule maps to a specific document ID.

## Results

On Windows build 26300, Python 3.12.3, and PyYAML 6.0.3, we ran both search implementations sequentially on the same directory. Times below run from process startup through result receipt and exit. Both versions read 30,000 records for the initial index. Subsequent searches reread zero canonical records.

| 30,000 records, identical questions and documents | Before | After |
| --- | ---: | ---: |
| Correct result in top three for Korean paraphrases | 3/9 | 9/9 |
| Correct result ranked first for Korean paraphrases | 1/9 | 8/9 |
| Overall judgments, including identifiers, distractors, and empty results | 8/14 | 14/14 |
| Mean reciprocal rank of the first correct result for the 13 questions with designated answers | 0.4487 | 0.9615 |
| Initial indexing and incident ID lookup | 383.93 s | 212.49 s |
| Incident ID lookup using existing index | 47.33 s | 3.30 s |
| Existing-index lookup for Korean input ‘카메라’ (camera, 2,518 matches) | 28.46 s | 3.75 s |
| Existing-index lookup for Korean input ‘뒤로 달리면 시점이 주인공을 앞질러요’ | 49.42 s | 4.13 s |
| Search for a new phrase after editing one document | 61.74 s | 3.50 s |

All three camera formulations placed the target first. Across the camera, music, and module-boundary cases, the only question that placed it second was the Korean input “곡을 끄고 또 껐더니 재생을 다시 눌러도 한 박자 늦게 시작해” (after stopping the track twice, pressing play again starts it a beat late). The game music knowledge document ranked first. Questions on camera clipping through walls and loudness calibration both ranked their respective synthetic answers first, with the forbidden incident absent from the top three. In the edit test, the helper reread just one canonical file, and searching the new phrase found that document alone.

During file enumeration the helper obtains modification time and size from directory entries and compares them with the cache. It filters out terms that cannot match before checking field boundaries, and writes JSON row by row when replacing the cache. Across three individual searches, index preparation after the improvement took 1.94–2.50 seconds. We ran each command once per version without clearing the OS file cache. Some measurements overlapped with regression tests, so machine load contributed to the timing differences in the table.

**Results from 50 questions run as individual commands.** We used the 14 questions above, three additional formulations and three controls with similar symptoms, and 30 questions selected from existing evaluation sets using a fixed seed. All 50 distinct questions passed their specified judgments, with zero canonical rereads. Median time was **3.97 seconds**, P95 was **5.64 seconds** (48th fastest), and the range was **2.22–8.44 seconds**. P95 exceeded the project's proposed two-second target. Combining three individual lookups with `--query` returned the same IDs in the same order in **3.95 seconds**. The three individual runs totaled **11.17 seconds**. [Project measurement criteria](../../skills/vegabond-knowledge/references/search-scale.md)

The relevant incident or knowledge record ranked first for each of the three extra Korean formulations. The similar-symptom controls tested for incorrect concept expansion. For example, the Korean input “음악 재생을 두 번 누르면 곡이 처음으로 돌아가요” (pressing play twice returns the song to the beginning) did not activate the duplicate-stop rule. Nevertheless, the duplicate-stop incident ranked second because the music topic overlapped. Passing this check does not establish the accuracy of every lower-ranked result.

All 223 cases from the seven existing evaluation files also passed at 30,000 records, with 100% recall of designated required IDs and zero forbidden IDs exposed. Some cases overlap between evaluation files. All 223 also passed on the small production store. We verified 94 knowledge helper tests and five distribution tests. The sandbox blocked junction creation in two Windows helper tests, so we reran those two separately.

## Follow-up experiment reducing full-index preparation on the same corpus

We used the same 30,000 records and 50 questions in the same order. All 30,000 document-path and canonical SHA-256 pairs agreed between the previous JSON cache and the new SQLite index. With the search options and judgment file held constant, we ran an independent Python process for each question and timed through output receipt and process exit. P95 is the 48th value in ascending order. The index was prebuilt for each formal measurement, with zero canonical rereads. [Per-query result IDs, timings, and aggregates](2026-11-23-indexed-search-measurements.json)

| 50 individual searches | Median | P95 | Maximum | Within 2 seconds |
| --- | ---: | ---: | ---: | ---: |
| JSON search in the earlier experiment | 3.968 s | 5.641 s | 8.435 s | 0/50 |
| Same JSON search rerun in this environment | 2.160 s | 3.213 s | 3.669 s | 6/50 |
| SQLite | 0.425 s | **0.527 s** | 1.495 s | **50/50** |
| SQLite repeat measurement | 0.379 s | **0.448 s** | 1.356 s | **50/50** |

The old version also ran faster in the repeat measurement. Use the concurrent experiment's control value of 3.213 seconds to calculate the improvement. Median index preparation dropped from 1.816 to 0.211 seconds. Enumerating filenames, sizes, and modification times still costs time proportional to the file count. Search reads only candidates for the relevant terms from the persistent index, though broad questions may still score many documents.

The displayed IDs and order for all 50 questions agreed across all measurements. Among the original nine Korean paraphrases, eight ranked the target first and one second. All three additional formulations ranked it first. The separate set of 223 existing regression cases also passed. Searching a new expression after editing one document took 0.626 seconds and reread one canonical file. After adding a temporary document, the next query found it among 30,001 records. After deletion, the next query returned to 30,000 records and the expression no longer produced a result.

Initial index preparation in a development run took approximately 106 seconds. In a preliminary 50-run measurement, a schema change during development caused one question to reread all 30,000 records, and P95 was 2.287 seconds. The table includes only runs that started with the index ready. We did not clear the OS file cache between measurements or measure P95 on 30,000 distinct real-world topics or under concurrent user load.

## Building an empty SQLite index for the first time

We used the 30,000 canonical files in the same directory. Before each run we moved the existing SQLite file into an experiment folder and looked up a single incident ID through the ordinary search command. Every build reported `index.backend=sqlite`, `read_files=30000`, and `cached_files=0`. Build time covers the helper's index-preparation phase. Separately reported wall time also includes Python startup, searching and displaying sources for the first question, and process exit. We did not clear the OS file cache. [Raw measurements by build and question](2026-11-23-cold-index-measurements.json)

We instrumented the previous version on 1,663 records including 172 real canonical records and a synthetic sample. Of 3.95 seconds total, path checks took 1.72 seconds and YAML parsing 0.96 seconds. The revised helper reuses each document's path-validation result to identify the document. When PyYAML has a C parser, it uses that parser with the same safe constructor and duplicate-key checks. When reading at least 1,000 records, eight workers check batches of 32, each with independent validation state. At most 256 records are prepared at a time and written to SQLite in canonical order. The helper also checks for duplicate IDs across batches and missing relations before committing.

The two rebuilds of the previous version in this environment took **70.29 and 364.05 seconds**. The intermediate version with only path and YAML improvements took **52.64 seconds**. The first two runs with parallel reads took **28.84 and 25.01 seconds**. The earlier experiment recorded 106.19 seconds. Machine load and OS caching were uncontrolled, so these values cannot establish a fixed speedup.

With improvements only to building, individual-search P95 across the 50 questions was **1.867 and 2.073 seconds**. The second measurement exceeded two seconds. We then changed compound-ID candidate selection to check up to three words together. For an exact `R-CODE-UE-MUSIC-STOP` lookup, the candidates read dropped **from 2,494 to 2**. Regrouping duplicate bodies is also skipped when all candidate body fingerprints differ.

Rebuilding an empty index with the final search implementation took **41.15 seconds**, or **42.22 seconds** including process startup and the first search. We compared the path and canonical SHA-256 pairs, stored document rows, 30,000 per-document search-term sets, and relations with the previous index. All agreed.

| Same 50 questions, fresh process each time | Median | P95 | Maximum | Within 2 seconds |
| --- | ---: | ---: | ---: | ---: |
| Previous SQLite implementation rerun | 1.622 s | 2.176 s | 4.540 s | 46/50 |
| Final implementation, round 1 | 1.545 s | **1.997 s** | 2.223 s | 48/50 |
| Final implementation, round 2 | 1.552 s | **2.405 s** | 2.780 s | 43/50 |

In both rounds, displayed IDs and order agreed with the previous measurement for all 50 questions. Eight of the nine Korean paraphrases ranked the target first and one second. All three extra formulations ranked it first. All 223 existing regression cases passed. The measurements confirmed faster builds and preserved rankings. Individual-search P95 did not consistently meet the two-second target in this environment.

P95 measured inside the final helper was 0.462 and 0.608 seconds respectively. After subtracting internal time from total time, the median remainder was 1.23 and 1.22 seconds. In a separate diagnostic, even six empty Python process runs took 0.95–1.16 seconds. We judged P95 by wall time including startup and exit.

## From request start to response in a search session

We reread the 30,000 canonical records in the same corpus and verified that their paths and SHA-256 values matched the previous measurement. For each of five rounds, we started a fresh `search.py session` process with the SQLite index ready. We sent the original 50 questions one at a time with the same order and filters. The client started its timer immediately before encoding each question and stopped it immediately after reading the full response from the pipe and parsing its JSON. For the first question of each round, timing began immediately before process launch. The client waited for each response before sending the next question. [Raw measurements by round and question](2026-11-23-search-session-measurements.json)

| Round | First response (including startup) | Median | P95 | Maximum | Within 2 seconds |
| --- | ---: | ---: | ---: | ---: | ---: |
| Session 1 | 0.816 s | 0.510 s | 1.244 s | 4.100 s | 49/50 |
| Session 2 | 0.736 s | 0.575 s | 1.281 s | 3.378 s | 48/50 |
| Session 3 | 1.198 s | 0.448 s | 1.307 s | 2.443 s | 49/50 |
| Session 4 | 0.810 s | 0.449 s | 0.829 s | 2.266 s | 49/50 |
| Session 5 | 0.856 s | 0.526 s | 1.717 s | 2.665 s | 48/50 |

P95 in every round (48th fastest of 50) was within two seconds. All 250 responses displayed the same document IDs in the same order as the previous measurement. In every round, eight of the nine Korean paraphrases ranked the target first and one second, and all three extra formulations ranked it first. Of the responses, 243 took at most two seconds and seven took longer. The question exceeding two seconds in all five rounds was `music loudness calibration`.

In a separate run of the same 50 questions through the existing single-shot command, median time was 0.601 seconds and P95 was 1.391 seconds, measured from process startup through output receipt and exit. The single-shot control also met the target in this environment. A session uses an already running process when a question is sent, checks canonical files for changes on every query, and closes the SQLite read snapshot after each query. We tested processing the next question after a session error, file edits and deletions between questions, and independence of filters across requests. The 223 existing regressions also passed.

## Rechecking the seven responses over two seconds

The seven earlier overruns comprised five music questions, one Korean query `녹스`, and one camera interpolation question. The music query matched 29,846 records because synthetic bodies repeated `calibration`. In a separate trace before the change, search and ranking took 747 ms and created 29,846 result summaries to display three results. We changed the helper to calculate weights and order using a per-field word index first, then compare only the three displayed items with their bodies. In the same trace after the change, search and ranking took 130 ms and the total match count remained 29,846. The existing sorting and diversification path still handles duplicate bodies and queries requiring phrase or context conditions.

In the pre-change reproduction, `녹스` and the camera question matched two and 28 records respectively. Index freshness checks took 399 ms and 323 ms, and the searches themselves took 4 ms and 32 ms. The earlier records do not contain phase timings from when these two requests exceeded two seconds. We reduced the cost of sorting excluded files during canonical file enumeration. Separate post-change traces showed freshness checks of 160 ms and 158 ms respectively.

We reread all 30,000 canonical records and verified that paths and content hashes matched their earlier values. Building the new-format index took 31.943 seconds, measured separately from individual searches. With the index ready, we measured five fresh sessions using the same questions, filters, and order. Timing ran from process startup for the first question and from immediately before encoding for later questions through parsing the full JSON response. [Seven earlier overruns, phase diagnostics, and 250 raw records](2026-11-23-search-tail-measurements.json)

| Round | First response | P95 | Maximum | Music question | Within 2 seconds | Displayed rankings matched |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.374 s | 0.461 s | 0.615 s | 0.282 s | 50/50 | 50/50 |
| 2 | 0.366 s | 0.516 s | 0.531 s | 0.283 s | 50/50 | 50/50 |
| 3 | 0.374 s | 0.459 s | 0.544 s | 0.287 s | 50/50 | 50/50 |
| 4 | 0.371 s | 0.463 s | 0.641 s | 0.290 s | 50/50 | 50/50 |
| 5 | 0.384 s | 0.557 s | 1.282 s | 0.296 s | 50/50 | 50/50 |

In every round, eight of the nine Korean paraphrases ranked the correct answer first and one second. All three extra formulations ranked it first. All 223 separate regression cases also passed, with zero forbidden IDs exposed.

## Reproduction

From the repository root, choose a fresh, empty experiment path. To compare versions, keep a separate copy of the pre-change script directory and run `measure` and `update` first on the same project. For both commands, pass the path to the saved `search.py` as `--script`. Then measure the current version as shown below. Confirm that `index.read_files` equals the total record count for the first search and is zero on individual repeat searches. Measurements record correct-answer rank, time inside the search helper, and elapsed time through Python process exit.

```powershell
$bench = 'skills/vegabond-knowledge/tests/benchmark_scale.py'
$dir = '.cache/onestep/scale-replay'
python -B -X utf8 $bench build $dir --size 30000
python -B -X utf8 $bench measure $dir "$dir/measure.json"
python -B -X utf8 $bench sample $dir "$dir/sample.json"
python -B -X utf8 $bench update $dir "$dir/update.json"
```

Use the following command to remeasure sessions on the same preserved corpus. If the index format has changed, build the index first with one ordinary search. Specify a new output path. The measurement tool compares the displayed rankings for the previous 50 questions and records P95 and maximum time per round. It fails if even one request exceeds two seconds.

```powershell
python -B -X utf8 skills/vegabond-knowledge/tests/benchmark_scale.py sample-sessions .cache/onestep/korean-30k/corpus .cache/onestep/korean-30k/session-replay.json --rounds 5
```

The synthetic topics and sentence structures repeat. This experiment verified ranking when many similar documents compete and measured the costs associated with the actual file count. Semantic discrimination across 30,000 distinct real incidents, concurrent searches by multiple users, and external source access time require separate measurements.
