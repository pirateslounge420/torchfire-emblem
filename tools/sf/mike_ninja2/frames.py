"""Mike's ninja #2 (arms at the sides, two swords on the back; his sprite, Oct 16) — basic animation.

Everything here moves Mike's own pixels: regions of the sprite are shifted, or cut out and re-placed
rotated (the arm as a unit). No redrawing except a smear and the blade.

Animations: idle (8, breathing), select (fists up into a guard), attack (5 beats: wind-up with the
near arm pulled back → punch out → smear → arm out → recover). Box 80x80, ground 75, origin (40, 76).
Run: python3 tools/sf/mike_ninja2/frames.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "hand"))
from handkit import Grid, Palette, render, strip, gif, sheet  # noqa: E402

NAME = "mike_ninja2"
BOX, GROUND, X_OFF = 80, 75, 22
ORIGIN = (40, 76)
SPRITE_H = 68
TOP = GROUND - (SPRITE_H - 1)

PAL = Palette(NAME, {l: tuple(int(v) for v in rest.split()) for l, rest in
                     (ln.strip().split(" ", 1) for ln in open(os.path.join(HERE, "palette.txt")) if ln.strip())})


def _nearest(rgb):
    return min(((l, c) for l, c in PAL.map.items() if l != "o"), key=lambda lc: sum((a - b) ** 2 for a, b in zip(lc[1], rgb)))[0]


STEEL_L, STEEL_M, BLACK, GREY = _nearest((186, 202, 210)), _nearest((105, 124, 138)), _nearest((8, 8, 14)), _nearest((120, 141, 182))

# sprite-space regions (x0, y0, x1, y1), measured off stance.txt
NEAR_ARM = (0, 12, 10, 41)       # shoulder to fist, near side (screen left)
FAR_ARM = (26, 12, 36, 41)
BELT = 27                        # sprite row of the belt


def body(dx=0, dy=0):
    return Grid.from_text(os.path.join(HERE, "stance.txt"), BOX, BOX, anchor_bottom=GROUND + dy, x_off=X_OFF + dx)


def S(x, y):
    """sprite coords -> box coords"""
    return X_OFF + x, TOP + y


SUIT = set("AEIK")          # the blue suit's letters: never part of an arm


def cut(g, region):
    """lift the ARM out of a sprite-space rectangle: skin, glove and armour pixels (plus the outline pixels
    touching them), leaving the blue suit and anything else in place. Returns a block ('.' = empty)."""
    x0, y0, x1, y1 = region
    bx, by = S(x0, y0)
    w, h = x1 - x0, y1 - y0
    raw = [[g.g[by + j][bx + i] for i in range(w)] for j in range(h)]
    core = [[(c not in SUIT and c not in ".No") for c in row] for row in raw]
    block = [["."] * w for _ in range(h)]
    for j in range(h):
        for i in range(w):
            c = raw[j][i]
            take = core[j][i] or (c in "No" and any(0 <= j + dj < h and 0 <= i + di < w and core[j + dj][i + di]
                                                   for dj, di in ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1))))
            if take:
                block[j][i] = c
                g.g[by + j][bx + i] = "."
    return block


def paste(g, block, x, y, rot=0):
    """put a block back at sprite (x, y); rot = 0/90/180/270 degrees clockwise"""
    for _ in range((rot // 90) % 4):
        block = [list(r) for r in zip(*block[::-1])]
    bx, by = S(x, y)
    for j, row in enumerate(block):
        for i, ch in enumerate(row):
            if ch != "." and 0 <= by + j < g.h and 0 <= bx + i < g.w:
                g.g[by + j][bx + i] = ch


def breathe(k):
    """idle: chest and head rise 1 px; the arms lag a frame behind"""
    g = body()
    if k >= 1:
        g.shift_region(0, TOP, BOX, TOP + BELT, 0, -1)
    if k == 1 or k == 3:
        for reg in (NEAR_ARM, FAR_ARM):
            x0, y0, x1, y1 = reg
            bx, by = S(x0, y0)
            g.shift_region(bx, by - 1, bx + (x1 - x0), by + (y1 - y0), 0, 1)
    return g.tidy()


def guard():
    """select: both fists come up — the forearms fold up at the elbow"""
    g = body()
    for reg, fx, fy in ((NEAR_ARM, 1, 10), (FAR_ARM, 27, 10)):
        blk = cut(g, reg)
        upper, fore = blk[:14], blk[14:]
        paste(g, upper, fx - 1 if reg is NEAR_ARM else fx + 1, 12)
        paste(g, fore, fx + 1 if reg is NEAR_ARM else fx - 1, 11, rot=180)        # forearm folded up over the upper arm, fist by the jaw
    return g.tidy()


def windup():
    """beat 1: the near fist pulls back to the hip, shoulders turn"""
    g = body()
    blk = cut(g, NEAR_ARM)
    paste(g, blk, 3, 14)                              # the near arm drawn back and a touch lower
    g.shift_region(*S(10, 8), *S(26, BELT), -1, 0)    # chest turns a hair
    return g.tidy()


def punch(dx=0):
    """beat 2/4: the near arm thrown straight out toward the foe"""
    g = body(dx=dx)
    blk = cut(g, NEAR_ARM)
    paste(g, blk, -17, 12, rot=90)                    # arm rotated to point left, pivoting at the shoulder
    g.shift_region(*S(0, 0), *S(36, BELT), -2, 0)     # the upper body leans into it
    return g.tidy()


def smear():
    g = punch()
    # a straight pale streak along the punch
    for i in range(14):
        g.put(TOP + 14, X_OFF - 19 - i, GREY)
        g.put(TOP + 15, X_OFF - 19 - i, STEEL_L)
        g.put(TOP + 16, X_OFF - 19 - i, STEEL_L)
        g.put(TOP + 17, X_OFF - 19 - i, STEEL_L)
        g.put(TOP + 18, X_OFF - 19 - i, GREY)
    return g.tidy()


def animations():
    return {
        "idle": ([breathe(0), breathe(0), breathe(1), breathe(2), breathe(2), breathe(3), breathe(0), breathe(0)], 6, True),
        "select": ([body(), guard(), guard(), guard(), body()], 8, False),
        "lean": ([windup(), windup(), windup()], 10, False),
        "hold": ([windup(), windup()], 5, True),
        "lunge": ([smear(), punch(-2), punch(-2)], 20, False),
        "recover": ([punch(), windup(), body()], 9, False),
    }


BEATS = ["stance", "guard", "wind-up", "smear", "punch"]


def main():
    anims = animations()
    n = PAL.check([g for fr, _, _ in anims.values() for g in fr])
    beats = [body(), guard(), windup(), smear(), punch(-2)]
    imgs = [render(g, PAL) for g in beats]
    strip(imgs, os.path.join(HERE, f"{NAME}_attack.png"), zoom=5, labels=BEATS)
    seq = [render(g, PAL) for g in anims["idle"][0]] + [render(g, PAL) for g in anims["select"][0]] + imgs[2:] + [imgs[0]]
    gif(seq, os.path.join(HERE, f"{NAME}_attack.gif"), [160] * 8 + [200] * 5 + [300, 70, 300, 400], zoom=5)
    out_dir = os.path.join(HERE, "..", "..", "..", "godot", "art", NAME)
    rendered = {k: ([render(g, PAL) for g in fr], fps, loop) for k, (fr, fps, loop) in anims.items()}
    sheet(rendered, out_dir, NAME, BOX, ORIGIN, columns=8)
    print(f"{NAME}: {n} colours, {sum(len(f) for f, _, _ in anims.values())} frames")


if __name__ == "__main__":
    main()
