# PEProbe — first Directbox research prototype

PEProbe is a deliberately narrow **read-only, generic PE/COFF inspector**. It demonstrates how Directbox plans to build bounded file processing and reproducible reports. It neither executes programs nor implements Xbox Series-specific parsing.

## Usage

```powershell
python prototypes/peprobe.py PATH_TO_YOUR_OWN_PE_FIXTURE --json
python -m unittest discover -s prototypes -p "test_*.py"
```

Requires Python 3.11+. The provided tests create synthetic, non-proprietary fixtures in memory.

## Design constraints

- 128 MiB input limit; 96-section sanity cap
- Checked offsets, checked header size and section ranges
- No memory mapping of executable pages, no import resolution, no code execution
- No Xbox game data, SDK, or protected package required

CI is intended to execute these tests using GitHub Actions. The tests have not been represented as passed until the workflow confirms them.

## Next steps

Expand with clearly bounded parsing of import/relocation metadata on self-authored fixtures, structured errors and corpus-based malformed-file tests.
