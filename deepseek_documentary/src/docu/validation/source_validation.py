"""Every quantitative statement must be traceable to the claim ledger."""
from __future__ import annotations

import csv
import re

from ..paths import RESEARCH, ROOT
from ..script import load_script

NUM_WORDS = re.compile(r"\b(\d|thousand|million|billion|trillion|percent)\b", re.I)
MODELS = {"DeepSeek-V2": "V2", "DeepSeek-V3": "V3", "DeepSeek-V4.1-Flash": "V4.1"}
# on-screen numbers that are purely pedagogical (toy examples), with the reason
ALLOW_ONSCREEN = {"0.21", "0.82", "0.05", "0.41", "0.22", "0.12", "0.08", "3.9", "5.5", "437", "57",
                  "100.6", "447316", "0.02",
                  "000",          # LaTeX digit grouping 37{,}000{,}000{,}000
                  "2609.19969"}   # arXiv identifier of the V4.1-Flash paper


def load_ledger():
    with (RESEARCH / "claim_ledger.csv").open() as f:
        return {r["claim_id"]: r for r in csv.DictReader(f)}


def check_script():
    ledger = load_ledger()
    issues, stats = [], {"beats": 0, "tagged": 0, "tags": 0}
    used = set()
    for s in load_script():
        for b in s.beats:
            stats["beats"] += 1
            tags = b.tags
            used.update(tags)
            if tags:
                stats["tagged"] += 1
                stats["tags"] += len(tags)
            for t in tags:
                if t != "MATH" and t not in ledger:
                    issues.append(f"{s.id}/{b.id}: tag {t} not in ledger")
            if NUM_WORDS.search(b.spoken) and not tags:
                issues.append(f"{s.id}/{b.id}: quantitative wording without a claim tag: {b.spoken[:80]!r}")
            models = {ledger[t]["model_version"] for t in tags if t in ledger}
            named = {MODELS[m] for m in models if m in MODELS}
            if len(named) > 1:
                missing = [m for m in named if m not in b.spoken]
                if missing:
                    issues.append(f"{s.id}/{b.id}: mixes models {sorted(named)} without naming {missing}")
    unused = sorted(set(ledger) - used)
    return issues, stats, unused


def check_onscreen():
    """Numbers with units/magnitude drawn in scene code must appear in the ledger."""
    ledger_text = (RESEARCH / "claim_ledger.csv").read_text().replace(",", "")
    issues = []
    pat = re.compile(r'"[^"\n]*?(\d[\d,\.]*\s?(?:B|T|M|K|GB|MB|%|×)?)[^"\n]*"')
    num = re.compile(r"\d[\d,]*\.?\d*")
    for path in sorted((ROOT / "src/docu/scenes").glob("act*.py")):
        for line_no, line in enumerate(path.read_text().splitlines(), 1):
            if "T(" not in line and "M(" not in line:
                continue
            for lit in re.findall(r'"([^"]*)"', line):
                for n in num.findall(lit):
                    raw = n.replace(",", "").rstrip(".")
                    if len(raw.replace(".", "")) < 3 and not re.search(re.escape(n) + r"\s?(B|T|M|K|GB|%)", lit):
                        continue
                    if raw in ALLOW_ONSCREEN or raw in ledger_text:
                        continue
                    if raw.isdigit() and 1900 < int(raw) < 2100:
                        continue
                    issues.append(f"{path.name}:{line_no}: on-screen number {n!r} not found in ledger")
    return issues
