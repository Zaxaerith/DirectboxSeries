# Graphics translation research: D3D12.X to Windows graphics

**Status:** exploration plan, not an implemented translator.

## Ground truth and unknowns

Microsoft documents that Xbox GDK targets a console-specific D3D12.X graphics environment, and public vcpkg documentation identifies distinct Scarlett target triplets. The undocumented differences, driver contracts, shader representations and hardware expectations of any given game cannot be inferred from API naming alone.

Do **not** state that Xbox Series GPU command buffers or shaders can simply be sent to a PC GPU.

Primary public references:
- https://learn.microsoft.com/en-us/gaming/gdk/docs/gdk-dev/intro/introduction
- https://learn.microsoft.com/en-us/vcpkg/users/platforms/xbox
- https://learn.microsoft.com/en-us/windows/win32/direct3d12/direct3d-12-graphics

## Proposed architecture

```text
    Potential guest rendering API
                 |
     [verified frontend required]
                 |
          dbx-gfx frontend
                 |
       DBX Render IR (owned)
                 |
      +----------+-----------+
      |                      |
  Validation              Trace capture
      |
  Host D3D12 backend  ----> D3D12 debug layer / PIX (where available)
      |
  Windows GPU driver
```

The **DBX Render IR** is an original Directbox design for testing, not a decoded representation of Xbox commands.

## Initial IR

```cpp
enum class CommandKind {
    CreateBuffer, CreateTexture, Upload, Barrier,
    SetPipeline, SetBindings, Draw, Dispatch, Present
};
struct ResourceDesc {
    uint64_t size_bytes;
    Format format;
    UsageFlags usage;
    uint32_t width, height, depth;
};
struct RenderCommand {
    CommandKind kind;
    CommandPayload payload; // tagged union, project-defined
};
```

All resource IDs must be opaque and generation-checked; command execution must have explicit ordering and lifetime rules.

## Translation subsystems

### Resources and heaps
- Track buffer/texture dimensions, formats, alignment and host allocation.
- Maintain resource state transitions explicitly.
- Distinguish CPU-visible upload resources from GPU-local resource usage.
- Model aliasing and lifetime conflicts with validation errors rather than undefined host-driver behavior.

### Command lists and queues
- Record original command stream into Directbox IR.
- Group draws/dispatches by queue and dependency.
- Use fence-backed retirement for temporary allocations.
- Validate that no descriptor or upload allocation is retired before GPU completion.

### Descriptors and binding
- Maintain project-defined tables for SRV, UAV, CBV and samplers.
- Separate guest-neutral logical resource identity from host descriptor heaps.
- Reject out-of-range bindings; never silently bind a null descriptor to hide a missing semantic contract.

### Shaders and pipelines
- Stage 1: compile **self-authored HLSL** via supported desktop tools; verify ordinary D3D12 pipelines.
- Stage 2: develop IR representation for resources, signatures, specialization and validation.
- Stage 3: investigate the actual representations encountered in lawful Scarlett research. Their compatibility with desktop DXIL must be established empirically; no assumption of direct loading.
- Stage 4: evaluate translation, re-compilation or unsupported-format handling based on observed facts.

### Synchronization and presentation
- Track producer/consumer dependencies and hazards.
- Implement fences and bounded waits, with deadlock detection.
- Use DXGI swap chains for the first Windows prototype; do not treat them as equivalent to console presentation behavior until verified.

## Proposed acceptance sequence

| Gate | Original workload | Evidence |
| --- | --- | --- |
| G0 | Create D3D12 device and report features | Capabilities JSON |
| G1 | Triangle with fixed color | Screenshot + source + hash |
| G2 | Textured quad / descriptor table | Pixel compare |
| G3 | Compute write then render read | Fence correctness trace |
| G4 | Multi-queue resource use | No validation errors |
| G5 | Resize, suspend, device loss | Controlled recovery trace |
| G6 | Frame pacing | p50/p95/p99 latency report |

Performance must be measured after correctness. A 30 FPS target for a future commercial game is not a meaningful forecast before a reproducible workload exists.

## Performance knobs to evaluate
- Pipeline state cache keyed by complete source/config identity;
- Upload staging with per-frame transient heaps;
- Descriptor reuse with generation tracking;
- CPU trace sampling rather than full logging in performance mode;
- GPU/CPU fence overlap and asynchronous loading.

Each optimization requires an A/B correctness regression. Optimizations must not change results silently.
