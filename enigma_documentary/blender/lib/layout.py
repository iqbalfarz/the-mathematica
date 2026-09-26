"""Physical layout of the Enigma I rig: pure Python, no bpy.

Units are metres. Axes: +X to the operator's right, +Y away from the operator,
+Z up. Dimensions follow museum Enigma I machines closely enough to read as the
real thing (case about 34 x 28 cm, rotors about 10 cm across); exact millimetres
are pedagogical, not engineering drawings.

Angles around the rotor axis (the X axis): angle 0 is straight up (the window);
positive angles turn toward the operator. Contact k of any fixed part sits at
angle k * STEP. A rotor showing window letter p with ring setting r is rotated
by -p * STEP; its wiring core is rotated by +r * STEP relative to the rotor.
This makes the geometry agree with enigma_core.rotor: fixed contact c meets core
pin c + (p - r). tests/test_layout.py checks this.
"""
from __future__ import annotations

import math

STEP = 2 * math.pi / 26
ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ROWS = ["QWERTZUIO", "ASDFGHJK", "PYXCVBNML"]

CASE = {"x": 0.34, "y": 0.28, "z": 0.12, "y0": -0.15, "wall": 0.165}   # keyboard deck at z = 0.12
KEY_PITCH = 0.031
KEY_ROWS_Y = [-0.070, -0.100, -0.130]      # QWERTZUIO row is furthest back
KEY_Z = 0.132
KEY_TRAVEL = 0.006
LAMP_ROWS_Y = [0.012, -0.012, -0.036]
LAMP_Z = 0.124
SOCKET_ROWS_Z = [0.085, 0.060, 0.035]
SOCKET_Y = CASE["y0"] - 0.001
ROTOR_AXIS_Y = 0.075
ROTOR_AXIS_Z = 0.110
ROTOR_R = 0.046              # alphabet ring radius
CONTACT_R = 0.030            # radius of the contact circle on rotor faces
ROTOR_W = 0.024
# Order along the axis, operator's left to right: reflector, left, middle, right, entry wheel.
AXIS_X = {"reflector": -0.066, "left": -0.036, "middle": -0.006, "right": 0.024, "entry": 0.054}
WINDOW_Z = ROTOR_AXIS_Z + ROTOR_R + 0.006


def row_x(i: int, n: int, offset: float = 0.0) -> float:
    return (i - (n - 1) / 2) * KEY_PITCH + offset


def key_pos(letter: str) -> tuple[float, float, float]:
    for r, row in enumerate(ROWS):
        if letter in row:
            return (row_x(row.index(letter), len(row), 0.008 * (r == 1)), KEY_ROWS_Y[r], KEY_Z)
    raise KeyError(letter)


def lamp_pos(letter: str) -> tuple[float, float, float]:
    for r, row in enumerate(ROWS):
        if letter in row:
            return (row_x(row.index(letter), len(row), 0.008 * (r == 1)), LAMP_ROWS_Y[r], LAMP_Z)
    raise KeyError(letter)


def socket_pos(letter: str) -> tuple[float, float, float]:
    """Plugboard on the front panel; same QWERTZ layout as the keyboard."""
    for r, row in enumerate(ROWS):
        if letter in row:
            return (row_x(row.index(letter), len(row), 0.008 * (r == 1)), SOCKET_Y, SOCKET_ROWS_Z[r])
    raise KeyError(letter)


def ring_point(x: float, angle: float, radius: float) -> tuple[float, float, float]:
    """World point on a circle around the rotor axis."""
    return (x, ROTOR_AXIS_Y - radius * math.sin(angle), ROTOR_AXIS_Z + radius * math.cos(angle))


def contact(part: str, letter_index: int, side: str) -> tuple[float, float, float]:
    """Fixed-frame contact `letter_index` on the left ('L') or right ('R') face of a part."""
    x = AXIS_X[part] + (ROTOR_W / 2 if side == "R" else -ROTOR_W / 2)
    return ring_point(x, letter_index * STEP, CONTACT_R)


def rotor_angle(position: int) -> float:
    return -position * STEP


def core_angle(ring: int) -> float:
    return ring * STEP


def pin_world_angle(pin: int, position: int, ring: int) -> float:
    """World angle of core pin `pin` for a rotor at window `position`, ring `ring`."""
    return pin * STEP + core_angle(ring) + rotor_angle(position)


def _idx(c: str) -> int:
    return ALPHA.index(c)


def signal_points(press: dict) -> tuple[list, list]:
    """Polyline for one key press, split into (forward, return) halves.

    `press` is one entry of an enigma_core event stream. Rotor hops use their
    fixed-frame in/out letters, so the path is drawn where the contacts are
    *after* stepping, i.e. at the moment the current flows.
    """
    hops = {h["stage"]: h for h in press["path"]}
    key = press["key"]
    fwd: list = []
    kx, ky, kz = key_pos(key)
    fwd += [(kx, ky, kz - 0.01), (kx, ky, 0.05)]
    s_in = hops["plugboard_in"]
    sx, sy, sz = socket_pos(s_in["in_letter"])
    fwd += [(sx, sy + 0.012, sz), (sx, sy, sz)]
    if s_in["out_letter"] != s_in["in_letter"]:
        ox, oy, oz = socket_pos(s_in["out_letter"])
        fwd += [(sx, sy - 0.03, sz - 0.02), (ox, oy - 0.03, oz - 0.02), (ox, oy, oz)]
        sx, sy, sz = ox, oy, oz
    e = _idx(hops["entry_in"]["out_letter"])
    fwd += [(sx, sy + 0.02, 0.03), (AXIS_X["entry"] + 0.03, ROTOR_AXIS_Y, 0.03), contact("entry", e, "R"),
            contact("entry", e, "L")]
    for part in ("right", "middle", "left"):
        h = hops[f"rotor_{part}_in"]
        a, b = _idx(h["in_letter"]), _idx(h["out_letter"])
        fwd += [contact(part, a, "R"), _mid(part, a, b), contact(part, b, "L")]
    r = hops["reflector"]
    a, b = _idx(r["in_letter"]), _idx(r["out_letter"])
    fwd += [contact("reflector", a, "R"), _mid("reflector", a, b, bulge=-0.008)]
    back: list = [_mid("reflector", a, b, bulge=-0.008), contact("reflector", b, "R")]
    for part in ("left", "middle", "right"):
        h = hops[f"rotor_{part}_out"]
        a, b = _idx(h["in_letter"]), _idx(h["out_letter"])
        back += [contact(part, a, "L"), _mid(part, b, a), contact(part, b, "R")]
    e = _idx(hops["entry_out"]["out_letter"])
    back += [contact("entry", e, "L"), contact("entry", e, "R"), (AXIS_X["entry"] + 0.035, ROTOR_AXIS_Y, 0.035)]
    p_out = hops["plugboard_out"]
    px, py, pz = socket_pos(p_out["in_letter"])
    back += [(px, py + 0.02, 0.035), (px, py, pz)]
    if p_out["out_letter"] != p_out["in_letter"]:
        qx, qy, qz = socket_pos(p_out["out_letter"])
        back += [(px, py - 0.03, pz - 0.02), (qx, qy - 0.03, qz - 0.02), (qx, qy, qz)]
        px, py, pz = qx, qy, qz
    lx, ly, lz = lamp_pos(press["lamp"])
    back += [(px, py + 0.02, pz), (lx, ly, 0.06), (lx, ly, lz - 0.004)]
    return fwd, back


def _mid(part: str, a: int, b: int, bulge: float = 0.0):
    """A point inside the part between contact angles a and b (wires cross the core)."""
    ang_a, ang_b = a * STEP, b * STEP
    d = (ang_b - ang_a + math.pi) % (2 * math.pi) - math.pi
    return ring_point(AXIS_X[part] + bulge, ang_a + d / 2, CONTACT_R * 0.55)
