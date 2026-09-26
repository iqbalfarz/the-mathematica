"""Historical wirings (Enigma I and related German military machines).

Each string is the letter a current entering at contact A, B, C ... leaves at,
measured with the ring setting at A and the rotor in position A.
Sources: see research/sources.md (Crypto Museum wiring tables; Hamer, Sullivan &
Weierud 1998). `notches` are the window letters at which a rotor, when stepping,
also lets the pawl to its left advance the next rotor.
"""
from __future__ import annotations

ROTORS: dict[str, dict] = {
    # Enigma I / M3 (Army, Air Force, Navy)
    "I":    {"wiring": "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "notches": "Q", "variants": ["Enigma I", "M3", "M4"]},
    "II":   {"wiring": "AJDKSIRUXBLHWTMCQGZNPYFVOE", "notches": "E", "variants": ["Enigma I", "M3", "M4"]},
    "III":  {"wiring": "BDFHJLCPRTXVZNYEIWGAKMUSQO", "notches": "V", "variants": ["Enigma I", "M3", "M4"]},
    "IV":   {"wiring": "ESOVPZJAYQUIRHXLNFTGKDCMWB", "notches": "J", "variants": ["Enigma I", "M3", "M4"]},
    "V":    {"wiring": "VZBRGITYUPSDNHLXAWMJQOFECK", "notches": "Z", "variants": ["Enigma I", "M3", "M4"]},
    # Naval only (M3/M4) -- data only; the film's hero machine never uses them.
    "VI":   {"wiring": "JPGVOUMFYQBENHZRDKASXLICTW", "notches": "ZM", "variants": ["M3", "M4"]},
    "VII":  {"wiring": "NZJHGRCXMYSWBOUFAIVLPEKQDT", "notches": "ZM", "variants": ["M3", "M4"]},
    "VIII": {"wiring": "FKQHTLXOCBJSPDZRAMEWNIUYGV", "notches": "ZM", "variants": ["M3", "M4"]},
}

REFLECTORS: dict[str, dict] = {
    "A": {"wiring": "EJMZALYXVBWFCRQUONTSPIKHGD", "variants": ["Enigma I"]},
    "B": {"wiring": "YRUHQSLDPXNGOKMIEBFZCWVJAT", "variants": ["Enigma I", "M3"]},
    "C": {"wiring": "FVPJIAOYEDRZXWGCTKUQSBNMHL", "variants": ["Enigma I", "M3"]},
}

# Entry wheel (Eintrittswalze). On all German military machines it is the identity.
ETW_MILITARY = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Physical keyboard / lampboard layout of the Enigma I (German QWERTZ order).
KEYBOARD_ROWS = ["QWERTZUIO", "ASDFGHJK", "PYXCVBNML"]
