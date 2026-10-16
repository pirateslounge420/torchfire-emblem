"""Pull a pixel sprite off a phone photo / screenshot into a native-resolution letter grid.

    python3 tools/sf/extract.py <photo> <out_dir> [--bg red] [--crop x0 y0 x1 y1] [--colours 14]

Finds the pixel grid (scale + offset) by searching for the cell size whose cells are most
uniform, samples each cell's centre, drops the background colour, quantises the rest to
N colours (k-means on the pixel colours, with near-black folded into one), and writes
stance.txt (letters, '.' transparent, 'o' outline where the background fringe was) and
palette.txt ("letter r g b" per line) into out_dir. Mike's sprites come in this way.
"""
import os
import sys

import numpy as np
from PIL import Image
from scipy.cluster.vq import kmeans2

LETTERS = "ABCDEFGHIJKLMN"


BG_RGB = {"red": (228, 22, 26), "green": (72, 160, 80), "white": (255, 255, 255)}


def is_bg(rgb, bg, tol=70):
    """within `tol` (euclidean) of the background colour"""
    ref = np.array(BG_RGB[bg])
    return np.sqrt(((rgb - ref) ** 2).sum(-1)) < tol


def find_grid(sub, s_lo=10.0, s_hi=22.0):
    H, W = sub.shape[:2]
    best = None
    for s in np.arange(s_lo, s_hi + 0.01, 0.1):
        for ox in np.arange(0, s, s / 6):
            for oy in np.arange(0, s, s / 6):
                xs = np.arange(ox, W, s)[::3]
                ys = np.arange(oy, H, s)[::3]
                score, n = 0.0, 0
                for y in ys:
                    for x in xs:
                        x0, y0 = int(x), int(y)
                        x1, y1 = int(min(W - 1, x + s * 0.8)), int(min(H - 1, y + s * 0.8))
                        if x1 <= x0 or y1 <= y0:
                            continue
                        p = sub[[y0, y0, y1, y1], [x0, x1, x0, x1]]
                        score += np.abs(p - p.mean(0)).sum()
                        n += 1
                score /= max(n, 1)
                if best is None or score < best[0]:
                    best = (score, s, ox, oy)
    return best[1:]


def main():
    args = sys.argv[1:]
    photo, out_dir = args[0], args[1]
    bg = args[args.index("--bg") + 1] if "--bg" in args else "red"
    ncol = int(args[args.index("--colours") + 1]) if "--colours" in args else 14
    im = Image.open(photo).convert("RGB")
    if "--crop" in args:
        i = args.index("--crop")
        im = im.crop(tuple(int(v) for v in args[i + 1:i + 5]))
    a = np.array(im).astype(int)
    fg = ~is_bg(a, bg)
    fg[:int(a.shape[0] * 0.05), :] = False          # phone status bar
    rows = np.where(fg.any(1))[0]
    cols = np.where(fg.any(0))[0]
    sub = a[rows[0]:rows[-1] + 1, cols[0]:cols[-1] + 1]
    if "--scale" in args:
        s = float(args[args.index("--scale") + 1]); ox = oy = 0.0
        # refine the offset only
        best = None
        H0, W0 = sub.shape[:2]
        for ox_ in np.arange(0, s, s / 8):
            for oy_ in np.arange(0, s, s / 8):
                xs_ = np.arange(ox_, W0, s)[::3]; ys_ = np.arange(oy_, H0, s)[::3]
                sc, n = 0.0, 0
                for y in ys_:
                    for x in xs_:
                        x0, y0 = int(x), int(y); x1, y1 = int(min(W0 - 1, x + s * 0.8)), int(min(H0 - 1, y + s * 0.8))
                        if x1 <= x0 or y1 <= y0: continue
                        p = sub[[y0, y0, y1, y1], [x0, x1, x0, x1]]; sc += np.abs(p - p.mean(0)).sum(); n += 1
                sc /= max(n, 1)
                if best is None or sc < best[0]: best = (sc, ox_, oy_)
        ox, oy = best[1:]
    else:
        s, ox, oy = find_grid(sub)
    H, W = sub.shape[:2]
    xs = np.arange(ox + s / 2, W, s)
    ys = np.arange(oy + s / 2, H, s)
    nat = np.zeros((len(ys), len(xs), 3), int)
    alpha = np.zeros((len(ys), len(xs)), bool)
    for j, y in enumerate(ys):
        for i, x in enumerate(xs):
            y0, y1 = int(max(0, y - s * 0.3)), int(min(H, y + s * 0.3)) + 1
            x0, x1 = int(max(0, x - s * 0.3)), int(min(W, x + s * 0.3)) + 1
            m = sub[y0:y1, x0:x1].reshape(-1, 3).mean(0)
            nat[j, i] = m.astype(int)
            alpha[j, i] = not bool(is_bg(m[None, None, :], bg)[0, 0])
    r, g, b = nat[..., 0], nat[..., 1], nat[..., 2]
    # fringe = cells on the silhouette's edge that averaged sprite + background; interior cells are never fringe
    from scipy import ndimage
    edge = alpha & ~ndimage.binary_erosion(alpha)
    fringe = edge & is_bg(nat, bg, tol=140)
    clean = alpha & ~fringe
    pix = nat[clean].astype(float)
    dark = pix.sum(1) < 45
    np.random.seed(3)
    cent, lab = kmeans2(pix[~dark], ncol - 1, minit="++", iter=80)
    colors = [tuple(int(v) for v in c) for c in cent] + [(8, 8, 14)]
    labels = np.zeros(len(pix), int)
    labels[~dark] = lab
    labels[dark] = ncol - 1
    grid = [["."] * nat.shape[1] for _ in range(nat.shape[0])]
    k = 0
    for y in range(nat.shape[0]):
        for x in range(nat.shape[1]):
            if clean[y, x]:
                grid[y][x] = LETTERS[labels[k]]
                k += 1
    for y in range(nat.shape[0]):
        for x in range(nat.shape[1]):
            if alpha[y, x] and fringe[y, x]:
                nb = sum(clean[yy, xx] for yy, xx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1))
                         if 0 <= yy < nat.shape[0] and 0 <= xx < nat.shape[1])
                grid[y][x] = "o" if nb >= 1 and (g[y, x] + b[y, x]) < 200 else "."
    # trim empty rows/cols
    rows_txt = ["".join(rw) for rw in grid]
    while rows_txt and set(rows_txt[0]) == {"."}:
        rows_txt.pop(0)
    while rows_txt and set(rows_txt[-1]) == {"."}:
        rows_txt.pop()
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "stance.txt"), "w") as f:
        f.write(f"# extracted from {os.path.basename(photo)}: {len(rows_txt[0])}x{len(rows_txt)}, scale {s:.1f}, {ncol} colours + outline\n")
        f.write("\n".join(rows_txt) + "\n")
    with open(os.path.join(out_dir, "palette.txt"), "w") as f:
        for l, c in zip(LETTERS, colors):
            f.write(f"{l} {c[0]} {c[1]} {c[2]}\n")
    print(f"{out_dir}: {len(rows_txt[0])}x{len(rows_txt)} at scale {s:.1f}, {ncol} colours")


if __name__ == "__main__":
    main()
