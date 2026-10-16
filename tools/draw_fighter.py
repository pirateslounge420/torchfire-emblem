#!/usr/bin/env python3
"""Render one fighter's sprite sheet from tools/fighters/<name>.py.

    python3 tools/draw_fighter.py samurai            # sheet + json + previews
    python3 tools/draw_fighter.py samurai idle 0 8   # one frame, zoomed 8x, to tools/_peek_<name>.png

Each fighter module exposes:
    NAME, BOX (64 or 96), PALETTE (pixelkit.Palette), FIGURE (pixelkit.Figure)
    animations() -> list[(anim_name, fps, loop, [pose, ...])]
A pose may be a dict (rendered through FIGURE.render) or a pixelkit.Canvas.
"""
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from pixelkit import Animation, pack_sheet, preview_gif, preview_png, check_palette, Canvas  # noqa: E402

ROOT = os.path.join(HERE, "..")
ART = os.path.join(ROOT, "godot", "art")


def render_pose(mod, pose):
    if isinstance(pose, Canvas):
        return pose
    return mod.FIGURE.render(pose)


def main():
    name = sys.argv[1]
    mod = importlib.import_module(f"fighters.{name}")
    if len(sys.argv) >= 3:                      # peek at one frame
        anim = sys.argv[2]
        idx = int(sys.argv[3]) if len(sys.argv) > 3 else 0
        zoom = int(sys.argv[4]) if len(sys.argv) > 4 else 8
        for an, fps, loop, poses in mod.animations():
            if an == anim:
                cv = render_pose(mod, poses[idx])
                img = mod.PALETTE.render(cv)
                from PIL import Image
                bg = Image.new("RGBA", img.size, (88, 140, 60, 255))
                bg.alpha_composite(img)
                bg = bg.resize((img.width * zoom, img.height * zoom), Image.NEAREST)
                out = os.path.join(HERE, f"_peek_{name}.png")
                bg.save(out)
                print("wrote", out)
                return
        print("no such animation", anim)
        return

    anims = []
    letters = set()
    for an, fps, loop, poses in mod.animations():
        frames = []
        for p in poses:
            cv = render_pose(mod, p)
            letters |= cv.letters_used()
            frames.append(mod.PALETTE.render(cv))
        anims.append(Animation(an, frames, fps, loop))
    n = check_palette(mod.PALETTE, letters)
    out_dir = os.path.join(ART, mod.NAME)
    origin = [getattr(mod, "RX", mod.BOX // 2), getattr(mod, "GROUND", 54)]
    sheet, meta = pack_sheet(anims, out_dir, mod.NAME, frame_w=mod.BOX, frame_h=mod.BOX, columns=16,
                             meta_extra={"origin": origin})
    preview_gif(anims, os.path.join(out_dir, f"{mod.NAME}_preview.gif"), scale=3)
    preview_png(anims, os.path.join(HERE, f"_contact_{mod.NAME}.png"), scale=3)
    total = sum(len(a.frames) for a in anims)
    print(f"{mod.NAME}: {total} frames, {len(anims)} animations, {n} opaque colours, sheet {sheet.size}")


if __name__ == "__main__":
    main()
