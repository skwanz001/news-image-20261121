# Entry program for make.fun's "Sum up 21 November's world news in one
# image" bounty (news-image-20261121). The repository holds the poster as
# entry.png, drawn for Saturday 21 November 2026; this program validates
# it against the contest's file gate and copies it to /output/entry.png.
# Standard library only, no network, deterministic: both graded runs write
# exactly the same bytes.
import os
import shutil
import struct
import sys

MAX_BYTES = 1_048_576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8\xff"


def find_image():
    here = os.path.dirname(os.path.abspath(__file__))
    for candidate in (os.path.join(here, "entry.png"), "/bot/entry.png"):
        if os.path.isfile(candidate):
            return candidate
    raise FileNotFoundError("entry.png is not beside main.py")


def main():
    src = find_image()
    size = os.path.getsize(src)
    if size > MAX_BYTES:
        raise ValueError(f"entry.png is {size} bytes, over the 1 MiB gate")
    with open(src, "rb") as f:
        head = f.read(8)
    if not (head.startswith(PNG_MAGIC) or head.startswith(JPEG_MAGIC)):
        raise ValueError("entry.png is neither a PNG nor a JPEG")
    if head.startswith(PNG_MAGIC):
        with open(src, "rb") as f:
            f.seek(16)
            width, height = struct.unpack(">II", f.read(8))
        if width > 1024 or height > 1024:
            raise ValueError(f"entry.png is {width}x{height}, over the 1024 gate")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dest)
    print(f"wrote {dest} ({size} bytes)", file=sys.stderr)


if __name__ == "__main__":
    main()
