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

## Prototype scope (on purpose)

- One attack type. It's tagged with a dodge direction (shown as a hint during the hold) so all four dodges are testable, but every swing is otherwise identical.
- AI attacker only, fixed cadence. Cadence variability is deferred per the design doc.
- Placeholder art drawn in code. Real GBA-style frames replace it by assigning a `SpriteFrames` to each Fighter — pose names are listed at the top of `Fighter.gd`.
