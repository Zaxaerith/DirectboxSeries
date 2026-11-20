# Validation, evidence and compatibility reporting

Directbox Series should use ambitious goals and conservative evidence.

## State vocabulary

| State | Required public evidence |
| --- | --- |
| Idea | Problem statement and intended outcome |
| Design | Reviewed architecture / interface proposal |
| Prototype | Code and reproduction steps for a controlled fixture |
| Verified | Tests with logs and independent reproduction |
| Integrated | Multiple validated components demonstrated together |
| Game-specific exploration | Clearly attributed observations and supported assets |
| Compatible | Repeatable end-to-end execution with defined limitations |

A design document is not a compatibility result.

## Technical milestones and failure taxonomy

| Area | First proposed test | Critical failures to classify |
| --- | --- | --- |
| File inspection | Synthetic x64 PE sample | truncated-header, invalid-offset, overflow |
| Image model | Section/relocation fixture | incompatible-layout, unresolved-symbol |
| ABI | Own x64 call stub | bad-stack-alignment, register-clobber |
| Runtime | clock/handle/task suite | deadlock, double-close, dropped completion |
| Memory | mapping/quota stress test | invalid-access, guard-page fault |
| VFS | randomized path fixture | traversal, symlink-escape, partial-read |
| Graphics | original triangle + texture | device-lost, invalid-barrier, shader-fail |
| Audio | generated PCM chirp | underrun, latency drift |
| Input | recorded local controller inputs | wrong mapping, replay mismatch |
| Lifecycle | suspend/resume model | leaked-task, illegal-transition |

## Trace format proposal

Use newline-delimited JSON; one object per event:

```json
{"schema":1,"session":"fixture-001","seq":12,"t_ns":1844002,"thread":4,"module":"dbx-inspect","level":"info","event":"pe.section","data":{"name":".text","raw_size":512}}
{"schema":1,"session":"fixture-001","seq":13,"t_ns":1844302,"thread":4,"module":"dbx-loader","level":"error","event":"unsupported.import","data":{"id":"test.symbol.42"}}
```

**Illustrative fake events only**, included as a schema example, not logs from an actual run. Timestamp sources must be monotonic and per-run sequences strictly increasing. Logs should redact user paths and secrets by default.

## Reproducibility record

Every genuine report should contain:
- Commit SHA and component versions;
- Host Windows build, CPU, GPU and driver;
- Fixture identity, source and SHA-256;
- Exact command and environment;
- Observed behavior, expected behavior and known deviations;
- Raw diagnostic log where appropriate;
- Whether the result is locally observed, independently reproduced, or only hypothesized.

## Gate policy

- A new high-level capability must first demonstrate a self-authored fixture.
- Compatibility claims require a repeatable setup and logs; a static image proves only that an image existed.
- Traces of protected or proprietary assets must not be redistributed.
- No performance headline without a reproducible workload and measurement methodology.
- No automatic pull-request merge based solely on a green Markdown lint job.

## Example release labels

- `research-note/YYYY-MM`: documentation-only publication
- `prototype/peprobe-0.1`: bounded inspection utility
- `lab/loader-fixture-0.1`: synthetic loader proof of concept
- `alpha`: reserved for a functional integrated runtime, not a repository initialization

These labels are proposals, not existing releases.
