"""Checks on rendered media: format, decode errors, black frames, loudness, silence, clipping, sync."""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


def ffprobe(path: Path) -> dict:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
                       capture_output=True, text=True, check=True)
    return json.loads(r.stdout)


def _ff(args, path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), *args, "-f", "null", "-"],
                       capture_output=True, text=True)
    return r.stderr


def visual(path: Path, q: dict, black_min=1.5, allowed=()):
    """`allowed`: (start, end) windows of intentional black. A frame counts as
    empty only if 99.9% of it is near-black: the house style is sparse text on a
    dark background, so the ffmpeg default (98%) would flag ordinary frames."""
    info = ffprobe(path)
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    issues = []
    if (int(v["width"]), int(v["height"])) != (q["width"], q["height"]):
        issues.append(f"resolution {v['width']}x{v['height']} != {q['width']}x{q['height']}")
    num, den = (int(x) for x in v["r_frame_rate"].split("/"))
    if abs(num / den - q["fps"]) > 0.01:
        issues.append(f"fps {num/den} != {q['fps']}")
    if abs(int(v["width"]) / int(v["height"]) - 16 / 9) > 0.01:
        issues.append("aspect ratio is not 16:9")
    log = _ff(["-vf", f"blackdetect=d={black_min}:pix_th=0.08:pic_th=0.999", "-an"], path)
    blacks = re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", log)
    for a, b in blacks:
        a, b = float(a), float(b)
        if any(w0 - 0.5 <= a and b <= w1 + 0.5 for w0, w1 in allowed):
            continue
        issues.append(f"empty (black) segment {a:.1f}s–{b:.1f}s")
    return issues, {"codec": v["codec_name"], "width": v["width"], "height": v["height"],
                    "fps": round(num / den, 3), "duration": float(info["format"]["duration"]),
                    "pix_fmt": v.get("pix_fmt")}


def decode_errors(path: Path):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "null", "-"], capture_output=True, text=True)
    return [l for l in r.stderr.splitlines() if l.strip()][:10]


def audio(path: Path, expected: float):
    info = ffprobe(path)
    a = [s for s in info["streams"] if s["codec_type"] == "audio"]
    issues = []
    if not a:
        return ["no audio stream"], {}
    a = a[0]
    log = _ff(["-af", "ebur128=peak=true", "-vn"], path)
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", log)
    lufs = float(m[-1]) if m else None
    pk = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", log)
    peak = float(pk[-1]) if pk else None
    sil = _ff(["-af", "silencedetect=noise=-45dB:d=4", "-vn"], path)
    silences = re.findall(r"silence_start: ([\d.]+)[\s\S]*?silence_end: ([\d.]+)", sil)
    if lufs is None or not (-19 <= lufs <= -13):
        issues.append(f"integrated loudness {lufs} LUFS outside [-19, -13]")
    if peak is not None and peak > -0.5:
        issues.append(f"true peak {peak} dBFS (clipping risk)")
    for s0, s1 in silences:
        issues.append(f"silence {float(s0):.1f}s–{float(s1):.1f}s (>4 s)")
    dur = float(a.get("duration", info["format"]["duration"]))
    if abs(dur - expected) > 1.0:
        issues.append(f"audio duration {dur:.1f}s vs expected {expected:.1f}s")
    return issues, {"codec": a["codec_name"], "sample_rate": a["sample_rate"], "channels": a["channels"],
                    "lufs": lufs, "true_peak_dbfs": peak, "duration": dur}
