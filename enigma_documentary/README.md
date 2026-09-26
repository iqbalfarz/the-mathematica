# The Insane Real Engineering of the Nazi Enigma Machine

A first-principles documentary pipeline where **one tested Enigma simulator drives every frame**.
Blender shows the physical machine, Manim the mathematics, and Remotion assembles the film with
Kokoro narration. Everything renders on your own computer: see **[LOCAL_SETUP.md](LOCAL_SETUP.md)**.

```bash
pip install -r requirements.txt && (cd remotion && npm install)
python run.py doctor
python run.py all --profile draft        # then: estimate / all --profile final
```

## What's built

| | Status |
|---|---|
| Design package A–J (`design/`) | complete: thesis, 23-min structure, all scenes planned, first 5 in full detail |
| Enigma I simulator (`src/enigma_core/`) | complete, 50+ tests incl. published vectors and the 1941 Barbarossa message |
| Research ledger (`research/`) | claims for Acts I–II plus the numbers and history used later |
| Script (`story/acts/`) | Acts I–VI (scenes s0101–s0604) fully written |
| Blender rig (`blender/`) | procedural Enigma I, named parts, helper API, event player, tracked labels, shots s0101, s0102, s0301 (parts tour), s0302 (current traced key → lamp), s0401–s0403 (one rotor: exploded, its 26 wires, turning it), s0501–s0503 (three rotors, the reflector's 13 wires, the way back to the lamp), s0601–s0603 (pawls, ratchets and notches in slow motion: the double step) |
| Manim (`manim_scenes/`) | Act II scenes s0201–s0203, Act IV s0404 (the rotor as a permutation, 26!), Act VI s0604 (state table, 16,900) |
| Narration, SFX, music (`src/enigma_doc/`) | Kokoro per beat; synthesised mechanical SFX |
| Remotion (`remotion/`) | full-film composition, overlays for s0101–s0603 (tracked part labels, live current/wire/reflector captions, the full journey chain, the rotor window readout), slates for unrendered scenes |

Acts VI–XXIV are specified in `design/B_structure.md` and `design/C_scene_breakdown.md` and are added act by act with the same pipeline.

## How it fits together

```
story/acts/*.yaml ─► Kokoro ─► build/audio (per-beat WAVs + timing)
config/machines.yaml + shots.yaml ─► enigma_core ─► build/events/<shot>.json
                     └──► timeline (audio-first) ─► build/timeline.json ◄─ every tool reads this clock
       Blender (renders/blender)   Manim (renders/manim)   stage ─► Remotion ─► output/enigma_<profile>.mp4
```

**Truth flows one way.** Blender never decides a letter, a rotor step or a lamp: it plays the simulator's event stream. The tests fail if the script, the rig geometry, the animated rig or the Manim wheel disagree with `enigma_core`.

## Layout

```
design/        A–J design deliverables
research/      build_ledger.py → claim_ledger.csv · sources.md · accuracy_checklist.md
story/         acts/*.yaml (the script) · loop_map.yaml
config/        machines.yaml · shots.yaml · render_profiles.yaml · voice.yaml
src/enigma_core/  simulator: rotor, reflector, plugboard, stepping, machine, events, keyspace, crib, menu, cli
src/enigma_doc/   pipeline: script, timeline, narration, audio, render_manim, stage, pipeline (run.py)
blender/       enigma_model/build.py · lib/{layout,api,player,staging,materials,util}.py · shots/ · render.py
manim_scenes/  style · base (timeline-locked scenes) · components · act02
remotion/      src/{Root,Film,Scene}.tsx · overlays/
tests/         simulator, keyspace, crib/menu, layout, rig (bpy), script
```

## Tests

```bash
python run.py test          # or: PYTHONPATH=src pytest -q tests
```
`tests/test_blender_rig.py` runs only if the `bpy` module is installed (`pip install bpy==4.2.0` on Python 3.11).
