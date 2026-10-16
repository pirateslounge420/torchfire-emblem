# Hand-pixelled fighters — the method and the rules

This folder replaces the rig in `tools/pixelkit` for the final look. Nothing
here is generated: every pixel of every body is placed by hand in a text grid,
the way the GBA Fire Emblem sheets were drawn. Read `samurai/` end to end
before starting a fighter — `body.txt`, `body_back.txt`, `body_lunge.txt` and
`frames.py` are the pattern to copy.

The reference sheets (study only, never copied, never in the repo) are at
`/mnt/user-data/uploads/sprite sheets/` and
`/root/.claude/uploads/833a9c3a-da8e-56d4-9d74-b292495ea2ad/`. Crop the
class closest to yours and look at it at 5–8× next to your own frame before
every revision. `scratchpad/study/scan.py` shows how to crop single frames.

## What the sheets do (measured over 73 sheets)

- Infantry stand **32–41 px**; the head is ~10–11 px of that and the **legs are
  almost half the height** (hips at mid-height). Mounted figures run 45–58 px.
- **Exactly 15 opaque colours + transparency** per sprite — and all 15 painted
  (Mike, Oct 16): a fighter using fewer is leaving tone on the table. The jumps between
  tones are hard: deep red → bright red → white, not five near-identical darks.
  Our palettes: 3 tones for the trigram colour, 3 skin, 3 hair/neutral, 2 for a
  second cloth, 2 leather, 1 steel mid (steel edge = white), 1 outline = 15.
  Letters may share an RGB; only unique RGBs count. `handkit.Palette.check`
  refuses more than 15.
- **Outline (40,40,40)** on the silhouette and wherever two parts meet; inside a
  part the separating lines are the material's own dark tone.
- **Shading in bands, not lines**: 2–3 px highlight on the upper-left of each
  form, big flat mid, 3–4 px shadow on the lower-right, diagonal fold lines in
  the dark tone. About a third of the figure's pixels are dark.
- **Faces**: brow line 2 px, eye = dark pixel + white glint, nose dot, chin
  shadow. Hair is a mass with 2–3 px highlight strands and jagged tips.
- **Limbs articulate**: elbows bend, hands are 3×3 clusters, knees bend, feet
  point different ways. **Shoes are small** (5×2–3) with a highlight, not blocks.
- **Weapons are the biggest shape**: blades 20–26 px, axe heads two heads wide,
  lance/glaive longer than the figure is tall.

## Mike's register (dark, raw, edgy — early-2000s Yu-Gi-Oh card art)

- Clothes are **dark** (near-black cloth); the fighter's trigram colour is a
  saturated accent on hair, trousers, trim, sash or a glow — jewel tone on dark.
- **Baggy**: wide sleeves, loose trousers, robes, cloaks, plate — the physique is
  suggested, never drawn. **Slender**, not round: narrow waist, long legs.
- Faces are hard: scowl, narrowed eye, mask, hood, visor, horned or crested helm.
- Raw details: bandaged forearms, a scar, torn hems, a sash tail that whips.
- One glowing accent per fighter (eyes, gem, blade edge).

Trigram colours (Mike, Oct 15 — Thunder/Wind pending his confirmation):
Fire **red**, Mountain **orange**, Thunder **yellow**, Earth **green**,
Water **blue**, Lake **indigo**, Heaven **violet**, Wind **magenta**.

## The vibe (Mike, Oct 16): LANKY and SNAPPY, never blocky or basic

- **Lanky**: long thin limbs, narrow shoulders and hips, a long waist, small
  head (~1/4 of the height at most), big loose cloth hanging off a thin frame.
  Silhouettes made of diagonals and points (a sleeve that flares to a tip, a
  slanted hem, jagged hair), not rectangles. Break every straight edge longer
  than ~6 px with a 1-px step or a fold line.
- **Snappy**: poses at full extension, one smear frame between them, short
  holds; the anticipation frame is small and quick, the hit frame is extreme.
  No two consecutive frames with the same silhouette.
- Eyes are plain dark dots (no glint pixel).
- Every unit paints all 15 colours (+ transparent), with the smear fringe
  tinted in the unit's trigram colour.
- **Scale (Oct 16)**: Street Fighter Alpha / CPS2 detail at a **96×96 base
  box** — figures ~84 px tall, ground row 89, origin (48, 90); 15 colours, hard
  pixels. Drawn with `tools/big/bigkit.py` (hand-placed shapes + bands) in a
  160×128 design space and scaled 0.8 onto the box. Wide moves (lunges, smears)
  may use a wider box; the base unit is 96×96. The Samurai goes first.

## Mike's notes from the Samurai pass (Oct 15)

- Stand **tall and upright**, slim; no hunch; hips at mid-height.
- Hair **falls** (no spiked-back ponytail): a low tail hanging down the back
  that swings, trails and whips per beat; bangs over the brow (Kenshin shape).
- **Cloth moves**: bell sleeves hang from the elbow and swing, obi tails whip,
  the hakama flares in the lunge.
- Shading moodier: near-black cloth lit from the upper-left with a 1-px rim,
  the trigram colour kept for one big mass (the hakama).
- Feet move every beat; the sheath is worn on the NEAR side so the draw and
  resheathe are visible. At rest: no lean, feet under the shoulders, both legs even.
- Idle is 8 frames; every unit also has a one-shot "select" flourish.
- Costume notes: Pirate = durag + tattered below-the-knee pants, axe rests on
  the shoulder at idle; Shinobi = face hidden (mask + wrap, eye slit), flourish
  whirls the chain weight.

## The six beats of an attack (every GBA sword/axe/lance sheet uses them)

1. **stance** — wide, low, weight on the back foot, weapon held low-back.
2. **weapon back** — the arm swings the weapon further back/down; weight shifts.
3. **raised** — the weapon high behind the head (two hands for two-handed
   weapons), body leaning **away** from the foe, hair swept back.
4. **smear** — ONE frame where the whole weapon becomes a single pale wedge
   sweeping over the head toward the foe (letters `H`/`h`, no outline).
5. **impact** — full extension toward the foe: body lunged forward (head and
   torso lead, front knee driven out, back leg stretched), hair and sash
   streaming **back**, weapon level or buried low.
6. **lower / return** — weapon drops, body eases back to the stance.

Fluidity comes from the **body changing between beats**, not from the arm
alone: draw three bodies (stance, lean-back, lunge) and overlay the arms and
weapon per beat. For thrusts (lance) beats 3–5 become: lance couched back →
smear streak → full thrust. For a two-handed overhead chop (axe, mace) beat 5
buries the weapon at the foe's feet.

## Workflow

1. Draw `body.txt` (48×40, feet on the last row, facing LEFT, no far-side
   arm/weapon yet). Render at 8× (`handkit.render` + `strip`) and look. Compare
   against your reference class at the same zoom. Fix. Repeat until it reads.
2. Draw `body_back.txt` and `body_lunge.txt` the same way.
3. Write `frames.py` from the Samurai one: palette, body loader, overlays per
   beat, `animations()` returning idle(4) / lean(3) / hold(2) / lunge(3) /
   recover(3) with the same fps, `main()` writing `<name>_attack.png`,
   `<name>_attack.gif` and the Godot sheet to `godot/art/<name>_v2/`.
4. Check: 15 colours, feet on row 53 of the 64 box, nothing important clipped
   (a blade tip or smear may leave the box; a hand or head may not), the figure
   reads at 2× as well as at 8×.
