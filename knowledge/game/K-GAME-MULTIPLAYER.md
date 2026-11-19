---
id: K-GAME-MULTIPLAYER
title: Define multiplayer fairness through information and resolution contracts
summary: Align what players can recognize with how contested actions resolve under network conditions. Separate perceptual clarity, simulation fairness, and balance when diagnosing losses.
kind: reference
scope: Competitive real-time multiplayer; clarity and network-sensitive design
keywords: [multiplayer, PvP, fairness, netcode, latency, server authority, client-side prediction, server correction, server rewind, clarity, VFX, competitive integrity, prototype, 멀티플레이, 대전, 공정성, 지연, 서버 권한, 클라이언트 예측, 가독성, 판정, 기획]
status: active
checked_at: '2026-11-19'
context:
  evidence_check: Riot official design and engineering article sections read
  application_status: Proposed design checks; no multiplayer simulation or user study run
---
# Define multiplayer fairness through information and resolution contracts

## Guidance

**Source claims.** Riot's clarity article ties ability attention to gameplay importance, discusses effect/hitbox alignment, and seeks clarity parity across skins. VALORANT's developers describe competing goals for responsiveness, fairness, territory holding, and broad hardware/network support. Their server-authoritative approach combines prediction, correction, and bounded historical hit resolution. These describe Riot's goals and implementation, not a guarantee that every match is fair.

**Transferable synthesis.** Write two contracts for each contested action: what each participant can know, and which event determines the result. Trace perceive opponent → commit action → resolve contention → receive feedback → adapt. A clear effect with surprising authoritative timing still breaks understanding; accurate resolution with an obscured cue still denies usable information.

With **server authority**, the server decides the accepted simulation state. **Client-side prediction** lets the local client display the expected result of its own input before confirmation. A **server correction** brings a diverging client back to the accepted state. **Server rewind** addresses a different delay. For hit registration, Riot describes testing the shot against historical positions corresponding to what the shooter could see, subject to a limit. When players report a hit after taking cover, compare the shooter's view, the target's view and the server's evaluation time. The rewind limit is a design choice with consequences for both players.

Before adding an ability, cosmetic, camera effect, or movement burst, inspect team recognition, threat priority, collision representation, and latency interaction together. Decide the intended advantage of holding, chasing, initiating, or escaping. A networking model cannot choose those design priorities for the team. Give designers a condition matrix so the same interaction is reviewed under local, delayed, jittery, and asymmetric connections.

Classify a complaint before changing balance: ambiguous visual information, simulation disagreement, unavailable counterplay, or numerical dominance require different experiments. Review the loser's and winner's views together; one convincing local recording cannot establish the entire event sequence.

## Applicability and exceptions

Useful for shooters, MOBAs, fighting games, and other contested real-time systems. Different genres may choose rollback, lockstep, or other authority policies; the cited model is not universal. Turn-based games still need information and resolution contracts but have different delay sensitivities. This entry does not cover matchmaking, social moderation, ranked population health, or economy fairness.

## Checks

**Proposed checks, not executed:** Test identical abilities with alternate cosmetics in crowded combat. Ask players to identify threat, direction, and affected area. Replay a contested interaction from both clients and an authoritative event log under emulated delay, jitter, and loss. Inspect corrections and feedback after cover transitions. Define acceptable discrepancies for the intended audience before interpreting results; report observations separately from perceived fairness.

## Evidence

- [Riot, Clarity in League](https://www.leagueoflegends.com/en-us/news/dev/clarity-in-league/), “Abilities” and skin “Abilities”/clarity-parity discussion; official text opened 2026-11-07. Examples describe author intent; no skin comparison performed.
- [Riot, Peeking into VALORANT's Netcode](https://www.riotgames.com/en/news/peeking-valorants-netcode), “A Few VALORANT Design Goals,” “Resolving Disagreements” and “Confirming Hit Registration.” Official text first checked 2026-11-07. The movement and combat mechanisms were rechecked 2026-11-19. This is a historical 2020 explanation. Current implementation and service targets remain unverified.
