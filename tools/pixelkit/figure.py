"""The puppet: a GBA-proportioned figure (facing LEFT, like the FE rips) built
from hand-drawn text-grid parts plus shaded capsule limbs.

A pose is a plain dict; see `Figure.render` for the keys. Angles are in
degrees in screen space: 0 = right, 90 = straight down, 180 = left (toward
the opponent), -90 = up.
"""
from __future__ import annotations
import math
from .canvas import Canvas, Part, grid, flip_part
from .shapes import polyline_capsule, ellipse

GROUND_Y = 54   # bottom of the feet in the 64-px box

# Proportions. GBA infantry are ~36 px tall: head ~10, torso ~11, legs ~15.
BUILD = {
    "lean":   dict(upper=6, fore=6, thigh=7, shin=7, arm_w=3, leg_w=4, torso_h=11, shoulder_dx=3, shoulder_dy=2, hip_dx=2),
    "medium": dict(upper=6, fore=6, thigh=7, shin=7, arm_w=4, leg_w=5, torso_h=11, shoulder_dx=4, shoulder_dy=2, hip_dx=3),
    "heavy":  dict(upper=7, fore=6, thigh=7, shin=7, arm_w=5, leg_w=6, torso_h=12, shoulder_dx=5, shoulder_dy=3, hip_dx=4),
}

# --- default small parts (skin hands, leather boots) -------------------------
HANDS = {
    "fist": grid("""
.SS.
sssz
.zz.
""", anchor=(1, 1)),
    "open": grid("""
.SSs
ssss
.zzz
""", anchor=(1, 1)),
    "grip": grid("""
.SS.
Sssz
.szz
""", anchor=(1, 1)),
}

BOOTS = {
    # toe pointing left (toward the opponent); anchor = ankle (top centre)
    "side": grid("""
..LLl.
.Llllj
Llllljj
jjjjjjj
""", anchor=(3, 0)),
    # three-quarter / planted
    "front": grid("""
.LLl..
Lllllj
lllljj
jjjjjj
""", anchor=(2, 0)),
    # toe pointing right (a trailing back foot seen from the side)
    "back": grid("""
.lLL..
jllllL
jjllllL
jjjjjjj
""", anchor=(3, 0)),
    # ball of the foot (tiptoe / airborne)
    "tip": grid("""
.LLl.
lllll
.jjj.
""", anchor=(2, 0)),
}


def _pt(p, ang, length):
    r = math.radians(ang)
    return (p[0] + length * math.cos(r), p[1] + length * math.sin(r))


def _ip(p):
    return (int(round(p[0])), int(round(p[1])))


class Figure:
    """Holds a fighter's parts and renders poses.

    parts: dict with
        heads:  {variant: Part}       anchored at the neck (bottom-centre of the head)
        torsos: {name: Part}          anchored at the neck (top-centre of the torso)
        hands:  {variant: Part}       optional override, anchored at the wrist
        boots:  {variant: Part}       optional override, anchored at the ankle (top-centre)
        extras: {name: Part}          anything else (capes, sashes, coat tails)
    sleeves / pants: (hi, base, shadow) letters for the arm and leg capsules.
    weapon: callable(angle, variant) -> Part anchored at the grip, or None.
    """

    def __init__(self, build="medium", parts=None, sleeves=("C", "c", "k"), pants=("A", "a", "q"),
                 weapon=None, box=64, ground=None, arm_w=None, leg_w=None):
        self.b = dict(BUILD[build])
        if arm_w:
            self.b["arm_w"] = arm_w
        if leg_w:
            self.b["leg_w"] = leg_w
        self.parts = parts or {}
        self.hands = dict(HANDS)
        self.hands.update(self.parts.get("hands", {}))
        self.boots = dict(BOOTS)
        self.boots.update(self.parts.get("boots", {}))
        self.sleeves = sleeves
        self.pants = pants
        self.weapon = weapon
        self.box = box
        self.ground = ground if ground is not None else (GROUND_Y if box == 64 else box - 10)

    # ------------------------------------------------------------------
    def joints(self, pose):
        """Compute joint positions (floats) for a pose."""
        b = self.b
        root = pose.get("root", (32, 38))
        lean = pose.get("lean", (0, 0))
        th = pose.get("torso_h", b["torso_h"])
        pelvis = (root[0], root[1])
        neck = (pelvis[0] + lean[0], pelvis[1] - th + lean[1])
        sdx, sdy = b["shoulder_dx"], b["shoulder_dy"]
        sh_near = (neck[0] - sdx + pose.get("shoulder_near_dx", 0), neck[1] + sdy)
        sh_far = (neck[0] + sdx + pose.get("shoulder_far_dx", 0), neck[1] + sdy)
        hdx = b["hip_dx"]
        hip_near = (pelvis[0] - hdx + pose.get("hip_near_dx", 0), pelvis[1] + pose.get("hip_near_dy", 0))
        hip_far = (pelvis[0] + hdx + pose.get("hip_far_dx", 0), pelvis[1] + pose.get("hip_far_dy", 0))
        J = {"pelvis": pelvis, "neck": neck, "sh_near": sh_near, "sh_far": sh_far,
             "hip_near": hip_near, "hip_far": hip_far}
        for side in ("near", "far"):
            ua, fa = pose.get(f"{side}_arm", (90, 90))
            ul = pose.get(f"{side}_upper_len", b["upper"])
            fl = pose.get(f"{side}_fore_len", b["fore"])
            el = _pt(J[f"sh_{side}"], ua, ul)
            wr = _pt(el, fa, fl)
            J[f"el_{side}"], J[f"wr_{side}"] = el, wr
            ta, sa = pose.get(f"{side}_leg", (90, 90))
            tl = pose.get(f"{side}_thigh_len", b["thigh"])
            sl = pose.get(f"{side}_shin_len", b["shin"])
            kn = _pt(J[f"hip_{side}"], ta, tl)
            an = _pt(kn, sa, sl)
            J[f"kn_{side}"], J[f"an_{side}"] = kn, an
        return J

    def planted_root(self, pose):
        """Shift root vertically so the lowest boot sits on the ground line."""
        J = self.joints(pose)
        boot_h = 4
        lowest = max(J["an_near"][1], J["an_far"][1]) + boot_h
        root = pose.get("root", (32, 38))
        dy = self.ground - lowest
        return (root[0], root[1] + dy)

    # ------------------------------------------------------------------
    def render(self, pose) -> Canvas:
        """Pose keys (all optional):
            root (x,y)           pelvis position; planted=True (default) snaps feet to the ground
            lean (dx,dy)         neck offset: + dx = toward the viewer's right (away from the foe)
            torso 'name'         which torso grid
            head 'variant'       which head grid; head_off (dx,dy)
            near_arm / far_arm   (upper_angle, forearm_angle)
            near_leg / far_leg   (thigh_angle, shin_angle)
            near_hand / far_hand hand variant name or None
            near_boot / far_boot boot variant name or None
            weapon dict          hand='far'|'near'|None, angle, variant, off=(dx,dy), layer='top'|'front'|'far'|'back'
            extras [..]          (part_or_name, joint_or_(x,y), dx, dy, layer)
            effects [..]         (Part, x, y) drawn last, unoutlined
            shadow (rx, ry)      ground shadow; shadow_off (dx,dy); shadow=None for airborne
            order [..]           full layer order override
        """
        pose = dict(pose)
        if pose.get("planted", True):
            pose["root"] = self.planted_root(pose)
        J = self.joints(pose)
        b = self.b
        cv = Canvas(self.box, self.box)

        layers = {k: [] for k in ("shadow", "back", "far_arm", "far_leg", "mid", "torso",
                                  "near_leg", "front", "head", "near_arm", "top", "effects")}

        # ground shadow
        if pose.get("shadow", (9, 2)) is not None:
            rx, ry = pose.get("shadow", (9, 2))
            sx, sy = pose.get("shadow_off", (0, 0))
            layers["shadow"].append((ellipse((J["pelvis"][0] + sx, self.ground - 1 + sy), rx, ry), 0, 0, False))

        # limbs
        def limb(pts, w, letters, out_layer):
            layers[out_layer].append((polyline_capsule([_ip(p) for p in pts], w, letters), 0, 0, True))

        for side, arm_layer, leg_layer in (("far", "far_arm", "far_leg"), ("near", "near_arm", "near_leg")):
            if pose.get(f"{side}_arm", (90, 90)) is not None:
                limb([J[f"sh_{side}"], J[f"el_{side}"], J[f"wr_{side}"]], pose.get("arm_w", b["arm_w"]),
                     pose.get(f"{side}_sleeve", self.sleeves), arm_layer)
                hv = pose.get(f"{side}_hand", "fist")
                if hv:
                    hp = self.hands[hv]
                    if pose.get(f"{side}_hand_flip"):
                        hp = flip_part(hp)
                    wx, wy = _ip(J[f"wr_{side}"])
                    hx, hy = pose.get(f"{side}_hand_off", (0, 0))
                    layers[arm_layer].append((hp, wx + hx, wy + hy, True))
            if pose.get(f"{side}_leg", (90, 90)) is not None:
                limb([J[f"hip_{side}"], J[f"kn_{side}"], J[f"an_{side}"]], pose.get("leg_w", b["leg_w"]),
                     pose.get(f"{side}_pants", self.pants), leg_layer)
                bv = pose.get(f"{side}_boot", "side")
                if bv:
                    ax, ay = _ip(J[f"an_{side}"])
                    bx, by = pose.get(f"{side}_boot_off", (0, 0))
                    layers[leg_layer].append((self.boots[bv], ax + bx, ay + by, True))

        # torso + head
        tname = pose.get("torso", "front")
        torso = self.parts["torsos"][tname]
        nx, ny = _ip(J["neck"])
        layers["torso"].append((torso, nx, ny, True))
        hv = pose.get("head", "normal")
        if hv:
            hx, hy = pose.get("head_off", (0, 0))
            layers["head"].append((self.parts["heads"][hv], nx + hx, ny + hy, True))

        # extras
        for ex in pose.get("extras", []):
            part, at, dx, dy, layer = ex
            if isinstance(part, str):
                part = self.parts["extras"][part]
            if isinstance(at, str):
                px, py = _ip(J[at])
            else:
                px, py = at
            layers[layer].append((part, px + dx, py + dy, True))

        # weapon
        wp = pose.get("weapon")
        if wp and self.weapon:
            hand = wp.get("hand", "far")
            part = self.weapon(wp.get("angle", 90), wp.get("variant", "normal"))
            if hand in ("far", "near"):
                wx, wy = _ip(J[f"wr_{hand}"])
            else:
                wx, wy = wp.get("at", (32, 32))
            ox, oy = wp.get("off", (0, 0))
            layer = wp.get("layer", "far" if hand == "far" else "top")
            lay = {"top": "top", "front": "front", "far": "far_arm", "back": "back", "mid": "mid"}[layer]
            layers[lay].append((part, wx + ox, wy + oy, True))

        for fx in pose.get("effects", []):
            # (part, x, y) in canvas space, or (part, joint_name, dx, dy)
            if len(fx) == 4:
                part, jn, dx, dy = fx
                jx, jy = _ip(J[jn])
                layers["effects"].append((part, jx + dx, jy + dy, False))
            else:
                part, x, y = fx
                layers["effects"].append((part, x, y, False))

        order = pose.get("order", ["shadow", "back", "far_arm", "far_leg", "mid", "torso", "near_leg",
                                   "front", "head", "near_arm", "top", "effects"])
        for name in order:
            for part, x, y, outline in layers[name]:
                cv.blit(part, x, y, outline=outline)
        cv.outline_silhouette()
        return cv
