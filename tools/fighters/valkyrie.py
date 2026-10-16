"""Valkyrie — pure Wind (☴ over ☴, hexagram 57). Glaive. Seafoam. Mounted on a
flying wyvern (two legs, bat wings). 96×96 box; the wyvern hovers above its
ground shadow.

Rider: a tall woman in a winged steel helm, seafoam tunic over mail, long
blonde braid, a long glaive. Wyvern: dark green-grey hide, seafoam wing
membranes and belly. Drawn original in the GBA FE idiom; faces LEFT.
"""
import math
from pixelkit import (Figure, Palette, grid, capsule, polyline_capsule, blade, arc, ellipse,
                      shaded_ellipse, tapered_chain, fill_polygon, line, Part)
from pixelkit.palette import SKIN, OUTLINE, TRIGRAM

NAME = "valkyrie"
BOX = 96
GROUND = 86

# 15 opaque colours. Shared: M=w=E (white), e=C, j=z.
_white = (240, 246, 250)
PALETTE = Palette(NAME, {
    **SKIN,
    **TRIGRAM["wind"],
    "e": TRIGRAM["wind"]["C"],
    "A": (110, 160, 140), "a": (58, 104, 92), "q": (28, 58, 56),
    "M": _white, "m": (176, 186, 204), "n": (96, 104, 136),
    "w": _white, "E": _white,
    "L": (232, 200, 120), "l": (176, 136, 64), "j": SKIN["z"],
})

# --- rider parts ------------------------------------------------------------
# Winged helm, open face; the wing crests are white. Anchor = neck.
HEAD = grid("""
.w..MMm..w.
ww.MMmmm.ww
.wMMmmmmmw.
.MMmmmmmnn.
.MmnmmmSnn.
.msSoSSsnl.
.sSsSsszll.
..sssszzl..
..zsssz.l..
...zzz..l..
""", anchor=(5, 10))

HEAD_HURT = grid("""
.w..MMm..w.
ww.MMmmm.ww
.wMMmmmmmw.
.MMmmmmmnn.
.MmnmmmSnn.
.msSooSsnl.
.sSszsszll.
..sszszzl..
..zsssz.l..
...zzz..l..
""", anchor=(5, 10))

BRAID = {
    "rest": grid("""
Ll
lL
Ll
lL
.l
""", anchor=(0, 0)),
    "fly": grid("""
lL...
.lLl.
...Ll
....l
""", anchor=(0, 0)),
}

TORSO_FRONT = grid("""
....mm....
.MMmCcckmn
MMmmCccknn
MmmmCcckkn
.mmCccckk.
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


def dash_lines(n=3, length=10, step=3):
    p = Part({}, (0, 0))
    for i in range(n):
        for k in range(length - i * 2):
            p.pixels[(k, i * step)] = "e" if k % 3 else "E"
    return p


def glaive(angle, variant="normal"):
    """Glaive anchored at the grip: 9 px of haft behind the hand, 15 px ahead + a 9 px leaf blade."""
    r = math.radians(angle)
    dx, dy = math.cos(r), math.sin(r)
    butt = (round(-9 * dx), round(-9 * dy))
    neck = (round(15 * dx), round(15 * dy))
    tip = (round(25 * dx), round(25 * dy))
    if variant == "blur":
        return blade((round(8 * dx), round(8 * dy)), tip, width=5, letters=("E", "e", "e"), taper=0.35, edge=None)
    p = capsule(butt, neck, 2, ("L", "l", "j"))
    head = blade(neck, tip, width=4, letters=("M", "m", "n"), taper=0.55, edge="w")
    p = p.union(head)
    if variant == "glint":
        for (ex, ey) in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
            p.pixels[(round(21 * dx) + ex, round(21 * dy) + ey)] = "E"
    return p


FIGURE = Figure(
    build="medium", arm_w=4, leg_w=4, box=BOX, ground=GROUND,
    parts={"heads": {"normal": HEAD, "hurt": HEAD_HURT},
           "torsos": {"front": TORSO_FRONT, "side": TORSO_SIDE, "back": TORSO_BACK},
           "hands": GAUNTLET,
           "extras": {**{"braid_" + k: v for k, v in BRAID.items()}, "star": STAR, "spark": SPARK}},
    sleeves=("M", "m", "n"),
    pants=("C", "c", "k"),
    weapon=glaive,
)

# --- the wyvern ------------------------------------------------------------------
WYVERN_HEAD = grid("""
..........qq..
.........qaq..
........aaaqq.
......Aaaaaaq.
....AAaaaoaaq.
..AAAaaaaaaaq.
.AAaaaaaaaaq..
AAaaaaaaaqq...
.qawawaaq.....
..qqaaaq......
""", anchor=(10, 2))     # anchor = where the neck joins (back of the skull); faces left-down

FOOT = grid("""
qaaq
q.q.
""", anchor=(1, 0))

WINGS = {
    # (wrist offset from root, [tip offsets from root]) — near wing
    "up":   ((4, -18), [(-12, -34), (4, -38), (20, -30)]),
    "mid":  ((10, -10), [(-4, -22), (14, -24), (28, -12)]),
    "down": ((14, 0), [(2, 6), (16, 12), (28, 16)]),
    "fold": ((8, -6), [(12, -10), (20, -6), (26, 2)]),
}
FAR_PHASE = {"up": "mid", "mid": "up", "down": "mid", "fold": "fold"}


def wing(root, variant, letters_m=("C", "c", "k"), letters_b=("A", "a", "q"), shade=False):
    """One bat wing: membrane polygon + three finger bones. root = shoulder in canvas coords."""
    rx, ry = root
    (wx, wy), tips = WINGS[variant]
    wrist = (rx + wx, ry + wy)
    tp = [(rx + tx, ry + ty) for (tx, ty) in tips]
    pts = [root, wrist, tp[0]]
    for a, b in zip(tp[:-1], tp[1:]):
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        web = (mx + (wrist[0] - mx) * 0.4, my + (wrist[1] - my) * 0.4)   # scalloped trailing edge
        pts += [web, b]
    pts.append((rx + 10, ry + 8))
    mem = fill_polygon(pts, letters_m[2] if shade else letters_m[1])
    # a lighter band along the leading edge
    out = mem
    for (tx, ty) in tips:
        out = out.union(capsule(wrist, (rx + tx, ry + ty), 2, letters_b))
    out = out.union(capsule(root, wrist, 3, letters_b))
    return out


def wyvern(gx, gy, hover=26, wings="mid", tilt=0.0, head_dx=0, head_dy=0, legs="hang", tail="s"):
    """Parts for the wyvern. (gx, gy) = ground point under the body centre; hover = body lift."""
    t = math.radians(tilt)
    ct, st = math.cos(t), math.sin(t)
    by0 = -hover

    def L(x, y):
        rx, ry = x, y - by0
        return (round(gx + rx * ct - ry * st), round(gy + by0 + rx * st + ry * ct))

    back = []
    body_c = L(0, by0)
    root_far = L(8, by0 - 6)
    root_near = L(2, by0 - 3)
    # far wing (behind everything, darker, half a beat ahead)
    back.append((wing(root_far, FAR_PHASE[wings], shade=True), (0, 0), 0, 0, "back"))
    # tail
    if tail == "s":
        tp = [L(13, by0 + 1), L(22, by0 + 5), L(30, by0 + 2), L(37, by0 - 5)]
    elif tail == "up":
        tp = [L(13, by0 + 1), L(22, by0 - 2), L(30, by0 - 10), L(35, by0 - 18)]
    else:  # down
        tp = [L(13, by0 + 1), L(21, by0 + 8), L(28, by0 + 16), L(33, by0 + 24)]
    back.append((tapered_chain(tp, 6, 2, ("A", "a", "q")), (0, 0), 0, 0, "back"))
    # body
    back.append((shaded_ellipse(body_c, 17, 8, ("A", "a", "q"), tilt=tilt), (0, 0), 0, 0, "back"))
    belly = shaded_ellipse(L(0, by0 + 4), 13, 3, ("C", "c", "k"), tilt=tilt)
    back.append((belly, (0, 0), 0, 0, "back"))
    # legs
    if legs == "hang":
        la = ((115, 70), (105, 75))
    elif legs == "tuck":
        la = ((150, 30), (140, 40))
    else:  # reach (landing / strike)
        la = ((130, 110), (120, 115))
    for i, (hx, hy, (ua, lo), w, lt) in enumerate((
            (6, by0 + 4, la[1], 4, ("a", "q", "q")),
            (3, by0 + 5, la[0], 5, ("A", "a", "q")))):
        kx, ky = hx + 7 * math.cos(math.radians(ua)), hy + 7 * math.sin(math.radians(ua))
        fx, fy = kx + 7 * math.cos(math.radians(lo)), ky + 7 * math.sin(math.radians(lo))
        pts = [L(hx, hy), L(kx, ky), L(fx, fy)]
        back.append((polyline_capsule(pts, w, lt), (0, 0), 0, 0, "back"))
        back.append((FOOT, pts[2], 0, 0, "back"))
    # neck + head
    n0 = L(-12, by0 - 2)
    n1 = L(-18 + head_dx // 2, by0 - 11 + head_dy // 2)
    n2 = L(-24 + head_dx, by0 - 17 + head_dy)
    back.append((tapered_chain([n0, n1, n2], 8, 5, ("A", "a", "q")), (0, 0), 0, 0, "back"))
    back.append((WYVERN_HEAD, n2, 0, 0, "back"))
    # near wing
    back.append((wing(root_near, wings), (0, 0), 0, 0, "back"))
    # saddle
    saddle = grid("""
..jlljj..
.jllllljj
jjjjjjjjj
""", anchor=(4, 1))
    sx, sy = L(-3, by0 - 7)
    back.append((saddle, (sx, sy), 0, 0, "back"))
    rider_root = L(-3, by0 - 9)
    return back, rider_root


RX = 50


def P(dx=0, hover=26, wings="mid", tilt=0.0, head_dx=0, head_dy=0, legs="hang", tail="s",
      braid="rest", shadow=(18, 2), **kw):
    """Base mounted pose: wyvern hovering, rider upright, glaive held upright in the near hand."""
    parts, root = wyvern(RX + dx, GROUND, hover, wings, tilt, head_dx, head_dy, legs, tail)
    base = dict(
        root=root, planted=False, torso="front", head="normal", lean=(0, 0),
        near_arm=(100, 20), far_arm=(70, 110), near_hand="grip", far_hand="fist",
        near_leg=(125, 92), far_leg=None, near_boot="side",
        extras=parts + [("braid_" + braid, "neck", 4, -6, "back")],
        weapon=dict(hand="near", angle=-78, layer="top"),
        shadow=shadow, shadow_off=(0, 0),
    )
    base.update(kw)
    return base


def slash(joint, r, a0, a1, width=6, dx=0, dy=0):
    return (arc((0, 0), r - width, r, a0, a1), joint, dx, dy)


def animations():
    idle = [
        P(wings="up", hover=26),
        P(wings="mid", hover=27, near_arm=(100, 22)),
        P(wings="down", hover=28, near_arm=(100, 24), weapon=dict(hand="near", angle=-80, layer="top")),
        P(wings="mid", hover=27, near_arm=(100, 22)),
    ]
    # regular: the wyvern rears back, then lunges as the rider chops the glaive down across
    lean = [
        P(dx=1, hover=27, wings="mid", tilt=6, torso="front", near_arm=(110, 30), far_arm=(60, 100),
          weapon=dict(hand="near", angle=-55, layer="top"), braid="fly"),
        P(dx=3, hover=29, wings="up", tilt=12, head_dy=-4, torso="back", lean=(2, 0), near_arm=(40, -60),
          weapon=dict(hand="near", angle=-70, layer="top"), braid="fly", tail="down"),
        P(dx=4, hover=31, wings="up", tilt=16, head_dy=-6, torso="back", lean=(3, -1), near_arm=(20, -80),
          weapon=dict(hand="near", angle=-95, layer="top"), braid="fly", tail="down"),
    ]
    hold = [
        lean[2],
        P(dx=4, hover=32, wings="up", tilt=17, head_dy=-7, torso="back", lean=(3, -2), near_arm=(20, -82),
          weapon=dict(hand="near", angle=-97, layer="top"), braid="fly", tail="down"),
    ]
    lunge = [
        P(dx=-6, hover=24, wings="down", tilt=-6, head_dx=-3, head_dy=3, torso="side", lean=(-3, 1),
          near_arm=(150, -150), far_arm=(80, 120), tail="up",
          weapon=dict(hand="near", angle=-160, layer="top", variant="blur"), braid="fly",
          effects=[slash("sh_near", 30, -100, -200, width=7), (dash_lines(3, 14), "pelvis", 18, -6)]),
        P(dx=-3, hover=22, wings="down", tilt=-8, head_dx=-4, head_dy=4, torso="side", lean=(-4, 1),
          near_arm=(170, 190), far_arm=(80, 120), tail="up", legs="reach",
          weapon=dict(hand="near", angle=165, layer="top"), braid="fly",
          effects=[slash("sh_near", 30, -150, -195, width=7), (STAR, "wr_near", -22, 6)]),
        P(dx=-3, hover=21, wings="mid", tilt=-4, head_dx=-3, head_dy=2, torso="side", lean=(-3, 2),
          near_arm=(165, 200), far_arm=(80, 120), tail="s", legs="reach",
          weapon=dict(hand="near", angle=150, layer="top"), braid="fly"),
    ]
    recover = [
        P(dx=-6, hover=23, wings="up", tilt=0, torso="side", lean=(-2, 1), near_arm=(150, 150),
          weapon=dict(hand="near", angle=150, layer="top"), braid="fly"),
        P(dx=-5, hover=25, wings="mid", torso="front", lean=(-1, 0), near_arm=(120, 70),
          weapon=dict(hand="near", angle=-30, layer="top")),
        P(dx=-1, hover=26, wings="up"),
    ]
    block = [
        P(dx=1, wings="fold", torso="front", near_arm=(150, -80), far_arm=(150, -70), far_hand="open",
          weapon=dict(hand="near", angle=-95, layer="top")),
        P(dx=2, wings="fold", hover=25, torso="front", lean=(1, 1), near_arm=(150, -82), far_arm=(150, -72), far_hand="open",
          weapon=dict(hand="near", angle=-97, layer="top")),
    ]
    parry = [
        P(dx=1, wings="fold", torso="front", near_arm=(150, -80), far_arm=(150, -70), far_hand="open",
          weapon=dict(hand="near", angle=-110, layer="top")),
        P(dx=-1, wings="down", torso="side", lean=(-2, 0), near_arm=(165, -140), far_arm=(120, -60), far_hand="open",
          weapon=dict(hand="near", angle=-150, layer="top", variant="blur"),
          effects=[slash("wr_near", 18, -80, -170, width=4)]),
        P(dx=-2, wings="down", torso="side", lean=(-2, 0), near_arm=(172, 178), far_arm=(110, -50), far_hand="open",
          weapon=dict(hand="near", angle=178, layer="top"),
          effects=[(SPARK, "wr_near", -24, 0)]),
    ]
    hit = [
        P(dx=2, head="hurt", lean=(2, 1), head_off=(1, 0), wings="up", tilt=8, head_dy=-3, head_dx=1,
          near_arm=(70, 0), far_arm=(40, 70), far_hand="open",
          weapon=dict(hand="near", angle=-60, layer="top"), braid="fly"),
        P(dx=2, head="hurt", lean=(2, 1), head_off=(1, 1), wings="mid", tilt=6, head_dy=-2,
          near_arm=(80, 10), far_arm=(45, 75), far_hand="open",
          weapon=dict(hand="near", angle=-65, layer="top"), braid="fly"),
    ]
    # Stagger (glaive): the wyvern is knocked into a tumble — nose-down, wings askew, rider thrown
    # onto its neck — then flaps hard to recover.
    stagger = [
        P(dx=3, head="hurt", lean=(3, 1), head_off=(1, 0), wings="up", tilt=10, head_dy=-4,
          near_arm=(60, -20), far_arm=(30, 60), far_hand="open",
          weapon=dict(hand="near", angle=-50, layer="top"), braid="fly"),
        P(dx=1, head="hurt", lean=(-5, 3), head_off=(-1, 1), wings="down", tilt=-22, hover=18, head_dy=6, head_dx=-3,
          tail="up", legs="tuck", near_arm=(170, 150), far_arm=(150, 120), far_hand="open", near_leg=(140, 100),
          weapon=dict(hand="near", angle=160, layer="top"), braid="fly", shadow=(22, 3)),
        P(dx=-1, head="normal", lean=(-2, 1), wings="up", tilt=-6, hover=22, head_dy=2,
          near_arm=(140, 90), far_arm=(120, 110),
          weapon=dict(hand="near", angle=-40, layer="top"), braid="fly"),
    ]
    dodge_up = [
        P(dx=0, wings="down", hover=24, lean=(0, 1)),
        P(dx=1, wings="up", hover=38, tilt=6, head_dy=-3, tail="down", lean=(1, -1), near_arm=(110, 30),
          weapon=dict(hand="near", angle=-70, layer="top"), braid="fly", shadow=(14, 2)),
    ]
    dodge_down = [
        P(dx=0, wings="up", hover=22, lean=(-2, 2), head_dy=3, head_dx=-2, near_arm=(130, 60), far_arm=(110, 110), far_hand="open",
          weapon=dict(hand="near", angle=-30, layer="top")),
        P(dx=0, wings="down", hover=14, tilt=-8, lean=(-5, 4), head_off=(-1, 1), head_dy=6, head_dx=-4, tail="up",
          near_arm=(150, 100), far_arm=(150, 110), far_hand="open", near_leg=(135, 95), legs="tuck",
          weapon=dict(hand="near", angle=10, layer="top"), braid="fly", shadow=(24, 3)),
    ]
    dodge_forward = [
        P(dx=-6, wings="down", hover=25, tilt=-4, lean=(-2, 0), head_dx=-2, tail="up", legs="tuck",
          effects=[(dash_lines(2, 8), "pelvis", 20, 6)]),
        P(dx=-10, wings="mid", hover=26, lean=(-1, 0), legs="hang"),
    ]
    dodge_back = [
        P(dx=4, wings="up", hover=27, tilt=8, lean=(2, 0), head_dy=-3, head_dx=2, tail="down", braid="fly",
          effects=[(dash_lines(2, 8), "pelvis", -32, 6)]),
        P(dx=5, wings="mid", hover=26, lean=(1, 0)),
    ]
    # Critical: climb, dive, cleave, pull up.
    crit_lean = [
        P(dx=2, wings="down", hover=28, tilt=8, torso="back", lean=(2, 0), near_arm=(60, -40),
          weapon=dict(hand="near", angle=-50, layer="top"), braid="fly", tail="down"),
        P(dx=4, wings="up", hover=33, tilt=14, head_dy=-5, torso="back", lean=(3, -2), near_arm=(30, -70),
          weapon=dict(hand="near", angle=-80, layer="top"), braid="fly", tail="down", shadow=(14, 2)),
        P(dx=5, wings="up", hover=36, tilt=18, head_dy=-7, torso="back", lean=(4, -3), near_arm=(20, -50),
          weapon=dict(hand="near", angle=-50, layer="top", variant="glint"), braid="fly", tail="down", shadow=(12, 2)),
    ]
    crit_hold = [
        crit_lean[2],
        P(dx=5, wings="mid", hover=36, tilt=18, head_dy=-8, torso="back", lean=(4, -4), near_arm=(20, -50),
          weapon=dict(hand="near", angle=-50, layer="top"), braid="fly", tail="down", shadow=(12, 2),
          effects=[(STAR, "wr_near", 10, -18)]),
    ]
    crit_lunge = [
        # dive
        P(dx=-2, wings="fold", hover=36, tilt=-18, head_dx=-4, head_dy=6, torso="side", lean=(-3, 1), tail="up",
          near_arm=(-20, -100), far_arm=(80, 120), legs="tuck",
          weapon=dict(hand="near", angle=-110, layer="top"), braid="fly", shadow=(12, 2),
          effects=[(dash_lines(3, 16), "pelvis", 14, -12)]),
        P(dx=-8, wings="fold", hover=26, tilt=-24, head_dx=-5, head_dy=8, torso="side", lean=(-4, 1), tail="up",
          near_arm=(120, -150), far_arm=(80, 120), legs="tuck",
          weapon=dict(hand="near", angle=-165, layer="top", variant="blur"), braid="fly", shadow=(18, 2),
          effects=[slash("sh_near", 32, -90, -200, width=8), (dash_lines(3, 18), "pelvis", 16, -10)]),
        # the cleave at the bottom of the dive
        P(dx=-3, wings="down", hover=18, tilt=-10, head_dx=-4, head_dy=4, torso="side", lean=(-4, 2), tail="up",
          near_arm=(172, 195), far_arm=(80, 120), legs="reach",
          weapon=dict(hand="near", angle=160, layer="top"), braid="fly", shadow=(24, 3),
          effects=[slash("sh_near", 32, -160, -200, width=8), (STAR, "wr_near", -22, 8)]),
        P(dx=-4, wings="down", hover=18, tilt=-4, head_dx=-3, head_dy=2, torso="side", lean=(-3, 2), tail="s",
          near_arm=(168, 205), far_arm=(80, 120), legs="reach",
          weapon=dict(hand="near", angle=150, layer="top"), braid="fly", shadow=(24, 3)),
        # pull up
        P(dx=-4, wings="up", hover=24, tilt=6, head_dy=-2, torso="side", lean=(-2, 1), tail="down",
          near_arm=(160, 190), far_arm=(80, 120), legs="hang",
          weapon=dict(hand="near", angle=170, layer="top"), braid="fly", shadow=(18, 2)),
    ]
    crit_recover = [
        P(dx=-7, hover=25, wings="mid", torso="side", lean=(-2, 1), near_arm=(150, 150),
          weapon=dict(hand="near", angle=150, layer="top"), braid="fly"),
        P(dx=-5, hover=26, wings="down", torso="front", lean=(-1, 0), near_arm=(120, 70),
          weapon=dict(hand="near", angle=-30, layer="top")),
        P(dx=-1, hover=26, wings="up"),
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
