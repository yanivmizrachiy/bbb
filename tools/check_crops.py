# -*- coding: utf-8 -*-
"""Review aid: surface raster crops that MIGHT bleed stray text at an edge.

Signature of a bad crop (e.g. an unrelated paragraph line caught below a photo,
as once happened to the bicycle figure): a band of ink within the top/bottom
margin, separated from the main artwork by a clear white gap.

This is a heuristic REVIEW AID, not a pass/fail gate: legitimate crops also trip
it (a question diagram that includes its own text, a graph with axis labels, a
word-problem rendered as an image). Always eyeball each flagged crop — only a
*pure figure* with *unrelated* stray text is an actual bleed to re-crop.

Usage:  python tools/check_crops.py     # scan every */assets/*.png, list candidates
Run after regenerating worksheets, then visually review the flagged crops.
"""
import glob
import os
import sys

try:
    from PIL import Image
except ImportError:
    print("Pillow required: pip install Pillow")
    sys.exit(2)

DARK = 128            # pixel < DARK counts as ink
ROW_INK = 0.02        # fraction of row that must be ink to be "content"
EDGE = 0.16           # only inspect the top/bottom 16% of the image
MIN_GAP = 0.04        # white gap (fraction of H) separating bleed from artwork
MAX_BAND = 0.13       # a bleed band is at most this tall (fraction of H)


def row_is_content(px, W, y):
    ink = sum(1 for x in range(0, W, 2) if px[x, y] < DARK)
    return ink > ROW_INK * (W / 2)


def suspect(path):
    im = Image.open(path).convert("L")
    W, H = im.size
    px = im.load()
    content = [row_is_content(px, W, y) for y in range(H)]
    if not any(content):
        return None
    top = content.index(True)
    bottom = H - 1 - content[::-1].index(True)

    edge = int(EDGE * H)
    gap = int(MIN_GAP * H)
    band = int(MAX_BAND * H)

    # bottom bleed: a content band ending near the bottom edge, preceded by a
    # white gap, that is short (a text line, not the figure).
    for y0 in range(bottom, max(bottom - band, top), -1):
        if not content[y0]:
            continue
        # walk up the band
        b = y0
        while b > top and content[b]:
            b -= 1
        band_h = y0 - b
        gap_above = 0
        g = b
        while g > top and not content[g]:
            g -= 1
            gap_above += 1
        if bottom - y0 < edge and gap_above >= gap and band_h <= band and g > top:
            return f"bottom-bleed (band {band_h}px, gap {gap_above}px below artwork)"
        break

    # top bleed (symmetric)
    for y0 in range(top, min(top + band, bottom)):
        if not content[y0]:
            continue
        b = y0
        while b < bottom and content[b]:
            b += 1
        band_h = b - y0
        gap_below = 0
        g = b
        while g < bottom and not content[g]:
            g += 1
            gap_below += 1
        if y0 - top < edge and gap_below >= gap and band_h <= band and g < bottom:
            return f"top-bleed (band {band_h}px, gap {gap_below}px above artwork)"
        break
    return None


def main():
    strict = "--strict" in sys.argv
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = sorted(glob.glob(os.path.join(root, "*", "assets", "*.png")))
    flagged = []
    for p in paths:
        if p.endswith(".bak"):
            continue
        try:
            r = suspect(p)
        except Exception as e:  # noqa
            r = f"error: {e}"
        if r:
            rel = os.path.relpath(p, root)
            flagged.append((rel, r))
            print(f"SUSPECT  {rel}  -- {r}")
    print(f"\nScanned {len(paths)} crops, {len(flagged)} suspect.")
    if strict and flagged:
        sys.exit(1)


if __name__ == "__main__":
    main()
