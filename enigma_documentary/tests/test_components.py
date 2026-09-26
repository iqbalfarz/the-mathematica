import pytest

from enigma_core.alphabet import N
from enigma_core.plugboard import Plugboard
from enigma_core.reflector import Reflector
from enigma_core.rotor import Rotor
from enigma_core.wiring import REFLECTORS, ROTORS


@pytest.mark.parametrize("name", list(ROTORS))
def test_rotor_backward_inverts_forward_at_every_setting(name):
    for ring in range(0, N, 5):
        for pos in range(N):
            r = Rotor.from_name(name, ring=ring, position=pos)
            for c in range(N):
                out, pin, out_pin = r.forward(c)
                back, bpin, bout = r.backward(out)
                assert back == c
                assert (bpin, bout) == (out_pin, pin)


@pytest.mark.parametrize("name", list(ROTORS))
def test_rotor_wirings_are_permutations(name):
    assert sorted(ROTORS[name]["wiring"]) == sorted("ABCDEFGHIJKLMNOPQRSTUVWXYZ")


@pytest.mark.parametrize("name", list(REFLECTORS))
def test_reflector_is_reciprocal_and_has_no_fixed_points(name):
    r = Reflector.from_name(name)
    for c in range(N):
        assert r.reflect(c) != c
        assert r.reflect(r.reflect(c)) == c
    assert len(r.pairs()) == 13


def test_reflector_b_pairs_match_published_table():
    pairs = {"".join(sorted(chr(65 + a) + chr(65 + b))) for a, b in Reflector.from_name("B").pairs()}
    assert pairs == {"AY", "BR", "CU", "DH", "EQ", "FS", "GL", "IP", "JX", "KN", "MO", "TZ", "VW"}


def test_plugboard_is_reciprocal():
    p = Plugboard.parse("AQ BL")
    assert p.partner("A") == "Q" and p.partner("Q") == "A"
    assert p.partner("C") == "C"


@pytest.mark.parametrize("bad", ["AA", "AB AC", " ".join(a + b for a, b in zip("ABCDEFGHIJKLMN", "OPQRSTUVWXYZ??"))])
def test_plugboard_rejects_invalid(bad):
    with pytest.raises(ValueError):
        Plugboard.parse(bad)


def test_ring_setting_shifts_wiring_by_one():
    # Classic check: rotor I with ring B, position A maps A -> K (ring A gives E).
    assert Rotor.from_name("I", ring=0).forward(0)[0] == ord("E") - 65
    assert Rotor.from_name("I", ring=1).forward(0)[0] == ord("K") - 65


@pytest.mark.parametrize("name", ["I", "II", "III", "IV", "V"])
def test_rotor_positions_give_26_distinct_substitutions(name):
    r = Rotor.from_name(name)
    tables = set()
    for p in range(26):
        r.position = p
        tables.add(tuple(r.forward(c)[0] for c in range(26)))
    assert len(tables) == 26
