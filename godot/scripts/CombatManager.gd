class_name CombatManager
extends Node
## Runs the exchange: AI attacker winds up and strikes, player defends in
## real time with the four-tier ladder. Counts in physics frames (60/s).
##
## Flow per exchange:
##   LEAN -> HOLD -> LUNGE (window open) -> RESOLVE -> RECOVER -> next exchange
##
## PROTOTYPE SCOPE: one attack type ("regular"). It carries a dodge direction
## so the four dodges have something to read, but every attack is the same
## until multiple attack types return. The AI is a fixed-cadence attacker;
## cadence variability is deferred per the design doc.

enum Phase { IDLE, LEAN, HOLD, LUNGE, RESOLVE, RECOVER, OVER }

signal phase_changed(phase: Phase, frames_left: int, phase_total: int)
signal exchange_resolved(result: String, damage: int, target: Fighter)
signal match_over(winner: Fighter)

@export var attacker: Fighter
@export var defender: Fighter

var phase: Phase = Phase.IDLE
var frames_in_phase := 0
var phase_total := 0

# The current attack
var attack_damage := 0
var attack_dodge_dir := "dodge_down"  # which dodge beats this swing

# What the defender did this exchange
var holding_block := false
var pressed := ""          # "parry" / "dodge_x" / "block" — first decisive press
var pressed_at_frame := -999  # frame index relative to lunge start (neg = before)

var rng := RandomNumberGenerator.new()


func _ready() -> void:
	rng.randomize()


func start_match() -> void:
	attacker.hp = FrameData.MAX_HP
	defender.hp = FrameData.MAX_HP
	attacker.hp_changed.emit(attacker.hp)
	defender.hp_changed.emit(defender.hp)
	_begin_exchange()


func _begin_exchange() -> void:
	holding_block = false
	pressed = ""
	pressed_at_frame = -999
	var prof := attacker.profile()
	attack_damage = int(round(rng.randi_range(
		FrameData.REGULAR_DAMAGE_MIN, FrameData.REGULAR_DAMAGE_MAX) * prof["damage_mult"]))
	attack_dodge_dir = ["dodge_up", "dodge_down", "dodge_forward", "dodge_back"].pick_random()
	_enter(Phase.LEAN)


func _scaled(frames: int) -> int:
	return int(round(frames * attacker.profile()["duration_mult"]))


func _enter(p: Phase) -> void:
	phase = p
	frames_in_phase = 0
	match p:
		Phase.LEAN:
			phase_total = _scaled(FrameData.LEAN_FRAMES)
			attacker.set_pose("lean")
			defender.set_pose("idle")
		Phase.HOLD:
			phase_total = _scaled(FrameData.HOLD_FRAMES)
			attacker.set_pose("hold")
		Phase.LUNGE:
			phase_total = _scaled(FrameData.LUNGE_FRAMES)
			attacker.set_pose("lunge")
		Phase.RESOLVE:
			phase_total = 1
		Phase.RECOVER:
			phase_total = _scaled(FrameData.RECOVER_FRAMES)
			attacker.set_pose("recover")
		Phase.OVER:
			phase_total = 0
	phase_changed.emit(phase, phase_total, phase_total)


func _physics_process(_delta: float) -> void:
	if phase == Phase.IDLE or phase == Phase.OVER:
		return
	_read_input()
	frames_in_phase += 1
	phase_changed.emit(phase, phase_total - frames_in_phase, phase_total)
	if frames_in_phase >= phase_total:
		match phase:
			Phase.LEAN:    _enter(Phase.HOLD)
			Phase.HOLD:    _enter(Phase.LUNGE)
			Phase.LUNGE:   _enter(Phase.RESOLVE)
			Phase.RESOLVE: _resolve()
			Phase.RECOVER: _begin_exchange()


## Frame index relative to the first live lunge frame. Negative = before impact.
func _frame_rel_to_impact() -> int:
	match phase:
		Phase.LEAN: return frames_in_phase - phase_total - _scaled(FrameData.HOLD_FRAMES)
		Phase.HOLD: return frames_in_phase - phase_total
		Phase.LUNGE: return frames_in_phase
		_: return 999


func _read_input() -> void:
	holding_block = Input.is_action_pressed("block")
	if pressed != "":
		return  # first decisive press locks in
	var rel := _frame_rel_to_impact()
	var candidates := ["parry", "dodge_up", "dodge_down", "dodge_forward", "dodge_back", "block"]
	for action in candidates:
		if Input.is_action_just_pressed(action):
			pressed = action
			pressed_at_frame = rel
			defender.set_pose(action if action != "block" else "block")
			return


func _resolve() -> void:
	var result := "hit"
	var damage := attack_damage
	var target: Fighter = defender
	# Was the press inside its window? Windows are "within N frames before impact".
	var in_window := func(n: int) -> bool:
		return pressed_at_frame <= 0 and pressed_at_frame >= -n

	if pressed == "parry" and in_window.call(FrameData.PARRY_WINDOW):
		result = "parry"
		target = attacker
		damage = attack_damage          # counter-hit returns the attack's own value
	elif pressed.begins_with("dodge_") and in_window.call(FrameData.DODGE_WINDOW):
		if pressed == attack_dodge_dir:
			result = "dodge"
			damage = 0
		else:
			result = "wrong_dodge"      # read the attack wrong: full damage
	elif pressed == "block" and in_window.call(FrameData.PERFECT_BLOCK_WINDOW):
		result = "perfect_block"
		damage = 0
	elif holding_block or pressed == "block":
		result = "block"
		damage = int(ceil(attack_damage * FrameData.CHIP_RATIO))

	if damage > 0:
		target.take_damage(damage)
		# A parried attacker staggers (its own weapon's reel); a struck defender flinches.
		target.set_pose("stagger" if result == "parry" else "hit")
	exchange_resolved.emit(result, damage, target)

	if attacker.hp <= 0 or defender.hp <= 0:
		_enter(Phase.OVER)
		match_over.emit(defender if attacker.hp <= 0 else attacker)
	else:
		_enter(Phase.RECOVER)
