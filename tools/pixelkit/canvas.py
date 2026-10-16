"""Letter canvas and text-grid parts."""
from __future__ import annotations

TRANSPARENT = "."
NO_OUTLINE = set("Ee%")          # effect + ground-shadow letters never get an outline
KEEP = "?"


class Part:
    """A sparse set of letter pixels with an anchor.

    `pixels` maps (x, y) -> letter, in the part's own space. The anchor is the
    point that gets placed on the canvas position you blit to.
    """

    def __init__(self, pixels: dict, anchor=(0, 0)):
        self.pixels = dict(pixels)
        self.anchor = tuple(anchor)

    # -- geometry helpers ------------------------------------------------
    def bbox(self):
        if not self.pixels:
            return (0, 0, 0, 0)
        xs = [p[0] for p in self.pixels]
        ys = [p[1] for p in self.pixels]
        return (min(xs), min(ys), max(xs), max(ys))

    def shifted(self, dx, dy) -> "Part":
        return Part({(x + dx, y + dy): c for (x, y), c in self.pixels.items()},
                    (self.anchor[0] + dx, self.anchor[1] + dy))

    def with_anchor(self, ax, ay) -> "Part":
        return Part(self.pixels, (ax, ay))

    def recolor(self, mapping: dict) -> "Part":
        """Swap letters, e.g. {'c': 'a'} to turn primary cloth into accent."""
        return Part({k: mapping.get(v, v) for k, v in self.pixels.items()}, self.anchor)

    def union(self, other: "Part") -> "Part":
        px = dict(self.pixels)
        px.update(other.pixels)
        return Part(px, self.anchor)

    def __len__(self):
        return len(self.pixels)


def grid(text: str, anchor=(0, 0), keep_spaces=False) -> Part:
    """Parse a text grid into a Part.

    Lines are taken as-is (leading blank lines stripped); '.' and ' ' are
    transparent unless keep_spaces=True. Use '?' for a no-op pixel.
    """
    lines = text.split("\n")
    while lines and lines[0].strip() == "":
        lines.pop(0)
    while lines and lines[-1].strip() == "":
        lines.pop()
    px = {}
    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            if ch == TRANSPARENT or ch == KEEP:
                continue
            if ch == " " and not keep_spaces:
                continue
            px[(x, y)] = ch
    return Part(px, anchor)


def flip_part(p: Part, swap_shading=True) -> Part:
    """Mirror horizontally about the anchor. Light comes from the upper-left,
    so a mirrored part swaps its highlight/shadow letters by default."""
    ax, ay = p.anchor
    swap = {"S": "z", "z": "S", "H": "g", "g": "H", "C": "k", "k": "C",
            "A": "q", "q": "A", "M": "n", "n": "M", "L": "j", "j": "L"}
    out = {}
    for (x, y), c in p.pixels.items():
        nx = 2 * ax - x
        out[(nx, y)] = swap.get(c, c) if swap_shading else c
    return Part(out, (ax, ay))


def rot90_part(p: Part, times=1) -> Part:
    """Rotate 90° clockwise `times` times about the anchor (screen coords)."""
    ax, ay = p.anchor
    px = p.pixels
    for _ in range(times % 4):
        px = {(ax - (y - ay), ay + (x - ax)): c for (x, y), c in px.items()}
    return Part(px, (ax, ay))


class Canvas:
    """A W×H letter grid. Parts are blitted in painter order; each part can
    carry its own one-pixel outline so overlapping parts stay separated the
    way GBA sprites do."""

    def __init__(self, w=64, h=64):
        self.w, self.h = w, h
        self.px = [[TRANSPARENT] * w for _ in range(h)]

    def get(self, x, y):
        if 0 <= x < self.w and 0 <= y < self.h:
            return self.px[y][x]
        return TRANSPARENT

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h and c != KEEP:
            self.px[y][x] = c

    def blit(self, part: Part, x: int, y: int, outline=True, over=True, outline_letter="o"):
        """Place `part` so its anchor lands on (x, y).

        outline=True draws a dark ring around the part's silhouette *under* the
        part, which produces both the outer outline and the separation lines
        between overlapping parts. Effect/shadow letters are never outlined.
        over=False only paints onto transparent pixels (for back layers).
        """
        ox, oy = x - part.anchor[0], y - part.anchor[1]
        if outline:
            ring = set()
            for (px, py), c in part.pixels.items():
                if c in NO_OUTLINE:
                    continue
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    q = (px + dx, py + dy)
                    if q not in part.pixels or part.pixels[q] in NO_OUTLINE:
                        ring.add(q)
            for (px, py) in ring:
                cx, cy = px + ox, py + oy
                under = self.get(cx, cy)
                if over or under == TRANSPARENT:
                    if under not in NO_OUTLINE:   # don't outline over slash effects
                        self.set(cx, cy, outline_letter if under != TRANSPARENT else "o")
        for (px, py), c in part.pixels.items():
            cx, cy = px + ox, py + oy
            if over or self.get(cx, cy) == TRANSPARENT:
                self.set(cx, cy, c)

    def outline_silhouette(self):
        """Final pass: make sure every figure pixel that touches transparency
        has an outline pixel (catches parts blitted with outline=False)."""
        src = [row[:] for row in self.px]
        for y in range(self.h):
            for x in range(self.w):
                if src[y][x] != TRANSPARENT:
                    continue
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.w and 0 <= ny < self.h:
                        n = src[ny][nx]
                        if n != TRANSPARENT and n != "o" and n not in NO_OUTLINE:
                            self.px[y][x] = "o"
                            break

    def to_part(self) -> Part:
        px = {}
        for y in range(self.h):
            for x in range(self.w):
                c = self.px[y][x]
                if c != TRANSPARENT:
                    px[(x, y)] = c
        return Part(px, (0, 0))

    def letters_used(self):
        s = set()
        for row in self.px:
            s.update(row)
        s.discard(TRANSPARENT)
        return s

    def text(self):
        return "\n".join("".join(r) for r in self.px)
