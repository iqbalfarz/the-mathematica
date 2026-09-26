# H. Visual design system

Colour communicates **state**, never decoration. Tokens are shared by Blender (`blender/lib/materials.py`), Manim (`manim_scenes/style.py`) and Remotion (`remotion/src/theme.ts`).

| Token | Hex | Meaning |
|---|---|---|
| bg | `#0E0D0B` | warm near-black room |
| paper | `#EDE6D6` | primary text, plaintext |
| muted | `#8A857C` | secondary text, idle wires |
| brass | `#C8A04A` | the machine (rotor rims, wheel) |
| signal | `#FF9E38` | electricity; the active path; ciphertext |
| correct | `#4CD97B` | consistent / accepted |
| reject | `#F2403A` | contradiction / rejected |
| unknown | `#F5B942` | hypothesis, attention |

**Materials (Blender).** Black crinkle paint (fine bump, roughness 0.6–0.85, low specular), bakelite (dark brown-black, soft coat), brass (metallic, varied roughness), steel, copper wires, ivory key faces, oak case. All procedural: no downloads, low memory.

**Type.** IBM Plex Sans / IBM Plex Mono (OFL; free from Google Fonts). Mono for anything that is letters-as-data so columns line up. Fallbacks: DejaVu. Sizes are fractions of frame height in Remotion and fixed frame units in Manim, so every profile looks identical.

**Camera grammar.**
- Physical engineering → macro lenses (65–100 mm), f/2–4, slow push-ins, cuts on mechanical sounds.
- Mathematics → locked-off, orthographic feel, generous negative space.
- History → slow documentary drift over paper textures.
- Search/Bombe → rhythmic, readable tracking; never random shake.

**Light.** Warm key (≈3500 K) from front-left, cool rim from behind, very little fill, near-black world. The lamps and the signal are the brightest things in frame.

**Sound grammar.** key → *click*; rotor → *clack*; pawl → *tick*; ratchet/lid → *clunk*; Bombe relays → *relay*; room → *hum*. No sci-fi beeps. Before every big reveal, sound drops to near silence. All synthesised (`src/enigma_doc/audio/sfx.py`), deterministic and license-free; swap in recorded foley later by dropping WAVs with the same names into `build/sfx/`.

**Motion rule.** Every animation answers: what is moving, why, and what it tells the viewer. If a move teaches nothing, it doesn't happen.
