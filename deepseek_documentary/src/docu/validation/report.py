"""Run every validation and write output/<review|final>/validation_report.md.

    python -m docu.validation.report --quality preview
"""
from __future__ import annotations

import argparse
import json
import time

from ..paths import OUTPUT, SCENES_OUT, TIMING
from ..rendering.presets import load_video_config, resolve_quality
from ..script import load_script, word_count
from . import media_validation, source_validation, story_validation, technical_validation


def section(title, issues, extra=""):
    status = "PASS" if not issues else "FAIL"
    body = "\n".join(f"- {i}" for i in issues) if issues else "- no issues"
    return f"## {title}: **{status}**\n\n{extra}{body}\n", status


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--quality")
    a = ap.parse_args(argv)
    q = resolve_quality(a.quality)
    cfg = load_video_config()
    scenes = load_script()
    od = SCENES_OUT / q["name"]
    parts, statuses = [], {}

    # technical
    tech = technical_validation.check()
    missing = [s.id for s in scenes if not (od / f"{s.filename}.mp4").exists()]
    tech += [f"scene not rendered: {m}" for m in missing]
    if not TIMING.exists():
        tech.append("narration timing missing")
    txt, statuses["technical"] = section("Technical (imports, scene classes, beat coverage, renders)", tech)
    parts.append(txt)

    # layout (runtime guard in DocScene)
    lay = []
    for s in scenes:
        tl = od / f"{s.filename}.timeline.json"
        if tl.exists():
            for v in json.loads(tl.read_text())["violations"]:
                lay.append(f"{s.id} t={v['t']}s {v['type']}: {v['what']}")
    txt, statuses["layout"] = section("Visual layout (text in frame, no text overlap, legibility)", lay,
                                      "Checked after every animation in every scene.\n\n")
    parts.append(txt)

    # source
    src_issues, st, unused = source_validation.check_script()
    on = source_validation.check_onscreen()
    extra = (f"{st['beats']} narration beats; {st['tagged']} carry claim tags ({st['tags']} tags). "
             f"Ledger entries not cited in narration (on-screen/support only): {', '.join(unused) or 'none'}.\n\n")
    txt, statuses["sources"] = section("Research / sources (every number traceable, no model mixing)",
                                       src_issues + on, extra)
    parts.append(txt)

    # story
    st_issues, loops, checks = story_validation.check()
    tbl = "| Loop | Question | Opened | Payoff |\n|---|---|---|---|\n" + "".join(
        f"| {k} | {v['question']} | {v['opened']} | {v['payoff']} |\n" for k, v in loops.items())
    txt, statuses["story"] = section("Story (hook, central question, loops opened and closed)", st_issues, tbl + "\n")
    parts.append(txt)

    # media
    dest = OUTPUT / ("review" if q["name"] == "preview" else "final")
    film = dest / f"{cfg['output_basename']}_{q['height']}p_{q['name']}.mp4"
    media_info = {}
    if film.exists():
        manifest = json.loads(film.with_suffix(".manifest.json").read_text())
        expected = sum(m["duration"] for m in manifest)
        vi, vinfo = media_validation.visual(film, q)
        de = media_validation.decode_errors(film)
        ai, ainfo = media_validation.audio(film, expected)
        media_info = {"video": vinfo, "audio": ainfo}
        txt, statuses["video"] = section("Rendered video (format, black frames, decode errors)", vi + de,
                                         f"`{film.name}` — {vinfo}\n\n")
        parts.append(txt)
        txt, statuses["audio"] = section("Audio (narration present, loudness, peaks, silence, sync)", ai,
                                         f"{ainfo}\n\n")
        parts.append(txt)
    else:
        statuses["video"] = statuses["audio"] = "FAIL"
        parts.append(f"## Rendered video: **FAIL**\n\n- {film} not found\n")

    head = (f"# Validation report — {q['name']} ({q['width']}x{q['height']} @ {q['fps']} fps)\n\n"
            f"Generated {time.strftime('%Y-%m-%d %H:%M:%S')}. {len(scenes)} scenes, {word_count()} narration words.\n\n"
            "| Check | Status |\n|---|---|\n" + "".join(f"| {k} | {v} |\n" for k, v in statuses.items()) + "\n")
    dest.mkdir(parents=True, exist_ok=True)
    out = dest / f"validation_report_{q['name']}.md"
    out.write_text(head + "\n".join(parts))
    (dest / f"validation_{q['name']}.json").write_text(json.dumps({"statuses": statuses, "media": media_info}, indent=1))
    print(head)
    print(f"[report] {out}")


if __name__ == "__main__":
    main()
