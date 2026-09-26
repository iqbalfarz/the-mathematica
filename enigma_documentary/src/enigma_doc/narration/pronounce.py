"""TTS-only text fixes; captions keep the original spelling."""
import re

REPLACEMENTS = [
    (r"\bK H O O R\b", "K, H, O, O, R"),
    (r"\bHELLO\b", "hello"),
    (r"\bUKW\b", "U K W"),
    (r"\bRejewski\b", "Reh-yef-ski"),
    (r"\bBombe\b", "Bomb"),
    (r"(\d),(\d{3})", r"\1\2"),
]


def for_tts(text: str) -> str:
    for pat, rep in REPLACEMENTS:
        text = re.sub(pat, rep, text)
    return text
