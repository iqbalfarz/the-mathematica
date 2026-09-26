"""Generate narration audio for every beat and write build/audio/timing.json.

    python -m docu.narration.generate_voice            # all scenes (cached)
    python -m docu.narration.generate_voice --scene s0301 --force

Each beat is synthesised separately so animation timing can lock to it.
Cached by (provider settings + text) hash, so editing one line only
re-synthesises that line.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import time

import numpy as np
import soundfile as sf

from ..paths import AUDIO, TIMING
from ..script import load_script
from .pronounce import for_tts
from .providers import get_provider, load_voice_config

SR_OUT = 48000


def _trim(x: np.ndarray, sr: int, thresh=0.004, pad=0.04) -> np.ndarray:
    idx = np.where(np.abs(x) > thresh)[0]
    if len(idx) == 0:
        return x
    a = max(0, idx[0] - int(pad * sr))
    b = min(len(x), idx[-1] + int(pad * 2.5 * sr))
    y = x[a:b].copy()
    f = int(0.01 * sr)
    y[:f] *= np.linspace(0, 1, f)
    y[-f:] *= np.linspace(1, 0, f)
    return y


def _resample(x: np.ndarray, sr: int, to: int) -> np.ndarray:
    if sr == to:
        return x
    n = int(round(len(x) * to / sr))
    return np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x).astype(np.float32)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--scene", action="append", help="only these scene ids")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args(argv)

    cfg = load_voice_config()
    provider = get_provider()
    timing = json.loads(TIMING.read_text()) if TIMING.exists() else {"scenes": {}}
    timing["provider"] = provider.cache_key()
    timing["sample_rate"] = SR_OUT
    t0 = time.time()
    n_synth = 0
    for sc in load_script():
        if args.scene and sc.id not in args.scene:
            continue
        beats_out = []
        for b in sc.beats:
            text = for_tts(b.spoken)
            key = hashlib.sha1(f"{provider.cache_key()}|{text}".encode()).hexdigest()[:16]
            wav = AUDIO / "beats" / sc.id / f"{b.id}.wav"
            meta = wav.with_suffix(".json")
            if args.force or not (wav.exists() and meta.exists() and json.loads(meta.read_text()).get("key") == key):
                audio = provider.synth(text)
                audio = _trim(audio, provider.sample_rate)
                audio = _resample(audio, provider.sample_rate, SR_OUT)
                peak = float(np.max(np.abs(audio)) or 1.0)
                audio = (audio / peak * 0.89).astype(np.float32)   # ~-1 dBFS peak; loudness fixed in the mix
                wav.parent.mkdir(parents=True, exist_ok=True)
                sf.write(wav, audio, SR_OUT, subtype="PCM_16")
                meta.write_text(json.dumps({"key": key, "text": text}))
                n_synth += 1
            dur = sf.info(wav).duration
            beats_out.append({"id": b.id, "dur": round(dur, 4), "pause": b.pause,
                              "sfx": b.sfx, "wav": str(wav.relative_to(AUDIO))})
        timing["scenes"][sc.id] = {
            "index": sc.index, "act": sc.act, "beats": beats_out,
            "narration_total": round(sum(x["dur"] + x["pause"] for x in beats_out), 3),
        }
        print(f"[voice] {sc.id} {sc.title!r}: {timing['scenes'][sc.id]['narration_total']:.1f}s", flush=True)
        TIMING.write_text(json.dumps(timing, indent=1))
    total = sum(v["narration_total"] for v in timing["scenes"].values())
    print(f"[voice] synthesised {n_synth} beats in {time.time()-t0:.0f}s; narration total {total/60:.1f} min")


if __name__ == "__main__":
    main()
