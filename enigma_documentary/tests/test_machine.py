import random

from enigma_core import EnigmaMachine, MachineConfig
from enigma_core.alphabet import ALPHABET
from enigma_core.configuration import load_configs

from conftest import ROOT

CONFIGS = load_configs(ROOT / "config" / "machines.yaml")

BARBAROSSA_CT = ("EDPUD NRGYS ZRCXN UYTPO MRMBO FKTBZ REZKM LXLVE FGUEY SIOZV EQMIK UBPMM YLKLT TDEIS "
                 "MDICA GYKUA CTCDO MOHWX MUUIA UBSTS LRNBZ SZWNR FXWFY SSXJZ VIJHI DISHP RKLKA YUPAD "
                 "TXQSP INQMA TLPIF SVKDA SCTAC DPBOP VHJK")
BARBAROSSA_PT = ("AUFKLXABTEILUNGXVONXKURTINOWAXKURTINOWAXNORDWESTLXSEBEZXSEBEZXUAFFLIEGERSTRASZERIQTUNG"
                 "XDUBROWKIXDUBROWKIXOPOTSCHKAXOPOTSCHKAXUMXEINSAQTDREINULLXUHRANGETRETENXANGRIFFXINFXRGTX")


def random_config(rng):
    rotors = rng.sample(["I", "II", "III", "IV", "V"], 3)
    letters = rng.sample(ALPHABET, 20)
    plug = [letters[i] + letters[i + 1] for i in range(0, 20, 2)]
    return MachineConfig.from_dict({"rotors": rotors, "reflector": rng.choice("BC"),
                                    "rings": "".join(rng.choices(ALPHABET, k=3)),
                                    "positions": "".join(rng.choices(ALPHABET, k=3)),
                                    "plugboard": plug})


def test_textbook_vector():
    assert EnigmaMachine(CONFIGS["textbook_aaa"]).encrypt("AAAAA") == "BDZGO"


def test_barbarossa_1941_message_decrypts():
    assert EnigmaMachine(CONFIGS["barbarossa_1941"]).encrypt(BARBAROSSA_CT) == BARBAROSSA_PT


def test_same_state_same_output():
    a, b = EnigmaMachine(CONFIGS["hero_opening"]), EnigmaMachine(CONFIGS["hero_opening"])
    assert a.encrypt("HELLOWORLD") == b.encrypt("HELLOWORLD")


def test_same_key_different_state_different_output():
    out = EnigmaMachine(CONFIGS["hero_opening"]).encrypt("LLLL")
    assert len(set(out)) == 4


def test_encrypt_then_decrypt_roundtrip_random():
    rng = random.Random(1941)
    for _ in range(200):
        cfg = random_config(rng)
        text = "".join(rng.choices(ALPHABET, k=60))
        ct = EnigmaMachine(cfg).encrypt(text)
        assert EnigmaMachine(cfg).encrypt(ct) == text


def test_no_letter_ever_encrypts_to_itself():
    rng = random.Random(7)
    for _ in range(100):
        m = EnigmaMachine(random_config(rng))
        for _ in range(200):
            k = rng.choice(ALPHABET)
            assert m.press_key(k).lamp != k


def test_reciprocal_within_one_state():
    # E -> K implies K -> E for the same rotor positions.
    cfg = CONFIGS["hero_opening"]
    for k in ALPHABET:
        out = EnigmaMachine(cfg).press_key(k).lamp
        assert EnigmaMachine(cfg).press_key(out).lamp == k


def test_left_ring_is_equivalent_to_left_position():
    base = {"rotors": "I II III", "rings": "AAA", "positions": "AAA"}
    shifted = {"rotors": "I II III", "rings": "BAA", "positions": "BAA"}
    text = "THEQUICKBROWNFOX" * 40
    assert EnigmaMachine(MachineConfig.from_dict(base)).encrypt(text) == \
        EnigmaMachine(MachineConfig.from_dict(shifted)).encrypt(text)


def test_variant_mixing_is_rejected():
    import pytest
    with pytest.raises(ValueError):
        MachineConfig.from_dict({"rotors": "I II VI"})
