"""Cavalier (Heaven / violet) — hand-pixelled MOUNTED frames.

Five hand-drawn bodies, horse and rider together (80 wide): body.txt standing, body_idle.txt standing
with the near hind hoof cocked (rest), body_back.txt gathering / rearing slightly with the rider leaning
back, body_lunge.txt full gallop stretch with the rider leaning forward, body_rear.txt (76 rows) up on
the hind legs for the select flourish. The lance arm, lance, smears and dust are hand-placed overlays.

Animations
  idle     8 frames, at rest: horse standing, weight shifts (near hind hoof cocks and sets), head bobs,
           tail swishes, ear flicks; lance upright at the rider's side; cape drifts; rider breathes.
  select   10-frame one-shot flourish: gather -> half rear -> full rear, lance raised and twirled once
           (ring smear + afterimage) -> comes down -> lands with a dust puff -> rest pose.
  lean / hold / lunge / recover   the six beats of the GBA Cavalier / Paladin lance attack:
           stance -> lance couched back, horse gathering -> horse rearing slightly, lance levelled ->
           one long pale streak as the horse launches -> full gallop thrust -> settle back to rest.

Run:  python3 tools/hand/cavalier/frames.py
  -> cavalier_attack.png / .gif next to this file, Godot sheet in godot/art/cavalier_v2/
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from handkit import Grid, Palette, render, strip, gif, sheet  # noqa: E402

NAME = "cavalier"
BOX = 96
GROUND = 85          # row the hooves stand on
X_OFF = 8            # body grid column 0 -> box column (lunge frames get the room on the left)
ORIGIN = (48, 86)
BODY_H = 64          # rows in a standing body grid; body_rear is 76 (its row r = body row r - 12)
TOP = GROUND - (BODY_H - 1)   # box row of body row 0

# 15 opaque colours (+ transparency). H is the smear core, h its violet-tinted fringe (also dust fringe).
PAL = Palette(NAME, {
    "V": (196, 140, 255), "v": (126, 66, 220), "u": (66, 30, 134),        # violet ramp
    "W": (248, 248, 248), "M": (178, 182, 204), "m": (110, 112, 138),     # steel: edge, light, mid
    "k": (56, 54, 74), "K": (34, 30, 46),                                 # black plate / black mane, tail, barding
    "A": (164, 108, 80), "B": (120, 70, 52), "b": (72, 42, 36),           # dark bay coat
    "L": (116, 80, 48), "l": (64, 44, 28),                                # leather, lance shaft
    "H": (248, 248, 248), "h": (222, 204, 255),                           # smear core, violet-tinted fringe
})


def body(pose="body", dx=0, dy=0):
    return Grid.from_text(os.path.join(HERE, f"{pose}.txt"), BOX, BOX, anchor_bottom=GROUND + dy, x_off=X_OFF + dx)


def P(g, y, x, text, dx=0, dy=0):
    """overlay in body-grid coordinates (row 0 = top of the 64-row standing body; negative rows go above)"""
    g.put(y + TOP + dy, x + X_OFF + dx, text)


def px(g, y, x, c, dx=0, dy=0, behind=False):
    """one pixel in body coords; behind=True only paints onto transparency (the shaft passing behind the rider)"""
    yy, xx = y + TOP + dy, x + X_OFF + dx
    if 0 <= yy < g.h and 0 <= xx < g.w and (not behind or g.g[yy][xx] == "."):
        g.g[yy][xx] = c


def region(g, y0, x0, y1, x1, dx, dy):
    """shift_region in body coords (half-open rows/cols)"""
    g.shift_region(x0 + X_OFF, y0 + TOP, x1 + X_OFF, y1 + TOP, dx, dy)


# --- lance ------------------------------------------------------------------------
def lance(g, bx, by, tx, ty, dx=0, dy=0, head=8, behind=False):
    """2-px lance from the butt (bx,by) to the tip (tx,ty) in body coords, any angle: leather shaft (L over l,
    or L beside l when steeper than 45 degrees) with an outline, the last `head` px a steel head (M/m)
    with a white edge on the last 2 px and an outline cap past the tip."""
    n = max(abs(tx - bx), abs(ty - by))
    horiz = abs(tx - bx) >= abs(ty - by)
    for i in range(n + 1):
        t = i / n if n else 0
        x = round(bx + (tx - bx) * t)
        y = round(by + (ty - by) * t)
        if i >= n - 1:
            a, b = "W", "o"
        elif i >= n - head:
            a, b = "M", "m"
        else:
            a, b = "L", "l"
        if horiz:
            for k, c in ((-1, "o"), (0, a), (1, b), (2, "o")):
                px(g, y + k, x, c, dx, dy, behind)
        else:
            for k, c in ((-1, "o"), (0, a), (1, b), (2, "o")):
                px(g, y, x + k, c, dx, dy, behind)
    sx = (tx > bx) - (tx < bx)
    sy = (ty > by) - (ty < by)
    px(g, ty + (0 if horiz else sy), tx + (sx if horiz else 0), "o", dx, dy, behind)
    if horiz:
        px(g, ty + 1, tx + sx, "o", dx, dy, behind)
    else:
        px(g, ty + sy, tx + 1, "o", dx, dy, behind)


def afterimage(g, bx, by, tx, ty, dx=0, dy=0):
    """1-px pale ghost of where the lance just was (fringe colour, only over transparency)"""
    n = max(abs(tx - bx), abs(ty - by))
    for i in range(n + 1):
        t = i / n if n else 0
        px(g, round(by + (ty - by) * t), round(bx + (tx - bx) * t), "h", dx, dy, behind=True)


def ring(g, cx, cy, r, a0, a1, dx=0, dy=0, core=True):
    """ring smear of the twirl: an arc of radius r about the hand (cx,cy) from angle a0 to a1 (degrees,
    0 = toward the back/right, 90 = up, 180 = toward the foe). Core H 2 px with an h fringe. The upper half
    paints over everything, the lower half only behind the figure."""
    for y in range(cy - r - 3, cy + r + 4):
        for x in range(cx - r - 3, cx + r + 4):
            d = math.hypot(x - cx, y - cy)
            ang = math.degrees(math.atan2(cy - y, x - cx)) % 360
            if not (a0 <= ang <= a1):
                continue

            if core and r - 1.0 <= d <= r + 1.0:
                c = "H"
            elif r - 2.2 <= d <= r + 2.2:
                c = "h"
            else:
                continue
            px(g, y, x, c, dx, dy, behind=(y > cy))


def hand(g, y, x, dx=0, dy=0):
    """3x3 gauntlet gripping the shaft, top-left at body (x, y)"""
    P(g, y, x, "ommo", dx, dy); P(g, y + 1, x, "omko", dx, dy); P(g, y + 2, x, "okko", dx, dy)


def arm(g, pts, dx=0, dy=0):
    """thin plate arm: a chain of 2-px segments, each (row, col) = left end of 'okko'"""
    for y, x in pts:
        P(g, y, x, "okko", dx, dy)


# --- rest ---------------------------------------------------------------------------
REST_ARM = [(17, 36), (18, 36), (19, 36), (20, 35), (21, 35), (22, 34), (23, 33), (24, 33), (25, 32)]


def rest_lance(g, dx=0, dy=0):
    lance(g, 32, 52, 32, 4, dx, dy)
    arm(g, REST_ARM, dx, dy)
    hand(g, 26, 31, dx, dy)


def rest(step=0):
    """idle beats. step: 0 neutral | 1 breathe | 2 breathe + head bob | 3 + tail, ear | 4 hoof cocks, tail out
    | 5 hoof cocked, tail back | 6 cocked, cape drifts | 7 hoof sets, cape drifts"""
    g = body("body_idle" if step in (4, 5, 6) else "body")
    breathe = 1 if step in (1, 2, 3) else 0
    if breathe:                                   # rider sinks 1 px into the saddle (exhale); legs stay
        region(g, 2, 33, 33, 62, 0, 1)
    if step in (2, 3, 4):                         # horse head nods 1 px
        region(g, 12, 9, 31, 26, 0, 1)
    if step in (3, 4, 5):                         # tail tip swings out, near ear turns
        region(g, 46, 62, 62, 74, 2 if step == 4 else 1, 0)
        P(g, 13, 21, "oo"); P(g, 14, 20, "oKKo")
    if step in (6, 7):                            # cape drifts away from the back
        region(g, 28, 48, 38, 62, 1, 0)
    rest_lance(g, 0, breathe)
    return g.outline_missing(skip="Hh").tidy()


# --- attack beats -----------------------------------------------------------------------
def couched_back():
    """beat 2: horse gathering, rider leaning back, lance pulled back and couched under the arm"""
    g = body("body_back", dx=1)
    lance(g, 50, 34, 14, 27, dx=1)
    arm(g, [(25, 41), (26, 42), (27, 43), (28, 44), (29, 43), (30, 42)], 1)
    hand(g, 31, 40, 1)
    return g.tidy()


def levelled(tremble=0):
    """beat 3: horse rearing slightly, rider leaning back, lance levelled at the foe"""
    g = body("body_back", dy=tremble)
    lance(g, 46, 30, 6, 30, dy=tremble)
    arm(g, [(25, 40), (26, 41), (27, 41), (28, 39), (29, 37)], 0, tremble)
    hand(g, 29, 36, 0, tremble)
    return g.tidy()


def arm_extended(g, dx=0):
    """the thrusting arm, straight forward from the pauldron over the horse's head, gauntlet at the end"""
    P(g, 21, 21, "ooooooooo", dx)
    P(g, 22, 20, "ommmokkkk", dx)
    P(g, 23, 20, "omkkokkkk", dx)
    P(g, 24, 20, "okkkokkkko", dx)
    P(g, 25, 21, "ooooooooo", dx)


SMEAR = [
    (21, 10, "hhhhhhhhhhh"),
    (22, 2, "hhhHHHHHHHHHHHHHHHh"),
    (23, -12, "hhhhhHHHHHHHHHHHHHHHHHHHHHHHHHHHH"),
    (24, -4, "hhhhHHHHHHHHHHHHHHHHHHHHh"),
    (25, 6, "hhhhhhhhhhhhhhh"),
]


def smear():
    """beat 4: the horse launches; the lance is one long pale streak forward"""
    g = body("body_lunge", dx=4)
    for y, x, t in SMEAR:
        P(g, y, x, t, 4)
    arm_extended(g, 4)
    return g.tidy()


def impact():
    """beat 5: full gallop stretch, lance at full extension forward"""
    g = body("body_lunge", dx=-2)
    lance(g, 26, 23, -6, 23, dx=-2)
    arm_extended(g, -2)
    return g.tidy()


def settle():
    """beat 6: back to a stand, the lance dropping from level toward the ground"""
    g = body(dx=-1)
    lance(g, 38, 28, 4, 34, dx=-1)
    arm(g, [(24, 35), (25, 34), (26, 33), (27, 32), (28, 31)], -1)
    hand(g, 29, 30, -1)
    return g.tidy()


def raise_to_rest():
    """between settle and rest: the lance swings up through 45 degrees on its way to upright"""
    g = body()
    lance(g, 44, 42, 16, 10)
    arm(g, [(17, 36), (18, 36), (19, 35), (20, 34), (21, 33), (22, 32)])
    hand(g, 23, 30)
    return g.tidy()


# --- select flourish ---------------------------------------------------------------------
REAR_HAND = (37, -8)      # the raised gauntlet in the full-rear frames (body coords)
REAR_ARM = [(2, 40), (1, 40), (0, 39), (-1, 39), (-2, 38), (-3, 38), (-4, 37), (-5, 37), (-6, 36)]


def twirl_pts(ang, tip=20, butt=22):
    hx, hy = REAR_HAND
    c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    return round(hx - c * butt), round(hy + s * butt), round(hx + c * tip), round(hy - s * tip)


def twirl_lance(g, ang, behind_butt=False, behind_tip=False):
    """lance through the raised hand at angle `ang` (degrees, 0 back, 90 up, 180 forward)"""
    hx, hy = REAR_HAND
    bx, by, tx, ty = twirl_pts(ang)
    # butt half and tip half drawn separately so each can pass behind the figure
    lance(g, bx, by, hx, hy, head=0, behind=behind_butt)
    lance(g, hx, hy, tx, ty, behind=behind_tip)
    return (bx, by, tx, ty)


def gather():
    """s0: anticipation - horse tucks its head, rider lifts the upright lance a hand's width"""
    g = body()
    region(g, 12, 9, 31, 26, 0, 1)
    lance(g, 32, 42, 32, -6)
    arm(g, [(17, 36), (18, 35), (19, 34), (20, 33)])
    hand(g, 20, 31)
    return g.outline_missing(skip="Hh").tidy()


def half_rear():
    """s1: front hooves leave the ground; the lance swings back over the shoulder"""
    g = body("body_back")
    lance(g, 19, 27, 53, -7)
    arm(g, [(16, 40), (15, 39), (14, 38), (13, 37), (12, 36), (11, 35)])
    hand(g, 10, 35)
    return g.tidy()


def full_rear(beat):
    """s2-s6: up on the hind legs, lance overhead. beat 0 raised back | 1 swung forward, short arc |
    2 horizontal forward, big arc + afterimage | 3 back round, full ring | 4 upright, smear fading"""
    g = body("body_rear")
    hx, hy = REAR_HAND
    if beat == 0:
        twirl_lance(g, 60)
    elif beat == 1:
        ring(g, hx, hy, 19, 60, 125, core=False)
        twirl_lance(g, 120, behind_butt=True)
    elif beat == 2:
        ring(g, hx, hy, 19, 55, 185)
        twirl_lance(g, 175, behind_butt=True)
        bx, by, tx, ty = twirl_pts(120)            # ghost of beat 1's position
        afterimage(g, hx, hy, tx, ty)
    elif beat == 3:
        ring(g, hx, hy, 19, 0, 360)
        twirl_lance(g, 60)
    else:
        for y, x in ((-27, 30), (-29, 44), (-24, 52), (-20, 18), (-14, 56), (-26, 37)):
            px(g, y, x, "h", behind=True)
        twirl_lance(g, 80)
    arm(g, REAR_ARM)
    hand(g, hy, hx - 1)
    return g.tidy()


def coming_down():
    """s7: front hooves tucked and dropping, lance held high in front"""
    g = body("body_back", dy=-1)
    lance(g, 24, 26, 40, -14, dy=-1)
    arm(g, [(16, 40), (15, 38), (14, 36), (13, 34), (12, 33), (11, 32)], 0, -1)
    hand(g, 7, 31, 0, -1)
    return g.tidy()


def dust(g, fade=False):
    """dust puff at the front hooves on landing (steel greys with the pale violet fringe)"""
    if not fade:
        P(g, 55, 14, "..h.......h..")
        P(g, 56, 13, ".hMh.....hMh.")
        P(g, 57, 11, "hMWMh...hMWMh")
        P(g, 58, 10, "hMMmMh.hMmMMh")
        P(g, 59, 9, "hmMMmmh.hmmMMmh")
        P(g, 60, 8, "hmmMm?????mMmmh")
        P(g, 61, 7, "hmm?????????mmh")
        P(g, 62, 6, "hm???????????mh")
        P(g, 63, 36, ".hmmh")
        P(g, 62, 34, "..hMmh")
        P(g, 61, 36, "..hh")
    else:
        P(g, 54, 13, "h"); P(g, 56, 8, "hm"); P(g, 58, 5, "h"); P(g, 57, 24, "h")
        P(g, 60, 4, "hmh"); P(g, 62, 3, "h"); P(g, 59, 36, "hh"); P(g, 61, 39, "h")


def land():
    """s8: hooves slam down, dust kicks up, lance still high and dropping"""
    g = body()
    region(g, 2, 33, 33, 62, 0, 1)             # rider jolts down into the saddle
    region(g, 12, 9, 31, 26, 0, 1)             # head drops
    lance(g, 26, 36, 36, -6)
    arm(g, [(17, 36), (17, 34), (16, 32)])
    hand(g, 14, 30)
    dust(g)
    return g.outline_missing(skip="Hh").tidy()


def landed():
    """s9: rest pose with the dust thinning - chains straight into idle"""
    g = rest(0)
    dust(g, fade=True)
    return g


def animations():
    return {
        "idle": ([rest(i) for i in range(8)], 6, True),
        "select": ([gather(), half_rear(), full_rear(0), full_rear(1), full_rear(2), full_rear(3), full_rear(4),
                    coming_down(), land(), landed()], 10, False),
        "lean": ([couched_back(), levelled(), levelled()], 10, False),
        "hold": ([levelled(), levelled(-1)], 5, True),
        "lunge": ([smear(), impact(), impact()], 20, False),
        "recover": ([settle(), raise_to_rest(), rest(0)], 9, False),
    }


def main():
    anims = animations()
    n = PAL.check([g for frames, _, _ in anims.values() for g in frames])
    imgs = {k: ([render(g, PAL) for g in frames], fps, loop) for k, (frames, fps, loop) in anims.items()}
    sel = imgs["select"][0]
    beats = [imgs["idle"][0][0]] + sel + [imgs["lean"][0][0], imgs["lean"][0][1], imgs["lunge"][0][0], imgs["lunge"][0][1], imgs["recover"][0][0]]
    labels = ["rest", "gather", "half rear", "rear, lance up", "twirl 1", "twirl 2", "twirl 3", "twirl ends",
              "coming down", "lands, dust", "settles",
              "couched back", "rearing, levelled", "smear", "full gallop thrust", "settle"]
    strip(beats, os.path.join(HERE, f"{NAME}_attack.png"), zoom=5, labels=labels)
    gif(imgs["idle"][0] + sel + [imgs["lean"][0][0], imgs["lean"][0][1], imgs["lunge"][0][0], imgs["lunge"][0][1],
                               imgs["recover"][0][0], imgs["recover"][0][1], imgs["idle"][0][0]],
        os.path.join(HERE, f"{NAME}_attack.gif"),
        [160] * 8 + [100] * 10 + [120, 220, 70, 320, 160, 120, 500])
    out_dir = os.path.join(HERE, "..", "..", "..", "godot", "art", f"{NAME}_v2")
    sheet(imgs, out_dir, NAME, BOX, ORIGIN)
    print(f"{NAME}: {sum(len(f) for f, _, _ in imgs.values())} frames, {n} colours -> {os.path.abspath(out_dir)}")


if __name__ == "__main__":
    main()
