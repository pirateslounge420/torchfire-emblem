#!/usr/bin/env python3
"""Build a self-contained HTML page that plays every fighter's animations.

    python3 tools/build_preview.py            # writes preview/fighter-sprites.html

Reads godot/art/<name>/<name>_sheet.png + _frames.json for the roster below.
Everything (sheets as data URIs, metadata) is embedded, so the file can be
opened anywhere or published as an artifact.
"""
import base64
import io
import json
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
ART = os.path.join(ROOT, "godot", "art")
OUT = os.path.join(ROOT, "preview", "fighter-sprites.html")

ROSTER = [
    # name, title, trigram glyph, trigram, weapon, hexagram, colour word
    ("samurai",   "Samurai",   "☱", "Lake",     "Sword",      58, "silver"),
    ("shinobi",   "Shinobi",   "☲", "Fire",     "Kusarigama", 30, "red"),
    ("berserker", "Berserker", "☳", "Thunder",  "Axe",        51, "yellow"),
    ("bastion",   "Bastion",   "☶", "Mountain", "Long mace",  52, "orange"),
    ("monk",      "Monk",      "☷", "Earth",    "Staff",       2, "yellow"),
    ("jester",    "Jester",    "☵", "Water",    "Dagger",     29, "indigo"),
    ("paladin",   "Paladin",   "☰", "Heaven",   "Lance",       1, "violet"),
    ("valkyrie",  "Valkyrie",  "☴", "Wind",     "Glaive",     57, "seafoam"),
]

ANIM_ORDER = ["idle", "lean", "hold", "lunge", "recover", "block", "parry", "hit", "stagger",
              "dodge_up", "dodge_down", "dodge_forward", "dodge_back",
              "crit_lean", "crit_hold", "crit_lunge", "crit_recover"]


V2_ALIAS = {"berserker": "pirate", "paladin": "cavalier"}   # v2 folders use the archetype name


def load(name):
    """Prefer the hand-pixelled v2 sheet when it exists."""
    cands = [(os.path.join(ART, n + "_v2"), n) for n in (V2_ALIAS.get(name, name), name)] + [(os.path.join(ART, name), name)]
    for d, n in cands:
        png = os.path.join(d, f"{n}_sheet.png")
        js = os.path.join(d, f"{n}_frames.json")
        if os.path.exists(png) and os.path.exists(js):
            break
    else:
        return None
    with open(js) as f:
        meta = json.load(f)
    im = Image.open(png).convert("RGBA")
    cols = {}
    for px in list(im.getdata()):
        if px[3] == 255:
            cols[px[:3]] = cols.get(px[:3], 0) + 1
    swatches = [c for c, n in sorted(cols.items(), key=lambda kv: -kv[1])]
    buf = io.BytesIO()
    im.save(buf, format="PNG", optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode()
    frames = sum(a["count"] for a in meta["animations"].values())
    return {"meta": meta, "png": f"data:image/png;base64,{b64}", "swatches": swatches[:16], "frames": frames,
            "v2": d.endswith("_v2")}


def main():
    fighters = []
    for name, title, glyph, trigram, weapon, hexn, colour in ROSTER:
        data = load(name)
        entry = {"name": name, "title": title, "glyph": glyph, "trigram": trigram, "weapon": weapon,
                 "hex": hexn, "colour": colour, "ready": data is not None}
        if data:
            entry.update(data)
        fighters.append(entry)
    ready = [f for f in fighters if f["ready"]]
    print("ready:", ", ".join(f["name"] for f in ready))
    data_js = json.dumps({"fighters": fighters, "order": ANIM_ORDER})
    html = TEMPLATE.replace("/*__DATA__*/", data_js)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        f.write(html)
    print("wrote", OUT, f"{os.path.getsize(OUT) / 1024:.0f} KB")


TEMPLATE = r"""<title>Fighter Sprite Roster</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Pixelify+Sans:wght@400;600;700&family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&display=swap">
<style>
/* Layout: a control bar, then a 2-up (1-up on phones) grid of battle stages, one per fighter. */
:root {
  --bg: #e8edf5;
  --panel: #ffffff;
  --panel-2: #f1f4fa;
  --fg: #141c2e;
  --muted: #5a6681;
  --line: #c9d2e3;
  --accent: #2f5bc2;
  --accent-ink: #ffffff;
  --stage-sky-1: #8fc3e8;
  --stage-sky-2: #cfe6f4;
  --stage-ground: #5b8f3e;
  --stage-ground-2: #4a7a32;
  --display: "Pixelify Sans", "Press Start 2P", ui-monospace, monospace;
  --body: "Atkinson Hyperlegible", "Segoe UI", system-ui, sans-serif;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #11162a; --panel: #1a2138; --panel-2: #222a44; --fg: #e8edf8; --muted: #9aa6c4;
    --line: #2f3a5c; --accent: #8db2ff; --accent-ink: #0f1527;
    --stage-sky-1: #28406a; --stage-sky-2: #3a5a8a; --stage-ground: #3f6b2c; --stage-ground-2: #2f5221;
    color-scheme: dark;
  }
}
:root[data-theme="dark"] {
  --bg: #11162a; --panel: #1a2138; --panel-2: #222a44; --fg: #e8edf8; --muted: #9aa6c4;
  --line: #2f3a5c; --accent: #8db2ff; --accent-ink: #0f1527;
  --stage-sky-1: #28406a; --stage-sky-2: #3a5a8a; --stage-ground: #3f6b2c; --stage-ground-2: #2f5221;
  color-scheme: dark;
}
* { box-sizing: border-box; }
body { background: var(--bg); color: var(--fg); font-family: var(--body); font-size: 15px; line-height: 1.45;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px));
  padding-block: 18px 40px; }
header { display: flex; flex-wrap: wrap; align-items: baseline; gap: 6px 18px; max-width: 1180px; margin: 0 auto 14px; }
h1 { font-family: var(--display); font-weight: 700; font-size: clamp(24px, 4vw, 34px); margin: 0; letter-spacing: 0.5px; text-wrap: balance; }
header p { margin: 0; color: var(--muted); max-width: 62ch; }
.bar { max-width: 1180px; margin: 0 auto 16px; background: var(--panel); border: 1px solid var(--line); border-radius: 8px;
  padding: 10px 12px; display: flex; flex-wrap: wrap; gap: 10px 16px; align-items: center; position: sticky;
  top: env(safe-area-inset-top, 0px); z-index: 5; }
.bar label { display: inline-flex; align-items: center; gap: 6px; font-size: 13px; color: var(--muted); }
.bar select, .bar button { font: inherit; font-size: 13px; color: var(--fg); background: var(--panel-2); border: 1px solid var(--line);
  border-radius: 6px; padding: 5px 8px; }
.bar button { cursor: pointer; }
.bar button.primary { background: var(--accent); color: var(--accent-ink); border-color: var(--accent); font-weight: 700; }
.bar button:focus-visible, .bar select:focus-visible, .stage select:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.seg { display: inline-flex; border: 1px solid var(--line); border-radius: 6px; overflow: hidden; }
.seg button { border: 0; border-radius: 0; background: var(--panel-2); }
.seg button[aria-pressed="true"] { background: var(--accent); color: var(--accent-ink); }
.grid { max-width: 1180px; margin: 0 auto; display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 14px; }
.stage { background: var(--panel); border: 1px solid var(--line); border-radius: 8px; overflow: hidden; min-width: 0; display: flex; flex-direction: column; }
.stage .screen { position: relative; aspect-ratio: 3 / 2; max-width: 100%; overflow: hidden;
  background: linear-gradient(var(--stage-sky-1), var(--stage-sky-2) 70%, var(--stage-ground) 70%, var(--stage-ground-2)); }
.stage canvas { position: absolute; left: 50%; image-rendering: pixelated; image-rendering: crisp-edges; transform: translateX(-50%); }
.stage .hud { position: absolute; left: 8px; right: 8px; top: 6px; display: flex; justify-content: space-between; font-family: var(--display);
  font-size: 13px; color: #fff; text-shadow: 0 1px 0 #000, 1px 0 0 #000, 0 -1px 0 #000, -1px 0 0 #000; pointer-events: none; }
.stage .hud .hp { height: 6px; width: 90px; border: 1px solid #000; background: #2a2a2a; margin-top: 4px; }
.stage .hud .hp i { display: block; height: 100%; width: 100%; background: #6fd36a; }
.stage .fr { position: absolute; right: 8px; bottom: 6px; font-family: var(--display); font-size: 12px; color: #fff;
  text-shadow: 0 1px 0 #000, 1px 0 0 #000; font-variant-numeric: tabular-nums; pointer-events: none; }
.stage .info { padding: 10px 12px 12px; display: grid; grid-template-columns: 1fr auto; gap: 6px 10px; align-items: center; }
.stage h2 { font-family: var(--display); font-size: 20px; margin: 0; font-weight: 600; }
.stage h2 span { color: var(--muted); font-weight: 400; font-size: 15px; margin-left: 6px; }
.stage .meta { grid-column: 1 / -1; color: var(--muted); font-size: 13px; display: flex; flex-wrap: wrap; gap: 4px 14px; }
.stage select { font: inherit; font-size: 13px; color: var(--fg); background: var(--panel-2); border: 1px solid var(--line); border-radius: 6px; padding: 4px 6px; }
.sw { grid-column: 1 / -1; display: flex; gap: 2px; align-items: center; }
.sw i { width: 14px; height: 14px; border: 1px solid rgba(0,0,0,.25); display: inline-block; }
.sw small { color: var(--muted); margin-left: 6px; font-size: 12px; }
.pending .screen::after { content: "drawing…"; position: absolute; inset: 0; display: grid; place-items: center; font-family: var(--display); color: #fff;
  text-shadow: 0 1px 0 #000, 1px 0 0 #000; font-size: 16px; }
footer { max-width: 1180px; margin: 18px auto 0; color: var(--muted); font-size: 13px; }
kbd { font: inherit; font-size: 12px; border: 1px solid var(--line); border-radius: 4px; padding: 0 5px; background: var(--panel-2); }
@media (prefers-reduced-motion: reduce) { .stage canvas { transition: none; } }
</style>

<header>
  <h1>Fighter Sprite Roster</h1>
  <p>The eight pure fighters, drawn GBA Fire Emblem-style: 64×64 on foot, 96×96 mounted, 15 colours each. Pick an animation and watch it at speed.</p>
</header>

<div class="bar" role="toolbar" aria-label="Playback">
  <label>Animation
    <select id="anim"><option value="__all__">All, in sequence</option></select>
  </label>
  <button id="play" class="primary" type="button">Pause</button>
  <button id="prev" type="button" title="Step back one frame">◀ frame</button>
  <button id="next" type="button" title="Step forward one frame">frame ▶</button>
  <label>Speed
    <span class="seg" id="speed">
      <button type="button" data-v="1" aria-pressed="true">1×</button>
      <button type="button" data-v="0.5" aria-pressed="false">½×</button>
      <button type="button" data-v="0.25" aria-pressed="false">¼×</button>
    </span>
  </label>
  <label>Zoom
    <span class="seg" id="zoom">
      <button type="button" data-v="2" aria-pressed="false">2×</button>
      <button type="button" data-v="3" aria-pressed="true">3×</button>
      <button type="button" data-v="4" aria-pressed="false">4×</button>
    </span>
  </label>
  <label><input type="checkbox" id="flip"> Face right (player side)</label>
</div>

<div class="grid" id="grid"></div>

<footer>Sheets are packed 16 frames per row; the Godot build reads the same JSON. Wind-up → hold → strike → recover follow the timings in <code>FrameData.gd</code> (lean 18, hold 24, lunge 8, recover 20 frames at 60 fps). Keys: <kbd>space</kbd> pause, <kbd>←</kbd> <kbd>→</kbd> step, <kbd>1</kbd>–<kbd>8</kbd> jump a stage to the next animation.</footer>

<script>
const DATA = /*__DATA__*/;
const HOLD_LAST_MS = 420;   // pause on the last frame of a one-shot animation
const GAP_MS = 260;         // pause before a one-shot repeats
let zoom = 3, speed = 1, playing = true, flip = false, globalAnim = "__all__";
const stages = [];

function el(tag, cls, html) { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }

function buildStage(f) {
  const s = el("section", "stage" + (f.ready ? "" : " pending"));
  s.dataset.name = f.name;
  const screen = el("div", "screen");
  const cv = el("canvas");
  const hud = el("div", "hud");
  hud.innerHTML = `<div>${f.title.toUpperCase()}<div class="hp"><i></i></div></div><div>${f.glyph} ${f.trigram.toUpperCase()}</div>`;
  const fr = el("div", "fr", "");
  screen.append(cv, hud, fr);
  const info = el("div", "info");
  const h2 = el("h2", null, `${f.title}<span>#${f.hex} · ${f.weapon}</span>`);
  const sel = el("select");
  sel.setAttribute("aria-label", `${f.title} animation`);
  sel.id = `sel-${f.name}`;
  const meta = el("div", "meta");
  const sw = el("div", "sw");
  info.append(h2, sel, meta, sw);
  s.append(screen, info);
  const st = { f, el: s, cv, ctx: cv.getContext("2d"), fr, sel, img: null, anims: [], ai: 0, fi: 0, t: 0, holding: 0, own: null };
  if (f.ready) {
    const names = DATA.order.filter(n => f.meta.animations[n]);
    st.anims = names.map(n => ({ name: n, ...f.meta.animations[n] }));
    names.forEach(n => { const o = el("option"); o.value = n; o.textContent = n.replace("_", " "); sel.append(o); });
    const o = el("option"); o.value = "__all__"; o.textContent = "all, in sequence"; sel.prepend(o); sel.value = "__all__";
    sel.addEventListener("change", () => { st.own = sel.value; setStageAnim(st, sel.value); });
    meta.innerHTML = `<span>${f.frames} frames</span><span>${f.meta.frame_w}×${f.meta.frame_h} box</span><span>${f.swatches.length} colours</span>`;
    sw.innerHTML = f.swatches.map(c => `<i style="background:rgb(${c[0]},${c[1]},${c[2]})"></i>`).join("") + `<small>palette (most used first)</small>`;
    const img = new Image();
    img.onload = () => { st.img = img; draw(st); };
    img.src = f.png;
  } else {
    meta.innerHTML = `<span>sheet not drawn yet</span>`;
    sel.disabled = true;
  }
  return st;
}

function setStageAnim(st, name) {
  if (!st.anims.length) return;
  if (name === "__all__") { st.ai = 0; }
  else { st.ai = Math.max(0, st.anims.findIndex(a => a.name === name)); }
  st.fi = 0; st.t = 0; st.holding = 0;
  draw(st);
}

function sizeStage(st) {
  const fw = st.f.ready ? st.f.meta.frame_w : 64, fh = st.f.ready ? st.f.meta.frame_h : 64;
  st.cv.width = fw; st.cv.height = fh;
  st.cv.style.width = (fw * zoom) + "px"; st.cv.style.height = (fh * zoom) + "px";
  // feet on the 70% ground line: origin y maps to that line
  const oy = st.f.ready ? (st.f.meta.origin || [fw / 2, fh - 10])[1] : 54;
  st.cv.style.bottom = `calc(30% - ${(fh - oy) * zoom}px - 4px)`;
}

function draw(st) {
  if (!st.img) return;
  const m = st.f.meta, a = st.anims[st.ai];
  const idx = a.start + st.fi, cols = m.columns;
  const sx = (idx % cols) * m.frame_w, sy = Math.floor(idx / cols) * m.frame_h;
  const ctx = st.ctx;
  ctx.imageSmoothingEnabled = false;
  ctx.clearRect(0, 0, st.cv.width, st.cv.height);
  ctx.save();
  if (flip) { ctx.translate(st.cv.width, 0); ctx.scale(-1, 1); }
  ctx.drawImage(st.img, sx, sy, m.frame_w, m.frame_h, 0, 0, m.frame_w, m.frame_h);
  ctx.restore();
  st.fr.textContent = `${a.name} ${st.fi + 1}/${a.count}`;
}

function advance(st, dir) {
  const a = st.anims[st.ai];
  const seq = (st.own || globalAnim) === "__all__";
  st.fi += dir;
  if (st.fi >= a.count) {
    if (seq) { st.ai = (st.ai + 1) % st.anims.length; }
    st.fi = 0;
  } else if (st.fi < 0) {
    if (seq) { st.ai = (st.ai - 1 + st.anims.length) % st.anims.length; }
    st.fi = st.anims[st.ai].count - 1;
  }
  st.t = 0; st.holding = 0;
  draw(st);
}

let last = performance.now();
function tick(now) {
  const dt = Math.min(100, now - last); last = now;
  if (playing) {
    for (const st of stages) {
      if (!st.img) continue;
      const a = st.anims[st.ai];
      const frameMs = 1000 / a.fps / speed;
      st.t += dt;
      const onLast = st.fi === a.count - 1;
      const seq = (st.own || globalAnim) === "__all__";
      if (onLast && !a.loop) {
        // hold the final pose, then move on (sequence) or repeat after a short gap
        if (st.t >= frameMs + (seq ? HOLD_LAST_MS : HOLD_LAST_MS + GAP_MS) / speed) { advance(st, 1); }
      } else if (st.t >= frameMs) {
        st.t -= frameMs;
        st.fi++;
        if (st.fi >= a.count) st.fi = 0;
        draw(st);
      }
    }
  }
  requestAnimationFrame(tick);
}

// --- boot -------------------------------------------------------------------
const grid = document.getElementById("grid");
const animSel = document.getElementById("anim");
DATA.order.forEach(n => { const o = el("option"); o.value = n; o.textContent = n.replace("_", " "); animSel.append(o); });
for (const f of DATA.fighters) { const st = buildStage(f); stages.push(st); grid.append(st.el); sizeStage(st); }
animSel.addEventListener("change", () => { globalAnim = animSel.value; for (const st of stages) { st.own = null; if (st.sel) st.sel.value = globalAnim; setStageAnim(st, globalAnim); } });
document.getElementById("play").addEventListener("click", e => { playing = !playing; e.currentTarget.textContent = playing ? "Pause" : "Play"; });
document.getElementById("prev").addEventListener("click", () => { playing = false; document.getElementById("play").textContent = "Play"; stages.forEach(s => s.img && advance(s, -1)); });
document.getElementById("next").addEventListener("click", () => { playing = false; document.getElementById("play").textContent = "Play"; stages.forEach(s => s.img && advance(s, 1)); });
document.getElementById("flip").addEventListener("change", e => { flip = e.target.checked; stages.forEach(draw); });
for (const [id, setter] of [["speed", v => speed = v], ["zoom", v => { zoom = v; stages.forEach(sizeStage); stages.forEach(draw); }]]) {
  const seg = document.getElementById(id);
  seg.addEventListener("click", e => {
    const b = e.target.closest("button"); if (!b) return;
    seg.querySelectorAll("button").forEach(x => x.setAttribute("aria-pressed", x === b ? "true" : "false"));
    setter(parseFloat(b.dataset.v));
  });
}
document.addEventListener("keydown", e => {
  if (e.target.tagName === "SELECT" || e.target.tagName === "INPUT") return;
  if (e.key === " ") { e.preventDefault(); document.getElementById("play").click(); }
  else if (e.key === "ArrowLeft") document.getElementById("prev").click();
  else if (e.key === "ArrowRight") document.getElementById("next").click();
  else if (e.key >= "1" && e.key <= "8") { const st = stages[+e.key - 1]; if (st && st.anims.length) { st.own = st.anims[(st.ai + 1) % st.anims.length].name; st.sel.value = st.own; setStageAnim(st, st.own); } }
});
requestAnimationFrame(tick);
</script>
"""

if __name__ == "__main__":
    main()
