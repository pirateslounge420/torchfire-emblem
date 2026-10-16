"""Showcase of every hand-pixelled fighter: stacked attack strips (5x) and one
GIF with all of them attacking in sync. Each fighter is tools/hand/<name>/frames.py.

    python3 tools/hand/showcase.py [name ...]      -> tools/hand/showcase.png / showcase.gif
"""
import importlib.util
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from handkit import render  # noqa: E402

BG = (52, 48, 66)
BEAT_MS = [500, 120, 220, 70, 320, 160, 500]
LABELS = ["stance", "back", "raised", "smear", "impact", "lower"]


def load(name):
    spec = importlib.util.spec_from_file_location(f"fighter_{name}", os.path.join(HERE, name, "frames.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    anims = mod.animations()
    beats = [anims["idle"][0][0], anims["lean"][0][0], anims["lean"][0][1], anims["lunge"][0][0], anims["lunge"][0][1], anims["recover"][0][0]]
    return mod, [render(g, mod.PAL) for g in beats]


def main():
    names = sys.argv[1:] or [d for d in sorted(os.listdir(HERE)) if os.path.exists(os.path.join(HERE, d, "frames.py"))]
    rows = []
    for n in names:
        try:
            mod, imgs = load(n)
            rows.append((n, imgs))
        except Exception as e:  # a fighter mid-draw shouldn't break the others
            print(f"skip {n}: {e}")
    if not rows:
        return
    zoom = 5
    cell = max(im.width for _, imgs in rows for im in imgs) * zoom
    cellh = max(im.height for _, imgs in rows for im in imgs) * zoom
    W = 6 * (cell + 6) + 80
    H = len(rows) * (cellh + 18)
    out = Image.new("RGB", (W, H), (30, 28, 40))
    d = ImageDraw.Draw(out)
    for r, (n, imgs) in enumerate(rows):
        y = r * (cellh + 18)
        d.text((4, y + cellh // 2), n, fill=(230, 230, 240))
        for i, im in enumerate(imgs):
            x = 80 + i * (cell + 6)
            if r == 0:
                d.text((x + 2, y + 2), LABELS[i], fill=(200, 200, 210))
            b = Image.new("RGBA", im.size, (*BG, 255)); b.alpha_composite(im)
            b = b.resize((im.width * zoom, im.height * zoom), Image.NEAREST)
            out.paste(b, (x, y + 16 + cellh - b.height))
    out.save(os.path.join(HERE, "showcase.png"))
    # GIF: all fighters side by side, same beat timing
    gz = 3
    frames = []
    seq = [0, 1, 2, 3, 4, 5, 0]
    for k in seq:
        cw = max(imgs[k].width for _, imgs in rows) * gz
        ch = max(imgs[k].height for _, imgs in rows) * gz
        fr = Image.new("RGBA", (len(rows) * (cw + 4), ch), (*BG, 255))
        for i, (n, imgs) in enumerate(rows):
            im = imgs[k]
            b = Image.new("RGBA", im.size, (*BG, 255)); b.alpha_composite(im)
            b = b.resize((im.width * gz, im.height * gz), Image.NEAREST)
            fr.paste(b, (i * (cw + 4), ch - b.height))
        frames.append(fr.convert("P", palette=Image.ADAPTIVE, colors=64))
    frames[0].save(os.path.join(HERE, "showcase.gif"), save_all=True, append_images=frames[1:], duration=BEAT_MS, loop=0)
    print("wrote showcase.png / showcase.gif for", ", ".join(n for n, _ in rows))


if __name__ == "__main__":
    main()
