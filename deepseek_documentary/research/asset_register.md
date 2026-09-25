# Asset register (figures from source documents)

| Asset ID | Source | Page | Figure | Why it matters | Treatment | Attribution |
|---|---|---|---|---|---|---|
| A-01 | V4.1-Flash paper | 1 | Fig. 1(b) global KV cache per token across DeepSeek generations | The film's payoff number (890 B) | **Recreated** in Manim (s0906), values copied exactly, linear scale labelled | "Data: DeepSeek-AI, arXiv:2609.19969, Fig. 1(b) — recreated" |
| A-02 | V4.1-Flash paper | 1 | Fig. 1(a) agentic benchmark bars | Performance context | **Not used**: self-reported benchmarks against models the viewer doesn't know; replaced by a "reported" card | — |
| A-03 | V4.1-Flash paper | 5 | Fig. 2 decode FLOPs vs context | Shows compute nearly flat | **Recreated qualitatively** (s0906 b7): only the stated +¼ over 256× context | "paper Fig. 2" on screen |
| A-04 | V4.1-Flash paper | 7 | Fig. 3 overall architecture | Encoder/decoder split, CSA2 groups | **Recreated/simplified** (s0903, s0905) | source line on screen |
| A-05 | V4.1-Flash paper | 10 | Fig. 4 CSA2 Full/Reindex/Reuse | Core idea of layer reuse | **Recreated** as mode badges + borrowing arrows (s0903) | source line |
| A-06 | V4.1-Flash paper | 11 | Fig. 5 Hierarchical Sparse Indexer | Decoder candidate pool | Referenced implicitly (indexer scan, s0902); pool detail omitted for clarity | — |

No third-party internet images are used. All visuals are generated in Manim, and all music and SFX are synthesised procedurally (`src/docu/audio`), so there are no licensing dependencies.
