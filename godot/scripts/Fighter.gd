class_name Fighter
extends Node2D
## One combatant. Owns its HP, its pose, and its sprite.
##
## PLACEHOLDER ART: until the hand-drawn GBA-style frames land, every pose is
## generated in code inside the locked 64x64 frame box (see _build_placeholder_frames).
## To swap in real art, drop a SpriteFrames resource into `frames` in the
## editor and the placeholder builder is skipped. Pose names must match POSES.

const POSES := ["idle", "lean", "hold", "lunge", "recover", "block", "hit",
				"dodge_up", "dodge_down", "dodge_forward", "dodge_back", "parry", "stagger",
				"select"]   # select = the one-shot weapon flourish when the player picks this fighter

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

var art_faces_left := false
var art_origin := Vector2(32, 54)   # ground point under the figure, in sheet pixels
var art_box := Vector2(64, 64)


func _ready() -> void:
	if frames == null and art != "":
		frames = _load_sheet(art)
	if frames == null:
		frames = _build_placeholder_frames()
		sprite.centered = true
		sprite.offset = Vector2.ZERO
	sprite.sprite_frames = frames
	_apply_facing()
	set_pose("idle")


## Swap this fighter's art at runtime (used by the number keys in Main.gd).
func set_art(name: String) -> void:
	var sf := _load_sheet(name)
	if sf == null:
		return
	art = name
	frames = sf
	sprite.sprite_frames = frames
	_apply_facing()
	flourish()


## Play the pick-me flourish once (if the sheet has one), then settle back into idle.
func flourish() -> void:
	if frames.has_animation("select"):
		pose = "select"
		sprite.play("select")
		if not sprite.animation_finished.is_connected(_on_flourish_done):
			sprite.animation_finished.connect(_on_flourish_done)
	else:
		set_pose("idle")


func _on_flourish_done() -> void:
	if pose == "select":
		set_pose("idle")


func _apply_facing() -> void:
	# Hand-drawn sheets face LEFT (the GBA convention); placeholders face right.
	sprite.flip_h = facing_right if art_faces_left else not facing_right
	if not sprite.centered:
		# Keep the ground origin on the node whichever way the sheet is flipped.
		var ox := art_origin.x if not sprite.flip_h else art_box.x - art_origin.x
		sprite.offset = Vector2(-ox, -art_origin.y)


func set_pose(p: String) -> void:
	pose = p
	if frames.has_animation(p):
		sprite.play(p)


func take_damage(amount: int) -> void:
	hp = max(0, hp - amount)
	hp_changed.emit(hp)


func profile() -> Dictionary:
	return FrameData.ARCHETYPES.get(archetype, FrameData.ARCHETYPES["default"])


## Builds SpriteFrames from a sheet + JSON written by tools/draw_fighter.py.
## The sheet is a grid `columns` wide; frame i sits at (i % columns, i / columns).
## "origin" is the ground point under the figure, so the node's position is
## where the feet (or the steed's shadow) touch the floor for every box size.
func _load_sheet(name: String) -> SpriteFrames:
	var base := "res://art/%s/%s" % [name, name]
	var tex: Texture2D = load(base + "_sheet.png")
	var f := FileAccess.open(base + "_frames.json", FileAccess.READ)
	if tex == null or f == null:
		push_warning("Fighter: no art found for '%s', using placeholders" % name)
		return null
	var meta: Dictionary = JSON.parse_string(f.get_as_text())
	var fw: int = int(meta.get("frame_w", meta["frame_size"]))
	var fh: int = int(meta.get("frame_h", meta["frame_size"]))
	var columns: int = int(meta.get("columns", 9999))
	art_faces_left = meta.get("faces", "right") == "left"
	var origin: Array = meta.get("origin", [fw * 0.5, fh - 10])
	art_origin = Vector2(float(origin[0]), float(origin[1]))
	art_box = Vector2(fw, fh)
	sprite.centered = false
	var sf := SpriteFrames.new()
	sf.remove_animation("default")
	for anim in meta["animations"]:
		var a: Dictionary = meta["animations"][anim]
		sf.add_animation(anim)
		sf.set_animation_loop(anim, a["loop"])
		sf.set_animation_speed(anim, a["fps"])
		for i in range(a["count"]):
			var idx: int = int(a["start"]) + i
			var row: int = int(floor(float(idx) / float(columns)))
			var at := AtlasTexture.new()
			at.atlas = tex
			at.region = Rect2((idx % columns) * fw, row * fh, fw, fh)
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
