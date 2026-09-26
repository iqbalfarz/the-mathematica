# Sources

Short keys are used in `claim_ledger.csv`. Fetches from wikipedia.org are blocked
in the build environment, so Wikipedia entries were confirmed via search excerpts
and should be re-read before final lock (see accuracy_checklist.md).

| Key | Source | Used for |
|---|---|---|
| CRYPTOMUSEUM | Crypto Museum, *Enigma wiring* — cryptomuseum.com/crypto/enigma/wiring.htm | rotor/reflector wiring, notches |
| HAMER_1997 | D. Hamer, "Enigma: Actions Involved in the 'Double Stepping' of the Middle Rotor", *Cryptologia* 21(1), 1997 | double step |
| CODESANDCIPHERS | Tony Sale, *The components of the Enigma machine* — codesandciphers.org.uk/enigma/enigma2.htm | rotors IV/V date, cable count |
| WIKI_CRYPTANALYSIS | Wikipedia, *Cryptanalysis of the Enigma* | doubled indicator, timeline |
| WIKI_CYCLOMETER | Wikipedia, *Cyclometer* | 105,456 settings catalogued |
| WIKI_BOMBA | Wikipedia, *Bomba (cryptography)* | Polish bomba |
| WIKI_BOMBE | Wikipedia, *Bombe* | Bombe design |
| IEEE_MILESTONE | ETHW, *Milestones: First Breaking of Enigma Code by the Team of Polish Cipher Bureau, 1932–1939* | Rejewski, Pyry |
| MACTUTOR_REJEWSKI | MacTutor, *Marian Rejewski* | Rejewski biography |
| TNMOC_BOMBE | The National Museum of Computing, *The Turing-Welchman Bombe* — tnmoc.org/bombe | 36 scramblers, diagonal board |
| BOMBE_ORG | bombe.org.uk, *Enter Turing and Welchman* | Victory / Agnus dates |
| HISTORYHUB | historyhub.info, *British Signals Intelligence and the Shortening of World War Two* | Hinsley estimate and critics |
| WIKI_HINSLEY | Wikipedia, *Harry Hinsley* | Hinsley quote |

## Test vectors (all pass in `tests/test_machine.py`)

1. Rotors I-II-III, UKW-B, rings AAA, start AAA: `AAAAA` → `BDZGO` (standard vector used by every Enigma simulator).
2. Double step, rotors I-II-III from ADU: ADU → ADV → AEW → BFX.
3. German Army message of 7 July 1941 (Operation Barbarossa), rotors II IV V, UKW-B, rings 02 21 12, plugs AV BS CG DL FU HZ IN KM OW RX, message key BLA — decrypts to `AUFKLXABTEILUNGXVONXKURTINOWA…` ("Aufklärung abteilung von Kurtinowa…"). Published by Frode Weierud / Crypto Museum; also in the Wikipedia *Enigma machine* article. Because this decrypts correctly letter-for-letter, it independently confirms rotors II, IV, V, reflector B, ring and plugboard logic.
