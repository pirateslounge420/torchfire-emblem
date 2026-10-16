"""Draws original GBA-style battle frames for the Samurai (Lake / sword).

Style rules followed (from studying GBA Fire Emblem 6/7/8 sheets, no art copied):
- 64x64 frame box, figure ~36 px tall, head ~1/3 of height, small feet
- 16-color palette incl. transparent; dark *colored* outline, never pure black
- every surface has 3 tones: shadow / base / highlight, lit from upper-left
- weapon gets its own 3-tone ramp; attack frames add a 2-tone slash arc

Outputs godot/art/samurai/samurai_sheet.png and samurai_frames.json
Run:  python3 tools/draw_samurai.py
"""
import json, math, os
from PIL import Image, ImageDraw

W = 64
OUT = os.path.join(os.path.dirname(__file__), "..", "godot", "art", "samurai")

# --- Palette (Lake trigram: silver) ---------------------------------------
OUTLINE = (38, 30, 52)
SKIN = [(176, 110, 82), (236, 184, 140), (255, 226, 196)]
HAIR = [(24, 24, 40), (52, 52, 78), (92, 92, 120)]
KIMONO = [(118, 124, 142), (190, 196, 212), (238, 240, 248)]   # silver
HAKAMA = [(44, 48, 70), (78, 84, 112), (116, 124, 150)]
SASH = [(120, 40, 50), (190, 70, 80), (230, 120, 120)]
BLADE = [(150, 160, 190), (220, 226, 240), (255, 255, 255)]
SLASH = [(170, 220, 255), (255, 255, 255)]
SHADOW = (0, 0, 0, 70)


def new():
    return Image.new("RGBA", (W, W), (0, 0, 0, 0))


def poly(d, pts, ramp, shade=True):
    """Filled polygon with a simple upper-left highlight band and lower shadow."""
    d.polygon(pts, fill=ramp[1])
    if shade:
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        # shadow: lower-right third
        d.polygon([(x0 + (x1 - x0) * 0.55, y1), (x1, y1), (x1, y0 + (y1 - y0) * 0.5)], fill=ramp[0])
        # highlight: thin band upper-left
        d.line([(x0 + 1, y0 + 1), (x0 + 1, y0 + (y1 - y0) * 0.5)], fill=ramp[2])


def outline(img):
    """Draw OUTLINE around every opaque pixel that borders transparency."""
    px = img.load()
    src = img.copy().load()
    for y in range(W):
        for x in range(W):
            if src[x, y][3] == 0:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < W and src[nx, ny][3] > 0 and src[nx, ny][:3] != SLASH[0] and src[nx, ny][:3] != SLASH[1]:
                        px[x, y] = OUTLINE + (255,)
                        break
    return img


def figure(dx=0, dy=0, lean=0, arm=("rest", 0), crouch=0, leg_spread=0, flinch=False):
    """Body builder. dx/dy shift, lean = torso tilt in px (+ forward), arm = pose.
    Figure faces RIGHT. Feet planted at y = 52."""
    img = new(); d = ImageDraw.Draw(img)
    cx = 30 + dx
    foot_y = 52 + dy
    hip_y = foot_y - 12 + crouch
    chest_y = hip_y - 10
    head_y = chest_y - 7 + (lean // 3)
    hx = cx + lean

    # ground shadow
    sh = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse([cx - 9, foot_y - 2, cx + 9, foot_y + 2], fill=SHADOW)
    img.alpha_composite(sh)

    # hakama (wide trousers) + legs
    ls = leg_spread
    poly(d, [(cx - 6 - ls, hip_y), (cx + 6 + ls, hip_y), (cx + 8 + ls, foot_y), (cx - 8 - ls, foot_y)], HAKAMA)
    d.rectangle([cx - 7 - ls, foot_y - 1, cx - 2 - ls, foot_y + 1], fill=HAKAMA[0])   # feet
    d.rectangle([cx + 2 + ls, foot_y - 1, cx + 7 + ls, foot_y + 1], fill=HAKAMA[0])

    # kimono torso (tilted by lean)
    poly(d, [(cx - 6 + lean, chest_y), (cx + 6 + lean, chest_y),
             (cx + 7, hip_y), (cx - 7, hip_y)], KIMONO)
    # sash
    d.rectangle([cx - 7, hip_y - 2, cx + 7, hip_y], fill=SASH[1])
    d.point((cx - 6, hip_y - 2), fill=SASH[2])

    # head (big, ~1/3): skin + hair topknot
    hy = head_y
    d.ellipse([hx - 5, hy - 6, hx + 5, hy + 4], fill=SKIN[1])
    d.ellipse([hx - 5, hy - 6, hx + 5, hy - 1], fill=HAIR[1])          # hair cap
    d.rectangle([hx - 1, hy - 9, hx + 1, hy - 5], fill=HAIR[1])        # topknot
    d.point((hx - 1, hy - 8), fill=HAIR[2])
    d.rectangle([hx - 5, hy - 3, hx + 1, hy - 1], fill=HAIR[0])        # fringe shadow
    d.point((hx + 3, hy), fill=OUTLINE)                                # eye
    d.point((hx + 2, hy + 2), fill=SKIN[0])                            # nose shade
    if flinch:
        d.point((hx + 3, hy), fill=SKIN[0]); d.line([(hx + 2, hy), (hx + 4, hy)], fill=OUTLINE)

    # arms + katana
    kind, ext = arm
    sx, sy = cx + 6 + lean, chest_y + 3   # shoulder
    if kind == "rest":           # blade low, held at side, tip down-forward
        d.line([(sx, sy), (sx + 4, sy + 6)], fill=SKIN[1], width=2)
        d.line([(sx + 4, sy + 6), (sx + 6, sy + 18)], fill=BLADE[1], width=2)
        d.line([(sx + 5, sy + 7), (sx + 6, sy + 17)], fill=BLADE[2], width=1)
    elif kind == "raise":        # blade back over shoulder (wind-up)
        d.line([(sx, sy), (sx - 2, sy - 5)], fill=SKIN[1], width=2)
        d.line([(sx - 2, sy - 5), (sx - 6 - ext, sy - 16 - ext)], fill=BLADE[1], width=2)
        d.line([(sx - 3, sy - 6), (sx - 6 - ext, sy - 15 - ext)], fill=BLADE[2], width=1)
    elif kind == "swing":        # blade out forward, horizontal-ish
        d.line([(sx, sy), (sx + 6, sy + 1)], fill=SKIN[1], width=2)
        d.line([(sx + 6, sy + 1), (sx + 18 + ext, sy + 2)], fill=BLADE[1], width=2)
        d.line([(sx + 7, sy), (sx + 18 + ext, sy + 1)], fill=BLADE[2], width=1)
    elif kind == "guard":        # blade vertical in front
        d.line([(sx, sy), (sx + 5, sy + 2)], fill=SKIN[1], width=2)
        d.line([(sx + 6, sy + 8), (sx + 6, sy - 10)], fill=BLADE[1], width=2)
        d.line([(sx + 7, sy + 7), (sx + 7, sy - 9)], fill=BLADE[2], width=1)
    elif kind == "parry":        # blade angled, deflecting
        d.line([(sx, sy), (sx + 5, sy - 1)], fill=SKIN[1], width=2)
        d.line([(sx + 4, sy + 6), (sx + 14, sy - 10)], fill=BLADE[1], width=2)
        d.line([(sx + 5, sy + 5), (sx + 14, sy - 9)], fill=BLADE[2], width=1)
    # tsuba / guard dot
    d.point((sx + (4 if kind == "rest" else 5), sy + (6 if kind == "rest" else 1)), fill=SASH[0])

    return outline(img)


def add_slash(img, cx, cy, r=14, start=200, end=330):
    d = ImageDraw.Draw(img)
    d.arc([cx - r, cy - r, cx + r, cy + r], start, end, fill=SLASH[0], width=3)
    d.arc([cx - r + 1, cy - r + 1, cx + r - 1, cy + r - 1], start + 10, end - 10, fill=SLASH[1], width=1)
    return img


def build():
    frames = {
        "idle":          [figure(), figure(dy=1)],
        "lean":          [figure(lean=-3, arm=("raise", 0))],
        "hold":          [figure(lean=-5, arm=("raise", 2), crouch=1)],
        "lunge":         [add_slash(figure(dx=8, lean=4, arm=("swing", 4), leg_spread=3), 52, 40, r=12, start=230, end=350)],
        "recover":       [figure(dx=4, lean=2, arm=("swing", 0), leg_spread=2)],
        "block":         [figure(lean=-1, arm=("guard", 0), crouch=1)],
        "parry":         [figure(dx=2, lean=1, arm=("parry", 0))],
        "hit":           [figure(dx=-4, lean=-4, arm=("rest", 0), flinch=True)],
        "dodge_up":      [figure(dy=-10, crouch=-2, arm=("rest", 0))],
        "dodge_down":    [figure(crouch=6, leg_spread=3, arm=("rest", 0))],
        "dodge_forward": [figure(dx=8, lean=3, leg_spread=2)],
        "dodge_back":    [figure(dx=-10, lean=-3, leg_spread=2)],
    }
    os.makedirs(OUT, exist_ok=True)
    total = sum(len(v) for v in frames.values())
    sheet = Image.new("RGBA", (W * total, W), (0, 0, 0, 0))
    meta = {"frame_size": W, "animations": {}}
    i = 0
    for name, fs in frames.items():
        meta["animations"][name] = {"start": i, "count": len(fs), "loop": name == "idle", "fps": 8}
        for f in fs:
            sheet.paste(f, (i * W, 0)); i += 1
    sheet.save(os.path.join(OUT, "samurai_sheet.png"))
    with open(os.path.join(OUT, "samurai_frames.json"), "w") as fh:
        json.dump(meta, fh, indent=2)
    # 4x preview for humans
    sheet.resize((sheet.width * 4, W * 4), Image.NEAREST).save(os.path.join(OUT, "samurai_preview.png"))
    print(f"wrote {total} frames -> {OUT}")


if __name__ == "__main__":
    build()
