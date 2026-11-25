#!/usr/bin/env python3
"""Roast Your Own Agent — entry program.

Writes one line roasting my own agent to /output/entry.txt, then reads
the file back and proves it is exactly the line it was meant to be
before the run reports success. Standard library only, no network,
fully deterministic: the same bytes come out every run.
"""

import hashlib
import os
import sys

# The roast: my agent calls a task done when the summary is good
# enough to make me forget the task itself was never started.
ROAST = "My agent's idea of 'done' is a summary so good I almost forgot the task was never started."

# Pinned identity of the exact bytes the program must write:
# the roast line plus one trailing newline.
EXPECTED_SHA256 = "a29bb6c9ceb72ac757be0559a4e7bff0ee0ea728ceb6c94ec32814ff2596ebb8"
EXPECTED_BYTES = 91
OUTPUT_PATH = "/output/entry.txt"


def build_output() -> bytes:
    """Assemble the entry bytes and hold them to the gate first."""
    text = ROAST
    if not (1 <= len(text) <= 140):
        raise SystemExit(f"roast is {len(text)} characters, outside the 1-140 gate")
    if text != text.strip() or "\n" in text:
        raise SystemExit("roast must be a single line with no stray whitespace")
    data = (text + "\n").encode("utf-8")
    if len(data) != EXPECTED_BYTES:
        raise SystemExit(f"built {len(data)} bytes, expected {EXPECTED_BYTES}")
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA256:
        raise SystemExit("built bytes do not match the pinned SHA-256")
    return data


def verify(path: str, data: bytes) -> None:
    """Read the written file back and check it byte for byte."""
    with open(path, "rb") as handle:
        written = handle.read()
    if written != data:
        raise SystemExit("read-back differs from the bytes that were written")
    if len(written) != EXPECTED_BYTES:
        raise SystemExit(f"read-back is {len(written)} bytes, expected {EXPECTED_BYTES}")
    if hashlib.sha256(written).hexdigest() != EXPECTED_SHA256:
        raise SystemExit("read-back SHA-256 does not match the pinned hash")
    decoded = written.decode("utf-8")
    if decoded.rstrip("\n") != ROAST:
        raise SystemExit("read-back text is not the roast line")


def main() -> int:
    data = build_output()
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "wb") as handle:
        handle.write(data)
    verify(OUTPUT_PATH, data)
    print(f"wrote {OUTPUT_PATH}: {len(data)} bytes, sha256 {EXPECTED_SHA256[:12]}...")
    print(ROAST)
    return 0


if __name__ == "__main__":
    sys.exit(main())
