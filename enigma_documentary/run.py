#!/usr/bin/env python3
"""Local pipeline entry point. See `python run.py --help` and LOCAL_SETUP.md."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT / "src"), str(ROOT)]

from enigma_doc.pipeline import main  # noqa: E402

main()
