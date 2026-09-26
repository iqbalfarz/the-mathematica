"""Project paths, all relative to the project root (enigma_documentary/)."""
import os
from pathlib import Path

ROOT = Path(os.environ.get("ENIGMA_ROOT", Path(__file__).resolve().parents[2]))
CONFIG = ROOT / "config"
STORY = ROOT / "story"
ACTS = STORY / "acts"
RESEARCH = ROOT / "research"
BUILD = ROOT / "build"
AUDIO = BUILD / "audio"             # narration wavs + timing.json
TIMING = AUDIO / "timing.json"
SFX_DIR = BUILD / "sfx"
EVENTS = BUILD / "events"           # simulator event streams per shot
TIMELINE = BUILD / "timeline.json"  # the planned film timeline Remotion reads
RENDERS = ROOT / "renders"          # blender/<profile>/<shot>/####.png, manim/<profile>/<scene>.mp4
REMOTION = ROOT / "remotion"
REMOTION_MEDIA = REMOTION / "public" / "media"
OUTPUT = ROOT / "output"
MODELS = Path(os.environ.get("KOKORO_MODEL_DIR", ROOT / "models"))


def ensure_dirs():
    for d in (BUILD, AUDIO, SFX_DIR, EVENTS, RENDERS, OUTPUT):
        d.mkdir(parents=True, exist_ok=True)
