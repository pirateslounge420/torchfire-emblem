"""Shinobi (Fire / red) — hand-pixelled frames.

Three hand-drawn bodies (body.txt low crouch, body_back.txt lean-back with the
near arm raised, body_lunge.txt deep lunge with the near arm thrust out) plus
hand-placed overlays for the kusarigama: the sickle in the far hand, the chain
and its 3x3 iron weight in the near hand, the sash tail, the whirl ring and the
streak. The attack follows the six beats of the GBA sheets, read as a flail:
stance (chain coiled, sickle back) → weight swung back behind the body →
weight whirling overhead → one long streak shooting forward → impact at full
extension with the chain taut → yank, the chain snapping back and the sickle
coming up.

Run:  python3 tools/hand/shinobi/frames.py
  -> shinobi_attack.png / .gif next to this file, Godot sheet in godot/art/shinobi_v2/
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from handkit import Grid, Palette, render, strip, gif, sheet  # noqa: E402

NAME = "shinobi"
BOX = 64
GROUND = 53          # row the feet stand on
X_OFF = 8            # body grid column 0 -> box column
ORIGIN = (26, 54)         # ground point between the stance feet

# 14 opaque colours. H/h double as steel edge, chain and smear; g is iron (chain links, weight).
PAL = Palette(NAME, {
    "H": (248, 248, 248), "h": (178, 186, 204), "g": (104, 110, 130),   # steel edge, steel, iron/chain
    "S": (236, 190, 150), "s": (182, 126, 94),                          # skin (eye slot, hands)
    "K": (130, 136, 164), "k": (80, 84, 110), "n": (46, 50, 72),        # black cloth: highlight, mid, shadow
    "R": (236, 52, 52), "r": (164, 22, 36), "q": (96, 8, 26),           # red ramp (trigram)
    "L": (118, 84, 56), "l": (70, 48, 32),                              # bandage / wrap
})


def body(pose="body", dx=0, dy=0):
    return Grid.from_text(os.path.join(HERE, f"{pose}.txt"), BOX, BOX, anchor_bottom=GROUND + dy, x_off=X_OFF + dx)


def P(g, y, x, text, dx=0):
    """overlay in body-grid coordinates (row 0 = top of the 40-row body); '?' skips.
    dx = the body's own shift, so overlays stay attached to a shifted body."""
    g.put(y + (GROUND - 39), x + X_OFF + dx, text)


def U(g, y, x, text, dx=0):
    """like P but only onto transparent pixels: draws BEHIND what is already there"""
    yy = y + (GROUND - 39)
    for i, ch in enumerate(text):
        xx = x + X_OFF + dx + i
        if ch != "?" and 0 <= yy < g.h and 0 <= xx < g.w and g.g[yy][xx] == ".":
            g.g[yy][xx] = ch


def weight(g, y, x, dx=0):
    """3x3 iron weight with its top-left fill pixel at body (x, y), outlined"""
    for j, row in enumerate(("ooooo", "oHggo", "ogggo", "ogggo", "ooooo")):
        P(g, y - 1 + j, x - 1, row, dx)


def chain(g, pts, dx=0, put=None):
    """1-px chain through body points: 2-px links alternating steel / iron"""
    put = put or P
    for i, (y, x) in enumerate(pts):
        put(g, y, x, "h" if (i // 2) % 2 == 0 else "g", dx)


def blade_down(g, y, x, dx=0):
    """6-px sickle blade hanging from the handle end at body (x, y), curving in; edge (H) inside"""
    P(g, y - 1, x, "oo", dx); P(g, y, x - 1, "oHho", dx); P(g, y + 1, x, "Hho", dx); P(g, y + 2, x - 1, "oHho", dx)
    P(g, y + 3, x - 1, "oHho", dx); P(g, y + 4, x - 2, "oHho", dx); P(g, y + 5, x - 3, "oHho", dx); P(g, y + 6, x - 4, "oHo", dx)
    P(g, y + 7, x - 4, "oo", dx)


def blade_up(g, y, x, dx=0):
    """6-px sickle blade rising from the handle end at body (x, y) and curving forward (left)"""
    P(g, y + 1, x - 1, "oooo", dx); P(g, y, x, "Hho", dx); P(g, y - 1, x - 1, "oHho", dx); P(g, y - 2, x - 1, "oHho", dx)
    P(g, y - 3, x - 2, "oHho", dx); P(g, y - 4, x - 3, "oHho", dx); P(g, y - 5, x - 4, "oHHo", dx); P(g, y - 6, x - 5, "oHo", dx)
    P(g, y - 7, x - 5, "oo", dx)


def sickle_back(g, dx=0):
    """far arm from the far shoulder down-back to a hand at hip height holding the sickle level
    behind the body, blade hanging and curving in. Used for the stance / swing-back / whirl beats."""
    P(g, 15, 23, "kko", dx); P(g, 16, 24, "RRo", dx); P(g, 17, 24, "oRro", dx)
    P(g, 18, 25, "okko", dx); P(g, 19, 25, "oknko", dx); P(g, 20, 26, "oLlo", dx); P(g, 21, 27, "oLlo", dx)
    P(g, 22, 27, "oSSsoooooooo", dx); P(g, 23, 27, "oSssLLLLLLL", dx); P(g, 24, 27, "osssoooooooo", dx)
    P(g, 25, 27, "ooooo", dx)
    blade_down(g, 23, 38, dx)


def sash_tail(g, y, x, whip=0, dx=0):
    """2-px red ribbon trailing from the sash's back end at body (x, y): 0 hanging, 1 lifted, 2 streaming"""
    if whip == 0:
        P(g, y - 1, x, "ooo", dx); P(g, y, x, "Rrro", dx); P(g, y + 1, x + 1, "oqrro", dx); P(g, y + 2, x + 3, "oqro", dx)
        P(g, y + 3, x + 4, "oqo", dx); P(g, y + 4, x + 4, "oo", dx)
    elif whip == 1:
        P(g, y - 1, x, "oooo", dx); P(g, y, x, "Rrrro", dx); P(g, y + 1, x + 1, "oorrro", dx); P(g, y + 2, x + 4, "oqro", dx)
        P(g, y + 3, x + 5, "oo", dx)
    else:
        P(g, y - 1, x, "ooooooo", dx); P(g, y, x, "RRRrrrroo", dx); P(g, y + 1, x, "orrrqqqrro", dx); P(g, y + 2, x + 2, "oooqqqqo", dx)
        P(g, y + 3, x + 5, "oooo", dx)


# --- frames -------------------------------------------------------------------
def idle(bob=0, swing=0):
    """beat 1: low crouch, chain coiled in the near fist, weight dangling, sickle held back"""
    g = body()
    if bob:
        g.shift_region(0, 0, BOX, GROUND - 12, 0, bob)
    sickle_back(g)
    sash_tail(g, 22, 25, 0)
    # chain looped twice across the fist, one link out of the bottom, the weight dangling below
    P(g, 25 + bob, 6, "hgh"); P(g, 26 + bob, 6, "ghg")
    P(g, 27 + bob, 4, "ho")
    chain(g, [(28 + bob, 3 + swing)])
    weight(g, 30 + bob, 2 + swing)
    return g.tidy()


def swing_back():
    """beat 2: the weight swung back behind the body, chain crossing the front thigh"""
    g = body(dx=1)
    sickle_back(g, 1)
    sash_tail(g, 22, 25, 0, 1)
    P(g, 25, 6, "hgh", 1); P(g, 26, 6, "ghg", 1)
    # chain leaves the fist down-back over the near thigh; the weight hangs low behind it, at the
    # bottom of the pendulum swing, in the gap between the shins
    chain(g, [(27, 8), (27, 9), (28, 10), (28, 11), (29, 12), (29, 13), (30, 14), (30, 15), (31, 16), (31, 17), (32, 18)], 1)
    weight(g, 33, 20, 1)
    return g.tidy()


RING = [(-5, 0), (-5, 1), (-4, -2), (-4, -1), (-4, 2), (-4, 3), (-3, -3), (-3, 4), (-2, -4), (-2, 5),
        (-1, -5), (-1, 5), (0, -5), (0, 6), (1, -5), (1, 6), (2, -4), (2, 5), (3, -3), (3, 4),
        (4, -2), (4, -1), (4, 2), (4, 3), (5, 0), (5, 1)]


def whirl(tremble=0):
    """beat 3: body leaning away, the near hand high, the weight whirling in a pale ring around it"""
    g = body("body_back", dx=-3, dy=tremble)
    sickle_back(g, -1)
    sash_tail(g, 22, 25, 1, -2)
    cx, cy = 32, 2 + tremble            # hand centre (body coords); ring radius ~5
    for dy, dx in RING:
        U(g, cy + dy, cx + dx, "H" if dy <= -3 or (dy <= 0 and dx < 0) else "h", -3)
    # the weight itself, smeared, at the front of the ring (upper left)
    U(g, cy - 4, cx - 3, "gg", -3); U(g, cy - 3, cx - 4, "Hg", -3); U(g, cy - 2, cx - 5, "g", -3)
    return g.tidy()


def smear():
    """beat 4: the chain and weight become one long pale streak shooting forward and down"""
    g = body("body_back", dx=-5, dy=1)
    sickle_back(g, -3)
    sash_tail(g, 22, 25, 1, -4)
    # comet streak from the top of the whirl (body (30,-2)) arcing over the hood and dipping to the
    # foe's chest: a 1-px tail at the hand thickening to 4 px, no outline, the weight a pale blur
    x0, y0, n = 30, -2, 30
    for i in range(n):
        x = x0 - i
        y = y0 + (i * i * 24) // (n * n)
        if i < 6:
            P(g, y, x, "h", -5)
        elif i < 13:
            P(g, y, x, "H", -5); P(g, y + 1, x, "h", -5)
        elif i < 21:
            P(g, y - 1, x, "h", -5); P(g, y, x, "H", -5); P(g, y + 1, x, "h", -5)
        else:
            P(g, y - 1, x, "h", -5); P(g, y, x, "H", -5); P(g, y + 1, x, "H", -5); P(g, y + 2, x, "h", -5)
    xh, yh = x0 - n, y0 + 24            # head of the streak: the weight, still a blur
    P(g, yh - 2, xh - 1, "hhh", -5); P(g, yh - 1, xh - 2, "hHHHh", -5); P(g, yh, xh - 3, "hHgHHH", -5)
    P(g, yh + 1, xh - 2, "hHgHH", -5); P(g, yh + 2, xh - 1, "hhhh", -5)
    return g.tidy()


def impact():
    """beat 5: full extension — the weight out front, chain taut, body lunged, sash streaming back"""
    g = body("body_lunge", dx=8)
    # far arm trailing straight back at shoulder height, sickle level behind, blade rising
    P(g, 21, 22, "ooooooooo", 8); P(g, 22, 22, "kkkLLlSSsoooooooo", 8); P(g, 23, 22, "kkkLllSssLLLLLL", 8)
    P(g, 24, 23, "oooooosssooooooo", 8); P(g, 25, 28, "ooooo", 8)
    blade_up(g, 23, 37, 8)
    sash_tail(g, 27, 26, 2, 8)
    # taut chain leftward from the hand (hand x 1-3, rows 22-24) and the weight at full extension
    chain(g, [(23, -1 - i) for i in range(11)], 8)
    weight(g, 22, -15, 8)
    # the last of the streak still fading behind the weight
    P(g, 21, -10, "hh", 8); P(g, 25, -10, "hh", 8)
    return g.tidy()


def yank():
    """beat 6: the chain snapping back into a wave, the sickle coming up over the shoulder"""
    g = body("body_lunge", dx=4)
    # far arm up and back behind the hood tails, hand above them, the sickle raised over the head
    U(g, 20, 21, "okko", 4); U(g, 19, 22, "okko", 4); U(g, 18, 22, "okko", 4); U(g, 17, 23, "oRRo", 4); U(g, 16, 23, "oRro", 4)
    U(g, 15, 24, "oLlo", 4); U(g, 14, 24, "oLlo", 4); U(g, 13, 24, "oLlo", 4)
    P(g, 9, 24, "ooooo", 4); P(g, 10, 24, "oSSso", 4); P(g, 11, 24, "oSsso", 4); P(g, 12, 24, "ossso", 4)
    for i in range(6):                        # handle up-left from the hand
        P(g, 9 - i, 23 - i, "oLo", 4)
    P(g, 10, 23, "o", 4)
    blade_up(g, 3, 18, 4)
    sash_tail(g, 27, 26, 2, 4)
    # slack chain: a wave left of the hand, the weight lifted at the end
    chain(g, [(23, -1), (24, -2), (25, -3), (25, -4), (24, -5), (23, -6), (22, -7), (21, -8), (20, -9), (19, -9)], 4)
    weight(g, 16, -11, 4)
    return g.tidy()


def animations():
    return {
        "idle": ([idle(0, 0), idle(1, 1), idle(1, 0), idle(0, -1)], 5, True),
        "lean": ([swing_back(), whirl(), whirl()], 10, False),
        "hold": ([whirl(), whirl(-1)], 5, True),
        "lunge": ([smear(), impact(), impact()], 20, False),
        "recover": ([yank(), idle(0, 0), idle(0, 0)], 9, False),
    }


def main():
    anims = animations()
    n = PAL.check([g for frames, _, _ in anims.values() for g in frames])
    imgs = {k: ([render(g, PAL) for g in frames], fps, loop) for k, (frames, fps, loop) in anims.items()}
    beats = [imgs["idle"][0][0], imgs["lean"][0][0], imgs["lean"][0][1], imgs["lunge"][0][0], imgs["lunge"][0][1], imgs["recover"][0][0]]
    strip(beats, os.path.join(HERE, f"{NAME}_attack.png"), zoom=5,
          labels=["stance", "weight back", "whirl overhead", "streak", "impact", "yank"])
    gif(beats + [imgs["idle"][0][0]], os.path.join(HERE, f"{NAME}_attack.gif"), [500, 120, 220, 70, 320, 160, 500])
    out_dir = os.path.join(HERE, "..", "..", "..", "godot", "art", f"{NAME}_v2")
    sheet(imgs, out_dir, NAME, BOX, ORIGIN)
    print(f"{NAME}: {sum(len(f) for f, _, _ in imgs.values())} frames, {n} colours -> {os.path.abspath(out_dir)}")


if __name__ == "__main__":
    main()
