"""TTS-only text fixes; captions keep the original spelling."""
import re

REPLACEMENTS = [
    (r"\bK H O O R\b", "K, H, O, O, R"),
    (r"\bHELLO\b", "hello"),
    (r"\bUKW\b", "U K W"),
    (r"\bRejewski\b", "Reh-yef-ski"),
    (r"\bBombe\b", "Bomb"),
    (r"\bPin ([A-Z])\b", r"Pin \1,"),        # "Pin A goes to" -> a small pause after the letter
    (r"\bat ([A-Z])\.", r"at \1."),
    (r"(\d),(\d{3})", r"\1\2"),
]


def for_tts(text: str) -> str:
    for pat, rep in REPLACEMENTS:
        text = re.sub(pat, rep, text)
    return text
