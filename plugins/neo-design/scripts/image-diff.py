#!/usr/bin/env python3
"""Image diff for comparing the design system against the built interface.

Compares two PNG screenshots pixel by pixel, states the deviation as a
number and writes a difference image in which every deviating spot is
marked in magenta. That turns "looks like the design" into something
proven instead of claimed.

No dependencies: PNG is read and written with the standard library, so the
script runs in any CI.

    image-diff.py design.png built.png
    image-diff.py design.png built.png --diff diff.png --threshold 0.5
    image-diff.py design.png built.png --ignore 20,600,400,40

Exit code 0 when the deviation is below the threshold, 1 otherwise.
"""
from __future__ import annotations

import argparse
import pathlib
import struct
import sys
import zlib

SIGNATURE = b"\x89PNG\r\n\x1a\n"
CHANNELS = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}


class ImageError(ValueError):
    pass


def _unfilter(raw: bytes, width: int, height: int, channels: int) -> bytearray:
    """Undoes the PNG row filters and returns raw pixels."""
    row_length = width * channels
    out = bytearray(row_length * height)
    previous = bytearray(row_length)
    pos = 0
    for y in range(height):
        filter_type = raw[pos]
        pos += 1
        row = bytearray(raw[pos:pos + row_length])
        pos += row_length
        if filter_type == 1:      # Sub
            for i in range(channels, row_length):
                row[i] = (row[i] + row[i - channels]) & 0xFF
        elif filter_type == 2:    # Up
            for i in range(row_length):
                row[i] = (row[i] + previous[i]) & 0xFF
        elif filter_type == 3:    # Average
            for i in range(row_length):
                left = row[i - channels] if i >= channels else 0
                row[i] = (row[i] + ((left + previous[i]) >> 1)) & 0xFF
        elif filter_type == 4:    # Paeth
            for i in range(row_length):
                a = row[i - channels] if i >= channels else 0
                b = previous[i]
                c = previous[i - channels] if i >= channels else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                prediction = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                row[i] = (row[i] + prediction) & 0xFF
        elif filter_type != 0:
            raise ImageError(f"Unknown row filter {filter_type}")
        out[y * row_length:(y + 1) * row_length] = row
        previous = row
    return out


def read_png(path: pathlib.Path) -> tuple[int, int, bytearray]:
    """Reads a PNG and returns width, height and the pixels as RGB."""
    data = path.read_bytes()
    if not data.startswith(SIGNATURE):
        raise ImageError(f"{path} is not a PNG file")
    pos = len(SIGNATURE)
    width = height = colour_type = bit_depth = 0
    idat = bytearray()
    palette = b""
    while pos < len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        kind = data[pos + 4:pos + 8]
        content = data[pos + 8:pos + 8 + length]
        pos += 12 + length
        if kind == b"IHDR":
            width, height, bit_depth, colour_type, _, _, interlaced = struct.unpack(
                ">IIBBBBB", content)
            if bit_depth != 8:
                raise ImageError(f"{path}: only 8 bit per channel, found {bit_depth}")
            if interlaced:
                raise ImageError(f"{path}: interlaced PNG are not read")
            if colour_type not in CHANNELS:
                raise ImageError(f"{path}: colour type {colour_type} is not read")
        elif kind == b"PLTE":
            palette = content
        elif kind == b"IDAT":
            idat += content
        elif kind == b"IEND":
            break

    channels = CHANNELS[colour_type]
    pixels = _unfilter(zlib.decompress(bytes(idat)), width, height, channels)

    # Bring everything to RGB; alpha is composited over white.
    rgb = bytearray(width * height * 3)
    for i in range(width * height):
        q = i * channels
        if colour_type == 0:
            r = g = b = pixels[q]
        elif colour_type == 2:
            r, g, b = pixels[q], pixels[q + 1], pixels[q + 2]
        elif colour_type == 3:
            k = pixels[q] * 3
            r, g, b = palette[k], palette[k + 1], palette[k + 2]
        elif colour_type == 4:
            a = pixels[q + 1] / 255
            r = g = b = round(pixels[q] * a + 255 * (1 - a))
        else:
            a = pixels[q + 3] / 255
            r = round(pixels[q] * a + 255 * (1 - a))
            g = round(pixels[q + 1] * a + 255 * (1 - a))
            b = round(pixels[q + 2] * a + 255 * (1 - a))
        rgb[i * 3], rgb[i * 3 + 1], rgb[i * 3 + 2] = r, g, b
    return width, height, rgb


def write_png(path: pathlib.Path, width: int, height: int, rgb: bytearray) -> None:
    raw = bytearray()
    for y in range(height):
        raw.append(0)                                   # filter "None"
        raw += rgb[y * width * 3:(y + 1) * width * 3]

    def chunk(kind: bytes, content: bytes) -> bytes:
        return (struct.pack(">I", len(content)) + kind + content
                + struct.pack(">I", zlib.crc32(kind + content) & 0xFFFFFFFF))

    path.write_bytes(
        SIGNATURE
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(bytes(raw), 6))
        + chunk(b"IEND", b""))


def compare(a: tuple[int, int, bytearray], b: tuple[int, int, bytearray],
            tolerance: int, ignore: list[tuple[int, int, int, int]]):
    width, height, left = a
    _, _, right = b
    difference = bytearray(width * height * 3)
    deviating = largest = 0
    total_delta = 0
    skipped = 0

    def ignored(x: int, y: int) -> bool:
        return any(rx <= x < rx + rw and ry <= y < ry + rh for rx, ry, rw, rh in ignore)

    for y in range(height):
        for x in range(width):
            i = (y * width + x) * 3
            if ignored(x, y):
                skipped += 1
                difference[i:i + 3] = bytes((230, 230, 235))
                continue
            d = max(abs(left[i] - right[i]),
                    abs(left[i + 1] - right[i + 1]),
                    abs(left[i + 2] - right[i + 2]))
            largest = max(largest, d)
            total_delta += d
            if d > tolerance:
                deviating += 1
                difference[i:i + 3] = bytes((255, 0, 200))     # magenta
            else:
                # Matching areas stay visible, but pale.
                pale = 255 - (255 - left[i]) // 5
                difference[i], difference[i + 1], difference[i + 2] = pale, pale, pale
    total = width * height
    checked = total - skipped
    return {
        "width": width, "height": height, "total": total, "checked": checked,
        "skipped": skipped, "deviating": deviating,
        "share": (deviating / checked * 100) if checked else 0.0,
        "largest": largest, "mean": (total_delta / checked) if checked else 0.0,
        "image": difference,
    }


def area(text: str) -> tuple[int, int, int, int]:
    parts = text.split(",")
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("give the area as x,y,width,height")
    return tuple(int(p) for p in parts)  # type: ignore[return-value]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Compare two PNG screenshots and state the deviation as a number.",
        epilog="Meant for matching a design proposal against the built interface.")
    parser.add_argument("design", type=pathlib.Path, help="screenshot from the design system")
    parser.add_argument("built", type=pathlib.Path, help="screenshot of the built interface")
    parser.add_argument("--diff", type=pathlib.Path, help="path for the difference image")
    parser.add_argument("--tolerance", type=int, default=8,
                        help="allowed deviation per colour channel, 0 to 255 "
                             "(default 8, covers anti-aliasing)")
    parser.add_argument("--threshold", type=float, default=1.0,
                        help="allowed share of deviating pixels in percent (default 1.0)")
    parser.add_argument("--ignore", type=area, action="append", default=[],
                        metavar="X,Y,W,H", help="exclude an area, may be given more than once")
    args = parser.parse_args(argv)

    try:
        left = read_png(args.design)
        right = read_png(args.built)
    except (ImageError, OSError, zlib.error) as error:
        print(str(error), file=sys.stderr)
        return 2

    if left[0] != right[0] or left[1] != right[1]:
        print(f"The images have different dimensions: "
              f"design {left[0]}x{left[1]}, built {right[0]}x{right[1]}.\n"
              f"Take both screenshots with the same viewport and the same scale.",
              file=sys.stderr)
        return 2

    r = compare(left, right, args.tolerance, args.ignore)
    if args.diff:
        write_png(args.diff, r["width"], r["height"], r["image"])

    print(f"Dimensions       {r['width']} x {r['height']} ({r['total']} pixels)")
    if r["skipped"]:
        areas = "area" if len(args.ignore) == 1 else "areas"
        print(f"Excluded         {r['skipped']} pixels in {len(args.ignore)} {areas}")
    print(f"Deviating        {r['deviating']} of {r['checked']}  =  {r['share']:.3f} %")
    print(f"Largest deviation per channel   {r['largest']}")
    print(f"Mean deviation per channel      {r['mean']:.2f}")
    print(f"Tolerance {args.tolerance}, threshold {args.threshold} %")
    if args.diff:
        print(f"Difference image {args.diff}")
    print()
    if r["share"] <= args.threshold:
        print("Passed. The built interface matches the design.")
        return 0
    print(f"Failed. {r['share']:.3f} % deviate, allowed is {args.threshold} %.")
    if args.diff:
        print("Look at the magenta spots in the difference image and align them.")
    else:
        print("Use --diff to write a difference image and see where the spots are.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
