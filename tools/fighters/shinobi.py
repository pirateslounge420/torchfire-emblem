"""Shinobi — pure Fire (☲ over ☲, hexagram 30). Kusarigama. Red.

A lean male skirmisher from the same fantasy kingdom as everyone else: short
red hooded cowl (hood up), a dark cloth mask so only the eyes show, fitted red
jacket over a charcoal undershirt and trousers, leather-wrapped forearms, soft
boots. Sickle in the far hand, chain and weight in the near hand.
Drawn original in the GBA FE idiom; faces LEFT.
"""
import math
from pixelkit import Figure, Palette, Part, grid, capsule, blade, arc
from pixelkit.palette import SKIN, OUTLINE, TRIGRAM
from pixelkit.figure import HANDS

NAME = "shinobi"
BOX = 64

# 14 opaque colours. Shared slots: w=E (near-white), M=e (slash edge), n=q
# (steel shadow = charcoal shadow), L=s, j=z (leather shares skin), g=o.
_white = (244, 246, 252)
_charcoal = {"A": (122, 122, 140), "a": (74, 74, 92), "q": (40, 40, 56)}
PALETTE = Palette(NAME, {
    **SKIN,
    **TRIGRAM["fire"],
    **_charcoal,
    "M": (168, 224, 255), "m": (150, 160, 190), "n": _charcoal["q"],
    "L": SKIN["s"], "l": (142, 94, 58), "j": SKIN["z"],
    "w": _white, "E": _white,
    "H": _charcoal["A"], "h": _charcoal["a"], "g": OUTLINE,
})

# --- parts -----------------------------------------------------------------
# Head: hood up, mask over the lower face. Anchor = neck (bottom centre).
HEAD = grid("""
...ccccck.
..Cccccckk
.CCccccckk
.Cccccccck
.Ckkkkkckk
.kSSSskkkk
.kSowSskkk
.kqaaaqkkk
..qaaaaqk.
..qaaaqq..
...qqq....
""", anchor=(5, 11))

HEAD_HURT = grid("""
...ccccck.
..Cccccckk
.CCccccckk
.Cccccccck
.Ckkkkkckk
.kSzzskkkk
.kSoosskkk
.kqaaaqkkk
..qaaaaqk.
..qaaaqq..
...qqq....
""", anchor=(5, 11))

# Torso, anchored at the neck (top centre). Cowl over the shoulders (rows 1-3,
# dark hem on row 4), fitted jacket, leather belt, charcoal trousers at the hips.
TORSO_FRONT = grid("""
....qq....
..Ccccqq..
.CcccccqCc
.Cccccccck
.Ckkkkkkkk
.Cccccckkk
..Cccccckk
..Ccccckk.
..lLLllj..
..Aaaaqq..
.AAaaaaqqq
.Aaaaaqqqq
""", anchor=(5, 0))

TORSO_SIDE = grid("""
...qq...
.Cccck..
.Cccccc.
.Cccccck
.kkkkkk.
.Cccckk.
..ccckk.
..ccckk.
..lLlj..
..aaqq..
.Aaaaqqq
.Aaaaqqq
""", anchor=(4, 0))

TORSO_BACK = grid("""
....qq....
..ccccccc.
.kccccccCc
.kccccccCc
.kkkkkkkkC
.kkcccccCc
..kcccccc.
..kcccccc.
..jllllL..
..qaaaaA..
.qqaaaaaA.
.qqaaaaAA.
""", anchor=(5, 0))

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

# The chain's weight: a 3x3 steel blob, anchored at its centre.
WEIGHT = grid("""
Mmm
mmn
nnn
""", anchor=(1, 1))


def dash_lines(x, y, n=3, length=8):
    p = grid("", anchor=(0, 0))
    for i in range(n):
        yy = y + i * 3
        for k in range(length - i * 2):
            p.pixels[(x + k, yy)] = "e" if k % 3 else "E"
    return p


def chain(pts, weight=True, width=2):
    """Chain links along `pts` (relative to the hand that holds it, which is
    (0, 0)); the weight sits on the last point."""
    p = Part({}, (0, 0))
    for a, b in zip(pts[:-1], pts[1:]):
        p = p.union(capsule(a, b, width, ("M", "m", "n")))
    if weight:
        wx, wy = pts[-1]
        p = p.union(WEIGHT.shifted(round(wx) - 1, round(wy) - 1))
    return p


def hang(end, sag=2, weight=True):
    """A chain that droops from the hand to `end` (relative), sagging by `sag` px."""
    ex, ey = end
    mid = (ex * 0.5, ey * 0.5 + sag)
    return chain([(0, 0), mid, (ex, ey)], weight)


def whirl(r, ang):
    """A taut chain from the hand to a weight circling it at radius r."""
    a = math.radians(ang)
    return chain([(0, 0), (r * math.cos(a), r * math.sin(a))])


def throw_blur(length, y=0):
    """The weight shooting out to the left as a streak: a thin chain under a
    tapered E/e line, the weight at the leading end."""
    p = chain([(0, 0), (-length + 4, y)], weight=False)
    p = p.union(blade((-length - 1, y), (-length + 9, y), width=3, letters=("E", "e", "e"), taper=0.6, edge=None))
    p = p.union(WEIGHT.shifted(-length - 1, y - 1))
    return p


def sickle(angle, variant="normal"):
    """Kusarigama sickle anchored at the grip: 2 px of handle behind the hand,
    5 px of handle beyond it, then a 6 px curved blade set at a right angle,
    hooking toward the foe when the handle points up. A `_rev` suffix on the
    variant mirrors the blade to the other side of the handle."""
    rev = variant.endswith("_rev")
    v = variant[:-4] if rev else variant
    r = math.radians(angle)
    dx, dy = math.cos(r), math.sin(r)
    nx, ny = (-dy, dx) if rev else (dy, -dx)
    hx, hy = 5 * dx, 5 * dy
    p = capsule((round(-2 * dx), round(-2 * dy)), (round(hx), round(hy)), 2, ("L", "l", "j"))
    b0 = (hx, hy)
    b1 = (hx + 4 * nx, hy + 4 * ny)
    b2 = (hx + 6 * nx - 1.5 * dx, hy + 6 * ny - 1.5 * dy)
    if v == "blur":
        t = (hx + 7.5 * nx - 1.5 * dx, hy + 7.5 * ny - 1.5 * dy)
        return p.union(blade(b0, t, width=4, letters=("E", "e", "e"), taper=0.5, edge=None))
    p = p.union(blade(b0, b1, width=2, letters=("M", "m", "n"), taper=0.0, edge="w"))
    p = p.union(blade(b1, b2, width=2, letters=("M", "m", "n"), taper=0.6, edge="w"))
    # a steel ferrule where the blade meets the handle
    p.pixels[(round(hx), round(hy))] = "m"
    if v == "glint":
        gx, gy = round(hx + 3 * nx), round(hy + 3 * ny)
        for ox, oy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
            p.pixels[(gx + ox, gy + oy)] = "E"
    return p


FIGURE = Figure(
    build="lean", arm_w=4, leg_w=4,
    parts={"heads": {"normal": HEAD, "hurt": HEAD_HURT},
           "torsos": {"front": TORSO_FRONT, "side": TORSO_SIDE, "back": TORSO_BACK},
           "extras": {"star": STAR, "spark": SPARK}},
    sleeves=("C", "c", "k"),
    pants=("A", "a", "q"),
    weapon=sickle,
)

RX = 36   # resting root x; the opponent is to the left


def _wraps(pose):
    """Leather forearm wraps: a capsule from the elbow to the wrist drawn over
    each sleeve, with the hand re-drawn on top so it stays skin."""
    J = FIGURE.joints(pose)
    out = []
    for side in ("near", "far"):
        if pose.get(f"{side}_arm", (90, 90)) is None:
            continue
        el, wr = J[f"el_{side}"], J[f"wr_{side}"]
        vx, vy = wr[0] - el[0], wr[1] - el[1]
        L = math.hypot(vx, vy) or 1.0
        ux, uy = vx / L, vy / L
        a = (el[0] - wr[0] + 1.5 * ux, el[1] - wr[1] + 1.5 * uy)
        b = (-0.5 * ux, -0.5 * uy)
        w = pose.get("arm_w", FIGURE.b["arm_w"])
        out.append((capsule(a, b, w, ("L", "l", "j")), f"wr_{side}", 0, 0, f"{side}_arm"))
        hv = pose.get(f"{side}_hand", "fist")
        if hv:
            hp = HANDS[hv]
            hx, hy = pose.get(f"{side}_hand_off", (0, 0))
            out.append((hp, f"wr_{side}", hx, hy, f"{side}_arm"))
    return out


DEFAULT = object()   # sentinel: "use the resting chain"


def P(dx=0, chain_part=DEFAULT, chain_at="wr_near", chain_layer="top", **kw):
    """Base pose: a low ready stance, sickle hanging behind the far hip, the
    chain in the near hand with the weight dangling in front of the shins.
    chain_part: a Part from chain()/hang()/whirl(), None for no chain."""
    base = dict(
        root=(RX + dx, 38), torso="front", head="normal", lean=(-1, 0),
        near_arm=(120, 110), far_arm=(75, 95),
        near_leg=(118, 98), far_leg=(62, 88),
        near_boot="side", far_boot="front",
        near_hand="grip", far_hand="grip",
        weapon=dict(hand="far", angle=60, layer="top"),
        shadow=(9, 2),
        extras=[],
    )
    base.update(kw)
    if chain_part is DEFAULT:
        chain_part = hang((-3, 8), sag=1)
    if chain_part is not None:
        base["extras"] = list(base["extras"]) + [(chain_part, chain_at, 0, 0, chain_layer)]
    base["extras"] = list(base["extras"]) + _wraps(base)
    return base


def slash(joint, r, a0, a1, width=5, dx=0, dy=0):
    """A slash arc effect centred on a joint (usually the far shoulder, the pivot)."""
    return (arc((0, 0), r - width, r, a0, a1), joint, dx, dy)


def ring(joint, r, a0, a1, width=2, dx=0, dy=0):
    """A thin whirl trail around a joint (the near wrist when the weight spins)."""
    return (arc((0, 0), r - width, r, a0, a1, letters=("e", "e"), taper=False), joint, dx, dy)


def animations():
    idle = [
        P(chain_part=hang((-4, 8), sag=1)),
        P(lean=(-1, 1), near_arm=(120, 112), far_arm=(75, 97), chain_part=hang((-3, 8), sag=1),
          weapon=dict(hand="far", angle=62, layer="top")),
        P(lean=(-1, 1), head_off=(0, 1), near_arm=(120, 114), far_arm=(76, 99), chain_part=hang((-2, 8), sag=1),
          weapon=dict(hand="far", angle=64, layer="top")),
        P(lean=(-1, 1), near_arm=(120, 112), far_arm=(75, 97), chain_part=hang((-3, 8), sag=1),
          weapon=dict(hand="far", angle=62, layer="top")),
    ]

    # --- regular attack: crouch, whirl the weight, whip it out, yank, sickle up ---
    lean = [
        P(dx=1, torso="front", lean=(0, 0), near_arm=(150, 60), far_arm=(20, -50),
          near_leg=(120, 100), far_leg=(60, 86),
          weapon=dict(hand="far", angle=-70, layer="top"),
          chain_part=whirl(5, 120),
          effects=[ring("wr_near", 6, 40, 120)]),
        P(dx=3, torso="back", lean=(1, 1), near_arm=(160, 20), far_arm=(5, -75),
          near_leg=(118, 100), far_leg=(55, 84),
          weapon=dict(hand="far", angle=-80, layer="top"),
          chain_part=whirl(6, 200),
          effects=[ring("wr_near", 7, 80, 200)]),
        P(dx=4, torso="back", lean=(2, 2), near_arm=(165, 0), far_arm=(-10, -95),
          near_leg=(116, 102), far_leg=(50, 80),
          weapon=dict(hand="far", angle=-85, layer="top"),
          chain_part=whirl(6, 280),
          effects=[ring("wr_near", 7, 150, 280)]),
    ]
    hold = [
        lean[2],
        P(dx=4, torso="back", lean=(2, 1), near_arm=(165, 0), far_arm=(-12, -97),
          near_leg=(116, 102), far_leg=(50, 80),
          weapon=dict(hand="far", angle=-87, layer="top"),
          chain_part=whirl(6, 320),
          effects=[ring("wr_near", 7, 190, 320)]),
    ]
    lunge = [
        # the weight shoots out toward the foe
        P(dx=-3, torso="side", lean=(-2, 0), near_arm=(165, 150), far_arm=(0, -90),
          near_leg=(138, 100), far_leg=(50, 80), far_boot="back",
          weapon=dict(hand="far", angle=-85, layer="top"),
          chain_part=throw_blur(16, -1)),
        # impact: chain taut, weight at full extension
        P(dx=-6, torso="side", lean=(-3, 1), near_arm=(160, 165), far_arm=(10, -80),
          near_leg=(150, 98), far_leg=(40, 70), far_boot="back",
          weapon=dict(hand="far", angle=-80, layer="top"),
          chain_part=chain([(0, 0), (-18, -1)]),
          effects=[(SPARK, "wr_near", -21, -1)]),
        # yank back: the weight flies home, sickle raised
        P(dx=-6, torso="side", lean=(-2, 0), near_arm=(120, 40), far_arm=(-40, -120),
          near_leg=(148, 98), far_leg=(42, 72), far_boot="back",
          weapon=dict(hand="far", angle=-120, layer="top"),
          chain_part=chain([(0, 0), (-7, 4), (-13, 3)]),
          effects=[ring("wr_near", 14, 150, 200, width=2)]),
    ]
    recover = [
        P(dx=-5, torso="side", lean=(-2, 1), near_arm=(130, 70), far_arm=(0, -60),
          near_leg=(142, 98), far_leg=(45, 75), far_boot="back",
          weapon=dict(hand="far", angle=-60, layer="top"),
          chain_part=hang((-5, 5), sag=2)),
        P(dx=-3, torso="front", lean=(-1, 0), near_arm=(125, 100), far_arm=(50, 60),
          near_leg=(125, 98), far_leg=(55, 85),
          weapon=dict(hand="far", angle=20, layer="top"),
          chain_part=hang((-3, 7), sag=1)),
        P(dx=-1),
    ]

    # --- defence: sickle up in front, chain pulled taut across it ---------------
    def guard(dx, lean_, legs=None, crouch=0):
        pose = P(dx=dx, lean=lean_, torso="front", far_arm=(165, -110), near_arm=(135, -60),
                 weapon=dict(hand="far", angle=-95, layer="top"),
                 **(legs or {}))
        return pose

    block = [
        P(dx=1, lean=(0, 0), torso="front", far_arm=(165, -110), near_arm=(140, -40),
          weapon=dict(hand="far", angle=-95, layer="top"),
          chain_part=chain([(0, 0), (6, -8), (7, -2)])),
        P(dx=2, lean=(1, 1), torso="front", far_arm=(165, -110), near_arm=(140, -40),
          near_leg=(122, 100), far_leg=(58, 84),
          weapon=dict(hand="far", angle=-95, layer="top"),
          chain_part=chain([(0, 0), (6, -8), (7, -2)])),
    ]
    parry = [
        P(dx=1, lean=(0, 0), torso="front", far_arm=(165, -110), near_arm=(140, -40),
          weapon=dict(hand="far", angle=-95, layer="top"),
          chain_part=chain([(0, 0), (6, -8), (7, -2)])),
        # the chain whips outward and catches the blow
        P(dx=-1, torso="side", lean=(-2, 0), far_arm=(160, -120), near_arm=(170, -110),
          weapon=dict(hand="far", angle=-100, layer="top"),
          chain_part=whirl(8, 200),
          effects=[ring("wr_near", 10, 120, 210, width=3)]),
        P(dx=-2, torso="side", lean=(-2, 0), far_arm=(160, -120), near_arm=(175, -120),
          weapon=dict(hand="far", angle=-100, layer="top"),
          chain_part=whirl(8, 220),
          effects=[(SPARK, "wr_near", -7, -7)]),
    ]
    hit = [
        P(dx=3, head="hurt", lean=(2, 1), head_off=(1, 0), torso="front",
          near_arm=(115, 55), far_arm=(40, 80), near_hand="open",
          near_leg=(105, 95), far_leg=(70, 95),
          weapon=dict(hand="far", angle=70, layer="top"),
          chain_part=hang((-6, 7), sag=2)),
        P(dx=2, head="hurt", lean=(2, 1), head_off=(1, 1), torso="front",
          near_arm=(120, 60), far_arm=(45, 85), near_hand="open",
          near_leg=(110, 95), far_leg=(65, 92),
          weapon=dict(hand="far", angle=65, layer="top"),
          chain_part=hang((-7, 8), sag=2)),
    ]
    # Stagger (kusarigama): tangled in his own chain — stumbles back, drops to
    # a crouch on one hand, the chain trailing on the ground.
    tangle = chain([(-7, 7), (3, 10), (-6, 13), (2, 16)], weight=False)
    stagger = [
        P(dx=6, head="hurt", lean=(3, 1), head_off=(1, 0), torso="front",
          near_arm=(140, 30), far_arm=(30, -30), near_hand="open",
          near_leg=(130, 108), far_leg=(45, 60), far_boot="back",
          weapon=dict(hand="far", angle=-20, layer="top"),
          chain_part=chain([(0, 0), (-4, 6), (-9, 13), (-6, 18)]),
          extras=[(tangle, "pelvis", 0, 0, "front")]),
        P(dx=5, head="hurt", lean=(1, 2), head_off=(0, 1), torso="front", planted=False, root=(RX + 5, 45),
          near_arm=(105, 85), near_fore_len=7, far_arm=(130, 100), near_hand="open",
          near_leg=(170, 110), near_shin_len=5, far_leg=(75, 0), far_shin_len=6, far_boot="back", far_boot_off=(0, -2),
          shadow=(10, 2),
          weapon=dict(hand="far", angle=150, layer="top"),
          chain_part=chain([(2, 2), (-6, 3), (-13, 2), (-18, 3)]), chain_at="wr_near", chain_layer="front",
          extras=[(chain([(-8, 10), (0, 13), (-7, 15)], weight=False), "pelvis", 0, 0, "front")]),
        P(dx=4, head="normal", lean=(0, 1), torso="front", planted=False, root=(RX + 4, 42),
          near_arm=(130, 70), far_arm=(110, 120), near_hand="grip",
          near_leg=(150, 105), near_shin_len=6, far_leg=(70, 20), far_shin_len=6, far_boot="back", far_boot_off=(0, -2),
          shadow=(10, 2),
          weapon=dict(hand="far", angle=135, layer="top"),
          chain_part=chain([(0, 0), (-6, 6), (-12, 9)])),
    ]

    # --- dodges ----------------------------------------------------------------
    dodge_up = [
        P(dx=0, lean=(-1, 2), near_leg=(132, 105), far_leg=(48, 75), near_arm=(120, 100), far_arm=(60, 110),
          weapon=dict(hand="far", angle=60, layer="top"), chain_part=hang((-3, 7), sag=1)),
        P(dx=-1, planted=False, root=(RX - 1, 24), lean=(-1, 0), shadow=(6, 1),
          near_leg=(190, 115), far_leg=(165, 100), near_boot="tip", far_boot="tip",
          near_arm=(140, 70), far_arm=(40, 100),
          weapon=dict(hand="far", angle=50, layer="top"), chain_part=chain([(0, 0), (-2, 6), (-1, 12)])),
    ]
    dodge_down = [
        P(dx=0, lean=(-2, 2), near_leg=(135, 100), far_leg=(45, 80), near_arm=(120, 100), far_arm=(50, 100),
          weapon=dict(hand="far", angle=50, layer="top"), chain_part=hang((-3, 7), sag=1)),
        P(dx=0, lean=(-3, 3), head_off=(-1, 1), near_leg=(165, 100), far_leg=(15, 85), near_arm=(150, 100), far_arm=(30, 110),
          far_boot="back",
          weapon=dict(hand="far", angle=20, layer="top"), chain_part=chain([(0, 0), (-4, 4), (-9, 5)])),
    ]
    dodge_forward = [
        P(dx=-6, torso="side", lean=(-3, 2), near_leg=(150, 95), far_leg=(60, 100), near_arm=(130, 60), far_arm=(40, 100),
          weapon=dict(hand="far", angle=40, layer="top"), chain_part=hang((3, 6), sag=1),
          effects=[(dash_lines(0, 0, 2, 7), "pelvis", 12, -3)]),
        P(dx=-10, torso="side", lean=(-3, 2), near_leg=(145, 100), far_leg=(65, 95), near_arm=(125, 70), far_arm=(45, 95),
          weapon=dict(hand="far", angle=45, layer="top"), chain_part=hang((4, 6), sag=1),
          effects=[(dash_lines(0, 0, 3, 9), "pelvis", 10, -5)]),
    ]
    dodge_back = [
        P(dx=6, lean=(2, 0), near_leg=(100, 80), far_leg=(60, 100), near_arm=(120, 60), far_arm=(60, 100),
          weapon=dict(hand="far", angle=70, layer="top"), chain_part=hang((-6, 5), sag=2),
          effects=[(dash_lines(0, 0, 2, 7), "pelvis", -16, 6)]),
        P(dx=10, lean=(1, 0), near_leg=(130, 95), far_leg=(70, 90), near_arm=(120, 80), far_arm=(60, 100),
          weapon=dict(hand="far", angle=75, layer="top"), chain_part=hang((-5, 7), sag=1)),
    ]

    # --- critical: spin the weight overhead, leap, whip, double sickle cut ------
    crit_lean = [
        P(dx=2, torso="back", lean=(1, 0), near_arm=(-135, -110), far_arm=(20, 10),
          near_leg=(115, 98), far_leg=(58, 86),
          weapon=dict(hand="far", angle=10, layer="top"),
          chain_part=whirl(6, -150),
          effects=[ring("wr_near", 7, -60, -150)]),
        P(dx=4, torso="back", lean=(2, 1), near_arm=(-135, -110), far_arm=(15, 0),
          near_leg=(125, 100), far_leg=(50, 80),
          weapon=dict(hand="far", angle=0, layer="top"),
          chain_part=whirl(8, -200),
          effects=[ring("wr_near", 9, -40, -200)]),
        P(dx=5, torso="back", lean=(3, 2), head_off=(-1, 0), near_arm=(-135, -110), far_arm=(10, -5),
          near_leg=(135, 102), far_leg=(45, 75),
          weapon=dict(hand="far", angle=-8, layer="top", variant="glint"),
          chain_part=whirl(9, -230),
          effects=[ring("wr_near", 10, -20, -230, width=3)]),
    ]
    crit_hold = [
        crit_lean[2],
        P(dx=5, torso="back", lean=(3, 2), head_off=(-1, 0), near_arm=(-135, -110), far_arm=(10, -5),
          near_leg=(135, 102), far_leg=(45, 75),
          weapon=dict(hand="far", angle=-8, layer="top"),
          chain_part=whirl(9, -250),
          effects=[ring("wr_near", 10, -40, -250, width=3), (STAR, "wr_near", -6, -7)]),
    ]
    crit_lunge = [
        # leap: the weight whips round in a 270° arc
        P(dx=-6, planted=False, root=(RX - 6, 28), lean=(-2, -1), shadow=(6, 1),
          near_arm=(-150, -120), far_arm=(20, -20), near_leg=(75, 118), far_leg=(50, 100),
          near_boot="tip", far_boot="tip",
          weapon=dict(hand="far", angle=-20, layer="top"),
          chain_part=whirl(10, 200),
          effects=[ring("wr_near", 12, -70, 200, width=4)]),
        # landing + first sickle cut (blur, downward)
        P(dx=-9, torso="side", lean=(-3, 0), far_arm=(-60, -140), near_arm=(150, 120),
          near_leg=(135, 100), far_leg=(50, 80), far_boot="back",
          weapon=dict(hand="far", angle=-160, layer="top", variant="blur"),
          chain_part=hang((-2, 6), sag=1),
          effects=[slash("sh_far", 24, -60, -200, width=6)]),
        # impact: full extension, the hook bites
        P(dx=-11, torso="side", lean=(-3, 1), far_arm=(178, 178), near_arm=(160, 110),
          near_leg=(150, 98), far_leg=(40, 70), far_boot="back",
          weapon=dict(hand="far", angle=185, layer="top"),
          chain_part=hang((-2, 6), sag=1),
          effects=[slash("sh_far", 26, -110, -185, width=7), (STAR, "wr_far", -7, 5)]),
        # second cut: rising (blur)
        P(dx=-11, torso="side", lean=(-3, 1), far_arm=(195, 230), near_arm=(160, 110),
          near_leg=(150, 98), far_leg=(40, 70), far_boot="back",
          weapon=dict(hand="far", angle=-125, layer="top", variant="blur_rev"),
          chain_part=hang((-2, 6), sag=1),
          effects=[slash("sh_far", 24, 160, 250, width=6)]),
        # follow-through: sickle high
        P(dx=-11, torso="side", lean=(-3, 1), far_arm=(-120, -100), near_arm=(160, 110),
          near_leg=(152, 100), far_leg=(38, 68), far_boot="back",
          weapon=dict(hand="far", angle=-100, layer="top"),
          chain_part=hang((-2, 6), sag=1)),
    ]
    crit_recover = [
        P(dx=-9, torso="side", lean=(-2, 1), far_arm=(-60, -60), near_arm=(140, 100),
          near_leg=(140, 98), far_leg=(45, 75), far_boot="back",
          weapon=dict(hand="far", angle=-60, layer="top"),
          chain_part=hang((-3, 7), sag=1)),
        P(dx=-4, torso="front", lean=(-1, 0), far_arm=(50, 60), near_arm=(125, 100),
          near_leg=(125, 98), far_leg=(55, 85),
          weapon=dict(hand="far", angle=20, layer="top"),
          chain_part=hang((-3, 7), sag=1)),
        P(dx=-1),
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
