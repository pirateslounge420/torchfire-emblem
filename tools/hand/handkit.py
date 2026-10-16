"""handkit — helpers for HAND-PIXELLED GBA-style frames.

Every frame is a letter grid (one character per pixel) authored by hand in a
.txt file or built in code from a body grid plus hand-drawn overlays. There is
no rig and no procedural shading here: the point is that every pixel is placed
on purpose, the way the GBA Fire Emblem sheets are.

    from handkit import Grid, Palette, render, strip, gif, sheet

Grid letters are per character (see each fighter's frames.py); '.' is
transparent and 'o' is the outline (40,40,40), shared by everyone.
"""
from __future__ import annotations
import json
import os
from PIL import Image, ImageDraw

OUTLINE = (40, 40, 40)
BG = (52, 48, 66)


class Palette:
    """letter -> RGB. At most 15 opaque colours (GBA: 16 entries incl. transparent).
    Several letters may share one RGB; only unique RGBs count."""

    def __init__(self, name, letters):
        self.name = name
        self.map = {"o": OUTLINE}
        self.map.update(letters)

    def unique(self):
        return set(self.map.values())

    def check(self, grids=None):
        used = set(self.map.values()) if grids is None else {self.map[c] for g in grids for r in g.g for c in r if c in self.map}
        if len(used) > 15:
            raise ValueError(f"{self.name}: {len(used)} opaque colours, the budget is 15")
        return len(used)


class Grid:
    """A W×H character grid with the editing helpers used to build frames."""

    def __init__(self, w=64, h=64, fill="."):
        self.w, self.h = w, h
        self.g = [[fill] * w for _ in range(h)]

    @classmethod
    def from_text(cls, text_or_path, w=None, h=None, anchor_bottom=None, x_off=0):
        """Load a .txt grid ('#' lines are comments). With w/h, place it in a
        box: anchor_bottom = the row the grid's last line should sit on."""
        if os.path.exists(text_or_path):
            lines = [ln.rstrip("\n") for ln in open(text_or_path) if not ln.startswith("#")]
        else:
            lines = text_or_path.split("\n")
        lines = [ln for ln in lines if ln.strip() != ""]
        gw = max(len(ln) for ln in lines)
        gh = len(lines)
        if w is None:
            w, h = gw, gh
        grid = cls(w, h)
        oy = 0 if anchor_bottom is None else anchor_bottom - gh + 1
        for y, ln in enumerate(lines):
            for x, ch in enumerate(ln):
                if ch != "." and 0 <= x + x_off < w and 0 <= y + oy < h:
                    grid.g[y + oy][x + x_off] = ch
        return grid

    def copy(self):
        n = Grid(self.w, self.h)
        n.g = [row[:] for row in self.g]
        return n

    def put(self, y, x, text):
        """Write a string at (x, y); '?' leaves the pixel alone."""
        for i, ch in enumerate(text):
            if ch == "?":
                continue
            if 0 <= y < self.h and 0 <= x + i < self.w:
                self.g[y][x + i] = ch
        return self

    def put_block(self, y, x, text):
        """Write a multi-line block (first line at row y)."""
        for j, ln in enumerate(text.strip("\n").split("\n")):
            self.put(y + j, x, ln)
        return self

    def clear(self, x0, y0, x1, y1):
        for y in range(max(0, y0), min(self.h, y1)):
            for x in range(max(0, x0), min(self.w, x1)):
                self.g[y][x] = "."
        return self

    def shift(self, dx, dy):
        n = Grid(self.w, self.h)
        for y in range(self.h):
            for x in range(self.w):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.w and 0 <= ny < self.h:
                    n.g[ny][nx] = self.g[y][x]
        return n

    def shift_region(self, x0, y0, x1, y1, dx, dy):
        """Move a rectangle of pixels (used to lean a head or slide a foot)."""
        buf = {}
        for y in range(y0, y1):
            for x in range(x0, x1):
                if 0 <= y < self.h and 0 <= x < self.w and self.g[y][x] != ".":
                    buf[(x, y)] = self.g[y][x]
                    self.g[y][x] = "."
        for (x, y), c in buf.items():
            if 0 <= y + dy < self.h and 0 <= x + dx < self.w:
                self.g[y + dy][x + dx] = c
        return self

    def flip(self):
        n = Grid(self.w, self.h)
        for y in range(self.h):
            n.g[y] = self.g[y][::-1]
        return n

    def tidy(self):
        """Drop outline pixels that no longer touch any fill (after edits)."""
        changed = True
        while changed:
            changed = False
            for y in range(self.h):
                for x in range(self.w):
                    if self.g[y][x] == "o":
                        ok = False
                        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < self.w and 0 <= ny < self.h and self.g[ny][nx] not in "o.":
                                ok = True
                        if not ok:
                            self.g[y][x] = "."
                            changed = True
        return self

    def outline_missing(self, skip=""):
        """Add an 'o' wherever a fill pixel touches transparency (final pass).
        Letters in `skip` (smears, effects) never get outlined."""
        add = []
        for y in range(self.h):
            for x in range(self.w):
                if self.g[y][x] in ".o" or self.g[y][x] in skip:
                    continue
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.w and 0 <= ny < self.h and self.g[ny][nx] == ".":
                        add.append((nx, ny))
        for x, y in add:
            self.g[y][x] = "o"
        return self

    def text(self):
        return "\n".join("".join(r) for r in self.g)

    def letters(self):
        return {c for r in self.g for c in r if c != "."}


def render(grid: Grid, pal: Palette) -> Image.Image:
    img = Image.new("RGBA", (grid.w, grid.h), (0, 0, 0, 0))
    px = img.load()
    for y in range(grid.h):
        for x in range(grid.w):
            c = grid.g[y][x]
            if c in pal.map:
                px[x, y] = (*pal.map[c], 255)
            elif c != ".":
                raise KeyError(f"{pal.name}: letter {c!r} at ({x},{y}) has no colour")
    return img


def _bg(img, zoom, bg=BG):
    b = Image.new("RGBA", img.size, (*bg, 255))
    b.alpha_composite(img)
    return b.resize((img.width * zoom, img.height * zoom), Image.NEAREST)


def strip(images, path, zoom=5, labels=None, bg=BG):
    w, h = images[0].size
    out = Image.new("RGB", (len(images) * (w * zoom + 6), h * zoom + (14 if labels else 0)), (30, 28, 40))
    d = ImageDraw.Draw(out)
    for i, im in enumerate(images):
        x = i * (w * zoom + 6)
        if labels:
            d.text((x + 2, 1), labels[i], fill=(230, 230, 240))
        out.paste(_bg(im, zoom, bg), (x, 14 if labels else 0))
    out.save(path)
    return out


def gif(images, path, durations_ms, zoom=4, bg=BG):
    frames = [_bg(im, zoom, bg).convert("P", palette=Image.ADAPTIVE, colors=48) for im in images]
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=list(durations_ms), loop=0)


def sheet(anims, out_dir, name, box, origin, columns=16):
    """Pack {anim_name: (frames, fps, loop)} into the Godot sheet + JSON."""
    os.makedirs(out_dir, exist_ok=True)
    total = sum(len(f) for f, _, _ in anims.values())
    rows = (total + columns - 1) // columns
    sh = Image.new("RGBA", (columns * box, rows * box), (0, 0, 0, 0))
    meta = {"frame_size": box, "frame_w": box, "frame_h": box, "columns": columns, "faces": "left",
            "origin": list(origin), "animations": {}}
    i = 0
    for an, (frames, fps, loop) in anims.items():
        meta["animations"][an] = {"start": i, "count": len(frames), "loop": loop, "fps": fps}
        for fr in frames:
            sh.paste(fr, ((i % columns) * box, (i // columns) * box))
            i += 1
    sh.save(os.path.join(out_dir, f"{name}_sheet.png"))
    with open(os.path.join(out_dir, f"{name}_frames.json"), "w") as f:
        json.dump(meta, f, indent=2)
    return sh, meta
