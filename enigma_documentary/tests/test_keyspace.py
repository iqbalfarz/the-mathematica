from enigma_core import keyspace as K


def test_plugboard_counts():
    assert K.plugboard_settings(0) == 1
    assert K.plugboard_settings(1) == 325
    assert K.plugboard_settings(10) == 150_738_274_937_250
    assert K.plugboard_settings(6) == 100_391_791_500
    assert max(range(14), key=K.plugboard_settings) == 11


def test_enigma_i_total_is_the_widely_quoted_figure():
    f = K.enigma_i_factors()
    assert [x.value for x in f] == [60, 17_576, 150_738_274_937_250]
    assert K.total(f) == 158_962_555_217_826_360_000


def test_commercial_total():
    assert K.total(K.commercial_factors()) == 6 * 17_576 == 105_456


def test_rotor_wirings_is_26_factorial():
    from math import factorial
    assert K.rotor_wirings() == factorial(26) == 403_291_461_126_605_635_584_000_000
