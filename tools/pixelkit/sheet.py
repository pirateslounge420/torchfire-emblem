"""Packing frames into the strip + JSON that godot/scripts/Fighter.gd loads,
plus preview images for review without opening Godot."""
from __future__ import annotations
import json
import os
from dataclasses import dataclass, field
from PIL import Image, ImageDraw


@dataclass
class Animation:
    name: str
    frames: list = field(default_factory=list)   # PIL RGBA images, all the same size
    fps: float = 8
    loop: bool = False


def pack_sheet(anims, out_dir, name, frame_w=64, frame_h=None, columns=16, faces="left", meta_extra=None):
    """Write <name>_sheet.png (a grid, `columns` wide) and <name>_frames.json.

    JSON layout matches what Fighter.gd reads: frame_size / frame_w / frame_h,
    columns, faces, and per-animation start/count/loop/fps. Frame index i lives
    at column i % columns, row i // columns.
    """
    frame_h = frame_h or frame_w
    os.makedirs(out_dir, exist_ok=True)
    total = sum(len(a.frames) for a in anims)
    rows = (total + columns - 1) // columns
    sheet = Image.new("RGBA", (columns * frame_w, rows * frame_h), (0, 0, 0, 0))
    meta = {"frame_size": frame_w, "frame_w": frame_w, "frame_h": frame_h, "columns": columns,
            "faces": faces, "animations": {}}
    if meta_extra:
        meta.update(meta_extra)
    i = 0
    for a in anims:
        meta["animations"][a.name] = {"start": i, "count": len(a.frames), "loop": a.loop, "fps": a.fps}
        for fr in a.frames:
            assert fr.size == (frame_w, frame_h), f"{a.name}: frame is {fr.size}, expected {(frame_w, frame_h)}"
            sheet.paste(fr, ((i % columns) * frame_w, (i // columns) * frame_h))
            i += 1
    sheet.save(os.path.join(out_dir, f"{name}_sheet.png"))
    with open(os.path.join(out_dir, f"{name}_frames.json"), "w") as f:
        json.dump(meta, f, indent=2)
    return sheet, meta


def _scale(img, k):
    return img.resize((img.width * k, img.height * k), Image.NEAREST)


def preview_gif(anims, path, scale=3, bg=(88, 140, 60), sequence=None, hold_last=0.35):
    """One looping GIF that plays every animation in turn (or `sequence`,
    a list of names) over a flat FE-green background."""
    frames, durs = [], []
    names = sequence or [a.name for a in anims]
    by = {a.name: a for a in anims}
    for n in names:
        a = by[n]
        for idx, fr in enumerate(a.frames):
            base = Image.new("RGBA", fr.size, bg + (255,))
            base.alpha_composite(fr)
            frames.append(_scale(base, scale).convert("P", palette=Image.ADAPTIVE, colors=64))
            d = 1000.0 / a.fps
            if idx == len(a.frames) - 1:
                d += hold_last * 1000
            durs.append(int(d))
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=durs, loop=0, disposal=2)


def preview_png(anims, path, scale=3, bg=(88, 140, 60), per_row=12):
    """Contact sheet: one row per animation, labelled, scaled up for review."""
    fw, fh = anims[0].frames[0].size
    rows = []
    for a in anims:
        n = len(a.frames)
        rows.append((a, (n + per_row - 1) // per_row))
    total_rows = sum(r for _, r in rows)
    pad = 14
    W = per_row * fw * scale
    H = total_rows * (fh * scale + pad)
    out = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(out)
    y = 0
    for a, nrows in rows:
        d.text((4, y + 1), f"{a.name}  ({len(a.frames)}f @ {a.fps}fps{' loop' if a.loop else ''})", fill=(255, 255, 255))
        for i, fr in enumerate(a.frames):
            x = (i % per_row) * fw * scale
            yy = y + pad + (i // per_row) * (fh * scale + pad)
            out.paste(_scale(fr, scale), (x, yy), _scale(fr, scale))
        y += nrows * (fh * scale + pad)
    out.save(path)
    return out


def contact_sheet(frames, path, scale=4, bg=(88, 140, 60), cols=8):
    """Quick zoomed grid of arbitrary frames."""
    fw, fh = frames[0].size
    rows = (len(frames) + cols - 1) // cols
    out = Image.new("RGB", (cols * fw * scale, rows * fh * scale), bg)
    for i, fr in enumerate(frames):
        s = _scale(fr, scale)
        out.paste(s, ((i % cols) * fw * scale, (i // cols) * fh * scale), s)
    out.save(path)
    return out
