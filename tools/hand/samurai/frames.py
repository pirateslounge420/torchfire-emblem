"""Samurai (Lake / indigo) — v3: the anime iai sequence, composed from hand-pixelled parts.

Parts (parts.py): head / tail / torso / near-arm / legs variants, each a letter
grid drawn by hand. frames.py stamps them together per beat, then lays the
sword (saya, hilt, blade, smear) over the top. Nothing is generated — the
parts are the drawing; the code only decides where each part sits per beat.

The sequence (16 beats):
  stance → grip (coil) → draw → draw-cut smear → draw-cut impact
  → raise (both hands overhead) → down-cut smear → down-cut impact
  → chiburi: wipe the blade (2) → noto: resheathe (2) → click (stance)
  → bow (2) → stance

Godot animations: idle / lean / hold / lunge / recover (the fight phases) plus
"flourish" (wipe → resheathe → bow) for the end of a round, and the crit_*
set (the same beats with a long still and an afterimage smear).

Run:  python3 tools/hand/samurai/frames.py
  -> samurai_attack.png / .gif next to this file, Godot sheet in godot/art/samurai_v2/
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
from handkit import Grid, Palette, render, strip, gif, sheet  # noqa: E402
import parts as P  # noqa: E402

NAME = "samurai"
BOX_W, BOX_H = 112, 80
GROUND = 69
ORIGIN = (56, 70)
STANCE_X = 36            # left edge of the stance legs in the box

PAL = Palette(NAME, {
    "H": (248, 248, 248), "h": (184, 190, 210), "g": (112, 118, 146),
    "S": (248, 200, 160), "s": (200, 140, 104), "z": (136, 86, 66),
    "C": (112, 118, 146), "c": (60, 62, 88), "k": (30, 30, 46),
    "I": (150, 140, 255), "i": (88, 72, 200), "n": (46, 36, 120),
    "R": (200, 56, 64), "r": (120, 24, 40),
    "L": (72, 46, 28), "l": (72, 46, 28),
    "m": (184, 190, 210),
})


# --- stamping -----------------------------------------------------------------
def stamp(g, x, y, part):
    for j, row in enumerate(part):
        for i, ch in enumerate(row):
            if ch != "?" and 0 <= y + j < g.h and 0 <= x + i < g.w:
                g.g[y + j][x + i] = ch


def shear(part, per_row, start=0):
    """lean a part forward: row j (from `start`) shifts left by int(j*per_row)"""
    out = []
    for j, row in enumerate(part):
        k = int(max(0, j - start) * per_row + 0.5)
        out.append(row[k:] + "?" * k if k > 0 else row)
    return out


def shift_part(part, dx):
    if dx >= 0:
        return ["?" * dx + r for r in part]
    return [r[-dx:] + "?" * (-dx) for r in part]


def bresenham(x0, y0, x1, y1):
    pts = []
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    err = dx + dy
    x, y = x0, y0
    while True:
        pts.append((x, y))
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy; x += sx
        if e2 <= dx:
            err += dx; y += sy
    return pts


def blade_poly(g, x0, y0, x1, y1, edge="H", body="m"):
    """a 2-px blade from (x0,y0) to (x1,y1) at any angle: 'edge' line, 'body' line one
    pixel to the lower/right side, outlined wherever a neighbour is empty."""
    edge_pts = bresenham(x0, y0, x1, y1)
    steep = abs(y1 - y0) > abs(x1 - x0)
    off = (1, 0) if steep else (0, 1)
    body_pts = [(x + off[0], y + off[1]) for x, y in edge_pts]
    filled = set(edge_pts) | set(body_pts)
    for x, y in body_pts:
        if 0 <= x < g.w and 0 <= y < g.h:
            g.g[y][x] = body
    for x, y in edge_pts:
        if 0 <= x < g.w and 0 <= y < g.h:
            g.g[y][x] = edge
    for x, y in list(filled):
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if (nx, ny) not in filled and 0 <= nx < g.w and 0 <= ny < g.h and g.g[ny][nx] == ".":
                g.g[ny][nx] = "o"


def hilt_poly(g, x0, y0, x1, y1):
    """the tsuka (wrapped grip) as a 2-px bar from (x0,y0) to (x1,y1)"""
    blade_poly(g, x0, y0, x1, y1, edge="L", body="L")


# --- the figure ---------------------------------------------------------------
class Fig:
    """places the parts for one beat. legs decide where everything else sits."""

    def __init__(self, legs, lx, torso=None, torso_dy=0, lean=0.0):
        self.g = Grid(BOX_W, BOX_H)
        self.legs = legs
        self.lx = lx
        self.ly = GROUND - (len(legs) - 1)
        waist = next(i for i, c in enumerate(legs[0]) if c == "o")
        torso = torso or P.TORSO
        if lean:
            torso = shear(torso, lean)
        tw = next(i for i, c in enumerate(torso[-1]) if c == "o")
        self.torso = torso
        self.tx = self.lx + waist - tw
        self.ty = self.ly - (len(torso) - 1) + torso_dy
        self.nx = self.tx + torso[0].index("s")      # the neck pixel on the torso's top row
        self.ny = self.ty
        self.hx, self.hy = self.nx - 5, self.ny - 19     # head: neck base at local (5,19)
        self.tiex, self.tiey = self.hx + 15, self.hy + 17  # the hair tie

    def saya(self, mouth=None, part=None):
        mx, my = mouth or self.mouth()
        stamp(self.g, mx - 1, my - 1, part or P.SAYA)

    def far_sleeve(self, dx=0, dy=0, part=None):
        stamp(self.g, self.tx + 12 + dx, self.ty + 1 + dy, part or P.FAR_SLEEVE)

    def tail(self, part, dx=0, dy=0):
        stamp(self.g, self.tiex + dx, self.tiey + 1 + dy, part)

    def body(self, head=None, hdx=0, hdy=0):
        stamp(self.g, self.lx, self.ly, self.legs)
        stamp(self.g, self.tx, self.ty, self.torso)
        stamp(self.g, self.hx + hdx, self.hy + hdy, head or P.HEAD)

    def arm(self, part, dx=0, dy=0):
        stamp(self.g, self.tx - 1 + dx, self.ty + dy, part)

    def obi_tails(self, pts):
        for (x, y, t) in pts:
            self.g.put(self.ty + y, self.tx + x, t)

    def mouth(self):
        """the saya mouth: just in front of the near hip under the obi"""
        return (self.tx + 3, self.ty + 15)

    def hilt_sheathed(self, n=4):
        mx, my = self.mouth()
        self.g.put(my - 1, mx - 1, "gg"); self.g.put(my, mx - 1, "gg")        # tsuba
        hilt_poly(self.g, mx - 2, my - 1, mx - 2 - 2 * n, my - 1 - n)


OBI_STANCE = [(18, 13, "oRro"), (19, 14, "oRro"), (20, 15, "orro"), (21, 16, "oro")]
OBI_LUNGE = [(19, 13, "oRro"), (22, 14, "oRrro"), (26, 15, "orro")]


# --- beats --------------------------------------------------------------------
def stance(bob=0, sway=0):
    f = Fig(P.LEGS_STANCE, STANCE_X)
    f.far_sleeve()
    f.tail(P.TAIL_SWAY if sway else P.TAIL_HANG, dy=bob)
    f.body(hdy=bob)
    f.saya()
    f.arm(P.ARM_REST_SWING if sway else P.ARM_REST, dy=bob)
    f.hilt_sheathed()
    f.g.put(f.ty + 15 + bob, f.tx + 2, "oSsso"); f.g.put(f.ty + 16 + bob, f.tx + 2, "ozzzo")   # the near hand resting on the hilt
    f.obi_tails(OBI_STANCE)
    return f.g.tidy()


def grip():
    """knees sink, the front foot slides back, both hands on the hilt"""
    f = Fig(P.LEGS_COIL, STANCE_X + 2, lean=0.08)
    f.far_sleeve(dx=-2, dy=1)
    f.tail(P.TAIL_HANG, dx=1)
    f.body()
    f.saya()
    f.arm(P.ARM_GRIP)
    f.hilt_sheathed()
    mx, my = f.mouth()
    f.g.put(my - 3, mx - 6, "oSso"); f.g.put(my - 2, mx - 7, "oSszo"); f.g.put(my - 1, mx - 6, "ozzo")   # the drawing hand on the tsuka
    f.g.put(my + 1, mx, "Ss"); f.g.put(my + 2, mx, "zz")                                                 # the far hand at the mouth
    f.obi_tails(OBI_STANCE)
    return f.g.tidy()


def draw(tremble=0):
    """the blade partway out: hilt pulled up-left, 9 px of steel showing"""
    f = Fig(P.LEGS_COIL, STANCE_X + 2, lean=0.12)
    f.far_sleeve(dx=-2, dy=1)
    f.tail(P.TAIL_SWING_BACK)
    f.body(hdy=tremble)
    f.saya()
    f.arm(P.ARM_DRAW, dx=-3, dy=1 + tremble)
    mx, my = f.mouth()
    f.g.put(my - 1, mx - 1, "gg"); f.g.put(my, mx - 1, "g")                     # the koiguchi
    blade_poly(f.g, mx - 2, my - 1, mx - 10, my - 9)
    hx, hy = mx - 10, my - 9
    f.g.put(hy, hx - 1, "gg"); f.g.put(hy + 1, hx - 1, "gg")                   # tsuba
    hilt_poly(f.g, hx - 2, hy - 1, hx - 7, hy - 6)
    f.g.put(hy - 3, hx - 6, "oSso"); f.g.put(hy - 2, hx - 7, "oSszo"); f.g.put(hy - 1, hx - 6, "ozzo")   # the drawing hand
    f.g.put(my + 1, mx, "Ss"); f.g.put(my + 2, mx, "zz")
    f.g.put(my - 2, mx - 3, "H")                                                 # glint at the mouth
    f.obi_tails([(14, 11, "oRro"), (16, 12, "oRro"), (18, 13, "orro")])
    return f.g.tidy()


DRAW_SMEAR = [  # the horizontal draw-cut: one pale wedge from the hip sweeping up and across to the left
    (-16, "hhHHHHHHhh"), (-19, "hhHHHHHHHHHHhh"), (-22, "hHHHHHHHHHHHHHHhhh"), (-24, "hHHHHHHHHHHHHHHHHHHhhh"),
    (-25, "HHHHHHHHHHHHHHHHHHHHHHhhhh"), (-25, "HHHHHHHHHHHHHHHHHHHHHHHhhhhhh"), (-24, "hHHHHHHHHHHHHHHHHHHHHhhhhhhhh"),
    (-22, "hhHHHHHHHHHHHHHHHHhhhhhhhhhh"), (-19, "hhhHHHHHHHHHHHHHhhhhhhhhhh"), (-15, "hhhhhhHHHHHHHhhhhhhhhhh"),
    (-10, "hhhhhhhhhhhhhhhhhhhh"), (-5, "hhhhhhhhhhhhhhh"), (0, "hhhhhhhhh"),
]


def cut_smear():
    f = Fig(P.LEGS_LUNGE, STANCE_X - 6, lean=0.4)
    f.far_sleeve(dx=-1, dy=2)
    f.tail(P.TAIL_STREAM, dx=1, dy=-2)
    f.body()
    f.saya((f.tx + 4, f.ty + 12))
    f.arm(P.ARM_OUT, dx=-4, dy=1)
    for j, (x, t) in enumerate(DRAW_SMEAR):
        f.g.put(f.ty + j, f.tx + x, t)
    f.obi_tails(OBI_LUNGE)
    return f.g.tidy()


def cut_impact(settle=0):
    f = Fig(P.LEGS_LUNGE, STANCE_X - 6 - settle, lean=0.4)
    f.far_sleeve(dx=-1, dy=2)
    f.tail(P.TAIL_STREAM, dx=1, dy=-1)
    f.body()
    f.saya((f.tx + 4, f.ty + 12))
    f.arm(P.ARM_OUT, dx=-4, dy=1)
    hx, hy = f.tx - 5, f.ty + 2
    f.g.put(hy - 1, hx + 1, "gg"); f.g.put(hy, hx + 1, "gg")           # the tsuba just past the hand
    blade_poly(f.g, hx - 1, hy, hx - 20, hy)
    f.obi_tails(OBI_LUNGE)
    return f.g.tidy()


def raise_():
    """both hands overhead-behind (jodan): the back foot steps up, the body stands tall"""
    f = Fig(P.LEGS_STANCE, STANCE_X - 4)
    f.far_sleeve(dx=1, dy=-2)
    f.tail(P.TAIL_HANG, dx=-2)
    f.body()
    f.saya()
    f.arm(P.ARM_RAISE, dy=-16)
    hx, hy = f.tx + 14, f.ty - 16          # the hands
    f.g.put(hy + 1, hx + 3, "gg"); f.g.put(hy + 2, hx + 3, "gg")        # tsuba behind the hands
    blade_poly(f.g, hx + 5, hy + 1, hx + 20, hy - 7)
    f.obi_tails(OBI_STANCE)
    return f.g.tidy()


DOWN_SMEAR = [  # the vertical two-handed cut: a wedge from over the head down to the ground in front
    (-2, "hhHHhh"), (-5, "hHHHHHhh"), (-8, "hHHHHHHHhh"), (-11, "hHHHHHHHHHhh"), (-13, "hHHHHHHHHHHhh"),
    (-15, "hHHHHHHHHHHHhh"), (-17, "hHHHHHHHHHHHhhh"), (-18, "hHHHHHHHHHHhhhh"), (-19, "hHHHHHHHHHhhhhh"),
    (-20, "hHHHHHHHHhhhhh"), (-21, "hHHHHHHhhhhh"), (-21, "hHHHHHhhhhh"), (-21, "hHHHhhhhh"), (-21, "hHHhhhh"),
    (-21, "hhhhhh"), (-20, "hhhh"), (-19, "hh"),
]


def down_smear():
    f = Fig(P.LEGS_DOWNCUT, STANCE_X - 8, lean=0.5)
    f.far_sleeve(dx=-2, dy=1)
    f.tail(P.TAIL_STREAM, dx=1, dy=-3)
    f.body()
    f.saya((f.tx + 4, f.ty + 12))
    f.arm(P.ARM_DOWN, dx=-17)
    for j, (x, t) in enumerate(DOWN_SMEAR):
        f.g.put(f.ty - 10 + j, f.tx + x, t)
    f.obi_tails(OBI_LUNGE)
    return f.g.tidy()


def down_impact():
    f = Fig(P.LEGS_DOWNCUT, STANCE_X - 8, lean=0.5)
    f.far_sleeve(dx=-2, dy=1)
    f.body()
    f.saya((f.tx + 4, f.ty + 12))
    f.tail(P.TAIL_WHIP_FWD, dx=-8, dy=-14)     # over the head: the tail whips forward past the crown
    f.arm(P.ARM_DOWN, dx=-17)
    hx, hy = f.tx - 16, f.ty + 13           # the hands
    f.g.put(hy, hx - 1, "gg"); f.g.put(hy + 1, hx - 2, "gg")
    blade_poly(f.g, hx - 2, hy + 2, hx - 9, hy + 16)
    f.obi_tails(OBI_LUNGE)
    return f.g.tidy()


def wipe(stage=0):
    """chiburi as the anime does it: the blade held level at the chest, the off hand runs a cloth down it"""
    f = Fig(P.LEGS_STANCE, STANCE_X)
    f.far_sleeve()
    f.tail(P.TAIL_SETTLE if stage == 0 else P.TAIL_HANG)
    f.body()
    f.saya()
    f.arm(P.ARM_WIPE, dx=-3, dy=2)
    hx, hy = f.tx - 2, f.ty + 5             # the hilt hand
    f.g.put(hy - 1, hx - 1, "gg"); f.g.put(hy, hx - 1, "gg")
    blade_poly(f.g, hx - 2, hy, hx - 22, hy)
    # the far hand with the cloth: at the guard first, then out at the tip
    wx = hx - 5 if stage == 0 else hx - 19
    stamp(f.g, wx, hy - 3, P.FAR_WIPE)
    f.g.put(hy - 1, wx + 1, "HH"); f.g.put(hy, wx, "Hh")                 # the cloth
    if stage == 1:                                                        # the glint at the tip
        f.g.put(hy - 3, hx - 24, "H"); f.g.put(hy - 2, hx - 25, "HHH"); f.g.put(hy - 1, hx - 24, "H")
    f.obi_tails(OBI_STANCE)
    return f.g.tidy()


def noto(stage=0):
    """the blade back into the saya: its spine on the far hand at the mouth, the hilt hand high"""
    f = Fig(P.LEGS_STANCE, STANCE_X)
    f.far_sleeve()
    f.tail(P.TAIL_HANG)
    f.body()
    f.saya()
    mx, my = f.mouth()
    f.g.put(my - 1, mx - 1, "gg"); f.g.put(my, mx - 1, "g")
    f.g.put(my + 1, mx - 1, "oSsso"); f.g.put(my + 2, mx - 1, "ozzzo")      # the far hand cupping the mouth
    if stage == 0:
        f.arm(P.ARM_NOTO, dx=-4, dy=-1)
        hx, hy = f.tx - 4, f.ty + 1
        blade_poly(f.g, mx - 2, my - 1, hx + 2, hy + 3)                   # steel from the mouth up to the hilt
        f.g.put(hy + 2, hx + 2, "gg"); f.g.put(hy + 3, hx + 2, "gg")
        hilt_poly(f.g, hx + 1, hy + 1, hx - 3, hy - 3)
    else:
        f.arm(P.ARM_NOTO, dx=-2, dy=5)
        hilt_poly(f.g, mx - 2, my - 1, mx - 10, my - 5)
        f.g.put(my - 2, mx - 3, "H")                                       # the click
    f.obi_tails(OBI_STANCE)
    return f.g.tidy()


def bow(depth=1):
    """rei: the torso folds forward from the hips, head down, hands sliding down the thighs"""
    if depth == 1:
        f = Fig(P.LEGS_BOW, STANCE_X + 2, lean=0.45)
        f.far_sleeve(dx=-2, dy=1)
        f.tail(P.TAIL_FALL_FWD, dx=-4, dy=1)
        f.body(head=P.HEAD_DOWN, hdx=-2, hdy=2)
        f.saya()
        f.arm(P.ARM_BOW, dx=-1, dy=2)
        f.hilt_sheathed()
        f.obi_tails(OBI_STANCE)
        return f.g.tidy()
    # the deep bow: a torso drawn folded, the head hanging below the shoulder line
    g = Grid(BOX_W, BOX_H)
    legs = P.LEGS_BOW
    lx, ly = STANCE_X + 2, GROUND - (len(legs) - 1)
    tx, ty = lx + 5 - 14, ly - 11
    stamp(g, lx, ly, legs)
    stamp(g, tx, ty, P.TORSO_BOW)
    stamp(g, tx + 14, ty + 10, P.SAYA)
    hx, hy = tx + 6 - 5, ty + 1 - 19 + 10        # the head hangs forward-down from the shoulder
    stamp(g, hx + 10, hy + 3, P.TAIL_FALL_FWD)
    stamp(g, hx, hy, P.HEAD_DOWN)
    stamp(g, tx + 2, ty + 2, P.ARM_BOW)         # the near arm hangs straight down in front of the thigh
    g.put(ty + 11, tx + 15, "gg"); g.put(ty + 12, tx + 15, "gg")       # the tsuba at the hip; the hilt is behind the hanging arm
    for (x, y, t) in OBI_STANCE:
        g.put(ty + y - 4, tx + x + 4, t)
    return g.tidy()



def click_loose():
    """select 1: the thumb pushes the tsuba — an inch of steel shows at the mouth with a glint"""
    f = Fig(P.LEGS_STANCE, STANCE_X)
    f.far_sleeve()
    f.tail(P.TAIL_HANG)
    f.body()
    f.saya()
    f.arm(P.ARM_GRIP)
    mx, my = f.mouth()
    f.g.put(my - 1, mx - 2, "gg"); f.g.put(my, mx - 2, "gg")
    blade_poly(f.g, mx - 3, my - 1, mx - 4, my - 2)
    hilt_poly(f.g, mx - 4, my - 2, mx - 12, my - 6)
    f.g.put(my - 3, mx - 7, "oSsso"); f.g.put(my - 2, mx - 8, "oSsszo"); f.g.put(my - 1, mx - 7, "ozzzo")
    f.g.put(my - 3, mx - 3, "H"); f.g.put(my - 4, mx - 4, "H"); f.g.put(my - 2, mx - 4, "H")        # the glint
    f.obi_tails(OBI_STANCE)
    return f.g.tidy()


def flash():
    """select 3: the blade fully out, held up-left and still, light running down the edge"""
    f = Fig(P.LEGS_STANCE, STANCE_X)
    f.far_sleeve()
    f.tail(P.TAIL_SWING_BACK)
    f.body()
    f.saya()
    f.arm(P.ARM_NOTO, dx=-4, dy=-1)
    hx, hy = f.tx - 4, f.ty + 1
    hilt_poly(f.g, hx + 1, hy + 2, hx - 3, hy + 6)
    f.g.put(hy + 1, hx + 2, "gg"); f.g.put(hy + 2, hx + 2, "gg")
    blade_poly(f.g, hx + 3, hy + 1, hx + 20, hy - 16)
    f.g.put(hy - 18, hx + 21, "H"); f.g.put(hy - 17, hx + 20, "HHH"); f.g.put(hy - 16, hx + 21, "H")   # tip sparkle
    f.obi_tails(OBI_STANCE)
    return f.g.tidy()


def flick():
    """select 4: one fast horizontal flick — a smear, feet planted"""
    f = Fig(P.LEGS_STANCE, STANCE_X)
    f.far_sleeve()
    f.tail(P.TAIL_SWING_BACK)
    f.body()
    f.saya()
    f.arm(P.ARM_OUT, dx=-4, dy=2)
    for j, (x, t) in enumerate(DRAW_SMEAR):
        f.g.put(f.ty - 2 + j, f.tx + x, t)
    f.obi_tails(OBI_STANCE)
    return f.g.tidy()


def select_frames():
    return [stance(), click_loose(), click_loose(), draw(), flash(), flash(), flick(), wipe(1), wipe(1), noto(0), noto(1), stance()]


# --- animation sets -------------------------------------------------------------
def animations():
    return {
        "idle": ([stance(0, 0), stance(0, 0), stance(1, 0), stance(1, 1), stance(2, 1), stance(1, 1), stance(1, 0), stance(0, 0)], 6, True),
        "lean": ([grip(), draw(), draw()], 10, False),
        "hold": ([draw(), draw(-1)], 5, True),
        "lunge": ([cut_smear(), cut_impact(), raise_(), down_smear(), down_impact(), down_impact()], 20, False),
        "recover": ([wipe(0), wipe(1), noto(0), noto(1), stance()], 9, False),
        "select": (select_frames(), 10, False),
        "flourish": ([wipe(0), wipe(1), noto(0), noto(1), stance(), bow(1), bow(2), bow(2), bow(1), stance()], 6, False),
    }


BEATS = ["stance", "grip", "draw", "draw-cut", "impact", "raise", "down-cut", "lands", "wipe", "wipe 2",
         "resheathe", "click", "bow", "bow 2"]


def beat_grids():
    return [stance(), grip(), draw(), cut_smear(), cut_impact(), raise_(), down_smear(), down_impact(),
            wipe(0), wipe(1), noto(0), noto(1), bow(1), bow(2)]


def main():
    bs = beat_grids()
    anims = animations()
    n = PAL.check(bs + [g for fr, _, _ in anims.values() for g in fr])
    imgs = [render(g, PAL) for g in bs]
    strip(imgs, os.path.join(HERE, f"{NAME}_attack.png"), zoom=4, labels=BEATS)
    gif(imgs + [imgs[0]], os.path.join(HERE, f"{NAME}_attack.gif"),
        [600, 160, 220, 70, 260, 240, 70, 320, 300, 300, 260, 320, 260, 500, 600], zoom=4)
    out_dir = os.path.join(HERE, "..", "..", "..", "godot", "art", f"{NAME}_v2")
    rendered = {k: ([render(g, PAL) for g in fr], fps, loop) for k, (fr, fps, loop) in anims.items()}
    sheet(rendered, out_dir, NAME, (BOX_W, BOX_H), ORIGIN, columns=8)
    print(f"{NAME}: {len(bs)} beats, {sum(len(f) for f, _, _ in anims.values())} frames, {n} colours -> {os.path.abspath(out_dir)}")


if __name__ == "__main__":
    main()
