"""Single source of truth for the claim ledger. Run to regenerate claim_ledger.csv.

Every sentence in story/acts/*.yaml that states a number or a historical fact
carries a [[CLAIM-ID]] tag that must exist here (tests/test_script.py checks).

Status values:
  SIMULATED            computed by enigma_core and checked by its tests (the film's own machine)
  DERIVED              our own exact arithmetic (enigma_core/keyspace.py), labelled as such on screen
  VERIFIED_SECONDARY   reputable secondary source (museum, IEEE, university history pages)
  ESTIMATE             a historian's judgement; must be attributed on screen, never stated as fact
"""
import csv
import pathlib

COLS = ["claim_id", "claim", "source", "source_type", "date", "variant", "confidence", "status",
        "allowed_wording", "forbidden_overstatement"]

R = [
# ---------------- the machine itself (simulated) ----------------
("SIM-SAMEKEY", "On the hero_opening setting, pressing L four times lights four different lamps.",
 "enigma_core (tests/test_machine.py)", "simulation", "n/a", "Enigma I", "high", "SIMULATED",
 "Press the same key four times, get four different letters.", "Enigma never repeats an output letter."),
("SIM-NOSELF", "Enigma I can never encrypt a letter to itself, because the reflector wires no contact to itself.",
 "enigma_core (test_no_letter_ever_encrypts_to_itself); CRYPTOMUSEUM", "simulation+secondary", "n/a", "Enigma I", "high", "SIMULATED",
 "No letter can ever become itself.", ""),
("SIM-RECIP", "In the same machine state, if E encrypts to K then K encrypts to E; the same setting decrypts.",
 "enigma_core (test_reciprocal_within_one_state)", "simulation", "n/a", "Enigma I", "high", "SIMULATED",
 "Same setting, type the ciphertext, the plaintext lights up.", ""),
("SIM-DOUBLESTEP", "Middle rotor double-steps: ADU -> ADV -> AEW -> BFX with rotors I-II-III.",
 "enigma_core (test_double_step_sequence); HAMER_1997", "simulation+secondary", "n/a", "Enigma I", "high", "SIMULATED",
 "The middle rotor sometimes moves twice in a row.", "The rotors behave exactly like a car odometer."),
("SIM-PERIOD", "A 3-rotor Enigma I returns to its start after 26 x 25 x 26 = 16,900 key presses (because of the double step).",
 "enigma_core (test_period_of_three_rotor_machine_is_26_25_26)", "simulation", "n/a", "Enigma I", "high", "SIMULATED",
 "It takes 16,900 key presses before the rotors come back to where they started.", "17,576 key presses before it repeats."),
("MACH-ROTORS", "Enigma I: three rotors chosen from five (I-V), rotors IV and V added on 15 December 1938.",
 "CODESANDCIPHERS; WIKI_CRYPTANALYSIS", "secondary", "1938-12-15", "Enigma I", "high", "VERIFIED_SECONDARY",
 "From December 1938, operators chose three rotors out of a box of five.", "Enigma always had five rotors."),
("MACH-CABLES", "By January 1939 the German Army used ten plugboard cables (six letters left unplugged); earlier, fewer cables (typically six).",
 "CODESANDCIPHERS; WIKI_CRYPTANALYSIS", "secondary", "1939-01", "Enigma I", "high", "VERIFIED_SECONDARY",
 "By 1939, ten cables: twenty letters swapped in pairs.", "Every letter was plugged."),
("MACH-NOTCHES", "Turnover letters: I at Q, II at E, III at V, IV at J, V at Z.",
 "CRYPTOMUSEUM; enigma_core", "secondary+simulation", "n/a", "Enigma I", "high", "SIMULATED", "", ""),
# ---------------- keyspace (derived) ----------------
("KEY-COMM-ORDER", "Three fixed rotors can be arranged in 3x2x1 = 6 orders.", "enigma_core.keyspace", "arithmetic", "n/a", "commercial / pre-1938 military", "high", "DERIVED", "", ""),
("KEY-POS", "26 x 26 x 26 = 17,576 rotor starting positions.", "enigma_core.keyspace", "arithmetic", "n/a", "3-rotor machines", "high", "DERIVED", "", ""),
("KEY-105456", "6 x 17,576 = 105,456 rotor orders x positions, the number Rejewski's cyclometer catalogued.",
 "enigma_core.keyspace; WIKI_CYCLOMETER", "arithmetic+secondary", "1934-", "3 rotors, 6 orders", "high", "DERIVED", "", ""),
("KEY-ORDER", "Choosing and ordering 3 of 5 rotors: 5x4x3 = 60 orders.", "enigma_core.keyspace", "arithmetic", "n/a", "Enigma I from Dec 1938", "high", "DERIVED", "", ""),
("KEY-RINGS", "Ring settings: 26^3 nominal, but only the middle and right rings change the machine's behaviour (26^2 = 676 effective).",
 "enigma_core (test_left_ring_is_equivalent_to_left_position)", "arithmetic+simulation", "n/a", "Enigma I", "high", "DERIVED",
 "Ring settings add hundreds more possibilities.", "Ring settings multiply the keyspace by 17,576."),
("KEY-PLUG", "Ten cables on 26 letters: 26!/(6!·10!·2^10) = 150,738,274,937,250 plugboard settings.",
 "enigma_core.keyspace", "arithmetic", "n/a", "Enigma I, 10 cables", "high", "DERIVED",
 "About 150 trillion ways to plug ten cables.", ""),
("KEY-TOTAL", "60 x 17,576 x 150,738,274,937,250 = 158,962,555,217,826,360,000 (rings ignored).",
 "enigma_core.keyspace", "arithmetic", "n/a", "Enigma I, 5 rotors, 10 cables", "high", "DERIVED",
 "About 159 quintillion settings — not counting the rings.", "Stated without naming the variant; mixed with naval figures."),
# ---------------- history ----------------
("HIS-REJEWSKI", "Marian Rejewski broke the military Enigma in December 1932 using permutation theory, helped by documents obtained by French intelligence from Hans-Thilo Schmidt.",
 "MACTUTOR_REJEWSKI; IEEE_MILESTONE", "secondary", "1932-12", "Enigma I", "high", "VERIFIED_SECONDARY",
 "Rejewski used the mathematics of permutations, plus documents French intelligence had bought from a German spy.", "Rejewski broke Enigma by pure maths alone."),
("HIS-DOUBLEKEY", "Operators enciphered the 3-letter message key twice at the start of each message; the Army/Air Force stopped the doubling in May 1940.",
 "WIKI_CRYPTANALYSIS; CODESANDCIPHERS", "secondary", "1932-1940", "Enigma I", "high", "VERIFIED_SECONDARY", "", ""),
("HIS-BOMBA", "The Polish bomba (ready mid-November 1938) was an electrically powered aggregate of six Enigmas; six were built.",
 "WIKI_BOMBA; IEEE_MILESTONE", "secondary", "1938-11", "Enigma I", "high", "VERIFIED_SECONDARY",
 "The Polish 'bomba' — six Enigmas wired together.", "The Polish bomba was the same machine as the British Bombe."),
("HIS-PYRY", "On 26-27 July 1939 at Pyry the Poles shared their methods and reconstructed Enigmas with French and British intelligence.",
 "IEEE_MILESTONE", "secondary", "1939-07-26", "n/a", "high", "VERIFIED_SECONDARY", "", ""),
("HIS-BOMBE", "The British Bombe (Turing, 1939; Welchman's diagonal board 1940) had 36 Enigma equivalents (scramblers) in three banks of 12.",
 "TNMOC_BOMBE; WIKI_BOMBE", "secondary", "1939-1940", "3-rotor Enigma", "high", "VERIFIED_SECONDARY",
 "Thirty-six Enigmas, spinning together.", "Turing invented the bombe from nothing."),
("HIS-VICTORY", "First Bombe 'Victory' began work 14 March 1940; 'Agnus' with the diagonal board installed 8 August 1940.",
 "TNMOC_BOMBE; BOMBE_ORG", "secondary", "1940", "n/a", "high", "VERIFIED_SECONDARY", "", ""),
("HIS-HINSLEY", "Official historian Harry Hinsley estimated Ultra shortened the war by about two years (possibly more); others argue for much less.",
 "HISTORYHUB; WIKI_HINSLEY", "secondary", "1993", "n/a", "medium", "ESTIMATE",
 "The historian Harry Hinsley estimated it shortened the war by around two years.", "Enigma codebreaking won the war / shortened it by exactly two years."),
("HIS-SCALE", "German armed forces used Enigma machines in the thousands (estimates of total production run to tens of thousands).",
 "CRYPTOMUSEUM", "secondary", "1926-1945", "all", "medium", "VERIFIED_SECONDARY",
 "Thousands of them.", "A precise production number."),
("HIS-CAESAR", "Suetonius reports Julius Caesar used a shift of three letters.",
 "SUETONIUS (Life of Julius Caesar, 56)", "ancient secondary", "c. 121 AD", "n/a", "medium", "VERIFIED_SECONDARY",
 "Julius Caesar is said to have used exactly this.", "Caesar invented cryptography."),
("MACH-BATTERY", "Enigma I machines were powered by a 4.5 V battery (a common flat 'lantern'/torch battery type).",
 "CHIFFRIERMASCHINE_C0009", "museum collection record", "1930s-1945", "Enigma I", "high", "VERIFIED_SECONDARY",
 "A small battery, four and a half volts.", "A specific battery brand or capacity."),
("MACH-PATH", "Current path: key, plugboard, entry wheel, rotors right-to-left, reflector, rotors left-to-right, entry wheel, plugboard, lamp.",
 "CHIFFRIERMASCHINE_C0009; enigma_core (test_path_is_a_continuous_chain_ending_at_the_lamp)", "secondary+simulation", "n/a",
 "Enigma I", "high", "SIMULATED", "Through the plugboard, the entry wheel and the rotors to the reflector, and back.", ""),
("MACH-ETW", "On military Enigmas the entry wheel is wired straight through (A to A).",
 "CRYPTOMUSEUM", "secondary", "n/a", "Enigma I", "high", "VERIFIED_SECONDARY",
 "The entry wheel just passes the current on.", "The entry wheel scrambles letters (true only of commercial machines)."),
("MACH-ROTOR-PARTS", "An Enigma rotor has 26 spring-loaded pin contacts on one face, 26 flat plate contacts on the other, one wire joining each pin to a plate, an alphabet ring with a turnover notch, and a ratchet wheel.",
 "CODESANDCIPHERS; CIPHERMACHINES_TECH", "secondary", "n/a", "Enigma I", "high", "VERIFIED_SECONDARY",
 "Twenty-six spring-loaded pins on one face, twenty-six flat plates on the other.", ""),
("SIM-ROTOR26", "One rotor gives a different substitution at each of its 26 positions (tested for rotors I-V).",
 "enigma_core (test_rotor_positions_give_26_distinct_substitutions)", "simulation", "n/a", "Enigma I", "high", "SIMULATED",
 "Twenty-six positions, twenty-six different substitutions.", ""),
("KEY-WIRINGS", "A rotor wiring is a permutation of 26 letters: 26! = 403,291,461,126,605,635,584,000,000 possible wirings.",
 "enigma_core.keyspace.rotor_wirings", "arithmetic", "n/a", "any 26-contact rotor", "high", "DERIVED",
 "About four hundred septillion possible wirings.", "The Germans chose from 26! wirings every day (they used a handful of fixed rotors)."),
("MACH-REFLECTOR", "The reflector (Umkehrwalze) has contacts on one side only; 13 wires join its 26 contacts in pairs, and no contact is wired to itself. UKW-B pairs: AY BR CU DH EQ FS GL IP JX KN MO TZ VW.",
 "CRYPTOMUSEUM; enigma_core (test_reflector_b_pairs_match_published_table)", "secondary+simulation", "n/a", "Enigma I (UKW-B)", "high", "VERIFIED_SECONDARY",
 "Thirteen wires join its twenty-six contacts in pairs.", "The reflector turns like a rotor (it does not on Enigma I)."),
("MACH-PAWLS", "Stepping: one pawl per rotor, all moved by every key press. Each pawl lies half over the notched index ring of the rotor to its right and half over the 26 ratchet teeth of the rotor to its left; the ring holds it clear of the teeth except at the notch. The rightmost pawl has no ring beside it, so it steps the right rotor on every press.",
 "WIKI_ENIGMA (via search excerpt); CIPHERMACHINES_TECH; HAMER_1997; enigma_core.stepping", "secondary", "n/a", "Enigma I", "high", "VERIFIED_SECONDARY",
 "Each pawl sits half on the notched ring of one rotor and half over the teeth of the next.", "Gears inside the machine turn the rotors like clockwork."),
("MACH-STEP-FIRST", "The rotors step as the key goes down, before the key's contact closes and current flows.",
 "WIKI_ENIGMA (via search excerpt); enigma_core.stepping docstring; test_blender_rig", "secondary+simulation", "n/a", "Enigma I", "high", "SIMULATED",
 "The rotors move first; only then does the current flow.", ""),
("MACH-THUMBWHEEL", "Each rotor's serrated finger wheel and its ratchet are on the pin (right) side; the notched index ring and the flat plates are on the left.",
 "WIKI_ROTOR_DETAILS exploded-view caption (via search excerpt); CIPHERMACHINES_TECH", "secondary", "n/a", "Enigma I", "medium", "VERIFIED_SECONDARY",
 "", ""),
("LANG-E", "E is the most frequent letter in German text.", "standard letter-frequency tables", "secondary", "n/a", "n/a", "high", "VERIFIED_SECONDARY", "", ""),
]

out = pathlib.Path(__file__).with_name("claim_ledger.csv")
with out.open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(COLS)
    for r in R:
        assert len(r) == len(COLS), r[0]
        w.writerow(r)
print(f"wrote {len(R)} claims -> {out}")
