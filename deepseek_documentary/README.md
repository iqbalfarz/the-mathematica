# DeepSeek Did the Impossible — The First-Principles Story of How

A complete, reproducible production system for a ~38-minute technical documentary. It covers everything from research, claim ledger and script, through Kokoro-82M narration and Manim animation, to the audio mix, validation and cloud rendering. The same source renders 720p previews and 4K or 8K masters.

The story runs from a single multiplication to DeepSeek-V4.1-Flash's 890-byte-per-token KV cache. Along the way it explains why GPUs matter, how a Transformer computes, why Mixture-of-Experts trades compute for communication, and why memory became the wall. Every number is traceable to `research/claim_ledger.csv`.

## Layout

```
deepseek_documentary/
├── config/            video.yaml (quality presets) · voice.yaml (TTS) · sources.yaml
├── research/          build_ledger.py → claim_ledger.csv, number_ledger.md · research_notes.md · source_map.md
│                      bibliography.md · timeline.md · architecture_map.md · asset_register.md
├── story/             acts/act01..12.yaml  ← THE SCRIPT (single source of truth)
│                      blueprint.md · loop_map.yaml · script.md · storyboard.md · scene_manifest.yaml (generated)
├── src/docu/
│   ├── base_scene.py  DocScene: audio-locked beat timing + runtime layout guard
│   ├── style.py       semantic colour system and type scale
│   ├── components/    Token, MatrixGrid, Heatmap, GPU, MemoryBank, Pipe, Expert(Grid), Router, KVShelf,
│   │                  LayerTower, Block, HBarChart, WallsLegend, typography helpers …
│   ├── scenes/        act01.py … act12.py  (44 scene classes)
│   ├── narration/     generate_voice.py · pronounce.py · providers/{kokoro,cloned}.py
│   ├── audio/         music.py (procedural score) · sfx.py (synthesised SFX)
│   ├── rendering/     render.py (cached, resumable, sharded queue) · compose.py · presets.py
│   ├── validation/    source, story, technical, media checks · report.py · contact_sheet.py
│   └── docs.py        generates script.md / storyboard.md / scene_manifest.yaml
├── Dockerfile · Makefile · requirements.txt · pyproject.toml
└── output/            review/ (preview film + report) · final/ (1080p/4K/8K masters)
```

## How the pipeline works

```
story/acts/*.yaml ──► Kokoro-82M (per beat) ──► build/audio/timing.json
        │                                             │
        ▼                                             ▼
   claim tags ──► validation            Manim scenes wait on beat durations
                                                      │
                                   build/scenes/<quality>/scene_NNN.mp4 + timeline.json (actual beat starts)
                                                      │
                     compose: narration placed at actual beat starts + procedural score (ducked) + SFX
                                                      │
                                      output/…/deepseek_first_principles_<h>p_<quality>.mp4 (+ .srt, chapters)
```

Timing is audio-first. Each scene calls `self.beat("b3")`, which waits until the previous beat's narration has finished and then records the real start time. The composer puts the audio exactly there, so picture and sound stay in sync at any resolution or frame rate.

Layout is resolution-independent. All positions are in Manim frame units (the frame is 8 units tall at every resolution), so presets change only the pixel count and fps.

## Local development

```bash
sudo apt-get install -y ffmpeg espeak-ng libcairo2-dev libpango1.0-dev pkg-config \
     texlive-latex-base texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended dvisvgm fonts-inter
python -m venv .venv && . .venv/bin/activate
pip install -r deepseek_documentary/requirements.txt
cd deepseek_documentary
export PYTHONPATH=$PWD/src

make ledger                                     # regenerate claim + number ledgers
make voice                                      # Kokoro narration (weights auto-download from GitHub release)
python -m docu.rendering.render --scenes s0404 --quality preview    # one scene
python -m docu.validation.contact_sheet --scenes s0404               # frame per beat → build/review/
make all QUALITY=preview                        # voice → render → compose → validate → docs
```

Useful flags: `--act 4`, `--force`, `--workers N`, `--shard i/n`, `--list`, `--resolution 3840x2160 --fps 60`. You can also set `RESOLUTION=…` and `FPS=…` as environment variables.

## Cloud preview (no laptop needed)

GitHub → **Actions** → **Render documentary** → *Run workflow*:

| input | preview | 1080p | 4K | 8K |
|---|---|---|---|---|
| quality | `preview` | `1080p` | `4k` | `8k` |
| shards | `8` | `8` | `12` | `16` |

Or from a terminal: `gh workflow run render-documentary.yml -f quality=preview -f shards=8`.

Each run caches narration and every rendered scene per shard, retries failed scenes once, and uploads:
- `documentary-<quality>`: the MP4, `.srt` captions, `.chapters.txt`, `.manifest.json` and the validation report;
- `scenes-<n>`: the individual scene files and logs.

Re-running after an edit only re-renders the scenes whose code, script beats or narration changed.

## Cloud 4K / 8K on your own VM

```bash
docker build -t deepseek-doc deepseek_documentary
docker run -d --name doc4k -v $PWD/out:/work/output -e QUALITY=4k deepseek-doc make all QUALITY=4k WORKERS=8
docker run -d --name doc8k -v $PWD/out:/work/output -e QUALITY=8k deepseek-doc make all QUALITY=8k WORKERS=4
docker logs -f doc4k        # detach any time; the job keeps running
```

The queue is resumable. If the machine restarts, run the same command again: finished scenes are skipped, because their hash is stored next to each `scene_NNN.mp4`.

**Memory and 8K.**
- One render worker peaks at about 1.2 GB at 1080p, about 3 GB at 4K and about 9.3 GB at 8K (measured).
- The queue caps parallel workers to what `MemAvailable` can hold, so an 8K shard on a 16 GB GitHub runner uses one worker.
- `DocScene` also bounds Manim's frame queue (Manim's default queue is unbounded, which pushed 8K past 12 GB).
- The 8K preset uses 30 fps to keep file size and render time sane; override with `--fps 60`.

**Masters are not re-encoded.** For 1080p and above, compose stream-copies Manim's H.264 scene files and only encodes the audio mix. Re-encoding a 36-minute 8K film would take many hours on a CI runner. Set `reencode: true` in `config/video.yaml` to change this.

## Voice

The default is **Kokoro-82M**, male voice `am_michael` (`config/voice.yaml`, or env `KOKORO_VOICE`, `KOKORO_SPEED`).

Kokoro cannot clone voices. `VOICE_PROVIDER=cloned` is a documented extension point (`narration/providers/cloned.py`): plug in a backend that supports zero-shot cloning and point `cloned.reference_audio` at your recording. Timing regenerates from the new audio automatically, so no scene code changes.

## Validation

`python -m docu.validation.report --quality preview` writes `output/review/validation_report_preview.md`. It covers:

| Area | Checks |
|---|---|
| technical | every scene class exists; code beats match script beats; all scenes rendered |
| layout | recorded after every animation: text outside frame, text overlapping text, text below legibility size |
| sources | every sentence with a number carries a claim tag; tags exist; no unlabelled model mixing; on-screen numbers exist in the ledger |
| story | hook, central question, every loop opened and paid off in order |
| video | resolution, fps, 16:9, decode errors, black segments over 2 s |
| audio | loudness (target −16 LUFS), true peak, silences over 4 s, audio/video duration match |

## Honesty rules baked into the project

- The attached V4.1-Flash paper reports no hardware, GPU-hours or cost, and the film says so rather than guessing.
- The "$5.6M" is shown as what DeepSeek said it was: final-run GPU-hours × an assumed $2/hour. It excludes research, experiments, hardware and staff.
- H800 bandwidth figures are labelled "widely reported" (secondary sources disagree).
- Derived arithmetic is labelled as ours on screen.
- Toy examples (attention scores, heads, probabilities, loads) are labelled illustrative.

## Music and SFX

Everything is synthesised in `src/docu/audio` (deterministic, license-free). Moods per act are set in the act YAML (`music:`), and SFX cues per beat (`sfx: impact|whoosh|pulse|hum`).
