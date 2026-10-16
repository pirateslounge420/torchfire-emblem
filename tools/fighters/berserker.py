"""Berserker — pure Thunder (☳ over ☳, hexagram 51). Axe. Cyan.

A big bare-armed axeman: sleeveless cyan jerkin open over a bare chest, cyan
head-scarf knotted at the back (the tail whips), dark stubble, baggy dark
trousers tucked into boots, leather belt with a big buckle, leather bracers.
Heavy build, ~42 px tall. One-handed bearded axe in the far hand: overhead
chops; the critical is a full windmill spin into the chop.
Drawn original in the GBA FE idiom; faces LEFT.
"""
import math
from pixelkit import Figure, Palette, Part, grid, capsule, blade, arc, rot90_part, flip_part
from pixelkit.palette import SKIN_TAN, OUTLINE, TRIGRAM
from pixelkit.figure import HANDS

NAME = "berserker"
BOX = 64

# 15 opaque colours. Shared slots: L=z (dark leather highlight = skin shadow),
# j=h=H (leather shadow = hair, one tone), q=n (accent shadow = steel shadow),
# e=C (slash edge = cloth highlight), w=E (white), g=o (hair shadow = outline).
_cyan = TRIGRAM["thunder"]
_teal = {"A": (104, 126, 138), "a": (66, 84, 98), "q": (44, 54, 74)}
_hair = (52, 40, 44)
PALETTE = Palette(NAME, {
    **SKIN_TAN,
    "H": _hair, "h": _hair, "g": OUTLINE,
    **_cyan,
    "e": _cyan["C"],
    **_teal,
    "M": (204, 214, 236), "m": (150, 164, 190), "n": _teal["q"],
    "L": SKIN_TAN["z"], "l": (104, 66, 40), "j": _hair,
})

# --- parts -----------------------------------------------------------------
# Head, 3/4 view facing left, bandana knotted at the back. Anchor = neck.
HEAD = grid("""
...ccccc..
..CCccccc.
.CCcccccck
.Cccccccck
.kkkkkkkkh
.sSSSsszhh
.SSowSsszh
.SSsSssszz
.zsssszzz.
.zzsszzzz.
..zzzzzz..
...zzzz...
""", anchor=(5, 12))

HEAD_HURT = grid("""
...ccccc..
..CCccccc.
.CCcccccck
.Cccccccck
.kkkkkkkkh
.sSSSsszhh
.SSozSsszh
.SSsSssszz
.zwwwszzz.
.zzsszzzz.
..zzzzzz..
...zzzz...
""", anchor=(5, 12))

# Bandana tail; anchor = where it leaves the knot at the back of the head.
TAIL = {
    "rest": grid("""
cc..
.cck
..ck
..ck
...k
""", anchor=(0, 0)),
    "back": grid("""
ccc..
..cck
....k
""", anchor=(0, 0)),
    "up": grid("""
...k
..ck
.cc.
cc..
""", anchor=(0, 3)),
    "fwd": grid("""
.cc
cck
c..
""", anchor=(2, 0)),
}

# Torso, anchored at the neck (top centre). 12 wide, 13 tall: rows 0-8 chest
# (open jerkin, bare chest), row 9 belt + buckle, rows 10-12 trousers/hips.
TORSO_FRONT = grid("""
.....ss.....
..CCsSsscc..
.CCcsSssscck
.CCcsSzsscck
CCccsSzsskkk
CCcccSzsskkk
CCccczzsckkk
.Ccccczcckkk
.Cccccccckkk
.lLLMMLllj..
.AAaaaaaqqq.
.AAaaaaaqqq.
..Aaaaaaqq..
""", anchor=(6, 0))

TORSO_SIDE = grid("""
...ss...
.SSsckk.
SSsscckk
SSsscckk
Ssszckkk
Ssszckkk
.sszckk.
.sszckk.
.sszckk.
.LMMllj.
.Aaaaqq.
.Aaaaqq.
..aaaq..
""", anchor=(4, 0))

TORSO_BACK = grid("""
.....ss.....
..cccsscCC..
.kccccsccCC.
.kkccccccCCC
kkkcccccccCC
kkkcccccccCC
kkkcccccccC.
.kkccccccCC.
.kkcccccccC.
.jllLLMMLL..
.qqaaaaaAA..
.qqaaaaaAA..
..qaaaaaA...
""", anchor=(6, 0))

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

# Ground dust kicked up by the chop; anchor = the impact point on the ground.
DUST = grid("""
e.....e
.e.E.e.
..eEe..
E..e..E
""", anchor=(3, 3))


def dash_lines(x, y, n=3, length=8):
    p = grid("", anchor=(0, 0))
    for i in range(n):
        yy = y + i * 3
        for k in range(length - i * 2):
            p.pixels[(x + k, yy)] = "e" if k % 3 else "E"
    return p


# --- the axe ---------------------------------------------------------------
# Bearded axe head authored at 0 deg (haft pointing right, blade on top) and
# 45 deg (haft pointing down-right, blade up-right). The blade is always on the
# LEFT of the grip->tip direction, so an overhead-raised axe (-90) faces the
# foe. Anchor = the socket, 8 px along an 11-px haft. 'm' is the body (shaded
# procedurally after rotation so the light stays upper-left), 'w' the edge.
_HEAD_0 = grid("""
...www..
..wmmmw.
.wmmmmmw
wmmmmmmm
mmmmmmmm
....mmmm
....mmmm
....mmmm
""", anchor=(4, 6))

_HEAD_45 = grid("""
...www...
.wmmmmw..
.mmmmmmw.
..mmmmmmw
...mmmmmw
..mmmmmmm
..mmmmmm.
...mmmm..
....mm...
""", anchor=(2, 6))


def _reshade(p):
    """Light from the upper-left: body pixels on a left/top edge -> M, on a
    right/bottom edge -> n, otherwise m. Edge ('w') pixels are kept."""
    px = p.pixels
    out = {}
    for (x, y), c in px.items():
        if c != "m":
            out[(x, y)] = c
            continue
        score = ((x - 1, y) not in px) + ((x, y - 1) not in px) \
            - ((x + 1, y) not in px) - ((x, y + 1) not in px)
        out[(x, y)] = "M" if score > 0 else ("n" if score < 0 else "m")
    return Part(out, p.anchor)


_HEADS = {}
for _k in range(4):
    _HEADS[(_k * 90) % 360] = _reshade(rot90_part(_HEAD_0, _k))
    _HEADS[(45 + _k * 90) % 360] = _reshade(rot90_part(_HEAD_45, _k))

HAFT = 11


def haft(a, b, letters=("L", "l", "j")):
    """A true 2-px shaft: the capsule's centre line is nudged half a pixel
    toward the blade side (left of travel) so axis-aligned hafts are 2 px."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy) or 1.0
    sx, sy = 0.5 * dy / L, -0.5 * dx / L
    return capsule((a[0] + sx, a[1] + sy), (b[0] + sx, b[1] + sy), 1.8, letters)


def axe(angle, variant="normal"):
    """Axe anchored at the grip. The haft/head snap to the nearest 45 deg; the
    blur smear uses the exact angle."""
    r = math.radians(angle)
    dx, dy = math.cos(r), math.sin(r)
    if variant == "blur":
        p = blade((round(2 * dx), round(2 * dy)), (round(12 * dx), round(12 * dy)), width=4,
                  letters=("E", "e", "e"), taper=0.2, edge=None)
        q = blade((round(6 * dx), round(6 * dy)), (round(14 * dx), round(14 * dy)), width=8,
                  letters=("E", "e", "e"), taper=0.55, edge=None)
        return p.union(q)
    a = (round(angle / 45.0) * 45) % 360
    r = math.radians(a)
    dx, dy = math.cos(r), math.sin(r)
    p = haft((0, 0), (round(HAFT * dx), round(HAFT * dy)))
    hx, hy = round(8 * dx), round(8 * dy)
    head = _HEADS[a]
    for (x, y), c in head.pixels.items():
        p.pixels[(x - head.anchor[0] + hx, y - head.anchor[1] + hy)] = c
    if variant == "glint":
        # sparkle on the cutting edge (perpendicular, blade side = left of travel)
        gx, gy = round(8 * dx + 6 * dy), round(8 * dy - 6 * dx)
        for ox, oy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
            p.pixels[(gx + ox, gy + oy)] = "E"
    return p


def axe_tip(angle):
    """Where the blade bites, relative to the grip (for STAR / dust effects)."""
    a = (round(angle / 45.0) * 45) % 360
    r = math.radians(a)
    dx, dy = math.cos(r), math.sin(r)
    return (round(8 * dx + 5 * dy), round(8 * dy - 5 * dx))


def bracer(fore_angle, w=6, back=5, front=2):
    """Leather cuff across the forearm just behind the wrist (a square band,
    not a capsule, so it stays short). Anchor = wrist."""
    r = math.radians(fore_angle)
    dx, dy = math.cos(r), math.sin(r)
    return blade((-back * dx, -back * dy), (-front * dx, -front * dy), width=w,
                 letters=("L", "l", "j"), taper=0.0, edge=None)


FIGURE = Figure(
    build="heavy", arm_w=5, leg_w=6,
    parts={"heads": {"normal": HEAD, "hurt": HEAD_HURT},
           "torsos": {"front": TORSO_FRONT, "side": TORSO_SIDE, "back": TORSO_BACK},
           "extras": {**{"tail_" + k: v for k, v in TAIL.items()},
                      "star": STAR, "spark": SPARK, "dust": DUST}},
    sleeves=("S", "s", "z"),
    pants=("A", "a", "q"),
    weapon=axe,
)

RX = 36   # resting root x; the opponent is to the left


def P(dx=0, tail="rest", hand_front=True, **kw):
    """Base pose: wide ready stance, axe resting on the far shoulder.
    hand_front draws a copy of the far (axe) hand over the torso so the grip
    stays visible when the far arm is behind the body."""
    base = dict(
        root=(RX + dx, 38), torso="front", torso_h=13, head="normal", lean=(-1, 0),
        near_arm=(100, 80), far_arm=(80, -105),
        near_leg=(122, 100), far_leg=(58, 86),
        near_boot="side", far_boot="front",
        weapon=dict(hand="far", angle=-45, layer="top"),
        shadow=(11, 2),
    )
    base.update(kw)
    extras = list(base.pop("extras", []))
    extras.append(("tail_" + tail, "neck", 4, -9, "back"))
    if hand_front:
        extras.append((HANDS["grip"], "wr_far", 0, 0, "front"))
    # bracers on both forearms
    for side in ("near", "far"):
        arm = base.get(f"{side}_arm")
        if arm is not None:
            extras.append((bracer(arm[1]), f"wr_{side}", 0, 0, f"{side}_arm"))
    base["extras"] = extras
    return base


def slash(joint, r, a0, a1, width=5, dx=0, dy=0):
    """A slash arc effect centred on a joint (usually the far shoulder, the pivot)."""
    return (arc((0, 0), r - width, r, a0, a1), joint, dx, dy)


def tipfx(part, angle, dx=0, dy=0):
    """An effect placed where the blade bites (relative to the far wrist)."""
    tx, ty = axe_tip(angle)
    return (part, "wr_far", tx + dx, ty + dy)


def animations():
    idle = [
        P(),
        P(lean=(-1, 1), near_arm=(100, 82), far_arm=(80, -103)),
        P(lean=(-1, 1), head_off=(0, 1), near_arm=(100, 84), far_arm=(81, -101),
          weapon=dict(hand="far", angle=-45, layer="top", off=(0, 1))),
        P(lean=(-1, 1), near_arm=(100, 82), far_arm=(80, -103)),
    ]

    # --- regular attack: raise the axe high behind the head, overhead chop ---
    lean = [
        P(dx=1, torso="front", lean=(0, 0), far_arm=(30, -70), near_arm=(120, 70),
          weapon=dict(hand="far", angle=-90, layer="top"), tail="back"),
        P(dx=3, torso="back", lean=(1, 0), far_arm=(-20, -90), near_arm=(135, 90),
          near_leg=(115, 96), far_leg=(52, 82),
          weapon=dict(hand="far", angle=-45, layer="top"), tail="back"),
        P(dx=4, torso="back", lean=(2, 0), far_arm=(-50, -110), near_arm=(145, 100),
          near_leg=(112, 96), far_leg=(50, 80),
          weapon=dict(hand="far", angle=0, layer="top"), tail="back"),
    ]
    hold = [
        lean[2],
        P(dx=4, torso="back", lean=(2, -1), far_arm=(-52, -112), near_arm=(145, 100),
          near_leg=(112, 96), far_leg=(50, 80),
          weapon=dict(hand="far", angle=0, layer="top"), tail="back"),
    ]
    lunge = [
        # blur: the axe arcs overhead toward the foe
        P(dx=-3, torso="side", lean=(-2, 0), far_arm=(-80, -120), near_arm=(150, 120),
          near_leg=(135, 100), far_leg=(48, 78), tail="up",
          weapon=dict(hand="far", angle=-140, layer="top", variant="blur"),
          effects=[slash("sh_far", 26, -10, -200, width=7)]),
        # impact: the axe buried low in front at the foe's feet
        P(dx=-10, torso="side", lean=(-4, 2), far_arm=(150, 115), near_arm=(165, 110),
          near_leg=(150, 98), far_leg=(38, 68), far_boot="back", tail="back",
          weapon=dict(hand="far", angle=135, layer="top"),
          effects=[slash("sh_far", 27, -120, -195, width=7),
                   tipfx(STAR, 135), tipfx(DUST, 135, 0, 3)]),
        # follow-through: the body settles over the buried axe
        P(dx=-10, torso="side", lean=(-4, 3), head_off=(0, 1), far_arm=(150, 118), near_arm=(160, 115),
          near_leg=(150, 98), far_leg=(38, 68), far_boot="back", tail="back",
          weapon=dict(hand="far", angle=135, layer="top"),
          effects=[tipfx(DUST, 135, -1, 2)]),
    ]
    recover = [
        # haul the axe back up
        P(dx=-7, torso="side", lean=(-2, 1), far_arm=(160, 170), near_arm=(140, 100),
          near_leg=(140, 98), far_leg=(45, 75), far_boot="back", tail="back",
          weapon=dict(hand="far", angle=180, layer="top")),
        P(dx=-3, torso="front", lean=(-1, 0), far_arm=(120, 20), near_arm=(110, 85),
          near_leg=(125, 98), far_leg=(55, 85),
          weapon=dict(hand="far", angle=-90, layer="top")),
        P(dx=-1),
    ]

    # --- defence -------------------------------------------------------------
    guard = dict(torso="front", far_arm=(150, -95), near_arm=(175, -25), near_hand="grip",
                 weapon=dict(hand="far", angle=180, layer="top"))
    block = [
        P(dx=1, lean=(0, 0), **guard),
        P(dx=2, lean=(1, 1), near_leg=(126, 102), far_leg=(54, 82), **guard),
    ]
    parry = [
        P(dx=1, torso="front", far_arm=(150, -95), near_arm=(175, -25), near_hand="grip",
          weapon=dict(hand="far", angle=-90, layer="top")),
        P(dx=-1, torso="side", lean=(-2, 0), far_arm=(165, -140), near_arm=(140, -60), near_hand="open",
          weapon=dict(hand="far", angle=-135, layer="top", variant="blur"),
          effects=[slash("wr_far", 16, -90, -180, width=4)]),
        # shoulder-check: drives the near shoulder into the foe
        P(dx=-4, torso="side", lean=(-4, 1), far_arm=(60, 0), near_arm=(120, 160), near_hand="fist",
          near_leg=(150, 98), far_leg=(40, 70), far_boot="back", tail="back",
          weapon=dict(hand="far", angle=-45, layer="top"),
          effects=[(SPARK, "sh_near", -4, 0)]),
    ]
    hit = [
        P(dx=3, head="hurt", lean=(2, 1), head_off=(1, 0), torso="front",
          near_arm=(115, 55), far_arm=(60, -80), near_hand="open",
          near_leg=(108, 95), far_leg=(70, 95), tail="fwd",
          weapon=dict(hand="far", angle=-45, layer="top")),
        P(dx=2, head="hurt", lean=(2, 1), head_off=(1, 1), torso="front",
          near_arm=(120, 60), far_arm=(65, -75), near_hand="open",
          near_leg=(112, 95), far_leg=(65, 92), tail="fwd",
          weapon=dict(hand="far", angle=-45, layer="top")),
    ]
    # Stagger (axe): reels back, the axe head drops to the ground and he leans
    # on the haft, head down; then half rises.
    stagger = [
        P(dx=6, head="hurt", lean=(3, 1), head_off=(1, 0), torso="front",
          near_arm=(130, 40), far_arm=(20, -60), near_hand="open",
          near_leg=(130, 108), far_leg=(45, 60), far_boot="back", tail="fwd",
          weapon=dict(hand="far", angle=-45, layer="top")),
        P(dx=5, head="hurt", lean=(-3, 4), head_off=(-1, 2), torso="front",
          near_arm=(125, 95), far_arm=(145, 110), near_hand="open",
          near_leg=(140, 102), far_leg=(50, 70), far_boot="back", tail="fwd",
          weapon=dict(hand="far", angle=135, layer="top")),
        P(dx=4, head="normal", lean=(-2, 2), head_off=(0, 1), torso="front",
          near_arm=(115, 85), far_arm=(140, 105), near_hand="fist",
          near_leg=(130, 100), far_leg=(55, 78), far_boot="front", tail="rest",
          weapon=dict(hand="far", angle=135, layer="top")),
    ]

    # --- dodges ----------------------------------------------------------------
    dodge_up = [
        P(dx=0, lean=(-1, 2), near_leg=(135, 105), far_leg=(45, 75), near_arm=(110, 100), far_arm=(70, -90),
          weapon=dict(hand="far", angle=-45, layer="top")),
        P(dx=-1, planted=False, root=(RX - 1, 25), lean=(-1, 0), shadow=(6, 1),
          near_leg=(190, 115), far_leg=(165, 100), near_boot="tip", far_boot="tip",
          near_arm=(130, 60), far_arm=(50, -100), tail="up",
          weapon=dict(hand="far", angle=-45, layer="top")),
    ]
    dodge_down = [
        P(dx=0, lean=(-2, 2), near_leg=(135, 100), far_leg=(45, 80), near_arm=(110, 90), far_arm=(75, -95),
          weapon=dict(hand="far", angle=-45, layer="top")),
        P(dx=0, lean=(-3, 4), head_off=(-1, 1), near_leg=(165, 100), far_leg=(15, 85), near_arm=(150, 100),
          far_arm=(60, -70), far_boot="back", tail="up",
          weapon=dict(hand="far", angle=-45, layer="top")),
    ]
    dodge_forward = [
        P(dx=-6, torso="side", lean=(-2, 0), near_leg=(145, 95), far_leg=(65, 100), near_arm=(120, 90),
          far_arm=(80, -100), tail="back", weapon=dict(hand="far", angle=-45, layer="top"),
          effects=[(dash_lines(0, 0, 2, 7), "pelvis", 13, -3)]),
        P(dx=-10, torso="front", lean=(-1, 0), near_leg=(112, 95), far_leg=(78, 95), near_arm=(100, 85),
          far_arm=(80, -105), tail="back", weapon=dict(hand="far", angle=-45, layer="top")),
    ]
    dodge_back = [
        P(dx=6, lean=(2, 0), near_leg=(100, 80), far_leg=(60, 100), near_arm=(110, 70), far_arm=(85, -100),
          tail="fwd", weapon=dict(hand="far", angle=-45, layer="top"),
          effects=[(dash_lines(0, 0, 2, 7), "pelvis", -18, 6)]),
        P(dx=10, lean=(1, 0), near_leg=(130, 95), far_leg=(70, 90), near_arm=(100, 80), far_arm=(80, -105),
          tail="fwd", weapon=dict(hand="far", angle=-45, layer="top")),
    ]

    # --- critical: crouch, windmill the axe twice round, overhead chop -------------
    crit_lean = [
        P(dx=2, torso="back", lean=(1, 0), far_arm=(40, 30), near_arm=(130, 80),
          near_leg=(118, 98), far_leg=(58, 86), tail="back",
          weapon=dict(hand="far", angle=0, layer="top")),
        P(dx=4, torso="back", lean=(2, 1), far_arm=(25, 10), near_arm=(140, 90),
          near_leg=(128, 100), far_leg=(50, 80), tail="back",
          weapon=dict(hand="far", angle=0, layer="top")),
        P(dx=5, torso="back", lean=(3, 2), head_off=(-1, 0), far_arm=(10, -10), near_arm=(150, 100),
          near_leg=(138, 102), far_leg=(45, 75), tail="back",
          weapon=dict(hand="far", angle=-45, layer="top", variant="glint")),
    ]
    crit_hold = [
        crit_lean[2],
        P(dx=5, torso="back", lean=(3, 2), head_off=(-1, 0), far_arm=(10, -10), near_arm=(150, 100),
          near_leg=(138, 102), far_leg=(45, 75), tail="back",
          weapon=dict(hand="far", angle=-45, layer="top"),
          effects=[tipfx(STAR, -45)]),
    ]
    crit_lunge = [
        # spin, first half: the axe whirls down and forward
        P(dx=-4, torso="back", lean=(-1, 1), far_arm=(80, 100), near_arm=(-60, -100), tail="up",
          near_leg=(135, 100), far_leg=(45, 78),
          weapon=dict(hand="far", angle=100, layer="top", variant="blur"),
          effects=[slash("sh_far", 23, 60, -260, width=6)]),
        # spin, second half: up and over the back
        P(dx=-6, torso="side", lean=(-2, 0), far_arm=(-100, -80), near_arm=(120, 100), tail="up",
          near_leg=(140, 100), far_leg=(42, 75),
            weapon=dict(hand="far", angle=-80, layer="top", variant="blur"),
          effects=[slash("sh_far", 23, 240, -80, width=6)]),
        # the chop comes over the top
        P(dx=-8, torso="side", lean=(-3, 0), far_arm=(-90, -130), near_arm=(150, 120), tail="up",
          near_leg=(140, 100), far_leg=(45, 75),
          weapon=dict(hand="far", angle=-150, layer="top", variant="blur"),
          effects=[slash("sh_far", 27, -20, -205, width=8)]),
        # impact
        P(dx=-12, torso="side", lean=(-4, 2), far_arm=(150, 115), near_arm=(165, 110),
          near_leg=(152, 98), far_leg=(36, 66), far_boot="back", tail="back",
          weapon=dict(hand="far", angle=135, layer="top"),
          effects=[slash("sh_far", 28, -125, -200, width=8),
                   tipfx(STAR, 135), tipfx(DUST, 135, 0, 3)]),
        # follow-through
        P(dx=-12, torso="side", lean=(-4, 3), head_off=(0, 1), far_arm=(150, 118), near_arm=(160, 115),
          near_leg=(152, 98), far_leg=(36, 66), far_boot="back", tail="back",
          weapon=dict(hand="far", angle=135, layer="top"),
          effects=[tipfx(DUST, 135, -1, 2)]),
    ]
    crit_recover = [
        P(dx=-9, torso="side", lean=(-2, 1), far_arm=(160, 170), near_arm=(140, 100),
          near_leg=(140, 98), far_leg=(45, 75), far_boot="back", tail="back",
          weapon=dict(hand="far", angle=180, layer="top")),
        P(dx=-4, torso="front", lean=(-1, 0), far_arm=(120, 20), near_arm=(110, 85),
          near_leg=(125, 98), far_leg=(55, 85),
          weapon=dict(hand="far", angle=-90, layer="top")),
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
