# I. Narration philosophy and Kokoro plan

**Rhythm:** SHOW → QUESTION → OBSERVE → EXPLAIN → GENERALISE. The picture creates the question; the voice answers it a beat later. Never explain a visual before it appears.

**Sentences:** short, spoken, one idea each. Pauses are written into the script (`pause:` per beat) and become real silence in the timeline.

> "Press it… and a lamp lights up. Y." (pause) "Press the same key again. H."

**Terms:** introduced only after their physical meaning (see D). "Permutation" arrives in Act IV, after the viewer has watched wires map letters.

**Open loops:** `story/loop_map.yaml`. Each is a real question the viewer carries; each is paid off in order; no fake suspense.

**Claims:** any sentence with a number or historical fact ends with a `[[CLAIM-ID]]` tag (stripped before speech, checked by tests against `research/claim_ledger.csv`). Estimates are attributed ("the historian Harry Hinsley estimated…").

**Kokoro-82M plan.**
- Voice `am_michael` at speed 0.95 (`config/voice.yaml`; override with `KOKORO_VOICE`, `KOKORO_SPEED`). Try `bm_george` for a British documentary register.
- One WAV per beat, trimmed, normalised; cached by text + voice, so editing one line re-synthesises one line.
- Pronunciation fixes in `src/enigma_doc/narration/pronounce.py` (Rejewski, UKW, spelled-out ciphertext) affect speech only; captions keep the original spelling.
- Timing is audio-first: after `make voice`, re-run `make timeline` and every tool re-times to the real voice.
- Your own voice later: implement `narration/providers/cloned.py` (extension point, same as the DeepSeek film).
