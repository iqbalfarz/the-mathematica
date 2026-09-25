# The Mathematica

First-principles explainers that make computer science, mathematics and AI easier to understand.

## Projects

| Project | What it is |
|---|---|
| [`deepseek_documentary/`](deepseek_documentary/README.md) | *DeepSeek Did the Impossible — The First-Principles Story of How*. A ~36-minute research-backed technical documentary with a sourced claim ledger, Kokoro-82M narration, Manim animation, and a validated render pipeline for 720p through 8K. |

## Cloud rendering (no laptop needed)

Renders run on GitHub Actions: **Actions → Render documentary → Run workflow**.

| Quality | `quality` input | `shards` input |
|---|---|---|
| Review | `preview` | `8` |
| 1080p | `1080p` | `8` |
| 4K | `4k` | `12` |
| 8K | `8k` | `16` |

From a terminal: `gh workflow run render-documentary.yml -f quality=4k -f shards=12`.

Finished videos, captions, chapters and the validation report are uploaded as the `documentary-<quality>` artifact. Unchanged scenes are cached between runs.

For local development and Docker/VM rendering, see [`deepseek_documentary/README.md`](deepseek_documentary/README.md).
