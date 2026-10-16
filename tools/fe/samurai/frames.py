"""Samurai at GBA-native scale (35 px) — tools/fe. Letter grids, 15 colours, 64x64 box, ground row 53.
Run: python3 tools/fe/samurai/frames.py -> samurai_fe.png next to this file.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "hand"))
from handkit import Grid, Palette, render, strip  # noqa: E402

NAME = "samurai"
BOX, GROUND, X_OFF = 64, 53, 12
PAL = Palette(NAME, {
    "H": (236, 236, 246), "h": (184, 190, 210), "g": (148, 148, 176),   # hakama light / steel light / grey
    "S": (248, 200, 160), "s": (200, 140, 104), "z": (136, 86, 66),      # skin
    "c": (226, 70, 136), "k": (164, 34, 104), "q": (104, 18, 70),        # the gi, red-magenta
    "n": (148, 148, 176),                                                # hakama shadow (= g)
    "R": (200, 56, 64), "r": (120, 24, 40),                              # obi; r = hair shadow
    "A": (255, 128, 64), "a": (222, 64, 30),                             # scarlet hair
    "L": (96, 60, 36),                                                   # leather (soles, hilt wrap) — its own colour, per the FE rule
    "C": (40, 40, 40),                                                   # saya lacquer = outline black
})


def stance():
    return Grid.from_text(os.path.join(HERE, "stance.txt"), BOX, BOX, anchor_bottom=GROUND, x_off=X_OFF)


def main():
    g = stance()
    n = PAL.check([g])
    strip([render(g, PAL)], os.path.join(HERE, f"{NAME}_fe.png"), zoom=8, labels=["stance"])
    print(f"{NAME} fe: {n} colours")


if __name__ == "__main__":
    main()
