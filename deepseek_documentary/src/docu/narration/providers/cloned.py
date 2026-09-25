"""Optional cloned-voice provider.

Kokoro-82M has no voice-cloning ability, so cloning needs a separate backend.
This provider is a documented extension point: implement `synth` with a backend
that supports zero-shot cloning from `cloned.reference_audio` (e.g. an XTTS-style
model). Timing is recomputed from the new audio automatically, so scenes stay in
sync without code changes. The project never depends on this provider.
"""
from __future__ import annotations

from ...paths import ROOT
from .base import VoiceProvider


class ClonedProvider(VoiceProvider):
    name = "cloned"

    def __init__(self, cfg: dict):
        c = cfg.get("cloned", {})
        self.reference = ROOT / c.get("reference_audio", "assets/voice/reference.wav")
        self.backend = c.get("backend", "none")
        if self.backend == "none":
            raise RuntimeError(
                "VOICE_PROVIDER=cloned but no cloning backend is configured. "
                "Set cloned.backend in config/voice.yaml and implement it in "
                "narration/providers/cloned.py, or use VOICE_PROVIDER=kokoro.")
        if not self.reference.exists():
            raise FileNotFoundError(f"reference recording not found: {self.reference}")

    def synth(self, text: str):  # pragma: no cover - backend specific
        raise NotImplementedError(f"cloning backend {self.backend!r} not implemented yet")

    def cache_key(self) -> str:
        return f"cloned:{self.backend}:{self.reference.name}"
