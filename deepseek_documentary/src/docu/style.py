"""Visual design system. Colours are semantic: once a colour means something
(e.g. MEMORY = teal) it means that everywhere in the film."""
from manim import ManimColor

BG = ManimColor("#0B0E14")
PANEL = ManimColor("#141925")
GRID = ManimColor("#232A38")
TEXT = ManimColor("#E6E9EF")
MUTED = ManimColor("#8A93A6")
DIM = ManimColor("#3A4252")

TOKEN = ManimColor("#4DA3FF")      # tokens / inputs
PARAM = ManimColor("#F2C14E")      # weights / parameters
COMPUTE = ManimColor("#FF7A45")    # arithmetic, FLOPs
MEMORY = ManimColor("#2EC4B6")     # HBM, KV cache, storage
COMM = ManimColor("#8B7BFF")       # interconnect, bandwidth, communication
ATTN = ManimColor("#E86BFF")       # attention scores / weights
EXPERT = ManimColor("#6BD968")     # MoE experts
ROUTER = ManimColor("#F5F5F0")     # router
LOSS = ManimColor("#FF4D6D")       # loss / restriction / warnings
GRAD = ManimColor("#7CF2FF")       # gradients
QCOL = ManimColor("#FFB86B")       # query vectors
KCOL = ManimColor("#6BCBFF")       # key vectors
VCOL = ManimColor("#B6F09C")       # value vectors

FONT = "Inter"
MONO = "DejaVu Sans Mono"

# Type scale (Manim font_size). Frame is 8 units tall at every resolution,
# so these are resolution independent.
H1 = 52
H2 = 40
BODY = 30
SMALL = 24
TINY = 20          # never go below this (legibility at 720p)

SAFE = 0.45        # frame-unit margin kept clear on each edge
