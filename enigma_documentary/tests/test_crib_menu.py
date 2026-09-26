import pytest

from enigma_core import EnigmaMachine
from enigma_core.configuration import load_configs
from enigma_core.crib import alignments, possible_offsets
from enigma_core.menu import build_menu, find_loops

from conftest import ROOT

CONFIGS = load_configs(ROOT / "config" / "machines.yaml")


def test_true_crib_position_is_always_possible():
    cfg = CONFIGS["barbarossa_1941"]
    pt = "XXWETTERBERICHTXXNORDSEEXX"
    ct = EnigmaMachine(cfg).encrypt(pt)
    assert 2 in possible_offsets(ct, "WETTERBERICHT")


def test_clash_detected():
    a = alignments("QWETTER", "WETTER")
    assert not a[1].possible and a[1].clashes  # W over W at offset 1
    assert a[0].possible is (not a[0].clashes)


def test_menu_rejects_self_mapping():
    with pytest.raises(ValueError):
        build_menu("ABC", "XBZ", 0)


def test_loops_close_and_use_menu_edges():
    # R-W, W-E, E-O, O-S, S-R : one five-letter loop
    edges = build_menu("WEOSR", "RWEOS", 0)
    loops = find_loops(edges)
    assert len(loops) == 1
    loop = loops[0]
    letters = [l for l, _ in loop]
    assert sorted(letters) == sorted("RWEOS")
    positions = sorted(k for _, k in loop)
    assert positions == [0, 1, 2, 3, 4]
    # Consecutive letters in the loop are joined by the edge recorded between them.
    by_pos = {e.position: {e.a, e.b} for e in edges}
    for (a, k), (b, _) in zip(loop, loop[1:] + loop[:1]):
        assert by_pos[k] == {a, b}


def test_tree_menu_has_no_loops():
    assert find_loops(build_menu("BCD", "AAA", 0)) == []
