"""Self-contained unit tests; generates synthetic files only."""
import struct
import unittest

from peprobe import ProbeError, inspect

def fixture(machine=0x8664, count=1):
    b = bytearray(0x400)
    b[0:2] = b"MZ"
    struct.pack_into("<I", b, 0x3C, 0x80)
    b[0x80:0x84] = b"PE\0\0"
    struct.pack_into("<H", b, 0x84, machine)
    struct.pack_into("<H", b, 0x86, count)
    struct.pack_into("<H", b, 0x94, 0xF0)
    struct.pack_into("<H", b, 0x98, 0x20B)
    struct.pack_into("<I", b, 0xA8, 0x1000)
    struct.pack_into("<Q", b, 0xB0, 0x140000000)
    s = 0x188
    b[s:s+8] = b".text\0\0\0"
    struct.pack_into("<IIII", b, s+8, 0x100, 0x1000, 0x200, 0x200)
    struct.pack_into("<I", b, s+36, 0x60000020)
    return bytes(b)

class PEProbeTests(unittest.TestCase):
    def test_pe64(self):
        report = inspect(fixture())
        self.assertEqual(report["format"], "PE32+")
        self.assertEqual(report["machine"], "0x8664")
        self.assertEqual(report["section_count"], 1)
        self.assertEqual(report["sections"][0]["name"], ".text")

    def test_reject_empty(self):
        with self.assertRaises(ProbeError):
            inspect(b"")

    def test_reject_signature(self):
        b = bytearray(fixture())
        b[0:2] = b"NO"
        with self.assertRaises(ProbeError):
            inspect(bytes(b))

    def test_reject_truncated_section(self):
        with self.assertRaises(ProbeError):
            inspect(fixture()[:0x250])

    def test_reject_unreasonable_section_count(self):
        with self.assertRaises(ProbeError):
            inspect(fixture(count=65535))

if __name__ == "__main__":
    unittest.main()
