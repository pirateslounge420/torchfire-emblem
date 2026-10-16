"""Cavalier (Heaven / violet) — hand-pixelled MOUNTED frames.

Three hand-drawn 80x60 bodies, horse and rider together (body.txt standing, body_back.txt
gathering / rearing slightly with the rider leaning back, body_lunge.txt full gallop stretch
with the rider leaning forward) plus hand-placed overlays for the lance arm, the lance and the
smear. The attack follows the six beats of the GBA Cavalier / Paladin lance sheets:
stance (lance couched low) -> lance couched back, horse gathering -> horse rearing slightly,
lance levelled -> one long pale streak as the horse launches -> full gallop, lance at full
extension -> settle back to a stand.

Run:  python3 tools/hand/cavalier/frames.py
  -> cavalier_attack.png / .gif next to this file, Godot sheet in godot/art/cavalier_v2/
"""
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
BODY_H = 60          # rows in a body grid

# 15 opaque colours (+ transparency). H is the smear core, h its violet-tinted fringe.
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
    """overlay in body-grid coordinates (row 0 = top of the 60-row body)"""
    g.put(y + (GROUND - (BODY_H - 1)) + dy, x + X_OFF + dx, text)


def lance(g, bx, by, tx, ty, dx=0, dy=0, head=8):
    """2-px lance from the butt (bx,by) to the tip (tx,ty) in body coords: leather shaft (L over l)
    with an outline, the last `head` px a steel head (M over m) with a white edge on its last 3 px."""
    n = abs(tx - bx)
    step = 1 if tx > bx else -1
    for i in range(n + 1):
        x = bx + step * i
        y = round(by + (ty - by) * i / n)
        if i >= n - 2:
            top, bot = "W", "o"
        elif i >= n - head:
            top, bot = "M", "m"
        else:
            top, bot = "L", "l"
        P(g, y - 1, x, "o", dx, dy); P(g, y, x, top, dx, dy); P(g, y + 1, x, bot, dx, dy); P(g, y + 2, x, "o", dx, dy)
    P(g, round(ty), tx + step, "o", dx, dy)


def hand(g, y, x, dx=0, dy=0):
    """3x3 gauntlet gripping the shaft, top-left at body (x, y)"""
    P(g, y, x, "ommo", dx, dy); P(g, y + 1, x, "omko", dx, dy); P(g, y + 2, x, "okko", dx, dy)


# --- frames -------------------------------------------------------------------
def idle(bob=0, flick=False):
    """beat 1: horse standing, lance couched low across the neck, near arm hanging from the pauldron"""
    g = body()
    lance(g, 40, 28, 8, 37)
    P(g, 24, 36, "omkko"); P(g, 25, 36, "omkko"); P(g, 26, 36, "omkko"); P(g, 27, 36, "okkko")
    P(g, 28, 35, "okkko"); P(g, 29, 34, "okkko")
    hand(g, 30, 33)
    if flick:                                                   # tail tip swings out, near ear turns
        g.shift_region(X_OFF + 62, GROUND - 59 + 50, X_OFF + 72, GROUND - 59 + 57, 1, 0)
        P(g, 13, 21, "oo"); P(g, 14, 20, "oKKo")
    if bob:                                                     # rider and barrel breathe; hooves stay
        g.shift_region(0, 0, BOX, GROUND - 16, 0, bob)
    return g.tidy()


def couched_back():
    """beat 2: horse gathering, rider leaning back, lance pulled back and couched under the arm"""
    g = body("body_back", dx=1)
    lance(g, 50, 34, 14, 27, dx=1)
    P(g, 25, 41, "omkko", 1); P(g, 26, 42, "omkko", 1); P(g, 27, 43, "okkko", 1); P(g, 28, 44, "okkko", 1)
    P(g, 29, 43, "okkko", 1); P(g, 30, 42, "okkko", 1)
    hand(g, 31, 40, 1)
    return g.tidy()


def levelled(tremble=0):
    """beat 3: horse rearing slightly, rider leaning back, lance levelled at the foe"""
    g = body("body_back", dy=tremble)
    lance(g, 46, 30, 6, 30, dy=tremble)
    P(g, 25, 40, "omkko", 0, tremble); P(g, 26, 41, "omkko", 0, tremble); P(g, 27, 41, "okkkko", 0, tremble)
    P(g, 28, 39, "okkkkko", 0, tremble); P(g, 29, 37, "okkkko", 0, tremble)
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
    """beat 6: back to a stand, the lance dropping from level toward the couched rest"""
    g = body(dx=-1)
    lance(g, 38, 28, 4, 34, dx=-1)
    P(g, 24, 35, "omkko", -1); P(g, 25, 34, "omkko", -1); P(g, 26, 33, "okkko", -1)
    P(g, 27, 32, "okkko", -1); P(g, 28, 31, "okkko", -1)
    hand(g, 29, 30, -1)
    return g.tidy()


def animations():
    return {
        "idle": ([idle(0), idle(1), idle(1, flick=True), idle(0)], 5, True),
        "lean": ([couched_back(), levelled(), levelled()], 10, False),
        "hold": ([levelled(), levelled(-1)], 5, True),
        "lunge": ([smear(), impact(), impact()], 20, False),
        "recover": ([settle(), idle(0), idle(0)], 9, False),
    }


def main():
    anims = animations()
    n = PAL.check([g for frames, _, _ in anims.values() for g in frames])
    imgs = {k: ([render(g, PAL) for g in frames], fps, loop) for k, (frames, fps, loop) in anims.items()}
    beats = [imgs["idle"][0][0], imgs["lean"][0][0], imgs["lean"][0][1], imgs["lunge"][0][0], imgs["lunge"][0][1], imgs["recover"][0][0]]
    strip(beats, os.path.join(HERE, f"{NAME}_attack.png"), zoom=5,
          labels=["stance", "couched back, gathering", "rearing, levelled", "smear", "full gallop thrust", "settle"])
    gif(beats + [imgs["idle"][0][0]], os.path.join(HERE, f"{NAME}_attack.gif"), [500, 120, 220, 70, 320, 160, 500])
    out_dir = os.path.join(HERE, "..", "..", "..", "godot", "art", f"{NAME}_v2")
    sheet(imgs, out_dir, NAME, BOX, ORIGIN)
    print(f"{NAME}: {sum(len(f) for f, _, _ in imgs.values())} frames, {n} colours -> {os.path.abspath(out_dir)}")


if __name__ == "__main__":
    main()
