"""bigkit — CPS2-scale (~105 px) fighters drawn as hand-placed SHAPES.

At this size a letter grid is 10,000+ characters per frame, so each part is
instead a hand-authored outline polygon with hand-placed shading bands, and
the kit rasterises it with hard pixels, a 1-px outline and the fighter's
15-colour palette. The silhouette, the bands and the folds are all placed by
hand per part per beat — the kit only fills and outlines.

    part = Part("sleeve", [(x,y),...], "k")            # the silhouette, filled with a letter
    part.band([(x,y),...], "c")                         # a lit plane, clipped to the silhouette
    part.fold([(x,y),...], "n", width=1)                # a crease / pleat line
    frame = Frame(160, 128); frame.add(part) ...; grid = frame.raster()

Letters are the fighter's palette; 'o' is the outline; '.' transparent.
"""
from __future__ import annotations
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "hand"))
from handkit import Grid, Palette, render, strip, gif, sheet, OUTLINE, BG  # noqa: E402,F401


def _edges(pts):
    n = len(pts)
    return [(pts[i], pts[(i + 1) % n]) for i in range(n)]


def poly_mask(pts, w, h):
    """scanline fill with pixel centres (x+0.5, y+0.5)"""
    mask = [[False] * w for _ in range(h)]
    if len(pts) < 3:
        return mask
    ys = [p[1] for p in pts]
    for y in range(max(0, int(math.floor(min(ys)))), min(h, int(math.ceil(max(ys))) + 1)):
        cy = y + 0.5
        xs = []
        for (x0, y0), (x1, y1) in _edges(pts):
            if (y0 <= cy < y1) or (y1 <= cy < y0):
                xs.append(x0 + (cy - y0) * (x1 - x0) / (y1 - y0))
        xs.sort()
        for i in range(0, len(xs) - 1, 2):
            xa, xb = xs[i], xs[i + 1]
            for x in range(max(0, int(math.floor(xa + 0.5))), min(w, int(math.floor(xb + 0.5)))):
                mask[y][x] = True
    return mask


def line_pixels(pts, width=1):
    out = set()
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(1, int(max(abs(x1 - x0), abs(y1 - y0)) * 2))
        for i in range(n + 1):
            t = i / n
            x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            for dx in range(width):
                for dy in range(width):
                    out.add((int(math.floor(x)) + dx, int(math.floor(y)) + dy))
    return out


class Part:
    def __init__(self, name, outline_pts, fill, outline=True):
        self.name = name
        self.pts = outline_pts
        self.fill = fill
        self.bands = []     # (pts, letter)
        self.folds = []     # (pts, letter, width)
        self.dots = []      # (x, y, letter)
        self.outline = outline

    def band(self, pts, letter):
        self.bands.append((pts, letter)); return self

    def fold(self, pts, letter, width=1):
        self.folds.append((pts, letter, width)); return self

    def dot(self, x, y, letter):
        self.dots.append((x, y, letter)); return self

    def shifted(self, dx, dy):
        p = Part(self.name, [(x + dx, y + dy) for x, y in self.pts], self.fill, self.outline)
        p.bands = [([(x + dx, y + dy) for x, y in b], l) for b, l in self.bands]
        p.folds = [([(x + dx, y + dy) for x, y in f], l, w) for f, l, w in self.folds]
        p.dots = [(x + dx, y + dy, l) for x, y, l in self.dots]
        return p

    def scaled(self, s, ox, oy, nx, ny):
        """scale about (ox,oy) by s and move that point to (nx,ny)"""
        t = lambda p: (nx + (p[0] - ox) * s, ny + (p[1] - oy) * s)
        p = Part(self.name, [t(q) for q in self.pts], self.fill, self.outline)
        p.bands = [([t(q) for q in b], l) for b, l in self.bands]
        p.folds = [([t(q) for q in f], l, max(1, int(round(w * s)))) for f, l, w in self.folds]
        p.dots = [(int(round(t((x, y))[0])), int(round(t((x, y))[1])), l) for x, y, l in self.dots]
        return p

    def raster(self, w, h):
        """returns a dict {(x,y): letter} for this part alone, outlined"""
        mask = poly_mask(self.pts, w, h)
        px = {}
        for y in range(h):
            for x in range(w):
                if mask[y][x]:
                    px[(x, y)] = self.fill
        for pts, letter in self.bands:
            bm = poly_mask(pts, w, h)
            for (x, y) in list(px):
                if bm[y][x]:
                    px[(x, y)] = letter
        for pts, letter, width in self.folds:
            for (x, y) in line_pixels(pts, width):
                if (x, y) in px:
                    px[(x, y)] = letter
        for x, y, letter in self.dots:
            if (x, y) in px:
                px[(x, y)] = letter
        if self.outline:
            inner = set(px)
            edge = set()
            for (x, y) in inner:
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if (nx, ny) not in inner:
                        edge.add((x, y))
            for p in edge:
                px[p] = "o"
        return px


class Frame:
    def __init__(self, w=160, h=128):
        self.w, self.h = w, h
        self.parts = []

    def add(self, *parts):
        self.parts.extend(parts); return self

    def scale(self, s, ox, oy, nx, ny):
        self.parts = [p.scaled(s, ox, oy, nx, ny) for p in self.parts]; return self

    def raster(self):
        g = Grid(self.w, self.h)
        for part in self.parts:                       # back to front
            for (x, y), letter in part.raster(self.w, self.h).items():
                if 0 <= x < self.w and 0 <= y < self.h:
                    g.g[y][x] = letter
        return g
