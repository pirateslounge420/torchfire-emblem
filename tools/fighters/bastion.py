"""Bastion — pure Mountain (☶ over ☶, hexagram 52). Long mace. Orange.

A walking wall of plate: orange-enamelled breastplate, square pauldrons and
plated skirt with steel trim, a great helm with a narrow visor slit and a
short orange crest, dark gambeson showing at the joints. Two-handed long
mace. The heaviest silhouette in the roster (~42 px). Drawn original in the
GBA FE idiom; faces LEFT.
"""
import math
from pixelkit import Figure, Palette, Part, grid, capsule, blade, arc, ellipse, flip_part, rot90_part
from pixelkit.palette import TRIGRAM, STEEL

NAME = "bastion"
BOX = 64

# 12 opaque colours (budget 15). No skin, hair or leather: everything is plate.
# Shared slots: E = w (white).
_gambeson = {"A": (112, 96, 92), "a": (72, 60, 62), "q": (42, 36, 44)}
PALETTE = Palette(NAME, {
    **TRIGRAM["mountain"],     # C c k  orange enamel (dominant)
    **STEEL,                   # M m n  steel trim, helm, mace
    **_gambeson,               # A a q  padded gambeson at the joints
})

# --- parts -----------------------------------------------------------------
# Great helm, 3/4 view facing left. Anchor = neck (bottom centre). The crest
# is the two orange rows on top; the visor slit is the `o` row.
HELM = grid("""
....CCc....
...CCCcck..
..MMkccckkM
.MMMMmmmmmn
.MMMMmmmmmn
.MMMmmmmmmn
.Moooooomnn
.Mmmommmmnn
.Mmmommmmnn
.Mmmmmmmnnn
.Mmmmmmmnnn
..Mmmmmnnn.
..nnnnnnnn.
""", anchor=(5, 13))

# Hurt: the crest flops down the back of the helm.
HELM_HURT = grid("""
...........
...........
...........
..MMMMmmmCc
.MMMMmmmmCk
.MMMmmmmmck
.Moooooomkk
.Mmmommmmnk
.Mmmommmmnn
.Mmmmmmmnnn
.Mmmmmmmnnn
..Mmmmmnnn.
..nnnnnnnn.
""", anchor=(5, 13))

# Torsos, anchored at the neck (top centre). Row 0 = gambeson collar,
# rows 1-7 breastplate (orange with a central `o` ridge), row 8 steel belt,
# rows 9-11 hips (mostly hidden by the fauld).
TORSO_FRONT = grid("""
....qaaq....
..MMCCcccmm.
.MCCCCccckkn
.MCCCCccckkn
.MCCCoCcckkn
.MCCCoCccckn
..MCCoCcckn.
..MCCoccckn.
..nmmmmmmnn.
..MCCccckkn.
..MCCcccckn.
..nnnnnnnnn.
""", anchor=(6, 0))

TORSO_SIDE = grid("""
...qaaq..
..MMCccm.
.MCCCcckn
.MCCCcckn
.MCCoccnn
.MCCoccnn
..MCoccn.
..MCcckn.
..nmmmmn.
..MCcckn.
..MCcckn.
..nnnnnn.
""", anchor=(4, 0))

TORSO_BACK = grid("""
....qaaq....
..mmcccCCMM.
.nkkcccCCCCM
.nkkcccCCCCM
.nkkccoCCCCM
.nkkccoCCCCM
..nkcoCCCCM.
..nkcoCCCCM.
..nnmmmmmmn.
..nkkccCCCM.
..nkkcccCCM.
..nnnnnnnnn.
""", anchor=(6, 0))

# Plated skirt (fauld), anchored at the pelvis; covers the hip joints.
FAULD = grid("""
.MMMMmmmmmmmmn.
MCCCoCccocckkkn
MCCCoCccocckkkn
.mCCoCccockkkn.
..nnnnnnnnnnn..
""", anchor=(7, 1))

# Square pauldron, anchored on the shoulder joint.
PAULDRON = grid("""
.MMMMm.
MCCCCkm
MCCCckn
MCCcckn
mCcckkn
.nnnnn.
""", anchor=(3, 2))

# Gambeson showing at a knee (wide) and an elbow (small diamond).
JOINT = grid("""
.Aaa.
Aaaqq
.aqq.
""", anchor=(2, 1))
ELBOW = grid("""
.a.
Aaq
.q.
""", anchor=(1, 1))

# Gauntlets (anchor = wrist) and sabatons (anchor = ankle, top centre).
GAUNT = grid("""
.MMm.
Mmmmn
mmmnn
.nnn.
""", anchor=(2, 1))
GAUNT_OPEN = grid("""
.MMmm.
Mmmmmn
mmmnnn
.nnnn.
""", anchor=(2, 1))
HANDS = {"fist": GAUNT, "grip": GAUNT, "open": GAUNT_OPEN}

SABATON_SIDE = grid("""
..MMmm..
.Mmmmmmn
Mmmmmnnn
nnnnnnnn
""", anchor=(4, 0))
SABATON_FRONT = grid("""
.MMmm..
Mmmmmmn
mmmmnnn
nnnnnnn
""", anchor=(3, 0))
SABATON_TIP = grid("""
.MMmm.
mmmmmn
.nnnn.
""", anchor=(3, 0))
BOOTS = {"side": SABATON_SIDE, "front": SABATON_FRONT,
         "back": flip_part(SABATON_SIDE), "tip": SABATON_TIP}

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

# A small patch of ground shadow under the mace head on impact.
BUMP = ellipse((0, 0), 5, 1.5, "%").with_anchor(0, 0)


def dash_lines(x, y, n=3, length=8):
    p = grid("", anchor=(0, 0))
    for i in range(n):
        yy = y + i * 3
        for k in range(length - i * 2):
            p.pixels[(x + k, yy)] = "e" if k % 3 else "E"
    return p


def dust(stage=0):
    """Dust kicked up by the mace head: stage 0 = the burst, 1 = rising, 2 = fading."""
    sets = [
        [(-5, -4, "e"), (-4, -7, "E"), (-2, -9, "e"), (1, -9, "e"), (3, -7, "E"), (6, -4, "e"),
         (-6, -1, "e"), (8, -2, "e"), (-6, 2, "e"), (9, 1, "e"), (0, -6, "e")],
        [(-6, -7, "e"), (-5, -11, "e"), (-2, -13, "E"), (3, -12, "e"), (7, -9, "e"), (10, -5, "e"),
         (-6, -2, "e"), (12, 0, "e"), (-4, -9, "e"), (5, -6, "e")],
        [(-6, -11, "e"), (-4, -15, "e"), (2, -16, "e"), (8, -13, "e"), (12, -8, "e"), (-6, -5, "e")],
    ]
    return Part({(x, y): c for x, y, c in sets[stage]}, (0, 0))


def shockwave(rx, ry, dotted=False):
    """A ring of dust along the ground around the impact point."""
    out = {}
    for y in range(-ry - 1, ry + 2):
        for x in range(-rx - 1, rx + 2):
            v = ((x + 0.5) / rx) ** 2 + ((y + 0.5) / ry) ** 2
            if 0.62 <= v <= 1.0:
                if dotted and (x + y) % 2:
                    continue
                out[(x, y)] = "E" if (v < 0.8 and y < 0) else "e"
    return Part(out, (0, 0))


# --- the mace ----------------------------------------------------------------
# Flanged head authored at 0° (haft enters from the left) and 45° (from the
# upper-left); the other six angles are rotations, re-lit from the upper-left.
_HEAD_0 = grid("""
....m....
...mmm.m.
..mmmmm..
.mmmmmmm.
.mmmmmmmm
.mmmmmmm.
..mmmmm..
...mmm.m.
....m....
""", anchor=(4, 4))

_HEAD_45 = grid("""
.........
...mmm.m.
..mmmmm..
.mmmmmmm.
.mmmmmmmm
.mmmmmmm.
..mmmmm..
.m.mmm.m.
....m....
""", anchor=(4, 4))


def _relight(p):
    out = {}
    ax, ay = p.anchor
    for (x, y), c in p.pixels.items():
        if c in "Mmn":
            v = -0.6 * (x - ax) - 0.8 * (y - ay)
            c = "M" if v >= 1.3 else ("n" if v <= -1.3 else "m")
        out[(x, y)] = c
    return Part(out, p.anchor)


def _mace_heads():
    heads = {}
    for k in range(8):
        ang = k * 45
        base = _HEAD_0 if k % 2 == 0 else _HEAD_45
        heads[ang] = _relight(rot90_part(base, k // 2))
    return heads


MACE_HEADS = _mace_heads()
HAFT = 16          # grip -> haft end
HEAD_R = 19        # grip -> centre of the head
HAND_UP = 6        # near hand sits this far up the haft from the far hand


def head_offset(angle, r=HEAD_R):
    a = math.radians(angle)
    return (round(r * math.cos(a)), round(r * math.sin(a)))


def _ringed(p):
    """Add a 1-px outline ring around a part (in its own space) so a hand
    reads as separate from the haft it is drawn over."""
    out = dict(p.pixels)
    for (x, y) in list(p.pixels):
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            q = (x + dx, y + dy)
            if q not in p.pixels:
                out[q] = "o"
    return Part(out, p.anchor)


def mace(angle, variant="normal"):
    """Two-handed mace anchored at the far hand's grip. Both gauntlets are
    part of the weapon so they sit on top of the haft whatever layer the
    body parts are on. Variants: normal, blur, glint, solo (far hand only)."""
    r = math.radians(angle)
    dx, dy = math.cos(r), math.sin(r)
    hx, hy = head_offset(angle)
    hands = [(0, 0)] if variant == "solo" else [(0, 0), (round(HAND_UP * dx), round(HAND_UP * dy))]
    if variant == "blur":
        p = blade((round(2 * dx), round(2 * dy)), (hx, hy), width=5, letters=("E", "e", "e"), taper=0.0, edge=None)
        p = p.union(ellipse((hx, hy), 4.0, 4.0, "e"))
        p = p.union(ellipse((hx, hy), 2.2, 2.2, "E"))
    else:
        p = capsule((round(-3 * dx), round(-3 * dy)), (round(HAFT * dx), round(HAFT * dy)), 3, ("m", "m", "n"))
        p.pixels[(round(-3 * dx), round(-3 * dy))] = "M"        # pommel cap
        head = MACE_HEADS[round(angle / 45.0) % 8 * 45]
        p = p.union(_place(head, hx, hy))
        if variant == "glint":
            gx, gy = hx - 2, hy - 2
            for ox, oy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
                p.pixels[(gx + ox, gy + oy)] = "E"
    for (gx, gy) in hands:
        p = p.union(_place(_ringed(GAUNT), gx, gy))
    return p


def _place(part, x, y):
    """A copy of `part` moved so its anchor sits at (x, y) in weapon space."""
    ax, ay = part.anchor
    return Part({(px - ax + x, py - ay + y): c for (px, py), c in part.pixels.items()}, (0, 0))


FIGURE = Figure(
    build="heavy", arm_w=6, leg_w=6,
    parts={"heads": {"normal": HELM, "hurt": HELM_HURT},
           "torsos": {"front": TORSO_FRONT, "side": TORSO_SIDE, "back": TORSO_BACK},
           "hands": HANDS, "boots": BOOTS,
           "extras": {"fauld": FAULD, "pauldron": PAULDRON, "joint": JOINT, "elbow": ELBOW,
                      "star": STAR, "spark": SPARK, "bump": BUMP}},
    sleeves=("M", "m", "n"),      # plated arms
    pants=("C", "c", "k"),        # orange greaves
    weapon=mace,
)

RX = 36   # resting root x; the opponent is to the left

BASE_EXTRAS = [
    ("elbow", "el_far", 0, 0, "far_arm"),
    ("joint", "kn_far", 0, 0, "far_leg"),
    ("pauldron", "sh_far", 0, 0, "torso"),
    ("joint", "kn_near", 0, 0, "near_leg"),
    ("fauld", "pelvis", 0, 0, "front"),
    ("elbow", "el_near", 0, 0, "near_arm"),
    ("pauldron", "sh_near", 0, 0, "near_arm"),
]


# --- posing helpers -----------------------------------------------------------
def _ik(sh, tgt, l1, l2, bend=1):
    """Two-bone IK: angles (upper, fore) so the wrist lands on tgt."""
    dx, dy = tgt[0] - sh[0], tgt[1] - sh[1]
    d = math.hypot(dx, dy)
    base = math.atan2(dy, dx)
    if d >= l1 + l2 - 1e-6:
        a = math.degrees(base)
        return (a, a)
    d = max(d, abs(l1 - l2) + 1e-6)
    cos_a = (l1 * l1 + d * d - l2 * l2) / (2 * l1 * d)
    a = math.acos(max(-1.0, min(1.0, cos_a)))
    ua = base - bend * a
    ex, ey = sh[0] + l1 * math.cos(ua), sh[1] + l1 * math.sin(ua)
    fa = math.atan2(tgt[1] - ey, tgt[0] - ex)
    return (math.degrees(ua), math.degrees(fa))


def _solve_arms(pose, far, far_bend, up, bend):
    """far = far-wrist target relative to the root (or None to keep far_arm);
    the near wrist is then put `up` px along the haft from the far wrist."""
    p = dict(pose)
    p["near_arm"] = (90, 90)
    if far is not None:
        p["far_arm"] = (90, 90)
    J = FIGURE.joints(p)
    b = FIGURE.b
    if far is not None:
        tgt = (J["pelvis"][0] + far[0], J["pelvis"][1] + far[1])
        p["far_arm"] = _ik(J["sh_far"], tgt, pose.get("far_upper_len", b["upper"]),
                           pose.get("far_fore_len", b["fore"]), far_bend)
        pose["far_arm"] = p["far_arm"]
        J = FIGURE.joints(p)
    if pose.get("near_arm") == "auto":
        wp = pose["weapon"]
        a = math.radians(wp["angle"])
        ox, oy = wp.get("off", (0, 0))
        wf = J["wr_far"]
        tgt = (wf[0] + ox + up * math.cos(a), wf[1] + oy + up * math.sin(a))
        pose["near_arm"] = _ik(J["sh_near"], tgt, pose.get("near_upper_len", b["upper"]),
                               pose.get("near_fore_len", b["fore"]), bend)
    return pose


def P(dx=0, far=(-1, 1), far_bend=1, up=HAND_UP, bend=1, extra=(), **kw):
    """Base pose: at rest, mace head on the ground in front, both hands on the haft.
    `far` is the far wrist relative to the pelvis (None keeps `far_arm`)."""
    base = dict(
        root=(RX + dx, 36), torso="front", head="normal", lean=(-1, 0),
        far_arm=(100, 130), near_arm="auto",
        near_leg=(120, 96), far_leg=(60, 86),
        near_boot="side", far_boot="front",
        near_hand=None, far_hand=None,
        extras=list(BASE_EXTRAS) + list(extra),
        weapon=dict(hand="far", angle=143, layer="top"),
        shadow=(11, 2),
    )
    base.update(kw)
    return _solve_arms(base, far, far_bend, up, bend)


def W(angle, variant="normal", layer="top", off=None):
    d = dict(hand="far", angle=angle, layer=layer)
    if variant != "normal":
        d["variant"] = variant
    if off:
        d["off"] = off
    return d


def slash(joint, r, a0, a1, width=5, dx=0, dy=0):
    """A swing arc centred on a joint (the far shoulder is the pivot)."""
    return (arc((0, 0), r - width, r, a0, a1), joint, dx, dy)


def at_head(part, angle, dx=0, dy=0):
    """An effect placed on the mace head."""
    hx, hy = head_offset(angle)
    return (part, "wr_far", hx + dx, hy + dy)


def animations():
    # --- idle: resting on the mace, a slow 1-px breathe (A B C B) --------------
    idle = [
        P(),
        P(lean=(-1, 1)),
        P(lean=(-1, 1), head_off=(0, 1), far=(-2, 1), weapon=W(144)),
        P(lean=(-1, 1)),
    ]

    # --- regular attack: hoist over the far shoulder, smash the ground --------
    lean = [
        P(dx=1, lean=(0, 0), far=(-2, -4), weapon=W(172)),
        P(dx=3, torso="back", lean=(1, 0), far=(5, -10), far_bend=-1, weapon=W(-94), bend=-1),
        P(dx=4, torso="back", lean=(2, 0), far=(7, -10), far_bend=-1, weapon=W(-68), bend=-1,
          near_leg=(112, 94), far_leg=(55, 84)),
    ]
    hold = [
        lean[2],
        P(dx=4, torso="back", lean=(2, -1), far=(7, -11), far_bend=-1, weapon=W(-70), bend=-1,
          near_leg=(112, 94), far_leg=(55, 84)),
    ]
    squat = dict(near_leg=(150, 108), far_leg=(30, 72))
    lunge = [
        # blur: the mace coming over the top
        P(dx=-2, torso="side", lean=(-2, 0), far=(-5, -20), far_bend=-1, bend=-1,
          near_leg=(130, 100), far_leg=(50, 82),
          weapon=W(-150, "blur"),
          effects=[slash("sh_far", 25, -55, -195, width=6)]),
        # impact: the head smashes the ground in front
        P(dx=-5, torso="side", lean=(-4, 3), far=(-8, 0), weapon=W(150), **squat,
          extra=[at_head(BUMP, 150, 0, 3)[:4] + ("back",)],
          effects=[at_head(STAR, 150), at_head(dust(0), 150)]),
        # follow-through: head still down, body settling
        P(dx=-5, torso="side", lean=(-4, 4), head_off=(-1, 1), far=(-9, -1), weapon=W(148), **squat,
          effects=[at_head(dust(1), 148, 1, 0)]),
    ]
    recover = [
        P(dx=-4, torso="side", lean=(-2, 1), far=(-6, -3), weapon=W(158),
          near_leg=(132, 100), far_leg=(48, 82)),
        P(dx=-2, lean=(-1, 0), far=(-3, -3), weapon=W(128)),
        P(dx=-1),
    ]

    # --- defence ---------------------------------------------------------------
    guard = dict(far=(7, 3), far_bend=-1, bend=-1, weapon=W(-160))
    block = [
        P(dx=1, lean=(0, 0), **guard),
        P(dx=2, lean=(1, 2), near_leg=(126, 100), far_leg=(54, 82), **guard),
    ]
    parry = [
        P(dx=1, lean=(0, 0), **guard),
        P(dx=-2, torso="side", lean=(-2, 0), far=(-7, -3), weapon=W(-112, "blur"), bend=-1,
          effects=[slash("wr_far", 19, -160, -100, width=4)]),
        P(dx=-3, torso="side", lean=(-2, 0), far=(-12, -8), weapon=W(-22), up=7, bend=-1,
          effects=[(SPARK, "wr_far", -6, 2)]),
    ]
    hit = [
        P(dx=1, head="hurt", lean=(0, 0), head_off=(1, 0), far=(0, 1)),
        P(dx=1, head="hurt", lean=(0, 1), head_off=(1, 1), far=(0, 1)),
    ]
    # Stagger (mace): too armoured to kneel. Rocks back on the heels, arms
    # out, the mace dropping to vertical; then a wide squat, hands on the
    # pommel, catching himself on the planted mace.
    stagger = [
        P(dx=5, head="hurt", lean=(4, 0), head_off=(2, 0),
          near_leg=(100, 80), far_leg=(76, 104), far_boot="back",
          far=(-4, -6), far_bend=-1, weapon=W(97, "solo"),
          near_arm=(182, 150), near_hand="open"),
        P(dx=4, head="hurt", lean=(-1, 2), head_off=(1, 1), far=(-3, -8), weapon=W(118), **squat),
        P(dx=3, head="normal", lean=(0, 1), far=(-3, -4), weapon=W(128),
          near_leg=(128, 100), far_leg=(52, 84)),
    ]

    # --- dodges: low, heavy hops -----------------------------------------------
    dodge_up = [
        P(dx=0, lean=(-1, 2), near_leg=(134, 104), far_leg=(46, 78), far=(-3, 1), weapon=W(150)),
        P(dx=-1, planted=False, root=(RX - 1, 29), lean=(-1, 0), shadow=(6, 1),
          near_leg=(150, 112), far_leg=(30, 84), near_boot="tip", far_boot="tip",
          far=(-4, -2), weapon=W(160)),
    ]
    dodge_down = [
        P(dx=0, lean=(-2, 2), near_leg=(135, 100), far_leg=(45, 80), far=(-3, 0), weapon=W(152)),
        P(dx=0, lean=(-3, 4), head_off=(-1, 1), near_leg=(160, 100), far_leg=(20, 82), far_boot="back",
          far=(-5, -1), weapon=W(168)),
    ]
    dodge_forward = [
        P(dx=-4, torso="side", lean=(-3, 0), shoulder_near_dx=-1, near_leg=(142, 96), far_leg=(66, 100),
          far=(-2, 0), weapon=W(150),
          effects=[(dash_lines(0, 0, 2, 7), "pelvis", 13, -4)]),
        P(dx=-8, lean=(-2, 0), near_leg=(114, 95), far_leg=(76, 95), far=(-2, 1), weapon=W(146)),
    ]
    dodge_back = [
        P(dx=4, lean=(2, 0), near_leg=(102, 82), far_leg=(62, 100), far=(-2, 0), weapon=W(150),
          effects=[(dash_lines(0, 0, 2, 7), "pelvis", -19, -2)]),
        P(dx=8, lean=(1, 0), near_leg=(128, 95), far_leg=(70, 90), far=(-1, 1), weapon=W(146)),
    ]

    # --- critical: the mace raised straight overhead, then a huge smash --------
    tall = dict(near_leg=(104, 92), far_leg=(76, 88))
    crit_lean = [
        P(dx=1, lean=(0, 0), far=(-3, -5), weapon=W(-158), bend=-1),
        P(dx=2, lean=(0, -1), far=(-7, -8), weapon=W(-100), bend=-1, **tall),
        P(dx=3, lean=(0, -1), far=(-8, -10), weapon=W(-88, "glint"), bend=-1, **tall),
    ]
    crit_hold = [
        crit_lean[2],
        P(dx=3, lean=(0, -1), far=(-8, -10), weapon=W(-88), bend=-1, **tall,
          effects=[at_head(STAR, -88, -1, 0)]),
    ]
    crit_lunge = [
        # blur 1: coming forward over the top
        P(dx=-2, lean=(-2, 0), far=(-4, -12), far_bend=-1, bend=-1, weapon=W(-135, "blur"),
          near_leg=(126, 98), far_leg=(54, 84),
          effects=[slash("sh_far", 26, -50, -175, width=6)]),
        # blur 2: horizontal in front, about to come down
        P(dx=-4, torso="side", lean=(-3, 1), far=(-7, -7), bend=-1, weapon=W(178, "blur"),
          near_leg=(134, 100), far_leg=(46, 80),
          effects=[slash("sh_far", 26, -110, -215, width=7)]),
        # impact: STAR + shockwave along the ground
        P(dx=-4, torso="side", lean=(-4, 3), far=(-7, 0), weapon=W(150), **squat,
          extra=[at_head(BUMP, 150, 0, 3)[:4] + ("back",)],
          effects=[at_head(STAR, 150), at_head(dust(0), 150), at_head(shockwave(9, 3), 150, 2, 3)]),
        # dust settling 1
        P(dx=-4, torso="side", lean=(-4, 4), head_off=(-1, 1), far=(-8, -1), weapon=W(148), **squat,
          extra=[at_head(BUMP, 148, 0, 4)[:4] + ("back",)],
          effects=[at_head(dust(1), 148), at_head(shockwave(10, 4, dotted=True), 148, 4, 4)]),
        # dust settling 2
        P(dx=-4, torso="side", lean=(-4, 3), far=(-8, -1), weapon=W(148), **squat,
          effects=[at_head(dust(2), 148)]),
    ]
    crit_recover = [
        P(dx=-4, torso="side", lean=(-2, 1), far=(-6, -3), weapon=W(158),
          near_leg=(132, 100), far_leg=(48, 82)),
        P(dx=-2, lean=(-1, 0), far=(-3, -3), weapon=W(128)),
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
