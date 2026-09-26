"""Visual tokens shared with Blender and Remotion (design/H_visual_design_system.md)."""
from __future__ import annotations

import manimpango

BG = "#0E0D0B"          # warm near-black
PAPER = "#EDE6D6"       # ivory text
MUTED = "#8A857C"       # secondary text, faint wires
BRASS = "#C8A04A"       # the machine
SIGNAL = "#FF9E38"      # electricity / "this is the path"
CORRECT = "#4CD97B"
REJECT = "#F2403A"
UNKNOWN = "#F5B942"
STEEL = "#9AA3AD"


def _first(names):
    have = set(manimpango.list_fonts())
    for n in names:
        if n in have:
            return n
    return names[-1]


SANS = _first(["IBM Plex Sans", "Inter", "Source Sans 3", "DejaVu Sans"])
MONO = _first(["IBM Plex Mono", "JetBrains Mono", "Source Code Pro", "DejaVu Sans Mono"])

# Type scale (Manim font_size at the default 8-unit-tall frame)
H1, H2, BODY, SMALL, LABEL = 56, 40, 30, 22, 18
