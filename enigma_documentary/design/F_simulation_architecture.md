# F. Enigma simulation architecture (`src/enigma_core/`)

| Module | Responsibility |
|---|---|
| `alphabet.py` | letters ↔ 0..25 |
| `wiring.py` | historical wirings (rotors I–VIII, Beta/Gamma omitted, UKW A/B/C) with the variants each existed on |
| `rotor.py` | a rotor with window position and ring setting; forward/backward return **fixed-frame out contact, core pin in, core pin out** |
| `reflector.py`, `plugboard.py` | reciprocal maps, validated (no self-pairs, no reuse, ≤13 cables) |
| `stepping.py` | three pawls; returns `StepEvent(pawl, rotor, reason, from, to)`; reasons: `every_keypress`, `right_notch`, `middle_notch`, `double_step` |
| `configuration.py` | `MachineConfig` exactly as a key sheet (rotor order L→R, rings, start, plugs, reflector, variant); rejects variant mixing |
| `machine.py` | `EnigmaMachine.press_key()` → `KeyPress` (steps first, then current), `encrypt()` |
| `events.py` | `KeyPress`/`Hop`, stage list, versioned JSON stream |
| `keyspace.py` | exact integer factors with ledger ids |
| `crib.py`, `menu.py` | crib alignment/clashes; menu graph and fundamental loops |
| `cli.py` | `python -m enigma_core encrypt|events|shots|keyspace` |

**Order of events on one key press** (the order Blender animates):
1. key goes down → pawls rise → rotors that the pawls engage turn (0.03–0.10 s)
2. key contact closes (0.11 s): current flows keyboard → plugboard → entry wheel → right → middle → left → reflector → left → middle → right → entry wheel → plugboard → lamp
3. lamp stays lit while the key is held.

**Frames of reference.** Fixed contacts belong to the machine body (what wires in Blender connect). Core pins turn with the rotor. With window letter *p*, ring *r*: fixed contact *c* meets core pin *c + p − r*. Hops record both, so the animation can highlight the exact physical wire.

**Invariants tested** (`tests/`): forward/backward inverse for every rotor, position and ring; reflector & plugboard reciprocal, no fixed points; `AAAAA→BDZGO`; `ADU→ADV→AEW→BFX`; the 1941 Barbarossa message decrypts letter-for-letter; encrypt∘encrypt = identity (200 random configs); no letter ever maps to itself; period 16,900; left ring ≡ left position; keyspace numbers; crib/menu logic; path continuity.
