"""Procedural, license-free score. Each act has a mood; the music is quiet by
design (it is ducked further under narration in the mix).

All synthesis is deterministic (seeded), so re-renders sound identical."""
from __future__ import annotations

import numpy as np
from scipy.signal import lfilter

SR = 48000


def mf(m):
    return 440.0 * 2 ** ((m - 69) / 12)


MOODS = {
    # chords as MIDI notes; secs per chord; pluck density; pulse bpm; lowpass cutoff (Hz); gain
    "tension":    dict(chords=[[38, 45, 50, 53], [38, 45, 50, 56], [36, 43, 48, 51], [38, 45, 50, 53]], secs=8,
                       pluck=0.0, pulse=0, cutoff=900, gain=0.9, drone=26),
    "curious":    dict(chords=[[48, 55, 62, 64], [45, 52, 60, 64], [41, 48, 57, 64], [43, 50, 59, 62]], secs=6,
                       pluck=0.5, pulse=0, cutoff=2200, gain=0.8, drone=36),
    "pulse":      dict(chords=[[45, 52, 57, 60], [41, 48, 57, 60], [43, 50, 55, 59], [40, 47, 55, 59]], secs=6,
                       pluck=0.25, pulse=96, cutoff=1600, gain=0.8, drone=33),
    "minimal":    dict(chords=[[40, 47, 55, 59], [36, 43, 52, 55], [38, 45, 54, 57], [40, 47, 55, 59]], secs=10,
                       pluck=0.12, pulse=0, cutoff=1200, gain=0.7, drone=28),
    "rising":     dict(chords=[[45, 52, 57, 60], [46, 53, 58, 62], [48, 55, 60, 64], [50, 57, 62, 65]], secs=5,
                       pluck=0.35, pulse=80, cutoff=1400, gain=0.85, drone=33, rise=True),
    "discovery":  dict(chords=[[41, 48, 55, 57, 64], [43, 50, 57, 59, 66], [45, 52, 57, 60, 64], [41, 48, 53, 60, 67]],
                       secs=6, pluck=0.6, pulse=0, cutoff=2600, gain=0.8, drone=29),
    "resolution": dict(chords=[[48, 55, 60, 64], [43, 50, 59, 62], [45, 52, 57, 60], [41, 48, 57, 60]], secs=5,
                       pluck=0.4, pulse=0, cutoff=2400, gain=0.9, drone=36),
}
PENTA = [0, 2, 4, 7, 9]


def _env(n, a, r):
    e = np.ones(n)
    na, nr = int(a * SR), int(r * SR)
    if na:
        e[:na] = np.linspace(0, 1, na) ** 1.5
    if nr:
        e[-nr:] *= np.linspace(1, 0, nr) ** 1.5
    return e


def _lowpass(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = lfilter([1 - a], [1, -a], x)
    return lfilter([1 - a], [1, -a], y)


def _pad(freqs, dur, rng, amp=0.08):
    n = int(dur * SR)
    t = np.arange(n) / SR
    out = np.zeros((n, 2))
    for f in freqs:
        for ch, det in ((0, 0.997), (1, 1.003)):
            ph = rng.uniform(0, 2 * np.pi)
            vib = 0.0015 * np.sin(2 * np.pi * 0.2 * t + ph)
            sig = np.sin(2 * np.pi * f * det * t * (1 + vib) + ph)
            sig += 0.3 * np.sin(2 * np.pi * 2 * f * det * t + ph)
            out[:, ch] += sig
    out *= amp / max(1, len(freqs))
    return out * _env(n, min(2.0, dur / 3), min(2.5, dur / 3))[:, None]


def _pluck(f, dur=1.6, amp=0.05):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t) + 0.12 * np.sin(6 * np.pi * f * t))
    return amp * s * np.exp(-t * 3.2) * _env(n, 0.005, 0.2)


def _kick(amp=0.12):
    n = int(0.35 * SR)
    t = np.arange(n) / SR
    f = 60 + 40 * np.exp(-t * 30)
    return amp * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)


def generate(mood: str, duration: float, seed: int = 0) -> np.ndarray:
    cfg = MOODS.get(mood, MOODS["minimal"])
    rng = np.random.default_rng(seed)
    n = int(duration * SR)
    out = np.zeros((n, 2))
    secs = cfg["secs"]
    k = 0
    t0 = 0.0
    while t0 < duration:
        chord = cfg["chords"][k % len(cfg["chords"])]
        seg = min(secs + 2.5, duration - t0 + 2.5)
        p = _pad([mf(m) for m in chord], seg, rng)
        a = int(t0 * SR)
        b = min(n, a + len(p))
        out[a:b] += p[: b - a]
        # plucks: pentatonic notes over the chord root, sparse and random
        if cfg["pluck"] > 0:
            steps = int(secs / 0.75)
            root = chord[0] + 24
            for s in range(steps):
                if rng.random() < cfg["pluck"]:
                    note = root + PENTA[rng.integers(0, 5)] + 12 * rng.integers(0, 2)
                    pl = _pluck(mf(note), amp=0.035)
                    pa = int((t0 + s * 0.75) * SR)
                    pb = min(n, pa + len(pl))
                    if pa < n:
                        pan = rng.uniform(0.3, 0.7)
                        out[pa:pb, 0] += pl[: pb - pa] * (1 - pan)
                        out[pa:pb, 1] += pl[: pb - pa] * pan
        t0 += secs
        k += 1
    # drone
    t = np.arange(n) / SR
    drone = 0.05 * np.sin(2 * np.pi * mf(cfg["drone"]) * t) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.05 * t))
    out += drone[:, None]
    if cfg.get("pulse"):
        beat = 60.0 / cfg["pulse"]
        kk = _kick(0.06)
        tt = 0.0
        while tt < duration:
            a = int(tt * SR)
            b = min(n, a + len(kk))
            out[a:b] += kk[: b - a, None]
            tt += beat * 2
    cutoff = cfg["cutoff"]
    if cfg.get("rise"):
        # open the filter over the segment
        half = n // 2
        out[:half] = np.stack([_lowpass(out[:half, c], cutoff * 0.6) for c in range(2)], 1)
        out[half:] = np.stack([_lowpass(out[half:, c], cutoff * 1.6) for c in range(2)], 1)
    else:
        out = np.stack([_lowpass(out[:, c], cutoff) for c in range(2)], 1)
    out *= cfg["gain"]
    out *= _env(n, 1.5, 2.0)[:, None]
    return out.astype(np.float32)
