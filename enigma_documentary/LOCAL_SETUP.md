# Running everything on your own computer

Everything renders **locally**. Nothing runs on GitHub Actions. A low-spec laptop
works; it's just slower, and every step can be stopped and resumed.

## 1. Install once

| Tool | Version | Where |
|---|---|---|
| Python | 3.11 recommended (3.10–3.12 work) | python.org |
| Blender | **4.2 LTS** or newer | blender.org/download/lts |
| Node.js | 20 LTS or newer | nodejs.org |
| Fonts (optional) | IBM Plex Sans + IBM Plex Mono | fonts.google.com (install "for all users") |

Linux only, before the Python packages (Manim needs Pango headers):
```bash
sudo apt install libpango1.0-dev pkg-config python3-dev
```

Then, in this folder (`enigma_documentary/`):
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate        macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cd remotion && npm install && cd ..
python run.py doctor
```
`doctor` lists anything missing and how to fix it. If Blender isn't found, set its path:
- Windows (PowerShell): `$env:BLENDER="C:\Program Files\Blender Foundation\Blender 4.2\blender.exe"`
- macOS: `export BLENDER=/Applications/Blender.app/Contents/MacOS/Blender`

The Kokoro voice model (~350 MB) downloads automatically the first time you run the voice step.

## 2. First run: a draft (about 11 hours for Acts I–VI on 4 cores; `preview` takes about 3)

```bash
python run.py all --profile draft
```
This runs every step in order: tests → claim ledger → narration → simulator events → SFX → timeline → Blender → Manim → stage → Remotion.
Result: `output/enigma_draft.mp4` plus `output/enigma_draft.srt` captions.

Watch it before you spend a night on the final render. To scrub the edit live in a browser:
```bash
python run.py studio --profile draft
```
Scenes that aren't rendered yet show up as labelled storyboard slates, so the studio works from the very start.

## 3. Estimate, then render the final version overnight

```bash
python run.py estimate --profile final     # renders 1 frame per Blender shot, prints projected hours
python run.py all --profile final          # 1080p24; resumable
```
Measured on a 4-core CPU with no GPU: about **135 hours** of Blender time for Acts I–VI (about 20 h for Acts I–II, 45 h for I–III, 70 h for I–IV, 100 h for I–V). Manim and Remotion take minutes. Render one scene per night if you like: `python run.py blender --profile final --scene s0301`.

- **Stop any time** (Ctrl+C, close the lid, reboot). Run the same command again and it continues. Finished frames are kept; the frame that was interrupted is redone.
- **Keep the laptop usable** while it renders: `BLENDER_THREADS=3 python run.py blender --profile final` (Windows PowerShell: `$env:BLENDER_THREADS=3`).
- **Only one scene:** `python run.py blender --profile final --scene s0101`.
- **Continue after Blender finishes:** `python run.py all --profile final --from manim`.
- **Laptop sleeps?** Turn off sleep while plugged in. On Windows: Settings → Power → Screen and sleep → *Never* (when plugged in).

## 4. If you have a GPU (even a modest one)

| Command | When |
|---|---|
| `BLENDER_DEVICE=GPU python run.py all --profile final_gpu` | NVIDIA/AMD/Apple GPU that Cycles supports: 64 samples, much faster |
| `python run.py all --profile final_eevee` | Any GPU with OpenGL 4.3, including Intel/AMD integrated: EEVEE renders in seconds per frame |

Run `estimate` with the profile first. EEVEE couldn't be tested in the build environment (it had no GPU), so check the sample frame in `build/estimate/` before committing.

## Profiles

| Profile | Size | fps | Blender | Use |
|---|---|---|---|---|
| smoke | 320×180 | 6 | 8 samples | proves the pipeline works (minutes) |
| preview | 640×360 | 12 | 4 samples | watch the whole film (about 3 h for Acts I–VI) |
| draft | 960×540 | 12 | 8 samples | timing & story check (about 11 h for Acts I–VI) |
| review | 1280×720 | 24 | 12 samples | look check |
| **final** | 1920×1080 | 24 | 16 samples + denoise | CPU-only master |
| final_gpu | 1920×1080 | 24 | 64 samples | with a GPU |
| final_eevee | 1920×1080 | 24 | EEVEE 64 | with any GPU |
| final4k | 3840×2160 | 24 | 64 samples | GPU + patience |

Scene code never changes between profiles; they only change pixels, frame rate and samples (`config/render_profiles.yaml`).

## Where things end up

```
output/enigma_<profile>.mp4 / .srt       the film + captions
renders/blender/<profile>/<scene>/       PNG frames (resumable)
renders/manim/<profile>/<scene>.mp4      Manim clips
build/audio/                             narration per beat + timing.json
build/events/                            simulator event streams
build/timeline.json                      the one clock every tool follows
build/blend/<scene>.blend                (with --save-blend) open in Blender to look around
```

## Troubleshooting

- **`manimpango` fails to build (Linux):** install `libpango1.0-dev pkg-config`, then `pip install -r requirements.txt` again.
- **Remotion can't find a browser:** it downloads Chrome Headless Shell on first render. If that is blocked, point it at an installed Chrome/Chromium: `REMOTION_BROWSER="/path/to/chrome" python run.py remotion --profile draft`.
- **Out of memory in Remotion:** `python run.py remotion --profile final --concurrency 1`.
- **A scene looks wrong after an edit:** Blender frames are invalidated automatically when a shot's code, events, timing or profile changes; Manim clips too.
- **Rig and simulator disagree:** rendering stops with `rig and simulator disagree`. That is deliberate. Fix the shot, never the check.
