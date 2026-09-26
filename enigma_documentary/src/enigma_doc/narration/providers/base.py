from __future__ import annotations

import abc

import numpy as np


class VoiceProvider(abc.ABC):
    """Turns one beat of narration into mono float32 audio."""

    name = "base"
    sample_rate = 24000

    @abc.abstractmethod
    def synth(self, text: str) -> np.ndarray: ...

    def cache_key(self) -> str:
        """Anything that changes the audio for identical text (voice, speed, model)."""
        return self.name
