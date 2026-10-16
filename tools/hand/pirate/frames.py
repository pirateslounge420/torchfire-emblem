"""Pirate (Thunder / yellow, pure form Berserker) — hand-pixelled frames.

Four hand-drawn LANKY bodies (body_idle.txt easy stand, body.txt wide low stance, body_back.txt
twisted-away wind-up with both hands raised, body_lunge.txt folded-forward crouch with both arms
driven down) plus hand-placed overlays for the far arm, the big broad axe, the smears and sparks.
Costume (Mike, Oct 16): yellow durag with two tails, open dark vest, bandaged forearms, baggy
cut-off pants with a ragged hem, bare shins, small sandalled feet.

idle   — 8-frame at-rest loop: the axe RESTS ON THE SHOULDER (haft over the far shoulder, head
         behind/above it, far fist holding the haft at the chest). 1-px breath, the sash tail
         sways, the free hand shifts.
select — 11-frame one-shot flourish: axe lifted off the shoulder → three frames of a one-handed
         spin in front (ring smear + pale afterimage of the head) → two-hand catch overhead →
         vertical slam smear → the head slammed into the ground with a yellow spark and dirt →
         hauled back up → re-shouldered → at rest with a cocky glint on the edge.
lean / hold / lunge / recover — the six GBA axe beats: lift off the shoulder → axe hung straight
         down from stacked hands → raised overhead behind the head → one big smear → crouched
         two-handed chop buried at the foe's feet → hauled back up.

Run:  python3 tools/hand/pirate/frames.py
  -> pirate_attack.png / .gif next to this file, Godot sheet in godot/art/pirate_v2/
"""
import math
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

# 15 opaque colours. W = steel glint, smear core and spark; Y (pale yellow) is the axe edge glow,
# durag highlight, smear fringe and the afterimage; C shades the steel by the eye and the vest.
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


def empty(dx=0, dy=0):
    g = Grid(BOX, BOX)
    g.dx, g.dy = dx, dy
    return g


def merge(under, over):
    """draw `over`'s pixels on top of `under` (both 64-boxes); returns `under`"""
    for y in range(BOX):
        for x in range(BOX):
            if over.g[y][x] != ".":
                under.g[y][x] = over.g[y][x]
    return under


def P(g, y, x, text):
    """overlay in body-grid coordinates (row 0 = top of the 40-row body file, shifted with the
    body's dx/dy); '.' leaves the pixel alone"""
    g.put(y + (GROUND - 39) + g.dy, x + X_OFF + g.dx, text.replace(".", "?"))


def block(g, y, x, rows):
    """hand-drawn multi-row overlay ('.' = leave alone)"""
    for j, ln in enumerate(rows):
        P(g, y + j, x, ln)


def clear(g, y0, x0, y1, x1):
    """clear a body-coordinate rectangle (rows y0..y1-1, cols x0..x1-1)"""
    g.clear(x0 + X_OFF + g.dx, y0 + (GROUND - 39) + g.dy, x1 + X_OFF + g.dx, y1 + (GROUND - 39) + g.dy)


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


AXE_R = rot_ccw(AXE_DOWN)        # edge RIGHT, haft vertical
AXE_UP = rot_ccw(AXE_R)          # edge UP, haft horizontal
AXE_L = rot_ccw(AXE_UP)          # edge LEFT, haft vertical


def eye(rows):
    """centre of the eye (the C patch) of a block, in block-local (row, col)"""
    pts = [(j, i) for j, ln in enumerate(rows) for i, ch in enumerate(ln) if ch == "C"]
    return sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)


def block_at_eye(g, ey, ex, rows, draw=None):
    """place a block so its eye centre sits on body coords (ey, ex); `draw` = a same-shape
    variant (e.g. its ghost) to draw in its place"""
    cy, cx = eye(rows)
    block(g, round(ey - cy), round(ex - cx), draw or rows)


def ghost(rows):
    """pale afterimage of a block: just its outline, in pale yellow"""
    return ["".join("Y" if ch == "o" else "." for ch in ln) for ln in rows]


def hand(g, y, x):
    """3x3 fist with its outline; (y, x) = its top-left skin pixel"""
    P(g, y - 1, x - 1, "ooooo"); P(g, y, x - 1, "oSSso"); P(g, y + 1, x - 1, "oSszo"); P(g, y + 2, x - 1, "oszzo"); P(g, y + 3, x - 1, "ooooo")


def haft_h(g, y, x0, x1, drop=0):
    """horizontal haft (rows y..y+3 = o L l o) from col x0 to x1 inclusive, dropping `drop` px over its length"""
    n = abs(x1 - x0)
    step = 1 if x1 >= x0 else -1
    for i in range(n + 1):
        x = x0 + i * step
        d = (i * drop) // max(1, n)
        P(g, y + d, x, "o"); P(g, y + 1 + d, x, "L"); P(g, y + 2 + d, x, "l"); P(g, y + 3 + d, x, "o")


def haft_v(g, x, y0, y1):
    """vertical haft (cols x..x+3 = o L l o) from row y0 to y1 inclusive"""
    for y in range(min(y0, y1), max(y0, y1) + 1):
        P(g, y, x, "oLlo")


def haft_d(g, y, x, i0, i1):
    """45-degree haft through (y, x): pixel i sits at (y - i, x + i), 2 px thick"""
    for i in range(i0, i1 + 1):
        P(g, y - i, x + i, "oLlo")


# --- effects -------------------------------------------------------------------
def ring(g, cy, cx, r, a0, a1):
    """smear ring of radius r around body coords (cy, cx): W core with a Y fringe, drawn only over
    the trailing sector a0..a1 (degrees, screen-clockwise from 3 o'clock, so 90 = down)"""
    for y in range(cy - r - 4, cy + r + 5):
        for x in range(cx - r - 4, cx + r + 5):
            d = math.hypot(y - cy, x - cx)
            if r - 3 <= d <= r + 3:
                a = math.degrees(math.atan2(y - cy, x - cx)) % 360
                span = (a1 - a0) % 360
                if (a - a0) % 360 <= span:
                    frac = ((a - a0) % 360) / span          # 0 at the tail, 1 behind the head
                    thick = 0.8 + 1.7 * frac
                    if abs(d - r) <= thick - 1.0 and frac > 0.3:
                        P(g, y, x, "W")
                    elif abs(d - r) <= thick:
                        P(g, y, x, "Y")


def arc(g, cy, cx, r, a_front, a_tail, w_front=4, w_tail=1):
    """a sweep smear: an arc of radius r from the thick blunt front (angle a_front) back to the thin
    tail (a_tail), measured screen-clockwise (degrees from 3 o'clock, 90 = down)"""
    for y in range(cy - r - 6, cy + r + 7):
        for x in range(cx - r - 6, cx + r + 7):
            d = math.hypot(y - cy, x - cx)
            if r - 6 <= d <= r + 6:
                a = math.degrees(math.atan2(y - cy, x - cx)) % 360
                span = (a_tail - a_front) % 360
                t = (a - a_front) % 360
                if t <= span:
                    frac = t / span                       # 0 at the front, 1 at the tail
                    thick = w_front + (w_tail - w_front) * frac
                    if abs(d - r) <= thick - 1.2 and frac < 0.8:
                        P(g, y, x, "W")
                    elif abs(d - r) <= thick:
                        P(g, y, x, "Y")


def spark(g, y, x, big=True):
    """four-point yellow spark with a white heart"""
    if big:
        P(g, y - 3, x, "Y"); P(g, y - 2, x, "W"); P(g, y - 1, x - 1, "WWW"); P(g, y, x - 3, "YWWWWWY")
        P(g, y + 1, x - 1, "WWW"); P(g, y + 2, x, "W"); P(g, y + 3, x, "Y")
        P(g, y - 2, x - 2, "Y"); P(g, y - 2, x + 2, "Y"); P(g, y + 2, x - 2, "Y"); P(g, y + 2, x + 2, "Y")
    else:
        P(g, y - 1, x, "Y"); P(g, y, x - 1, "YWY"); P(g, y + 1, x, "Y")


def glint(g, y, x):
    """small cocky sparkle on the blade edge"""
    P(g, y - 2, x, "Y"); P(g, y - 1, x, "W"); P(g, y, x - 2, "YWWWY"); P(g, y + 1, x, "W"); P(g, y + 2, x, "Y")
    P(g, y - 2, x - 2, "Y"); P(g, y - 2, x + 2, "Y"); P(g, y + 2, x - 2, "Y"); P(g, y + 2, x + 2, "Y")


# --- idle: the axe rests on the far shoulder -------------------------------------------
REST_EYE = (1, 35)        # body coords of the axe eye when it rests on the shoulder
REST_HAND = (16, 18)      # top-left skin pixel of the far fist holding the haft at the chest


def far_arm_rest(g):
    """far arm: upper arm hanging down the coat's back, elbow out, forearm up across the chest"""
    for y in range(13, 20):
        P(g, y, 25, "oCco")
    P(g, 20, 24, "oCco"); P(g, 19, 22, "oCcko"); P(g, 18, 20, "ocCko")


def sash_tail(g, sway=0):
    """the sash tail hanging off the far hip; sway moves the lower half 1 px"""
    P(g, 24, 25, "oyo"); P(g, 25, 25, "oyvo"); P(g, 26, 25, "ovvo")
    P(g, 27, 25 + sway, "oyvo"); P(g, 28, 25 + sway, "ovvo"); P(g, 29, 26 + sway, "ovo"); P(g, 30, 26 + sway, "oo")


def idle(bob=0, sway=0, hand_shift=0, sparkle=False):
    g = empty()
    block_at_eye(g, REST_EYE[0], REST_EYE[1], AXE_DIAG)      # the bit sits BEHIND the head and shoulder
    merge(g, body("body_idle"))
    far_arm_rest(g)
    sash_tail(g, sway)
    hy, hx = REST_HAND
    haft_d(g, hy + 1, hx + 1, -4, 16)                        # butt below the fist, up over the shoulder to the eye
    hand(g, hy, hx)
    if hand_shift:                                           # the free hand swings in a px
        g.shift_region(X_OFF + 10, GROUND - 39 + 18, X_OFF + 15, GROUND - 39 + 26, hand_shift, 0)
    if sparkle:
        glint(g, -6, 33)
    if bob:                                                  # head, torso and the shouldered axe breathe
        g.shift_region(0, 0, BOX, GROUND - 39 + 25, 0, bob)
    return g.tidy()


def lift():
    """the axe comes off the shoulder: far arm straight up, haft vertical, head high behind"""
    g = empty()
    block_at_eye(g, -4, 25, AXE_R)
    merge(g, body("body_idle"))
    sash_tail(g)
    for y in range(13, 21):
        P(g, y, 25, "oCco")
    haft_v(g, 24, -1, 16)
    hand(g, 10, 25)
    return g.tidy()


# --- select flourish ----------------------------------------------------------------
SPIN_C = (15, 1)          # body coords of the spinning fist (near arm thrown out toward the foe)
SPIN_R = 9


def spin_body():
    """idle body with the near arm thrown straight out to the left and the far arm hanging"""
    g = body("body_idle")
    clear(g, 11, 10, 26, 15)
    for y in range(11, 22):
        P(g, y, 14, "o")
    P(g, 12, 3, "ooooooooooo"); P(g, 13, 4, "CcccSSssss"); P(g, 14, 4, "ckkksszzzz"); P(g, 15, 3, "ooooooooooo")
    for y in range(13, 22):
        P(g, y, 25, "oCco")
    hand(g, 22, 26)
    sash_tail(g, 1)
    return g


def spin(k):
    """k = 0: head down (edge left) / 1: head left (edge up) / 2: head up (edge right), screen-clockwise"""
    cy, cx = SPIN_C
    g = spin_body()
    heads = [(AXE_L, (cy + SPIN_R, cx)), (AXE_UP, (cy, cx - SPIN_R)), (AXE_R, (cy - SPIN_R, cx))]
    head_angle = [90, 180, 270][k]
    # afterimage of the previous position, then the trailing ring, then the real head and haft
    prev = heads[k - 1] if k > 0 else (AXE_R, (cy - SPIN_R, cx))
    block_at_eye(g, prev[1][0], prev[1][1], prev[0], ghost(prev[0]))
    ring(g, cy + 1, cx + 1, SPIN_R + 5, head_angle - 170, head_angle - 20)
    rows, (ey, ex) = heads[k]
    if k == 1:
        haft_h(g, cy - 1, cx + 6, cx - SPIN_R)
    else:
        haft_v(g, cx - 1, cy - (SPIN_R if k == 2 else 6), cy + (SPIN_R if k == 0 else 6))
    block_at_eye(g, ey, ex, rows)
    hand(g, cy, cx)
    return g.tidy()


def slam():
    """vertical slam smear: the whole axe becomes one arc from behind the head down to the foe's feet"""
    g = body("body_lunge", dx=-2, dy=-1)
    arc(g, 16, 10, 21, 130, 290)
    return g.tidy()


def impact(spark_size=None, recoil=0):
    """beat 5: crouched two-handed chop, the head buried at the foe's feet"""
    g = body("body_lunge", dx=-4 + recoil)
    haft_h(g, 26, 8, -7, 3)
    block(g, 27, -12, AXE_DOWN)
    hand(g, 25, 1); hand(g, 26, 4)
    if spark_size == "big":
        spark(g, 35, -5, True)
        P(g, 31, -9, "l"); P(g, 30, 1, "L"); P(g, 33, -14, "l"); P(g, 29, -4, "L")
    elif spark_size == "small":
        spark(g, 34, -7, False)
        P(g, 28, -12, "l"); P(g, 27, 3, "L"); P(g, 31, -16, "l"); P(g, 26, -6, "l"); P(g, 36, -16, "c"); P(g, 36, 2, "c")
    return g.tidy()


# --- attack beats ----------------------------------------------------------------
def axe_hung():
    """beat 2: the axe hangs straight down from stacked hands, head resting at the front foot"""
    g = body(dx=1)
    clear(g, 24, 6, 28, 11)                                   # the body's own fist
    P(g, 18, 17, "ozo"); P(g, 19, 16, "oszo"); P(g, 20, 14, "oCcko"); P(g, 21, 12, "ocCko")   # far forearm
    haft_v(g, 9, 20, 33)
    block(g, 22, 7, AXE_R)
    hand(g, 22, 10); hand(g, 25, 9)
    return g.tidy()


def raised(tremble=0):
    """beat 3: twisted away, both hands up behind the head, the axe head high behind"""
    g = body("body_back", dx=-6, dy=tremble)
    haft_d(g, 10, 32, -3, 13)                                 # butt below the near hand, up through both hands
    block(g, -10, 35, AXE_DIAG)
    haft_d(g, 10, 32, -3, 10)                                 # the haft shows over the bit's back as far as the eye
    hand(g, 9, 31); hand(g, 5, 36)
    return g.tidy()


SMEAR = [   # one pale arc over the head: thick blunt front at the left, thin tail trailing to the upper right
    (-13, 27, "YYWWWYY"), (-12, 23, "YYWWWWWWWWWWWYY"), (-11, 20, "YWWWWWWWWWWWWWWWWWWWY"),
    (-10, 18, "YWWWWWWWWWWWWWWWWWWWWWWWY"), (-9, 16, "YWWWWWWWWWWWWWWWWWWWWWWWWWWWY"),
    (-8, 15, "YWWWWWWWWY"), (-8, 36, "YWWWWWWWWY"), (-7, 14, "YWWWWWWWY"), (-7, 38, "YWWWWWWWY"),
    (-6, 13, "YWWWWWWWY"), (-6, 40, "YWWWWWY"), (-5, 13, "YWWWWWWY"), (-5, 42, "YWWWWY"),
    (-4, 12, "YWWWWWWY"), (-4, 44, "YWWY"), (-3, 12, "YWWWWWWY"), (-3, 46, "YY"),
    (-2, 12, "YWWWWWY"), (-1, 12, "YWWWWWY"), (0, 13, "YWWWWY"), (1, 13, "YWWWWY"),
    (2, 14, "YWWWY"), (3, 15, "YWWY"), (4, 16, "YYY"),
]


def smear():
    """beat 4: the whole axe head becomes one pale wedge sweeping over the head"""
    g = body("body_back", dx=-8, dy=1)
    for y, x, t in SMEAR:
        P(g, y, x, t)
    return g.tidy()


def lower():
    """beat 6: hauling the axe back up out of the ground"""
    g = body("body_lunge", dx=-1)
    for i in range(14):
        P(g, 26 - i // 3, 7 - i, "o"); P(g, 27 - i // 3, 7 - i, "L"); P(g, 28 - i // 3, 7 - i, "l"); P(g, 29 - i // 3, 7 - i, "o")
    block(g, 21, -12, AXE_DOWN)
    hand(g, 25, 1); hand(g, 26, 4)
    return g.tidy()


def animations():
    rest = idle(0, 0, 0)
    return {
        "idle": ([rest, idle(0, 1, 0), idle(1, 1, 0), idle(1, 1, 1), idle(1, 0, 1), idle(1, -1, 1), idle(0, -1, 1), idle(0, -1, 0)], 6, True),
        "select": ([lift(), spin(0), spin(1), spin(2), raised(), slam(), impact("big"), impact("small", 1), lower(), lift(), idle(0, 0, 0, True)], 10, False),
        "lean": ([lift(), axe_hung(), raised(), raised(-1)], 10, False),
        "hold": ([raised(), raised(-1)], 5, True),
        "lunge": ([smear(), impact(), impact(None, 1)], 20, False),
        "recover": ([lower(), lift(), rest], 9, False),
    }


def main():
    anims = animations()
    n = PAL.check([g for frames, _, _ in anims.values() for g in frames])
    imgs = {k: ([render(g, PAL) for g in frames], fps, loop) for k, (frames, fps, loop) in anims.items()}
    sel = imgs["select"][0]
    beats = [imgs["idle"][0][0], sel[0], sel[2], sel[4], sel[5], sel[6], sel[10],
             imgs["lean"][0][1], imgs["lean"][0][2], imgs["lunge"][0][0], imgs["lunge"][0][1], imgs["recover"][0][0]]
    labels = ["rest", "sel: lift", "sel: spin", "sel: catch", "sel: slam", "sel: spark", "sel: glint",
              "axe hung low", "raised", "smear", "buried chop", "haul up"]
    strip(beats, os.path.join(HERE, f"{NAME}_attack.png"), zoom=4, labels=labels)
    seq = imgs["idle"][0] + sel + imgs["lean"][0] + imgs["hold"][0] + imgs["lunge"][0] + imgs["recover"][0]
    durs = [166] * 8 + [100] * 11 + [100] * 4 + [200] * 2 + [50] * 3 + [110] * 3
    gif(seq, os.path.join(HERE, f"{NAME}_attack.gif"), durs)
    out_dir = os.path.join(HERE, "..", "..", "..", "godot", "art", f"{NAME}_v2")
    sheet(imgs, out_dir, NAME, BOX, ORIGIN)
    print(f"{NAME}: {sum(len(f) for f, _, _ in imgs.values())} frames, {n} colours -> {os.path.abspath(out_dir)}")


if __name__ == "__main__":
    main()
