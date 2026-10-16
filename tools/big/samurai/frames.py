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
W, H, GROUND = 128, 128, 119           # the base box (Mike, Oct 16: try 128x128)
SCALE = 1.06                            # figure ~111 px

PAL = Palette(NAME, {
    "H": (184, 190, 210), "h": (184, 190, 210), "g": (112, 118, 146),   # white dropped to make room for the orange hair; H = h
    "S": (248, 200, 160), "s": (200, 140, 104), "z": (136, 86, 66),
    "C": (40, 40, 40), "c": (226, 70, 136), "k": (164, 34, 104),         # C = saya lacquer (shares the outline black); the gi: magenta lit / mid
    "P": (124, 72, 212),                                                  # Kenshin's violet eyes
    "I": (238, 238, 246), "i": (184, 190, 210), "n": (148, 148, 176),    # the hakama: white lit / mid (= steel light) / shadow
    "R": (200, 56, 64), "r": (120, 24, 40),          # obi; r doubles as the hair shadow
    "A": (255, 128, 64), "a": (222, 64, 30),          # Kenshin scarlet hair (anime): light, mid
    "L": (136, 86, 66), "l": (136, 86, 66),           # leather (hilt wrap, soles) shares the skin-dark brown
    "m": (184, 190, 210),
})


def stance(bob=0):
    f = Frame(DW, DH)
    b = bob
    # ---- hair tail, hanging down the back (behind everything)
    tail = Part("tail", [(96, 31 + b), (102, 30 + b), (105, 44 + b), (104, 60 + b), (102, 76 + b), (99, 86 + b), (97, 80 + b), (98, 64 + b), (97, 48 + b)], "a")
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
    neck = Part("neck", [(77, 30 + b), (87, 30 + b), (87, 37 + b), (85, 42 + b), (79, 41 + b), (77, 36 + b)], "s")
    neck.band([(77, 30 + b), (81, 30 + b), (80, 39 + b), (77, 36 + b)], "S")
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
    hand = Part("hand", [(58, 62 + b), (65, 60 + b), (68, 63 + b), (67, 68 + b), (62, 70 + b), (58, 68 + b), (57, 65 + b)], "s")
    hand.band([(59, 62 + b), (64, 61 + b), (64, 64 + b), (59, 64 + b)], "S")             # the back of the hand, lit
    for i, (x0, y0) in enumerate([(58, 65), (60, 66), (62, 67), (64, 67)]):              # fingers curling over the hilt
        hand.fold([(x0, y0 + b), (x0, y0 + 3 + b)], "z")
    hand.fold([(58, 68 + b), (66, 69 + b)], "z")                                          # the fingertips' edge
    hand.fold([(65, 60 + b), (68, 63 + b)], "z")                                          # the thumb
    # ---- head (Kenshin build): a short, soft face with big eyes and a small pointed chin; spiky long
    # bangs parting over the brow; two long side locks down past the jaw; the tail tied at the back of the head
    face = Part("face", [(73, 16 + b), (87, 16 + b), (91, 21 + b), (91, 27 + b), (87, 32 + b), (81, 35 + b), (75, 32 + b), (70, 27 + b), (70, 21 + b)], "S")
    face.band([(87, 16 + b), (91, 21 + b), (91, 27 + b), (87, 32 + b), (86, 24 + b)], "s")   # narrow far-cheek shadow
    face.fold([(75, 31 + b), (81, 34 + b), (87, 31 + b)], "z")                                 # small chin
    face.fold([(73, 20 + b), (77, 19 + b)], "z"); face.fold([(81, 19 + b), (85, 20 + b)], "z")   # brows
    face.fold([(73, 23 + b), (70, 27 + b), (73, 28 + b)], "z")                                # the nose: bridge down to a tip, back under
    face.fold([(77, 30 + b), (81, 30 + b)], "z")                                               # mouth
    hair = Part("hair", [(67, 14 + b), (72, 7 + b), (78, 4 + b), (84, 5 + b), (90, 4 + b), (96, 9 + b), (99, 16 + b), (100, 26 + b), (97, 35 + b), (93, 38 + b), (92, 26 + b),
                         (91, 18 + b), (89, 22 + b), (87, 15 + b), (85, 21 + b), (83, 15 + b), (81, 22 + b), (79, 15 + b), (77, 21 + b), (75, 15 + b), (73, 21 + b), (71, 16 + b), (70, 22 + b), (68, 19 + b)], "a")
    hair.band([(71, 12 + b), (77, 6 + b), (88, 6 + b), (93, 9 + b), (84, 11 + b), (75, 14 + b)], "A")
    hair.fold([(79, 15 + b), (79, 20 + b)], "A"); hair.fold([(87, 15 + b), (87, 20 + b)], "A")
    hair.band([(93, 10 + b), (98, 14 + b), (99, 24 + b), (97, 34 + b), (93, 38 + b), (92, 26 + b), (92, 16 + b)], "r")
    hair.fold([(85, 8 + b), (91, 13 + b), (94, 24 + b)], "r")
    hair.fold([(78, 10 + b), (76, 16 + b)], "A"); hair.fold([(82, 9 + b), (81, 16 + b)], "A")
    lock_near = Part("lock_near", [(70, 22 + b), (74, 22 + b), (75, 36 + b), (74, 48 + b), (71, 52 + b), (69, 44 + b), (69, 32 + b)], "a")
    lock_near.band([(70, 22 + b), (72, 22 + b), (72, 48 + b), (71, 52 + b), (69, 44 + b), (69, 32 + b)], "A")
    lock_far = Part("lock_far", [(88, 22 + b), (93, 22 + b), (94, 36 + b), (93, 50 + b), (90, 54 + b), (88, 46 + b), (87, 32 + b)], "a")
    lock_far.band([(91, 22 + b), (93, 22 + b), (94, 36 + b), (93, 50 + b), (90, 54 + b), (91, 40 + b)], "r")
    tie = Part("tie", [(95, 28 + b), (100, 27 + b), (101, 32 + b), (96, 33 + b)], "R")
    f.add(tail, far_sleeve, foot_near, foot_far, hak, torso, neck, obi, knot, saya, tsuba, hilt, sleeve, hand, face, hair, lock_near, lock_far, tie)
    f.scale(SCALE, 80, DGROUND + 1, W // 2, GROUND + 1)
    f.w, f.h = W, H
    g = f.raster()
    # eyes: placed in box pixels after scaling so both are exactly 2 px wide (Mike)
    ey = GROUND + 1 + int(round((22 + b - DGROUND - 1) * SCALE))
    ex = [W // 2 + int(round((dx - 80) * SCALE)) for dx in (73, 80)]
    # bigger anime eyes, 3x3 like the pixeljoint reference: a thin dark upper edge, a tall violet iris
    # with a light glint top-left and a dark pupil bottom-right
    for x in ex:
        g.g[ey - 1][x] = "o"; g.g[ey - 1][x + 1] = "o"; g.g[ey - 1][x + 2] = "o"
        g.g[ey][x] = "h"; g.g[ey][x + 1] = "P"; g.g[ey][x + 2] = "P"
        g.g[ey + 1][x] = "P"; g.g[ey + 1][x + 1] = "P"; g.g[ey + 1][x + 2] = "o"
    return g


def main():
    g = stance()
    n = PAL.check([g])
    im = render(g, PAL)
    strip([im], os.path.join(HERE, f"{NAME}_big.png"), zoom=4, labels=["stance"])
    print(f"{NAME} big: {n} colours")


if __name__ == "__main__":
    main()
