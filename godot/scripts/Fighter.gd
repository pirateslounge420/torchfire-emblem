class_name Fighter
extends Node2D
## One combatant. Owns its HP, its pose, and its sprite.
##
## PLACEHOLDER ART: until the hand-drawn GBA-style frames land, every pose is
## generated in code inside the locked 64x64 frame box (see _build_placeholder_frames).
## To swap in real art, drop a SpriteFrames resource into `frames` in the
## editor and the placeholder builder is skipped. Pose names must match POSES.

const POSES := ["idle", "lean", "hold", "lunge", "recover", "block", "hit",
				"dodge_up", "dodge_down", "dodge_forward", "dodge_back", "parry", "stagger"]

@export var fighter_name := "Fighter"
@export var archetype := "default"
@export var facing_right := true
@export var body_color := Color("4a6cf7")   # trigram color placeholder
@export var frames: SpriteFrames            # leave empty to use placeholders

var hp: int = FrameData.MAX_HP
var pose := "idle"

@onready var sprite: AnimatedSprite2D = $Sprite

signal hp_changed(new_hp: int)


## Folder name under res://art/ holding <name>_sheet.png + <name>_frames.json.
## Leave empty to use code-drawn placeholders.
@export var art := ""


func _ready() -> void:
	if frames == null and art != "":
		frames = _load_sheet(art)
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


## Builds SpriteFrames from a horizontal strip + JSON written by tools/draw_*.py.
func _load_sheet(name: String) -> SpriteFrames:
	var base := "res://art/%s/%s" % [name, name]
	var tex: Texture2D = load(base + "_sheet.png")
	var f := FileAccess.open(base + "_frames.json", FileAccess.READ)
	if tex == null or f == null:
		push_warning("Fighter: no art found for '%s', using placeholders" % name)
		return null
	var meta: Dictionary = JSON.parse_string(f.get_as_text())
	var size: int = meta["frame_size"]
	var sf := SpriteFrames.new()
	sf.remove_animation("default")
	for anim in meta["animations"]:
		var a: Dictionary = meta["animations"][anim]
		sf.add_animation(anim)
		sf.set_animation_loop(anim, a["loop"])
		sf.set_animation_speed(anim, a["fps"])
		for i in range(a["count"]):
			var at := AtlasTexture.new()
			at.atlas = tex
			at.region = Rect2((a["start"] + i) * size, 0, size, size)
			sf.add_frame(anim, at)
	return sf


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
		"stagger":
			out.append(_figure(5, 1, 3, Color.RED))
			out.append(_figure(-2, 0, 0, Color.RED))
	return out


## Draws a figure in the 64x64 frame box: head, torso, a weapon arm. dx/dy shift the body,
## arm_dx extends the weapon. `accent` colors the weapon.
func _figure(dx: int, dy: int, arm_dx: int, accent: Color = Color.LIGHT_GRAY) -> Texture2D:
	var img := Image.create(64, 64, false, Image.FORMAT_RGBA8)
	img.fill(Color(0, 0, 0, 0))
	var cx := 30 + dx
	var cy := 36 + dy
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
	for i in range(max(0, x), min(64, x + w)):
		for j in range(max(0, y), min(64, y + h)):
			img.set_pixel(i, j, c)
