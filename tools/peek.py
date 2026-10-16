#!/usr/bin/env python3
"""Zoomed contact sheet of chosen frames for review.

    python3 tools/peek.py samurai idle:0 lean:2 lunge:1 crit_lunge:2 [--zoom 6] [--cols 4]
    python3 tools/peek.py samurai lunge          # every frame of one animation
Writes tools/_peek.png
"""
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pixelkit import Canvas  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    opts = {a.split("=")[0][2:]: a.split("=")[1] for a in sys.argv[1:] if a.startswith("--") and "=" in a}
    zoom = int(opts.get("zoom", 6))
    cols = int(opts.get("cols", 4))
    name = args[0]
    mod = importlib.import_module(f"fighters.{name}")
    anims = {an: (poses, fps) for an, fps, loop, poses in mod.animations()}
    sel = []
    for a in args[1:]:
        if ":" in a:
            an, idx = a.split(":")
            sel.append((an, int(idx)))
        else:
            sel += [(a, i) for i in range(len(anims[a][0]))]
    frames = []
    for an, idx in sel:
        pose = anims[an][0][idx]
        cv = pose if isinstance(pose, Canvas) else mod.FIGURE.render(pose)
        img = mod.PALETTE.render(cv)
        bg = Image.new("RGBA", img.size, (88, 140, 60, 255))
        bg.alpha_composite(img)
        frames.append((f"{an}:{idx}", bg))
    fw, fh = frames[0][1].size
    rows = (len(frames) + cols - 1) // cols
    out = Image.new("RGB", (cols * fw * zoom, rows * (fh * zoom + 12)), (40, 70, 30))
    d = ImageDraw.Draw(out)
    for i, (label, fr) in enumerate(frames):
        x = (i % cols) * fw * zoom
        y = (i // cols) * (fh * zoom + 12)
        out.paste(fr.resize((fw * zoom, fh * zoom), Image.NEAREST), (x, y + 12))
        d.text((x + 2, y), label, fill=(255, 255, 255))
    p = os.path.join(HERE, "_peek.png")
    out.save(p)
    print("wrote", p)


if __name__ == "__main__":
    main()
