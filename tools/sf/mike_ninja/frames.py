"""Mike's ninja (his own sprite, 34x69, Oct 16) — animation practice.

stance.txt is Mike's drawing, pulled off the photo at native resolution and quantized to 14
colours + outline. Nothing in the stance is redrawn; the animation moves regions of it and
lays small hand-drawn overlays (arm, sword, smear) on top per beat.

Animations: idle (8, breathing), select (unfold the arms into a guard and flash the eyes),
attack (6 beats: reach for the back sword → draw high → smear → slash → recover).
Box 80x80, ground row 75, origin (40, 76). Run: python3 tools/sf/mike_ninja/frames.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "hand"))
from handkit import Grid, Palette, render, strip, gif, sheet  # noqa: E402

NAME = "mike_ninja"
BOX, GROUND, X_OFF = 80, 75, 22
ORIGIN = (40, 76)
TOP = GROUND - 66          # the sprite's row 0 in the box

PAL = Palette(NAME, {l: tuple(int(v) for v in rest.split()) for l, rest in
                     (ln.strip().split(" ", 1) for ln in open(os.path.join(HERE, "palette.txt")) if ln.strip())})
# letters: N near-black (the sprite's own outline), E/G dark cloth, A/H/F/M blues, B/D steel, I/K blue-grey,
#          C/J/L skin (mid / light / dark). 'o' = our outline where the photo's red fringe was.

ARM_ROWS = (14, 28)        # the crossed-arms band in sprite rows


def body(dx=0, dy=0):
    return Grid.from_text(os.path.join(HERE, "stance.txt"), BOX, BOX, anchor_bottom=GROUND + dy, x_off=X_OFF + dx)


def P(g, y, x, text, dx=0, dy=0):
    """overlay in sprite coordinates"""
    g.put(TOP + y + dy, X_OFF + x + dx, text)


def breathe(k):
    """idle: everything above the belt rises 1 px and settles; the eyes glint on the top of the breath"""
    g = body()
    if k:
        g.shift_region(0, 0, BOX, TOP + 29, 0, -1)
    return g.tidy()


# ------------------------------------------------------------------ the open-arms torso
# the crossed arms are replaced by the suit's chest and two straight arms (overlays in sprite rows 14-28)
CHEST = [
    "...NNNNNNNNNN....",
    "..NFFHHMMHHFFN...",
    "..NFFHHMMHHFFAN..",
    ".NAFFHHMHHFFAAN..",
    ".NAFFHHMHHFFAAN..",
    ".NAAFFHHHFFAAAN..",
    ".NAAFFHHHFFAAAN..",
    ".NAAAFFHFFAAAEN..",
    ".NAAAAFFFAAAEEN..",
    ".NAAAAAFAAAEEEN..",
    "..NAAAAAAAEEEN...",
    "..NNNNNNNNNNNN...",
]
ARM_DOWN_NEAR = [          # the near arm hanging, fist by the hip
    "NCJN",
    "NCJCN",
    "NCCJCN",
    ".NCJCN",
    ".NCJCN",
    ".NCCLN",
    ".NJJCN",
    ".NCCLN",
    "..NNN.",
]
ARM_UP_FAR = [             # the far arm reaching up over the shoulder to the hilt
    ".NJCN",
    "NJCCN",
    "NCCLN",
    "NCLN.",
    "NCLN.",
    ".NN..",
]


def open_torso(g, dx=0, dy=0):
    """erase the crossed arms and lay the open chest + arms"""
    g.clear(X_OFF + dx + 2, TOP + dy + ARM_ROWS[0], X_OFF + dx + 32, TOP + dy + ARM_ROWS[1])
    for i, row in enumerate(CHEST):
        P(g, 15 + i, 9, row, dx, dy)
    for i, row in enumerate(ARM_DOWN_NEAR):
        P(g, 17 + i, 5, row, dx, dy)


def blade(g, x, y, n, step, dx=0, dy=0, edge="B", mid="D"):
    for i in range(n):
        px, py = x + step[0] * i, y + step[1] * i
        if step[1] == 0:
            P(g, py - 1, px, "N", dx, dy); P(g, py, px, edge, dx, dy); P(g, py + 1, px, mid, dx, dy); P(g, py + 2, px, "N", dx, dy)
        else:
            P(g, py, px, "N" + edge + mid + "N", dx, dy)


def reach():
    """beat 2: arms unfold; the far hand goes up over the shoulder to the hilt"""
    g = body()
    open_torso(g)
    for i, row in enumerate(ARM_UP_FAR):
        P(g, 9 + i, 22, row)
    return g.tidy()


def draw_high():
    """beat 3: the sword comes off the back, raised up and behind the head"""
    g = body()
    open_torso(g)
    # the back sheath now empty: the little hilt that stuck up behind the head is gone
    g.clear(X_OFF + 24, TOP + 1, X_OFF + 34, TOP + 10)
    for i, row in enumerate(ARM_UP_FAR):
        P(g, 6 + i, 20, row)
    P(g, 5, 20, "NLLN"); P(g, 4, 21, "NLLN")               # the hilt in the hand
    blade(g, 24, 3, 12, (1, -1))                            # blade up-right
    return g.tidy()


SMEAR = [  # a wedge sweeping from over the head down to the front
    (-6, 20, "KBBBK"), (-4, 14, "KBBBBBBBBK"), (-2, 9, "KBBBBBBBBBBBBK"), (0, 5, "KBBBBBBBBBBBBBBBK"), (2, 2, "KBBBBBBBBBBBBBBBBK"),
    (4, 0, "KKBBBBBBBBBBBBBBBKK"), (6, -2, "KKKBBBBBBBBBBBBKKK"), (8, -4, "KKKKBBBBBBBBBKKKK"), (10, -6, "KKKKKBBBBBKKKKK"), (12, -8, "KKKKKKKKKKKK"),
    (14, -9, "KKKKKKKK"), (16, -10, "KKKK"),
]


def smear():
    g = body(dx=-2)
    open_torso(g, dx=-2)
    g.clear(X_OFF + 22, TOP + 1, X_OFF + 32, TOP + 10)
    for y, x, t in SMEAR:
        P(g, y + 6, x, t, -2)
    return g.tidy()


def slash():
    """beat 5: full extension — the torso leans in, the blade ends low in front"""
    g = body(dx=-4)
    g.shift_region(0, TOP, BOX, TOP + 29, -2, 0)             # the upper body leans toward the foe
    open_torso(g, dx=-6)
    g.clear(X_OFF + 20, TOP + 1, X_OFF + 30, TOP + 10)
    # the far arm swung down and forward past the near side
    P(g, 20, 1, "NCJN", -6); P(g, 21, -1, "NJCCN", -6); P(g, 22, -3, "NCCLN", -6); P(g, 23, -4, "NLLN", -6)
    blade(g, -6, 24, 10, (-1, 1), dx=-6)                    # blade down-left
    return g.tidy()


def recover():
    g = body(dx=-2)
    open_torso(g, dx=-2)
    g.clear(X_OFF + 22, TOP + 1, X_OFF + 32, TOP + 10)
    P(g, 24, 2, "NCJN", -2); P(g, 25, 1, "NCCN", -2); P(g, 26, 1, "NLLN", -2)
    blade(g, 0, 27, 9, (-1, 1), dx=-2)
    return g.tidy()


def select_frames():
    a = body(); b = reach()
    c = body(); open_torso(c)
    for i, row in enumerate(["NJCN", "NCCN", "NLLN"]):
        P(c, 22 + i, 22, row)
    # eye flash: the visor slit glints
    d = c.copy(); P(d, 7, 12, "BB"); P(d, 7, 16, "BB")
    return [a, b, c, d, d, c, b, a]


def animations():
    return {
        "idle": ([breathe(0), breathe(0), breathe(1), breathe(1), breathe(1), breathe(1), breathe(0), breathe(0)], 6, True),
        "select": (select_frames(), 8, False),
        "lean": ([reach(), draw_high(), draw_high()], 10, False),
        "hold": ([draw_high(), draw_high()], 5, True),
        "lunge": ([smear(), slash(), slash()], 20, False),
        "recover": ([recover(), reach(), body()], 9, False),
    }


BEATS = ["stance", "reach", "draw high", "smear", "slash", "recover"]


def main():
    anims = animations()
    n = PAL.check([g for fr, _, _ in anims.values() for g in fr])
    beats = [body(), reach(), draw_high(), smear(), slash(), recover()]
    imgs = [render(g, PAL) for g in beats]
    strip(imgs, os.path.join(HERE, f"{NAME}_attack.png"), zoom=5, labels=BEATS)
    seq = [render(g, PAL) for g in anims["idle"][0]] + imgs + [imgs[0]]
    gif(seq, os.path.join(HERE, f"{NAME}_attack.gif"), [160] * 8 + [400, 160, 220, 70, 300, 200, 400], zoom=5)
    out_dir = os.path.join(HERE, "..", "..", "..", "godot", "art", f"{NAME}")
    rendered = {k: ([render(g, PAL) for g in fr], fps, loop) for k, (fr, fps, loop) in anims.items()}
    sheet(rendered, out_dir, NAME, BOX, ORIGIN, columns=8)
    print(f"{NAME}: {n} colours, {sum(len(f) for f, _, _ in anims.values())} frames -> {os.path.abspath(out_dir)}")


if __name__ == "__main__":
    main()
