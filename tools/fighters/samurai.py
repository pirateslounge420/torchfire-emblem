"""Samurai — pure Lake (☱ over ☱, hexagram 58). Sword. Silver.

A swift, light swordswoman: cropped silver coat over a slate undershirt and
trousers, leather belt and boots, dark hair in a high ponytail. Lean build.
Drawn original in the GBA FE idiom; faces LEFT.
"""
import math
from pixelkit import Figure, Palette, grid, capsule, blade, arc, flip_part, Canvas
from pixelkit.palette import SKIN, OUTLINE

NAME = "samurai"
BOX = 64

# 15 opaque colours. Shared slots: C=w=E (near-white), g=o, j=z, L=s, q=n, M=e.
_white = (244, 246, 252)
_slate = {"A": (120, 130, 160), "a": (76, 84, 112), "q": (44, 50, 78)}
PALETTE = Palette(NAME, {
    **SKIN,
    "H": (96, 100, 150), "h": (46, 48, 84), "g": OUTLINE,
    "C": _white, "c": (198, 202, 214), "k": (124, 130, 152),
    "w": _white, "E": _white,
    **_slate,
    "M": (168, 224, 255), "m": (130, 150, 200), "n": (44, 50, 78),
    "L": SKIN["s"], "l": (142, 94, 58), "j": SKIN["z"],
})

# --- parts -----------------------------------------------------------------
# Head, 3/4 view facing left. Anchor = neck (bottom centre).
HEAD = grid("""
...hhhhh..
..hHHhhhh.
.hHHhhhhhh
.hHhhhhhhh
.hhsSshhhh
.hsSSSsshh
.SSowSsshh
.SSsSsssh.
..ssssszh.
..zsssz...
...zzz....
""", anchor=(5, 11))

HEAD_HURT = grid("""
...hhhhh..
..hHHhhhh.
.hHHhhhhhh
.hHhhhhhhh
.hhsSshhhh
.hsSSSsshh
.SSooSsshh
.SSszsssh.
..sszsszh.
..zsssz...
...zzz....
""", anchor=(5, 11))

# High ponytail; anchor = where it leaves the back of the head.
PONYTAIL = {
    "rest": grid("""
hh..
hhh.
.hHh
.hhh
..hh
..hh
...h
""", anchor=(0, 0)),
    "back": grid("""
hhh..
.hhHh
...hh
....h
""", anchor=(0, 0)),
    "up": grid("""
....h
...hH
..hh.
hhh..
""", anchor=(0, 3)),
    "fwd": grid("""
.hh
hHh
hh.
h..
""", anchor=(2, 0)),
}

# Torso, anchored at the neck (top centre).
TORSO_FRONT = grid("""
....aa....
..Ccccaa..
.CccccaaCc
.Cccccakkk
.Cccccckkk
.Ccccccckk
..Cccccckk
..Ccccckk.
..lLLllj..
..Cccckkk.
.CCcccckkk
.Ccccckkkk
""", anchor=(5, 0))

TORSO_SIDE = grid("""
...aa...
.Cccca..
.Cccccc.
.Cccckk.
.Cccckk.
.Ccccckk
..ccckk.
..ccckk.
..lLlj..
..ccckk.
.Cccckkk
.Cccckkk
""", anchor=(4, 0))

TORSO_BACK = grid("""
....aa....
..ccccccc.
.kccccccCc
.kccccccCc
.kkcccccCc
.kkccccccC
..kcccccc.
..kcccccc.
..jllllL..
..kccccc..
.kkcccccC.
.kkccccCC.
""", anchor=(5, 0))

# Coat tails below the belt; anchor = pelvis (top centre).
TAILS = {
    "rest": grid("""
.Cccc.ckkk.
.Ccc..ckkkk
..cc...kkkk
..c.....kkk
.........kk
""", anchor=(5, 0)),
    "flare": grid("""
.Cccc.ckkkk..
.Ccc...kkkkkk
..c......kkkk
...........kk
""", anchor=(5, 0)),
    "fwd": grid("""
kkkk.cccC.
kkkk..ccC.
kkk....cC.
kk......C.
""", anchor=(5, 0)),
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


def dash_lines(x, y, n=3, length=8):
    p = grid("", anchor=(0, 0))
    for i in range(n):
        yy = y + i * 3
        for k in range(length - i * 2):
            p.pixels[(x + k, yy)] = "e" if k % 3 else "E"
    return p


def katana(angle, variant="normal"):
    """Sword anchored at the grip: 3 px of handle behind the hand, ~17 px of blade."""
    r = math.radians(angle)
    dx, dy = math.cos(r), math.sin(r)
    tip = (round(17 * dx), round(17 * dy))
    pommel = (round(-3 * dx), round(-3 * dy))
    if variant == "blur":
        return blade((round(2 * dx), round(2 * dy)), tip, width=4, letters=("E", "e", "e"), taper=0.45, edge=None)
    p = capsule(pommel, (0, 0), 2, ("L", "l", "j"))
    b = blade((round(1.5 * dx), round(1.5 * dy)), tip, width=2, letters=("M", "m", "n"), taper=0.3, edge="w")
    p = p.union(b)
    nx, ny = -dy, dx                      # tsuba: one pixel either side of the blade base
    for s in (-1, 1):
        p.pixels[(round(dx + s * nx), round(dy + s * ny))] = "l"
    if variant == "glint":
        p.pixels[(round(13 * dx), round(13 * dy))] = "E"
        p.pixels[(round(13 * dx) - 1, round(13 * dy))] = "E"
        p.pixels[(round(13 * dx) + 1, round(13 * dy))] = "E"
        p.pixels[(round(13 * dx), round(13 * dy) - 1)] = "E"
        p.pixels[(round(13 * dx), round(13 * dy) + 1)] = "E"
    return p


FIGURE = Figure(
    build="lean", arm_w=4, leg_w=4,
    parts={"heads": {"normal": HEAD, "hurt": HEAD_HURT},
           "torsos": {"front": TORSO_FRONT, "side": TORSO_SIDE, "back": TORSO_BACK},
           "extras": {**{"tail_" + k: v for k, v in TAILS.items()},
                      **{"pony_" + k: v for k, v in PONYTAIL.items()},
                      "star": STAR, "spark": SPARK}},
    sleeves=("C", "c", "k"),
    pants=("A", "a", "q"),
    weapon=katana,
)

RX = 36   # resting root x; the opponent is to the left


def P(dx=0, tail="rest", pony="rest", **kw):
    """Base pose: relaxed ready stance, sword low in the far hand pointing back."""
    base = dict(
        root=(RX + dx, 38), torso="front", head="normal", lean=(-1, 0),
        near_arm=(95, 80), far_arm=(55, 95),
        near_leg=(118, 98), far_leg=(62, 88),
        near_boot="side", far_boot="front",
        extras=[("tail_" + tail, "pelvis", 0, 0, "front"), ("pony_" + pony, "neck", 5, -7, "back")],
        weapon=dict(hand="far", angle=40, layer="top"),
        shadow=(9, 2),
    )
    base.update(kw)
    return base


def slash(joint, r, a0, a1, width=5, dx=0, dy=0):
    """A slash arc effect centred on a joint (usually the far shoulder, the pivot)."""
    return (arc((0, 0), r - width, r, a0, a1), joint, dx, dy)


def animations():
    idle = [
        P(),
        P(lean=(-1, 1), near_arm=(95, 82), far_arm=(55, 97), weapon=dict(hand="far", angle=42, layer="top")),
        P(lean=(-1, 1), head_off=(0, 1), near_arm=(95, 84), far_arm=(56, 99), weapon=dict(hand="far", angle=44, layer="top")),
        P(lean=(-1, 1), near_arm=(95, 82), far_arm=(55, 97), weapon=dict(hand="far", angle=42, layer="top")),
    ]

    # --- regular attack: raise over the far shoulder, then a diagonal cut ---
    lean = [
        P(dx=1, torso="front", lean=(0, 0), far_arm=(20, -50), near_arm=(120, 70),
          weapon=dict(hand="far", angle=-60, layer="top"), pony="back"),
        P(dx=3, torso="back", lean=(1, 0), far_arm=(-10, -80), near_arm=(135, 90),
          near_leg=(110, 95), far_leg=(55, 85),
          weapon=dict(hand="far", angle=-95, layer="top"), pony="back"),
        P(dx=4, torso="back", lean=(2, 0), far_arm=(-30, -110), near_arm=(140, 100),
          near_leg=(108, 95), far_leg=(52, 82),
          weapon=dict(hand="far", angle=-120, layer="top"), pony="back", tail="flare"),
    ]
    hold = [
        lean[2],
        P(dx=4, torso="back", lean=(2, -1), far_arm=(-32, -112), near_arm=(140, 100),
          near_leg=(108, 95), far_leg=(52, 82),
          weapon=dict(hand="far", angle=-122, layer="top"), pony="back", tail="flare"),
    ]
    lunge = [
        # blur: blade sweeping overhead toward the foe
        P(dx=-3, torso="side", lean=(-2, 0), far_arm=(-60, -140), near_arm=(150, 120),
          near_leg=(135, 100), far_leg=(50, 80), tail="flare", pony="up",
          weapon=dict(hand="far", angle=-160, layer="top", variant="blur"),
          effects=[slash("sh_far", 24, -60, -200, width=6)]),
        # impact: full extension
        P(dx=-9, torso="side", lean=(-3, 1), far_arm=(175, 175), near_arm=(170, 110),
          near_leg=(150, 98), far_leg=(40, 70), far_boot="back", tail="flare", pony="back",
          weapon=dict(hand="far", angle=172, layer="top"),
          effects=[slash("sh_far", 26, -110, -185, width=7)]),
        # follow-through: blade dips low
        P(dx=-9, torso="side", lean=(-3, 1), far_arm=(178, 190), near_arm=(170, 110),
          near_leg=(150, 98), far_leg=(40, 70), far_boot="back", tail="flare", pony="back",
          weapon=dict(hand="far", angle=160, layer="top")),
    ]
    recover = [
        P(dx=-6, torso="side", lean=(-2, 1), far_arm=(150, 160), near_arm=(140, 100),
          near_leg=(140, 98), far_leg=(45, 75), far_boot="back", tail="rest", pony="back",
          weapon=dict(hand="far", angle=150, layer="top")),
        P(dx=-3, torso="front", lean=(-1, 0), far_arm=(90, 120), near_arm=(110, 90),
          near_leg=(125, 98), far_leg=(55, 85),
          weapon=dict(hand="far", angle=95, layer="top")),
        P(dx=-1),
    ]

    # --- defence -------------------------------------------------------------
    guard = dict(torso="front", far_arm=(160, -100), near_arm=(150, -75), near_hand="open",
                 weapon=dict(hand="far", angle=-95, layer="top"))
    block = [
        P(dx=1, lean=(0, 0), **guard),
        P(dx=2, lean=(1, 1), near_leg=(122, 100), far_leg=(58, 84), **guard),
    ]
    parry = [
        P(dx=1, torso="front", far_arm=(160, -100), near_arm=(150, -75), near_hand="open",
          weapon=dict(hand="far", angle=-110, layer="top")),
        P(dx=-1, torso="side", lean=(-2, 0), far_arm=(165, -150), near_arm=(140, -60), near_hand="open",
          weapon=dict(hand="far", angle=-150, layer="top", variant="blur"),
          effects=[slash("wr_far", 16, -90, -175, width=4)]),
        P(dx=-2, torso="side", lean=(-2, 0), far_arm=(170, -170), near_arm=(135, -50), near_hand="open",
          weapon=dict(hand="far", angle=-172, layer="top"),
          effects=[(SPARK, "wr_far", -17, 0)]),
    ]
    hit = [
        P(dx=3, head="hurt", lean=(2, 1), head_off=(1, 0), torso="front",
          near_arm=(115, 55), far_arm=(40, 80), near_hand="open",
          near_leg=(105, 95), far_leg=(70, 95), tail="fwd", pony="fwd",
          weapon=dict(hand="far", angle=70, layer="top")),
        P(dx=2, head="hurt", lean=(2, 1), head_off=(1, 1), torso="front",
          near_arm=(120, 60), far_arm=(45, 85), near_hand="open",
          near_leg=(110, 95), far_leg=(65, 92), tail="fwd", pony="fwd",
          weapon=dict(hand="far", angle=65, layer="top")),
    ]
    # Stagger (sword): knocked back, drops to a knee and plants the blade.
    stagger = [
        P(dx=6, head="hurt", lean=(3, 1), head_off=(1, 0), torso="front",
          near_arm=(125, 50), far_arm=(60, 110), near_hand="open",
          near_leg=(128, 108), far_leg=(45, 60), far_boot="back", tail="fwd", pony="fwd",
          weapon=dict(hand="far", angle=110, layer="top")),
        P(dx=5, head="hurt", lean=(1, 2), head_off=(0, 1), torso="front", planted=False, root=(RX + 5, 45),
          near_arm=(140, 60), far_arm=(130, 100), near_hand="open",
          near_leg=(170, 110), near_shin_len=5, far_leg=(75, 0), far_shin_len=6, far_boot="back", far_boot_off=(0, -2),
          tail="fwd", pony="fwd", shadow=(10, 2),
          weapon=dict(hand="far", angle=150, layer="top")),
        P(dx=4, head="normal", lean=(0, 1), torso="front", planted=False, root=(RX + 4, 42),
          near_arm=(130, 70), far_arm=(110, 120), near_hand="open",
          near_leg=(150, 105), near_shin_len=6, far_leg=(70, 20), far_shin_len=6, far_boot="back", far_boot_off=(0, -2),
          tail="rest", pony="rest", shadow=(10, 2),
          weapon=dict(hand="far", angle=135, layer="top")),
    ]

    # --- dodges ----------------------------------------------------------------
    dodge_up = [
        P(dx=0, lean=(-1, 2), near_leg=(132, 105), far_leg=(48, 75), near_arm=(110, 100), far_arm=(60, 110),
          weapon=dict(hand="far", angle=60, layer="top")),
        P(dx=-1, planted=False, root=(RX - 1, 24), lean=(-1, 0), shadow=(6, 1),
          near_leg=(190, 115), far_leg=(165, 100), near_boot="tip", far_boot="tip",
          near_arm=(130, 60), far_arm=(40, 100), tail="flare", pony="up",
          weapon=dict(hand="far", angle=40, layer="top")),
    ]
    dodge_down = [
        P(dx=0, lean=(-2, 2), near_leg=(135, 100), far_leg=(45, 80), near_arm=(110, 90), far_arm=(50, 100),
          weapon=dict(hand="far", angle=50, layer="top")),
        P(dx=0, lean=(-3, 3), head_off=(-1, 1), near_leg=(165, 100), far_leg=(15, 85), near_arm=(150, 100), far_arm=(30, 110),
          far_boot="back", tail="flare", pony="up",
          weapon=dict(hand="far", angle=20, layer="top")),
    ]
    dodge_forward = [
        P(dx=-6, torso="side", lean=(-2, 0), near_leg=(145, 95), far_leg=(65, 100), near_arm=(120, 90), far_arm=(50, 100),
          tail="flare", pony="back", weapon=dict(hand="far", angle=45, layer="top"),
          effects=[(dash_lines(0, 0, 2, 7), "pelvis", 12, -3)]),
        P(dx=-10, torso="front", lean=(-1, 0), near_leg=(112, 95), far_leg=(78, 95), near_arm=(100, 85), far_arm=(55, 95),
          tail="rest", pony="back", weapon=dict(hand="far", angle=40, layer="top")),
    ]
    dodge_back = [
        P(dx=6, lean=(2, 0), near_leg=(100, 80), far_leg=(60, 100), near_arm=(110, 70), far_arm=(60, 100),
          tail="fwd", pony="fwd", weapon=dict(hand="far", angle=70, layer="top"),
          effects=[(dash_lines(0, 0, 2, 7), "pelvis", -16, 6)]),
        P(dx=10, lean=(1, 0), near_leg=(130, 95), far_leg=(70, 90), near_arm=(100, 80), far_arm=(60, 100),
          tail="rest", pony="fwd", weapon=dict(hand="far", angle=75, layer="top")),
    ]

    # --- critical: a low dash into a leaping overhead cut ----------------------
    crit_lean = [
        P(dx=2, torso="back", lean=(1, 0), far_arm=(30, 10), near_arm=(130, 80),
          near_leg=(115, 98), far_leg=(58, 86), pony="back",
          weapon=dict(hand="far", angle=10, layer="top")),
        P(dx=4, torso="back", lean=(2, 1), far_arm=(20, 0), near_arm=(140, 90),
          near_leg=(125, 100), far_leg=(50, 80), pony="back", tail="flare",
          weapon=dict(hand="far", angle=0, layer="top")),
        P(dx=5, torso="back", lean=(3, 2), head_off=(-1, 0), far_arm=(10, -5), near_arm=(150, 100),
          near_leg=(135, 102), far_leg=(45, 75), pony="back", tail="flare",
          weapon=dict(hand="far", angle=-8, layer="top", variant="glint")),
    ]
    crit_hold = [
        crit_lean[2],
        P(dx=5, torso="back", lean=(3, 2), head_off=(-1, 0), far_arm=(10, -5), near_arm=(150, 100),
          near_leg=(135, 102), far_leg=(45, 75), pony="back", tail="flare",
          weapon=dict(hand="far", angle=-8, layer="top"),
          effects=[(STAR, "wr_far", 9, -3)]),
    ]
    crit_lunge = [
        # dash
        P(dx=-6, torso="side", lean=(-3, 1), far_arm=(20, 0), near_arm=(170, 150),
          near_leg=(150, 100), far_leg=(35, 70), far_boot="back", tail="flare", pony="back",
          weapon=dict(hand="far", angle=-5, layer="top"),
          effects=[(dash_lines(0, 0, 3, 12), "pelvis", 8, -4)]),
        # leap, blade overhead
        P(dx=-8, planted=False, root=(RX - 8, 29), lean=(-2, -1), shadow=(6, 1),
          far_arm=(-30, -90), near_arm=(140, 60), near_leg=(75, 118), far_leg=(50, 100),
          near_boot="tip", far_boot="tip", tail="flare", pony="up",
          weapon=dict(hand="far", angle=-35, layer="top")),
        # the cut
        P(dx=-8, planted=False, root=(RX - 8, 29), torso="side", lean=(-3, 0), shadow=(7, 1),
          far_arm=(-100, -170), near_arm=(150, 80), near_leg=(120, 125), far_leg=(70, 105),
          near_boot="tip", far_boot="tip", tail="flare", pony="up",
          weapon=dict(hand="far", angle=-175, layer="top", variant="blur"),
          effects=[slash("sh_far", 26, -70, -200, width=7)]),
        # impact on landing
        P(dx=-11, torso="side", lean=(-3, 1), far_arm=(178, 185), near_arm=(165, 100),
          near_leg=(150, 100), far_leg=(40, 70), far_boot="back", tail="flare", pony="back",
          weapon=dict(hand="far", angle=170, layer="top"),
          effects=[slash("sh_far", 27, -120, -190, width=8), (STAR, "wr_far", -16, 2)]),
        # follow-through
        P(dx=-11, torso="side", lean=(-3, 2), far_arm=(180, 200), near_arm=(165, 100),
          near_leg=(152, 100), far_leg=(38, 68), far_boot="back", tail="flare", pony="back",
          weapon=dict(hand="far", angle=155, layer="top")),
    ]
    crit_recover = [
        P(dx=-9, torso="side", lean=(-2, 1), far_arm=(150, 160), near_arm=(140, 100),
          near_leg=(140, 98), far_leg=(45, 75), far_boot="back", tail="rest", pony="back",
          weapon=dict(hand="far", angle=150, layer="top")),
        P(dx=-4, torso="front", lean=(-1, 0), far_arm=(90, 120), near_arm=(110, 90),
          near_leg=(125, 98), far_leg=(55, 85),
          weapon=dict(hand="far", angle=95, layer="top")),
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
