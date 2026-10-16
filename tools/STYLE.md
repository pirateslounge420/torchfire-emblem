# Fighter battle sprites — style guide

All eight pure fighters are drawn with `tools/pixelkit` and a per-fighter
module in `tools/fighters/<name>.py`. **`tools/fighters/samurai.py` is the
reference implementation** — read it top to bottom before starting a new
fighter, and keep the same structure (palette → parts → weapon → FIGURE →
`P()` base pose → `animations()`).

Everything is drawn original. The GBA Fire Emblem rips are *style*
references only (proportions, palette discipline, motion) and never enter the
repo. Nothing is traced or copied.

## The look (what "Fire Emblem enough" means)

- **Scale.** 64×64 box, figure ~36–40 px tall, feet on `y = 54`. Head ~11 px
  with hair (about 1/3 of the height), hands and boots chunky, limbs 4 px.
  Heavy fighters go up to 42 px tall with 5–6 px limbs; lean ones stay 36.
- **One dark outline colour** on every silhouette and between overlapping
  parts (the kit does this when you `blit` with `outline=True`). Never pure
  black — the shared `OUTLINE` is `(24, 20, 37)`.
- **15 opaque colours max** (GBA budget). Three tones per material: highlight
  / base / shadow. Share slots to fit: hair shadow = outline, leather shadow =
  skin shadow, leather highlight = skin base, accent shadow = metal shadow,
  slash edge = metal highlight, white = cloth highlight. `draw_fighter.py`
  refuses to pack a sheet that uses more than 15.
- **Light from the upper-left.** Highlight on left/top edges (1 px), shadow
  on right/bottom (1–2 px), big flat base areas. Shadow mass is larger than
  highlight mass. Capsule limbs do this automatically.
- **Faces left.** The opponent is to the left. `near_*` limbs are the ones
  toward the viewer/opponent (drawn in front), `far_*` are behind the torso.
  The weapon lives in the **far** hand so swings cross the body toward the foe.
- **Trigram colour owns the costume.** Roughly 60 % of the cloth is the
  trigram ramp from `pixelkit.palette.TRIGRAM`; skin, hair, leather and steel
  are neutral. A second cloth ramp (`A a q`) is for trousers/undershirt.
- **Readable at 1×.** Check the contact sheet at 3× and the `_peek.png` at 5–6×,
  but the sprite is judged at 1×: big shapes, no 1-px noise, no dithering.
- **One shared medieval-fantasy world.** Everyone wears gear from the same
  fantasy kingdom; the archetype shows through weapon, colour and build, not
  through national costume. (So: a hooded light fighter, not a ninja suit; a
  bandana'd axeman, not a tricorn pirate.)

## Motion rules (GBA FE timing)

| animation | frames | fps | what it shows |
|---|---|---|---|
| `idle` | 4, loop | 6 | breathing: 1-px torso/weapon bob, frames A B C B |
| `lean` | 3 | 10 | wind-up: weight back, weapon raised/cocked, torso twists **away** (`torso="back"`) |
| `hold` | 2, loop | 5 | the tell: last lean pose ± 1 px tremble |
| `lunge` | 3 | 20 | **blur frame** (weapon `variant="blur"` + arc) → **impact** (full extension, `torso="side"`, deep stance) → follow-through |
| `recover` | 3 | 9 | pull back → weapon down → back to idle pose |
| `block` | 2 | 10 | guard raised in front; second frame braced (crouch 1–2 px, lean back) |
| `parry` | 3 | 12 | guard → deflecting swing (blur + small arc) → counter pose with `SPARK` |
| `hit` | 2 | 10 | flinch: `head="hurt"`, lean back 2 px, root +3 then +2 |
| `stagger` | 3 | 6 | **weapon-specific**: knocked back → the big recovery pose → half risen |
| `dodge_up` | 2 | 10 | crouch → airborne (`planted=False`, root y ≈ 24–29, `shadow=(6,1)`, `tip` boots) |
| `dodge_down` | 2 | 10 | half crouch → deep crouch, head tilted down |
| `dodge_forward` | 2 | 10 | step toward the foe (root −6, −10) with `dash_lines` trailing behind |
| `dodge_back` | 2 | 10 | hop away (root +6, +10) with `dash_lines` |
| `crit_lean` | 3 | 10 | a bigger wind-up than `lean`; last frame gets `variant="glint"` |
| `crit_hold` | 2, loop | 5 | last crit_lean pose, `STAR` flash toggling |
| `crit_lunge` | 5 | 20 | dash/leap → the big strike with a wide arc → impact `STAR` → follow-through |
| `crit_recover` | 3 | 9 | back to idle |

Phase lengths come from `godot/scripts/FrameData.gd` (lean 18, hold 24,
lunge 8, recover 20 engine frames at 60 fps); the fps above make each
animation fill its phase.

Motion grammar: **anticipation → snap → settle.** The wind-up is slow and
moves away from the foe; the strike covers the distance in one blur frame;
the impact pose is held with full extension; recovery drifts back. The whole
body moves (root x), not just the arm: lunge root −8 to −12 px, wind-up +2 to
+5 px. Keep the weapon tip inside the box — `RX = 36` leaves room to the left.

## Weapon-specific notes

- **Sword (Samurai)** — raise over the far shoulder, diagonal cut. Done.
- **Kusarigama (Shinobi)** — sickle in the far hand, chain + weight in the near
  hand. Regular: whip the weight out horizontally (chain as a `capsule` with
  `("M","m","n")`, 2 px, in segments that sag), yank, sickle slash. Critical:
  spin the weight overhead (arc of `e`) then a double sickle cut.
- **Axe (Berserker)** — one-handed broad axe, overhead chop. Wind-up raises it
  high behind the head; impact buries it low in front; recovery pulls it up.
  Critical: a full spin (two blur frames, 360° arc) ending in the chop.
- **Long mace (Bastion)** — two-handed, slow, heavy. Both hands on the haft
  (`near_hand`/`far_hand` both `grip`). Wind-up over the shoulder, impact is a
  downward smash with a ground `SPARK`/dust; stagger = rocks back on heels,
  does not kneel (too armoured to kneel).
- **Staff (Monk)** — two-handed, fast, acrobatic. Regular: a thrust (`torso=
  "side"`, staff horizontal). Critical: vault off the staff into a flying kick
  (airborne frames) then a spin strike.
- **Dagger (Jester)** — one short blade (8 px), fast stabs; low stance,
  tumbling dodges (dodge_forward = a roll: `planted=False`, body as a ball).
  Critical: a cartwheel into a triple stab (three blur frames).
- **Lance (Paladin, mounted)** and **glaive (Valkyrie, flying)** — see the
  mounted guide at the end.

## Heads

~10 wide × 11 tall, anchor at the neck (bottom centre, `(5, 11)`). Hair is
a big mass with one 2–3 px highlight streak; face is ~5×6 with the eye as
`o` + `w` (dark + glint) on row 6; chin tapers with `z`. Make a `hurt`
variant (eyes `oo`, mouth `z`). Helmets replace hair with `M m n` and keep
the same silhouette size.

## Torsos

~10 wide × 12 tall, anchor at the neck (top centre, `(5, 0)`); rows 0–7 chest,
row 8 belt, rows 9–11 hips. Make three: `front` (3/4, the default), `side`
(profile, 8 wide, used for lunges/thrusts) and `back` (twisted away for
wind-ups: highlight moves to the right side). Heavy armour: 12 wide, pauldron
blocks on the shoulders, `M m n` plates with `o` seams.

## Workflow

```
python3 tools/draw_fighter.py <name>            # sheet + json + gif + tools/_contact_<name>.png
python3 tools/peek.py <name> idle:0 lunge:1 ... # tools/_peek.png at 6x, --zoom= --cols=
```
Look at `_peek.png` after every change. Check: feet on the ground line,
nothing clipped by the box, weapon attached to the hand, arcs anchored to
`sh_far`/`wr_far`, hurt face on hit/stagger, ≤ 15 colours.

Never edit `tools/pixelkit/`. If you need a new shape, write a helper in your
own fighter module (see `katana`, `slash`, `dash_lines` in samurai.py).

## Mounted fighters (Paladin, Valkyrie)

Box 96×96, ground `y = 86`. The steed is a hand-drawn `Part` set (body with
2–3 leg positions: stand, gallop-stretch, gallop-gather; a rear pose for
`dodge_up`), blitted first; the rider is a `Figure` with `box=96`, seated
(legs `(140, 90)` / `(40, 90)`, root on the saddle, `planted=False`), drawn
over the steed. A lunge moves the whole steed. War horse: strong, heavy neck,
armoured chamfron, purple caparison. Wyvern: two legs, bat wings (wing `up`
and `down` variants alternate during idle), seafoam markings.
