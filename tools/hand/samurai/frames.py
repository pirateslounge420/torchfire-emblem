"""Samurai (Lake / indigo) — hand-pixelled frames.

Three hand-drawn bodies (body.txt neutral stance, body_back.txt wind-up with
both hands raised, body_lunge.txt deep lunge with both arms out) plus
hand-placed overlays for the katana, hair and smear. The attack follows the
six beats of the GBA Myrmidon sheets: stance → blade back → raised (two
hands) → one big smear → two-handed cut at full extension → blade lowering.

Run:  python3 tools/hand/samurai/frames.py
  -> samurai_attack.png / .gif next to this file, Godot sheet in godot/art/samurai_v2/
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from handkit import Grid, Palette, render, strip, gif, sheet  # noqa: E402

NAME = "samurai"
BOX = 64
GROUND = 53          # row the feet stand on
X_OFF = 18           # body grid column 0 -> box column
ORIGIN = (36, 54)

# 15 opaque colours. H/h/g double as hair, bandages, blade and smear.
PAL = Palette(NAME, {
    "H": (248, 248, 248), "h": (184, 190, 210), "g": (112, 118, 146),
    "S": (248, 200, 160), "s": (200, 140, 104), "z": (136, 86, 66),
    "C": (184, 190, 210), "c": (60, 62, 88), "k": (30, 30, 46),
    "I": (150, 140, 255), "i": (88, 72, 200), "n": (46, 36, 120),
    "R": (200, 56, 64), "r": (120, 24, 40),
    "L": (72, 46, 28), "l": (72, 46, 28),
    "m": (184, 190, 210),
})


def body(pose="body", dx=0, dy=0):
    g = Grid.from_text(os.path.join(HERE, f"{pose}.txt"), BOX, BOX, anchor_bottom=GROUND + dy, x_off=X_OFF + dx)
    for y in range(GROUND - 14 + dy, GROUND + 1 + dy):          # hakama rows take the indigo ramp
        for x in range(BOX):
            c = g.g[y][x]
            g.g[y][x] = {"C": "I", "c": "i", "k": "n"}.get(c, c)
    return g


def P(g, y, x, text):
    """overlay in body-grid coordinates (row 0 = top of the 40-row body)"""
    g.put(y + (GROUND - 39), x + X_OFF, text)


def blade(g, y, x, dyx, n, dx_off=0):
    """2-px katana from body coords (x,y); dyx = (dy, dx) per step; n steps"""
    dy, ddx = dyx
    for i in range(n):
        P(g, y + dy * i, x + ddx * i + dx_off, "oHmo")


# --- frames -------------------------------------------------------------------
def idle(bob=0):
    g = body()
    if bob:
        g.shift_region(0, 0, BOX, GROUND - 12, 0, bob)
    # far arm + katana held low-back, sash tail
    P(g, 16, 23, "occo"); P(g, 17, 24, "occko"); P(g, 18, 25, "occko"); P(g, 19, 26, "ocko")
    P(g, 20, 27, "ockko"); P(g, 21, 28, "ockko"); P(g, 22, 29, "ohgo"); P(g, 23, 30, "ohgo")
    P(g, 24, 31, "ohgo"); P(g, 25, 31, "ohgo"); P(g, 26, 32, "oszo"); P(g, 27, 32, "ozzo")
    P(g, 28, 32, "oLlo")
    blade(g, 29, 33, (1, 1), 8)
    P(g, 37, 41, "oHo"); P(g, 38, 42, "oo")
    P(g, 24, 36, "oRro"); P(g, 25, 37, "oRrro"); P(g, 26, 39, "oRro"); P(g, 27, 41, "orro")
    return g.tidy()


def blade_back():
    """beat 2: blade swung back-down, body still neutral but weight shifting"""
    g = body(dx=1)
    P(g, 20, 24, "occo"); P(g, 21, 25, "occko"); P(g, 22, 26, "ockko"); P(g, 23, 27, "ockko")
    P(g, 24, 28, "ohgo"); P(g, 25, 29, "ohgo"); P(g, 26, 29, "ohgo"); P(g, 27, 30, "oszo"); P(g, 28, 30, "ozzo")
    P(g, 29, 30, "oLlo")
    for i in range(10):
        P(g, 30 + i, 31 + i // 2, "oHmo")
    P(g, 40, 36, "oo")
    P(g, 25, 34, "oRro"); P(g, 26, 35, ".oRro"); P(g, 27, 37, "orro")
    return g.tidy()


def raised(tremble=0):
    """beat 3: both hands over the far shoulder, blade straight up"""
    g = body("body_back", dx=-4, dy=tremble)
    # blade from the hands (body coords ~ (40,2)) straight up, 14 px, clipped by the box top
    for i in range(14):
        P(g, 1 - i, 39, "oHmo")
    P(g, 1, 38, "oLo"); P(g, 2, 38, "oLo")          # hilt showing below the hands
    P(g, 24, 32, "oRro"); P(g, 25, 34, "oRro"); P(g, 26, 36, "orro")
    return g.tidy()


SMEAR = [
    (1, 44, "HHHHHhh"), (2, 40, "HHHHHHHHHhh"), (3, 36, "HHHHHHHHHHHHhhh"), (4, 32, "HHHHHHHHHHHHHHHhhh"),
    (5, 28, "HHHHHHHHHHHHHHHHHhhhh"), (6, 24, "HHHHHHHHHHHHHHHHHHHhhhhh"), (7, 20, "HHHHHHHHHHHHHHHHHHHHHhhhhhh"),
    (8, 17, "hHHHHHHHHHHHHHHHHHHHHhhhhhhhh"), (9, 15, "hhHHHHHHHHHHHHHHHHHhhhhhhhhhh"), (10, 14, "hhhhHHHHHHHHHHHHhhhhhhhhhhh"),
    (11, 14, "hhhhhhhHHHHHHhhhhhhhhhhh"), (12, 15, "hhhhhhhhhhhhhhhhhhhhh"), (13, 17, "hhhhhhhhhhhhhhhhhh"),
    (14, 20, "hhhhhhhhhhhhhh"), (15, 24, "hhhhhhhhh"), (16, 28, "hhhhh"),
]


def smear():
    """beat 4: the whole blade becomes one pale wedge over the head"""
    g = body("body_back", dx=-6, dy=1)
    for y, x, t in SMEAR:
        P(g, y, x - 8, t)
    return g.tidy()


def impact():
    """beat 5: two-handed cut at full extension, blade level to the left"""
    g = body("body_lunge", dx=-4)
    # tsuba + blade leftwards from the hands (body x~1, rows 20-21)
    P(g, 19, 0, "oLo"); P(g, 20, 0, "oLo"); P(g, 21, 0, "oLo")
    for i in range(1, 16):
        g.put(GROUND - 39 + 20, X_OFF - 4 - i, "H")
        g.put(GROUND - 39 + 21, X_OFF - 4 - i, "m")
        g.put(GROUND - 39 + 19, X_OFF - 4 - i, "o")
        g.put(GROUND - 39 + 22, X_OFF - 4 - i, "o")
    g.put(GROUND - 39 + 20, X_OFF - 20, "o"); g.put(GROUND - 39 + 21, X_OFF - 20, "o")
    return g.tidy()


def lower():
    """beat 6: blade dropping, body easing back"""
    g = body("body_lunge", dx=-1)
    P(g, 23, 1, "oLo")
    for i in range(12):
        P(g, 24 + i, 1 - i, "oHmo")
    return g.tidy()


def animations():
    return {
        "idle": ([idle(0), idle(1), idle(1), idle(0)], 5, True),
        "lean": ([blade_back(), raised(), raised()], 10, False),
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
          labels=["stance", "blade back", "raised, two hands", "smear", "two-handed cut", "lower"])
    gif(beats + [imgs["idle"][0][0]], os.path.join(HERE, f"{NAME}_attack.gif"), [500, 120, 220, 70, 320, 160, 500])
    out_dir = os.path.join(HERE, "..", "..", "..", "godot", "art", f"{NAME}_v2")
    sheet(imgs, out_dir, NAME, BOX, ORIGIN)
    print(f"{NAME}: {sum(len(f) for f, _, _ in imgs.values())} frames, {n} colours -> {os.path.abspath(out_dir)}")


if __name__ == "__main__":
    main()
