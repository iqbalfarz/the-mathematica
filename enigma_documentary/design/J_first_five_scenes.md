# J. The first five scenes in full detail

Times below are from the real Kokoro narration (`build/timeline.json`, profile-independent). Scene time 0 is the first frame; each scene starts with 0.6 s lead-in.

---

## s0101 — Cold open: "Same key, different answer" · 19.2 s · Blender

**Educational objective:** create the central mystery (L1): one key, four different lamps.

| Beat | Start | Narration | Picture | Sound |
|---|---|---|---|---|
| b1 | 2.60 | "One key." | Black (2 s intentional). Key L rises out of darkness, 100 mm macro, f/2.2, slow push-in. | room hum fades up |
| b2 | 4.31 | "Press it… and a lamp lights up. Y." | Key L goes down 6 mm in 0.10 s. Cut on the click to the lampboard (85 mm): **Y** glows while the key is held. | clack (rotor, hidden) + click |
| b3 | 7.49 | "Press the same key again. H." | Back to the key; second press; cut: **H**. | clack + click |
| b4 | 10.15 | "Again. X. And again. G." | Two quicker presses: **X**, **G**. Lower-third strip builds: `L → Y  L → H  L → X  L → G`. | clack + click ×2 |
| b5 | 13.06 | "Same machine. Same finger. Same key. Four different answers." | Pull-back camera from the key into darkness; strip holds. | silence under the voice |

- **Objects:** `ENIGMA_key_L`, `ENIGMA_lamp_{Y,H,X,G}`, rotor stack (turning under the closed lid), `CAM_key_macro`, `CAM_lamp_macro`, `CAM_pullback`.
- **Exact state:** `config/machines.yaml: hero_opening` = Enigma I, rotors I-II-III, UKW-B, rings AAA, start **AFP**, no plugs. Presses LLLL → **YHXG**; positions AFP→AFQ→AFR→AFS→**AFT**; right rotor steps every press, no turnovers. File: `build/events/s0101_keys.json`.
- **Implementation:** Blender `blender/shots/s0101.py` + `player.play()`; Remotion `overlays/S0101.tsx` (strip reads letters from the event stream); SFX cues from `press_at` in `config/shots.yaml`.
- **Validation:** `test_script.py` (spoken letters = YHXG = simulator), `test_blender_rig.py` (lit lamp & rotor angles per press), Remotion strip uses stream data only.
- **Transition:** hard cut to s0102 on the last word.

## s0102 — "Open the machine" · 30.2 s · Blender + Remotion titles

**Objective:** establish the real object and the question as text (L2: what's inside?).

| Beat | Start | Narration | Picture |
|---|---|---|---|
| b1 | 0.60 | "This is an Enigma machine. The German armed forces used thousands of them…" [HIS-SCALE] | 30° orbit around the machine (50 mm, f/5.6). Windows read **A F T** — the state s0101 left. |
| b2 | 10.25 | "Twenty-six keys, twenty-six lamps, and no screen, no chip, no software." | Settle front; rack focus keyboard → lampboard. Remotion label `26 KEYS · 26 LAMPS`. |
| b3 | 16.40 | "So how can a box of wires answer the same question differently every time?" | Hold wide. Title: **HOW CAN THE SAME KEY HAVE A DIFFERENT ANSWER?** (Remotion). impact SFX. |
| b4 | 22.28 | "To understand that, we are going to take it apart. But first, let's forget Enigma for a moment." | Lid hinges open over 1.1 s (clunk), camera dives to the rotors. |

- **State:** `s0102_reveal` continues `s0101_keys` → windows AFT (read from the stream, not typed).
- **Validation:** window letters come from `positions_after` of the last s0101 press.
- **Transition:** dip to the clean dark Manim background.

## s0201 — "The oldest trick" · 19.8 s · Manim

**Objective:** substitution as a rule on letters. Two alphabets; bottom slides 3 (X Y Z wrap in real time); arrows A→D, B→E; caption "Caesar shift +3" [HIS-CAESAR]; HELLO drops through the arrows into KHOOR, each pair highlighted on the alphabets.
- **Validation:** `caesar()` computes KHOOR; no hand-typed ciphertext.

## s0202 — "Why a fixed rule leaks" · 26.9 s · Manim

**Objective:** a fixed rule preserves patterns. The two L's → two O's boxed; H→K ×3; bottom alphabet scrambles (using rotor I's wiring as a fixed substitution — a quiet foreshadowing); frequency bars of a German sentence vs its substitution have identical shapes, E→L; label *illustrative* [LANG-E].

## s0203 — "What if the alphabet moved?" · 30.2 s · Manim

**Objective:** the moving rule; name "rotor" (opens L3: why don't all three turn?).
- Wheel: 26 fixed letters, 26 chords = rotor I's real wiring. H → **Q**; chords turn one step (click) → **U**; → **X**; → **K**. Results column, then `same input + different wheel position = different output`. The wheel collapses into a rotor silhouette and two more slide in.
- **Exact state:** `enigma_core.rotor.Rotor("I")`, ring A, positions A,B,C,D with key H → QUXK. The scene *asserts* the drawn chord agrees with `Rotor.forward` while rendering; `test_script.py` checks the narration.
- **Transition:** into Act III (lid off, parts tour) — next build.

---

**Common validation for all five:** `make test` (simulator, script, rig), no Manim overruns reported by `make manim`, `make stage` shows every scene has media, and a watch-through of the draft render.
