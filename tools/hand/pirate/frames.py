"""Pirate (Thunder / yellow, pure form Berserker) — hand-pixelled frames.

Three hand-drawn bodies (body.txt wide low stance, body_back.txt twisted-away
wind-up with both hands raised, body_lunge.txt folded-forward crouch with both
arms driven down) plus hand-placed overlays for the far arm, the big broad axe
and the smear. The attack follows the six beats of the GBA Brigand / Warrior
sheets: stance (axe low in front) → axe hung straight down, hands stacked →
raised overhead behind the head, two hands → one big smear over the head →
crouched two-handed chop buried at the foe's feet → the axe hauled back up.

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

# 15 opaque colours. W doubles as teeth, eye glint, steel edge glint and smear core;
# Y (pale yellow) is the axe edge glow and the smear fringe; C shades the steel by the socket.
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
    """overlay in body-grid coordinates (row 0 = top of the 40-row body)"""
    g.put(y + (GROUND - 39), x + X_OFF, text)


def PB(g, y, x, text):
    """overlay BEHIND the body: only writes onto empty pixels"""
    by, bx = y + (GROUND - 39), x + X_OFF
    for i, ch in enumerate(text):
        if ch == "?" or ch == ".":
            continue
        if 0 <= by < g.h and 0 <= bx + i < g.w and g.g[by][bx + i] == ".":
            g.g[by][bx + i] = ch


def block(g, y, x, rows, behind=False):
    """hand-drawn multi-row overlay ('.' = leave alone)"""
    for j, ln in enumerate(rows):
        (PB if behind else P)(g, y + j, x, ln.replace(".", "?"))


def haft(g, y, x, dyx, n, pat="oLlo"):
    """2-px haft from body coords (x,y); dyx = (dy, dx) per step; n steps"""
    dy, ddx = dyx
    for i in range(n):
        P(g, y + dy * i, x + ddx * i, pat)


# --- the axe head: one bit two heads wide, pale-yellow edge glow, steel body ------------
# edge DOWN (socket at the top, local cols 6-9): stance, impact, haul
AXE_DOWN = [
    "......oooo......",
    ".....oCCCCo.....",
    "....oCMMMMMo....",
    "...oCMMMMMMMo...",
    "..oMMMMMMMMMMo..",
    ".oMMMMMMMMMMMMo.",
    "oMMMMMMMMMMMMMMo",
    "oYWMMMMMMMMMMMYo",
    "oYYWWMMMMMMMYYYo",
    ".oYYYYYYYYYYYYo.",
    "..oooooooooooo..",
]
# edge UP-LEFT (socket at the lower right, local (13,11)): raised
AXE_DIAG = [
    "......oooo......",
    "....ooYYMMoo....",
    "...oYYWWMMMMo...",
    "..oYWMMMMMMMMo..",
    ".oYWMMMMMMMMMMo.",
    ".oYMMMMMMMMMMCo.",
    "oYMMMMMMMMMMMCo.",
    "oYMMMMMMMMMMCCo.",
    "oYMMMMMMMMMCCo..",
    "oYMMMMMMMMCCo...",
    ".oYMMMMMMMCo....",
    "..oYMMMMMCo.....",
    "...oYMMMo.......",
    ".....ooo........",
]


def mirror(rows):
    return [r[::-1] for r in rows]


def rot_ccw(rows):
    """rotate a block 90 degrees counter-clockwise (edge DOWN -> edge RIGHT)"""
    w = len(rows[0])
    return ["".join(r[c] for r in rows) for c in range(w - 1, -1, -1)]


# --- frames -------------------------------------------------------------------
def far_arm_stance(g):
    """far forearm curling in front of the belly to the rear hand on the haft"""
    P(g, 19, 18, "ozo"); P(g, 20, 16, "oszo"); P(g, 21, 15, "oCcko"); P(g, 22, 14, "ocCko")
    P(g, 23, 13, "oCcko")


def hands_stance(g):
    P(g, 24, 12, "oSSso"); P(g, 25, 12, "oSszo"); P(g, 26, 12, "oszzo"); P(g, 27, 13, "ooo")   # rear hand
    P(g, 25, 6, "oSSso"); P(g, 26, 6, "oSszo"); P(g, 27, 6, "oszzo"); P(g, 28, 7, "ooo")       # lead hand (over the haft)


def idle(bob=0):
    g = body()
    if bob:
        g.shift_region(0, 0, BOX, GROUND - 12, 0, bob)
    far_arm_stance(g)
    # haft held nearly level, pointing at the foe; head hanging edge-down in front of the shin
    for i in range(14):
        P(g, 26 + (1 if i > 6 else 0), 14 - i, "L")
        P(g, 27 + (1 if i > 6 else 0), 14 - i, "l")
        P(g, 25 + (1 if i > 6 else 0), 14 - i, "o")
        P(g, 28 + (1 if i > 6 else 0), 14 - i, "o")
    P(g, 25, 15, "o"); P(g, 26, 15, "o"); P(g, 27, 15, "o")
    block(g, 27, -9, AXE_DOWN)
    hands_stance(g)
    return g.tidy()


def axe_hung():
    """beat 2: the axe hangs straight down from stacked hands, head resting at the front foot"""
    g = body(dx=1)
    # far forearm comes down the front of the chest to the upper hand
    P(g, 18, 18, "ozo"); P(g, 19, 16, "oszo"); P(g, 20, 14, "oCcko"); P(g, 21, 13, "ocCko")
    # vertical haft from the upper hand down into the socket
    for i in range(10):
        P(g, 22 + i, 10, "oLlo")
    block(g, 30, 5, rot_ccw(AXE_DOWN))
    P(g, 22, 9, "oSSso"); P(g, 23, 9, "oSszo"); P(g, 24, 9, "oszzo")      # upper (rear) hand
    P(g, 26, 8, "oSSso"); P(g, 27, 8, "oSszo"); P(g, 28, 8, "oszzo"); P(g, 29, 9, "ooo")  # lead hand
    return g.tidy()


def raised(tremble=0):
    """beat 3: twisted away, both hands up behind the head, the axe head high behind"""
    g = body("body_back", dx=-5, dy=tremble)
    haft(g, 4, 39, (-1, 1), 8)                        # up-right through the hands to the socket
    P(g, 6, 38, "oLlo"); P(g, 7, 37, "oLlo")          # butt of the haft below the hands
    block(g, -10, 34, AXE_DIAG)
    # hands re-drawn over the haft
    P(g, 1, 38, "oSSso"); P(g, 2, 37, "oSoSszo"); P(g, 3, 37, "oSsozzo"); P(g, 4, 37, "oszzoo"); P(g, 5, 37, "ozzo")
    return g.tidy()


SMEAR = [
    (-13, 39, "YY"), (-12, 36, "YYWWY"), (-11, 33, "YYWWWWY"), (-10, 30, "YYWWWWWWY"),
    (-9, 28, "YWWWWWWWWY"), (-8, 26, "YWWWWWWWWWY"), (-7, 24, "YWWWWWWWWWWY"), (-6, 22, "YWWWWWWWWWWWY"),
    (-5, 21, "YWWWWWWWWWWWY"), (-4, 20, "YWWWWWWWWWWWY"), (-3, 19, "YWWWWWWWWWWWY"), (-2, 18, "YWWWWWWWWWWWY"),
    (-1, 18, "YWWWWWWWWWWY"), (0, 17, "YWWWWWWWWWWY"), (1, 17, "YWWWWWWWWWY"), (2, 17, "YWWWWWWWWY"),
    (3, 17, "YWWWWWWWY"), (4, 18, "YWWWWWWY"), (5, 18, "YWWWWWY"), (6, 19, "YWWWWY"), (7, 19, "YYYYY"),
]


def smear():
    """beat 4: the whole axe head becomes one pale wedge sweeping over the head"""
    g = body("body_back", dx=-7, dy=1)
    for y, x, t in SMEAR:
        P(g, y, x - 7, t)
    return g.tidy()


def impact():
    """beat 5: crouched two-handed chop, the head buried at the foe's feet"""
    g = body("body_lunge", dx=-4)
    for i in range(7):                                # haft from the hands down-left to the socket
        P(g, 27 + i // 2, 3 - i, "oLlo")
    block(g, 30, -13, AXE_DOWN)
    # hands over the haft
    P(g, 26, 1, "oSSso"); P(g, 27, 1, "oSszo"); P(g, 28, 1, "oszzo"); P(g, 29, 2, "ooo")
    P(g, 27, 5, "oSso"); P(g, 28, 5, "oszo"); P(g, 29, 6, "oo")
    return g.tidy()


def lower():
    """beat 6: hauling the axe back up out of the ground"""
    g = body("body_lunge", dx=-1)
    for i in range(8):
        P(g, 27 - i // 2, 3 - i, "oLlo")
    block(g, 23, -14, AXE_DOWN)
    P(g, 26, 1, "oSSso"); P(g, 27, 1, "oSszo"); P(g, 28, 1, "oszzo"); P(g, 29, 2, "ooo")
    P(g, 27, 5, "oSso"); P(g, 28, 5, "oszo"); P(g, 29, 6, "oo")
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
