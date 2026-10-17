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


def _nearest(rgb):
    return min(((l, c) for l, c in PAL.map.items() if l != "o"), key=lambda lc: sum((a - b) ** 2 for a, b in zip(lc[1], rgb)))[0]


# overlays are written in ROLE letters and translated to whatever letters the extractor assigned this time
ROLE = {
    "c": _nearest((195, 129, 66)), "j": _nearest((232, 189, 123)), "l": _nearest((112, 56, 21)),      # skin mid / light / dark
    "f": _nearest((43, 77, 190)), "h": _nearest((27, 58, 150)), "a": _nearest((17, 36, 91)),         # blue light / mid / dark
    "b": _nearest((186, 202, 210)), "d": _nearest((105, 124, 138)), "k": _nearest((8, 8, 14)),       # steel light / mid, black
    "e": _nearest((32, 30, 45)), "g": _nearest((120, 141, 182)),                                     # dark cloth, blue-grey
}
TR = str.maketrans({k: v for k, v in ROLE.items()})


def R(text):
    return text.translate(TR)

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
        g.stretch(0, 0, BOX, TOP + 29, 0, -1)
    return g.tidy()


# ------------------------------------------------------------------ the open-arms torso
# The crossed arms (sprite rows 13-23, cols 3-29) are erased; the neck and shoulder tops (rows 10-12) stay.
# Over the gap: the suit's chest, a thick bare near arm ending in the dark glove, and the far arm.
CHEST = [R(s) for s in [          # stamped at sprite (9, 13)
    "kkffhhhhhaakk..",
    "kffffhhhhhaaak.",
    "kfffkhhhkhaaaak",
    "kffffkhkhhaaaak",
    "kfffffkhhhaaaak",
    "kffffhhhhhaaaak",
    "kffffhhhhhaaaak",
    ".kfffhhhhhaaak.",
    ".kfffhhhhhaaak.",
    ".kffhhhhhhaaak.",
    ".kkkkkkkkkkkkk.",
]]
# Arm anatomy at this scale (head = 14 px): shoulder at row 12, elbow at the belt (row ~24), wrist at row ~33,
# fingertips at mid-thigh (row ~40). Upper arm 6 px wide with the deltoid cap and biceps swell, forearm swelling
# just under the elbow then tapering to a 3-px wrist; the hanging arm hangs with a slight bend at the elbow.
# Light from the upper-left: j (light) on the outer-top planes, c (mid), l (dark) on the underside.
ARM_DOWN_NEAR = [R(s) for s in [  # stamped at sprite (2, 12)
    ".kkjjck.",     # 12 deltoid cap
    "kjjjjcck",     # 13
    "kjjjccclk",    # 14
    "kjjcccclk",    # 15 biceps
    "kjjcccclk",    # 16
    ".kjccclk.",    # 17
    ".kjccclk.",    # 18
    ".kcccllk.",    # 19
    ".kccclk..",    # 20 toward the elbow
    ".kcclk...",    # 21
    ".kkeek...",    # 22 elbow / glove cuff
    ".keeeek..",    # 23 forearm swell (gloved)
    ".keeeek..",    # 24
    ".kdeeek..",    # 25
    ".kdeeek..",    # 26
    "..kdeek..",    # 27
    "..kdeek..",    # 28 taper
    "..kdek...",    # 29
    "..kdek...",    # 30
    "..keek...",    # 31 wrist
    ".kdeeek..",    # 32 fist
    ".kdeeeek.",    # 33
    ".kdeeeek.",    # 34
    ".kkeeeek.",    # 35
    "..kkkkk..",    # 36
]]
ARM_UP_FAR = [R(s) for s in [     # stamped at sprite (23, 1): shoulder bottom-left, elbow top-right, forearm back to the hand at the hilt
    "...kjjcck.k.",   # 1 hand gripping the hilt (hilt drawn by the beat, passes behind)
    "..kjjjccclkk",   # 2 forearm, running right to the elbow
    "..kkcccccllk",   # 3
    "....kkkcclk.",   # 4 elbow point
    ".....kjcclk.",   # 5 upper arm, down-left to the shoulder
    "....kjjcclk.",   # 6
    "...kjjccllk.",   # 7
    "..kjjcccllk.",   # 8
    ".kjjcccllk..",   # 9
    "kjjccccllk..",   # 10 deltoid
    "kjccccllk...",   # 11
    ".kkkkkkk....",   # 12
]]
ARM_DOWN_FAR = [R(s) for s in [   # the far arm hanging behind the far side of the chest (partly hidden)
    "kjcck",
    "kjcclk",
    "kjcclk",
    "kccllk",
    ".kcllk",
    ".kcllk",
    ".kcclk",
    ".kcclk",
    ".kcllk",
    ".kcllk",
    ".kkllk",
    ".keeek",
    ".keeek",
    ".kkkk.",
]]


def open_torso(g, dx=0, dy=0, far="up"):
    """erase the crossed arms and lay the open chest + arms; far = 'up' (reaching) or 'down'"""
    g.clear(X_OFF + dx + 2, TOP + dy + 13, X_OFF + dx + 30, TOP + dy + 24)
    for i, row in enumerate(CHEST):
        P(g, 13 + i, 9, row, dx, dy)
    for i, row in enumerate(ARM_DOWN_NEAR):
        P(g, 12 + i, 2, row, dx, dy)
    if far == "up":
        for i, row in enumerate(ARM_UP_FAR):
            P(g, 1 + i, 23, row, dx, dy)
    else:
        for i, row in enumerate(ARM_DOWN_FAR):
            P(g, 13 + i, 25, row, dx, dy)


def blade(g, x, y, n, step, dx=0, dy=0):
    edge, mid, k = ROLE["b"], ROLE["d"], ROLE["k"]
    for i in range(n):
        px, py = x + step[0] * i, y + step[1] * i
        if step[1] == 0:
            P(g, py - 1, px, k, dx, dy); P(g, py, px, edge, dx, dy); P(g, py + 1, px, mid, dx, dy); P(g, py + 2, px, k, dx, dy)
        else:
            P(g, py, px, k + edge + mid + k, dx, dy)


def reach():
    """beat 2: arms unfold; the far hand goes up over the shoulder to the hilt"""
    g = body()
    open_torso(g, far="up")
    return g.tidy()


def draw_high():
    """beat 3: the sword comes off the back, raised up and behind the head"""
    g = body()
    open_torso(g, far="up")
    # the back sheath now empty: the little hilt that stuck up behind the head is gone
    g.clear(X_OFF + 27, TOP + 1, X_OFF + 34, TOP + 9)
    P(g, 0, 26, R("kllk")); P(g, -1, 27, R("kllk"))              # the hilt in the raised hand
    blade(g, 28, -2, 12, (1, -1))                                # blade up-right from the hilt
    return g.tidy()


SMEAR = [(y, x, R(t)) for y, x, t in [  # a wedge sweeping from over the head down to the front
    (-6, 20, "gbbbg"), (-4, 14, "gbbbbbbbbg"), (-2, 9, "gbbbbbbbbbbbbg"), (0, 5, "gbbbbbbbbbbbbbbbg"), (2, 2, "gbbbbbbbbbbbbbbbbg"),
    (4, 0, "ggbbbbbbbbbbbbbbbgg"), (6, -2, "gggbbbbbbbbbbbbggg"), (8, -4, "ggggbbbbbbbbbgggg"), (10, -6, "gggggbbbbbggggg"), (12, -8, "gggggggggggg"),
    (14, -9, "gggggggg"), (16, -10, "gggg"),
]]


def smear():
    g = body(dx=-2)
    open_torso(g, dx=-2, far="up")
    g.clear(X_OFF + 25, TOP + 1, X_OFF + 34, TOP + 9)
    for y, x, t in SMEAR:
        P(g, y + 6, x, t, -2)
    return g.tidy()


def slash():
    """beat 5: full extension — the torso leans in, the blade ends low in front"""
    g = body(dx=-4)
    g.shift_region(0, TOP, BOX, TOP + 29, -2, 0)             # the upper body leans toward the foe
    open_torso(g, dx=-6, far="down")
    g.clear(X_OFF + 21, TOP + 1, X_OFF + 32, TOP + 9)
    # the far arm swung down and forward past the near side: a full arm from the far shoulder to the hand
    SWING = [R(s) for s in [
        "...............kjjck",
        "..............kjjcclk",
        ".............kjjccllk",
        "...........kkjjccllk.",
        ".........kkjjcccllk..",
        ".......kkjjccccllk...",
        ".....kkjjccccllkk....",
        "...kkjjcccccllkk.....",
        ".kkjjcccccllkk.......",
        "kjjccccllkkk.........",
        "kjcccllkk............",
        "kccllkk..............",
        "kllkk................",
        "kkk..................",
    ]]
    for i, row in enumerate(SWING):
        P(g, 12 + i, 8, row, -6)
    P(g, 24, 6, R("kllk"), -6); P(g, 25, 5, R("kllk"), -6)   # the hilt in the hand
    blade(g, 4, 26, 10, (-1, 1), dx=-6)                       # blade down-left
    return g.tidy()


def recover():
    g = body(dx=-2)
    open_torso(g, dx=-2, far="down")
    g.clear(X_OFF + 25, TOP + 1, X_OFF + 34, TOP + 9)
    P(g, 24, 2, R("kcjk"), -2); P(g, 25, 1, R("kcck"), -2); P(g, 26, 1, R("kllk"), -2)
    blade(g, 0, 27, 9, (-1, 1), dx=-2)
    return g.tidy()


def select_frames():
    a = body(); b = reach()
    c = body(); open_torso(c, far="down")
    # eye flash: the visor slit glints
    d = c.copy(); P(d, 7, 12, R("bb")); P(d, 7, 16, R("bb"))
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
