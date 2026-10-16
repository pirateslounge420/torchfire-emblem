"""Palettes: letter -> RGB(A). GBA sprites get 15 colours + transparent, so
each fighter's palette is checked against that budget at pack time."""
from __future__ import annotations
from PIL import Image

OUTLINE = (24, 20, 37)            # dark plum-navy, never pure black
GROUND_SHADOW = (0, 0, 0, 110)
WHITE = (255, 255, 255)
SKIN = {"S": (255, 226, 196), "s": (236, 184, 140), "z": (176, 110, 82)}
SKIN_TAN = {"S": (240, 204, 160), "s": (206, 150, 100), "z": (140, 86, 56)}
SKIN_DARK = {"S": (196, 150, 110), "s": (150, 102, 70), "z": (96, 60, 40)}
LEATHER = {"L": (176, 128, 84), "l": (124, 84, 52), "j": (76, 48, 30)}
STEEL = {"M": (236, 240, 248), "m": (168, 176, 196), "n": (96, 104, 132)}
SLASH = {"E": (255, 255, 255), "e": (168, 224, 255)}

# Trigram colours (locked, fighter-design-doc §3). Three tones each: hi / base / shadow.
TRIGRAM = {
    "heaven":   {"C": (214, 170, 255), "c": (150, 92, 220), "k": (82, 40, 140)},   # purple
    "thunder":  {"C": (170, 240, 255), "c": (70, 180, 230), "k": (28, 96, 160)},   # cyan, leaning blue
    "wind":     {"C": (190, 250, 220), "c": (100, 210, 160), "k": (36, 130, 100)},  # seafoam, leaning green
    "fire":     {"C": (255, 140, 120), "c": (218, 56, 56), "k": (130, 24, 40)},    # red
    "water":    {"C": (150, 160, 255), "c": (70, 80, 200), "k": (34, 36, 120)},    # indigo, on the blue side
    "earth":    {"C": (255, 240, 150), "c": (232, 196, 70), "k": (160, 120, 30)},  # yellow
    "mountain": {"C": (255, 196, 120), "c": (230, 128, 40), "k": (150, 68, 20)},   # orange
    "lake":     {"C": (240, 242, 250), "c": (190, 196, 212), "k": (110, 118, 140)},  # silver
}


class Palette:
    def __init__(self, name: str, letters: dict):
        self.name = name
        self.map = {"o": OUTLINE, "w": WHITE, "%": GROUND_SHADOW}
        self.map.update(SLASH)
        self.map.update(letters)

    def rgba(self, letter):
        c = self.map.get(letter)
        if c is None:
            raise KeyError(f"palette {self.name!r} has no colour for letter {letter!r}")
        return c if len(c) == 4 else (c[0], c[1], c[2], 255)

    def render(self, canvas) -> Image.Image:
        img = Image.new("RGBA", (canvas.w, canvas.h), (0, 0, 0, 0))
        px = img.load()
        for y in range(canvas.h):
            row = canvas.px[y]
            for x in range(canvas.w):
                c = row[x]
                if c != ".":
                    px[x, y] = self.rgba(c)
        return img

    def opaque_colours(self, letters=None):
        cols = set()
        for k, v in self.map.items():
            if letters is not None and k not in letters:
                continue
            if k == "%":
                continue
            cols.add(tuple(v[:3]))
        return cols


def check_palette(pal: Palette, letters_used: set, limit=15):
    cols = pal.opaque_colours(letters_used)
    if len(cols) > limit:
        raise ValueError(f"{pal.name}: {len(cols)} opaque colours used, GBA budget is {limit}: "
                         f"{sorted(letters_used)}")
    return len(cols)
