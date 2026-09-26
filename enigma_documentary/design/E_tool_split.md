# E. Tool split and data contracts

```
story/acts/*.yaml ──► enigma_doc.narration (Kokoro) ──► build/audio/beats/*.wav + timing.json
config/machines.yaml + config/shots.yaml ──► enigma_core ──► build/events/<shot>.json
                           │
          enigma_doc.timeline (audio-first) ──► build/timeline.json  ◄── the one clock everyone reads
                 │                    │                     │
      blender/render.py      enigma_doc.render_manim    enigma_doc.stage ──► remotion/public/
   renders/blender/<p>/<scene>/  renders/manim/<p>/<scene>.mp4        │
                 └──────────────────────┴────────────► Remotion EnigmaFilm ──► output/enigma_<p>.mp4 (+ .srt)
```

| Tool | Owns | Never does |
|---|---|---|
| **enigma_core** (Python) | all cryptography: stepping, current path, lamps, keyspace, cribs, menus | rendering |
| **Blender** | the physical machine: materials, mechanisms, current in wires, macro camera | decide a letter, a rotor step or a lamp |
| **Manim** | abstraction: alphabets, wheels, permutations, counts, graphs, crib tables | physical realism |
| **Remotion** | editorial: sequencing, narration placement, SFX, music ducking, typography overlays, slates for unrendered scenes | compute content |
| **Kokoro** | narration per beat | — |

**Contracts**
- `build/events/<shot>.json` — schema in `src/enigma_core/events.py` (schema_version 1). Every press lists pawl events and hop-by-hop path in fixed-frame letters plus rotor core pins.
- `build/timeline.json` — per scene: `film_start`, `duration`, `frames`, beats with `start`/`dur`, resolved `press_times`, `sfx` cues. Blender, Manim and Remotion all use it, so a press's click sound, the key motion and the lamp are on the same frame.
- **Shot continuity** — `continues: <shot>` in `config/shots.yaml` starts a shot's rotors where another shot left them (resolved by `enigma_core.cli.resolve_shots`).
- **Rotor demos** — a shot with `rotor_demo: {rotor, ring, slot, positions, key}` adds `rotor_demo_spec` (all 26 pin→plate wires) and `rotor_demo` (per position: in contact, pin, plate, out contact) to its event stream (`enigma_core.cli.rotor_demo`). Act IV's glowing wires and exit contacts come only from these.
- **Replays** — `replay: <shot>` in `config/shots.yaml` shows the same key press again in a later scene (key still held, rotors already stepped); pins with numbers outside the scene say where the current already is (negative seconds) or hasn't reached yet (very large). Act V splits one press across s0501–s0503 this way.
- **Signal schedule** — `blender/lib/layout.signal_schedule` decides when the current reaches each part (weighted legs, optionally pinned to narration beats). Blender's glowing trace, the follow camera and the Remotion caption all use it.
- **Tracked labels** — `blender/lib/labels.py` projects 3D anchors to 2D per frame into `renders/blender/<profile>/<scene>/labels.json`; `stage` embeds them in `timeline.json`; Remotion draws the text, so labels are crisp at any resolution.
- **Consistency gates** (pytest): script letters = simulator (`test_script.py`), rig geometry = simulator (`test_layout.py`), animated rig = simulator at every press (`test_blender_rig.py`), Manim wheel asserts against `Rotor.forward` while rendering.
