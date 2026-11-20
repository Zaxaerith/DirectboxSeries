# Directbox Series — Engineering blueprint

**Document class:** DESIGN PROPOSAL / DRAFT 0.1  
**Target:** Windows 11 x86-64 host; Xbox Series X|S ("Scarlett") application environment as a subject of research  
**North star:** a credible path toward modern, demanding titles, including GTA VI

This is an architectural proposal, not a claim that the components described below exist. Every internal name prefixed `dbx-` is a **proposed Directbox component**, not a discovered Microsoft symbol.

## 1. Problem statement

Xbox Series and modern PCs both support x86-64 execution, but instruction-set overlap is not application binary compatibility. A console application may depend on a distinct Game OS, a platform-specific import surface, a different app model, graphics and memory semantics, package identity, asynchronous services, and hardware-specific assumptions. The goal is to study where these boundaries are, and build independent host-side implementations where doing so is feasible.

A Windows-hosted compatibility layer is favored over full-system emulation as an **initial research direction**. That choice must be reconsidered if executable layout, ABI, protection, or GPU requirements make native execution unworkable.

### Public documentation anchors

- GDK introduction and Game OS: https://learn.microsoft.com/en-us/gaming/gdk/docs/gdk-dev/intro/introduction
- Xbox target triplets and console graphics differences: https://learn.microsoft.com/en-us/vcpkg/users/platforms/xbox
- GDK configuration: https://learn.microsoft.com/en-us/gaming/gdk/docs/features/common/game-config/microsoftgameconfig-overview
- PE/COFF: https://learn.microsoft.com/en-us/windows/win32/debug/pe-format
- D3D12 fundamentals: https://learn.microsoft.com/en-us/windows/win32/direct3d12/direct3d-12-graphics

No public source above establishes the full internal layout of any specific commercial Scarlett build.

## 2. System boundaries

```text
    [Legally obtained / self-authored test program]
                         |
                    dbx-launch
                         |
                    dbx-inspect
             (metadata + dependency graph)
                         |
            +------------+-------------+
            |                          |
      dbx-loader                    dbx-policy
   image/section model       permitted inputs/sandbox
            |                          |
       dbx-exec <------------ dbx-abi / dbx-thunks
     proposed native path            |
            |             +----------+----------------+
            |             |          |                |
            |        dbx-runtime  dbx-gfx          dbx-services
            |             |          |                |
            |        OS adapters  D3D12 host        VFS/input/
            |        and handles  prototype         audio/tasks
            +-------------+----------+----------------+
                                      |
                              Windows 11 x86-64
                                      |
                             dbx-trace + dbx-testkit
```

An error in one layer should be diagnosable without pretending a later layer works.

## 3. Component contracts

| Component | Inputs | Outputs | First measurable prototype |
| --- | --- | --- | --- |
| `dbx-inspect` | Self-authored PE/COFF, XML or synthetic metadata | Validated structured inventory | Header and section report |
| `dbx-launch` | Explicit fixture path + options | Launch plan / error | Deterministic dry run |
| `dbx-loader` | Validated portable image model | Mapped regions / unresolved imports | Inert synthetic image inspection |
| `dbx-abi` | Interface manifest | Generated dispatch entries | Call-convention tests using own functions |
| `dbx-runtime` | Guest-facing requests | Host results / typed errors | Allocator, clocks, threads on test clients |
| `dbx-gfx` | Frontend-neutral graphics operations | Host D3D12 commands | Original colored-triangle scene |
| `dbx-services` | VFS, task, audio, input requests | Service results | Read, async queue, loopback audio tests |
| `dbx-trace` | Structured events | JSONL / human trace | Correlated test run |
| `dbx-testkit` | Synthetic fixtures + expected outcomes | Reproducible pass/fail | Parser + lifecycle regressions |

The interfaces are *project-internal*; their names and shapes must not be confused with actual guest exports.

## 4. Prototype data model

A normalized `ImagePlan` is preferable to passing raw file offsets through every layer:

```cpp
struct ImageSection {
    std::string name;
    uint64_t virtual_address;
    uint64_t virtual_size;
    uint32_t raw_offset;
    uint32_t raw_size;
    Access access;
};
struct ImagePlan {
    Architecture machine;
    uint64_t preferred_base;
    uint64_t entry_rva;
    std::vector<ImageSection> sections;
    std::vector<ImportedSymbol> imports;
    std::vector<Relocation> relocations;
    Confidence provenance; // documented | inferred | unknown
};
```

These are design-only types. No Xbox-specific structure is assumed to be identical to the PE structures used in initial tests.

Use a result type `Result<T, DbxError>`, not exceptions across the boundary between runtime modules. Error codes must carry a category (`invalid-image`, `unresolved-import`, `unsupported-api`, `device-lost`, `guest-fault`) and a structured context.

## 5. Proposed repository decomposition

```text
DirectboxSeries/
  docs/
  prototypes/          # first independently executable research utilities
  include/directbox/   # future public internal headers
  src/
    core/              # configuration, errors, handles, logging
    inspect/           # file and metadata inspection
    loader/            # guarded image model and mapping
    abi/               # guest-facing stubs and dispatch
    runtime/           # scheduling, memory and OS service adapters
    graphics/          # frontend + desktop D3D12 backend
    platform/          # VFS, save, input, audio
    launcher/          # diagnostic CLI
  tests/
    unit/
    integration/
    fixtures/          # synthetic, freely distributable data only
```

The directory names under `src/` describe a future structure, **not existing source**.

## 6. Proposed implementation order

1. **Observability first.** Define structured events, error taxonomy and deterministic fixture IDs. Unknown behavior must produce actionable traces.
2. **Input hygiene.** Read only approved fixtures initially; create a bounded metadata parser with strict overflow and allocation limits. Never execute an image as a side effect of inspection.
3. **Synthetic loader.** Model PE sections, imports, relocation entries, access flags and zero-filled ranges for self-authored test cases.
4. **In-process ABI tests.** Call self-authored x64 functions through dispatch prototypes and verify argument registers, stack alignment, error paths, SIMD preservation and exception isolation.
5. **Runtime services.** Implement virtual handles, clocks, memory, threads, events and asynchronous dispatch in isolation.
6. **Graphics testbed.** Add a desktop D3D12 backend fed by Directbox's own neutral command stream; compare screenshots/hashes with a native reference implementation.
7. **Integrated demo.** Execute a wholly original test application through the proposed abstractions.
8. **Compatibility exploration.** Only after these gates, investigate what additional target-specific research would be required for commercial-scale engines.

## 7. Scheduling and resource budgets (proposals)

For a single developer, treat each phase as an **exit-criteria gate**, not a calendar promise. A draft 12-iteration sequence:

| Iteration | Scope | Exit artifact |
| --- | --- | --- |
| I01 | Probe and validated file view | Header dump + malformed-file tests |
| I02 | Metadata schema | JSON report + schema version |
| I03 | Error/trace foundation | Correlated JSONL traces |
| I04 | Loader image plan | Test-driven mapping plan |
| I05 | Synthetic import resolver | Stable unresolved-import behavior |
| I06 | ABI and thunk harness | Calling convention unit tests |
| I07 | Memory and threading services | Handle lifetime tests |
| I08 | Async VFS | Deterministic I/O demo |
| I09 | Graphics command schema | Recorder + validator |
| I10 | Desktop D3D12 backend | Original triangle frame |
| I11 | Integrated original demo | Cold-start to orderly exit |
| I12 | Assessment | Public evidence table + revised roadmap |

**Resource discipline:** Windows x86-64 baseline; C++20 for low-level prototypes, Python 3 for inspection and fixtures; no compulsory local Rust builds. Use cloud CI for costly build/test work. Each test fixture should have a cryptographic hash and a documented origin.

## 8. Risk register

| Risk | Severity | Mitigation / investigation |
| --- | --- | --- |
| Console executable differs significantly from ordinary PE | Critical | Treat format compatibility as hypothesis; prototype only on synthetic PE first |
| Undocumented system ABI or restricted SDK surfaces | Critical | Trace own fixtures, cite public contracts, explicitly reject unsupported calls |
| Console graphics cannot map directly to PC D3D12 | Critical | Intermediate representation and isolated backend; never promise shader compatibility |
| Guest address-space assumptions conflict with host | High | Reserve regions only after validated, synthetic memory tests; add guard pages |
| Streaming and high I/O rate assumptions | High | Async VFS, operation tracing, stress tests on original datasets |
| Threading and synchronization nondeterminism | High | Deterministic scheduler tests, lock-order instrumentation |
| Proprietary or licensed service dependency | High | Avoid impersonating licensed/online services; document unsupported requirements |
| Inflated milestones | High | "Design", "prototype", "verified" states, with evidence links for each |

## 9. Decision rules

If the console app format, code loading model, or graphics ISA cannot be studied through lawful and reproducible methods, pause that path and publish the blocker. A research project can be ambitious without overstating the state of implementation. A successful outcome may be a strong toolchain for understanding the ecosystem rather than immediate game execution.
