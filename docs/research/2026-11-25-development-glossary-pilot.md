# Does a development glossary change acceptance tests?

Four AI readers who had no access to the prior conversation independently drafted acceptance tests. The two readers given the [OneStep development glossary](../development-glossary.md) and the two given the original sources alone each covered all 11 criteria. Both glossary readers cited it. This trial found no gain in the correctness of the proposed tests.

## Why these terms

- **Individual search response time.** The measurement history contains both helper-side timing and caller-side timing. Charging process launch to the first request and waiting for JSON decoding changes what a test measures. [Measurement history](2026-11-23-korean-retrieval-at-30000.md)
- **Within two seconds.** In an earlier run, all five rounds met their P95 target and seven individual responses exceeded two seconds. The user subsequently tightened the target to every response. Both meanings have been valid at different times. [Earlier measurements](2026-11-23-search-session-measurements.json)
- **Feedback submitted.** Feedback was mentioned in session reports while the reports were missing from the destination inbox. The inbox owner defines how to verify delivery independently of preparation and review. [Incident](../../feedback/2026-11-20-feedback-lines-not-submitted.md) · [Delivery rule](../../feedback/README.md#confirm-delivery-at-handoff)

## Comparison

Each reader received the same Korean request and eight identical project files, including the benchmark, earlier measurements, incident, inbox rules and checker tests. Only the treatment packet added the glossary. Readers could inspect their packet and had no conversation history or answer key. Before collecting responses we fixed 11 binary criteria. We manually scored explicit criteria in each answer. The exact request, file hashes, scoring key, individual scores and answer excerpts are in the [trial record](2026-11-25-development-glossary-trial.json).

| Proposed test | Original sources only, two readers | Same sources plus glossary, two readers |
| --- | --- | --- |
| Caller timer (4 criteria) | Both used a prebuilt index, started before launch for the first request of each round and before encoding for subsequent requests, and ended after receiving and decoding JSON. | Both chose those same boundaries. |
| Two-second target (3 criteria) | Both took the 48th of 50 per round, compared unrounded durations inclusively, and passed P95 while failing the every-response target. | Both used the same threshold, statistic and verdicts. |
| Feedback receipt (4 criteria) | Both checked matching nonempty regular files in the configured inbox, reported prepared before retry and submitted after rechecking, and treated review as a separate decision. | Both used the same destination, file checks, state transitions and review boundary. |
| Total per reader | 11/11 and 11/11 | 11/11 and 11/11 |

In the supplied example, 0.23 seconds before encoding, 1.76 seconds through receipt, and 0.0104 seconds decoding add up to **2.0004 seconds**. The separate response of exactly two seconds passed. All five P95 values were 0.8 seconds, and 249 of 250 responses were within the limit. For feedback, all readers expected the inbox checker to return code 1 for an empty Korean file and code 0 only after refilling it and checking again. These are judgments on a constructed scenario. The trial did not rerun the search benchmark.

## Decision

Keep the three entries available to the development design and implementation skills when a term affects acceptance. The original sources were sufficient for both baseline readers. Two cases, four readers, a detailed request and a small curated source packet leave open whether a glossary helps with a terse request in the full repository. We did not measure lookup time, implementation quality or later rework. Add an entry when a real development disagreement changes a test and link it to the source that owns the behavior.
