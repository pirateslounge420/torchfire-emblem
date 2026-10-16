"""Bastion (Mountain / orange) — hand-pixelled frames.

Three hand-drawn bodies (body.txt planted stance, body_back.txt crouched and
leaning away with both gauntlets raised behind the helm, body_lunge.txt folded
into a two-handed ground smash) plus hand-placed overlays for the arms, the
two-handed mace, the smear and the impact dust. The attack follows the six
beats of the GBA General / Hawkeye sheets: stance → mace hauled back-low →
raised behind the helm (two hands) → one big smear → ground smash → haul up.

idle (8, loops): at rest with the mace head on the ground; the pauldrons breathe 1 px, the
visor glow pulses V → G → V, the tabard tail sways through three hand-drawn states.
select (10, one-shot): haul → mace level at the chest (mid-haft grip) → swung up-forward →
one ring smear whirling over the helm (+ glint) → caught pointing up → up on the toes →
slam streak → head buried with a 1-px body drop and dust → dust spreads → idle frame 0.

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

# 15 opaque colours. G is the plate edge; h the orange-tinted smear fringe; d the impact dust.
PAL = Palette(NAME, {
    "O": (255, 168, 56), "p": (216, 104, 24), "q": (140, 52, 16),      # orange enamel ramp
    "V": (255, 232, 120),                                               # visor glow (the accent)
    "K": (48, 50, 66), "k": (98, 102, 124), "G": (176, 180, 200),       # plate: near-black, dark grey, light edge
    "H": (248, 248, 248), "h": (255, 226, 176),                         # white edge / smear core, orange-tinted smear fringe
    "d": (150, 124, 92),                                                # impact dust
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


DUST = [(40, -8, "dh"), (38, -7, "H"), (41, 3, "hd"), (39, 2, "H"), (36, -3, "H"), (42, -9, "d"), (42, 5, "d")]


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


# --- idle: an 8-frame at-rest loop -------------------------------------------------------------
# The tabard tail hanging behind the far leg, rows 28-32, cols 29-35 of the body grid.
# '?' = the leg underneath, '.' clears a pixel. Three hand-drawn states of the cloth.
TAIL_REST = """
?Cco...
??Cco..
???cco.
???co..
???o...
"""
TAIL_OUT = """
?Cco...
??Ccco.
???ccco
???occo
???.ooo
"""
TAIL_TUCK = """
?Cco...
??Co...
???co..
???o...
???....
"""


def breathe(g, up):
    """lift both pauldrons `up` px (1 = inhale). Body-grid regions converted to box coords;
    the chest plate, helm and arms stay put so only the shoulders move."""
    if not up:
        return
    bx, by = X_OFF, GROUND - (BODY_H - 1)
    g.shift_region(bx + 6, by + 11, bx + 16, by + 27, 0, -up)     # near pauldron
    g.shift_region(bx + 28, by + 10, bx + 39, by + 26, 0, -up)    # far pauldron


def idle(up=0, visor="VVV", tail=TAIL_REST):
    """at rest: planted wide, mace head on the ground in front, both gauntlets stacked on the haft"""
    g = body()
    breathe(g, up)
    P(g, 6, 15, visor)                                       # the glow pulses: V -> G (plate edge) -> V
    B(g, 28, 29, tail)
    haft(g, -2, 36, 15, 24, grip=range(23, 31))
    mace_head(g, 37, -6)
    P(g, 23, 15, "oKo"); P(g, 24, 15, "oKKo")                # pommel knob
    B(g, 21, 12, FAR_ARM_STANCE)
    B(g, 20, 4, NEAR_ARM_STANCE)
    return g.tidy()


# --- select: a one-shot flourish when the player picks him ----------------------------------------
# Both gauntlets grip the MIDDLE of the haft out in front at chest height (near hand below, far hand
# above); the near arm hangs from the pauldron to the elbow and the forearm rises to the gauntlet.
NEAR_ARM_FRONT = """
?oooooo???
oGGkKKo???
oGkKKKo???
opqqqKo???
oGkKKKoKo?
oGkKKKoKKo
oGkKKKoKKo
?oKKKKokKo
?oKKKKKkKo
??oooooooo
"""

GLINT = [(0, -2, "H"), (1, -2, "H"), (2, -4, "hHHHh"), (3, -2, "H"), (4, -2, "H")]


def front_grip(g):
    B(g, 15, 3, FAR_GAUNTLET)
    B(g, 20, 2, NEAR_ARM_FRONT)


def spin_level():
    """select beat 2: mace hauled up level at chest height, head forward, hands at the mid-haft"""
    g = body()
    haft(g, 14, 19, -4, 19)
    P(g, 18, 15, "oo"); P(g, 19, 15, "Ko"); P(g, 20, 15, "Ko"); P(g, 21, 15, "oo")   # pommel knob at the chest
    mace_head(g, 16, -11)
    front_grip(g)
    return g.tidy()


def spin_fwdup():
    """select beat 3: the head swings up and forward (45 degrees)"""
    g = body()
    haft(g, 13, 27, -2, 12)
    P(g, 28, 13, "oKo"); P(g, 29, 14, "oKo")                                       # pommel knob
    mace_head(g, 5, -9)
    front_grip(g)
    return g.tidy()


def ring_pixels():
    """the spin smear: one thick crescent of the mace head's path over the helm, pointed at both ends.
    Exaggerated like the GBA crit crescents: centred above the grip at (10,14), radius ~20, so the
    crown of the ring clears the horns and the back end tapers off over the far pauldron."""
    import math
    cx, cy = 10.0, 14.0
    px = {}
    steps = 240
    for i in range(steps + 1):
        t = i / steps
        ang = math.pi + 0.45 - t * (math.pi + 0.45 - 0.55)   # from forward-low, over the top, down the back
        thick = 1.0 + 3.4 * math.sin(math.pi * t) ** 0.8     # thin tips, thick crown
        for r in (17.5, 18.0, 18.5, 19.0, 19.5, 20.0, 20.5, 21.0, 21.5, 22.0):
            dr = abs(r - 19.75)
            if dr > thick / 2:
                continue
            x = round(cx + r * math.cos(ang)); y = round(cy - r * math.sin(ang))
            ch = "H" if dr <= thick / 2 - 1.0 and thick > 2.2 else "h"
            if px.get((y, x)) != "H":
                px[(y, x)] = ch
    return px


RING = ring_pixels()


def spin_ring():
    """select beat 4: the whole mace is one orange-fringed ring smear whirling over the helm"""
    g = body()
    front_grip(g)
    for (y, x), ch in RING.items():
        P(g, y, x, ch)
    for y, x, t in [(26, -11, "h"), (-7, 24, "h"), (-9, 4, "h"), (18, 33, "h")]:    # loose flecks
        P(g, y, x, t)
    for y, x, t in [(13, 3, "h"), (11, 2, "h"), (9, 1, "h"), (7, 0, "h"), (5, -1, "h")]:   # the blurred haft, grip to ring
        P(g, y, x, t)
    return g.tidy()


def spin_up(glint=True, rise=0):
    """select beat 5: caught pointing straight up (3:1 lean forward so the head clears the horn);
    rise=1 lifts the whole figure onto its toes for the one-frame anticipation before the slam"""
    g = body()
    haft(g, 9, 30, 3, 10)
    P(g, 31, 9, "oKo"); P(g, 32, 9, "oKo")                                         # pommel knob
    mace_head(g, 3, -1)
    front_grip(g)
    if glint:
        for y, x, t in GLINT:
            P(g, y, x, t)
    g = g.tidy()
    return g.shift(0, -rise) if rise else g


STREAK = [(8, 2, "hh"), (9, 1, "hh"), (10, 0, "hHh"), (11, -1, "hHh"), (12, -2, "hHHh"), (13, -3, "hHHh"), (14, -4, "hHHh"),
          (15, -5, "hHHHh"), (16, -5, "hHHHh"), (17, -6, "hHHHh"), (18, -6, "hHHHh"), (19, -7, "hHHHh"), (20, -7, "hHHHh"),
          (21, -8, "hHHHh"), (22, -8, "hHHh"), (23, -9, "hHHh"), (24, -9, "hHHh"), (25, -9, "hHh"), (26, -10, "hHh"),
          (27, -10, "hh"), (28, -10, "hh"), (29, -10, "h")]


def slam_streak():
    """select beat 6: the mace comes down hard, the head's path a pale streak down the front;
    the hands have slid back to the pommel end for the slam"""
    g = body()
    for y, x, t in STREAK:
        P(g, y, x, t)
    haft(g, 14, 22, -3, 33, grip=range(22, 27))
    mace_head(g, 30, -9)
    P(g, 21, 14, "oKo"); P(g, 22, 15, "oKo")                                       # pommel knob
    B(g, 21, 8, FAR_GAUNTLET)
    P(g, 21, 13, "KKo"); P(g, 22, 13, "kKo"); P(g, 23, 13, "ooo")                   # far forearm stub
    B(g, 21, 3, NEAR_ARM_LIFT)
    return g.tidy()


SLAM_DUST = [(36, -12, "dd"), (37, -13, "ddd"), (38, -12, "dd"), (39, -14, "d"), (33, -9, "d"), (31, -6, "d"),
             (38, 2, "dd"), (39, 2, "ddd"), (40, 3, "dd"), (41, 6, "d"), (33, 4, "d"),
             (35, -3, "H"), (34, -2, "h"), (36, 2, "H"), (35, 3, "h")]
SLAM_DUST2 = [(32, -14, "dd"), (33, -15, "d"), (34, -9, "d"), (30, -5, "d"), (38, -14, "d"), (40, -15, "d"),
              (31, 4, "d"), (33, 7, "dd"), (35, 8, "d"), (41, 8, "d"), (36, 5, "d")]


def slam_impact(drop=1, dust=SLAM_DUST):
    """select beat 7: the head buried back in its resting spot; the whole body drops `drop` px
    (the screen-shake jolt) while the head stays in the ground, so the haft steepens a hair"""
    g = body(dy=drop)
    haft(g, -2, 36, 15, 24 + drop, grip=range(23 + drop, 31 + drop))
    mace_head(g, 37, -6)
    P(g, 23, 15, "oKo", dy=drop); P(g, 24, 15, "oKKo", dy=drop)
    B(g, 21, 12, FAR_ARM_STANCE, dy=drop)
    B(g, 20, 4, NEAR_ARM_STANCE, dy=drop)
    for y, x, t in dust:
        P(g, y, x, t)
    return g.tidy()


def animations():
    idle_frames = [
        idle(0, "VVV", TAIL_REST), idle(0, "VVV", TAIL_OUT), idle(1, "VVV", TAIL_OUT), idle(1, "VVV", TAIL_REST),
        idle(1, "GVG", TAIL_TUCK), idle(0, "GGG", TAIL_TUCK), idle(0, "GVG", TAIL_REST), idle(0, "VVV", TAIL_REST),
    ]
    select_frames = [
        haul(), spin_level(), spin_fwdup(), spin_ring(), spin_up(True), spin_up(False, rise=1),
        slam_streak(), slam_impact(1, SLAM_DUST), slam_impact(0, SLAM_DUST2), idle_frames[0],
    ]
    return {
        "idle": (idle_frames, 6, True),
        "select": (select_frames, 10, False),
        "lean": ([mace_back(), raised(), raised()], 10, False),
        "hold": ([raised(), raised(-1)], 5, True),
        "lunge": ([smear(), impact(), impact()], 20, False),
        "recover": ([haul(), stance(0), stance(0)], 9, False),
    }


def main():
    anims = animations()
    n = PAL.check([g for frames, _, _ in anims.values() for g in frames])
    imgs = {k: ([render(g, PAL) for g in frames], fps, loop) for k, (frames, fps, loop) in anims.items()}
    sel = imgs["select"][0]
    beats = [imgs["idle"][0][0], sel[1], sel[2], sel[3], sel[4], sel[6], sel[7], sel[8],
             imgs["lean"][0][0], imgs["lean"][0][1], imgs["lunge"][0][0], imgs["lunge"][0][1], imgs["recover"][0][0]]
    strip(beats, os.path.join(HERE, f"{NAME}_attack.png"), zoom=5,
          labels=["idle", "sel: level", "sel: swing up", "sel: ring", "sel: caught", "sel: slam", "sel: impact", "sel: dust",
                  "mace back-low", "raised, two hands", "smear", "ground smash", "haul up"])
    gif(imgs["idle"][0] + sel + beats[8:] + [imgs["idle"][0][0]], os.path.join(HERE, f"{NAME}_attack.gif"),
        [160] * 8 + [100] * 10 + [160, 260, 70, 360, 200, 500])
    out_dir = os.path.join(HERE, "..", "..", "..", "godot", "art", f"{NAME}_v2")
    sheet(imgs, out_dir, NAME, BOX, ORIGIN)
    print(f"{NAME}: {sum(len(f) for f, _, _ in imgs.values())} frames, {n} colours -> {os.path.abspath(out_dir)}")


if __name__ == "__main__":
    main()
