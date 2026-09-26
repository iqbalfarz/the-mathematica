"""Kokoro-82M (ONNX export) — default narrator. Weights are fetched from the
kokoro-onnx GitHub release on first use (HuggingFace is not required)."""
from __future__ import annotations

import os
import urllib.request

import numpy as np

from ...paths import MODELS, ROOT
from .base import VoiceProvider


def _fetch(url: str, dest):
    if dest.exists() and dest.stat().st_size > 0:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    print(f"[kokoro] downloading {url}")
    urllib.request.urlretrieve(url, tmp)
    tmp.rename(dest)


class KokoroProvider(VoiceProvider):
    name = "kokoro"

    def __init__(self, cfg: dict):
        k = cfg["kokoro"]
        model_dir = MODELS if os.environ.get("KOKORO_MODEL_DIR") else (ROOT / k.get("model_dir", "models"))
        self.model_path = model_dir / "kokoro-v1.0.onnx"
        self.voices_path = model_dir / "voices-v1.0.bin"
        _fetch(k["model_url"], self.model_path)
        _fetch(k["voices_url"], self.voices_path)
        from kokoro_onnx import Kokoro
        self.tts = Kokoro(str(self.model_path), str(self.voices_path))
        self.voice = os.environ.get("KOKORO_VOICE", k.get("voice", "am_michael"))
        self.speed = float(os.environ.get("KOKORO_SPEED", k.get("speed", 1.0)))
        self.lang = k.get("lang", "en-us")

    def synth(self, text: str) -> np.ndarray:
        audio, sr = self.tts.create(text, voice=self.voice, speed=self.speed, lang=self.lang)
        self.sample_rate = sr
        return np.asarray(audio, dtype=np.float32)

    def cache_key(self) -> str:
        return f"kokoro-v1.0:{self.voice}:{self.speed}:{self.lang}"
