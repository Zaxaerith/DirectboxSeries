# Directbox Series

**Exploring a native-execution compatibility layer for Xbox Series X|S software on Windows.**

> Project Scarlett, meet the PC.

Directbox Series is an independent, experimental project exploring the technical path from Xbox Series X|S software to Windows execution. Rather than replicating every component of a console, the proposed approach starts with the shared x86-64 architecture and investigates the runtime, graphics, memory, and I/O boundaries that separate console applications from desktop programs.

**Long-term north star:** investigate what it would take to support demanding, modern Xbox Series titles — with **Grand Theft Auto VI (GTA VI)** as an aspirational, high-profile compatibility target.

This is an **early-stage research initiative**. The public repository is being populated incrementally with architecture notes, interface studies, experimental designs, and, where feasible, reproducible proof-of-concept code. Roadmap entries describe intended work, not completed implementations.

## The approach

| Track | Research direction |
| --- | --- |
| Native execution | Reuse compatible x86-64 code paths where technically possible |
| Scarlett environment | Map executable, application-model, and system-service dependencies |
| Runtime layer | Explore host-side replacements for relevant guest APIs |
| Graphics | Investigate the differences between Xbox D3D12.X and desktop graphics APIs |
| Memory and I/O | Study allocation, synchronization, storage, input, and audio assumptions |
| Validation | Begin with legal, reproducible homebrew experiments before broader compatibility work |

No single one of these tracks implies that a full title can be executed. They are distinct engineering problems, and every claim of progress should be backed by an artifact.

## The GTA VI horizon

A modern flagship title is an excellent *stress test for the research questions*:

- Can a Windows host satisfy the executable and runtime requirements of a Scarlett-targeted application?
- How much of the GPU command and shader pipeline needs translation?
- Which console-only services prevent otherwise compatible native code from advancing?
- What tooling would be necessary to trace faults, validate output, and measure performance?

**GTA VI is a long-term research target, not a compatibility announcement.** Directbox Series has no affiliation with Rockstar Games, Take-Two Interactive, or Microsoft.

See [the GTA VI research horizon](docs/gta-vi-horizon.md).

## Project map

- [Architecture proposal](docs/architecture.md) — boundaries, components, and assumptions
- [Platform overview](docs/platform-overview.md) — terminology and known technical differences
- [Roadmap](ROADMAP.md) — milestones and criteria for evidence
- [Research log](docs/research-log.md) — dated, sourced notes
- [Contributing](CONTRIBUTING.md) — proposals, prototypes, and reproducibility
- [Source workspace](src/README.md) — intended code organization

## Development philosophy

**Native first. Evidence always. Hype optional.**

Directbox Series is an independent open research effort. The name is descriptive, not an official Xbox or DirectX product name. The project does not distribute proprietary console firmware, SDK binaries, decrypted commercial titles, or game assets.

**Status:** Concept and research planning · **Platform:** Windows x86-64 · **License:** MIT
