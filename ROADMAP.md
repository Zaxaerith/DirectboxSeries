# Roadmap

Directbox Series is organized around research milestones rather than promised release dates.

## Stage S0 — Mapping Scarlett
- Collect and reference publicly available Xbox GDK and Windows GDK documentation.
- Distinguish Xbox One ERA, Xbox PC GDK, and Series X|S Scarlett assumptions.
- Identify testable hypotheses without depending on commercial game files.
**Exit evidence:** a referenced platform inventory and reproducible study questions.

## Stage S1 — Executable and runtime exploration
- Study documented PE/COFF concepts and console-specific application metadata at a conceptual level.
- Create a self-authored synthetic executable fixture for safe parser experiments.
- Outline guest-to-host API dispatch, error handling, and logging.
**Exit evidence:** an independently testable parser or trace prototype.

## Stage S2 — Host interface bridge
- Prototype interfaces against self-authored stubs.
- Explore thread scheduling, memory allocation, clocks, files, input, and audio.
- Track feature gaps explicitly.
**Exit evidence:** a minimal homebrew-style test program communicating with host stubs.

## Stage S3 — Graphics research
- Compare desktop D3D12 with documented Xbox D3D12.X constraints.
- Experiment with command abstraction using original, self-authored workloads.
- Define graphics validation and debugging workflows.
**Exit evidence:** reproduced test frames from original experiments; no commercial game implied.

## Stage S4 — Homebrew experiments
- Integrate loader, runtime, and graphics hypotheses.
- Test permitted self-authored code, retain logs and environment details.
**Exit evidence:** a repeatable independent demo.

## Stage S5 — Broader compatibility horizon
- Investigate scaling requirements for complex commercial engines.
- Use GTA VI as a **long-term performance and compatibility north star**, not as a shipped compatibility claim.
- Publish findings only when supported by independently reproducible evidence.

## Evidence policy
Each milestone should link to source commits, test fixtures, documented limitations, and observed results. Proposed work is not completed work. No compatibility claims from screenshots alone.
