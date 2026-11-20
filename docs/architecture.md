# Proposed architecture

This is a **design hypothesis**, not a description of an existing executable implementation.

```text
   Scarlett-targeted application (future research)
                       |
             Package / metadata study
                       |
             Native x86-64 code path
                       |
       +---------------+---------------+
       |               |               |
  Runtime bridge   Graphics bridge   Platform services
       |               |               |
  Host API stubs     D3D12 research   I/O, audio, input
       +---------------+---------------+
                       |
                  Windows host
```

## Native execution
The x86-64 ISA overlap between Xbox Series and PCs suggests investigating direct execution of compatible machine instructions. This does not imply binary compatibility: machine code can depend on ABI conventions, memory constraints, security controls, and external services that differ significantly.

## Runtime boundary
A guest-facing dispatch layer could replace selected environment services with host implementations. Each API would require verified semantics, not merely matching function names. Unknown calls should fail observably, not be silently ignored.

## Graphics boundary
Xbox Series is associated with a console-specific D3D12.X environment. A future graphics bridge would need to establish the actual resource models, command behavior, shader formats, and host driver requirements before promising compatibility. Desktop D3D12 alone is not a drop-in substitute.

## Testing strategy
Start with self-authored, freely redistributable fixtures. Validate one boundary at a time, recording expected outputs, actual outputs, and trace artifacts. No proprietary SDK binaries, leaked games, or console keys are required for the documentation and proposed initial prototypes.

## Non-goals for the initial research stage
- Claiming a working Series X|S loader before one exists
- Reproducing proprietary firmware from redistributed binaries
- Representing game-resource inspection as proof of game execution
