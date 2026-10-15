extends Node2D
## Wires the scene together and drives the HUD / juice.

@onready var combat: CombatManager = $CombatManager
@onready var p1: Fighter = $Player
@onready var p2: Fighter = $Enemy
@onready var hud: CanvasLayer = $HUD
@onready var p1_bar: ProgressBar = $HUD/P1Bar
@onready var p2_bar: ProgressBar = $HUD/P2Bar
@onready var timing_bar: ProgressBar = $HUD/TimingBar
@onready var phase_label: Label = $HUD/PhaseLabel
@onready var result_label: Label = $HUD/ResultLabel
@onready var dodge_hint: Label = $HUD/DodgeHint
@onready var cam: Camera2D = $Camera2D

var shake_frames := 0
var shake_strength := 0.0

const PHASE_NAMES := {
	CombatManager.Phase.LEAN: "LEAN", CombatManager.Phase.HOLD: "HOLD",
	CombatManager.Phase.LUNGE: "!!!", CombatManager.Phase.RESOLVE: "",
	CombatManager.Phase.RECOVER: "recover", CombatManager.Phase.OVER: "MATCH OVER",
	CombatManager.Phase.IDLE: "",
}


func _ready() -> void:
	combat.attacker = p2
	combat.defender = p1
	p1.hp_changed.connect(func(v): p1_bar.value = v)
	p2.hp_changed.connect(func(v): p2_bar.value = v)
	combat.phase_changed.connect(_on_phase)
	combat.exchange_resolved.connect(_on_resolved)
	combat.match_over.connect(_on_over)
	result_label.text = ""
	combat.start_match()


func _on_phase(phase: CombatManager.Phase, frames_left: int, total: int) -> void:
	phase_label.text = PHASE_NAMES.get(phase, "")
	# Timing bar fills across lean+hold, so the player can learn the rhythm.
	if phase == CombatManager.Phase.LEAN or phase == CombatManager.Phase.HOLD:
		var lean := combat._scaled(FrameData.LEAN_FRAMES)
		var hold := combat._scaled(FrameData.HOLD_FRAMES)
		var elapsed := (lean - frames_left) if phase == CombatManager.Phase.LEAN else (lean + hold - frames_left)
		timing_bar.max_value = lean + hold
		timing_bar.value = elapsed
	elif phase == CombatManager.Phase.LUNGE:
		timing_bar.value = timing_bar.max_value
	# Prototype aid: show which dodge beats this swing during the hold.
	dodge_hint.text = ("dodge: " + combat.attack_dodge_dir.trim_prefix("dodge_")) \
		if phase == CombatManager.Phase.HOLD else ""


func _on_resolved(result: String, damage: int, target: Fighter) -> void:
	var text := {
		"hit": "HIT", "block": "BLOCK (chip)", "perfect_block": "PERFECT BLOCK",
		"dodge": "DODGE", "wrong_dodge": "WRONG READ", "parry": "PARRY!",
	}.get(result, result)
	result_label.text = text
	if damage > 0:
		_spawn_damage_number(target, damage)
		_flash(target)
		shake_frames = 6
		shake_strength = 3.0 if result != "parry" else 6.0


func _on_over(winner: Fighter) -> void:
	result_label.text = winner.fighter_name + " WINS  (R to restart)"


func _physics_process(_d: float) -> void:
	if shake_frames > 0:
		shake_frames -= 1
		cam.offset = Vector2(randf_range(-1, 1), randf_range(-1, 1)) * shake_strength
	else:
		cam.offset = Vector2.ZERO
	if Input.is_action_just_pressed("restart") and combat.phase == CombatManager.Phase.OVER:
		get_tree().reload_current_scene()


func _spawn_damage_number(target: Fighter, dmg: int) -> void:
	var l := Label.new()
	l.text = str(dmg)
	l.modulate = Color.WHITE
	l.position = target.position + Vector2(-6, -40)
	add_child(l)
	var tw := create_tween()
	tw.tween_property(l, "position:y", l.position.y - 24, 0.6)
	tw.parallel().tween_property(l, "modulate:a", 0.0, 0.6)
	tw.tween_callback(l.queue_free)


func _flash(target: Fighter) -> void:
	target.sprite.modulate = Color(3, 3, 3)
	var tw := create_tween()
	tw.tween_property(target.sprite, "modulate", Color.WHITE, 0.15)
