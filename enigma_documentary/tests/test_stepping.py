from enigma_core import EnigmaMachine, MachineConfig


def run(positions, n, rotors="I II III"):
    m = EnigmaMachine(MachineConfig.from_dict({"rotors": rotors, "positions": positions}))
    seq = [m.positions]
    reasons = []
    for _ in range(n):
        p = m.press_key("A")
        seq.append(m.positions)
        reasons.append([s.reason for s in p.steps])
    return seq, reasons


def test_right_rotor_steps_every_press():
    seq, _ = run("AAA", 3)
    assert seq == ["AAA", "AAB", "AAC", "AAD"]


def test_double_step_sequence():
    # Rotor III notch V, rotor II notch E: ADU ADV AEW BFX BFY
    seq, reasons = run("ADU", 4)
    assert seq == ["ADU", "ADV", "AEW", "BFX", "BFY"]
    assert reasons[1] == ["right_notch", "every_keypress"]
    assert reasons[2] == ["middle_notch", "double_step", "every_keypress"]


def test_each_rotor_turns_over_at_its_own_notch():
    for name, notch in [("I", "Q"), ("II", "E"), ("III", "V"), ("IV", "J"), ("V", "Z")]:
        after = chr((ord(notch) - 65 + 1) % 26 + 65)
        m = EnigmaMachine(MachineConfig.from_dict({"rotors": ["I" if name != "I" else "II", "III" if name != "III" else "IV", name],
                                                   "positions": "AA" + notch}))
        m.press_key("A")
        assert m.positions == "AB" + after, name


def test_notch_follows_window_letter_not_ring():
    # Ring settings move the wiring, not the turnover letter in the window.
    m = EnigmaMachine(MachineConfig.from_dict({"rotors": "I II III", "rings": "ZZZ", "positions": "AAV"}))
    m.press_key("A")
    assert m.positions == "ABW"


def test_period_of_three_rotor_machine_is_26_25_26():
    m = EnigmaMachine(MachineConfig.from_dict({"rotors": "I II III", "positions": "AAA"}))
    start = m.positions
    n = 0
    while True:
        m.press_key("A")
        n += 1
        if m.positions == start:
            break
    assert n == 26 * 25 * 26
