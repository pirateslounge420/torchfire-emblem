class_name FrameData
extends RefCounted
## All timing lives here, in FRAMES at 60 fps (same unit Melee players use).
## Tweak these numbers to tune difficulty. Nothing else in the project
## hard-codes timing.

# --- Attack phases (the attacker's cadence) ---------------------------------
# Lean (wind-up) -> Hold (the "tell") -> Lunge (the hit lands) -> Recover.
# The defender's window opens at the START of the lunge.
const LEAN_FRAMES    := 18
const HOLD_FRAMES    := 24
const LUNGE_FRAMES   := 8     # the hitbox is live for this long
const RECOVER_FRAMES := 20

# --- Defensive windows, measured from the first active lunge frame ---------
# Standard block: hold the button any time before the hit lands. Always works,
#   but ~15% chip damage gets through.
# Perfect block: press within this many frames before impact. Full negation.
#   (Melee powershield is ~2–4 frames; we start a touch wider.)
const PERFECT_BLOCK_WINDOW := 4
# Dodge: press the CORRECT direction within this window. Full negation.
const DODGE_WINDOW := 6
# Parry: the hardest input. Press within this window. Full negation + counter
#   hit that returns the attack's own damage to the attacker.
const PARRY_WINDOW := 2

# How early a press is still "early" rather than ignored. A press this many
# frames before the window opens counts as a whiffed attempt (punishable later).
const EARLY_PRESS_FRAMES := 12

# --- Damage ----------------------------------------------------------------
const REGULAR_DAMAGE_MIN := 8
const REGULAR_DAMAGE_MAX := 10
const CHIP_RATIO := 0.15
const MAX_HP := 100

# --- Archetype speed / power profiles (from the design doc) ----------------
# duration_mult scales every attack phase; damage_mult scales damage.
# Only the two extremes are filled in for the prototype; the rest slot in here.
const ARCHETYPES := {
	"rogue":       {"duration_mult": 0.75, "damage_mult": 0.85},
	"heavy_armor": {"duration_mult": 1.30, "damage_mult": 1.25},
	"default":     {"duration_mult": 1.00, "damage_mult": 1.00},
}
