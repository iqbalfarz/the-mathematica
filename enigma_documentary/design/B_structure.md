# B. Film structure (~23 minutes)

Durations are targets; the real length comes from the narration (audio-first timeline, `build/timeline.json`).

| # | Act | Scenes | Target | Tool mix | Loops |
|---|---|---|---|---|---|
| I | The impossible machine | s0101 cold open · s0102 open the machine | 1:00 | Blender | opens L1, L2 |
| II | Forget Enigma | s0201 Caesar · s0202 fixed rule leaks · s0203 moving alphabet | 1:30 | Manim | opens L3 |
| III | Enter Enigma | s0301 lid off, tour of parts · s0302 keyboard→lamp is a circuit | 1:00 | Blender | |
| IV | One rotor | s0401 rotor master shot (exploded) · s0402 26 contacts, 26 wires · s0403 turning changes the mapping · s0404 rotor = permutation | 1:45 | Blender + Manim | |
| V | Three rotors and a mirror | s0501 three in a row · s0502 the reflector · s0503 full current path, slow motion | 1:45 | Blender | pays L2 |
| VI | The machine moves | s0601 pawls and ratchets · s0602 turnover notch · s0603 the double step · s0604 state table | 2:00 | Blender (macro) + overlay table | pays L3 |
| VII | Same letter, different answer | s0701 back to L: split screen state vs output | 0:45 | Blender + Remotion | pays L1 |
| VIII | Reciprocity | s0801 E→K, K→E · s0802 why the same setting decrypts · no letter to itself | 1:00 | Blender + Manim | opens L4 |
| IX | The plugboard | s0901 cables, one swap · s0902 ten cables · s0903 as a graph | 1:15 | Blender → Manim | |
| X | The insane scale | s1001 rotor orders · s1002 positions, rings · s1003 plugboard, total | 1:15 | Manim | pays L4 |
| XI | The human system | s1101 key sheets · s1102 two machines, one setting · s1103 the doubled message key | 1:00 | Blender + Remotion | opens L5 |
| XII | Poland | s1201 Rejewski & Schmidt's documents · s1202 six-letter indicators as cycles · s1203 the bomba (1938) · s1204 Pyry, July 1939 | 2:00 | Manim + archival-style Remotion | |
| XIII | Bletchley Park | s1301 intercepts · s1302 operator habits (cillies, Herivel tip) | 1:00 | Remotion + Manim | |
| XIV | The crib | s1401 guessing plaintext · s1402 slide, reject, keep | 1:00 | Manim | |
| XV | Menus and loops | s1501 crib → graph · s1502 the loop closes | 1:00 | Manim | |
| XVI–XVII | Turing's inversion | s1601 eliminate, don't search · s1701 Enigmas in a chain | 1:15 | Manim + Blender | |
| XVIII | The plugboard contradiction | s1801 150 trillion · s1802 guess one pair · s1803 current spreads · s1804 contradiction ⇒ reject | 1:30 | Manim + Blender circuit | opens/pays L6 |
| XIX | The Bombe runs | s1901 power on · s1902 36 scramblers spinning | 0:45 | Blender | |
| XX | Welchman's diagonal board | s2001 R↔Y is Y↔R · s2002 propagation · s2003 fewer false stops | 1:15 | Manim + Blender | |
| XXI | A stop | s2101 D K X — a candidate, not an answer | 0:30 | Blender | opens L7 |
| XXII | Human + machine | s2201 checking stops · s2202 accepted | 0:45 | Remotion + Blender | pays L5, L7 |
| XXIII | Consequences | s2301 scale of intelligence, carefully sourced (Hinsley estimate + critics) | 1:00 | Remotion | |
| XXIV | The final reveal | s2401 simple parts + clever structure + changing state | 0:45 | Blender | |

Total ≈ 23 min. **This build contains Acts I–III (s0101–s0302) end to end**; every other scene is planned here and gets added act by act using the same pipeline.
