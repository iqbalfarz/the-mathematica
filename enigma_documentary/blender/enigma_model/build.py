"""Build the Enigma I hero asset procedurally.

Every component is its own named object (ENIGMA_*), grouped in collections, so
shots can hide, isolate, explode or animate any part. Nothing is one big mesh.

    rig = build_enigma(config_dict)      # config from an enigma_core event stream
    rig.rotors["right"].rotation_euler.x # turn with rotate_rotor(), not by hand
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

import bpy
from mathutils import Vector

from lib import layout as L
from lib import materials as M
from lib import util as U

WIRINGS = {  # duplicated from enigma_core.wiring so Blender needs no project import
    "I": "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "II": "AJDKSIRUXBLHWTMCQGZNPYFVOE",
    "III": "BDFHJLCPRTXVZNYEIWGAKMUSQO", "IV": "ESOVPZJAYQUIRHXLNFTGKDCMWB",
    "V": "VZBRGITYUPSDNHLXAWMJQOFECK",
}
NOTCHES = {"I": "Q", "II": "E", "III": "V", "IV": "J", "V": "Z"}
REFLECTORS = {"A": "EJMZALYXVBWFCRQUONTSPIKHGD", "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
              "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL"}


@dataclass
class Rig:
    root: object
    cols: dict = field(default_factory=dict)
    parts: dict = field(default_factory=dict)          # name -> object
    keys: dict = field(default_factory=dict)           # letter -> key cap object
    lamps: dict = field(default_factory=dict)          # letter -> glowing letter object
    sockets: dict = field(default_factory=dict)
    rotors: dict = field(default_factory=dict)         # left/middle/right -> rotor parent
    cores: dict = field(default_factory=dict)          # left/middle/right -> wiring core (child)
    rotor_names: dict = field(default_factory=dict)
    rings: dict = field(default_factory=dict)
    pawls: dict = field(default_factory=dict)          # 1/2/3 -> pawl object
    mats: dict = field(default_factory=dict)
    config: dict = field(default_factory=dict)


def build_enigma(config: dict) -> Rig:
    mats = M.all_materials()
    root_col = U.collection("ENIGMA")
    cols = {n: U.collection(f"ENIGMA_{n}", root_col) for n in
            ("casing", "keyboard", "lampboard", "plugboard", "rotor_stack", "stepping", "wiring", "signal")}
    root = U.empty("ENIGMA_root", root_col, size=0.1)
    rig = Rig(root=root, cols=cols, mats=mats, config=config)
    _casing(rig)
    _keyboard(rig)
    _lampboard(rig)
    _plugboard(rig)
    _rotor_stack(rig)
    _stepping(rig)
    return rig


# ------------------------------------------------------------------ casing
def _casing(rig: Rig):
    c, m = rig.cols["casing"], rig.mats
    X, Y, Z, y0 = L.CASE["x"], L.CASE["y"], L.CASE["z"], L.CASE["y0"]
    yc = y0 + Y / 2
    t = 0.012
    W = L.CASE["wall"]
    parts = {
        "ENIGMA_case_base": ((X, Y, 0.012), (0, yc, 0.006)),
        "ENIGMA_case_left": ((t, Y, W), (-X / 2 + t / 2, yc, W / 2)),
        "ENIGMA_case_right": ((t, Y, W), (X / 2 - t / 2, yc, W / 2)),
        "ENIGMA_case_back": ((X, t, W), (0, y0 + Y - t / 2, W / 2)),
    }
    for name, (size, loc) in parts.items():
        rig.parts[name] = U.mesh_object(name, c, U.bm_box(*size, bevel=0.002), m["oak"], rig.root, loc)
    # Front panel (plugboard lives here), black crinkle paint.
    rig.parts["ENIGMA_front_panel"] = U.mesh_object(
        "ENIGMA_front_panel", c, U.bm_box(X - 2 * t, 0.006, Z - 0.012, bevel=0.001), m["crinkle"], rig.root,
        (0, y0 + 0.003, Z / 2 + 0.006))
    # Top deck: plate with the keyboard; lampboard plate; rotor well at the back.
    deck_front = (y0, -0.050)
    rig.parts["ENIGMA_deck_keyboard"] = U.mesh_object(
        "ENIGMA_deck_keyboard", c, U.bm_box(X - 2 * t, deck_front[1] - deck_front[0], 0.004, bevel=0.001),
        m["crinkle"], rig.root, (0, sum(deck_front) / 2, Z - 0.002))
    rig.parts["ENIGMA_deck_lamps"] = U.mesh_object(
        "ENIGMA_deck_lamps", c, U.bm_box(X - 2 * t, 0.075, 0.004, bevel=0.001), m["crinkle"], rig.root,
        (0, -0.0125, L.LAMP_Z - 0.002))
    # Rotor well: front wall between lampboard and rotors, rear deck behind them.
    rig.parts["ENIGMA_well_front"] = U.mesh_object(
        "ENIGMA_well_front", c, U.bm_box(X - 2 * t, 0.004, L.WINDOW_Z - L.LAMP_Z), m["crinkle"], rig.root,
        (0, 0.027, (L.WINDOW_Z + L.LAMP_Z) / 2))
    rig.parts["ENIGMA_well_back"] = U.mesh_object(
        "ENIGMA_well_back", c, U.bm_box(X - 2 * t, y0 + Y - t - 0.118, 0.004), m["crinkle"], rig.root,
        (0, (0.118 + y0 + Y - t) / 2, L.WINDOW_Z - 0.002))
    # Inner lid over the rotors, hinged at its back edge, with three windows.
    hinge = U.empty("ENIGMA_lid_hinge", c, (0, 0.118, L.WINDOW_Z), rig.root)
    rig.parts["ENIGMA_lid_hinge"] = hinge
    wl = 0.014
    lid_y0, lid_y1 = 0.028, 0.118
    xs = [L.AXIS_X[p] for p in ("left", "middle", "right")]
    xa, xb = -X / 2 + t, X / 2 - t
    strips = [(xa, xs[0] - wl / 2), (xs[0] + wl / 2, xs[1] - wl / 2), (xs[1] + wl / 2, xs[2] - wl / 2),
              (xs[2] + wl / 2, xb)]
    lid_parts = []
    for i, (a, b) in enumerate(strips):
        lid_parts.append(U.mesh_object(f"ENIGMA_lid_strip_{i}", c, U.bm_box(b - a, lid_y1 - lid_y0, 0.003),
                                       m["crinkle"], hinge, ((a + b) / 2, (lid_y0 + lid_y1) / 2 - 0.118, 0)))
    wy0, wy1 = L.ROTOR_AXIS_Y - 0.008, L.ROTOR_AXIS_Y + 0.008
    for x in xs:
        for (ya, yb) in ((lid_y0, wy0), (wy1, lid_y1)):
            lid_parts.append(U.mesh_object(f"ENIGMA_lid_window_frame_{x:.3f}_{ya:.3f}", c,
                                           U.bm_box(wl, yb - ya, 0.003), m["crinkle"], hinge,
                                           (x, (ya + yb) / 2 - 0.118, 0)))
    rig.parts["ENIGMA_lid"] = lid_parts
    U.text("ENIGMA_nameplate", c, "ENIGMA", 0.012, m["white"], (0, -0.046, Z + 0.0005), parent=rig.root)


# ------------------------------------------------------------------ keyboard
def _keyboard(rig: Rig):
    c, m = rig.cols["keyboard"], rig.mats
    for letter in L.ALPHA:
        x, y, z = L.key_pos(letter)
        stem = U.mesh_object(f"ENIGMA_key_{letter}", c, U.bm_cylinder(0.0022, 0.02, 16), m["steel"], rig.root,
                             (x, y, z - 0.01))
        cap = U.mesh_object(f"ENIGMA_keycap_{letter}", c, U.bm_cylinder(0.0105, 0.004, 40, bevel=0.0008),
                            m["crinkle"], stem, (0, 0, 0.012), smooth=True)
        disc = U.mesh_object(f"ENIGMA_keyface_{letter}", c, U.bm_cylinder(0.0088, 0.001, 40), m["ivory"], cap,
                             (0, 0, 0.0021), smooth=True)
        U.text(f"ENIGMA_keyletter_{letter}", c, letter, 0.014, m["ink"], (0, 0, 0.0006), extrude=0.0002,
               parent=disc)
        rig.keys[letter] = stem


# ------------------------------------------------------------------ lampboard
def _lampboard(rig: Rig):
    c, m = rig.cols["lampboard"], rig.mats
    for letter in L.ALPHA:
        x, y, z = L.lamp_pos(letter)
        U.mesh_object(f"ENIGMA_lampwindow_{letter}", c, U.bm_cylinder(0.0095, 0.0012, 40), m["lamp_window"],
                      rig.root, (x, y, z + 0.0006), smooth=True)
        glow = U.text(f"ENIGMA_lamp_{letter}", c, letter, 0.011, m["lamp"], (x, y, z + 0.0014), extrude=0.0002,
                      parent=rig.root)
        glow.color = (0, 0, 0, 1)
        bulb = U.mesh_object(f"ENIGMA_bulb_{letter}", c, U.bm_uv_sphere(0.004), m["lamp"], rig.root,
                             (x, y, z - 0.008), smooth=True)
        bulb.color = (0, 0, 0, 1)
        rig.lamps[letter] = (glow, bulb)


# ------------------------------------------------------------------ plugboard
def _plugboard(rig: Rig):
    c, m = rig.cols["plugboard"], rig.mats
    for letter in L.ALPHA:
        x, y, z = L.socket_pos(letter)
        s = U.mesh_object(f"ENIGMA_socket_{letter}", c, U.bm_cylinder(0.0055, 0.004, 32, axis="Y"),
                          m["bakelite"], rig.root, (x, y - 0.002, z), smooth=True)
        for dx in (-0.0022, 0.0022):
            U.mesh_object(f"ENIGMA_socket_{letter}_hole{'L' if dx < 0 else 'R'}", c,
                          U.bm_cylinder(0.0011, 0.0045, 12, axis="Y"), m["ink"], s, (dx, -0.0003, 0))
        U.text(f"ENIGMA_socketlabel_{letter}", c, letter, 0.006, m["white"], (x, y - 0.0005, z + 0.0095),
               rot=(math.pi / 2, 0, 0), parent=rig.root)
        rig.sockets[letter] = s
    set_plugboard(rig, rig.config.get("plugboard", ""))


def set_plugboard(rig: Rig, spec: str):
    """(Re)draw plugboard cables for pairs like 'AV BS CG'."""
    col = rig.cols["plugboard"]
    for ob in [o for o in col.objects if o.name.startswith("ENIGMA_cable_")]:
        bpy.data.objects.remove(ob, do_unlink=True)
    for pair in (spec or "").split():
        a, b = pair[0], pair[1]
        pa, pb = Vector(L.socket_pos(a)), Vector(L.socket_pos(b))
        sag = min(pa.z, pb.z) - 0.03 - 0.1 * (pa - pb).length
        pts = [tuple(pa + Vector((0, -0.008, 0))), tuple(pa + Vector((0, -0.03, -0.01))),
               ((pa.x + pb.x) / 2, pa.y - 0.05, sag), tuple(pb + Vector((0, -0.03, -0.01))),
               tuple(pb + Vector((0, -0.008, 0)))]
        U.poly_curve(f"ENIGMA_cable_{a}{b}", col, pts, bevel=0.0018, material=rig.mats["bakelite"],
                     parent=rig.root)


# ------------------------------------------------------------------ rotors
def _rotor_stack(rig: Rig):
    cfg = rig.config
    names = cfg["rotors"].split() if isinstance(cfg["rotors"], str) else list(cfg["rotors"])
    rings = [ord(ch) - 65 for ch in cfg.get("rings", "AAA")]
    positions = [ord(ch) - 65 for ch in cfg.get("positions", "AAA")]
    for slot, name, ring, pos in zip(("left", "middle", "right"), names, rings, positions):
        _rotor(rig, slot, name, ring, pos)
    _reflector(rig, cfg.get("reflector", "B"))
    _entry_wheel(rig)
    c, m = rig.cols["rotor_stack"], rig.mats
    rig.parts["ENIGMA_axle"] = U.mesh_object(
        "ENIGMA_axle", c, U.bm_cylinder(0.004, 0.16, 24, axis="X"), m["steel"], rig.root,
        (-0.005, L.ROTOR_AXIS_Y, L.ROTOR_AXIS_Z), smooth=True)


def _rotor(rig: Rig, slot: str, name: str, ring: int, pos: int):
    c, m = rig.cols["rotor_stack"], rig.mats
    x = L.AXIS_X[slot]
    parent = U.empty(f"ENIGMA_rotor_{slot}", c, (x, L.ROTOR_AXIS_Y, L.ROTOR_AXIS_Z), rig.root, size=0.03)
    parent.rotation_mode = "XYZ"
    parent.rotation_euler.x = L.rotor_angle(pos)
    parent["rotor_name"] = name
    rig.rotors[slot], rig.rotor_names[slot], rig.rings[slot] = parent, name, ring
    w = L.ROTOR_W
    # Alphabet ring (turns with the rotor; its letters show in the window)
    ringob = U.mesh_object(f"ENIGMA_rotor_{slot}_ring", c, U.bm_cylinder(L.ROTOR_R, w * 0.55, 78, axis="X"),
                           m["crinkle"], parent, (0.0015, 0, 0), smooth=True)
    for k in range(26):
        a = k * L.STEP
        U.text(f"ENIGMA_rotor_{slot}_ringletter_{L.ALPHA[k]}", c, L.ALPHA[k], 0.0085, m["white"],
               (0.0015, -(L.ROTOR_R + 0.0002) * math.sin(a), (L.ROTOR_R + 0.0002) * math.cos(a)),
               rot=(a, 0, 0), parent=parent)
    notch = NOTCHES[name]
    na = (L.ALPHA.index(notch) + 0.5) * L.STEP   # turnover notch cut just after the notch letter
    U.mesh_object(f"ENIGMA_rotor_{slot}_notch", c, U.bm_box(0.004, 0.006, 0.004), m["brass"], parent,
                  (-w / 2 + 0.002, -(L.ROTOR_R + 0.001) * math.sin(na), (L.ROTOR_R + 0.001) * math.cos(na)))
    # Thumbwheel (serrated, left side) and ratchet (26 teeth, right side)
    U.mesh_object(f"ENIGMA_rotor_{slot}_thumbwheel", c, U.bm_gear(L.ROTOR_R + 0.004, 0.004, 52, 0.0016),
                  m["bakelite"], parent, (-w / 2 + 0.001, 0, 0))
    U.mesh_object(f"ENIGMA_rotor_{slot}_ratchet", c, U.bm_gear(L.ROTOR_R - 0.012, 0.003, 26, 0.003),
                  m["steel"], parent, (w / 2 - 0.0005, 0, 0))
    # Wiring core, rotated by the ring setting relative to the ring
    core = U.empty(f"ENIGMA_rotor_{slot}_core", c, (0, 0, 0), parent, size=0.02)
    core.rotation_mode = "XYZ"
    core.rotation_euler.x = L.core_angle(ring)
    rig.cores[slot] = core
    body = U.mesh_object(f"ENIGMA_rotor_{slot}_body", c, U.bm_cylinder(L.ROTOR_R - 0.003, w * 0.9, 64, axis="X"),
                         m["bakelite"], core, smooth=True)
    body["xray_material"] = "core_glass"
    wiring = WIRINGS[name]
    for k in range(26):
        a = k * L.STEP
        py, pz = -L.CONTACT_R * math.sin(a), L.CONTACT_R * math.cos(a)
        U.mesh_object(f"ENIGMA_rotor_{slot}_pin_{k:02d}", c, U.bm_cylinder(0.0014, 0.003, 10, axis="X"),
                      m["brass"], core, (w / 2 + 0.001, py, pz), smooth=True)
        U.mesh_object(f"ENIGMA_rotor_{slot}_plate_{k:02d}", c, U.bm_cylinder(0.0017, 0.0008, 12, axis="X"),
                      m["brass"], core, (-w / 2 - 0.0002, py, pz), smooth=True)
    # Internal wires (core frame): right-face pin j -> left-face plate wiring[j]
    cu = bpy.data.curves.new(f"ENIGMA_rotor_{slot}_wires", "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = 0.00035
    for j in range(26):
        o = L.ALPHA.index(wiring[j])
        aj, ao = j * L.STEP, o * L.STEP
        d = (ao - aj + math.pi) % (2 * math.pi) - math.pi
        am = aj + d / 2
        pts = [(w / 2, -L.CONTACT_R * math.sin(aj), L.CONTACT_R * math.cos(aj)),
               (w / 6, -L.CONTACT_R * 0.6 * math.sin(am), L.CONTACT_R * 0.6 * math.cos(am)),
               (-w / 6, -L.CONTACT_R * 0.6 * math.sin(am), L.CONTACT_R * 0.6 * math.cos(am)),
               (-w / 2, -L.CONTACT_R * math.sin(ao), L.CONTACT_R * math.cos(ao))]
        U.add_spline(cu, pts)
    cu.materials.append(m["copper"])
    wires = bpy.data.objects.new(f"ENIGMA_rotor_{slot}_wires", cu)
    rig.cols["wiring"].objects.link(wires)
    wires.parent = core
    wires.hide_render = True           # revealed by show_wiring()
    rig.parts[f"ENIGMA_rotor_{slot}_wires"] = wires


def _reflector(rig: Rig, name: str):
    c, m = rig.cols["rotor_stack"], rig.mats
    x = L.AXIS_X["reflector"]
    ob = U.mesh_object("ENIGMA_reflector", c, U.bm_cylinder(L.ROTOR_R - 0.004, L.ROTOR_W * 0.8, 64, axis="X"),
                       m["crinkle"], rig.root, (x, L.ROTOR_AXIS_Y, L.ROTOR_AXIS_Z), smooth=True)
    ob["reflector"] = name
    rig.parts["ENIGMA_reflector"] = ob
    U.text("ENIGMA_reflector_label", c, f"UKW {name}", 0.006, m["white"], (0, 0, L.ROTOR_R - 0.0035),
           parent=ob)
    wiring = REFLECTORS[name]
    cu = bpy.data.curves.new("ENIGMA_reflector_wires", "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = 0.00035
    w = L.ROTOR_W * 0.4
    for a in range(26):
        b = L.ALPHA.index(wiring[a])
        if b < a:
            continue
        aa, ab = a * L.STEP, b * L.STEP
        d = (ab - aa + math.pi) % (2 * math.pi) - math.pi
        am = aa + d / 2
        U.add_spline(cu, [(w, -L.CONTACT_R * math.sin(aa), L.CONTACT_R * math.cos(aa)),
                          (-w / 2, -L.CONTACT_R * 0.5 * math.sin(am), L.CONTACT_R * 0.5 * math.cos(am)),
                          (w, -L.CONTACT_R * math.sin(ab), L.CONTACT_R * math.cos(ab))])
    cu.materials.append(m["copper"])
    wires = bpy.data.objects.new("ENIGMA_reflector_wires", cu)
    rig.cols["wiring"].objects.link(wires)
    wires.parent = ob
    wires.hide_render = True
    rig.parts["ENIGMA_reflector_wires"] = wires
    for k in range(26):
        a = k * L.STEP
        U.mesh_object(f"ENIGMA_reflector_contact_{k:02d}", c, U.bm_cylinder(0.0017, 0.0008, 12, axis="X"),
                      m["brass"], ob, (L.ROTOR_W * 0.4 + 0.0004, -L.CONTACT_R * math.sin(a), L.CONTACT_R * math.cos(a)))


def _entry_wheel(rig: Rig):
    c, m = rig.cols["rotor_stack"], rig.mats
    ob = U.mesh_object("ENIGMA_entry_wheel", c, U.bm_cylinder(L.ROTOR_R - 0.006, L.ROTOR_W * 0.8, 64, axis="X"),
                       m["bakelite"], rig.root, (L.AXIS_X["entry"], L.ROTOR_AXIS_Y, L.ROTOR_AXIS_Z), smooth=True)
    rig.parts["ENIGMA_entry_wheel"] = ob
    for k in range(26):
        a = k * L.STEP
        U.mesh_object(f"ENIGMA_entry_contact_{k:02d}", c, U.bm_cylinder(0.0017, 0.0008, 12, axis="X"),
                      m["brass"], ob, (-L.ROTOR_W * 0.4 - 0.0004, -L.CONTACT_R * math.sin(a), L.CONTACT_R * math.cos(a)))


# ------------------------------------------------------------------ stepping mechanism
def _stepping(rig: Rig):
    """Three pawls under the rotors (in front of the stack), one per rotor, pivoting
    on a common shaft. Each is keyed by the pawl number used in StepEvent."""
    c, m = rig.cols["stepping"], rig.mats
    y = L.ROTOR_AXIS_Y - L.ROTOR_R + 0.006
    z = L.ROTOR_AXIS_Z - L.ROTOR_R + 0.004
    rig.parts["ENIGMA_pawl_shaft"] = U.mesh_object(
        "ENIGMA_pawl_shaft", c, U.bm_cylinder(0.0025, 0.12, 20, axis="X"), m["steel"], rig.root,
        (0.0, y - 0.01, z - 0.012), smooth=True)
    for pawl, slot in ((1, "right"), (2, "middle"), (3, "left")):
        pivot = U.empty(f"ENIGMA_pawl_{pawl}_pivot", c, (L.AXIS_X[slot] + L.ROTOR_W / 2 - 0.002, y - 0.01, z - 0.012),
                        rig.root, size=0.01)
        pivot.rotation_mode = "XYZ"
        U.mesh_object(f"ENIGMA_pawl_{pawl}", c, U.bm_box(0.003, 0.004, 0.022, bevel=0.0004), m["steel"], pivot,
                      (0, 0.004, 0.011))
        U.mesh_object(f"ENIGMA_pawl_{pawl}_tip", c, U.bm_box(0.003, 0.006, 0.003), m["steel"], pivot,
                      (0, 0.007, 0.022))
        rig.pawls[pawl] = pivot
    lever = U.empty("ENIGMA_stepping_lever_pivot", c, (0.09, -0.02, 0.06), rig.root, size=0.01)
    lever.rotation_mode = "XYZ"
    U.mesh_object("ENIGMA_stepping_lever", c, U.bm_box(0.004, 0.12, 0.004), m["steel"], lever, (0, 0.05, 0))
    rig.parts["ENIGMA_stepping_lever"] = lever
