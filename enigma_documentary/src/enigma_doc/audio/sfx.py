"""Synthesised mechanical sound effects and a music bed (deterministic, license-free).

The film's sound grammar (design/H_visual_design_system.md):
  key press  -> click     rotor step -> clack     pawl -> tick
  ratchet    -> clunk     relay      -> relay     room -> hum
  current    -> current (soft electrical hum, never a sci-fi beep)
Nothing sounds like sci-fi beeps: every effect is a filtered transient with a
short metallic resonance, like a real mechanism.

    python -m enigma_doc.audio.sfx     # writes build/sfx/*.wav
"""
from __future__ import annotations

import numpy as np
import soundfile as sf
from scipy.signal import butter, lfilter

from ..paths import SFX_DIR, ensure_dirs

SR = 48000


def _t(dur):
    return np.arange(int(dur * SR)) / SR


def _band(x, lo, hi):
    b, a = butter(2, [lo / (SR / 2), min(hi, SR / 2 - 100) / (SR / 2)], btype="band")
    return lfilter(b, a, x)


def _transient(dur, lo, hi, decay, seed, modes=()):
    """Filtered noise burst + a few decaying metal resonances (freq, amp, decay)."""
    rng = np.random.default_rng(seed)
    t = _t(dur)
    s = _band(rng.normal(0, 1, len(t)), lo, hi) * np.exp(-t * decay)
    for f, a, d in modes:
        s += a * np.sin(2 * np.pi * f * t) * np.exp(-t * d)
    s[: int(0.0015 * SR)] *= np.linspace(0, 1, int(0.0015 * SR))
    return s / (np.max(np.abs(s)) or 1)


def click(dur=0.18):   # key reaching the bottom of its travel
    return 0.55 * _transient(dur, 1800, 9000, 70, 1, [(3150, 0.25, 60), (5200, 0.15, 90)])


def clack(dur=0.32):   # rotor jumping one position
    a = _transient(dur, 500, 5000, 30, 2, [(820, 0.5, 25), (1930, 0.3, 40)])
    b = np.roll(_transient(dur, 900, 7000, 60, 3), int(0.028 * SR)) * 0.5
    return 0.6 * (a + b) / 1.5


def tick(dur=0.1):     # pawl dropping into a notch
    return 0.4 * _transient(dur, 3000, 12000, 120, 4, [(6100, 0.2, 110)])


def clunk(dur=0.45):   # ratchet / heavy lid
    return 0.7 * _transient(dur, 80, 1500, 14, 5, [(140, 0.9, 10), (310, 0.4, 16)])


def relay(dur=0.22):   # Bombe relay: two quick contacts
    x = _transient(dur, 1200, 8000, 80, 6, [(2400, 0.3, 70)])
    return 0.45 * (x + 0.7 * np.roll(x, int(0.035 * SR)))


def hum(dur=4.0):      # dark room + transformer hum
    t = _t(dur)
    rng = np.random.default_rng(7)
    s = 0.4 * np.sin(2 * np.pi * 50 * t) + 0.15 * np.sin(2 * np.pi * 100 * t)
    s += 0.25 * _band(rng.normal(0, 1, len(t)), 60, 400)
    env = np.minimum(1, t / 1.0) * np.minimum(1, (dur - t) / 1.5)
    return 0.25 * s * env


def current(dur=2.5):  # electricity starting to flow: soft rising hum with a faint crackle
    t = _t(dur)
    rng = np.random.default_rng(9)
    hum_ = 0.5 * np.sin(2 * np.pi * 100 * t) + 0.25 * np.sin(2 * np.pi * 200 * t) + 0.1 * np.sin(2 * np.pi * 300 * t)
    crackle = _band(rng.normal(0, 1, len(t)), 2000, 8000) * (rng.random(len(t)) < 0.002) * 3
    env = np.minimum(1, t / 0.6) * np.minimum(1, (dur - t) / 1.0)
    return 0.3 * (hum_ + crackle) * env


def whoosh(dur=1.2):
    rng = np.random.default_rng(8)
    n = int(dur * SR)
    out = np.zeros(n)
    x = rng.normal(0, 1, n)
    for k in range(24):
        a, b = k * n // 24, (k + 1) * n // 24
        fc = 250 + 2500 * np.sin(np.pi * k / 24) ** 2
        out[a:b] = _band(x[a:b], fc * 0.6, fc * 1.4)
    return 0.4 * out * np.sin(np.pi * np.linspace(0, 1, n)) ** 2


def impact(dur=2.0):
    t = _t(dur)
    f = 32 + 55 * np.exp(-t * 4)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.4)
    return 0.6 * (boom + 0.5 * clunk(dur))


def music_bed(mood: str, dur: float = 60.0) -> np.ndarray:
    """A slow, quiet drone that loops under narration. Ducked in Remotion."""
    t = _t(dur)
    roots = {"tension": [55.0, 82.41, 103.83], "minimal": [65.41, 98.0, 130.81],
             "wonder": [73.42, 110.0, 146.83], "history": [49.0, 73.42, 98.0],
             "mechanism": [61.74, 92.5, 123.47]}[mood if mood in MOODS else "minimal"]
    s = np.zeros_like(t)
    for i, f in enumerate(roots):
        lfo = 0.6 + 0.4 * np.sin(2 * np.pi * (0.03 + 0.017 * i) * t + i)
        s += lfo * (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t + 0.5))
    fade = int(3 * SR)
    s[:fade] *= np.linspace(0, 1, fade)
    s[-fade:] *= np.linspace(1, 0, fade)
    return 0.12 * s / len(roots)


SFX = {"click": click, "clack": clack, "tick": tick, "clunk": clunk, "relay": relay,
       "hum": hum, "current": current, "whoosh": whoosh, "impact": impact}
MOODS = ["tension", "minimal", "wonder", "history", "mechanism"]


def main():
    ensure_dirs()
    for name, fn in SFX.items():
        sf.write(SFX_DIR / f"{name}.wav", fn().astype(np.float32), SR, subtype="PCM_16")
    for mood in MOODS:
        sf.write(SFX_DIR / f"music_{mood}.wav", music_bed(mood).astype(np.float32), SR, subtype="PCM_16")
    print(f"[sfx] wrote {len(SFX) + len(MOODS)} files to {SFX_DIR}")


if __name__ == "__main__":
    main()
