# Loader and native execution design

**Status: proposed design.** This file specifies how a loader might be engineered and tested; it does not assert that any Xbox Series executable has been loaded.

## A. Inspection before execution

Two distinct tools are proposed:

- `dbx-inspect`: a **read-only** metadata inspector, initially for synthetic PE/COFF files. It may print machine type, PE signature, section table, image base, declared entry RVA and import directory where properly bounded.
- `dbx-loader`: a future, explicitly opt-in mapping component. It accepts only a validated `ImagePlan`. At the beginning, it maps data and refuses to jump to any entry point.

A file that resembles PE/COFF is not proof that an Xbox application can be executed by the Windows loader.

### Strict inspection algorithm

1. Read with bounded file size, maximum 128 MiB for research fixtures by default.
2. Confirm DOS magic and validate `e_lfanew` as an unsigned offset before accessing it.
3. Validate PE signature, COFF header size and optional header declared size.
4. Require supported machine identifiers for the fixture format; initially `IMAGE_FILE_MACHINE_AMD64` for x64 tests.
5. For each section, bounds-check raw offsets and sizes with overflow-safe arithmetic.
6. Report overlaps, anomalous counts, out-of-range data directories, and truncated structures.
7. Return a nonzero error code with concise context on malformed data.

The above is specific to *PE/COFF fixtures*. A separate research task must establish how real Scarlett-targeted programs are represented, including packaging and any platform-specific metadata.

## B. Proposed mapping pipeline

```text
Input --> Inspect --> Normalize --> Validate --> Reserve --> Map
            |            |          |           |       |
          JSON        ImagePlan    policy     address  sections
                                                   |
                                              Relocate
                                                   |
                                              Bind imports
                                                   |
                                              Protect pages
                                                   |
                                              Report READY
```

`READY` here means that the loader has constructed a *synthetic in-memory image*, not that it is safe or able to run an Xbox title.

- **Reserve:** calculate `SizeOfImage` and align pages. Verify max memory budget; use `VirtualAlloc2` or `VirtualAlloc` only as justified by the host.
- **Map:** copy validated section bytes, zero-fill `VirtualSize - SizeOfRawData`, reject conflicting overlaps. Do not map untrusted files executable in the research tool.
- **Relocate:** for synthetic PE64 fixture relocations, compute the actual minus preferred base delta and apply only recognized relocation types.
- **Imports:** resolve known test exports through an explicit allowlist; do not fall back to host `GetProcAddress` for unknown guest imports.
- **Protect:** assign final page protections after relocation and binding. Tests should verify that writable/executable overlap is avoided where possible.
- **TLS and unwind:** eventually model thread-local initialization, exception tables, and runtime function registration, but defer execution until ABI correctness is demonstrated.

### Image states

`Unseen -> Parsed -> Validated -> Mapped -> Bound -> Ready`, with `Rejected` from every transition. The state should be monotonic and logged with a unique trace ID.

## C. Guest ABI boundary

A future guest-facing API shim needs to resolve calling conventions, alignment, ownership and structure layout, not just symbol names.

Proposed dispatch:

```cpp
struct GuestCall {
    SymbolId id;                 // Directbox-controlled identifier
    std::span<const std::byte> request;
    GuestThreadId thread;
};
struct GuestReply {
    DbxResult status;
    std::vector<std::byte> payload;
};
GuestReply dispatch(const GuestCall& call);
```

This is **not** an actual console syscall ABI; it is a testable internal message format. Production guest thunks, if ever possible, would translate verified guest call conventions into the internal dispatch model.

Test the following on original code:
- Integer arguments in registers vs stack positions;
- 16-byte stack alignment and nonvolatile registers;
- Struct packing, pointer width and sign extension;
- TLS, SIMD registers and error-result propagation;
- Callbacks and reentrancy, without outliving their host object.

## D. Native execution experiment

Native execution is a *conditional* goal. Only after original test stubs validate mapping and guest/host thunks:

1. Use a self-authored function with fixed inputs/outputs.
2. Map it with explicit host permissions and record address choices.
3. Call via a guarded test harness.
4. Compare output, side effects, register clobbers and faults against the native reference.
5. Add exception isolation and stack tracing.

At no stage should a "hello world" host-native function be advertised as executing an Xbox program.

## E. Exit criteria

- Reproducible malformed-input rejection and section decoding;
- Synthetic image mapping with no unsupported relocations silently ignored;
- An import resolver that fails with stable, typed diagnostics;
- A guarded native x64 function call with ABI assertions;
- Independent review of the evidence before a public "loader milestone" announcement.
