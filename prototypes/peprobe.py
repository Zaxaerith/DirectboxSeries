#!/usr/bin/env python3
"""Directbox PEProbe: bounded, read-only PE/COFF metadata inspector.

This is an original generic Windows PE parser research tool.
It does not load or execute binaries, and it is NOT an Xbox Series loader.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import struct
import sys

MAX_BYTES = 128 * 1024 * 1024
MAX_SECTIONS = 96

class ProbeError(ValueError):
    pass

def check_range(data: bytes, off: int, size: int, field: str) -> None:
    if off < 0 or size < 0 or off > len(data) or size > len(data) - off:
        raise ProbeError(f"{field}: out-of-bounds range offset={off} size={size}")

def read_u16(data: bytes, off: int, field: str) -> int:
    check_range(data, off, 2, field)
    return struct.unpack_from("<H", data, off)[0]

def read_u32(data: bytes, off: int, field: str) -> int:
    check_range(data, off, 4, field)
    return struct.unpack_from("<I", data, off)[0]

def read_u64(data: bytes, off: int, field: str) -> int:
    check_range(data, off, 8, field)
    return struct.unpack_from("<Q", data, off)[0]

def inspect(data: bytes) -> dict:
    if len(data) > MAX_BYTES:
        raise ProbeError("fixture exceeds 128 MiB limit")
    check_range(data, 0, 64, "DOS header")
    if data[:2] != b"MZ":
        raise ProbeError("invalid DOS signature")
    pe = read_u32(data, 0x3C, "e_lfanew")
    check_range(data, pe, 24, "PE/COFF header")
    if data[pe:pe + 4] != b"PE\0\0":
        raise ProbeError("invalid PE signature")
    machine = read_u16(data, pe + 4, "Machine")
    sections_count = read_u16(data, pe + 6, "NumberOfSections")
    if sections_count > MAX_SECTIONS:
        raise ProbeError("unreasonable section count")
    optional_size = read_u16(data, pe + 20, "SizeOfOptionalHeader")
    opt = pe + 24
    check_range(data, opt, optional_size, "OptionalHeader")
    if optional_size < 24:
        raise ProbeError("optional header too short")
    magic = read_u16(data, opt, "OptionalHeader.Magic")
    if magic not in (0x10B, 0x20B):
        raise ProbeError(f"unsupported optional header magic 0x{magic:x}")
    pe32plus = magic == 0x20B
    required = 112 if pe32plus else 96
    if optional_size < required:
        raise ProbeError("optional header is truncated")
    entry = read_u32(data, opt + 16, "AddressOfEntryPoint")
    image_base = read_u64(data, opt + 24, "ImageBase") if pe32plus else read_u32(data, opt + 28, "ImageBase")
    section_table = opt + optional_size
    check_range(data, section_table, sections_count * 40, "section table")
    parsed = []
    for i in range(sections_count):
        s = section_table + i * 40
        name = data[s:s+8].split(b"\0", 1)[0].decode("ascii", "backslashreplace")
        virtual_size = read_u32(data, s + 8, "section.VirtualSize")
        virtual_address = read_u32(data, s + 12, "section.VirtualAddress")
        raw_size = read_u32(data, s + 16, "section.SizeOfRawData")
        raw_offset = read_u32(data, s + 20, "section.PointerToRawData")
        if raw_size:
            check_range(data, raw_offset, raw_size, f"section {i} raw bytes")
        characteristics = read_u32(data, s + 36, "section.Characteristics")
        parsed.append({
            "name": name, "virtual_address": virtual_address,
            "virtual_size": virtual_size, "raw_offset": raw_offset,
            "raw_size": raw_size, "characteristics": f"0x{characteristics:08x}"
        })
    return {
        "format": "PE32+" if pe32plus else "PE32",
        "machine": f"0x{machine:04x}",
        "entry_rva": entry,
        "image_base": image_base,
        "section_count": sections_count,
        "sections": parsed,
        "note": "Generic PE/COFF metadata only; does not imply Xbox Series compatibility."
    }

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("file", type=Path, help="Self-authored or authorized local PE fixture")
    ap.add_argument("--json", action="store_true", help="JSON output (default also JSON)")
    args = ap.parse_args(argv)
    try:
        if args.file.stat().st_size > MAX_BYTES:
            raise ProbeError("fixture exceeds 128 MiB limit")
        data = args.file.read_bytes()
        result = inspect(data)
    except (ProbeError, OSError) as exc:
        print(f"peprobe: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
