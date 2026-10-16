"""Style study of the GBA Fire Emblem sprite sheets (reference only — nothing
from here enters the repo). For every sheet: background detection, sprite
component extraction, size / palette / outline statistics, and a montage of
representative frames for visual review.
"""
import json
import os
import sys
from collections import Counter, deque

from PIL import Image, ImageDraw

SRC_DIRS = ["/mnt/user-data/uploads/sprite sheets",
            "/root/.claude/uploads/833a9c3a-da8e-56d4-9d74-b292495ea2ad"]
OUT = "/tmp/claude-0/-home-claude/833a9c3a-da8e-56d4-9d74-b292495ea2ad/scratchpad/study"


def load(path):
    im = Image.open(path)
    if getattr(im, "n_frames", 1) > 1:
        im.seek(0)
    return im.convert("RGBA")


def components(im, bg):
    w, h = im.size
    px = im.load()
    seen = bytearray(w * h)
    comps = []
    for y0 in range(h):
        for x0 in range(w):
            if seen[y0 * w + x0]:
                continue
            p = px[x0, y0]
            if p[3] < 128 or p[:3] == bg:
                seen[y0 * w + x0] = 1
                continue
            # BFS
            q = deque([(x0, y0)])
            seen[y0 * w + x0] = 1
            pts = []
            while q:
                x, y = q.popleft()
                pts.append((x, y))
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx]:
                            pp = px[nx, ny]
                            seen[ny * w + nx] = 1
                            if pp[3] >= 128 and pp[:3] != bg:
                                q.append((nx, ny))
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            comps.append({"bbox": (min(xs), min(ys), max(xs) + 1, max(ys) + 1), "n": len(pts)})
    return comps


def analyse(path):
    im = load(path)
    w, h = im.size
    px = im.load()
    cnt = Counter()
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            p = px[x, y]
            if p[3] >= 128:
                cnt[p[:3]] += 1
    bg = cnt.most_common(1)[0][0]
    comps = components(im, bg)
    figs = [c for c in comps if 24 <= (c["bbox"][3] - c["bbox"][1]) <= 70 and (c["bbox"][2] - c["bbox"][0]) <= 90 and c["n"] > 250]
    heights = sorted(c["bbox"][3] - c["bbox"][1] for c in figs)
    widths = sorted(c["bbox"][2] - c["bbox"][0] for c in figs)
    # colours inside figure boxes (excluding bg)
    cols = Counter()
    edge = Counter()
    for c in figs[:40]:
        x0, y0, x1, y1 = c["bbox"]
        for y in range(y0, y1):
            for x in range(x0, x1):
                p = px[x, y]
                if p[3] < 128 or p[:3] == bg:
                    continue
                cols[p[:3]] += 1
                # silhouette edge: 4-neighbour is bg
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h:
                        q = px[nx, ny]
                        if q[3] < 128 or q[:3] == bg:
                            edge[p[:3]] += 1
                            break
    total_edge = sum(edge.values()) or 1
    edge_top = [(c, round(n / total_edge, 2)) for c, n in edge.most_common(4)]
    dark = sum(n for c, n in cols.items() if sum(c) < 150)
    return {
        "file": os.path.basename(path), "size": (w, h), "bg": bg, "figures": len(figs),
        "height_med": heights[len(heights) // 2] if heights else None,
        "height_range": (heights[0], heights[-1]) if heights else None,
        "width_med": widths[len(widths) // 2] if widths else None,
        "colours_in_figures": len(cols),
        "edge_colours": edge_top,
        "dark_share": round(dark / max(1, sum(cols.values())), 2),
        "comps": figs,
        "img": im, "px": px,
    }


def montage(results, path, per_sheet=6, zoom=3):
    rows = []
    for r in results:
        figs = sorted(r["comps"], key=lambda c: (c["bbox"][1] // 40, c["bbox"][0]))  # reading order
        pick = figs[:per_sheet]
        crops = []
        for c in pick:
            x0, y0, x1, y1 = c["bbox"]
            crop = r["img"].crop((x0 - 1, y0 - 1, x1 + 1, y1 + 1))
            bgimg = Image.new("RGBA", crop.size, (*r["bg"], 255))
            bgimg.alpha_composite(crop)
            crops.append(bgimg.resize((crop.width * zoom, crop.height * zoom), Image.NEAREST))
        rows.append((r["file"], crops))
    W = max(sum(c.width for c in crops) + 6 * len(crops) for _, crops in rows) if rows else 10
    H = sum(max([c.height for c in crops] + [10]) + 16 for _, crops in rows)
    out = Image.new("RGB", (max(W, 400), H), (30, 30, 36))
    d = ImageDraw.Draw(out)
    y = 0
    for name, crops in rows:
        d.text((2, y), name[:110], fill=(255, 255, 255))
        x = 0
        rh = max([c.height for c in crops] + [10])
        for c in crops:
            out.paste(c, (x, y + 14 + rh - c.height))
            x += c.width + 6
        y += rh + 16
    out.save(path)


def main():
    files = []
    for d in SRC_DIRS:
        for f in sorted(os.listdir(d)):
            if f.lower().endswith((".png", ".gif")) and "IMG_" not in f:
                files.append(os.path.join(d, f))
    # de-duplicate project copies of the same sheet
    seen = set()
    uniq = []
    for f in files:
        key = os.path.basename(f).split("-", 1)[-1] if "/.claude/" in f else os.path.basename(f)
        key = key.replace("_", " ").replace("  ", " ").lower()
        if key in seen:
            continue
        seen.add(key)
        uniq.append(f)
    results = []
    for f in uniq:
        try:
            r = analyse(f)
            results.append(r)
            print(f"{r['file'][:70]:70s} figs={r['figures']:3d} h_med={r['height_med']} h={r['height_range']} w_med={r['width_med']} cols={r['colours_in_figures']} dark={r['dark_share']} edge={r['edge_colours'][:2]}")
        except Exception as e:
            print("ERR", f, e)
    # montages, 5 sheets each
    for i in range(0, len(results), 5):
        montage(results[i:i + 5], os.path.join(OUT, f"montage_{i // 5:02d}.png"))
    summary = [{k: v for k, v in r.items() if k not in ("comps", "img", "px")} for r in results]
    with open(os.path.join(OUT, "summary.json"), "w") as fh:
        json.dump(summary, fh, indent=1)
    print(len(results), "sheets")


if __name__ == "__main__":
    main()


def crop_frames(path, indices=(0,), zoom=6, out="/tmp/claude-0/-home-claude/833a9c3a-da8e-56d4-9d74-b292495ea2ad/scratchpad/study/crop.png"):
    """Crop chosen figure frames (reading order) from one sheet at a zoom, for side-by-side study."""
    r = analyse(path)
    figs = sorted(r["comps"], key=lambda c: (c["bbox"][1] // 40, c["bbox"][0]))
    crops = []
    for i in indices:
        c = figs[i]; x0, y0, x1, y1 = c["bbox"]
        crop = r["img"].crop((x0 - 1, y0 - 1, x1 + 1, y1 + 1))
        bg = Image.new("RGBA", crop.size, (*r["bg"], 255)); bg.alpha_composite(crop)
        crops.append(bg.resize((crop.width * zoom, crop.height * zoom), Image.NEAREST))
    W = sum(c.width for c in crops) + 8 * len(crops); H = max(c.height for c in crops)
    o = Image.new("RGB", (W, H), (30, 30, 36)); x = 0
    for c in crops:
        o.paste(c, (x, H - c.height)); x += c.width + 8
    o.save(out)
    return out
