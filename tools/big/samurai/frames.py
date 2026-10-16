"""Samurai at CPS2 scale (~105 px) — rest stance first, built from hand-placed shapes (bigkit).

Facing LEFT. Drawn at ~105 px in a 160x128 design space, then scaled onto the
96x96 BASE BOX Mike chose (Oct 16): figure ~84 px, ground row 89, origin (48, 90).
Run: python3 tools/big/samurai/frames.py  -> samurai_big.png next to this file.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from bigkit import Part, Frame, Palette, render, strip  # noqa: E402

NAME = "samurai"
DW, DH, DGROUND = 160, 128, 117        # design space
W, H, GROUND = 96, 96, 89              # the base box
SCALE = 0.8

PAL = Palette(NAME, {
    "H": (184, 190, 210), "h": (184, 190, 210), "g": (112, 118, 146),   # white dropped to make room for the orange hair; H = h
    "S": (248, 200, 160), "s": (200, 140, 104), "z": (136, 86, 66),
    "C": (44, 40, 62), "c": (222, 72, 162), "k": (156, 34, 118),         # C = dark lacquer (saya); the gi: magenta lit / mid (Kenshin)
    "I": (238, 238, 246), "i": (184, 190, 210), "n": (148, 148, 176),    # the hakama: white lit / mid (= steel light) / shadow
    "R": (200, 56, 64), "r": (120, 24, 40),          # obi; r doubles as the hair shadow
    "A": (255, 150, 70), "a": (214, 88, 36),          # Kenshin-orange hair: light, mid
    "L": (136, 86, 66), "l": (136, 86, 66),           # leather (hilt wrap, soles) shares the skin-dark brown
    "m": (184, 190, 210),
})


def stance(bob=0):
    f = Frame(DW, DH)
    b = bob
    # ---- hair tail, hanging down the back (behind everything)
    tail = Part("tail", [(96, 40 + b), (101, 38 + b), (104, 48 + b), (103, 62 + b), (101, 76 + b), (98, 84 + b), (96, 78 + b), (97, 64 + b), (97, 50 + b)], "a")
    tail.band([(99, 40 + b), (104, 48 + b), (103, 76 + b), (100, 84 + b), (100, 60 + b)], "r")
    tail.fold([(100, 44 + b), (101, 70 + b)], "A")
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
    hak.fold([(90, 70), (94, 92), (96, 112)], "n")
    # ---- feet: small tabi on sandals, peeking out under the hem (hem overlaps their tops)
    foot_near = Part("foot_near", [(62, 111), (70, 111), (72, 114), (70, 118), (60, 118), (59, 114)], "h")
    foot_near.band([(59, 115), (72, 115), (70, 118), (60, 118)], "L")            # the sandal sole
    foot_near.fold([(64, 112), (64, 115)], "g")                                   # the tabi split
    foot_far = Part("foot_far", [(89, 111), (97, 111), (100, 114), (98, 118), (88, 118), (86, 114)], "h")
    foot_far.band([(86, 115), (100, 115), (98, 118), (88, 118)], "L")
    foot_far.band([(89, 111), (97, 111), (100, 114), (95, 114), (92, 112)], "g")
    # ---- torso: the gi, narrow, lit from the upper left
    torso = Part("torso", [(69, 36 + b), (95, 36 + b), (95, 50 + b), (93, 66 + b), (70, 66 + b), (68, 50 + b)], "k")
    torso.band([(69, 36 + b), (80, 36 + b), (77, 50 + b), (74, 66 + b), (70, 66 + b), (68, 50 + b)], "c")
    torso.fold([(84, 36 + b), (80, 46 + b), (77, 58 + b), (76, 66 + b)], "H")           # the lapel edge
    torso.fold([(78, 38 + b), (83, 48 + b), (84, 58 + b)], "c")                         # the far lapel, dim
    # ---- neck + chest skin in the V
    neck = Part("neck", [(76, 30 + b), (88, 30 + b), (88, 37 + b), (85, 42 + b), (79, 41 + b), (76, 36 + b)], "s")
    neck.band([(76, 30 + b), (81, 30 + b), (80, 39 + b), (76, 36 + b)], "S")
    # ---- obi
    obi = Part("obi", [(69, 59 + b), (93, 59 + b), (93, 66 + b), (69, 66 + b)], "r")
    obi.band([(69, 59 + b), (93, 59 + b), (93, 62 + b), (69, 62 + b)], "R")
    obi.fold([(80, 59 + b), (82, 66 + b)], "r")
    knot = Part("knot", [(93, 60 + b), (100, 58 + b), (104, 64 + b), (102, 72 + b), (97, 68 + b), (94, 66 + b)], "r")
    knot.band([(93, 60 + b), (98, 59 + b), (98, 64 + b), (94, 64 + b)], "R")
    # ---- saya (worn on the near hip, in front of the hakama) and the hilt
    saya = Part("saya", [(62, 66 + b), (66, 64 + b), (124, 94 + b), (124, 98 + b), (120, 99 + b), (60, 70 + b)], "C")
    saya.band([(63, 66 + b), (66, 64 + b), (124, 94 + b), (124, 96 + b)], "g")
    saya.fold([(121, 95 + b), (121, 99 + b)], "g")                                       # the kojiri cap
    tsuba = Part("tsuba", [(60, 62 + b), (66, 60 + b), (68, 66 + b), (62, 70 + b)], "g")
    hilt = Part("hilt", [(40, 50 + b), (62, 62 + b), (60, 67 + b), (37, 55 + b)], "L")
    hilt.fold([(44, 52 + b), (46, 56 + b), (50, 55 + b), (52, 59 + b), (56, 58 + b), (58, 62 + b)], "k")
    # ---- near sleeve: long, thin, flaring to a point at the wrist
    sleeve = Part("sleeve", [(66, 37 + b), (76, 37 + b), (74, 50 + b), (72, 62 + b), (70, 72 + b), (60, 76 + b), (56, 70 + b), (62, 60 + b), (64, 48 + b)], "k")
    sleeve.band([(66, 37 + b), (71, 37 + b), (68, 50 + b), (65, 62 + b), (60, 72 + b), (56, 70 + b), (62, 60 + b), (64, 48 + b)], "c")
    sleeve.fold([(66, 37 + b), (68, 36 + b), (72, 36 + b)], "g")
    sleeve.fold([(70, 52 + b), (67, 64 + b), (63, 72 + b)], "k")
    # ---- near hand resting on the hilt
    hand = Part("hand", [(56, 61 + b), (66, 59 + b), (70, 63 + b), (69, 70 + b), (62, 73 + b), (57, 70 + b), (55, 65 + b)], "s")
    hand.band([(57, 61 + b), (65, 60 + b), (65, 64 + b), (57, 64 + b)], "S")             # the back of the hand, lit
    for i, (x0, y0) in enumerate([(57, 65), (60, 66), (63, 67), (66, 68)]):              # four fingers curling over the hilt
        hand.fold([(x0, y0 + b), (x0 + 1, y0 + 4 + b)], "z")
    hand.fold([(57, 70 + b), (68, 72 + b)], "z")                                          # the fingertips' edge
    hand.fold([(66, 60 + b), (69, 63 + b)], "z")                                          # the thumb
    # ---- head: face, then hair over it
    face = Part("face", [(73, 15 + b), (87, 15 + b), (90, 21 + b), (90, 28 + b), (86, 34 + b), (79, 35 + b), (73, 31 + b), (70, 25 + b), (70, 20 + b)], "S")
    face.band([(85, 15 + b), (90, 21 + b), (90, 28 + b), (86, 34 + b), (84, 24 + b)], "s")
    face.fold([(75, 31 + b), (80, 34 + b), (86, 32 + b)], "z")                            # jaw shadow
    face.fold([(73, 22 + b), (76, 21 + b)], "z"); face.fold([(80, 21 + b), (83, 21 + b)], "z")   # brows
    face.dot(71, 27 + b, "z")                                                             # nose tip
    face.fold([(74, 30 + b), (77, 30 + b)], "z")                                          # mouth
    hair = Part("hair", [(70, 12 + b), (78, 8 + b), (88, 8 + b), (96, 12 + b), (99, 22 + b), (98, 34 + b), (94, 40 + b), (92, 32 + b), (90, 22 + b),
                         (86, 16 + b), (82, 20 + b), (79, 15 + b), (76, 21 + b), (73, 17 + b), (70, 22 + b), (68, 18 + b)], "a")
    hair.band([(72, 12 + b), (78, 8 + b), (88, 8 + b), (90, 12 + b), (80, 12 + b), (74, 16 + b)], "A")
    hair.band([(92, 12 + b), (96, 12 + b), (99, 22 + b), (98, 34 + b), (94, 40 + b), (92, 32 + b), (91, 20 + b)], "r")
    hair.fold([(84, 9 + b), (90, 14 + b), (93, 24 + b)], "r")
    hair.fold([(76, 10 + b), (74, 16 + b)], "A")
    sidelock = Part("sidelock", [(88, 20 + b), (92, 20 + b), (93, 36 + b), (90, 42 + b), (88, 36 + b)], "a")
    sidelock.band([(90, 20 + b), (92, 20 + b), (93, 36 + b), (91, 40 + b)], "r")
    tie = Part("tie", [(95, 36 + b), (100, 35 + b), (101, 40 + b), (96, 41 + b)], "R")

    f.add(tail, far_sleeve, foot_near, foot_far, hak, torso, neck, obi, knot, saya, tsuba, hilt, sleeve, hand, face, hair, sidelock, tie)
    f.scale(SCALE, 80, DGROUND + 1, 48, GROUND + 1)
    f.w, f.h = W, H
    g = f.raster()
    # eyes: placed in box pixels after scaling so both are exactly 2 px wide (Mike)
    ey = GROUND + 1 + int(round((24 + b - DGROUND - 1) * SCALE))
    for x in (43, 44, 49, 50):
        g.g[ey][x] = "o"
    return g


def main():
    g = stance()
    n = PAL.check([g])
    im = render(g, PAL)
    strip([im], os.path.join(HERE, f"{NAME}_big.png"), zoom=4, labels=["stance"])
    print(f"{NAME} big: {n} colours")


if __name__ == "__main__":
    main()
