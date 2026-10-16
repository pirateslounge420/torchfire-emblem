"""Monk — pure Earth (☷ over ☷, hexagram 2). Quarterstaff. Yellow.

A wiry fighting-monk: shaved head, thick dark brows, calm face; an ochre
wrap robe with a rope belt and a skirt split for kicking, sleeves to the
elbow, loose olive trousers, sandals. Fast and acrobatic: thrusts, vaults,
flying kicks. Drawn original in the GBA FE idiom; faces LEFT.
"""
import math
from pixelkit import Figure, Palette, grid, capsule, blade, arc, rot90_part
from pixelkit.palette import SKIN_TAN, OUTLINE, TRIGRAM
from pixelkit.figure import HANDS

NAME = "monk"
BOX = 64

# 15 opaque colours: tan skin (3), earth yellow (3), olive trousers (3),
# leather/wood (3), outline, white (= slash core E), slash edge e.
# Brows are leather shadow `j`; there is no hair ramp.
_olive = {"A": (150, 150, 110), "a": (100, 100, 70), "q": (58, 60, 42)}
PALETTE = Palette(NAME, {
    **SKIN_TAN,
    **TRIGRAM["earth"],
    **_olive,
    "L": (176, 128, 84), "l": (124, 84, 52), "j": (76, 48, 30),
})

# --- parts -----------------------------------------------------------------
# Shaved head, 3/4 view facing left. Anchor = neck (bottom centre).
HEAD = grid("""
...SSss...
..SSsssss.
.SSSssssss
.SSsssssss
.SSssssssz
.Sjjjssssz
.SSowSsszz
.SSsSsssz.
..ssssszz.
..zsssz...
...zzz....
""", anchor=(5, 11))

HEAD_HURT = grid("""
...SSss...
..SSsssss.
.SSSssssss
.SSsssssss
.SSssssssz
.Sjjjssssz
.SSooSsszz
.SSszsssz.
..sszsszz.
..zsssz...
...zzz....
""", anchor=(5, 11))

# Head bowed forward (crouches, the roll): crown toward the foe, face low.
HEAD_DOWN = grid("""
...SSss...
..SSsssss.
.SSSssssss
SSSsssssss
SSsssssssz
Sjjjsssssz
SowSssszz.
.SsSsszz..
..ssszz...
...zzz....
""", anchor=(5, 11))

# Torso, anchored at the neck (top centre). Wrap robe, V-neck, rope belt.
TORSO_FRONT = grid("""
....ss....
..CcsSsc..
.CccsSckkk
.CcccSkkkk
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
...ss...
.CcSsk..
.Cccckk.
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
....ss....
..cccsscC.
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

# Curled back for the forward roll; anchor = neck, which sits up-left of the pelvis.
TORSO_TUCK = grid("""
..CCccc.....
.Cccccccc...
.Cccccccckk.
.Ccccccckkk.
..ccccckkkk.
..lLlllkkkk.
...ccckkkk..
....kkkk....
""", anchor=(2, 0))

# Robe skirt below the belt; anchor = pelvis (top centre). Split at the front
# (left) so the near leg shows.
SKIRT = {
    "rest": grid("""
.Cccccckkkk
..Ccccckkkk
...cccckkkk
....ccckkk.
.....cckkk.
......ckk..
""", anchor=(5, 0)),
    "flare": grid("""
.Cccccckkkkk.
..Cccccckkkkkk
...ccccckkkkkk
.....cckkkkk..
.......kkk....
""", anchor=(5, 0)),
    "kick": grid("""
CCccccckkkk
Cccc...ckkk
Ccc....ckkk
cc......kkk
.........kk
""", anchor=(5, 0)),
    "fwd": grid("""
.Cccccckkk.
Ccccccc.kk.
Cccccc..k..
Cccc.......
cc.........
""", anchor=(5, 0)),
}

# Sandals: skin foot, leather strap and sole. Same 4-row height as the kit boots.
SANDALS = {
    "side": grid("""
..Sssz.
.Sslsz.
Ssssszz
jllllj.
""", anchor=(3, 0)),
    "front": grid("""
.Sssz.
Sslssz
sslszz
jllllj
""", anchor=(2, 0)),
    "back": grid("""
.zssS..
.zslsS.
zzsslsS
.jllllj
""", anchor=(3, 0)),
    "tip": grid("""
.Sss.
slssz
.ssz.
.jj..
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


def _swap_light(p):
    """Rotated parts keep their letters; swap hi/shadow so light stays upper-left."""
    return p.recolor({"S": "z", "z": "S", "C": "k", "k": "C", "A": "q", "q": "A", "L": "j", "j": "L"})


# Upside-down parts for the backflip frame (rotated 180° about the anchor).
HEAD_FLIP = _swap_light(rot90_part(HEAD, 2))
TORSO_FLIP = _swap_light(rot90_part(TORSO_FRONT, 2))


def dash_lines(x, y, n=3, length=8):
    p = grid("", anchor=(0, 0))
    for i in range(n):
        yy = y + i * 3
        for k in range(length - i * 2):
            p.pixels[(x + k, yy)] = "e" if k % 3 else "E"
    return p


def staff(angle, variant="normal"):
    """22-px wooden quarterstaff anchored at the grip, 1/3 along: 7 px of
    butt behind the hand, 15 px to the tip. `angle` is the direction of the tip."""
    r = math.radians(angle)
    dx, dy = math.cos(r), math.sin(r)

    def at(t):
        return (round(t * dx), round(t * dy))

    if variant == "blur":
        return blade(at(-6), at(18), width=4, letters=("E", "e", "e"), taper=0.4, edge=None)
    if variant == "spin":
        # twirled about the hand: the staff slides to its middle, a ring of blur around it
        p = capsule(at(-11), at(11), 2, ("L", "l", "j"), shade_px=(0, 1))
        return arc((0, 0), 9, 12, angle, angle + 360, letters=("e", "e")).union(p)
    p = capsule(at(-7), at(15), 2, ("L", "l", "j"), shade_px=(0, 1))
    for (x, y) in list(p.pixels):          # lighter bands near each end
        t = x * dx + y * dy
        if -6.5 <= t <= -4.5 or 11.5 <= t <= 13.5:
            p.pixels[(x, y)] = "L"
    if variant == "glint":
        tx, ty = at(15)
        for ox, oy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
            p.pixels[(tx + ox, ty + oy)] = "E"
    return p


FIGURE = Figure(
    build="medium", arm_w=4, leg_w=4,
    parts={"heads": {"normal": HEAD, "hurt": HEAD_HURT, "down": HEAD_DOWN, "flip": HEAD_FLIP},
           "torsos": {"front": TORSO_FRONT, "side": TORSO_SIDE, "back": TORSO_BACK,
                      "tuck": TORSO_TUCK, "flip": TORSO_FLIP},
           "boots": SANDALS,
           "extras": {**{"skirt_" + k: v for k, v in SKIRT.items()},
                      "fhand": HANDS["grip"], "star": STAR, "spark": SPARK}},
    sleeves=("S", "s", "z"),      # bare forearms; the rolled sleeve is drawn over the upper arm
    pants=("A", "a", "q"),
    weapon=staff,
)

# Same figure with the shoulders above the neck, for the one upside-down frame.
FIGURE_FLIP = Figure(
    build="medium", arm_w=4, leg_w=4, parts=FIGURE.parts,
    sleeves=("S", "s", "z"), pants=("A", "a", "q"), weapon=staff,
)
FIGURE_FLIP.b["shoulder_dy"] = -2

RX = 36   # resting root x; the opponent is to the left

# The staff lives in the "front" layer: over the torso and skirt, under the
# head is wrong for a staff held up, so the head is drawn before "front" and
# both hands (near arm, plus a copy of the far hand) go over the staff.
ORDER = ["shadow", "back", "far_arm", "far_leg", "mid", "torso", "near_leg",
         "head", "front", "near_arm", "top", "effects"]

U, F, SH = 6, 6, 4       # upper arm, forearm, shoulder half-width (medium build)


def ik(tx, ty, bend=1):
    """Two-link arm angles that put the wrist at (tx, ty) from the shoulder.
    bend=+1 swings the elbow clockwise (screen) off the shoulder->wrist line, -1 the other way."""
    d = math.hypot(tx, ty)
    reach = U + F - 0.05
    if d > reach:
        tx, ty = tx * reach / d, ty * reach / d
        d = reach
    th = math.degrees(math.atan2(ty, tx))
    al = math.degrees(math.acos(max(-1.0, min(1.0, (U * U + d * d - F * F) / (2 * U * d)))))
    ua = th + bend * al
    ex, ey = U * math.cos(math.radians(ua)), U * math.sin(math.radians(ua))
    fa = math.degrees(math.atan2(ty - ey, tx - ex))
    return (round(ua, 1), round(fa, 1))


def sleeve(ua):
    """The rolled robe sleeve: a loose capsule over the upper arm, anchored at the shoulder."""
    r = math.radians(ua)
    return capsule((0, 0), (round(U * math.cos(r)), round(U * math.sin(r))), 5, ("C", "c", "k"))


def dress(pose, fhand=True):
    """Add the sleeves (and a copy of the far hand over the staff) to a pose dict."""
    ex = list(pose.get("extras", []))
    ex.append((sleeve(pose["far_arm"][0]), "sh_far", 0, 0, "far_arm"))
    ex.append((sleeve(pose["near_arm"][0]), "sh_near", 0, 0, "near_arm"))
    if fhand:
        ex.append(("fhand", "wr_far", 0, 0, "near_arm"))
    pose["extras"] = ex
    return pose


def P(dx=0, skirt="rest", far=(1, 6), angle=150, along=8, bf=-1, bn=1,
      variant="normal", layer="front", off=(0, 0), two=True, fhand=True, **kw):
    """Base pose: light ready stance, staff low across the hips in both hands,
    tip toward the foe.

    far     = far wrist relative to the far shoulder; the staff grip sits there (+ off).
    angle   = staff direction (tip).  along = how far along the staff the near hand grips.
    bf / bn = elbow bend direction for the far / near arm (see ik).
    two     = compute the near arm so its hand lands on the staff.
    fhand   = draw a copy of the far hand over the staff (the far arm is behind the torso).
    """
    base = dict(
        root=(RX + dx, 38), torso="front", head="normal", lean=(-1, 0),
        near_leg=(115, 95), far_leg=(65, 90),
        near_boot="side", far_boot="front", near_hand="grip", far_hand="grip",
        extras=[("skirt_" + skirt, "pelvis", 0, 0, "front")],
        shadow=(9, 2), order=ORDER,
    )
    base["far_arm"] = ik(far[0], far[1], bf)
    base["weapon"] = dict(hand="far", angle=angle, variant=variant, layer=layer, off=off)
    if two:
        r = math.radians(angle)
        tx = far[0] + off[0] + along * math.cos(r) + 2 * SH
        ty = far[1] + off[1] + along * math.sin(r)
        base["near_arm"] = ik(tx, ty, bn)
    base.update(kw)
    return dress(base, fhand)


def slash(joint, r, a0, a1, width=5, dx=0, dy=0):
    """An arc effect centred on a joint (shoulder for staff sweeps, hip for kicks)."""
    return (arc((0, 0), r - width, r, a0, a1), joint, dx, dy)


def at_tip(part, angle, off=(0, 0), t=15, dx=0, dy=0):
    """Place an effect on the staff: t px along it from the grip (15 = tip, -7 = butt)."""
    r = math.radians(angle)
    return (part, "wr_far", round(off[0] + t * math.cos(r)) + dx, round(off[1] + t * math.sin(r)) + dy)


def butt_off(angle, k=7):
    """Weapon `off` that slides the far hand k px toward the butt (7 = gripping the very end)."""
    r = math.radians(angle)
    return (round(k * math.cos(r)), round(k * math.sin(r)))


def animations():
    # --- idle: a light bounce on the toes, staff across the body ---------------
    idle = [
        P(),
        P(lean=(-1, -1), near_boot="tip", far_boot="tip"),
        P(lean=(-1, -2), head_off=(0, -1), near_boot="tip", far_boot="tip", angle=148),
        P(lean=(-1, -1), near_boot="tip", far_boot="tip"),
    ]

    # --- regular attack: draw the staff back along the hip, thrust ------------
    lean = [
        P(dx=1, lean=(0, 0), far=(5, 8), angle=170, along=7, bn=1),
        P(dx=3, torso="back", lean=(1, 0), far=(4, 7), angle=178, along=7,
          near_leg=(110, 95), far_leg=(55, 85)),
        P(dx=4, torso="back", lean=(2, 0), far=(5, 7), angle=180, along=7,
          near_leg=(108, 95), far_leg=(52, 82)),
    ]
    hold = [
        lean[2],
        P(dx=4, torso="back", lean=(2, -1), far=(5, 6), angle=181, along=7,
          near_leg=(108, 95), far_leg=(52, 82)),
    ]
    lunge = [
        # blur: the staff streaks forward
        P(dx=-3, torso="side", lean=(-2, 0), far=(-8, 1), angle=180, along=7, variant="blur",
          near_leg=(135, 100), far_leg=(50, 80), skirt="flare",
          effects=[(dash_lines(0, 0, 2, 8), "pelvis", 8, -6)]),
        # impact: full thrust, spark at the tip
        P(dx=-9, torso="side", lean=(-3, 1), far=(-10, 0.5), angle=180, along=6,
          near_leg=(150, 98), far_leg=(40, 70), far_boot="back", skirt="flare",
          effects=[at_tip(SPARK, 180, dx=-1)]),
        # pulls back a touch
        P(dx=-8, torso="side", lean=(-3, 1), far=(-8, 1), angle=180, along=7,
          near_leg=(150, 98), far_leg=(40, 70), far_boot="back", skirt="flare"),
    ]
    recover = [
        # twirl it back
        P(dx=-6, torso="side", lean=(-2, 1), far=(-7, 7), angle=-150, along=4, variant="spin",
          near_leg=(140, 98), far_leg=(45, 75), far_boot="back", skirt="flare"),
        P(dx=-3, lean=(-1, 0), far=(-6, 7), angle=-110, along=7,
          near_leg=(125, 98), far_leg=(55, 85)),
        P(dx=-1),
    ]

    # --- defence -------------------------------------------------------------
    guard = dict(far=(-10, 7), angle=-100, along=7, bn=-1)
    block = [
        P(dx=1, lean=(0, 0), **guard),
        P(dx=2, lean=(1, 1), near_leg=(122, 100), far_leg=(58, 84), **guard),
    ]
    parry = [
        P(dx=1, lean=(0, 0), far=(-10, 7), angle=-105, along=7, bn=-1),
        # spinning deflect
        P(dx=-1, torso="side", lean=(-2, 0), far=(-9, 5), angle=-60, along=4, variant="spin"),
        # butt-strike: the back end snaps into the foe
        P(dx=-2, torso="side", lean=(-2, 0), far=(-9, 2), angle=15, along=7, bn=-1,
          near_leg=(135, 100), far_leg=(50, 80),
          effects=[at_tip(SPARK, 15, t=-8)]),
    ]
    hit = [
        P(dx=3, head="hurt", lean=(2, 1), head_off=(1, 0), far=(2, 10), angle=-130, along=7,
          near_leg=(105, 95), far_leg=(70, 95), skirt="fwd"),
        P(dx=2, head="hurt", lean=(2, 1), head_off=(1, 1), far=(2, 10), angle=-125, along=7,
          near_leg=(110, 95), far_leg=(65, 92), skirt="fwd"),
    ]
    # Stagger (staff): knocked back, jams the staff into the ground and hangs
    # off it, feet leaving the ground, then lands in a low crouch.
    stagger = [
        P(dx=6, head="hurt", lean=(3, 1), head_off=(1, 0), far=(-4, 9), angle=115, along=5,
          near_leg=(128, 108), far_leg=(45, 60), far_boot="back", skirt="fwd"),
        P(dx=5, head="hurt", lean=(1, 2), head_off=(0, 1), planted=False, root=(RX + 5, 31),
          far=(-6, 10), angle=105, off=butt_off(105, 5), along=-2, bn=-1,
          near_leg=(160, 60), far_leg=(120, 40), near_boot="tip", far_boot="tip",
          skirt="flare", shadow=(8, 1)),
        P(dx=4, head="normal", lean=(1, 2), head_off=(-1, 0), far=(-7, 3), angle=105, along=5,
          near_leg=(165, 100), far_leg=(30, 80), far_boot="back", skirt="flare"),
    ]

    # --- dodges ----------------------------------------------------------------
    dodge_up = [
        P(dx=0, lean=(-1, 2), near_leg=(132, 105), far_leg=(48, 75), far=(-3, 10), angle=-135),
        P(dx=-1, planted=False, root=(RX - 1, 22), lean=(-1, 0), shadow=(6, 1),
          near_leg=(190, 115), far_leg=(165, 100), near_boot="tip", far_boot="tip",
          far=(-4, 6), angle=-150, along=7, skirt="flare"),
    ]
    dodge_down = [
        P(dx=0, lean=(-2, 2), near_leg=(135, 100), far_leg=(45, 80), far=(-4, 9), angle=-140),
        # the splits, hanging on the planted staff
        P(dx=0, lean=(-2, 3), head="down", near_leg=(178, 180), far_leg=(2, 0), far_boot="back",
          far=(-8, -9), angle=90, off=butt_off(90, 7), along=-3, bn=-1, skirt="flare"),
    ]
    dodge_forward = [
        # a tucked forward roll
        P(dx=-6, planted=False, root=(RX - 6, 45), torso="tuck", lean=(-5, 5), head="down",
          head_off=(-3, 8), near_leg=(200, 80), far_leg=(215, 90), near_boot="tip", far_boot="tip",
          far=(-3, 5), angle=-35, along=6, skirt="flare", shadow=(8, 1),
          effects=[(dash_lines(0, 0, 2, 7), "pelvis", 8, -6)]),
        P(dx=-10, lean=(-2, 2), near_leg=(140, 100), far_leg=(50, 75), far=(-4, 9), angle=-140,
          skirt="flare"),
    ]
    dodge_back = [
        # backflip: upside down in the air (rendered with the flipped figure, see below)
        dress(dict(root=(RX + 6, 27), lean=(0, 22), torso="flip", head="flip", planted=False, shadow=(6, 1),
                   near_leg=(-120, -30), far_leg=(-100, -10), near_boot="tip", far_boot="tip",
                   near_boot_off=(0, -3), far_boot_off=(0, -3),
                   near_arm=(-150, -60), far_arm=(-30, -120), near_hand="grip", far_hand="grip",
                   weapon=dict(hand="far", angle=160, layer="front"),
                   extras=[("skirt_fwd", "pelvis", 0, 0, "front")], order=ORDER,
                   effects=[(dash_lines(0, 0, 2, 7), "pelvis", -18, 2)])),
        P(dx=10, lean=(1, 1), near_leg=(135, 100), far_leg=(45, 80), far=(-2, 10), angle=-135,
          skirt="flare"),
    ]

    # --- critical: plant the staff, coil, vault into a flying kick, spin strike --
    crit_lean = [
        P(dx=2, lean=(0, 0), far=(-7, 6), angle=100, along=5, bn=1),
        P(dx=3, lean=(1, 2), near_leg=(130, 102), far_leg=(50, 80),
          far=(-7, 5), angle=96, off=butt_off(96, 2), along=5, bn=1),
        P(dx=4, lean=(2, 3), head="down", head_off=(-1, 0), near_leg=(140, 105), far_leg=(45, 75),
          far=(-8, 4), angle=93, off=butt_off(93, 4), along=5, bn=1, variant="glint"),
    ]
    crit_hold = [
        crit_lean[2],
        P(dx=4, lean=(2, 3), head="down", head_off=(-1, 0), near_leg=(140, 105), far_leg=(45, 75),
          far=(-8, 4), angle=93, off=butt_off(93, 4), along=5, bn=1,
          effects=[at_tip(STAR, 93, off=butt_off(93, 4), t=-7, dy=-2)]),
    ]
    crit_lunge = [
        # vault: hands on top of the planted staff, legs swinging forward
        P(dx=-6, planted=False, root=(RX - 6, 30), lean=(-2, 0), shadow=(6, 1),
          far=(-4, 11), angle=100, off=butt_off(100, 7), along=-6, bn=-1,
          near_leg=(190, 160), far_leg=(150, 120), near_boot="side", far_boot="tip", skirt="kick",
          effects=[slash("hip_near", 15, 110, 175, width=5)]),
        # flying kick
        P(dx=-10, planted=False, root=(RX - 10, 26), torso="side", lean=(-3, 1), shadow=(7, 1),
          far=(3, 2), angle=-40, two=False, near_arm=(200, 170), near_hand="open",
          near_leg=(178, 178), far_leg=(120, 60), near_boot="side", far_boot="tip", skirt="kick",
          effects=[slash("hip_near", 17, 95, 170, width=6)]),
        # lands, whips the staff around
        P(dx=-10, lean=(-2, 1), far=(-8, 5), angle=-30, along=4, variant="spin",
          near_leg=(145, 100), far_leg=(45, 78), skirt="flare"),
        # spin strike impact
        P(dx=-11, torso="side", lean=(-3, 1), far=(-8, 0), angle=180, along=6,
          near_leg=(150, 98), far_leg=(40, 70), far_boot="back", skirt="flare",
          effects=[slash("sh_far", 26, -100, -185, width=7), at_tip(STAR, 180, dx=2)]),
        # follow-through
        P(dx=-11, torso="side", lean=(-3, 2), far=(-8, 1), angle=190, along=6,
          near_leg=(152, 100), far_leg=(38, 68), far_boot="back", skirt="flare"),
    ]
    crit_recover = [
        P(dx=-9, torso="side", lean=(-2, 1), far=(-7, 4), angle=-160, along=6,
          near_leg=(140, 98), far_leg=(45, 75), far_boot="back", skirt="flare"),
        P(dx=-4, lean=(-1, 0), far=(-5, 8), angle=-130, along=7,
          near_leg=(125, 98), far_leg=(55, 85)),
        P(dx=-1),
    ]

    # The upside-down backflip frame needs the shoulders above the neck.
    dodge_back[0] = FIGURE_FLIP.render(dodge_back[0])

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
