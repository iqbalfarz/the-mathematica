"""Text normalisation so the narrator says acronyms and model names naturally.
Applied only to the TTS input; captions keep the original spelling."""
import re

REPLACEMENTS = [
    (r"\bV4\.1 Flash\b", "V four point one Flash"),
    (r"\bV4 Flash\b", "V four Flash"),
    (r"\bV4\.1\b", "V four point one"),
    (r"\bV3\.2\b", "V three point two"),
    (r"\bV4\b", "V four"), (r"\bV3\b", "V three"), (r"\bV2\b", "V two"),
    (r"\bH100\b", "H one hundred"), (r"\bH800s\b", "H eight hundreds"), (r"\bH800\b", "H eight hundred"),
    (r"\bA100\b", "A one hundred"), (r"\bA800\b", "A eight hundred"), (r"\bH20\b", "H twenty"),
    (r"\bGPUs\b", "G P Us"), (r"\bGPU\b", "G P U"), (r"\bCPU\b", "C P U"),
    (r"\bFLOPs\b", "flops"), (r"\bKV\b", "K V"), (r"\bM L A\b", "M L A"),
    (r"\bMoE\b", "M o E"), (r"\bSQL\b", "sequel"), (r"\bAI\b", "A I"),
    (r"\bQ K\b", "Q K"), (r"\bdef\b", "deaf"),
    (r"(\d),(\d{3})", r"\1\2"),
]


def for_tts(text: str) -> str:
    for pat, rep in REPLACEMENTS:
        text = re.sub(pat, rep, text)
    return text
