"""Masked shadow-ninja, Street Fighter style, hand-pixelled (~58 px). 15 colours, 80x80 box, ground 73."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "hand"))
from handkit import Grid, Palette, render, strip  # noqa: E402

NAME = "ninja"
BOX, GROUND, X_OFF = 80, 73, 14
PAL = Palette(NAME, {
    "N": (88, 94, 150), "n": (44, 46, 86),                                # suit: lit / mid
    "V": (150, 200, 255), "Y": (255, 220, 90),                             # crest glow, eye glow
    "M": (210, 216, 232), "m": (130, 136, 168), "u": (78, 82, 110),        # steel light / mid / dark
    "S": (236, 190, 150), "s": (186, 130, 96), "z": (124, 78, 56),         # skin
    "R": (210, 60, 70), "r": (124, 26, 42),                                # sash
    "L": (96, 60, 36),                                                     # wraps
    "H": (240, 244, 250),                                                  # glint
})


def stance():
    return Grid.from_text(os.path.join(HERE, "stance.txt"), BOX, BOX, anchor_bottom=GROUND, x_off=X_OFF)


def main():
    g = stance()
    n = PAL.check([g])
    strip([render(g, PAL)], os.path.join(HERE, f"{NAME}_sf.png"), zoom=6, labels=["stance"])
    print(f"{NAME} sf: {n} colours")


if __name__ == "__main__":
    main()
