"""Synthesised sound effects (license-free, deterministic)."""
from __future__ import annotations

import numpy as np
from scipy.signal import butter, lfilter

SR = 48000


def _env(n, a, r):
    e = np.ones(n)
    na, nr = max(1, int(a * SR)), max(1, int(r * SR))
    e[:na] = np.linspace(0, 1, na)
    e[-nr:] *= np.linspace(1, 0, nr)
    return e


def hum(dur=3.0):
    t = np.arange(int(dur * SR)) / SR
    s = 0.5 * np.sin(2 * np.pi * 55 * t) + 0.25 * np.sin(2 * np.pi * 110 * t) + 0.1 * np.sin(2 * np.pi * 165 * t)
    s *= 0.85 + 0.15 * np.sin(2 * np.pi * 3 * t)
    return 0.35 * s * _env(len(t), 0.8, 1.2)


def pulse(dur=0.7):
    t = np.arange(int(dur * SR)) / SR
    f = 70 + 50 * np.exp(-t * 25)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)
    return 0.5 * s * _env(len(t), 0.003, 0.1)


def impact(dur=2.2):
    rng = np.random.default_rng(1)
    t = np.arange(int(dur * SR)) / SR
    f = 35 + 60 * np.exp(-t * 4)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.2)
    b, a = butter(2, 900 / (SR / 2))
    noise = lfilter(b, a, rng.normal(0, 1, len(t))) * np.exp(-t * 10) * 0.6
    return 0.6 * (boom + noise) * _env(len(t), 0.002, 0.4)


def whoosh(dur=1.3):
    rng = np.random.default_rng(2)
    n = int(dur * SR)
    x = rng.normal(0, 1, n)
    out = np.zeros(n)
    chunks = 26
    for k in range(chunks):
        a, b_ = k * n // chunks, (k + 1) * n // chunks
        fc = 300 + 3000 * np.sin(np.pi * k / chunks) ** 2
        b, a2 = butter(2, [max(50, fc * 0.6) / (SR / 2), min(fc * 1.4, SR / 2 - 100) / (SR / 2)], btype="band")
        out[a:b_] = lfilter(b, a2, x[a:b_])
    env = np.sin(np.pi * np.linspace(0, 1, n)) ** 2
    return 0.45 * out * env


SFX = {"hum": hum, "pulse": pulse, "impact": impact, "whoosh": whoosh}
