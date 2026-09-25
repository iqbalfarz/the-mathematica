"""Project paths. Everything is relative to the project root so the same code
runs locally, in Docker, and on GitHub Actions runners."""
import os
from pathlib import Path

ROOT = Path(os.environ.get("DOCU_ROOT", Path(__file__).resolve().parents[2]))
CONFIG = ROOT / "config"
STORY = ROOT / "story"
ACTS = STORY / "acts"
RESEARCH = ROOT / "research"
ASSETS = ROOT / "assets"
BUILD = ROOT / "build"
AUDIO = BUILD / "audio"            # narration wavs + timing.json (generated)
TIMING = AUDIO / "timing.json"
TIMELINE = BUILD / "timeline"      # per-scene actual beat start times written by DocScene
SCENES_OUT = BUILD / "scenes"      # rendered scene_NNN.mp4 per quality
LOGS = BUILD / "logs"
OUTPUT = ROOT / "output"
MODELS = Path(os.environ.get("KOKORO_MODEL_DIR", ROOT / "models"))

for d in (BUILD, AUDIO, TIMELINE, SCENES_OUT, LOGS):
    d.mkdir(parents=True, exist_ok=True)
