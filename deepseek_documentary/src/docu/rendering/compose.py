"""Assemble the film: concatenate scene videos, place every narration beat at the
time the scene actually started it, add score + SFX with sidechain ducking,
loudness-normalise, and mux. Also writes captions (SRT) and YouTube chapters.

    python -m docu.rendering.compose --quality preview
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.ndimage import uniform_filter1d

from ..audio import music, sfx
from ..paths import AUDIO, BUILD, OUTPUT, SCENES_OUT, TIMING
from ..script import load_script
from .presets import load_video_config, resolve_quality

SR = 48000


def ffprobe_duration(path: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=duration",
                        "-of", "csv=p=0", str(path)], capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def _fmt_srt(t: float) -> str:
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s - int(s)) * 1000)):03d}"


def _chunks(text: str, max_words=12):
    words = text.split()
    out, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) >= max_words or (w.endswith((".", "?", "!")) and len(cur) >= 5):
            out.append(" ".join(cur))
            cur = []
    if cur:
        out.append(" ".join(cur))
    return out


def compose(q: dict, out_path: Path | None = None) -> Path:
    cfg = load_video_config()
    timing = json.loads(TIMING.read_text())
    od = SCENES_OUT / q["name"]
    scenes = load_script()
    missing = [s.id for s in scenes if not (od / f"{s.filename}.mp4").exists()]
    if missing:
        raise SystemExit(f"cannot compose: scenes not rendered: {missing}")

    # ---- timeline
    offsets, durs = [], []
    t = 0.0
    for s in scenes:
        d = ffprobe_duration(od / f"{s.filename}.mp4")
        offsets.append(t)
        durs.append(d)
        t += d
    total = t
    n = int(np.ceil(total * SR)) + SR
    narr = np.zeros(n, dtype=np.float32)
    fx = np.zeros(n, dtype=np.float32)
    srt, chapters = [], []
    idx = 1
    seen_acts = set()
    for s, off, d in zip(scenes, offsets, durs):
        tl = json.loads((od / f"{s.filename}.timeline.json").read_text())
        beats = timing["scenes"][s.id]["beats"]
        if s.act not in seen_acts:
            seen_acts.add(s.act)
            chapters.append((off, s.act_title))
        for b, spec in zip(beats, s.beats):
            start = off + tl["starts"][b["id"]]
            y, sr = sf.read(AUDIO / b["wav"], dtype="float32")
            a = int(start * SR)
            narr[a:a + len(y)] += y[: max(0, n - a)]
            if b.get("sfx") in sfx.SFX:
                e = sfx.SFX[b["sfx"]]().astype(np.float32)
                fx[a:a + len(e)] += e[: max(0, n - a)]
            # captions: split the beat across its duration by word share
            chunks = _chunks(spec.spoken)
            wc = [len(c.split()) for c in chunks]
            tt = start
            for c, w in zip(chunks, wc):
                dd = b["dur"] * w / sum(wc)
                srt.append(f"{idx}\n{_fmt_srt(tt)} --> {_fmt_srt(tt + dd)}\n{c}\n")
                idx += 1
                tt += dd

    # ---- score: one mood per act, crossfaded
    mus = np.zeros((n, 2), dtype=np.float32)
    acts = {}
    for s, off, d in zip(scenes, offsets, durs):
        a0, a1, mood = acts.get(s.act, (off, off + d, s.music))
        acts[s.act] = (min(a0, off), max(a1, off + d), mood)
    xf = 2.5
    for act, (a0, a1, mood) in sorted(acts.items()):
        seg = music.generate(mood, (a1 - a0) + xf, seed=act)
        a = int(max(0, a0 - xf / 2) * SR)
        b = min(n, a + len(seg))
        mus[a:b] += seg[: b - a]

    # ---- sidechain ducking from the narration envelope
    env = np.sqrt(uniform_filter1d(narr.astype(np.float64) ** 2, size=int(0.25 * SR)))
    duck = np.clip(env / 0.04, 0, 1)
    duck = uniform_filter1d(duck, size=int(0.6 * SR))  # smooth attack/release
    music_gain = 0.60 * (1.0 - 0.55 * duck)
    mix = np.stack([narr, narr], 1) * 1.0 + mus * music_gain[:, None].astype(np.float32) + np.stack([fx, fx], 1) * 0.35
    peak = float(np.abs(mix).max() or 1)
    if peak > 0.98:
        mix *= 0.98 / peak
    mixd = BUILD / "mix" / q["name"]
    mixd.mkdir(parents=True, exist_ok=True)
    mix_wav = mixd / "mix.wav"
    sf.write(mix_wav, mix[: int(total * SR)], SR, subtype="PCM_24")
    sf.write(mixd / "narration_stem.wav", narr[: int(total * SR)], SR, subtype="PCM_16")

    # ---- video concat + mux
    lst = mixd / "concat.txt"
    lst.write_text("".join(f"file '{(od / f'{s.filename}.mp4').as_posix()}'\n" for s in scenes))
    dest_dir = OUTPUT / ("review" if q["name"] == "preview" else "final")
    dest_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_path or dest_dir / f"{cfg['output_basename']}_{q['height']}p_{q['name']}.mp4"
    if q.get("reencode", True):
        vcodec = ["-c:v", "libx264", "-preset", q["preset"], "-crf", str(q["crf"]), "-pix_fmt", "yuv420p",
                  "-r", str(q["fps"])]
    else:
        vcodec = ["-c:v", "copy"]   # scene files are already H.264; see config/video.yaml
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-i", str(mix_wav),
           "-map", "0:v:0", "-map", "1:a:0", *vcodec, "-movflags", "+faststart",
           "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", q["audio_bitrate"], "-ar", str(SR),
           "-t", f"{total:.3f}", str(out_path)]
    print("[compose] " + ("encoding" if q.get("reencode", True) else "stream-copying video to"), out_path)
    subprocess.run(cmd, check=True)
    base = out_path.with_suffix("")
    Path(str(base) + ".srt").write_text("\n".join(srt))
    ch = "\n".join(f"{int(t0 // 60):02d}:{int(t0 % 60):02d} {title}" for t0, title in chapters)
    Path(str(base) + ".chapters.txt").write_text(ch + "\n")
    manifest = [{"scene": s.id, "file": f"{s.filename}.mp4", "start": round(o, 3), "duration": round(d, 3),
                 "act": s.act, "title": s.title} for s, o, d in zip(scenes, offsets, durs)]
    Path(str(base) + ".manifest.json").write_text(json.dumps(manifest, indent=1))
    print(f"[compose] done: {out_path} ({total/60:.1f} min)")
    return out_path


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--quality")
    ap.add_argument("--resolution")
    ap.add_argument("--fps", type=int)
    a = ap.parse_args(argv)
    compose(resolve_quality(a.quality, a.resolution, a.fps))


if __name__ == "__main__":
    main()
