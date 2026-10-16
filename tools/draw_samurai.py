"""Draws original GBA-style battle frames for the Samurai (Lake / sword).

v2: studied the FE6 Myrmidon (Rutger / Fir) rips for proportions and stance —
nothing copied. Style rules:
- 64x64 frame box, figure ~36 px tall, head ~1/3 of height, small feet
- 16 colors incl. transparent; dark *colored* outline, never pure black
- 3 tones per surface (shadow / base / highlight), lit from upper-left
- myrmidon stance: forward foot, knees bent, blade low, torso twisted 3/4

Outputs godot/art/samurai/samurai_sheet.png + samurai_frames.json
Run:  python3 tools/draw_samurai.py
"""
import json, math, os
from PIL import Image, ImageDraw

W = 64
OUT = os.path.join(os.path.dirname(__file__), "..", "godot", "art", "samurai")

OUTLINE = (38, 30, 52)
SKIN   = [(176, 110, 82), (236, 184, 140), (255, 226, 196)]
HAIR   = [(24, 24, 40), (52, 52, 78), (92, 92, 120)]
KIMONO = [(118, 124, 142), (190, 196, 212), (238, 240, 248)]   # Lake silver
HAKAMA = [(44, 48, 70), (78, 84, 112), (116, 124, 150)]
SASH   = [(120, 40, 50), (190, 70, 80), (230, 120, 120)]
BLADE  = [(150, 160, 190), (220, 226, 240), (255, 255, 255)]
SLASH  = [(170, 220, 255), (255, 255, 255)]
SHADOW = (0, 0, 0, 70)


def new():
    return Image.new("RGBA", (W, W), (0, 0, 0, 0))


def limb(d, a, b, ramp, w=3):
    """A limb segment: base line, shadow edge below-right, highlight above-left."""
    d.line([a, b], fill=ramp[1], width=w)
    d.line([(a[0] + 1, a[1] + 1), (b[0] + 1, b[1] + 1)], fill=ramp[0], width=1)
    d.line([(a[0] - 1, a[1] - 1), (b[0] - 1, b[1] - 1)], fill=ramp[2], width=1)


def blade(d, hilt, tip):
    d.line([hilt, tip], fill=BLADE[1], width=2)
    d.line([(hilt[0], hilt[1] - 1), (tip[0], tip[1] - 1)], fill=BLADE[2], width=1)
    d.rectangle([hilt[0] - 1, hilt[1] - 2, hilt[0] + 1, hilt[1] + 2], fill=SASH[0])  # tsuba


def outline(img):
    px = img.load(); src = img.copy().load()
    for y in range(W):
        for x in range(W):
            if src[x, y][3] == 0:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < W and src[nx, ny][3] > 0 and src[nx, ny][:3] not in (SLASH[0], SLASH[1]):
                        px[x, y] = OUTLINE + (255,); break
    return img


def figure(dx=0, dy=0, lean=0, arm="rest", crouch=0, stride=4, flinch=False, airborne=False):
    """Faces RIGHT. lean: torso tilt px (+forward). stride: forward-foot offset.
    arm: rest | raise | swing | guard | parry | sheathe"""
    img = new(); d = ImageDraw.Draw(img)
    cx = 28 + dx
    foot_y = 52 + dy
    hip = (cx, foot_y - 13 + crouch)
    chest = (cx + lean, hip[1] - 10)
    head = (cx + lean + 1, chest[1] - 7)

    if not airborne:
        sh = Image.new("RGBA", (W, W), (0, 0, 0, 0))
        ImageDraw.Draw(sh).ellipse([cx - 9, 50, cx + 11, 54], fill=SHADOW)
        img.alpha_composite(sh)

    # --- legs (hakama): back leg straight, front leg bent forward ---
    back_foot = (cx - 5, foot_y)
    front_foot = (cx + 5 + stride, foot_y)
    knee = (cx + 3 + stride // 2, foot_y - 6 + crouch // 2)
    limb(d, hip, back_foot, HAKAMA, 5)
    limb(d, hip, knee, HAKAMA, 5)
    limb(d, knee, front_foot, HAKAMA, 5)
    # feet (dark, flat)
    d.rectangle([back_foot[0] - 3, foot_y - 1, back_foot[0] + 2, foot_y + 1], fill=HAKAMA[0])
    d.rectangle([front_foot[0] - 2, foot_y - 1, front_foot[0] + 3, foot_y + 1], fill=HAKAMA[0])

    # --- torso (kimono), 3/4 twist: wider at shoulders ---
    d.polygon([(chest[0] - 6, chest[1]), (chest[0] + 6, chest[1]),
               (hip[0] + 5, hip[1] + 1), (hip[0] - 5, hip[1] + 1)], fill=KIMONO[1])
    d.polygon([(chest[0] + 2, chest[1] + 2), (chest[0] + 6, chest[1]),
               (hip[0] + 5, hip[1] + 1), (hip[0] + 1, hip[1] + 1)], fill=KIMONO[0])   # shade right
    d.line([(chest[0] - 5, chest[1] + 1), (hip[0] - 4, hip[1])], fill=KIMONO[2])        # highlight left
    d.line([(chest[0] + 1, chest[1] + 1), (hip[0], hip[1])], fill=KIMONO[0])            # kimono fold
    # sash
    d.rectangle([hip[0] - 6, hip[1] - 1, hip[0] + 6, hip[1] + 1], fill=SASH[1])
    d.line([(hip[0] - 6, hip[1] - 1), (hip[0], hip[1] - 1)], fill=SASH[2])
    d.line([(hip[0] + 6, hip[1] + 1), (hip[0] + 8, hip[1] + 4)], fill=SASH[0])          # sash tail

    # --- back arm (behind torso) ---
    sh_b = (chest[0] - 4, chest[1] + 2)
    if arm in ("raise", "swing"):
        limb(d, sh_b, (sh_b[0] + 6, sh_b[1] - 6), SKIN, 3)   # both hands on hilt
    else:
        limb(d, sh_b, (sh_b[0] - 3, sh_b[1] + 8), SKIN, 3)

    # --- head: hair cap, topknot, face ---
    hx, hy = head
    d.ellipse([hx - 5, hy - 5, hx + 5, hy + 5], fill=SKIN[1])
    d.ellipse([hx - 5, hy - 6, hx + 5, hy], fill=HAIR[1])
    d.line([(hx - 4, hy - 1), (hx + 2, hy - 1)], fill=HAIR[0])            # fringe
    d.line([(hx - 3, hy - 5), (hx, hy - 5)], fill=HAIR[2])                # hair shine
    d.rectangle([hx - 1, hy - 9, hx + 1, hy - 5], fill=HAIR[1])           # topknot
    d.point((hx + 3, hy + 1), fill=OUTLINE)                                # eye
    d.line([(hx + 1, hy + 3), (hx + 4, hy + 3)], fill=SKIN[0])            # jaw shade
    if flinch:
        d.line([(hx + 2, hy + 1), (hx + 4, hy + 1)], fill=OUTLINE)

    # --- front arm + katana ---
    sh_f = (chest[0] + 5, chest[1] + 2)
    if arm == "rest":
        hand = (sh_f[0] + 3, sh_f[1] + 9); limb(d, sh_f, hand, SKIN, 3)
        blade(d, hand, (hand[0] + 9, hand[1] + 14))
    elif arm == "raise":
        hand = (sh_f[0] + 1, sh_f[1] - 7); limb(d, sh_f, hand, SKIN, 3)
        blade(d, hand, (hand[0] - 9, hand[1] - 12))
    elif arm == "swing":
        hand = (sh_f[0] + 9, sh_f[1] + 1); limb(d, sh_f, hand, SKIN, 3)
        blade(d, hand, (hand[0] + 17, hand[1] + 4))
    elif arm == "guard":
        hand = (sh_f[0] + 5, sh_f[1] + 3); limb(d, sh_f, hand, SKIN, 3)
        blade(d, (hand[0] + 1, hand[1] + 6), (hand[0] + 2, hand[1] - 13))
    elif arm == "parry":
        hand = (sh_f[0] + 7, sh_f[1] - 1); limb(d, sh_f, hand, SKIN, 3)
        blade(d, (hand[0] - 2, hand[1] + 7), (hand[0] + 9, hand[1] - 11))
    elif arm == "sheathe":
        hand = (sh_f[0] + 2, sh_f[1] + 8); limb(d, sh_f, hand, SKIN, 3)
        blade(d, hand, (hand[0] - 6, hand[1] + 10))
    return outline(img)


def add_slash(img, cx, cy, r=13, start=235, end=345):
    d = ImageDraw.Draw(img)
    d.arc([cx - r, cy - r, cx + r, cy + r], start, end, fill=SLASH[0], width=3)
    d.arc([cx - r + 1, cy - r + 1, cx + r - 1, cy + r - 1], start + 8, end - 8, fill=SLASH[1], width=1)
    return img


def build():
    frames = {
        "idle":          [figure(), figure(dy=1, lean=0)],
        "lean":          [figure(lean=-2, arm="raise", crouch=1)],
        "hold":          [figure(lean=-4, arm="raise", crouch=2, stride=2)],
        "lunge":         [add_slash(figure(dx=9, lean=5, arm="swing", stride=8, crouch=2), 54, 38)],
        "recover":       [figure(dx=5, lean=2, arm="swing", stride=6, crouch=1)],
        "block":         [figure(lean=-1, arm="guard", crouch=1)],
        "parry":         [figure(dx=2, lean=2, arm="parry", stride=5)],
        "hit":           [figure(dx=-4, lean=-5, arm="sheathe", flinch=True, stride=1)],
        "dodge_up":      [figure(dy=-11, crouch=-2, arm="rest", stride=2, airborne=True)],
        "dodge_down":    [figure(crouch=7, stride=7, arm="sheathe")],
        "dodge_forward": [figure(dx=9, lean=3, stride=9, arm="rest")],
        "dodge_back":    [figure(dx=-10, lean=-3, stride=1, arm="rest")],
        # Samurai stagger: parried mid-swing -> over-rotates, blade carried past,
        # back foot skids. Two frames: the stumble, then catching balance.
        "stagger":       [figure(dx=4, lean=7, arm="swing", stride=10, crouch=3, flinch=True),
                          figure(dx=1, lean=-2, arm="sheathe", stride=2, crouch=1, flinch=True)],
    }
    os.makedirs(OUT, exist_ok=True)
    total = sum(len(v) for v in frames.values())
    sheet = Image.new("RGBA", (W * total, W), (0, 0, 0, 0))
    meta = {"frame_size": W, "animations": {}}
    i = 0
    for name, fs in frames.items():
        meta["animations"][name] = {"start": i, "count": len(fs), "loop": name == "idle", "fps": (6 if name == "stagger" else 8)}
        for f in fs:
            sheet.paste(f, (i * W, 0)); i += 1
    sheet.save(os.path.join(OUT, "samurai_sheet.png"))
    with open(os.path.join(OUT, "samurai_frames.json"), "w") as fh:
        json.dump(meta, fh, indent=2)
    print(f"wrote {total} frames -> {OUT}")


if __name__ == "__main__":
    build()
