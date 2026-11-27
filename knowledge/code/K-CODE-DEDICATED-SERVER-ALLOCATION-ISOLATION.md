---
id: K-CODE-DEDICATED-SERVER-ALLOCATION-ISOLATION
title: Keep multiplayer branch builds separate when allocating a Dedicated Server
summary: Match the allocation target to the server build and verify the returned address and port from a different client machine. Unique listening ports prevent bind conflicts, while the fleet or selector controls which server can receive a session.
kind: reference
scope: Network multiplayer development stacks using Amazon GameLift Servers Anywhere or Agones with multiple server builds
keywords: [Dedicated Server, matchmaking, game session, server allocation, GameLift Anywhere, Compute, Fleet, fleet ID, ProcessReady, compute auth token, Agones, GameServerAllocation, port, private IP, branch isolation, 매치 서버, 포트, 사설 IP]
status: active
checked_at: 2026-11-25
---

# Keep multiplayer branch builds separate when allocating a Dedicated Server

## Guidance

A Dedicated Server runs the match simulation without rendering or a local player. A match service assembles players and asks for a game session. The allocator selects a ready server and returns its connection endpoint, which the clients use to join. Matchmaking and allocation can be implemented in the same service while remaining distinct decisions.

In GameLift Anywhere, a compute is a registered host you provide. Its server processes connect to the AWS service using parameters for that compute and a temporary compute authentication token. A fleet groups eligible hosting resources, and a process reports readiness with `ProcessReady()`. A direct `CreateGameSession` request selects an available process in the targeted fleet and location. In Agones, `GameServerAllocation` can select ready GameServers using labels, including the fleet label.

## Applicability and exceptions

For strict isolation, give each incompatible test build its own allocation target and configure the matchmaking process and registered servers to agree on that target. Inspect aliases, queues or fallback selectors when present. Distinct host ports on the same bind address and transport let processes listen simultaneously. The published IP or DNS name and port must also be reachable from the client network. A private IP can work over a routed LAN or VPN. Client and server builds must agree on the network protocol and any data the game requires to match.

## Checks

From a second client machine, create one session per branch and verify the expected server build, allocation target and reachable endpoint. With one branch's ready capacity exhausted, verify that a new request cannot silently use an incompatible branch. These are proposed checks for a consuming project.

## Evidence

- Epic Games explains the headless process and remote clients. [Setting Up Dedicated Servers in Unreal Engine](https://dev.epicgames.com/documentation/en-us/unreal-engine/setting-up-dedicated-servers-in-unreal-engine)
- AWS documents compute registration, tokens and readiness, plus direct session creation and connection fields. [Create an Anywhere fleet](https://docs.aws.amazon.com/gameliftservers/latest/developerguide/fleets-creating-anywhere.html) [CreateGameSession](https://docs.aws.amazon.com/gameliftservers/latest/apireference/API_CreateGameSession.html) [GameSession](https://docs.aws.amazon.com/gameliftservers/latest/apireference/API_GameSession.html)
- Agones documents fleet label selection, default Ready state and ordered fallbacks. [GameServerAllocation specification](https://agones.dev/site/docs/reference/gameserverallocation/)
- Official documentation checked on 2026-11-25. No live allocation, connectivity or build compatibility checks were run.
