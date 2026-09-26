# C. Scene-by-scene breakdown

Acts I–II are fully scripted in `story/acts/act01.yaml` and `act02.yaml` (narration, visuals, SFX, claim tags) and implemented. The rest are specified here at production-planning depth; each becomes a YAML scene with beats when its act is built.

| Scene | Purpose (what the viewer learns) | Visual | Tool | Sim data | Accuracy notes |
|---|---|---|---|---|---|
| s0101 | Same key gives different letters | macro key L, cut to lamps, 4 presses | Blender | `s0101_keys` (LLLL on hero_opening → YHXG) | illustrative setting, no plugs yet |
| s0102 | This is a real, simple machine | orbit, rack focus, title, lid opens | Blender + Remotion titles | windows = AFT (state after s0101) | "thousands" (HIS-SCALE) |
| s0201 | Substitution = a rule on letters | two alphabets, shift 3, HELLO→KHOOR | Manim | — | Caesar attributed (HIS-CAESAR) |
| s0202 | A fixed rule leaks patterns | repeated letters, frequency bars | Manim | rotor I wiring used as a fixed substitution | chart labelled illustrative |
| s0203 | Moving the rule hides patterns | wheel with 26 chords turning; H→Q,U,X,K | Manim | enigma_core Rotor I, ring A | asserted in code and tests |
| s0301 | Name the parts | lid open, parts labelled in turn | Blender | hero state | layout per accuracy checklist |
| s0302 | A key press closes a circuit | battery→key→…→lamp simplified path | Blender | one press | ETW is identity on Enigma I |
| s0401 | A rotor is 26 wires in a wheel | exploded rotor: ring, core, contacts | Blender (Cycles hero) | rotor I | — |
| s0402 | Each wire maps a letter | wires reveal one by one A→E… | Blender | wiring table | rotor I wiring from CRYPTOMUSEUM |
| s0403 | Turning changes the mapping | same entry contact, rotor steps | Blender + Manim | Rotor.forward per position | — |
| s0404 | The word "permutation" | table of 26 arrows | Manim | — | term introduced only after physical |
| s0501–s0503 | Full path through 3 rotors and reflector | camera follows pulse, slow motion | Blender | `show_signal: true` press | stepping happens before current |
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
