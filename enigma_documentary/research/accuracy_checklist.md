# Historical & technical accuracy checklist

Tick before locking each act. "Sim" = enforced by a test.

## The hero machine
- [x] Variant fixed: **Enigma I** (Heer/Luftwaffe), 3 rotors from I–V, UKW-B, ETW identity, 10 cables. (Sim: `MachineConfig` rejects naval rotors.)
- [x] Stepping happens **before** the current flows. (Sim)
- [x] Double step shown correctly, never as an odometer. (Sim)
- [x] Notch letter is on the alphabet ring, so it follows the window letter, not the ring setting. (Sim)
- [x] Left ring setting has no independent effect; say "ring settings" without claiming 26³. (Sim)
- [x] Reflector ⇒ reciprocal and no self-encipherment. (Sim)
- [ ] Physical proportions of the Blender model checked against museum photos (lampboard above keyboard, plugboard on the front panel, rotors behind the lampboard lid, rotor stack left→right = UKW, L, M, R, ETW).

## Numbers
- [x] Every on-screen number is in `claim_ledger.csv` and computed by `enigma_core.keyspace`.
- [x] Commercial (6 orders, 105,456) vs Enigma I (60 orders, 10 cables) never mixed.
- [ ] Naval M4 figures only as a labelled aside.

## History
- [x] Rejewski had help from Schmidt's documents (via French intelligence). Say so.
- [x] Polish bomba ≠ British Bombe. Different machines, different methods.
- [x] Bombe = Turing's design + Welchman's diagonal board; built by BTM (Harold "Doc" Keen). Don't credit Turing alone.
- [x] "Shortened the war by two years" = Hinsley's estimate; attribute and mention it is debated.
- [ ] Re-read Wikipedia pages listed in sources.md (blocked in build env) before final lock.
- [ ] Cillies and Herivel tip: confirm dates (Herivel tip: 1940) before writing Act XI.
