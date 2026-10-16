"""Samurai, big build — drawn FROM SCRATCH to GBA Fire Emblem proportions (Mike, Oct 16).

The FE skeleton, measured off the sheets and fe-battle-animations.neocities.org, for a
34-px man: head ~11 (a third), neck 1, torso 10 (short), legs 12, shoulders 13 wide, a
20-wide stance. Here every FE pixel is ~3 box pixels: a ~104-px figure in a 128x128 box,
ground row 119, origin (64, 120). Facing LEFT. Hand-placed shapes (bigkit), 15 colours.

Run: python3 tools/big/samurai/frames.py  -> samurai_big.png next to this file.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from bigkit import Part, Frame, Palette, render, strip  # noqa: E402

NAME = "samurai"
W, H, GROUND = 128, 128, 119

PAL = Palette(NAME, {
    "H": (236, 236, 246), "h": (184, 190, 210), "g": (148, 148, 176),   # hakama light / steel light / grey (= hakama shadow n)
    "S": (248, 200, 160), "s": (200, 140, 104), "z": (136, 86, 66),      # skin
    "c": (226, 70, 136), "k": (164, 34, 104), "q": (104, 18, 70),        # the gi: lit / mid / shadow (red-magenta)
    "n": (148, 148, 176),                                                # hakama shadow
    "R": (200, 56, 64), "r": (120, 24, 40),                              # obi; r doubles as hair shadow
    "A": (255, 128, 64), "a": (222, 64, 30),                             # scarlet hair: light, mid
    "P": (124, 72, 212),                                                 # violet eyes
    "L": (136, 86, 66), "l": (136, 86, 66),                              # leather shares skin-dark (sandal soles, hilt wrap)
    "C": (40, 40, 40),                                                   # saya lacquer shares the outline black
})

# landmarks (box pixels)
CX = 64            # body centre line
HAIR_TOP = 15
FACE_TOP, CHIN = 25, 47
SHOULDER = 50
OBI_TOP, WAIST = 66, 73
HEM = 115


def stance(bob=0):
    b = bob
    f = Frame(W, H)

    # ---- hair tail: from the tie at the back of the head, down the back to the obi
    tail = Part("tail", [(82, 36 + b), (90, 35 + b), (93, 48 + b), (92, 62 + b), (90, 74 + b), (86, 80 + b), (84, 72 + b), (85, 58 + b), (83, 46 + b)], "a")
    tail.band([(86, 36 + b), (90, 35 + b), (93, 48 + b), (92, 62 + b), (90, 74 + b), (89, 58 + b), (88, 46 + b)], "r")
    tail.fold([(87, 40 + b), (88, 60 + b)], "A")

    # ---- far sleeve (behind the torso): a big bell hanging from the far shoulder
    far_sleeve = Part("far_sleeve", [(76, 52 + b), (86, 52 + b), (92, 66 + b), (92, 82 + b), (80, 84 + b), (76, 70 + b)], "q")
    far_sleeve.band([(84, 52 + b), (86, 52 + b), (92, 66 + b), (92, 82 + b), (88, 82 + b), (88, 66 + b)], "k")

    # ---- feet: small tabi on sandal soles, under the hem
    foot_near = Part("foot_near", [(36, 112), (50, 112), (53, 116), (50, 119), (34, 119), (32, 116)], "h")
    foot_near.band([(32, 116), (53, 116), (50, 119), (34, 119)], "L")
    foot_near.fold([(42, 112), (42, 116)], "g")
    foot_far = Part("foot_far", [(80, 112), (94, 112), (97, 116), (95, 119), (79, 119), (77, 116)], "h")
    foot_far.band([(77, 116), (97, 116), (95, 119), (79, 119)], "L")
    foot_far.band([(80, 112), (94, 112), (97, 116), (90, 116), (84, 113)], "g")

    # ---- hakama: wide, short, one skirt split into two full legs; pleats as diagonals
    hak = Part("hakama", [(50, WAIST), (80, WAIST), (90, 86), (96, HEM), (70, HEM), (65, 100), (60, HEM), (34, HEM), (40, 86)], "h")
    hak.band([(50, WAIST), (62, WAIST), (56, 90), (48, HEM), (34, HEM), (40, 86)], "H")           # lit front leg
    hak.band([(76, WAIST), (80, WAIST), (90, 86), (96, HEM), (84, HEM), (82, 90)], "n")            # shadowed back leg
    hak.band([(62, 92), (68, 92), (70, HEM), (60, HEM), (65, 100)], "n")                          # the split
    hak.fold([(56, 74), (50, 94), (44, HEM)], "n"); hak.fold([(64, 74), (60, 94), (56, HEM)], "n")
    hak.fold([(72, 74), (74, 94), (76, HEM)], "n"); hak.fold([(80, 76), (86, 96), (90, HEM)], "g")
    hak.fold([(34, HEM), (96, HEM)], "n")

    # ---- torso: short and broad, the gi crossing left over right, lit from the camera side
    torso = Part("torso", [(46, SHOULDER + b), (82, SHOULDER + b), (82, 60 + b), (78, WAIST + b), (52, WAIST + b), (46, 60 + b)], "k")
    torso.band([(46, SHOULDER + b), (62, SHOULDER + b), (58, 60 + b), (56, WAIST + b), (52, WAIST + b), (46, 60 + b)], "c")
    torso.band([(76, SHOULDER + b), (82, SHOULDER + b), (82, 60 + b), (78, WAIST + b), (74, WAIST + b), (74, 60 + b)], "q")
    torso.fold([(70, SHOULDER + b), (64, 58 + b), (60, 66 + b), (59, WAIST + b)], "H")         # the lapel edge
    torso.fold([(62, SHOULDER + 1 + b), (67, 57 + b), (70, 63 + b)], "q")                      # the far lapel, dim
    neck = Part("neck", [(56, 44 + b), (70, 44 + b), (70, 52 + b), (66, 58 + b), (60, 57 + b), (56, 50 + b)], "s")
    neck.band([(56, 44 + b), (62, 44 + b), (61, 54 + b), (56, 50 + b)], "S")

    # ---- obi with a knot and tails at the back
    obi = Part("obi", [(50, OBI_TOP + b), (80, OBI_TOP + b), (79, WAIST + b), (51, WAIST + b)], "r")
    obi.band([(50, OBI_TOP + b), (80, OBI_TOP + b), (80, 69 + b), (50, 69 + b)], "R")
    obi.fold([(64, OBI_TOP + b), (66, WAIST + b)], "q")
    knot = Part("knot", [(79, 66 + b), (88, 64 + b), (92, 70 + b), (90, 80 + b), (84, 76 + b), (80, 72 + b)], "r")
    knot.band([(79, 66 + b), (86, 65 + b), (86, 70 + b), (80, 70 + b)], "R")

    # ---- the katana: a long saya worn on the near hip in front of the hakama; hilt forward-up
    saya = Part("saya", [(50, 72 + b), (55, 70 + b), (108, 102 + b), (108, 107 + b), (103, 108 + b), (47, 76 + b)], "C")
    saya.band([(51, 72 + b), (55, 70 + b), (108, 102 + b), (108, 104 + b)], "g")
    saya.fold([(105, 103 + b), (105, 108 + b)], "h")
    tsuba = Part("tsuba", [(47, 67 + b), (54, 65 + b), (56, 72 + b), (49, 75 + b)], "g")
    hilt = Part("hilt", [(26, 55 + b), (49, 68 + b), (46, 73 + b), (23, 60 + b)], "L")
    hilt.fold([(30, 57 + b), (32, 61 + b), (36, 60 + b), (38, 64 + b), (42, 63 + b), (44, 67 + b)], "C")

    # ---- near sleeve: FE-big, hanging from the near shoulder and belling out; the hand comes out at the hilt
    sleeve = Part("sleeve", [(42, SHOULDER + b), (58, SHOULDER + b), (56, 60 + b), (54, 70 + b), (52, 78 + b), (40, 82 + b), (34, 76 + b), (38, 64 + b), (40, 56 + b)], "k")
    sleeve.band([(42, SHOULDER + b), (50, SHOULDER + b), (47, 60 + b), (44, 70 + b), (40, 80 + b), (34, 76 + b), (38, 64 + b), (40, 56 + b)], "c")
    sleeve.band([(52, 62 + b), (54, 70 + b), (52, 78 + b), (46, 80 + b), (48, 70 + b)], "q")
    sleeve.fold([(48, 58 + b), (44, 70 + b), (40, 80 + b)], "q")
    hand = Part("hand", [(42, 64 + b), (52, 62 + b), (56, 66 + b), (54, 73 + b), (46, 76 + b), (41, 72 + b), (40, 67 + b)], "s")
    hand.band([(43, 64 + b), (51, 63 + b), (51, 67 + b), (43, 67 + b)], "S")
    for x0, y0 in [(42, 68), (45, 69), (48, 70), (51, 71)]:
        hand.fold([(x0, y0 + b), (x0, y0 + 4 + b)], "z")
    hand.fold([(42, 73 + b), (53, 75 + b)], "z"); hand.fold([(52, 62 + b), (56, 66 + b)], "z")

    # ---- head: FE-big, a third of the figure. Short soft face, pointed chin, big violet eyes
    face = Part("face", [(52, FACE_TOP + b), (72, FACE_TOP + b), (77, 32 + b), (77, 40 + b), (70, CHIN - 1 + b), (62, CHIN + 2 + b), (54, CHIN - 1 + b), (48, 40 + b), (48, 32 + b)], "S")
    face.band([(72, FACE_TOP + b), (77, 32 + b), (77, 40 + b), (70, CHIN - 1 + b), (69, 34 + b)], "s")
    face.fold([(54, 45 + b), (62, 48 + b), (70, 45 + b)], "z")                                 # jaw to a small chin
    face.fold([(52, 31 + b), (58, 30 + b)], "z"); face.fold([(63, 30 + b), (69, 31 + b)], "z")   # brows
    face.fold([(52, 34 + b), (48, 39 + b), (52, 40 + b)], "z")                                # nose: bridge, tip, under
    face.fold([(57, 43 + b), (63, 43 + b)], "z")                                               # mouth
    hair = Part("hair", [(44, 30 + b), (48, 20 + b), (54, 15 + b), (62, 13 + b), (72, 14 + b), (82, 18 + b), (87, 26 + b), (88, 38 + b), (84, 46 + b), (80, 36 + b),
                         (78, 28 + b), (76, 33 + b), (73, 25 + b), (70, 33 + b), (67, 25 + b), (64, 33 + b), (61, 25 + b), (58, 33 + b), (55, 26 + b), (52, 33 + b), (49, 27 + b), (46, 35 + b)], "a")
    hair.band([(50, 20 + b), (56, 15 + b), (70, 14 + b), (78, 17 + b), (66, 20 + b), (56, 24 + b)], "A")
    hair.band([(80, 18 + b), (87, 26 + b), (88, 38 + b), (84, 46 + b), (80, 36 + b), (79, 24 + b)], "r")
    hair.fold([(61, 25 + b), (61, 31 + b)], "A"); hair.fold([(73, 25 + b), (73, 31 + b)], "A")
    hair.fold([(72, 15 + b), (80, 22 + b), (83, 36 + b)], "r")
    lock_near = Part("lock_near", [(45, 32 + b), (51, 32 + b), (52, 50 + b), (50, 66 + b), (46, 72 + b), (43, 62 + b), (43, 46 + b)], "a")
    lock_near.band([(45, 32 + b), (48, 32 + b), (48, 66 + b), (46, 72 + b), (43, 62 + b), (43, 46 + b)], "A")
    lock_far = Part("lock_far", [(74, 34 + b), (80, 34 + b), (82, 50 + b), (81, 66 + b), (77, 74 + b), (74, 62 + b), (73, 48 + b)], "a")
    lock_far.band([(78, 34 + b), (80, 34 + b), (82, 50 + b), (81, 66 + b), (77, 74 + b), (78, 54 + b)], "r")
    tie = Part("tie", [(82, 32 + b), (89, 31 + b), (90, 37 + b), (83, 38 + b)], "R")

    f.add(tail, far_sleeve, foot_near, foot_far, hak, torso, neck, obi, knot, saya, tsuba, hilt, sleeve, hand, face, hair, lock_near, lock_far, tie)
    g = f.raster()
    # eyes 3x3: dark upper edge, tall violet iris with a light glint top-left and a dark pupil bottom-right
    for x in (52, 62):
        y = 33 + b
        for i in range(3):
            g.g[y][x + i] = "o"
        g.g[y + 1][x] = "h"; g.g[y + 1][x + 1] = "P"; g.g[y + 1][x + 2] = "P"
        g.g[y + 2][x] = "P"; g.g[y + 2][x + 1] = "P"; g.g[y + 2][x + 2] = "o"
    return g


def main():
    g = stance()
    n = PAL.check([g])
    im = render(g, PAL)
    strip([im], os.path.join(HERE, f"{NAME}_big.png"), zoom=4, labels=["stance"])
    print(f"{NAME} big: {n} colours")


if __name__ == "__main__":
    main()
