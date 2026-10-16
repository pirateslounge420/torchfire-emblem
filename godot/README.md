# Fighter — Godot prototype

Open this folder in **Godot 4.3+** (Import → pick `project.godot`) and press Play.

## What's here

| File | Job |
|---|---|
| `scripts/FrameData.gd` | **Every timing number**, in frames at 60 fps. Tune difficulty here. |
| `scripts/CombatManager.gd` | The exchange loop: AI winds up → holds → lunges; you defend. Resolves the four-tier ladder. |
| `scripts/Fighter.gd` | A combatant: HP, pose, sprite. Generates placeholder pixel figures until real art lands. |
| `scripts/Main.gd` | HUD, hit flash, screen shake, floating damage numbers. |
| `scenes/Main.tscn` | The arena. |

## Controls

- **J** — block. Hold early for a Standard Block (chip damage). Tap right at impact for a Perfect Block.
- **K** — parry (tightest window; counter-hits for the attack's own damage).
- **W / S / A / D** — dodge up / down / back / forward. Must match the attack's direction.
- **R** — restart after a match ends.
- **1–8** — swap your fighter's art (Samurai, Shinobi, Berserker, Bastion, Monk, Jester, Paladin, Valkyrie). **Shift+1–8** swaps the challenger's.

## Prototype scope (on purpose)

- One attack type. It's tagged with a dodge direction (shown as a hint during the hold) so all four dodges are testable, but every swing is otherwise identical.
- AI attacker only, fixed cadence. Cadence variability is deferred per the design doc.
- Battle sprites live in `art/<fighter>/` as a sheet + JSON written by `tools/draw_fighter.py` (see `tools/STYLE.md`). On-foot fighters use a 64×64 box, mounted ones 96×96; `Fighter.gd` reads the box size and ground origin from the JSON. Pose names are listed at the top of `Fighter.gd`; the `crit_*` animations are drawn but not yet driven by the combat loop.
