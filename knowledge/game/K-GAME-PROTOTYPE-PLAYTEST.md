---
id: "K-GAME-PROTOTYPE-PLAYTEST"
title: "Match a prototype and playtest to the design uncertainty"
summary: "Before expanding a game design, select the smallest playable representation that can challenge a consequential assumption. Separate observed player behavior, interpretation, proposed fixes, and evidence that a revised build actually improves the result."
kind: "reference"
scope: "Game design prototyping, usability and experience research across genres; not a fixed schedule, sample size or automatic execution authorization"
keywords: ["prototype", "playtest", "hypothesis", "usability", "iteration", "vertical-slice", "telemetry", "프로토타입", "플레이테스트", "가설", "시제품", "검증", "재미"]
status: "active"
checked_at: "2026-11-07"
context: {"evidence_check": "Named primary source text or slides inspected; source-specific access limits in Evidence", "application_status": "Source-based reference and proposed synthesis; no project gameplay trial"}
---

# Match a prototype and playtest to the design uncertainty

## Guidance

Source observations: Experimental Gameplay Project authors describe starting from a manipulable core mechanic and keeping exploratory builds small [S1]. Valve developer Ken Birdwell describes observing outside players without hints and feeding findings back into design [S2]. Games researcher Graham McAllister recommends aligning on prioritized questions that upcoming observations can answer [S3].

Proposed method: state the uncertain claim and the decision affected by its failure. Choose a paper model, greybox, interaction prototype, or representative integrated slice according to that claim. Include the feedback essential to the question; mark omitted systems and temporary assumptions.

Prepare tasks without teaching the answer. Observe actions and stumbling points, then ask what players understood. Keep unfamiliar and practiced players distinguishable. Capture build/version and conditions. Convert a finding into the smallest supported change, rerun the affected observation on the changed build, and retain contrary evidence.

## Applicability and exceptions

The seven-day project and Valve sessions are historical cases, not universal budgets or sample sizes. A toy can investigate feel without proving a complete game. A paper model can test choices while omitting execution timing; a polished slice can hide content-production cost. Separate usability, bug finding, balancing, experience, and performance questions. Recruitment, builds, data collection, and deployment still require the actual task scope.

## Checks

Proposed checks: could the chosen task expose a broken assumption? Is an observer hint masking the problem? Does telemetry identify behavior while leaving its cause uncertain? Has a proposed fix been retested rather than merely documented? Report sample and representation limits; a positive small test does not establish retention or population-wide preference.

## Evidence

- [S1] Experimental Gameplay Project authors, [How to Prototype a Game in Under 7 Days](https://www.gamedeveloper.com/game-platforms/how-to-prototype-a-game-in-under-7-days), 2005; Development / Build the Toy First. Original authored article opened.
- [S2] Ken Birdwell, [The Cabal](https://www.gamedeveloper.com/design/the-cabal-valve-s-design-process-for-creating-i-half-life-i-), 1999; Pearls Before Swine, playtesting and subsequent design revision. Original developer article opened.
- [S3] Graham McAllister, [Aligning on a Clear Purpose](https://grahammcallister.com/playtesting-book/step-1-alignment-on-clear-purpose), opening hypotheses and Step 1 Outcome. Author page opened.
- Sources checked 2026-11-07. Proposed checks were not exercised on a real game in this task.
