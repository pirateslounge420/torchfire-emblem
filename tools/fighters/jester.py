"""Jester — pure Water (☵ over ☵, hexagram 29). Dagger. Indigo.

A small, quick trickster: two-pointed indigo hood with a bell on each tip,
a motley doublet split on the diagonal (indigo / pale lavender-blue), tight
dark hose, soft curled shoes and a short half-cape. The smallest fighter
(~34 px), crouched low, always moving. Drawn original in the GBA FE idiom;
faces LEFT.
"""
import math
from pixelkit import Figure, Palette, grid, capsule, blade, arc, flip_part, rot90_part, Canvas
from pixelkit.palette import SKIN, OUTLINE, TRIGRAM

NAME = "jester"
BOX = 64

# 15 opaque colours. Shared slots: w=E (white), M=e (slash edge), q=n (hose
# shadow = steel shadow), L=s, j=z. `p` is the tongue.
_water = TRIGRAM["water"]
_dark = (18, 18, 60)
PALETTE = Palette(NAME, {
    **SKIN,
    **_water,                                        # C c k  indigo (trigram)
    "A": (214, 216, 250), "a": (164, 172, 236),      # pale lavender-blue (motley half)
    "q": _dark,
    "M": (168, 224, 255), "m": (130, 150, 200), "n": _dark,
    "L": SKIN["s"], "l": (142, 94, 58), "j": SKIN["z"],
    "p": (226, 104, 140),
})

# --- parts -----------------------------------------------------------------
# Head, 3/4 view facing left, hood instead of hair. Anchor = neck (bottom
# centre of the chin). The two hood points droop either side with a `w` bell.
HEAD = grid("""
......cCCccc....
...cccCCcccccccc
..c.cCCccccckk.c
..c.cccccckkkk.c
..c.cSsSSskkkk.c
..w.cSsSSsskkk.w
....cSowSsskkk..
....csSsSsskkk..
.....zzSsszkk...
.....zsssz.k....
......zzz.......
""", anchor=(7, 11))

HEAD_HURT = grid("""
......cCCccc....
...cccCCcccccccc
..c.cCCccccckk.c
..c.cccccckkkk.c
..c.cSsSSskkkk.c
..w.cSsSSsskkk.w
....cSooSsskkk..
....csSsSsskkk..
.....ozSsszkk...
....ppsssz.k....
......zzz.......
""", anchor=(7, 11))

# Mischievous: one eye shut in a wink, big grin.
HEAD_WINK = grid("""
......cCCccc....
...cccCCcccccccc
..c.cCCccccckk.c
..c.cccccckkkk.c
..c.cSsSSskkkk.c
..w.cSsSSsskkk.w
....cSzzSsskkk..
....csSsSsskkk..
.....zzzsszkk...
.....zsssz.k....
......zzz.......
""", anchor=(7, 11))

# Points flung straight out sideways (a sudden drop or a jump).
HEAD_SPLAY = grid("""
......cCCccc....
wccccccCCccccccw
....cCCccccckk..
....cccccckkkk..
....cSsSSskkkk..
....cSsSSsskkk..
....cSowSsskkk..
....csSsSsskkk..
.....zzSsszkk...
.....zsssz.k....
......zzz.......
""", anchor=(7, 11))

# Knocked flat: hurt face, points flung out.
HEAD_TUMBLE = grid("""
......cCCccc....
wccccccCCccccccw
....cCCccccckk..
....cccccckkkk..
....cSsSSskkkk..
....cSsSSsskkk..
....cSooSsskkk..
....csSsSsskkk..
.....ozSsszkk...
....ppsssz.k....
......zzz.......
""", anchor=(7, 11))

# Rolled: face down, crown toward the foe (forward roll / cartwheel entry).
HEAD_ROLL = rot90_part(HEAD_SPLAY, 3)
# Upside down (handstand), face still toward the foe.
HEAD_INV = flip_part(rot90_part(HEAD_SPLAY, 2))

# Torso, anchored at the neck (top centre). Motley: indigo on the left,
# lavender on the right, split on a diagonal. 10 wide x 10 tall.
TORSO_FRONT = grid("""
....cc....
..CccccAA.
.CcccccAaa
.Cccccaaac
.Cccccaaac
.Cccccaaac
..ccccaaac
..lLlljjj.
..ccaaaac.
.cccaaaacc
""", anchor=(5, 0))

TORSO_SIDE = grid("""
...cc...
.Cccca..
.Ccccaa.
.Cccccaa
.Cccccaa
.Ccccaac
..ccaaac
..lLljj.
..caaac.
.ccaaacc
""", anchor=(4, 0))

TORSO_BACK = grid("""
....cc....
..ccccAAA.
.kcccccAAa
.kccccaaAa
.kccccaaAa
.kkcccaaAa
..kccaaaa.
..jlllLL..
..kcaaaaA.
.kkcaaaaAa
""", anchor=(5, 0))

# Rotated torsos for the cartwheel: lying (neck left, pelvis right) and
# inverted (neck below the pelvis), chest still toward the foe.
TORSO_CART = rot90_part(TORSO_SIDE, 3)
TORSO_INV = flip_part(rot90_part(TORSO_SIDE, 2))

# Half-cape hanging from the shoulders; anchor = top-left, placed at the neck.
CAPE = {
    "rest": grid("""
cccccc..
.cccckk.
.ccccck.
.cccckk.
..ccckk.
..ccckk.
..cckkk.
...kkk..
...kk...
""", anchor=(0, 0)),
    "flare": grid("""
ccccccccc...
.cccccccckk.
..cccccckkkk
....ccckkkk.
......kkk...
""", anchor=(0, 0)),
    "fwd": grid("""
.ccccc..
ccccccc.
.cccckk.
...kkk..
""", anchor=(6, 0)),
    "up": grid("""
....ckk
...cckk
..cccck
..cccc.
.cccc..
cccc...
cc.....
""", anchor=(0, 6)),
}

# Soft pointed shoes with a curled toe; anchor = ankle (top centre).
SHOES = {
    "side": grid("""
...LLl.
L..llll
jllllll
.jjjjjj
""", anchor=(3, 0)),
    "front": grid("""
..LLl..
L.llllj
jlllljj
.jjjjj.
""", anchor=(3, 0)),
    "back": grid("""
.lLL...
jllll.L
jjllllj
.jjjjj.
""", anchor=(3, 0)),
    "tip": grid("""
..LLl.
l.llll
.jjjj.
""", anchor=(3, 0)),
}
SHOES["up"] = flip_part(rot90_part(SHOES["side"], 2))

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

GLINT = grid("""
.E.
EEE
.E.
""", anchor=(1, 1))


def dash_lines(x, y, n=3, length=8):
    p = grid("", anchor=(0, 0))
    for i in range(n):
        yy = y + i * 3
        for k in range(length - i * 2):
            p.pixels[(x + k, yy)] = "e" if k % 3 else "E"
    return p


def dagger(angle, variant="normal"):
    """Short dagger anchored at the grip: 2 px of leather grip behind the hand,
    a 2-px crossguard and an 8-px blade."""
    r = math.radians(angle)
    dx, dy = math.cos(r), math.sin(r)

    def at(t):
        return (round(t * dx), round(t * dy))

    if variant == "blur":
        return blade(at(0.5), at(9.5), width=4, letters=("E", "e", "e"), taper=0.4, edge=None)
    p = capsule(at(-2), (0, 0), 2, ("L", "l", "j"))
    b = blade(at(1.5), at(9.5), width=3, letters=("M", "m", "n"), taper=0.5, edge="w")
    p = p.union(b)
    nx, ny = -dy, dx                      # crossguard: one pixel either side of the blade base
    for s in (-1, 1):
        p.pixels[(round(dx + s * nx), round(dy + s * ny))] = "m"
    if variant == "glint":
        gx, gy = at(7)
        for ox, oy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
            p.pixels[(gx + ox, gy + oy)] = "E"
    return p


def tip_fx(part, angle, dist=11, dx=0, dy=0):
    """An effect sitting on the dagger's point (relative to the far wrist)."""
    r = math.radians(angle)
    return (part, "wr_far", round(dist * math.cos(r)) + dx, round(dist * math.sin(r)) + dy)


FIGURE = Figure(
    build="lean", arm_w=3, leg_w=3,
    parts={"heads": {"normal": HEAD, "hurt": HEAD_HURT, "wink": HEAD_WINK, "splay": HEAD_SPLAY,
                     "tumble": HEAD_TUMBLE, "roll": HEAD_ROLL, "inv": HEAD_INV},
           "torsos": {"front": TORSO_FRONT, "side": TORSO_SIDE, "back": TORSO_BACK,
                      "cart": TORSO_CART, "inv": TORSO_INV},
           "boots": SHOES,
           "extras": {**{"cape_" + k: v for k, v in CAPE.items()}, "star": STAR, "spark": SPARK}},
    sleeves=("C", "c", "k"),
    pants=("k", "k", "q"),
    weapon=dagger,
)

RX = 36   # resting root x; the opponent is to the left

CAPE_AT = {"rest": (2, 1), "flare": (2, 1), "fwd": (-1, -1), "up": (3, 1)}


def P(dx=0, cape="rest", **kw):
    """Base pose: low crouched stance, lead hand open and forward, dagger held
    reversed (point down) in the far hand by the hip."""
    cx, cy = CAPE_AT[cape]
    base = dict(
        root=(RX + dx, 40), torso="front", head="normal", lean=(-1, 1), torso_h=10,
        near_upper_len=5, near_fore_len=5, far_upper_len=5, far_fore_len=5,
        near_thigh_len=6, near_shin_len=6, far_thigh_len=6, far_shin_len=6,
        far_sleeve=("A", "a", "c"),
        near_arm=(140, 110), far_arm=(60, 100), near_hand="open",
        near_leg=(138, 102), far_leg=(42, 80),
        near_boot="side", far_boot="front",
        extras=[("cape_" + cape, "neck", cx, cy, "back")],
        weapon=dict(hand="far", angle=110, layer="top"),
        shadow=(8, 2),
    )
    base.update(kw)
    return base


def slash(joint, r, a0, a1, width=4, dx=0, dy=0):
    """A small deflect arc centred on a joint."""
    return (arc((0, 0), r - width, r, a0, a1), joint, dx, dy)


def animations():
    W = lambda angle, **k: dict(hand="far", angle=angle, layer="top", **k)   # noqa: E731

    idle = [
        P(weapon=W(110)),
        P(near_leg=(132, 98), far_leg=(48, 83), weapon=W(200)),
        P(lean=(-1, 0), near_leg=(125, 95), far_leg=(55, 85), weapon=W(290)),
        P(near_leg=(132, 98), far_leg=(48, 83), weapon=W(20)),
    ]

    # --- regular attack: coil back and down, then dart in with two stabs ---
    lean = [
        P(dx=1, lean=(0, 1), far_arm=(40, 70), near_arm=(130, 100), weapon=W(40)),
        P(dx=3, torso="back", lean=(1, 2), far_arm=(30, 60), near_arm=(145, 105),
          near_leg=(145, 104), far_leg=(35, 77), weapon=W(-20)),
        P(dx=4, torso="back", lean=(2, 3), far_arm=(20, 55), near_arm=(155, 110),
          near_leg=(150, 105), far_leg=(30, 75), weapon=W(-40)),
    ]
    hold = [
        lean[2],
        P(dx=4, torso="back", lean=(2, 2), far_arm=(20, 55), near_arm=(155, 110),
          near_leg=(150, 105), far_leg=(30, 75), weapon=W(-42)),
    ]
    lunge = [
        # blur: darting in, dagger whipping forward, dash streak behind
        P(dx=-4, torso="side", lean=(-3, 1), far_arm=(170, 160), near_arm=(60, 120),
          near_leg=(150, 95), far_leg=(40, 75), far_boot="back", cape="flare",
          weapon=W(190, variant="blur"),
          effects=[(dash_lines(0, 0, 3, 10), "pelvis", 9, -6)]),
        # impact: full-extension stab
        P(dx=-11, torso="side", lean=(-3, 2), far_arm=(180, 180), near_arm=(40, 110),
          near_leg=(155, 95), far_leg=(30, 70), far_boot="back", cape="flare",
          weapon=W(180), effects=[tip_fx(SPARK, 180)]),
        # second quick stab, a touch higher
        P(dx=-11, torso="side", lean=(-3, 2), far_arm=(165, 200), near_arm=(50, 120),
          near_leg=(155, 95), far_leg=(30, 70), far_boot="back", cape="flare",
          weapon=W(195), effects=[tip_fx(SPARK, 195)]),
    ]
    recover = [
        # backflip-ish hop away
        P(dx=-7, planted=False, root=(RX - 7, 31), shadow=(6, 1), lean=(2, -1), head_off=(1, -1),
          near_arm=(160, -150), far_arm=(-20, -60), near_leg=(160, 60), far_leg=(140, 40),
          near_boot="tip", far_boot="tip", cape="up", weapon=W(-60)),
        # landing crouch
        P(dx=-3, lean=(0, 2), near_leg=(150, 105), far_leg=(30, 75), near_arm=(130, 100),
          far_arm=(50, 90), cape="fwd", weapon=W(100)),
        P(dx=-1),
    ]

    # --- defence -------------------------------------------------------------
    guard = dict(torso="front", far_arm=(180, -120), near_arm=(135, 15), near_hand="fist",
                 weapon=W(-100))
    block = [
        P(dx=1, lean=(0, 0), **guard),
        P(dx=2, lean=(1, 2), near_leg=(142, 103), far_leg=(38, 78), **guard),
    ]
    parry = [
        P(dx=1, lean=(0, 0), torso="front", far_arm=(180, -120), near_arm=(135, 15), near_hand="fist",
          weapon=W(-110)),
        P(dx=0, torso="side", lean=(-2, 0), far_arm=(175, -150), near_arm=(130, 10), near_hand="fist",
          weapon=W(-160, variant="blur"),
          effects=[slash("wr_far", 10, -60, -175, width=4)]),
        P(dx=-4, torso="side", lean=(-3, 1), far_arm=(180, 180), near_arm=(45, 110),
          near_leg=(150, 95), far_leg=(35, 72), far_boot="back", cape="flare",
          weapon=W(180), effects=[tip_fx(SPARK, 180)]),
    ]
    hit = [
        P(dx=3, head="hurt", lean=(2, 1), head_off=(1, 0), near_arm=(115, 55), far_arm=(40, 85),
          near_leg=(125, 98), far_leg=(60, 90), cape="fwd", weapon=W(75)),
        P(dx=2, head="hurt", lean=(2, 2), head_off=(1, 1), near_arm=(120, 60), far_arm=(45, 88),
          near_leg=(128, 98), far_leg=(58, 88), cape="fwd", weapon=W(70)),
    ]
    # Stagger (dagger): a comic tumble — knocked onto her backside, legs in
    # the air, then scrambling back up from a squat.
    stagger = [
        P(dx=6, head="hurt", lean=(3, 1), head_off=(1, 0), near_arm=(-70, -130), far_arm=(-30, -90),
          near_leg=(160, 100), far_leg=(70, 95), cape="fwd", weapon=W(-60)),
        P(dx=9, head="tumble", planted=False, root=(RX + 9, 49), shadow=(11, 2), lean=(4, 3), head_off=(2, 1),
          near_arm=(120, 60), far_arm=(30, 70), near_hand="open",
          near_leg=(-140, -60), far_leg=(-120, -40), near_boot="side", far_boot="side",
          near_boot_off=(0, -2), far_boot_off=(0, -2), cape="fwd", weapon=W(-30)),
        P(dx=5, head="hurt", planted=False, root=(RX + 5, 46), shadow=(10, 2), lean=(1, 2),
          near_arm=(130, 110), far_arm=(40, 80), near_hand="open",
          near_leg=(170, 55), near_shin_len=5, far_leg=(75, -5), far_boot="back", far_boot_off=(0, -1),
          cape="rest", weapon=W(120)),
    ]

    # --- dodges ----------------------------------------------------------------
    dodge_up = [
        P(lean=(-1, 2), near_leg=(145, 103), far_leg=(35, 78), near_arm=(120, 100), far_arm=(50, 100),
          weapon=W(100)),
        P(dx=-1, planted=False, root=(RX - 1, 22), shadow=(6, 1), lean=(-1, 0), head="splay",
          near_leg=(-170, 50), far_leg=(-160, 60), near_boot="tip", far_boot="tip",
          near_arm=(-120, -170), far_arm=(-40, -100), cape="up", weapon=W(-80)),
    ]
    dodge_down = [
        P(lean=(-2, 2), near_leg=(145, 103), far_leg=(35, 78), near_arm=(120, 100), far_arm=(50, 100),
          weapon=W(100)),
        P(lean=(-4, 4), head="splay", head_off=(-1, 1), near_leg=(175, 95), far_leg=(5, 80),
          far_boot="back", near_arm=(150, 100), far_arm=(30, 100), cape="up", weapon=W(30)),
    ]
    dodge_forward = [
        # tucked ball, head down, rolling toward the foe
        P(dx=-7, planted=False, root=(RX - 7, 44), shadow=(7, 1), torso="side", lean=(-4, 5),
          head="roll", head_off=(-2, 2), near_arm=(150, 60), far_arm=(140, 50),
          near_leg=(-150, 20), far_leg=(-140, 30), near_boot="tip", far_boot="tip",
          cape="up", weapon=W(120),
          effects=[(dash_lines(0, 0, 2, 7), "pelvis", 11, -4)]),
        P(dx=-10, lean=(-2, 3), near_leg=(150, 105), far_leg=(30, 75), near_arm=(140, 100),
          far_arm=(50, 95), cape="flare", weapon=W(100)),
    ]
    dodge_back = [
        # high backward hop
        P(dx=6, planted=False, root=(RX + 6, 30), shadow=(6, 1), lean=(2, -1), head="splay",
          near_leg=(170, 110), far_leg=(150, 100), near_boot="tip", far_boot="tip",
          near_arm=(-130, -160), far_arm=(-30, -80), cape="fwd", weapon=W(-60),
          effects=[(dash_lines(0, 0, 2, 7), "pelvis", -16, 4)]),
        P(dx=10, lean=(1, 2), near_leg=(140, 103), far_leg=(40, 80), near_arm=(120, 90),
          far_arm=(50, 100), weapon=W(100)),
    ]

    # --- critical: crouch, hide the dagger, cartwheel in, triple stab ----------
    hidden = dict(hand="far", layer="far")
    crit_lean = [
        P(dx=2, torso="back", lean=(1, 1), far_arm=(70, 160), near_arm=(150, 110),
          near_leg=(140, 103), far_leg=(40, 80), weapon=dict(angle=20, **hidden)),
        P(dx=4, torso="back", lean=(2, 2), far_arm=(65, 165), near_arm=(155, 115),
          near_leg=(150, 105), far_leg=(30, 75), weapon=dict(angle=15, **hidden)),
        P(dx=5, torso="back", lean=(3, 3), head="wink", far_arm=(60, 170), near_arm=(158, 118),
          near_leg=(155, 106), far_leg=(25, 72), weapon=dict(angle=10, variant="glint", **hidden)),
    ]
    crit_hold = [
        crit_lean[2],
        P(dx=5, torso="back", lean=(3, 3), head="wink", far_arm=(60, 170), near_arm=(158, 118),
          near_leg=(155, 106), far_leg=(25, 72), weapon=dict(angle=10, **hidden),
          effects=[(STAR, "wr_far", 9, 1)]),
    ]
    crit_lunge = [
        # cartwheel entry: diving, hands to the ground, legs trailing
        P(dx=-6, planted=False, root=(RX - 6, 40), shadow=(8, 1), torso="cart", lean=(-10, 10),
          head="roll", head_off=(0, 0), near_arm=(110, 95), far_arm=(100, 90), near_hand="open", far_hand="open",
          near_leg=(-20, -30), far_leg=(0, -20), near_boot="back", far_boot="back",
          extras=[], weapon=W(0),
          effects=[(dash_lines(0, 0, 3, 10), "pelvis", 10, -8)]),
        # inverted: handstand, legs split in the air
        P(dx=-9, planted=False, root=(RX - 9, 30), shadow=(8, 1), torso="inv", lean=(0, 20),
          head="inv", near_arm=(95, 90), far_arm=(85, 90), near_hand="open", far_hand="open",
          near_leg=(-120, -100), far_leg=(-50, -70), near_boot="up", far_boot="up",
          extras=[], weapon=W(200)),
        # triple stab
        P(dx=-10, torso="side", lean=(-3, 2), far_arm=(170, 200), near_arm=(40, 110),
          near_leg=(155, 95), far_leg=(30, 70), far_boot="back", cape="flare",
          weapon=W(195, variant="blur"), effects=[tip_fx(SPARK, 195)]),
        P(dx=-11, torso="side", lean=(-3, 2), far_arm=(185, 165), near_arm=(45, 115),
          near_leg=(155, 95), far_leg=(30, 70), far_boot="back", cape="flare",
          weapon=W(165, variant="blur"), effects=[tip_fx(SPARK, 165)]),
        P(dx=-11, torso="side", lean=(-3, 2), far_arm=(180, 180), near_arm=(40, 110),
          near_leg=(158, 95), far_leg=(28, 68), far_boot="back", cape="flare",
          weapon=W(180, variant="blur"), effects=[tip_fx(STAR, 180, dist=12)]),
    ]
    crit_recover = [
        # a bow with a flourish
        P(dx=-8, lean=(-2, 3), head_off=(-2, 2), near_arm=(170, 100), far_arm=(0, -60),
          near_leg=(150, 95), far_leg=(40, 80), far_boot="back", weapon=W(-30)),
        P(dx=-4, lean=(-1, 1), near_arm=(120, 90), far_arm=(50, 90), weapon=W(100)),
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
