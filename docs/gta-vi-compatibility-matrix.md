# GTA VI — long-term compatibility research matrix

**Classification:** aspirational research target. This file contains no GTA VI executable, title-specific offsets, compatibility evidence or unauthorized build data.

A flagship title can help define the upper bound of the Directbox Series ambition, but it should never be used to claim functionality before the underlying platform layers are validated.

## Compatibility dependency chain

```text
Verified source provenance
  -> Known image and launch model
  -> Guest ABI + runtime dependencies
  -> CPU memory/thread behavior
  -> Graphics semantics + shader handling
  -> Storage / streaming
  -> Input / audio / saves
  -> Interactive gameplay stability
  -> Performance and frame pacing
```

Each link is independently necessary; skipping one can produce impressive-looking but meaningless partial demonstrations.

## Risk matrix

| Dependency | Research question | Intended measurement |
| --- | --- | --- |
| Launch and image | What executable model is actually required? | Structured, source-backed dependency report |
| Runtime | Which system services are exercised and how? | Allowed test coverage and unresolved-call counts |
| CPU | Are memory/ABI expectations host-compatible? | Synthetic conformance suite |
| Rendering | What is required beyond desktop D3D12? | Original render tests + validation |
| Streaming | Which latency/throughput characteristics matter? | Synthetic I/O workload |
| Input/audio | Are frame-time and device behaviors consistent? | Test harness and audio/input replay |
| Stability | Can a stateful application survive suspend/resume? | Multi-hour original test workload |
| Performance | Can overhead be bounded? | p50/p95/p99 frame-time traces |

## Staged aspiration

**Horizon A — Understand:** publicly document architectural questions.  
**Horizon B — Reproduce primitives:** original loader/runtime/graphics fixtures.  
**Horizon C — Integrate:** independent homebrew-style execution proof.  
**Horizon D — Characterize complexity:** study general constraints of large engines using lawfully distributable workloads.  
**Horizon E — Re-evaluate GTA VI:** only with verifiable technical facts, determine whether a game-specific compatibility effort is realistic.

The stages are **not calendar promises** and do not imply access to an unreleased or leaked commercial build.

## Success definitions

- **Investigated:** a sourced and falsifiable technical question.
- **Demonstrated primitive:** an original test application verifies one subsystem.
- **Launch-compatible:** the actual application can initialize to an explicitly defined state, with lawful reproducibility.
- **Render-compatible:** correct frames, synchronization and presentation are demonstrated.
- **Playable:** stable and interactive gameplay is independently verified.
- **Performance-qualified:** frame rate, frame-time, resolutions and limitations are measured.

Do not silently collapse these into "works".

## Project independence

Directbox Series is not affiliated with Microsoft, Xbox, Rockstar Games or Take-Two Interactive. No proprietary game files, keys or protected platform binaries are distributed. A high-profile target is a research motivation, not a status announcement.
