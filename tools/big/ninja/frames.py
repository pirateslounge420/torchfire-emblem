"""Masked shadow-ninja (original, after Mike's concept) in STREET FIGHTER style: ~62 px, 16-bit fighting-game
proportions (head ~1/6, broad shoulders, long legs), SF idle stance — fists up, knees bent, 3/4 to the camera.
Box 80x80, ground row 73, origin (40, 74). Hand-placed shapes (bigkit), 15 colours.
Run: python3 tools/big/ninja/frames.py -> ninja_big.png
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from bigkit import Part, Frame, Palette, render, strip  # noqa: E402

NAME = "ninja"
W, H, GROUND = 80, 80, 73
PAL = Palette(NAME, {
    "N": (88, 94, 150), "n": (44, 46, 86), "d": (26, 26, 52),              # the suit: lit / mid / shadow (blue-black)
    "V": (150, 200, 255), "Y": (255, 220, 90),                              # crest glow, eye glow
    "M": (210, 216, 232), "m": (130, 136, 168), "u": (78, 82, 110),         # steel: light / mid / dark
    "S": (236, 190, 150), "s": (186, 130, 96), "z": (124, 78, 56),          # skin
    "R": (210, 60, 70), "r": (124, 26, 42),                                 # the sash
    "L": (96, 60, 36),                                                      # leather wraps
    "H": (210, 216, 232),                                                   # glint shares steel light
})


def stance():
    f = Frame(W, H)
    # ---- legs: SF ready stance — near leg forward and bent, far leg back, baggy trousers tucked into wraps
    leg_far = Part("leg_far", [(46, 44), (60, 44), (66, 58), (64, 66), (56, 68), (50, 60), (46, 52)], "n")
    leg_far.band([(56, 44), (60, 44), (66, 58), (64, 66), (60, 66), (58, 56)], "d")
    leg_far.fold([(52, 46), (56, 58), (58, 66)], "d")
    wrap_far = Part("wrap_far", [(56, 64), (66, 64), (66, 70), (56, 70)], "L")
    foot_far = Part("foot_far", [(54, 70), (70, 70), (72, 73), (54, 73)], "s")
    foot_far.band([(54, 70), (62, 70), (62, 73), (54, 73)], "z")
    leg_near = Part("leg_near", [(26, 44), (46, 44), (44, 54), (38, 62), (28, 68), (18, 66), (16, 58), (22, 48)], "n")
    leg_near.band([(26, 44), (36, 44), (32, 54), (26, 64), (18, 66), (16, 58), (22, 48)], "N")
    leg_near.fold([(36, 46), (34, 56), (28, 64)], "d")
    wrap_near = Part("wrap_near", [(14, 62), (28, 64), (26, 70), (12, 68)], "L")
    foot_near = Part("foot_near", [(8, 68), (26, 70), (26, 73), (6, 73), (4, 70)], "s")
    foot_near.band([(16, 70), (26, 70), (26, 73), (16, 73)], "z")
    # ---- torso: broad V, suit with a pale armour vest front, red sash
    torso = Part("torso", [(24, 20), (60, 20), (58, 34), (54, 46), (30, 46), (26, 34)], "n")
    torso.band([(24, 20), (40, 20), (38, 34), (34, 46), (30, 46), (26, 34)], "N")
    torso.band([(52, 20), (60, 20), (58, 34), (54, 46), (50, 46), (50, 32)], "d")
    torso.fold([(34, 22), (42, 30), (46, 40)], "d"); torso.fold([(50, 22), (44, 30)], "M")      # the V collar line
    sash = Part("sash", [(29, 40), (55, 40), (54, 46), (30, 46)], "r")
    sash.band([(29, 40), (55, 40), (55, 42), (29, 42)], "R")
    sash_tail = Part("sash_tail", [(28, 44), (33, 44), (30, 58), (24, 62), (24, 54)], "r")
    sash_tail.band([(28, 44), (31, 44), (28, 54), (25, 58), (24, 54)], "R")
    # ---- far arm: back, fist near the far hip (guard)
    arm_far = Part("arm_far", [(56, 24), (64, 26), (68, 36), (66, 44), (60, 44), (58, 36), (54, 30)], "s")
    arm_far.band([(60, 26), (64, 26), (68, 36), (66, 44), (64, 44), (62, 34)], "z")
    pauldron_far = Part("pauldron_far", [(52, 18), (66, 18), (70, 26), (66, 30), (54, 28)], "m")
    pauldron_far.band([(52, 18), (60, 18), (58, 24), (54, 28)], "M"); pauldron_far.band([(64, 20), (70, 26), (66, 30), (62, 26)], "u")
    fist_far = Part("fist_far", [(58, 42), (68, 42), (70, 48), (66, 52), (58, 50), (56, 46)], "s")
    fist_far.band([(58, 42), (64, 42), (63, 46), (58, 46)], "S"); fist_far.fold([(58, 48), (66, 49)], "z")
    # ---- near arm: raised guard, fist up at chin height, bare and muscular
    arm_near = Part("arm_near", [(22, 22), (32, 24), (34, 36), (24, 42), (14, 40), (12, 32), (16, 26)], "s")
    arm_near.band([(22, 22), (30, 24), (28, 32), (18, 36), (14, 34), (16, 26)], "S")
    arm_near.band([(30, 26), (34, 36), (24, 42), (22, 38), (30, 32)], "z")
    bracer = Part("bracer", [(10, 30), (20, 26), (24, 32), (16, 40), (8, 38)], "m")
    bracer.band([(10, 30), (18, 27), (18, 32), (10, 34)], "M"); bracer.band([(20, 34), (24, 32), (16, 40), (12, 40)], "u")
    pauldron_near = Part("pauldron_near", [(16, 16), (34, 16), (36, 24), (30, 28), (18, 26), (14, 20)], "m")
    pauldron_near.band([(16, 16), (28, 16), (26, 22), (18, 24), (14, 20)], "M"); pauldron_near.band([(32, 18), (36, 24), (30, 28), (28, 24)], "u")
    for sx in (18, 24, 30):
        pauldron_near.fold([(sx, 16), (sx + 1, 13)], "M")                                   # spikes
    fist_near = Part("fist_near", [(6, 20), (18, 18), (22, 24), (18, 32), (8, 32), (4, 26)], "s")
    fist_near.band([(6, 20), (16, 19), (15, 24), (7, 24)], "S"); fist_near.fold([(7, 27), (17, 28)], "z")
    # ---- head: hooded, masked; glowing eyes under the brow; a short fin crest
    neck = Part("neck", [(38, 16), (48, 16), (48, 22), (38, 22)], "s")
    head = Part("head", [(34, 4), (50, 4), (54, 10), (54, 18), (48, 22), (38, 22), (32, 18), (31, 10)], "n")
    head.band([(34, 4), (44, 4), (42, 12), (36, 20), (32, 18), (31, 10)], "N")
    head.band([(50, 6), (54, 10), (54, 18), (48, 22), (46, 14)], "d")
    head.fold([(33, 12), (52, 12)], "d")                                                   # the brow / mask line
    head.dot(36, 13, "Y"); head.dot(37, 13, "Y"); head.dot(43, 13, "Y"); head.dot(44, 13, "Y")   # glowing eyes, 2 px each
    crest = Part("crest", [(42, 4), (48, 0), (54, 2), (52, 6), (46, 7)], "V")
    crest.band([(42, 4), (48, 0), (47, 4)], "H")
    f.add(leg_far, wrap_far, foot_far, arm_far, fist_far, pauldron_far, torso, sash, sash_tail, leg_near, wrap_near, foot_near,
          neck, head, crest, arm_near, bracer, pauldron_near, fist_near)
    return f.raster()


def main():
    g = stance()
    n = PAL.check([g])
    strip([render(g, PAL)], os.path.join(HERE, f"{NAME}_big.png"), zoom=6, labels=["stance"])
    print(f"{NAME} big: {n} colours")


if __name__ == "__main__":
    main()
