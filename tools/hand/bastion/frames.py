"""Bastion (Mountain / orange) — hand-pixelled frames.

Three hand-drawn bodies (body.txt planted stance, body_back.txt crouched and
leaning away with both gauntlets raised behind the helm, body_lunge.txt folded
into a two-handed ground smash) plus hand-placed overlays for the arms, the
two-handed mace, the smear and the impact dust. The attack follows the six
beats of the GBA General / Hawkeye sheets: stance → mace hauled back-low →
raised behind the helm (two hands) → one big smear → ground smash → haul up.

Run:  python3 tools/hand/bastion/frames.py
  -> bastion_attack.png / .gif next to this file, Godot sheet in godot/art/bastion_v2/
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from handkit import Grid, Palette, render, strip, gif, sheet  # noqa: E402

NAME = "bastion"
BOX = 64
GROUND = 53          # row the feet stand on
BODY_H = 44          # rows in each body .txt (feet on the last row)
X_OFF = 12           # body grid column 0 -> box column
ORIGIN = (34, 54)

# 13 opaque colours. G doubles as the plate edge, the smear fringe and the dust; H is the brightest edge.
PAL = Palette(NAME, {
    "O": (255, 168, 56), "p": (216, 104, 24), "q": (140, 52, 16),      # orange enamel ramp
    "V": (255, 232, 120),                                               # visor glow (the accent)
    "K": (48, 50, 66), "k": (98, 102, 124), "G": (176, 180, 200),       # plate: near-black, dark grey, light edge
    "H": (248, 248, 248), "h": (176, 180, 200),                         # white edge / smear core, smear fringe
    "C": (104, 64, 88), "c": (56, 32, 48),                              # dark cloth
    "L": (120, 80, 44), "l": (72, 46, 26),                              # leather grip
})


def body(pose="body", dx=0, dy=0):
    return Grid.from_text(os.path.join(HERE, f"{pose}.txt"), BOX, BOX, anchor_bottom=GROUND + dy, x_off=X_OFF + dx)


def P(g, y, x, text, dx=0, dy=0):
    """overlay in body-grid coordinates (row 0 = top of the 44-row body); dx/dy follow a shifted body"""
    g.put(y + (GROUND - (BODY_H - 1)) + dy, x + X_OFF + dx, text)


def B(g, y, x, block, dx=0, dy=0):
    """multi-line overlay in body coords; '?' leaves the pixel alone"""
    for j, ln in enumerate(block.strip("\n").split("\n")):
        P(g, y + j, x, ln, dx, dy)


def under(g, draw):
    """run draw(u) on an empty grid, then lay the body g over it (for a weapon behind the body)"""
    u = Grid(BOX, BOX)
    draw(u)
    for y in range(BOX):
        for x in range(BOX):
            if g.g[y][x] != ".":
                u.g[y][x] = g.g[y][x]
    return u


def haft(g, x0, y0, x1, y1, grip=(), dx=0, dy=0):
    """2-px steel haft from (x0,y0) to (x1,y1) in body coords, outlined; rows in `grip` get leather."""
    n = max(abs(x1 - x0), abs(y1 - y0))
    steep = abs(y1 - y0) >= abs(x1 - x0)
    for i in range(n + 1):
        x = round(x0 + (x1 - x0) * i / n)
        y = round(y0 + (y1 - y0) * i / n)
        a, b = ("L", "l") if y in grip else ("G", "k")
        if steep:
            P(g, y, x - 1, "o" + a + b + "o", dx, dy)
        else:
            P(g, y - 1, x, "o", dx, dy); P(g, y, x, a, dx, dy); P(g, y + 1, x, b, dx, dy); P(g, y + 2, x, "o", dx, dy)


MACE_HEAD = """
??ooo??
?oHkKo?
oGGkKKo
oGkKkKo
oGGkKKo
?oGkKo?
??ooo??
"""


def mace_head(g, y, x, dx=0, dy=0):
    """7x7 flanged head, top-left corner at body (x, y)"""
    B(g, y, x, MACE_HEAD, dx, dy)


# arm overlays for the stance body (its own arms are not in body.txt), body coords ------------------
NEAR_ARM_STANCE = """
oKKo
oGKKo
oGkKo
oGkKo
?oKKo
?oGGkKo
?oGkKKo
?opqqKo
??ooooo
"""
FAR_ARM_STANCE = """
oKKo
?oKkKo
??oKkKKo
???oGGkKo
???opqqKo
????ooooo
"""
NEAR_ARM_BACK = """
oKKo
oGKKo
oGkKo
?oKKKo
?oGGkKo
?oGkKKo
?opqqKo
??ooooo
"""
FAR_GAUNTLET = """
?oooo?
oGGkKo
oGkKKo
opqqKo
?oooo?
"""
NEAR_ARM_LIFT = """
oKKo
oGKKo
oGkKo
oGGkKo
oGkKKo
opqqKo
?oooo?
"""


# --- frames -------------------------------------------------------------------
def stance(bob=0):
    """beat 1: planted, mace head resting on the ground in front, both gauntlets on the haft"""
    g = body()
    if bob:
        g.shift_region(0, 0, BOX, GROUND - 14, 0, bob)       # plate barely moves: helm/torso only
    haft(g, -2, 36, 15, 24, grip=range(23, 31), dy=bob)
    mace_head(g, 37, -6)
    P(g, 23, 15, "oKo", dy=bob); P(g, 24, 15, "oKKo", dy=bob)        # pommel knob
    B(g, 21, 12, FAR_ARM_STANCE, dy=bob)
    B(g, 20, 4, NEAR_ARM_STANCE, dy=bob)
    return g.tidy()


def mace_back():
    """beat 2: mace hauled off the ground and back-low across the legs, both gauntlets at the near hip"""
    g = body(dx=1)
    haft(g, 5, 21, 27, 33, grip=range(22, 29), dx=1)
    mace_head(g, 31, 26, dx=1)
    P(g, 20, 4, "oKo", dx=1); P(g, 21, 3, "oKo", dx=1)                 # pommel knob
    B(g, 25, 12, FAR_GAUNTLET, dx=1)
    B(g, 18, 4, NEAR_ARM_BACK, dx=1)
    return g.tidy()


def raised(tremble=0):
    """beat 3: crouched, leaning away, mace cocked up and back behind the helm in both gauntlets"""
    dx = -6
    g = body("body_back", dx=dx, dy=tremble)

    def weapon(u):
        haft(u, 24, 8, 46, -3, grip=range(3, 8), dx=dx, dy=tremble)
        mace_head(u, -8, 46, dx=dx, dy=tremble)
        P(u, 8, 22, "oKo", dx=dx, dy=tremble); P(u, 9, 22, "oKo", dx=dx, dy=tremble)   # pommel knob
    return under(g, weapon).tidy()


SMEAR = [
    (-9, 44, "hhHHHh"), (-8, 38, "hhHHHHHHHhh"), (-7, 32, "hhHHHHHHHHHHHHHhh"), (-6, 26, "hhHHHHHHHHHHHHHHHHHHhh"),
    (-5, 20, "hhHHHHHHHHHHHHHHHHHHHHHHHhh"), (-4, 14, "hhHHHHHHHHHHHHHHHHHHHHHHHHHHhhh"),
    (-3, 9, "hhHHHHHHHHHHHHHHHHHHHHHHHHHHHhhhh"), (-2, 5, "hhHHHHHHHHHHHHHHHHHHHHHHHHhhhhhhh"),
    (-1, 2, "hhHHHHHHHHHHHHHHHHHHHHhhhhhhhhh"), (0, 0, "hhHHHHHHHHHHHHHHHhhhhhhhhhh"),
    (1, -1, "hhHHHHHHHHHHHhhhhhhhhhh"), (2, -2, "hhHHHHHHHHhhhhhhhhh"), (3, -3, "hhHHHHHHhhhhhhh"),
    (4, -3, "hhHHHhhhhhh"), (5, -3, "hhHhhhhhh"), (6, -3, "hhhhhhh"), (7, -2, "hhhhh"), (8, -1, "hhh"),
    (9, 0, "hh"), (10, 1, "h"),
]


def smear():
    """beat 4: the whole mace becomes one pale wedge arcing over the helm toward the foe"""
    g = body("body_back", dx=-6, dy=1)
    for y, x, t in SMEAR:
        P(g, y, x - 6, t, dx=0, dy=1)
    return g.tidy()


DUST = [(40, -8, "Gh"), (38, -7, "H"), (41, 3, "hG"), (39, 2, "H"), (36, -3, "H"), (42, -9, "h"), (42, 5, "h")]


def impact():
    """beat 5: crouched two-handed ground smash, head buried low in front, dust at the strike"""
    dx = -2
    g = body("body_lunge", dx=dx)

    def weapon(u):
        haft(u, 17, 21, -2, 36, grip=range(22, 30), dx=dx)
        mace_head(u, 37, -5, dx=dx)
        P(u, 20, 17, "oKo", dx=dx); P(u, 19, 18, "oKo", dx=dx)       # pommel knob
    g = under(g, weapon)
    for y, x, t in DUST:
        P(g, y, x, t, dx=dx)
    return g.tidy()


def haul():
    """beat 6: straightening up, the mace hauled back up to waist height in front"""
    g = body()
    haft(g, 14, 21, -5, 29, grip=range(21, 27))
    mace_head(g, 26, -10)
    P(g, 20, 14, "oKo"); P(g, 21, 15, "oKo")                         # pommel knob
    B(g, 21, 8, FAR_GAUNTLET)
    P(g, 21, 13, "KKo"); P(g, 22, 13, "kKo"); P(g, 23, 13, "ooo")     # far forearm stub from the chest
    B(g, 21, 3, NEAR_ARM_LIFT)
    return g.tidy()


def animations():
    return {
        "idle": ([stance(0), stance(1), stance(1), stance(0)], 5, True),
        "lean": ([mace_back(), raised(), raised()], 10, False),
        "hold": ([raised(), raised(-1)], 5, True),
        "lunge": ([smear(), impact(), impact()], 20, False),
        "recover": ([haul(), stance(0), stance(0)], 9, False),
    }


def main():
    anims = animations()
    n = PAL.check([g for frames, _, _ in anims.values() for g in frames])
    imgs = {k: ([render(g, PAL) for g in frames], fps, loop) for k, (frames, fps, loop) in anims.items()}
    beats = [imgs["idle"][0][0], imgs["lean"][0][0], imgs["lean"][0][1], imgs["lunge"][0][0], imgs["lunge"][0][1], imgs["recover"][0][0]]
    strip(beats, os.path.join(HERE, f"{NAME}_attack.png"), zoom=5,
          labels=["stance", "mace back-low", "raised, two hands", "smear", "ground smash", "haul up"])
    gif(beats + [imgs["idle"][0][0]], os.path.join(HERE, f"{NAME}_attack.gif"), [500, 160, 260, 70, 360, 200, 500])
    out_dir = os.path.join(HERE, "..", "..", "..", "godot", "art", f"{NAME}_v2")
    sheet(imgs, out_dir, NAME, BOX, ORIGIN)
    print(f"{NAME}: {sum(len(f) for f, _, _ in imgs.values())} frames, {n} colours -> {os.path.abspath(out_dir)}")


if __name__ == "__main__":
    main()
