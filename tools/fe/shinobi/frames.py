"""Masked shadow-ninja at GBA-native scale — tools/fe. 15 colours, 64x64 box, ground row 53."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "hand"))
from handkit import Grid, Palette, render, strip  # noqa: E402

NAME = "shinobi"
BOX, GROUND, X_OFF = 64, 53, 4
PAL = Palette(NAME, {
    "N": (74, 78, 128), "n": (34, 36, 70),                               # the suit: lit / mid (near-black blue)
    "V": (150, 200, 255), "Y": (255, 220, 90),                            # the crest's cold glow, the eyes' hot glow
    "M": (200, 206, 224), "m": (122, 128, 160),                           # steel plate: light / mid
    "H": (236, 240, 248), "h": (170, 178, 200),                           # blade edge / blade body
    "S": (236, 190, 150), "s": (182, 126, 94), "z": (120, 76, 56),        # skin
    "L": (96, 60, 36), "l": (96, 60, 36),                                 # leather (boots)
    "R": (200, 56, 64),                                                   # a red accent (sash tie) — the Fire trigram if this is the Shinobi
    "r": (120, 24, 40),
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
