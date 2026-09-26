# C. Scene-by-scene breakdown

Acts I–V are fully scripted in `story/acts/act01.yaml`–`act05.yaml` (narration, visuals, SFX, claim tags) and implemented. The rest are specified here at production-planning depth; each becomes a YAML scene with beats when its act is built.

| Scene | Purpose (what the viewer learns) | Visual | Tool | Sim data | Accuracy notes |
|---|---|---|---|---|---|
| s0101 | Same key gives different letters | macro key L, cut to lamps, 4 presses | Blender | `s0101_keys` (LLLL on hero_opening → YHXG) | illustrative setting, no plugs yet |
| s0102 | This is a real, simple machine | orbit, rack focus, title, lid opens | Blender + Remotion titles | windows = AFT (state after s0101) | "thousands" (HIS-SCALE) |
| s0201 | Substitution = a rule on letters | two alphabets, shift 3, HELLO→KHOOR | Manim | — | Caesar attributed (HIS-CAESAR) |
| s0202 | A fixed rule leaks patterns | repeated letters, frequency bars | Manim | rotor I wiring used as a fixed substitution | chart labelled illustrative |
| s0203 | Moving the rule hides patterns | wheel with 26 chords turning; H→Q,U,X,K | Manim | enigma_core Rotor I, ring A | asserted in code and tests |
| s0301 ✅ | Name the parts | lid open, camera tour, labels tracked onto the 3D parts (projected in Blender, drawn by Remotion) | Blender + Remotion | `s0301_tour` continues s0101 (AFT) | MACH-ROTORS |
| s0302 ✅ | A key press closes a circuit | cutaway, glass rotors, current traced key→rotors→reflector→lamp; camera follows the current; caption names each part and letter | Blender + Remotion | `s0302_circuit`: A at AFT → N (A→Q→T→P, reflector P→I, I→V→V→N) | MACH-BATTERY (4.5 V), MACH-PATH, MACH-ETW |
| s0401 ✅ | A rotor is a wheel with 26 pins, 26 plates, a lettered ring, a notch, a ratchet | left rotor (rotor I) lifts out, explodes along its axle, tracked labels | Blender + Remotion | `s0401_rotor` (continues s0302) | MACH-ROTOR-PARTS |
| s0402 ✅ | Each wire maps a letter | glass core, per-wire glow A→E, B→K, C→M, then all 26 | Blender + caption | `rotor_demo_spec.wires` | rotor I wiring from CRYPTOMUSEUM |
| s0403 ✅ | Turning changes the mapping | fixed contact A; rotor steps A→B→C→D; outputs E, J, K, C (the B→K wire exits at J) | Blender + caption | `rotor_demo` A..D, key A | SIM-ROTOR26 |
| s0404 ✅ | The word "permutation"; 26! wirings | two-row table, each letter once, position B table, 26! | Manim | Rotor.forward asserted | KEY-WIRINGS (derived) |
| s0501 ✅ | Three rotors in a chain | rotor I returns (showing D, turned back to A); press W; current right→left W→B→M→O, stops at the reflector | Blender + caption | `s0501_three` (AFU→AFV) | MACH-PATH |
| s0502 ✅ | The reflector pairs contacts; never with itself | glass reflector, 13 wires; AY BR CU; current crosses O↔M; all 13 again | Blender + caption | same press (`replay`), `reflector_pairs` | MACH-REFLECTOR; opens L8 |
| s0503 ✅ | The way back, to one lamp | return M→C→G→F, entry wheel, plugboard, lamp F; chain W→B→M→O⟲M→C→G→F | Blender + Remotion chain | same press (`replay`) | MACH-PATH; pays L2 |
| s0601–s0604 | Pawls, ratchets, notches, double step | macro behind rotors, state table ADU→BFX | Blender + Remotion table | `double_step_demo` | SIM-DOUBLESTEP; never "odometer" |
| s0701 | Payoff of L1 | split screen: state vs lamp | Blender + Remotion | s0101 stream | — |
| s0801–s0802 | Reciprocity & no self-encipherment | E→K, K→E, reflector geometry | Blender + Manim | test_reciprocal | SIM-RECIP, SIM-NOSELF |
| s0901–s0903 | Plugboard swaps | plug cables A↔Q … | Blender → Manim graph | config with plugs | 10 cables from 1939 (MACH-CABLES) |
| s1001–s1003 | Keyspace | branching tree zoom-out | Manim | enigma_core.keyspace | variant labelled; rings caveat (KEY-RINGS) |
| s1101–s1103 | Key sheets, doubled indicator | paper sheet, two machines | Remotion + Blender | — | doubled until May 1940 (HIS-DOUBLEKEY) |
| s1201–s1204 | Rejewski, cycles, bomba, Pyry | permutation cycles as graph | Manim | cycle structure from simulator | credit Schmidt's documents; bomba ≠ Bombe |
| s1301–s1302 | Bletchley, operator habits | intercept montage, cluster plot | Remotion + Manim | — | confirm cillies/Herivel dates before scripting |
| s1401–s1402 | Crib & alignment | slide crib, red clashes | Manim | `enigma_core.crib` | SIM-NOSELF |
| s1501–s1502 | Menu loops | letter graph, loop closes | Manim | `enigma_core.menu` | — |
| s1601–s1701 | Elimination; chained Enigmas | 3 scramblers R→Y→S→R | Manim + Blender | menu + machine at offsets | — |
| s1801–s1804 | Plugboard contradiction | live wires spreading | Manim + Blender | simulated test register | — |
| s1901–s1902 | The Bombe | 36 drums in 3 banks | Blender | — | HIS-BOMBE; built by BTM |
| s2001–s2003 | Diagonal board | symmetric wiring | Manim + Blender | — | HIS-VICTORY dates |
| s2101–s2202 | Stops need checking | candidate → check on Enigma → accept | Blender + Remotion | real decrypt check | — |
| s2301 | Consequences | maps, cautious wording | Remotion | — | HIS-HINSLEY as ESTIMATE |
| s2401 | Payoff | slow orbit, one key, lamp, black | Blender | hero | — |
