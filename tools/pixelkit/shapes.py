"""Procedural shaded shapes. All functions return a Part in canvas space
(anchor (0,0)) so you blit them at (0, 0).

Light comes from the upper-left: the edge of a shape facing up/left gets the
highlight letter, the edge facing down/right gets the shadow letter.
"""
from __future__ import annotations
import math
from .canvas import Part

LIGHT = (-0.6, -0.8)   # direction *toward* the light (screen coords, y down)


def _seg_dist(px, py, ax, ay, bx, by):
    """Distance from P to segment AB and the signed side (+ = toward light)."""
    vx, vy = bx - ax, by - ay
    L2 = vx * vx + vy * vy
    if L2 == 0:
        return math.hypot(px - ax, py - ay), 0.0
    t = max(0.0, min(1.0, ((px - ax) * vx + (py - ay) * vy) / L2))
    cx, cy = ax + t * vx, ay + t * vy
    dx, dy = px - cx, py - cy
    d = math.hypot(dx, dy)
    # unit normal, oriented toward the light
    nl = math.sqrt(L2)
    nx, ny = -vy / nl, vx / nl
    if nx * LIGHT[0] + ny * LIGHT[1] < 0:
        nx, ny = -nx, -ny
    side = dx * nx + dy * ny
    return d, side


def capsule(a, b, width, letters=("C", "c", "k"), shade_px=None, cap=True) -> Part:
    """A thick line from a to b with round caps, shaded across its width.

    letters = (highlight, base, shadow). shade_px = (hi_px, shadow_px) bands;
    default 1 px highlight, 1 px shadow (2 px shadow when width >= 5).
    """
    return polyline_capsule([a, b], width, letters, shade_px, cap)


def polyline_capsule(points, width, letters=("C", "c", "k"), shade_px=None, cap=True) -> Part:
    """Union of capsules along a polyline (a whole limb outlined once)."""
    hi, base, sh = letters
    if shade_px is None:
        shade_px = (1, 2 if width >= 5 else 1)
    hi_px, sh_px = shade_px
    r = width / 2.0
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    x0, x1 = int(min(xs) - r - 1), int(max(xs) + r + 2)
    y0, y1 = int(min(ys) - r - 1), int(max(ys) + r + 2)
    out = {}
    segs = list(zip(points[:-1], points[1:]))
    for y in range(y0, y1):
        for x in range(x0, x1):
            best = None
            for (ax, ay), (bx, by) in segs:
                d, side = _seg_dist(x + 0.5, y + 0.5, ax + 0.5, ay + 0.5, bx + 0.5, by + 0.5)
                if best is None or d < best[0]:
                    best = (d, side)
            d, side = best
            if d > r:
                continue
            if not cap:
                # square the ends: drop pixels beyond the segment ends
                pass
            if side >= r - hi_px:
                out[(x, y)] = hi
            elif side <= -r + sh_px:
                out[(x, y)] = sh
            else:
                out[(x, y)] = base
    return Part(out, (0, 0))


def line(a, b, letter="o") -> Part:
    """1-px Bresenham line."""
    (x0, y0), (x1, y1) = a, b
    out = {}
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    err = dx + dy
    while True:
        out[(x0, y0)] = letter
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy
    return Part(out, (0, 0))


def blade(hilt, tip, width=3, letters=("M", "m", "n"), taper=0.35, edge="w") -> Part:
    """A tapered blade/haft from hilt to tip. The last `taper` fraction narrows
    to a point. `edge` paints a 1-px bright edge on the lit side (use None for
    a plain haft).
    """
    hi, base, sh = letters
    (ax, ay), (bx, by) = hilt, tip
    L = math.hypot(bx - ax, by - ay) or 1.0
    r = width / 2.0
    x0, x1 = int(min(ax, bx) - r - 1), int(max(ax, bx) + r + 2)
    y0, y1 = int(min(ay, by) - r - 1), int(max(ay, by) + r + 2)
    vx, vy = (bx - ax) / L, (by - ay) / L
    out = {}
    for y in range(y0, y1):
        for x in range(x0, x1):
            px, py = x + 0.5 - (ax + 0.5), y + 0.5 - (ay + 0.5)
            t = px * vx + py * vy          # along
            if t < 0 or t > L:
                continue
            d, side = _seg_dist(x + 0.5, y + 0.5, ax + 0.5, ay + 0.5, bx + 0.5, by + 0.5)
            f = t / L
            rr = r
            if f > 1 - taper:
                rr = r * (1 - f) / taper
            if d > max(rr, 0.5):
                continue
            if edge and side >= rr - 1 and rr >= 1:
                out[(x, y)] = edge if f < 1 - taper * 0.5 else hi
            elif side >= rr - 1:
                out[(x, y)] = hi
            elif side <= -rr + 1:
                out[(x, y)] = sh
            else:
                out[(x, y)] = base
    return Part(out, (0, 0))


def arc(center, r_in, r_out, a0, a1, letters=("E", "e"), taper=True, steps=None) -> Part:
    """A slash blur: ring sector from angle a0 to a1 (degrees, screen coords,
    0 = right, 90 = down). Inner band is the core letter, outer the edge letter.
    taper thins the sector toward a0 (the trailing end)."""
    core, edge = letters
    cx, cy = center
    out = {}
    R = int(r_out) + 2
    sweep = (a1 - a0)
    for y in range(int(cy - R), int(cy + R + 1)):
        for x in range(int(cx - R), int(cx + R + 1)):
            dx, dy = x + 0.5 - cx, y + 0.5 - cy
            d = math.hypot(dx, dy)
            ang = math.degrees(math.atan2(dy, dx))
            # normalise angle into [a0, a1] range handling wrap
            k = (ang - a0) % 360
            if sweep >= 0:
                if k > sweep:
                    continue
                f = k / sweep if sweep else 0
            else:
                k = (a0 - ang) % 360
                if k > -sweep:
                    continue
                f = k / -sweep
            thick = (r_out - r_in)
            if taper:
                thick = thick * (0.25 + 0.75 * f)
            ro = r_in + thick
            if d < r_in or d > ro:
                continue
            out[(x, y)] = core if d < r_in + max(1.0, thick * 0.55) else edge
    return Part(out, (0, 0))


def ellipse(center, rx, ry, letter="%") -> Part:
    cx, cy = center
    out = {}
    for y in range(int(cy - ry - 1), int(cy + ry + 2)):
        for x in range(int(cx - rx - 1), int(cx + rx + 2)):
            if ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 <= 1.0:
                out[(x, y)] = letter
    return Part(out, (0, 0))


def fill_polygon(points, letter="c") -> Part:
    """Scanline-filled polygon (integer pixel centres)."""
    out = {}
    ys = [p[1] for p in points]
    n = len(points)
    for y in range(int(min(ys)), int(max(ys)) + 1):
        yc = y + 0.5
        xs = []
        for i in range(n):
            (x0, y0), (x1, y1) = points[i], points[(i + 1) % n]
            if (y0 <= yc < y1) or (y1 <= yc < y0):
                t = (yc - y0) / (y1 - y0)
                xs.append(x0 + t * (x1 - x0))
        xs.sort()
        for i in range(0, len(xs) - 1, 2):
            for x in range(int(math.floor(xs[i] + 0.5)), int(math.floor(xs[i + 1] + 0.5))):
                out[(x, y)] = letter
    return Part(out, (0, 0))
