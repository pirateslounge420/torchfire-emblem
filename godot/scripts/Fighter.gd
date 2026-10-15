class_name Fighter
extends Node2D
## One combatant. Owns its HP, its pose, and its sprite.
##
## PLACEHOLDER ART: until the hand-drawn GBA-style frames land, every pose is
## generated in code as a 32x32 pixel figure (see _build_placeholder_frames).
## To swap in real art, drop a SpriteFrames resource into `frames` in the
## editor and the placeholder builder is skipped. Pose names must match POSES.

const POSES := ["idle", "lean", "hold", "lunge", "recover", "block", "hit",
				"dodge_up", "dodge_down", "dodge_forward", "dodge_back", "parry"]

@export var fighter_name := "Fighter"
@export var archetype := "default"
@export var facing_right := true
@export var body_color := Color("4a6cf7")   # trigram color placeholder
@export var frames: SpriteFrames            # leave empty to use placeholders

var hp: int = FrameData.MAX_HP
var pose := "idle"

@onready var sprite: AnimatedSprite2D = $Sprite

signal hp_changed(new_hp: int)


func _ready() -> void:
	if frames == null:
		frames = _build_placeholder_frames()
	sprite.sprite_frames = frames
	sprite.flip_h = not facing_right
	set_pose("idle")


func set_pose(p: String) -> void:
	pose = p
	if frames.has_animation(p):
		sprite.play(p)


func take_damage(amount: int) -> void:
	hp = max(0, hp - amount)
	hp_changed.emit(hp)


func profile() -> Dictionary:
	return FrameData.ARCHETYPES.get(archetype, FrameData.ARCHETYPES["default"])


# ---------------------------------------------------------------------------
# Placeholder sprite generation. Each pose is a tiny stick-figure in the
# fighter's color, offset so the motion reads: lean back, hold, lunge forward.
# ---------------------------------------------------------------------------
func _build_placeholder_frames() -> SpriteFrames:
	var sf := SpriteFrames.new()
	sf.remove_animation("default")
	for p in POSES:
		sf.add_animation(p)
		sf.set_animation_loop(p, p == "idle")
		sf.set_animation_speed(p, 8.0)
		for tex in _frames_for_pose(p):
			sf.add_frame(p, tex)
	return sf


func _frames_for_pose(p: String) -> Array[Texture2D]:
	var out: Array[Texture2D] = []
	match p:
		"idle":
			out.append(_figure(0, 0, 0))
			out.append(_figure(0, 1, 0))
		"lean":
			out.append(_figure(-3, 0, -1))
		"hold":
			out.append(_figure(-5, 0, -2))
		"lunge":
			out.append(_figure(8, 0, 3))
		"recover":
			out.append(_figure(3, 0, 1))
		"block":
			out.append(_figure(-1, 0, 0, Color.WHITE))
		"parry":
			out.append(_figure(2, -1, 2, Color.GOLD))
		"hit":
			out.append(_figure(-4, 2, -2, Color.RED))
		"dodge_up":
			out.append(_figure(0, -8, 0))
		"dodge_down":
			out.append(_figure(0, 6, 0))
		"dodge_forward":
			out.append(_figure(6, 0, 1))
		"dodge_back":
			out.append(_figure(-8, 0, -1))
	return out


## Draws a 32x32 figure: head, torso, a weapon arm. dx/dy shift the body,
## arm_dx extends the weapon. `accent` colors the weapon.
func _figure(dx: int, dy: int, arm_dx: int, accent: Color = Color.LIGHT_GRAY) -> Texture2D:
	var img := Image.create(32, 32, false, Image.FORMAT_RGBA8)
	img.fill(Color(0, 0, 0, 0))
	var cx := 14 + dx
	var cy := 16 + dy
	# head
	_rect(img, cx - 2, cy - 10, 5, 5, body_color.lightened(0.3))
	# torso
	_rect(img, cx - 3, cy - 5, 7, 9, body_color)
	# legs
	_rect(img, cx - 3, cy + 4, 2, 6, body_color.darkened(0.3))
	_rect(img, cx + 2, cy + 4, 2, 6, body_color.darkened(0.3))
	# weapon arm, extending to the right (flip_h handles facing)
	_rect(img, cx + 4, cy - 3, 6 + arm_dx, 2, accent)
	return ImageTexture.create_from_image(img)


func _rect(img: Image, x: int, y: int, w: int, h: int, c: Color) -> void:
	for i in range(max(0, x), min(32, x + w)):
		for j in range(max(0, y), min(32, y + h)):
			img.set_pixel(i, j, c)
