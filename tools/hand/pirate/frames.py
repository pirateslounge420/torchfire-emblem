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
    g = Grid.from_text(os.path.join(HERE, f"{pose}.txt"), BOX, BOX, anchor_bottom=GROUND + dy, x_off=X_OFF + dx)
    g.dx, g.dy = dx, dy          # remembered so overlays can be placed in the body file's own coordinates
    return g


def P(g, y, x, text):
    """overlay in body-grid coordinates (row 0 = top of the 40-row body file, shifted with the
    body's dx/dy); '.' leaves the pixel alone"""
    g.put(y + (GROUND - 39) + g.dy, x + X_OFF + g.dx, text.replace(".", "?"))


def block(g, y, x, rows):
    """hand-drawn multi-row overlay ('.' = leave alone)"""
    for j, ln in enumerate(rows):
        P(g, y + j, x, ln)


# --- the broad axe: one bit, two heads wide. The crescent's horns run along the haft, the
# pale-yellow edge faces away from it; the haft passes through the eye (the C patch) and
# is drawn FIRST so the horn tips sit in front of it.
# edge DOWN, haft horizontal along the top; eye = the C patch at local cols 7-10, rows 2-5,
# with a short poll spike above it
AXE_DOWN = [
    ".......oMMo.......",
    ".......oMMo.......",
    "oo....oCCCCo....oo",
    "oYo...oCCCCo...oYo",
    "oYMo..oCCCCo..oMYo",
    "oYMMoooCCCCoooMMYo",
    "oYMMMMMMMMMMMMMMYo",
    ".oYWMMMMMMMMMMMYo.",
    ".oYWWMMMMMMMMMMYo.",
    "..oYWWMMMMMMMMYo..",
    "...oYYWWMMMMYYo...",
    "....ooYYYYYYoo....",
    "......oooooo......",
]
# edge UP-LEFT, haft at 45 degrees along the inner arc; eye where the haft meets the C patch
# (about local (9-10, 7-8)), poll spike off its lower-right
AXE_DIAG = [
    "...........ooo..",
    ".........ooMMMo.",
    ".......ooYMMMMMo",
    ".....ooYWWMMMMMo",
    "....oYWWMMMMMMo.",
    "...oYWMMMMMMMo..",
    "..oYWMMMMMMMo...",
    ".oYMMMMMMMCooo..",
    ".oYMMMMMMCoMMo..",
    "oYMMMMMMCo.oMMo.",
    "oYMMMMMCo...ooo.",
    "oYMMMMCo........",
    "oYMMMCo.........",
    ".oYMCo..........",
    "..ooo...........",
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
        g.shift_region(0, 0, BOX, GROUND - 14, 0, bob)      # head and torso breathe; hands and axe stay put
    # far forearm (bandaged) comes down across the sash to the rear hand
    P(g, 19, 20, "ozo"); P(g, 20, 19, "oszo"); P(g, 21, 17, "oCcko"); P(g, 22, 15, "oCcko"); P(g, 23, 13, "ocCko"); P(g, 24, 12, "oCko")
    # haft held level, pointing at the foe: rows 26-27 from the rear hand to 2 px past the eye
    P(g, 25, -7, "o" * 21); P(g, 26, -7, "L" * 21); P(g, 27, -7, "l" * 21); P(g, 28, -7, "o" * 21)
    block(g, 23, -11, AXE_DOWN)
    hand(g, 25, 11); hand(g, 25, 7)
    return g.tidy()


def axe_hung():
    """beat 2: the axe hangs straight down from stacked hands, head resting at the front foot"""
    g = body(dx=1)
    g.clear(X_OFF + 7, GROUND - 39 + 25, X_OFF + 12, GROUND - 39 + 29)     # the body's own hand
    P(g, 18, 20, "ozo"); P(g, 19, 18, "oszo"); P(g, 20, 16, "oCcko"); P(g, 21, 14, "ocCko")   # far forearm
    for y in range(20, 34):
        P(g, y, 9, "oLlo")
    block(g, 22, 7, rot_ccw(AXE_DOWN))
    hand(g, 22, 10); hand(g, 25, 9)
    return g.tidy()


def raised(tremble=0):
    """beat 3: twisted away, both hands up behind the head, the axe head high behind"""
    g = body("body_back", dx=-6, dy=tremble)
    for i in range(13):                               # haft from the butt up-right through both hands past the eye
        P(g, 8 - i, 35 + i, "oLlo")
    block(g, -10, 36, AXE_DIAG)
    for i in range(11):                               # the haft shows over the bit's back as far as the eye
        P(g, 8 - i, 35 + i, "oLlo")
    P(g, 2, 39, "oSSso"); P(g, 3, 39, "oSszo"); P(g, 4, 39, "osszo")      # far hand
    P(g, 5, 36, "oSSso"); P(g, 6, 36, "oSszo"); P(g, 7, 36, "oszzo")      # near hand
    return g.tidy()


SMEAR = [   # one pale arc over the head: thick blunt front at the left, thin tail trailing to the upper right
    (-14, 27, "YYWWWYY"), (-13, 23, "YYWWWWWWWWWWWYY"), (-12, 20, "YWWWWWWWWWWWWWWWWWWWY"),
    (-11, 18, "YWWWWWWWWWWWWWWWWWWWWWWWY"), (-10, 16, "YWWWWWWWWWWWWWWWWWWWWWWWWWWWY"),
    (-9, 15, "YWWWWWWWWY"), (-9, 36, "YWWWWWWWWY"), (-8, 14, "YWWWWWWWY"), (-8, 38, "YWWWWWWWY"),
    (-7, 13, "YWWWWWWWY"), (-7, 40, "YWWWWWY"), (-6, 13, "YWWWWWWY"), (-6, 42, "YWWWWY"),
    (-5, 12, "YWWWWWWY"), (-5, 44, "YWWY"), (-4, 12, "YWWWWWWY"), (-4, 46, "YY"),
    (-3, 12, "YWWWWWY"), (-2, 12, "YWWWWWY"), (-1, 13, "YWWWWY"), (0, 13, "YWWWWY"),
    (1, 14, "YWWWY"), (2, 15, "YWWY"), (3, 16, "YYY"),
]


def smear():
    """beat 4: the whole axe head becomes one pale wedge sweeping over the head"""
    g = body("body_back", dx=-8, dy=1)
    for y, x, t in SMEAR:
        P(g, y, x, t)
    return g.tidy()


def impact():
    """beat 5: crouched two-handed chop, the head buried at the foe's feet"""
    g = body("body_lunge", dx=-4)
    for i in range(16):                               # haft from the rear hand down-left, 3 px drop over its length
        P(g, 27 + i // 6, 8 - i, "o"); P(g, 28 + i // 6, 8 - i, "L"); P(g, 29 + i // 6, 8 - i, "l"); P(g, 30 + i // 6, 8 - i, "o")
    block(g, 28, -12, AXE_DOWN)
    hand(g, 26, 2); hand(g, 27, 6)
    return g.tidy()


def lower():
    """beat 6: hauling the axe back up out of the ground"""
    g = body("body_lunge", dx=-1)
    for i in range(14):
        P(g, 27 - i // 3, 7 - i, "o"); P(g, 28 - i // 3, 7 - i, "L"); P(g, 29 - i // 3, 7 - i, "l"); P(g, 30 - i // 3, 7 - i, "o")
    block(g, 21, -12, AXE_DOWN)
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
