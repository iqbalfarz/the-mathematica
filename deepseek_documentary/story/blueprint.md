# Project blueprint

## A. What the source documents teach us

- **Supplied PDF: DeepSeek-V4.1-Flash (arXiv:2609.19969, Sep 2026).** A memory-and-bandwidth paper. Its thesis: once sparse attention tamed long-context compute, the **KV cache** (HBM capacity, SSD capacity, data movement) became the main cost of serving long-horizon agents. Its answers:
  - CSA2 cross-layer reuse;
  - FP4 main cache;
  - Causal Encoder-Decoder;
  - SWA Bounded Replay.

  Together these give 890 B/token of global KV. Its figures (1b, 2, 3, 4, 5) are recreated, not pasted.
- **Pedagogy.** The Mathematica principles quoted in the brief: problem → why current knowledge fails → curiosity → discovery → intuition before notation → formal definition → visual → application → AI connection → cliffhanger.
- **Virality.** Setup → incomplete loop → payoff → new loop. Every loop is tracked in `story/loop_map.yaml` and machine-checked.
- The curriculum and viral-framework files referenced in the brief were not attached. The principles quoted in the brief were applied (decision recorded).

## B. What the DeepSeek story actually appears to be

- **V3 (Dec 2024):** trained on 2,048 **H800s**, a chip NVIDIA designed for China with narrower chip-to-chip links. 2.788M GPU-hours, with performance DeepSeek reports as comparable to leading closed models.
- **The surprise was engineering:**
  - sparse MoE (37B of 671B active);
  - MLA memory compression;
  - FP8 training;
  - compute/communication overlap aimed squarely at the narrow interconnect.
- **By V4.1-Flash (2026),** the frontier of the constraint had moved to memory.

## C. Verified central thesis

Scaling hits three walls: **compute, memory and communication.** DeepSeek's published work attacks each one with mathematics and systems engineering rather than more hardware. The claim is *not* that they did the impossible, or that constraints caused every choice. It is that, under constrained hardware, understanding the bottleneck bought what money could not.

## D. Technical dependency graph

See `research/architecture_map.md`:
multiply → matmul → parameters → FLOPs → GPU parallelism → bandwidth → tokens → embeddings → attention → softmax → blocks → scaling → MoE → routing → load balance → all-to-all → overlap/FP8 → decode → KV cache → MLA → three dials → sparse attention → CSA2 → FP4 → CED → loss → gradient descent → training loop → numbers → synthesis.

## E. Narrative arc (12 acts, 44 scenes, ~38 min)

1. The constraint
2. Compute
3. GPUs & the three walls
4. The Transformer
5. The explosion
6. Mixture of Experts
7. Communication
8. The memory wall (KV, MLA, three dials)
9. V4.1-Flash
10. How models learn (and V3's training)
11. The numbers, honestly
12. The whole machine and the answer

## F. Major open loops

L1–L9 in `story/loop_map.yaml`. Every one is opened and closed, and this is verified by `docu.validation.story_validation`.

## G. Scene architecture

One Manim `Scene` class per storyboard scene (`src/docu/scenes/actNN.py`), all built from a shared component library (`src/docu/components`). Every scene inherits `DocScene`, which provides:
- audio-first beat timing (`self.beat("b3")`);
- a runtime layout guard (frame bounds, text overlap, minimum size).

## H. Source / claim strategy

- `research/build_ledger.py` is the single source of truth. It generates `claim_ledger.csv` and `number_ledger.md`.
- Narration carries `[[CLAIM-ID]]` tags, which are stripped before TTS.
- The validator fails on any quantitative sentence without a tag, on unknown tags, on unlabelled model mixing, and on on-screen numbers absent from the ledger.
- Derived arithmetic is labelled "our arithmetic / estimate" on screen.

## I. Cloud rendering architecture

`.github/workflows/render-documentary.yml`:
- **voice job:** cached by script hash.
- **N-way sharded render matrix:** a per-shard scene cache, so unchanged scenes are skipped; failed scenes are retried.
- **compose + validate job:** uploads the MP4, SRT, chapters, manifest and validation report as artifacts.

The `Dockerfile` is the same environment for any VM (`docker run … make all QUALITY=4k`). Nothing depends on a laptop staying open.

## J. Implementation plan (as executed)

research → ledger → YAML script → Kokoro voice (timing.json) → components + DocScene → 44 scenes → sharded render → compose (narration placed at recorded beat times, procedural score with sidechain ducking, SFX, loudnorm −16 LUFS) → validation report → generated script.md / storyboard.md / manifest.
