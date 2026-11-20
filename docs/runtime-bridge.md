# Runtime bridge implementation proposal

**Status:** host-side design work; no console ABI or implementation is claimed here.

## Goal

Investigate whether the set of services expected by a Scarlett-targeted program could be represented by a host-facing interface and progressively implemented on Windows. The primary challenge is **semantic compatibility**, not matching a function name.

## Interface catalog

Represent each potential API boundary as a versioned record:

```yaml
interface_id: dbx.test.clock.monotonic
provenance: directbox-synthetic
signature: "() -> u64_nanoseconds"
threading: any
lifetime: process
error_behavior: typed-result
implementation: windows-qpc-adapter-proposed
status: design
tests:
  - monotonic-order
  - rollover
  - concurrent-reads
```

All example IDs are Directbox-owned. Do not copy private Xbox API definitions into the repository.

## Contract priorities

### P0: process foundation
- **Clock:** monotonic performance counters; do not conflate wall-clock time with elapsed time.
- **Virtual memory:** reserve/commit/decommit/query operations with page alignment and per-guest quotas.
- **Handles:** 64-bit opaque IDs with type tags, generation counters and reference ownership.
- **Threads and events:** create/join/signal/wait; avoid translating critical timing paths into unbounded blocking calls.
- **Diagnostics:** symbolize Directbox module frames separately from unknown guest frames.

### P1: asynchronous host services
- **Task queues:** model work and completion queues independently; support deterministic test dispatch.
- **Filesystem:** bounded virtual paths, normalized separators, explicit read-only and writable mount points.
- **User-facing state:** lifecycle, activation, suspend/resume test events, not just always-on placeholders.
- **Saves:** use a project-defined transactional store for test programs; do not impersonate Microsoft entitlement or cloud-save endpoints.
- **Input:** XInput or GameInput can provide a host controller adapter, with a separate guest-neutral event representation.

### P2: audio and optional services
- **Audio:** create a neutral buffer and voice abstraction before selecting WASAPI/XAudio2 on Windows.
- **Networking:** loopback-only tests initially; live multiplayer, identity and authorization are excluded without a legitimate supported service path.
- **Telemetry:** ring buffers, monotonically numbered events and per-thread trace contexts.

## Handle implementation (concept)

```cpp
struct Handle {
    uint32_t index;
    uint16_t generation;
    uint16_t kind;
};
struct HandleEntry {
    uint16_t generation;
    Kind kind;
    std::shared_ptr<HostObject> object;
};
```

On close, increment generation and recycle only after synchronization. Calls with a stale generation return `DBX_E_INVALID_HANDLE`. Never interpret guest-provided integer handles directly as Windows `HANDLE` pointers.

## Asynchronous dispatch

```text
guest request --> validate --> operation queue --> Windows async I/O
      |                                               |
      +<-- completion queue <-- translate result <----+
```

Use sequence IDs to detect duplicates or missing completion events. Preserve the *documented* ordering required by individual APIs; do not invent ordering guarantees globally.

Example internal call model:

```cpp
TaskToken enqueue_io(GuestFile file, ReadRequest request);
bool try_pop_completion(TaskToken token, IoCompletion& out);
```

Use `std::span` or bounded views when passing buffers. Copy buffers when lifetime cannot be safely guaranteed across asynchronous operations.

## Memory semantics research

The Xbox Game OS offers target-specific memory and resource contracts. Proposed translation must separate:
- Address reservation versus commitment;
- CPU visibility versus GPU accessibility;
- Page protection and executable mapping;
- Fixed/relative pointer layouts;
- Synchronization and cache coherence requirements.

A PC adapter cannot promise identical behavior without measurement. Begin with original stress fixtures: misaligned buffers, low-memory failures, repeated map/unmap, cross-thread transfers, and shutdown races.

## Error and observability policy

Never return "success" for an unimplemented service just to advance a startup sequence. Return an explicit `DBX_E_UNIMPLEMENTED` with:
- interface ID;
- call site and thread;
- normalized arguments (redacted where needed);
- expected contract source;
- host adapter version.

A noisy truthful failure is better engineering evidence than a silent no-op.

## Runtime acceptance suite

1. 100,000 create/close cycles with no stale-handle success.
2. Clock samples remain monotonic across multiple threads.
3. Async completions resolve once and only once.
4. VFS cannot escape a configured root.
5. Suspend/resume simulated lifecycle leaves no orphan callbacks.
6. Fault injection reveals deterministic error codes.

Targets here are **proposed acceptance tests**, not recorded measurements.
