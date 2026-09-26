# G. Blender asset architecture and render plan

## The hero asset (`blender/enigma_model/build.py`)

Built procedurally by a Python script every time a shot renders: no `.blend` to download or corrupt, deterministic, diff-able. `--save-blend` writes `build/blend/<scene>.blend` if you want to look around in the Blender UI.

```
ENIGMA (collection)            ENIGMA_root (empty)
├── ENIGMA_casing              case_base/left/right/back (oak), front_panel, deck_keyboard, deck_lamps,
│                              well_front/back, lid_hinge → lid strips with 3 windows, nameplate
├── ENIGMA_keyboard            key_<L> (stem, animated) → keycap_<L> → keyface_<L> → keyletter_<L>   × 26
├── ENIGMA_lampboard           lampwindow_<L>, lamp_<L> (glowing letter), bulb_<L>                     × 26
├── ENIGMA_plugboard           socket_<L> (+2 holes), socketlabel_<L>, cable_<AB> (from config)
├── ENIGMA_rotor_stack         rotor_{left,middle,right} (empty; rotates) → ring (+26 letters), notch,
│                              thumbwheel, ratchet, core (empty; ring offset) → body, pin_00..25,
│                              plate_00..25;  reflector (+26 contacts, label), entry_wheel (+26), axle
├── ENIGMA_stepping            pawl_{1,2,3}_pivot → pawl, tip; pawl_shaft; stepping_lever_pivot → lever
├── ENIGMA_wiring              rotor_<slot>_wires (26 real wires from the historical table), reflector_wires
└── ENIGMA_signal              signal_<press>_fwd / _ret (created per key press from the event stream)
```

Layout constants (`blender/lib/layout.py`, pure Python, unit-tested) put contact *k* of every part at angle *k·360°/26* around the rotor axis; rotors turn by −*p* steps and the core by +*r* (ring) steps. `tests/test_layout.py` proves this matches `enigma_core` exactly.

## Helper API (`blender/lib/api.py`)

`show_enigma` · `hide_casing` · `open_lid` · `explode_enigma` · `focus_rotor` · `show_wiring` · `animate_key` · `animate_lamp` · `set_rotor_positions` · `rotate_rotor` (always forward; refuses if the rig disagrees with the simulator) · `animate_pawls` · `show_signal_path` · `set_plugboard`.

`blender/lib/player.py` plays an event stream: for each press, pawls rise, the rotors named in `steps` turn, then the key contact closes, the current (optional) draws from key to lamp, and the simulator's lamp lights while the key is held.

## Tracked labels (`blender/lib/labels.py`)

Shots call `ctx.labels.track("ROTORS", anchor, t0, t1)` or `ctx.labels.caption(t, text)`. At render time the anchors are projected through the active camera for every frame into `labels.json`; Remotion draws the text, so labels are sharp at every profile and never baked into the 3D image.

## Shots

`blender/shots/<scene>.py` define cameras, cuts (timeline markers bound to cameras) and which helpers to call, using beat times from `build/timeline.json` and press times from `config/shots.yaml`. A shot never types a letter.

## Render plan for a low-spec laptop

Measured in the build container (4 CPU cores, no GPU), Cycles + OpenImageDenoise, one 1080p frame:

| Samples | s0101 (macro, DOF) | s0102 (wide/dive) | Acts I–II Blender (1,264 frames @24 fps) |
|---|---|---|---|
| 64 | 240 s | 161 s | ~67 h |
| **16 (profile `final`)** | **68 s** | **48 s** | **~20 h** |

Act III adds s0301 (parts tour, 910 frames) and s0302 (cutaway with glass rotors, 977 frames). At `final`, s0302 measured about 45 s per frame, so **Acts I–III together (about 3,150 Blender frames) come to roughly 45 hours** on a 4-core CPU: two or three nights, resumable.

Act IV adds s0401–s0403 (about 2,250 frames of a single lifted rotor, a lighter scene at roughly 40 s per frame), so **Acts I–IV come to about 70 hours** on a CPU-only laptop. Act V (s0501–s0503, about 2,170 frames of the cutaway) brings **Acts I–V to roughly 100 hours**. Act VI (s0601–s0603, about 3,230 frames of the rotor stack alone, a light scene) adds roughly 35 hours: **Acts I–VI come to about 135 hours**. Render one scene per night with `python run.py blender --profile final --scene <id>`, or use a GPU profile.

So on a CPU-only laptop, `final` (16 samples + denoiser) is the quality/time sweet spot: the denoiser removes the noise and hard-surface macro shots stay crisp (see a sample in `build/estimate/` after `make estimate`). Your machine may be faster or slower; `make estimate PROFILE=final` renders one frame per shot and prints *your* hours before you commit.

- **Resumable:** stop any time (Ctrl+C, sleep, reboot) and rerun `make blender PROFILE=final`; finished frames are kept, interrupted ones redone. Frames are only thrown away if the shot itself changed.
- **Overnight safety:** `make blender` renders shots one after another with all cores; set `BLENDER_THREADS=3` to keep the laptop usable.
- **If you have any GPU:** try `BLENDER_DEVICE=GPU make blender PROFILE=final_gpu` (OptiX/CUDA/HIP/Metal auto-detected) or `PROFILE=final_eevee` (EEVEE runs even on integrated graphics; typically seconds per frame). EEVEE was not testable in the build container (no GPU), so check one frame first with `make estimate PROFILE=final_eevee`.
- **Draft first:** `make all PROFILE=draft` gives the whole slice at 540p12 in about an hour so you can judge timing before spending a night on `final`.

As more acts are added, Blender footage grows to roughly 8–10 minutes. At `final` CPU speed that is several days of rendering, so for the full film plan either a GPU profile or rendering act by act overnight.

**Known polish items:** in the s0302 cutaway, ring letters on the far side of the glass rotors show through mirrored; a later pass can hide the back half of each ring's letters while the wiring is shown.
