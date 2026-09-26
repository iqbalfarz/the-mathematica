# Research notes

Status legend used everywhere: **FACT** (primary source, read directly) · **REPORTED** (primary source, self-reported by DeepSeek) · **SECONDARY** (reputable secondary analysis) · **DERIVED** (our arithmetic, shown as such on screen) · **UNKNOWN** (not public; we do not guess).

## 1. What the supplied document is (and is not)

The attached PDF is **"DeepSeek-V4.1-Flash: Pushing the Limits of KV Cache Compression"** (DeepSeek-AI, arXiv:2609.19969v1, 17 Sep 2026, 51 pages). It was read in full (text), and its figures were inspected as page images (Fig. 1 a/b, Fig. 2, Fig. 3, Fig. 4, Fig. 5).

It is a paper about **inference memory**: the KV cache, long-context agents, prefill cost, and storage/bandwidth. It does **not** mention export controls, GPU types, GPU counts, GPU-hours or training cost for V4.1-Flash (FACT, by absence, CLAIM V41-014).

The popular story (sanctions, "the GPUs China couldn't buy", "$5.6M") belongs to **DeepSeek-V3** (Dec 2024). The documentary therefore follows a **V3 → V4.1-Flash arc**, and every number is tagged with its model.

## 2. Export controls: what can be claimed

| Date | Event | Status | Source |
|---|---|---|---|
| 7 Oct 2022 | BIS rule (ECCN 3A090) restricts top AI chips to China; criteria include ≥600 GB/s interconnect with high performance. A100, H100 caught. | SECONDARY | Covington 2022, Epoch AI, BIS page |
| 2022–23 | NVIDIA ships China versions A800/H800 with cut interconnect bandwidth. | SECONDARY | CSET, Epoch AI |
| 17 Oct 2023 | Update: performance and performance-density criteria; A800/H800 restricted. | SECONDARY | CSET, CSIS, BIS |
| 9/14 Apr 2025 | NVIDIA told a licence is required for H20 exports to China, for the indefinite future. | FACT | NVIDIA Form 8-K (SEC) |

**H800 bandwidth.** It is widely reported as ≈400 GB/s NVLink vs 900 GB/s for H100, with compute and memory essentially unchanged. Sources differ (some say ≈300 GB/s), so the film says "widely reported" and never presents it as an NVIDIA spec.

**What "impossible" means.** It was not impossible. DeepSeek-V3 was trained on H800s, which NVIDIA designed for the Chinese market; the report does not say they were obtained illegally, and we make no such claim. The surprise is technical: a frontier-class result on a constrained interconnect, with openly published methods.

**Forbidden:**
- "DeepSeek used banned or smuggled chips."
- "China was cut off from all GPUs."
- "DeepSeek built its AI for $5.6M."
- "V4.1 was built because of sanctions." The paper says nothing of the kind.

## 3. DeepSeek-V3 (primary: official README, official config, technical report)

- 671B total, 37B active per token (FACT, README).
- 14.8T training tokens (FACT).
- 2.788M H800 GPU-hours in total: 2.664M pre-training + 119K context extension + 5K post-training (FACT, README and report Table 1).
- A 2,048×H800 cluster; 180K GPU-hours per trillion tokens ≈ 3.7 days (REPORTED; report excerpt).
- $5.576M at an assumed $2/GPU-hour. The report states this excludes prior research and ablation experiments (REPORTED).
- Architecture from `inference/configs/config_671B.json` (FACT):
  - 61 layers, dim 7168, 128 heads;
  - 256 routed experts + 1 shared expert, 8 activated per token;
  - MLA kv_lora_rank 512, rope head dim 64;
  - sigmoid router scoring;
  - FP8 weights.
- FP8 mixed-precision training, "validated for the first time at extremely large scale" (REPORTED, README).
- DualPipe: computation/communication overlap for cross-node expert parallelism (REPORTED, report §3.2).
- Performance: "comparable to leading closed-source models" is DeepSeek's own claim on its own benchmarks, and is presented as such.

## 4. DeepSeek-V2

236B total / 21B active (FACT). MLA reduced KV cache by 93.3% vs DeepSeek 67B (REPORTED, abstract).

## 5. DeepSeek-V4.1-Flash (primary: supplied paper)

| Topic | Details | Location |
|---|---|---|
| Size | 552B backbone parameters + 196B Engram parameters; 8B active in prefill, 16B in decode; context up to 1M tokens | Abstract, §2.1 |
| Depth | 40 layers = 20-layer causal encoder + 20-layer decoder; d = 5120 | §4.2.1 |
| MoE | 1 shared + 384 routed experts, 6 active | §4.2.1 |
| Attention | SWA window 128; attention top-k 512 | §4.2.1 |
| CSA2 modes | Full / Reindex / Reuse. Encoder: 2 SWA layers, then 3 groups × (1 Full + 5 Reuse) at m=2. Decoder: 5 groups × 4 at m=1 | §2.3, §4.2.1 |
| FP4 main KV | E2M1 values + E4M3 scale per 16 channels (NVFP4-like, no global scale); SWA KV stays FP8; nearly halves storage vs V4's FP8 | §2.4.4 |
| CED | Decoder global KV projected from the final encoder hidden state; prefill O(NL) → ≈O(NL/2) | §2.2 |
| KV footprint | Global KV 890 B/token ≈ ¼ of V4-Flash; persistent KV ≈ ⅛ | Abstract |
| Fig. 1b | V1 389,120 B · V3.2 48,068 B · V4-Flash 3,514 B · V4.1-Flash 890 B (≈437× vs V1) | Fig. 1b |
| Fig. 2 | 4K → 1M context (256×) raises decode FLOPs by only ≈¼ | Fig. 2, §1 |
| Pre-training | 45T multimodal tokens; batch 100.6M tokens; 64K sequence length, extended to 1M at 34T | §4.2.2 |
| Post-training | "introduces no algorithmic innovation"; the changes are in the data pipeline | §1 |
| Limitations | CSA2 selection errors and approximate SWA replay may degrade untested edge cases | §6 |

## 6. Derived numbers (always labelled on screen)

| ID | Calculation |
|---|---|
| DER-001 | 6 × 37B × 14.8T ≈ 3.3e24 FLOPs (a rule-of-thumb estimate, not DeepSeek's figure) |
| DER-002 | Hypothetical MHA KV for V3's shape: 2×61×128×128×2 B ≈ 4.0 MB/token → ≈524 GB at 128K tokens |
| DER-003 | 45T / 100.6M ≈ 447K optimizer steps |
| DER-004 | 671 GB of FP8 weights > eight 80 GB GPUs |
| DER-005 | 2 × 37B ≈ 74B FLOPs per token (forward) |
| DER-006 | 7168² = 51,380,224 multiplications |
| DER-007 | 37/671 ≈ 5.5% active |
| V3-010 | 32,768 vs 576 cached numbers per token per layer (≈57×) |

## 7. Accuracy decisions made during production

- The classic "it was tired" example is bidirectional. For a left-to-right language model, "it" cannot see "tired", so the attention visuals use a **causal mask**, and the narration says so explicitly.
- The router is shown with softmax for teaching. V3 actually scores experts with a sigmoid (config), so the narration avoids claiming a V3-specific gating formula.
- The Fig. 2 recreation shows only the paper's stated V4.1-Flash endpoints (+¼ for 256× context). No other curves are traced, to avoid inventing data points.
- The Fig. 1b recreation uses a **linear** scale, labelled on screen, with values copied from the figure.

## 8. Research environment limits (disclosed)

arxiv.org, huggingface.co and bis.gov were blocked by the build environment's egress proxy.

- V3 facts were read from DeepSeek's official GitHub repository (README + config). Report-only details (2,048 GPUs, $2/hour, the exclusions sentence, 180K/3.7 days, DualPipe, 119K/5K) come from verbatim search excerpts of the report and are marked PRIMARY_EXCERPT in the ledger.
- Before publication, spot-check those rows against the PDF (arXiv:2412.19437, §1 and Table 1).
