# Platform notes: Xbox Series X|S

## Naming
- **Durango** refers to the Xbox One generation.
- **Scarlett** is associated with the Xbox Series generation.
- **GDK** refers to Microsoft's Game Development Kit ecosystem, covering differing targets and platform capabilities.
- **D3D12.X** is the console-specific Direct3D 12 family, not a guarantee of desktop compatibility.

## Why x86-64 matters
The host and target ISA overlap is promising: some code may avoid full instruction-set emulation. But successful execution also requires compatible calling conventions, operating system services, memory behavior, driver interfaces, graphics support, and the application's expected runtime environment.

## Research questions
1. Which behavior is shared with Windows x86-64 and which is console-specific?
2. Which publicly documented interfaces can be safely modeled in an independent stub?
3. Which graphics abstractions could be tested using original workloads?
4. What is the smallest reproducible, non-proprietary execution milestone?

## Useful starting points
- Microsoft GDK documentation: https://learn.microsoft.com/en-us/gaming/gdk/
- Microsoft PE format specification: https://learn.microsoft.com/en-us/windows/win32/debug/pe-format
- Direct3D 12 documentation: https://learn.microsoft.com/en-us/windows/win32/direct3d12/direct3d-12-graphics

This document is a study outline. Any deeper claim about undocumented Scarlett internals needs its own cited evidence.
