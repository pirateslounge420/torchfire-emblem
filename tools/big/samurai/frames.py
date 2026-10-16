"""Samurai at CPS2 scale (~105 px) — rest stance first, built from hand-placed shapes (bigkit).

Facing LEFT. Box 160x128, ground row 117, origin (80, 118).
Run: python3 tools/big/samurai/frames.py  -> samurai_big.png next to this file.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from bigkit import Part, Frame, Palette, render, strip  # noqa: E402

NAME = "samurai"
W, H = 160, 128
GROUND = 117

PAL = Palette(NAME, {
    "H": (248, 248, 248), "h": (184, 190, 210), "g": (112, 118, 146),
    "S": (248, 200, 160), "s": (200, 140, 104), "z": (136, 86, 66),
    "C": (112, 118, 146), "c": (60, 62, 88), "k": (30, 30, 46),
    "I": (150, 140, 255), "i": (88, 72, 200), "n": (46, 36, 120),
    "R": (200, 56, 64), "r": (120, 24, 40),
    "L": (72, 46, 28), "l": (72, 46, 28),
    "m": (184, 190, 210),
})


def stance(bob=0):
    f = Frame(W, H)
    b = bob
    # ---- hair tail, hanging down the back (behind everything)
    tail = Part("tail", [(96, 40 + b), (101, 38 + b), (104, 48 + b), (103, 62 + b), (101, 76 + b), (98, 84 + b), (96, 78 + b), (97, 64 + b), (97, 50 + b)], "h")
    tail.band([(99, 40 + b), (104, 48 + b), (103, 76 + b), (100, 84 + b), (100, 60 + b)], "g")
    tail.fold([(100, 44 + b), (101, 70 + b)], "H")
    # ---- far sleeve (behind the torso)
    far_sleeve = Part("far_sleeve", [(90, 38 + b), (100, 38 + b), (103, 56 + b), (100, 70 + b), (92, 70 + b), (88, 56 + b)], "k")
    # ---- hakama: one wide skirt, two legs under it
    hak = Part("hakama", [(66, 64), (92, 64), (96, 80), (100, 98), (104, 112), (83, 112), (81, 100), (79, 112), (56, 112), (58, 96), (62, 80)], "i")
    hak.band([(66, 64), (74, 64), (70, 80), (64, 98), (60, 112), (56, 112), (58, 96), (62, 80)], "I")
    hak.band([(88, 66), (92, 64), (96, 80), (100, 98), (104, 112), (94, 112), (92, 96), (90, 80)], "n")
    hak.band([(81, 84), (86, 84), (86, 112), (83, 112), (81, 100)], "n")     # the split between the legs
    hak.fold([(72, 66), (68, 90), (65, 112)], "n")
    hak.fold([(78, 66), (76, 90), (74, 112)], "n")
    hak.fold([(85, 66), (88, 84)], "n")
    hak.fold([(90, 70), (94, 92), (96, 112)], "k")
    # ---- feet (tabi + sandals), small
    foot_near = Part("foot_near", [(56, 112), (76, 112), (78, 116), (74, 118), (54, 118), (52, 115)], "L")
    foot_near.band([(56, 112), (76, 112), (76, 114), (56, 114)], "z")
    foot_far = Part("foot_far", [(84, 112), (104, 112), (106, 115), (103, 118), (84, 118), (83, 115)], "L")
    foot_far.band([(84, 112), (104, 112), (104, 114), (84, 114)], "z")
    # ---- torso: the gi, narrow, lit from the upper left
    torso = Part("torso", [(69, 36 + b), (95, 36 + b), (95, 50 + b), (93, 66 + b), (70, 66 + b), (68, 50 + b)], "k")
    torso.band([(69, 36 + b), (80, 36 + b), (77, 50 + b), (74, 66 + b), (70, 66 + b), (68, 50 + b)], "c")
    torso.fold([(84, 36 + b), (80, 46 + b), (77, 58 + b), (76, 66 + b)], "H")           # the lapel edge
    torso.fold([(78, 38 + b), (83, 48 + b), (84, 58 + b)], "c")                         # the far lapel, dim
    # ---- neck + chest skin in the V
    neck = Part("neck", [(79, 30 + b), (86, 30 + b), (86, 37 + b), (84, 42 + b), (80, 40 + b), (79, 36 + b)], "s")
    neck.band([(79, 30 + b), (82, 30 + b), (81, 38 + b), (79, 36 + b)], "S")
    # ---- obi
    obi = Part("obi", [(69, 59 + b), (93, 59 + b), (93, 66 + b), (69, 66 + b)], "r")
    obi.band([(69, 59 + b), (93, 59 + b), (93, 62 + b), (69, 62 + b)], "R")
    obi.fold([(80, 59 + b), (82, 66 + b)], "k")
    knot = Part("knot", [(93, 60 + b), (100, 58 + b), (104, 64 + b), (102, 72 + b), (97, 68 + b), (94, 66 + b)], "r")
    knot.band([(93, 60 + b), (98, 59 + b), (98, 64 + b), (94, 64 + b)], "R")
    # ---- saya (worn on the near hip, in front of the hakama) and the hilt
    saya = Part("saya", [(62, 66 + b), (66, 64 + b), (104, 86 + b), (104, 90 + b), (100, 91 + b), (60, 70 + b)], "k")
    saya.band([(63, 66 + b), (66, 64 + b), (104, 86 + b), (104, 88 + b)], "c")
    tsuba = Part("tsuba", [(60, 62 + b), (66, 60 + b), (68, 66 + b), (62, 70 + b)], "g")
    hilt = Part("hilt", [(40, 50 + b), (62, 62 + b), (60, 67 + b), (37, 55 + b)], "L")
    hilt.fold([(44, 52 + b), (46, 56 + b), (50, 55 + b), (52, 59 + b), (56, 58 + b), (58, 62 + b)], "k")
    # ---- near sleeve: long, thin, flaring to a point at the wrist
    sleeve = Part("sleeve", [(66, 37 + b), (76, 37 + b), (74, 50 + b), (72, 62 + b), (70, 72 + b), (60, 76 + b), (56, 70 + b), (62, 60 + b), (64, 48 + b)], "k")
    sleeve.band([(66, 37 + b), (71, 37 + b), (68, 50 + b), (65, 62 + b), (60, 72 + b), (56, 70 + b), (62, 60 + b), (64, 48 + b)], "c")
    sleeve.fold([(66, 37 + b), (68, 36 + b), (72, 36 + b)], "g")
    sleeve.fold([(70, 52 + b), (67, 64 + b), (63, 72 + b)], "k")
    # ---- near hand resting on the hilt
    hand = Part("hand", [(58, 62 + b), (66, 60 + b), (69, 64 + b), (67, 70 + b), (60, 70 + b), (57, 66 + b)], "s")
    hand.band([(58, 62 + b), (64, 61 + b), (63, 65 + b), (59, 65 + b)], "S")
    hand.fold([(60, 67 + b), (66, 67 + b)], "z")
    # ---- head: face, then hair over it
    face = Part("face", [(72, 16 + b), (86, 14 + b), (90, 22 + b), (89, 30 + b), (84, 34 + b), (77, 34 + b), (72, 28 + b), (70, 22 + b)], "S")
    face.band([(84, 14 + b), (90, 22 + b), (89, 30 + b), (84, 34 + b), (84, 24 + b)], "s")
    face.fold([(75, 30 + b), (80, 33 + b), (84, 32 + b)], "z")                            # jaw shadow
    face.dot(74, 24 + b, "k"); face.dot(75, 24 + b, "k")                                  # near eye (dot)
    face.dot(81, 24 + b, "k")                                                             # far eye
    face.fold([(73, 22 + b), (76, 21 + b)], "z"); face.fold([(80, 21 + b), (83, 21 + b)], "z")   # brows
    face.dot(71, 27 + b, "z")                                                             # nose tip
    face.fold([(74, 30 + b), (77, 30 + b)], "z")                                          # mouth
    hair = Part("hair", [(70, 12 + b), (78, 8 + b), (88, 8 + b), (96, 12 + b), (99, 22 + b), (98, 34 + b), (94, 40 + b), (92, 32 + b), (90, 22 + b),
                         (86, 16 + b), (82, 20 + b), (79, 15 + b), (76, 21 + b), (73, 17 + b), (70, 22 + b), (68, 18 + b)], "h")
    hair.band([(72, 12 + b), (78, 8 + b), (88, 8 + b), (90, 12 + b), (80, 12 + b), (74, 16 + b)], "H")
    hair.band([(92, 12 + b), (96, 12 + b), (99, 22 + b), (98, 34 + b), (94, 40 + b), (92, 32 + b), (91, 20 + b)], "g")
    hair.fold([(84, 9 + b), (90, 14 + b), (93, 24 + b)], "g")
    hair.fold([(76, 10 + b), (74, 16 + b)], "H")
    sidelock = Part("sidelock", [(88, 20 + b), (92, 20 + b), (93, 36 + b), (90, 42 + b), (88, 36 + b)], "h")
    sidelock.band([(90, 20 + b), (92, 20 + b), (93, 36 + b), (91, 40 + b)], "g")
    tie = Part("tie", [(95, 36 + b), (100, 35 + b), (101, 40 + b), (96, 41 + b)], "R")

    f.add(tail, far_sleeve, hak, foot_near, foot_far, torso, neck, obi, knot, saya, tsuba, hilt, sleeve, hand, face, hair, sidelock, tie)
    return f.raster()


def main():
    g = stance()
    n = PAL.check([g])
    im = render(g, PAL)
    strip([im], os.path.join(HERE, f"{NAME}_big.png"), zoom=4, labels=["stance"])
    print(f"{NAME} big: {n} colours")


if __name__ == "__main__":
    main()
