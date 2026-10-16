"""Paladin — pure Heaven (☰ over ☰, hexagram 1). Lance. Purple. Mounted on a
strong war horse (ground steed). 96×96 box.

Rider: an armoured knight in purple-enamelled plate with steel trim, an open
nasal helm with a purple plume. Horse: a heavy bay charger with a steel
chamfron and a purple caparison. Drawn original in the GBA FE idiom; faces LEFT.
"""
import math
from pixelkit import (Figure, Palette, grid, capsule, polyline_capsule, blade, arc, ellipse,
                      shaded_ellipse, tapered_chain, flip_part, rot90_part, Part)
from pixelkit.palette import SKIN, OUTLINE, TRIGRAM

NAME = "paladin"
BOX = 96
GROUND = 86

# 14 opaque colours. Shared: M=w=E (white), j=z, g=o.
_white = (240, 244, 255)
PALETTE = Palette(NAME, {
    **SKIN,
    **TRIGRAM["heaven"],
    "M": _white, "m": (170, 178, 200), "n": (92, 98, 132),
    "w": _white, "E": _white, "e": (176, 220, 255),
    "L": (184, 136, 92), "l": (128, 84, 50), "j": SKIN["z"],
    "h": (56, 44, 70), "H": (56, 44, 70), "g": OUTLINE,
    "A": TRIGRAM["heaven"]["C"], "a": TRIGRAM["heaven"]["c"], "q": TRIGRAM["heaven"]["k"],
})

# --- rider parts ------------------------------------------------------------
# Nasal helm, open face. Anchor = neck.
HEAD = grid("""
....CC....
...MMmmm..
..MMmmmmn.
.MMmmmmmnn
.MmnmmmSnn
.msSoSSsnn
.sSsSsszn.
..sssszz..
..zsssz...
...zzz....
""", anchor=(5, 10))

HEAD_HURT = grid("""
....CC....
...MMmmm..
..MMmmmmn.
.MMmmmmmnn
.MmnmmmSnn
.msSooSsnn
.sSszsszn.
..sszszz..
..zsssz...
...zzz....
""", anchor=(5, 10))

PLUME = {
    "rest": grid("""
.CC
Ccc
ck.
k..
""", anchor=(0, 3)),
    "back": grid("""
CCc.
.cck
...k
""", anchor=(0, 2)),
}

# Breastplate in purple enamel with steel pauldrons; anchored at the neck.
TORSO_FRONT = grid("""
....mm....
.MMmCcckmn
MMmmCccknn
Mmmmccckkn
.mmCcccckk
..Ccccckk.
..Ccccckk.
..cccckkk.
..nmmmmn..
..Ccccck..
.CCcccckk.
.Ccccckkk.
""", anchor=(5, 0))

TORSO_SIDE = grid("""
...mm...
.MMmccmn
MMmmcknn
Mmmmckkn
.mmcckk.
..ccckk.
..ccckk.
..cckkk.
..nmmn..
..ccckk.
.Cccckk.
.Cccckk.
""", anchor=(4, 0))

TORSO_BACK = grid("""
....mm....
.nmkccmMM.
nnmkcccmMM
nmkkcccmmM
.kkccccmm.
..kccccC..
..kccccC..
..kkcccc..
..nmmmmn..
..kccccC..
.kkccccCC.
.kkkcccC..
""", anchor=(5, 0))

GAUNTLET = {
    "fist": grid("""
.Mm.
Mmmn
.nn.
""", anchor=(1, 1)),
    "grip": grid("""
.Mm.
Mmmn
.mnn
""", anchor=(1, 1)),
    "open": grid("""
.Mmm
Mmmn
.nnn
""", anchor=(1, 1)),
}

SABATON = {
    "side": grid("""
..Mmm.
.Mmmmn
Mmmmmnn
nnnnnnn
""", anchor=(3, 0)),
    "front": grid("""
.Mmm..
Mmmmmn
mmmmnn
nnnnnn
""", anchor=(2, 0)),
    "back": grid("""
.mMM..
nmmmmM
nnmmmmM
nnnnnnn
""", anchor=(3, 0)),
    "tip": grid("""
.Mmm.
mmmmn
.nnn.
""", anchor=(2, 0)),
}

STAR = grid("""
....E....
....E....
..E.E.E..
...EEE...
EEEEEEEEE
...EEE...
..E.E.E..
....E....
....E....
""", anchor=(4, 4))

SPARK = grid("""
..E..
.EEE.
EE.EE
.EEE.
..E..
""", anchor=(2, 2))

DUST = grid("""
..ee.ee..
.eEeeeEe.
ee.eee.ee
.e..e..e.
""", anchor=(4, 3))


def dash_lines(n=3, length=10, step=3):
    p = Part({}, (0, 0))
    for i in range(n):
        for k in range(length - i * 2):
            p.pixels[(k, i * step)] = "e" if k % 3 else "E"
    return p


def lance(angle, variant="normal"):
    """Lance anchored at the grip: 8 px of butt behind the hand, 22 px ahead."""
    r = math.radians(angle)
    dx, dy = math.cos(r), math.sin(r)
    tip = (round(22 * dx), round(22 * dy))
    butt = (round(-8 * dx), round(-8 * dy))
    if variant == "blur":
        return blade((round(4 * dx), round(4 * dy)), tip, width=4, letters=("E", "e", "e"), taper=0.3, edge=None)
    p = capsule(butt, (round(15 * dx), round(15 * dy)), 2, ("L", "l", "j"))
    head = blade((round(15 * dx), round(15 * dy)), tip, width=3, letters=("M", "m", "n"), taper=0.6, edge="w")
    p = p.union(head)
    # vamplate: a small steel disc just ahead of the hand
    for s in (-1, 0, 1):
        nx, ny = -dy, dx
        p.pixels[(round(3 * dx + s * nx), round(3 * dy + s * ny))] = "m"
    if variant == "glint":
        for (ex, ey) in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
            p.pixels[(round(19 * dx) + ex, round(19 * dy) + ey)] = "E"
    return p


FIGURE = Figure(
    build="medium", arm_w=4, leg_w=4, box=BOX, ground=GROUND,
    parts={"heads": {"normal": HEAD, "hurt": HEAD_HURT},
           "torsos": {"front": TORSO_FRONT, "side": TORSO_SIDE, "back": TORSO_BACK},
           "hands": GAUNTLET, "boots": SABATON,
           "extras": {**{"plume_" + k: v for k, v in PLUME.items()}, "star": STAR, "spark": SPARK, "dust": DUST}},
    sleeves=("M", "m", "n"),
    pants=("C", "c", "k"),
    weapon=lance,
)

# --- the war horse ------------------------------------------------------------
HORSE_HEAD = {
    # anchor = poll (top of the head where the neck joins). Faces left-down.
    "normal": grid("""
......hh..hh..
.....LLlllll..
....LLlmmllll.
...LLllmmlllj.
..LLlllmmlljj.
.LLlllomllljj.
.LllllsmmLljj.
.lllllmmllljj.
.jlllmmlllj...
.jllllllljj...
.zjlllljj.....
.zzjjjj.......
""", anchor=(10, 1)),
    "flare": grid("""
......hh..hh..
.....LLlllll..
....LLlmmllll.
...LLllmmlllj.
..LLlllmmlljj.
.LLllloomlljj.
.LlllllmmLljj.
.lllllmmllljj.
.jlllmmlllj...
.jwlllllljj...
.zjlllljj.....
.zzjjjj.......
""", anchor=(10, 1)),
}

HOOF = grid("""
nnnn
nnnn
""", anchor=(2, 0))

TAIL = {
    "hang": [(0, 0), (3, 5), (4, 11), (3, 16)],
    "flow": [(0, 0), (6, 3), (12, 5), (18, 5)],
    "flick": [(0, 0), (5, -3), (10, -2), (14, 1)],
}

# leg angle sets: (upper, lower) for near_front, far_front, near_rear, far_rear
LEGS = {
    "stand":   ((96, 84), (104, 80), (82, 98), (76, 100)),
    "stand2":  ((94, 86), (102, 82), (84, 96), (78, 98)),
    "step":    ((120, 100), (90, 80), (70, 95), (85, 100)),
    "stretch": ((135, 150), (120, 130), (45, 55), (55, 65)),
    "gather":  ((60, 125), (70, 130), (115, 95), (120, 90)),
    "brace":   ((125, 95), (115, 90), (60, 100), (65, 105)),
    "rear":    ((165, 70), (160, 80), (80, 100), (72, 104)),
    "stumble": ((150, 20), (140, 30), (60, 110), (65, 112)),
    "crouch":  ((110, 60), (105, 65), (95, 60), (90, 65)),
}


def horse(gx, gy, legs="stand", tail="hang", tilt=0.0, head_dy=0, head_dx=0, body_dy=0, head_var="normal"):
    """Parts for the war horse. (gx, gy) = ground point under the barrel centre.
    Returns extras entries for the figure's 'back' layer (far legs, tail, body,
    neck, head) and 'front' layer (near legs), plus the saddle point."""
    t = math.radians(tilt)
    ct, st = math.cos(t), math.sin(t)

    def L(x, y):
        """local (x right, y down; origin at ground under barrel centre) -> canvas, tilted about the barrel centre"""
        bx, by = 0, -19 + body_dy
        rx, ry = x - bx, y - by
        return (round(gx + bx + rx * ct - ry * st), round(gy + by + rx * st + ry * ct))

    back, front = [], []

    def leg(hip, angles, width, letters, layer):
        ua, la = angles
        hx, hy = hip
        kx, ky = hx + 7 * math.cos(math.radians(ua)), hy + 7 * math.sin(math.radians(ua))
        fx, fy = kx + 8 * math.cos(math.radians(la)), ky + 8 * math.sin(math.radians(la))
        pts = [L(hx, hy), L(kx, ky), L(fx, fy)]
        layer.append((polyline_capsule(pts, width, letters), (0, 0), 0, 0, "back"))
        layer.append((HOOF, pts[2], 0, 0, "back"))

    nf, ff, nr, fr = LEGS[legs]
    # far legs (darker)
    leg((-12, -17 + body_dy), ff, 4, ("l", "j", "j"), back)
    leg((12, -17 + body_dy), fr, 4, ("l", "j", "j"), back)
    # tail
    tp = [L(19 + x, -24 + body_dy + y) for (x, y) in TAIL[tail]]
    back.append((tapered_chain(tp, 4, 2, ("h", "h", "g")), (0, 0), 0, 0, "back"))
    # barrel + caparison
    barrel = shaded_ellipse(L(0, -19 + body_dy), 20, 8, ("L", "l", "j"), tilt=tilt)
    back.append((barrel, (0, 0), 0, 0, "back"))
    cap = shaded_ellipse(L(0, -21 + body_dy), 17, 7, ("C", "c", "k"), tilt=tilt)
    # scalloped hem: drop the lowest rows in a zigzag
    hem = {}
    for (x, y), c in cap.pixels.items():
        cx, cy = L(0, -21 + body_dy)
        ly = (x - cx) * -st + (y - cy) * ct      # local y
        lx = (x - cx) * ct + (y - cy) * st
        if ly > 4 and ((int(lx) // 3) % 2 == 0 or ly > 5.5):
            continue
        hem[(x, y)] = c
    back.append((Part(hem, (0, 0)), (0, 0), 0, 0, "back"))
    # saddle
    sx, sy = L(0, -28 + body_dy)
    saddle = grid("""
..jlljj..
.jllllljj
jjjjjjjjj
""", anchor=(4, 1))
    back.append((saddle, (sx, sy), 0, 0, "back"))
    # neck + mane + head
    n0 = L(-13, -22 + body_dy)
    nm = L(-19 + head_dx // 2, -31 + head_dy // 2)
    n1 = L(-24 + head_dx, -38 + head_dy)
    back.append((tapered_chain([n0, nm, n1], 11, 7, ("L", "l", "j")), (0, 0), 0, 0, "back"))
    m0 = L(-9, -27 + body_dy)
    m1 = L(-21 + head_dx, -42 + head_dy)
    back.append((capsule(m0, m1, 3, ("h", "h", "g")), (0, 0), 0, 0, "back"))
    back.append((HORSE_HEAD[head_var], n1, 0, 0, "back"))
    # near legs (in front of the barrel)
    leg((-11, -16 + body_dy), nf, 5, ("L", "l", "j"), front)
    leg((13, -16 + body_dy), nr, 5, ("L", "l", "j"), front)
    rider_root = L(0, -30 + body_dy)
    return back + front, rider_root


RX = 50   # ground point under the barrel centre at rest


def P(dx=0, legs="stand", tail="hang", tilt=0.0, head_dy=0, head_dx=0, body_dy=0, plume="rest",
      rider=None, head_var="normal", **kw):
    """Base mounted pose: horse standing, knight upright, lance held upright in the near hand."""
    parts, root = horse(RX + dx, GROUND, legs, tail, tilt, head_dy, head_dx, body_dy, head_var)
    base = dict(
        root=root, planted=False, torso="front", head="normal", lean=(0, 0),
        near_arm=(100, 20), far_arm=(70, 110), near_hand="grip", far_hand="fist",
        near_leg=(125, 92), far_leg=None, near_boot="side",
        extras=parts + [("plume_" + plume, "neck", 2, -10, "top")],
        weapon=dict(hand="near", angle=-78, layer="top"),
        shadow=(26, 3), shadow_off=(0, 0),
    )
    if rider:
        base.update(rider)
    base.update(kw)
    return base


def slash(joint, r, a0, a1, width=6, dx=0, dy=0):
    return (arc((0, 0), r - width, r, a0, a1), joint, dx, dy)


def animations():
    idle = [
        P(legs="stand"),
        P(legs="stand2", head_dy=1, tail="flick", near_arm=(100, 22)),
        P(legs="stand", head_dy=1, body_dy=1, near_arm=(100, 24), weapon=dict(hand="near", angle=-80, layer="top")),
        P(legs="stand2", tail="flick", near_arm=(100, 22)),
    ]
    # regular: couch the lance and surge forward
    lean = [
        P(dx=1, legs="gather", tail="flow", head_dy=-2, torso="front", near_arm=(120, 40), far_arm=(60, 100),
          weapon=dict(hand="near", angle=-40, layer="top"), plume="back"),
        P(dx=3, legs="gather", tail="flow", head_dy=-3, tilt=6, torso="back", lean=(2, 0), near_arm=(140, 60),
          weapon=dict(hand="near", angle=-15, layer="top"), plume="back"),
        P(dx=4, legs="rear", tail="flow", head_dy=-6, head_dx=2, tilt=12, torso="back", lean=(3, -1), near_arm=(150, 80),
          weapon=dict(hand="near", angle=0, layer="top"), plume="back"),
    ]
    hold = [
        lean[2],
        P(dx=4, legs="rear", tail="flow", head_dy=-7, head_dx=2, tilt=13, torso="back", lean=(3, -2), near_arm=(150, 82),
          weapon=dict(hand="near", angle=2, layer="top"), plume="back"),
    ]
    lunge = [
        P(dx=-6, legs="stretch", tail="flow", head_dy=2, head_dx=-4, tilt=-4, torso="side", lean=(-3, 1),
          near_arm=(165, 175), far_arm=(80, 120),
          weapon=dict(hand="near", angle=178, layer="top", variant="blur"), plume="back",
          effects=[(dash_lines(3, 14), "pelvis", 16, -6)]),
        P(dx=-14, legs="stretch", tail="flow", head_dy=1, head_dx=-5, tilt=-2, torso="side", lean=(-4, 1),
          near_arm=(172, 180), far_arm=(80, 120),
          weapon=dict(hand="near", angle=180, layer="top"), plume="back",
          effects=[(STAR, "wr_near", -24, 0), (dash_lines(3, 12), "pelvis", 18, -4)]),
        P(dx=-14, legs="brace", tail="flow", head_dy=0, head_dx=-3, tilt=0, torso="side", lean=(-3, 1),
          near_arm=(170, 182), far_arm=(80, 120),
          weapon=dict(hand="near", angle=184, layer="top"), plume="back",
          effects=[(DUST, "pelvis", -20, 32)]),
    ]
    recover = [
        P(dx=-10, legs="brace", tail="hang", torso="side", lean=(-2, 0), near_arm=(150, 130),
          weapon=dict(hand="near", angle=150, layer="top"), plume="back"),
        P(dx=-5, legs="step", tail="hang", torso="front", lean=(-1, 0), near_arm=(120, 70),
          weapon=dict(hand="near", angle=-30, layer="top")),
        P(dx=-1, legs="stand"),
    ]
    block = [
        P(dx=1, torso="front", near_arm=(150, -80), far_arm=(150, -70), far_hand="open",
          weapon=dict(hand="near", angle=-95, layer="top")),
        P(dx=2, legs="brace", torso="front", lean=(1, 1), near_arm=(150, -82), far_arm=(150, -72), far_hand="open",
          weapon=dict(hand="near", angle=-97, layer="top")),
    ]
    parry = [
        P(dx=1, torso="front", near_arm=(150, -80), far_arm=(150, -70), far_hand="open",
          weapon=dict(hand="near", angle=-110, layer="top")),
        P(dx=-1, torso="side", lean=(-2, 0), near_arm=(165, -140), far_arm=(120, -60), far_hand="open",
          weapon=dict(hand="near", angle=-150, layer="top", variant="blur"),
          effects=[slash("wr_near", 18, -80, -170, width=4)]),
        P(dx=-2, torso="side", lean=(-2, 0), near_arm=(172, 178), far_arm=(110, -50), far_hand="open",
          weapon=dict(hand="near", angle=178, layer="top"),
          effects=[(SPARK, "wr_near", -22, 0)]),
    ]
    hit = [
        P(dx=2, head="hurt", lean=(2, 1), head_off=(1, 0), head_dy=-3, head_dx=1, tail="flick",
          near_arm=(70, 0), far_arm=(40, 70), far_hand="open",
          weapon=dict(hand="near", angle=-60, layer="top"), plume="back"),
        P(dx=2, head="hurt", lean=(2, 1), head_off=(1, 1), head_dy=-2, tail="flick",
          near_arm=(80, 10), far_arm=(45, 75), far_hand="open",
          weapon=dict(hand="near", angle=-65, layer="top"), plume="back"),
    ]
    # Stagger (lance): the horse stumbles forward onto its knees; the knight lurches over its neck.
    stagger = [
        P(dx=3, head="hurt", lean=(3, 1), head_off=(1, 0), head_dy=-4, tail="flick", legs="brace",
          near_arm=(60, -20), far_arm=(30, 60), far_hand="open",
          weapon=dict(hand="near", angle=-50, layer="top"), plume="back"),
        P(dx=-2, head="hurt", lean=(-5, 3), head_off=(-1, 1), head_dy=8, head_dx=-2, tilt=-10, body_dy=4, tail="flow",
          legs="stumble", near_arm=(170, 150), far_arm=(150, 120), far_hand="open", near_leg=(140, 100),
          weapon=dict(hand="near", angle=160, layer="top"), plume="back",
          effects=[(DUST, "pelvis", -26, 30)]),
        P(dx=-1, head="normal", lean=(-2, 1), head_dy=2, tilt=-4, body_dy=2, tail="hang",
          legs="crouch", near_arm=(140, 90), far_arm=(120, 110),
          weapon=dict(hand="near", angle=-40, layer="top")),
    ]
    dodge_up = [
        P(dx=0, legs="gather", lean=(0, 1), head_dy=-2),
        P(dx=1, legs="rear", tilt=18, head_dy=-6, head_dx=3, tail="flow", lean=(2, -2), near_arm=(110, 30),
          weapon=dict(hand="near", angle=-70, layer="top"), plume="back"),
    ]
    dodge_down = [
        P(dx=0, lean=(-2, 2), head_dy=3, head_dx=-2, near_arm=(130, 60), far_arm=(110, 110), far_hand="open",
          weapon=dict(hand="near", angle=-30, layer="top")),
        P(dx=0, lean=(-5, 4), head_off=(-1, 1), head_dy=8, head_dx=-4, legs="crouch", body_dy=3, near_arm=(150, 100),
          far_arm=(150, 110), far_hand="open", near_leg=(135, 95),
          weapon=dict(hand="near", angle=10, layer="top"), plume="back"),
    ]
    dodge_forward = [
        P(dx=-6, legs="step", tail="flow", head_dy=1, head_dx=-2, lean=(-2, 0),
          effects=[(dash_lines(2, 8), "pelvis", 20, 10)]),
        P(dx=-10, legs="stand2", tail="flow", lean=(-1, 0)),
    ]
    dodge_back = [
        P(dx=6, legs="gather", tail="flick", head_dy=-3, head_dx=2, lean=(2, 0), plume="back",
          effects=[(dash_lines(2, 8), "pelvis", -30, 10)]),
        P(dx=10, legs="stand2", tail="hang", lean=(1, 0)),
    ]
    # Critical: a full charge — rear up, thunder forward, run the foe through, skid to a stop.
    crit_lean = [
        P(dx=2, legs="gather", tail="flow", head_dy=-3, torso="back", lean=(2, 0), near_arm=(130, 50),
          weapon=dict(hand="near", angle=-30, layer="top"), plume="back"),
        P(dx=4, legs="rear", tilt=16, head_dy=-6, head_dx=3, tail="flow", torso="back", lean=(3, -2), near_arm=(150, 70),
          weapon=dict(hand="near", angle=-10, layer="top"), plume="back"),
        P(dx=5, legs="rear", tilt=24, head_dy=-8, head_dx=4, tail="flow", torso="back", lean=(4, -3), near_arm=(155, 80),
          weapon=dict(hand="near", angle=0, layer="top", variant="glint"), plume="back"),
    ]
    crit_hold = [
        crit_lean[2],
        P(dx=5, legs="rear", tilt=25, head_dy=-9, head_dx=4, tail="flow", torso="back", lean=(4, -4), near_arm=(155, 82),
          weapon=dict(hand="near", angle=2, layer="top"), plume="back",
          effects=[(STAR, "wr_near", 18, 0)]),
    ]
    crit_lunge = [
        P(dx=-2, legs="stretch", tail="flow", tilt=4, head_dy=-2, head_dx=-2, torso="side", lean=(-2, 0),
          near_arm=(160, 160), far_arm=(80, 120),
          weapon=dict(hand="near", angle=170, layer="top"), plume="back",
          effects=[(dash_lines(3, 16), "pelvis", 14, -8), (DUST, "pelvis", 26, 30)]),
        P(dx=-10, legs="gather", tail="flow", tilt=-2, head_dy=1, head_dx=-4, torso="side", lean=(-3, 1),
          near_arm=(168, 176), far_arm=(80, 120),
          weapon=dict(hand="near", angle=178, layer="top", variant="blur"), plume="back",
          effects=[(dash_lines(3, 18), "pelvis", 16, -6)]),
        P(dx=-8, legs="stretch", tail="flow", tilt=-3, head_dy=2, head_dx=-5, torso="side", lean=(-4, 1),
          near_arm=(174, 180), far_arm=(80, 120),
          weapon=dict(hand="near", angle=180, layer="top"), plume="back",
          effects=[(STAR, "wr_near", -24, 0), slash("wr_near", 28, 150, 210, width=5), (dash_lines(3, 14), "pelvis", 18, -4)]),
        P(dx=-14, legs="brace", tail="flow", tilt=6, head_dy=-4, head_dx=-2, torso="side", lean=(-3, 0),
          near_arm=(172, 184), far_arm=(80, 120),
          weapon=dict(hand="near", angle=186, layer="top"), plume="back",
          effects=[(DUST, "pelvis", -22, 32), (DUST, "pelvis", 14, 32)]),
        P(dx=-14, legs="brace", tail="hang", tilt=2, head_dy=-2, torso="side", lean=(-2, 0),
          near_arm=(165, 180), far_arm=(80, 120),
          weapon=dict(hand="near", angle=182, layer="top"), plume="back",
          effects=[(DUST, "pelvis", -20, 33)]),
    ]
    crit_recover = [
        P(dx=-14, legs="brace", tail="hang", torso="side", lean=(-2, 0), near_arm=(150, 130),
          weapon=dict(hand="near", angle=150, layer="top"), plume="back"),
        P(dx=-7, legs="step", tail="hang", torso="front", lean=(-1, 0), near_arm=(120, 70),
          weapon=dict(hand="near", angle=-30, layer="top")),
        P(dx=-1, legs="stand"),
    ]
    return [
        ("idle", 6, True, idle),
        ("lean", 10, False, lean),
        ("hold", 5, True, hold),
        ("lunge", 20, False, lunge),
        ("recover", 9, False, recover),
        ("block", 10, False, block),
        ("parry", 12, False, parry),
        ("hit", 10, False, hit),
        ("stagger", 6, False, stagger),
        ("dodge_up", 10, False, dodge_up),
        ("dodge_down", 10, False, dodge_down),
        ("dodge_forward", 10, False, dodge_forward),
        ("dodge_back", 10, False, dodge_back),
        ("crit_lean", 10, False, crit_lean),
        ("crit_hold", 5, True, crit_hold),
        ("crit_lunge", 20, False, crit_lunge),
        ("crit_recover", 9, False, crit_recover),
    ]
