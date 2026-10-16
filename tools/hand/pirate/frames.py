"""Pirate (Thunder / yellow, pure form Berserker) — hand-pixelled frames.

Three hand-drawn bodies (body.txt wide low stance, body_back.txt twisted-away
wind-up with both hands raised, body_lunge.txt folded-forward crouch with both
arms driven down) plus hand-placed overlays for the far arm, the big broad axe
and the smear. The attack follows the six beats of the GBA Brigand / Warrior
sheets: stance (axe level in front, edge down) → axe hung straight down from
stacked hands → raised overhead behind the head, two hands → one big smear over
the head → crouched two-handed chop buried at the foe's feet → the axe hauled
back up.

Run:  python3 tools/hand/pirate/frames.py
  -> pirate_attack.png / .gif next to this file, Godot sheet in godot/art/pirate_v2/
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from handkit import Grid, Palette, render, strip, gif, sheet  # noqa: E402

NAME = "pirate"
BOX = 64
GROUND = 53          # row the feet stand on
X_OFF = 18           # body grid column 0 -> box column
ORIGIN = (36, 54)

# 15 opaque colours. W doubles as teeth, eye glint, steel glint and smear core;
# Y (pale yellow) is the axe edge glow and the smear fringe; C shades the steel by the eye.
PAL = Palette(NAME, {
    "W": (248, 248, 248), "M": (152, 160, 184),
    "Y": (255, 236, 136), "y": (240, 186, 28), "v": (170, 116, 16),
    "S": (248, 208, 168), "s": (206, 146, 100), "z": (138, 86, 60),
    "C": (86, 84, 104), "c": (52, 50, 66), "k": (26, 24, 34),
    "L": (136, 86, 44), "l": (84, 52, 28),
    "h": (84, 54, 42),
})


def body(pose="body", dx=0, dy=0):
    return Grid.from_text(os.path.join(HERE, f"{pose}.txt"), BOX, BOX, anchor_bottom=GROUND + dy, x_off=X_OFF + dx)


def P(g, y, x, text):
    """overlay in body-grid coordinates (row 0 = top of the 40-row body); '.' leaves the pixel alone"""
    g.put(y + (GROUND - 39), x + X_OFF, text.replace(".", "?"))


def block(g, y, x, rows):
    """hand-drawn multi-row overlay ('.' = leave alone)"""
    for j, ln in enumerate(rows):
        P(g, y + j, x, ln)


# --- the broad axe: one bit, two heads wide. The crescent's horns run along the haft, the
# pale-yellow edge faces away from it; the haft passes through the eye (the C patch) and
# is drawn FIRST so the horn tips sit in front of it.
# edge DOWN, haft horizontal along the top (eye at local cols 7-10, rows 1-3)
AXE_DOWN = [
    "oo.....oooo.....oo",
    "oYo...oCCCCo...oYo",
    "oYMoo.oCCCCo.ooMYo",
    "oYMMMooCCCCooMMMYo",
    ".oYMMMMMMMMMMMMYo.",
    ".oYWMMMMMMMMMMMYo.",
    "..oYWWMMMMMMMMYo..",
    "...oYYWWMMMMYYo...",
    "....ooYYYYYYoo....",
    "......oooooo......",
]
# edge UP-LEFT, haft at 45 degrees along the inner arc (eye at local (7-8, 7-8))
AXE_DIAG = [
    "......ooooooo..",
    "....ooYYYMMMMoo",
    "...oYYWWMMMMMMo",
    "..oYWWMMMMMMMo.",
    ".oYWMMMMMMMMo..",
    ".oYMMMMMMMMo...",
    "oYMMMMMMMMo....",
    "oYMMMMMMCo.....",
    "oYMMMMMCo......",
    "oYMMMMCo.......",
    "oYMMMCo........",
    "oYMMCo.........",
    "oYMCo..........",
    "oYCo...........",
    "ooo............",
]


def rot_ccw(rows):
    """rotate a block 90 degrees counter-clockwise (edge DOWN -> edge RIGHT, haft vertical)"""
    w = len(rows[0])
    return ["".join(r[c] for r in rows) for c in range(w - 1, -1, -1)]


def hand(g, y, x):
    """3x3 fist with its outline"""
    P(g, y - 1, x - 1, "ooooo"); P(g, y, x - 1, "oSSso"); P(g, y + 1, x - 1, "oSszo"); P(g, y + 2, x - 1, "oszzo"); P(g, y + 3, x - 1, "ooooo")


# --- frames -------------------------------------------------------------------
def idle(bob=0):
    g = body()
    if bob:
        g.shift_region(0, 0, BOX, GROUND - 12, 0, bob)
    # far forearm (bandaged) comes down across the sash to the rear hand
    P(g, 19, 20, "ozo"); P(g, 20, 19, "oszo"); P(g, 21, 17, "oCcko"); P(g, 22, 15, "oCcko"); P(g, 23, 13, "ocCko"); P(g, 24, 12, "oCko")
    # haft held level, pointing at the foe: rows 26-27 from the rear hand to 2 px past the eye
    P(g, 25, -7, "o" * 21); P(g, 26, -7, "L" * 21); P(g, 27, -7, "l" * 21); P(g, 28, -7, "o" * 21)
    block(g, 25, -12, AXE_DOWN)
    hand(g, 25, 11); hand(g, 25, 7)
    return g.tidy()


def axe_hung():
    """beat 2: the axe hangs straight down from stacked hands, head resting at the front foot"""
    g = body(dx=1)
    g.clear(X_OFF + 6, GROUND - 39 + 25, X_OFF + 12, GROUND - 39 + 29)     # the body's own hand
    P(g, 18, 20, "ozo"); P(g, 19, 18, "oszo"); P(g, 20, 16, "oCcko"); P(g, 21, 14, "ocCko")   # far forearm
    for y in range(20, 34):
        P(g, y, 9, "oLlo")
    block(g, 23, 9, rot_ccw(AXE_DOWN))
    hand(g, 22, 10); hand(g, 25, 9)
    return g.tidy()


def raised(tremble=0):
    """beat 3: twisted away, both hands up behind the head, the axe head high behind"""
    g = body("body_back", dx=-6, dy=tremble)
    for i in range(11):                               # haft from the butt up-right through the hands to the eye
        P(g, 6 - i, 36 + i, "oLlo")
    block(g, -9, 37, AXE_DIAG)
    P(g, 1, 39, "oSSso"); P(g, 2, 37, "oSoSszo"); P(g, 3, 37, "oSsozzo"); P(g, 4, 37, "oszzoo"); P(g, 5, 37, "ozzo")
    return g.tidy()


SMEAR = [
    (-13, 41, "YY"), (-12, 38, "YYWWY"), (-11, 35, "YYWWWWY"), (-10, 32, "YYWWWWWWY"),
    (-9, 30, "YWWWWWWWWY"), (-8, 28, "YWWWWWWWWWY"), (-7, 26, "YWWWWWWWWWWY"), (-6, 24, "YWWWWWWWWWWWY"),
    (-5, 23, "YWWWWWWWWWWWY"), (-4, 22, "YWWWWWWWWWWWY"), (-3, 21, "YWWWWWWWWWWWY"), (-2, 20, "YWWWWWWWWWWWY"),
    (-1, 20, "YWWWWWWWWWWY"), (0, 19, "YWWWWWWWWWWY"), (1, 19, "YWWWWWWWWWY"), (2, 19, "YWWWWWWWWY"),
    (3, 19, "YWWWWWWWY"), (4, 20, "YWWWWWWY"), (5, 20, "YWWWWWY"), (6, 21, "YWWWWY"), (7, 21, "YYYYY"),
]


def smear():
    """beat 4: the whole axe head becomes one pale wedge sweeping over the head"""
    g = body("body_back", dx=-8, dy=1)
    for y, x, t in SMEAR:
        P(g, y, x - 8, t)
    return g.tidy()


def impact():
    """beat 5: crouched two-handed chop, the head buried at the foe's feet"""
    g = body("body_lunge", dx=-4)
    for i in range(16):                               # haft from the rear hand down-left, 3 px drop over its length
        P(g, 27 + i // 6, 8 - i, "o"); P(g, 28 + i // 6, 8 - i, "L"); P(g, 29 + i // 6, 8 - i, "l"); P(g, 30 + i // 6, 8 - i, "o")
    block(g, 30, -13, AXE_DOWN)
    hand(g, 26, 2); hand(g, 27, 6)
    return g.tidy()


def lower():
    """beat 6: hauling the axe back up out of the ground"""
    g = body("body_lunge", dx=-1)
    for i in range(14):
        P(g, 27 - i // 3, 7 - i, "o"); P(g, 28 - i // 3, 7 - i, "L"); P(g, 29 - i // 3, 7 - i, "l"); P(g, 30 - i // 3, 7 - i, "o")
    block(g, 22, -14, AXE_DOWN)
    hand(g, 26, 2); hand(g, 27, 6)
    return g.tidy()


def animations():
    return {
        "idle": ([idle(0), idle(1), idle(1), idle(0)], 5, True),
        "lean": ([axe_hung(), raised(), raised()], 10, False),
        "hold": ([raised(), raised(-1)], 5, True),
        "lunge": ([smear(), impact(), impact()], 20, False),
        "recover": ([lower(), idle(0), idle(0)], 9, False),
    }


def main():
    anims = animations()
    n = PAL.check([g for frames, _, _ in anims.values() for g in frames])
    imgs = {k: ([render(g, PAL) for g in frames], fps, loop) for k, (frames, fps, loop) in anims.items()}
    beats = [imgs["idle"][0][0], imgs["lean"][0][0], imgs["lean"][0][1], imgs["lunge"][0][0], imgs["lunge"][0][1], imgs["recover"][0][0]]
    strip(beats, os.path.join(HERE, f"{NAME}_attack.png"), zoom=5,
          labels=["stance", "axe hung low", "raised, two hands", "smear", "buried chop", "haul up"])
    gif(beats + [imgs["idle"][0][0]], os.path.join(HERE, f"{NAME}_attack.gif"), [500, 120, 220, 70, 320, 160, 500])
    out_dir = os.path.join(HERE, "..", "..", "..", "godot", "art", f"{NAME}_v2")
    sheet(imgs, out_dir, NAME, BOX, ORIGIN)
    print(f"{NAME}: {sum(len(f) for f, _, _ in imgs.values())} frames, {n} colours -> {os.path.abspath(out_dir)}")


if __name__ == "__main__":
    main()
