---
id: K-CODE-DEDICATED-SERVER-READY-CAPACITY
title: Replace finished Dedicated Server processes while keeping ready capacity
summary: For one-match-per-process hosting, keep enough servers eligible for the next match and replenish them with a process supervisor or an Agones Fleet. Track waiting capacity separately from the number of running processes.
kind: reference
scope: Session-based multiplayer development stacks with disposable Dedicated Server processes
keywords: [Dedicated Server, process supervision, ready capacity, standby server, match lifecycle, GameLift Anywhere, Agones, Fleet, FleetAutoscaler, Buffer, Ready, Allocated, Shutdown, Kubernetes, Docker, container, 대기 서버, 프로세스 재시작]
status: active
checked_at: 2026-11-25
---

# Replace finished Dedicated Server processes while keeping ready capacity

## Guidance

When a game uses one Dedicated Server process per match, a process starts, reports ready, runs a match, and exits or shuts down when that match ends. Prestarting ready servers avoids making the next party wait for a process to boot. In a manually hosted GameLift Anywhere test setup, a launcher or supervisor can start a replacement and wait for its readiness signal. The Amazon GameLift Servers Agent can also manage registration and launch processes when configured.

Docker packages the server and its runtime dependencies in an image. A container is a running instance of an image. Kubernetes manages deployed containers, and Agones adds game-server lifecycle and allocation to Kubernetes. An Agones `Fleet` defines a common server template and target replica count. `Ready` marks a server eligible for allocation, `Allocated` marks one assigned to a session by the usual allocation path, and `Shutdown()` ends the GameServer and its backing Pod.

## Applicability and exceptions

One process per match is a lifecycle choice. A game designed to reset and reuse a process has a different lifecycle, and Agones documents reusing a server by returning it to Ready. A fixed Agones Fleet replica count includes both Ready and Allocated GameServers. Use a `FleetAutoscaler` with a Buffer policy when the target is spare ready capacity under load, within configured bounds.

## Checks

Allocate a waiting server, end the match through the normal path, and verify that enough servers become Ready for the next request. Compare ready and allocated counts under concurrent use. A process ID or a running container alone is insufficient evidence of readiness. These are proposed checks for a consuming project.

## Evidence

- AWS documents manual Anywhere launch, the optional Agent and `ProcessReady()`. [Create an Anywhere fleet](https://docs.aws.amazon.com/gameliftservers/latest/developerguide/fleets-creating-anywhere.html)
- Agones documents replica counting, Buffer autoscaling, and readiness, shutdown and reuse. [Fleet](https://agones.dev/site/docs/reference/fleet/) [FleetAutoscaler](https://agones.dev/site/docs/reference/fleetautoscaler/) [Game Server SDKs](https://agones.dev/site/docs/guides/client-sdks/)
- Docker documents images and running containers. [What is a container?](https://docs.docker.com/learn/content/what-is-a-container/)
- Official documentation checked on 2026-11-25. No lifecycle or load tests were run.
