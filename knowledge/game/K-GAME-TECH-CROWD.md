---
id: K-GAME-TECH-CROWD
title: Scale crowd decisions separately from crowd rendering
summary: Use shared routes for direction, local avoidance for nearby motion and admission control when
  safe motion can still leave requests waiting indefinitely.
kind: reference
scope: Game development. For sustained requests, first-in, first-out (FIFO) preserves admission order
  but a blocked head can stall the queue.
keywords: ["crowd", "Mass", "avoidance", "AI", "LOD", "spatial", "hash", "군중", "reservation", "dynamic-obstacle", "국소회피", "동적장애물", "bidirectional", "corridor", "radius", "clearance", "deadlock", "교행", "양방향", "반경", "통로", "교착", "경로장", "개체", "lifelong", "sustained", "inflow", "queue", "FIFO", "starvation", "overload", "throughput", "unlaned", "time-expanded", "지속", "유입", "개별", "무한", "대기", "차선", "없는", "지형", "시간", "확장", "예약", "과부하", "ORCA", "Optimal Reciprocal Collision Avoidance", "Mass Avoidance", "spatial hash", "flow field", "token bucket", "backpressure", "head-of-line blocking", "goodput", "level of detail", "NPC", "admission control", "lossless admission", "모든 요청 처리", "거부 불가", "대기열", "역압력"]
status: active
checked_at: '2026-11-11'
---
# Scale crowd decisions separately from crowd rendering

## Guidance

A spatial hash bins nearby agents for neighbor queries. A shared flow field supplies long-range direction. Local avoidance chooses near-term motion consistent with neighboring bodies. ORCA (Optimal Reciprocal Collision Avoidance) derives velocity constraints under reciprocal avoidance assumptions. A central reservation system instead assigns time and space. In a narrow corridor, a direction lease can admit one stream until bodies clear the exit. The Hitman: Absolution developer slides describe a 2.5D cell map, per-exit evacuation fields, local steering and promotion of selected crowd agents to NPCs.

## Applicability and exceptions

For sustained requests, first-in, first-out (FIFO) preserves admission order but a blocked head can stall the queue. A token bucket limits admission by refill rate and burst size. Backpressure shifts waiting upstream. Reject/drop policies reduce admitted load when loss is allowed. A queue cap bounds that queue alone. A collision-free scene can still deadlock or starve an agent. Keep rendering level of detail (LOD), behavior update frequency and physical safety budgets separate.

If every request must be served, queue rejection violates the service requirement. A finite queue under sustained demand above service capacity needs upstream backpressure, additional capacity or an explicit change to the offered workload. Preserve original request identity and arrival time across backpressure. Compare the oldest waiting request with total completions to expose starvation hidden by aggregate throughput. This conclusion assumes requests continue arriving and each completion consumes capacity. [Reactive Streams — asynchronous backpressure](https://www.reactive-streams.org/)

## Checks

At equal offered demand, retain each request's original arrival time. Measure arrivals, admissions, rejections, oldest age, completions and fraction of all offered work completed on time. Audit swept separation with actual radii, terminal moves and a deliberately conflicting control. Profile whole-frame tails including topology changes, synchronization, animation and rendering on target hardware.

To assess the frame budget, record CPU and GPU timings separately and mark missing GPU samples explicitly.

## Evidence

Fauerby's slides document the historical game architecture. The ORCA authors state their method's assumptions, and Epic documents Mass Avoidance's own spatial and steering model. Earlier grid examples observed both collision-free deadlock and finite queue drain. Finite drains do not prove unlimited progress or native Mass behavior.

- [Kasper Fauerby — Crowds in Hitman: Absolution slides](https://media.gdcvault.com/gdc2012/slides/Programming%20Track/Fauerby_Kasper_CrowdsInHitman.pdf)
- [Epic — Mass Avoidance Overview](https://dev.epicgames.com/documentation/unreal-engine/mass-avoidance-overview-in-unreal-engine?lang=en-US)
- [ORCA authors](https://gamma-web.iacs.umd.edu/ORCA/)
- [Li et al., corridor symmetry](https://mapf.info/index.php/Main.SKoen20k)
- [LaValle footprint/C-space](https://lavalle.pl/planning/node161.html)
- [fixed-path coordination](https://lavalle.pl/planning/node325.html)
- [RHCR](https://arxiv.org/abs/2005.07371)
- [PIBT](https://arxiv.org/abs/1901.11282)
- [online pickup/delivery](https://arxiv.org/abs/1705.10868)
