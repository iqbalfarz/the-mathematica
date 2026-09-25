# Number ledger

Generated from `build_ledger.py`. One record per quantitative claim.

### EXP-001
```text
NUMBER(S): 2022 , 600 GB
CLAIM: Oct 2022 US rules restricted export to China of top AI chips such as NVIDIA A100 and H100; one control criterion was chip-to-chip interconnect of 600 GB/s or more.
SOURCE: COVINGTON_2022; EPOCH_EXPORT; BIS_2023
MODEL: n/a
PAGE/SECTION/TABLE: ECCN 3A090 summary
PRIMARY OR SECONDARY: secondary+primary page (VERIFIED_SECONDARY)
ALLOWED WORDING: In October 2022 the US restricted exports of top AI chips like the A100 and H100 to China.
WHAT THE NUMBER DOES NOT MEAN: China was cut off from all GPUs / all NVIDIA chips.
```

### EXP-002
```text
NUMBER(S): 2022 
CLAIM: NVIDIA created China-specific A800 and H800 chips with reduced interconnect bandwidth to fall under the 2022 thresholds.
SOURCE: CSET_2023; EPOCH_EXPORT
MODEL: n/a
PAGE/SECTION/TABLE: explainer
PRIMARY OR SECONDARY: secondary (VERIFIED_SECONDARY)
ALLOWED WORDING: NVIDIA responded with China versions, the A800 and H800, with slower chip-to-chip links.
WHAT THE NUMBER DOES NOT MEAN: The H800 is a weak or slow chip overall.
```

### EXP-003
```text
NUMBER(S): 17, , 2023 B
CLAIM: The October 17, 2023 BIS update switched to performance / performance-density criteria and captured the A800 and H800.
SOURCE: CSET_2023; CSIS_2023; BIS_2023
MODEL: n/a
PAGE/SECTION/TABLE: explainer
PRIMARY OR SECONDARY: secondary+primary page (VERIFIED_SECONDARY)
ALLOWED WORDING: In October 2023 the rules were tightened, and the H800 itself was restricted.
WHAT THE NUMBER DOES NOT MEAN: DeepSeek used banned / smuggled chips.
```

### EXP-004
```text
NUMBER(S): 9, , 2025 , 14 
CLAIM: On April 9, 2025 NVIDIA was told a licence is required to export H20 to China; on April 14 it was told this applies for the indefinite future.
SOURCE: NVDA_8K_2025_04
MODEL: n/a
PAGE/SECTION/TABLE: Form 8-K Item 8.01
PRIMARY OR SECONDARY: primary (SEC filing) (VERIFIED_PRIMARY)
ALLOWED WORDING: In April 2025 even the H20, a chip designed for the Chinese market, required a US export licence.
WHAT THE NUMBER DOES NOT MEAN: H20 was permanently banned.
```

### EXP-005
```text
NUMBER(S): ~400 GB, 900 GB
CLAIM: H800 NVLink bandwidth is reduced relative to H100 (widely reported ~400 GB/s vs 900 GB/s); compute cores and memory essentially unchanged.
SOURCE: EPOCH_EXPORT; vendor spec summaries
MODEL: n/a
PAGE/SECTION/TABLE: spec comparisons
PRIMARY OR SECONDARY: secondary (VERIFIED_SECONDARY)
ALLOWED WORDING: Same engine, narrower pipes: the H800 kept its compute but its GPU-to-GPU links were cut — widely reported as about 400 versus 900 gigabytes per second.
WHAT THE NUMBER DOES NOT MEAN: Exact figure stated as official NVIDIA specification.
```

### V2-001
```text
NUMBER(S): 236B, 21B
CLAIM: DeepSeek-V2 has 236B total parameters with 21B activated per token.
SOURCE: V3_README (table); V2_REPORT
MODEL: DeepSeek-V2
PAGE/SECTION/TABLE: README comparison table
PRIMARY OR SECONDARY: primary (VERIFIED_PRIMARY)
ALLOWED WORDING: DeepSeek-V2: 236 billion parameters, about 21 billion active per token.
WHAT THE NUMBER DOES NOT MEAN: n/a
```

### V2-002
```text
NUMBER(S): 93.3%, 67B
CLAIM: MLA reduced KV cache by 93.3% relative to DeepSeek 67B.
SOURCE: V2_REPORT
MODEL: DeepSeek-V2
PAGE/SECTION/TABLE: Abstract
PRIMARY OR SECONDARY: primary (PRIMARY_EXCERPT)
ALLOWED WORDING: DeepSeek reported that MLA cut the KV cache by 93.3 percent compared with their earlier 67-billion-parameter model.
WHAT THE NUMBER DOES NOT MEAN: MLA invented KV-cache compression / reduces all memory 93%.
```

### V3-001
```text
NUMBER(S): 671B, 37B
CLAIM: DeepSeek-V3 has 671B total parameters, 37B activated per token.
SOURCE: V3_README
MODEL: DeepSeek-V3
PAGE/SECTION/TABLE: README §1
PRIMARY OR SECONDARY: primary (VERIFIED_PRIMARY)
ALLOWED WORDING: 671 billion parameters in total — but only 37 billion active for any one token.
WHAT THE NUMBER DOES NOT MEAN: V3 uses 37B parameters total.
```

### V3-002
```text
NUMBER(S): 14.8T
CLAIM: DeepSeek-V3 was pre-trained on 14.8T tokens.
SOURCE: V3_README
MODEL: DeepSeek-V3
PAGE/SECTION/TABLE: README §1-2
PRIMARY OR SECONDARY: primary (VERIFIED_PRIMARY)
ALLOWED WORDING: trained on 14.8 trillion tokens
WHAT THE NUMBER DOES NOT MEAN: n/a
```

### V3-003
```text
NUMBER(S): 2.788M, 2.664M, 119K, 5K
CLAIM: Full training of DeepSeek-V3 required 2.788M H800 GPU hours: 2.664M pre-training + 119K context extension + 5K post-training.
SOURCE: V3_README; V3_REPORT
MODEL: DeepSeek-V3
PAGE/SECTION/TABLE: README §1-2; report Table 1
PRIMARY OR SECONDARY: primary (VERIFIED_PRIMARY)
ALLOWED WORDING: DeepSeek reports 2.788 million H800 GPU-hours for the full training run.
WHAT THE NUMBER DOES NOT MEAN: The whole of DeepSeek cost 2.788M GPU hours.
```

### V3-004
```text
NUMBER(S): 2,048 , 180K, 3.7 
CLAIM: Training used a cluster of 2,048 NVIDIA H800 GPUs; each trillion tokens took 180K GPU hours, i.e. 3.7 days.
SOURCE: V3_REPORT
MODEL: DeepSeek-V3
PAGE/SECTION/TABLE: Abstract/§1 & §3.1
PRIMARY OR SECONDARY: primary (PRIMARY_EXCERPT)
ALLOWED WORDING: a cluster of 2,048 H800s; each trillion tokens took about 3.7 days
WHAT THE NUMBER DOES NOT MEAN: n/a
```

### V3-005
```text
NUMBER(S): 2 , 5.576M
CLAIM: Assuming $2 per H800 GPU hour rental, the official training run costs $5.576M; this excludes prior research and ablation experiments.
SOURCE: V3_REPORT
MODEL: DeepSeek-V3
PAGE/SECTION/TABLE: §1 Table 1 and following text
PRIMARY OR SECONDARY: primary (PRIMARY_EXCERPT)
ALLOWED WORDING: At an assumed rental price of $2 per GPU-hour, DeepSeek estimated the final run at about $5.6 million — and explicitly excluded research, experiments, staff and hardware.
WHAT THE NUMBER DOES NOT MEAN: DeepSeek built its AI for $5.6 million. / Total cost of DeepSeek was $5.6M.
```

### V3-006
```text
NUMBER(S): 
CLAIM: DeepSeek-V3 used an FP8 mixed-precision training framework, validated at extremely large scale for the first time (per DeepSeek).
SOURCE: V3_README
MODEL: DeepSeek-V3
PAGE/SECTION/TABLE: README §2
PRIMARY OR SECONDARY: primary (VERIFIED_PRIMARY)
ALLOWED WORDING: DeepSeek says V3 was the first to validate FP8 training at this scale.
WHAT THE NUMBER DOES NOT MEAN: FP8 was invented by DeepSeek.
```

### V3-007
```text
NUMBER(S): 
CLAIM: DeepSeek-V3 adopts MLA and DeepSeekMoE, validated in DeepSeek-V2.
SOURCE: V3_README
MODEL: DeepSeek-V3
PAGE/SECTION/TABLE: README §1
PRIMARY OR SECONDARY: primary (VERIFIED_PRIMARY)
ALLOWED WORDING: V3 reuses two ideas proven in V2: Multi-head Latent Attention and DeepSeekMoE.
WHAT THE NUMBER DOES NOT MEAN: n/a
```

### V3-008
```text
NUMBER(S): 256 , 1 , 8 , 61 , 7168, 128 
CLAIM: V3 MoE layers: 256 routed experts + 1 shared expert, 8 routed experts activated per token; 61 layers; hidden dim 7168; 128 heads.
SOURCE: V3 inference/configs/config_671B.json
MODEL: DeepSeek-V3
PAGE/SECTION/TABLE: config_671B.json
PRIMARY OR SECONDARY: primary (official config) (VERIFIED_PRIMARY)
ALLOWED WORDING: 256 routed experts plus one shared expert per layer; each token visits 8 of the 256.
WHAT THE NUMBER DOES NOT MEAN: n/a
```

### V3-009
```text
NUMBER(S): 512, 64, 512, 
CLAIM: V3's MLA caches a 512-dim compressed KV latent plus a 64-dim positional key per token per layer (kv_lora_rank 512, qk_rope_head_dim 64).
SOURCE: V3 config_671B.json
MODEL: DeepSeek-V3
PAGE/SECTION/TABLE: config_671B.json
PRIMARY OR SECONDARY: primary (official config) (VERIFIED_PRIMARY)
ALLOWED WORDING: Instead of full keys and values for every head, V3 stores one 512-number summary plus a 64-number position key.
WHAT THE NUMBER DOES NOT MEAN: n/a
```

### V3-010
```text
NUMBER(S): 128 , 128, 2x, 32,768 , 576 , ~57x
CLAIM: Standard multi-head attention with V3's shape (128 heads, 128-dim K and V) would cache 2x128x128 = 32,768 numbers per token per layer vs 576 for MLA (~57x fewer).
SOURCE: derived from V3-008, V3-009
MODEL: DeepSeek-V3
PAGE/SECTION/TABLE: our arithmetic
PRIMARY OR SECONDARY: derived (DERIVED)
ALLOWED WORDING: If V3 had used ordinary attention, a quick calculation from its published shape gives about 32 thousand numbers per token per layer; MLA stores 576.
WHAT THE NUMBER DOES NOT MEAN: DeepSeek reports a 57x reduction.
```

### V41-001
```text
NUMBER(S): 552B, 196B, 1M
CLAIM: DeepSeek-V4.1-Flash is a multimodal MoE model with 552B backbone parameters (plus 196B Engram parameters), up to 1M-token context.
SOURCE: V41_PAPER
MODEL: DeepSeek-V4.1-Flash
PAGE/SECTION/TABLE: Abstract; §2.1
PRIMARY OR SECONDARY: primary (VERIFIED_PRIMARY)
ALLOWED WORDING: 552 billion backbone parameters, contexts up to a million tokens.
WHAT THE NUMBER DOES NOT MEAN: 552B total parameters (omits Engram) / V4.1 has 748B active.
```

### V41-002
```text
NUMBER(S): 8B, 16B
CLAIM: Activates 8B parameters per token during prefill and 16B during decode (Causal Encoder-Decoder).
SOURCE: V41_PAPER
MODEL: DeepSeek-V4.1-Flash
PAGE/SECTION/TABLE: Abstract; §2.1; §4.2.1
PRIMARY OR SECONDARY: primary (VERIFIED_PRIMARY)
ALLOWED WORDING: about 16 billion active while writing, only 8 billion while reading the prompt
WHAT THE NUMBER DOES NOT MEAN: n/a
```

### V41-003
```text
NUMBER(S): 890 , 1, 4 
CLAIM: Global KV cache footprint is 890 bytes per token, roughly 1/4 of DeepSeek-V4-Flash.
SOURCE: V41_PAPER
MODEL: DeepSeek-V4.1-Flash
PAGE/SECTION/TABLE: Abstract; Fig. 1b
PRIMARY OR SECONDARY: primary (VERIFIED_PRIMARY)
ALLOWED WORDING: 890 bytes of global memory per token — about a quarter of its predecessor.
WHAT THE NUMBER DOES NOT MEAN: Total memory per token is 890 bytes (excludes SWA KV).
```

### V41-004
```text
NUMBER(S): 1, 389,120 B, 2023.11, 48,068 B, 2025.12, 3,514 B, 2026.04, 890 B, 2026.09, ~437x
CLAIM: Fig. 1b global KV cache per token: DeepSeek-V1 389,120 B (2023.11); V3.2 48,068 B (2025.12); V4-Flash 3,514 B (2026.04); V4.1-Flash 890 B (2026.09). ~437x vs V1.
SOURCE: V41_PAPER
MODEL: V1, V3.2, V4-Flash, V4.1-Flash
PAGE/SECTION/TABLE: Figure 1(b)
PRIMARY OR SECONDARY: primary (VERIFIED_PRIMARY)
ALLOWED WORDING: DeepSeek's own chart: from about 389 thousand bytes per token in their first model to 890 — roughly 437 times smaller.
WHAT THE NUMBER DOES NOT MEAN: Numbers presented as independent measurements.
```

### V41-005
```text
NUMBER(S): 1, 8 
CLAIM: Persistent KV cache (SSD/host memory) reduced to roughly 1/8 of V4-Flash via SWA Bounded Replay.
SOURCE: V41_PAPER
MODEL: DeepSeek-V4.1-Flash
PAGE/SECTION/TABLE: Abstract; §3.2.2
PRIMARY OR SECONDARY: primary (VERIFIED_PRIMARY)
ALLOWED WORDING: the long-term stored cache shrinks to about an eighth
WHAT THE NUMBER DOES NOT MEAN: n/a
```

### V41-006
```text
NUMBER(S): 40 , 20, 5120, 128.
CLAIM: Architecture: 40 layers = 20-layer causal encoder + 20-layer decoder; hidden dim 5120; first two layers SWA-only; SWA window 128.
SOURCE: V41_PAPER
MODEL: DeepSeek-V4.1-Flash
PAGE/SECTION/TABLE: §2.1; §4.2.1
PRIMARY OR SECONDARY: primary (VERIFIED_PRIMARY)
ALLOWED WORDING: 40 layers, split into a 20-layer encoder and a 20-layer decoder
WHAT THE NUMBER DOES NOT MEAN: n/a
```

### V41-007
```text
NUMBER(S): 1 , 384 , 6 
CLAIM: Each MoE layer has 1 shared expert and 384 routed experts; 6 routed experts activated per token.
SOURCE: V41_PAPER
MODEL: DeepSeek-V4.1-Flash
PAGE/SECTION/TABLE: §4.2.1
PRIMARY OR SECONDARY: primary (VERIFIED_PRIMARY)
ALLOWED WORDING: 384 routed experts per layer, 6 chosen per token, plus one shared expert
WHAT THE NUMBER DOES NOT MEAN: n/a
```

### V41-008
```text
NUMBER(S): 512 K
CLAIM: CSA2 selects top-512 KV entries per query via a lightweight indexer; layers run in Full, Reindex, or Reuse mode sharing global KV across layers.
SOURCE: V41_PAPER
MODEL: DeepSeek-V4.1-Flash
PAGE/SECTION/TABLE: §2.3; §4.2.1; Fig. 4
PRIMARY OR SECONDARY: primary (VERIFIED_PRIMARY)
ALLOWED WORDING: a small indexer picks the 512 most relevant memories; later layers reuse the same memory instead of storing their own
WHAT THE NUMBER DOES NOT MEAN: n/a
```

### V41-009
```text
NUMBER(S): 16 
CLAIM: Main KV cache stored in FP4 (E2M1 values with an E4M3 scale per 16 channels); SWA KV kept in FP8; nearly halves storage vs V4's FP8 main KV.
SOURCE: V41_PAPER
MODEL: DeepSeek-V4.1-Flash
PAGE/SECTION/TABLE: §2.4.4
PRIMARY OR SECONDARY: primary (VERIFIED_PRIMARY)
ALLOWED WORDING: the main memory is stored in 4-bit numbers, with one shared scale for every 16 values
WHAT THE NUMBER DOES NOT MEAN: n/a
```

### V41-010
```text
NUMBER(S): 2
CLAIM: CED reduces prefill from O(NL) to ~O(NL/2): decoder global KV is projected from the final encoder hidden state, nearly halving prefill computation.
SOURCE: V41_PAPER
MODEL: DeepSeek-V4.1-Flash
PAGE/SECTION/TABLE: §2.2 Eq.1
PRIMARY OR SECONDARY: primary (VERIFIED_PRIMARY)
ALLOWED WORDING: reading a prompt costs roughly half the computation
WHAT THE NUMBER DOES NOT MEAN: n/a
```

### V41-011
```text
NUMBER(S): 256, 4K, 1M, 1, 4.
CLAIM: Extending context 256-fold from 4K to 1M increases V4.1-Flash single-token decode FLOPs by only about 1/4.
SOURCE: V41_PAPER
MODEL: DeepSeek-V4.1-Flash
PAGE/SECTION/TABLE: §1; Fig. 2
PRIMARY OR SECONDARY: primary (VERIFIED_PRIMARY)
ALLOWED WORDING: going from 4 thousand to a million tokens of context raises the cost of each new token by only about a quarter
WHAT THE NUMBER DOES NOT MEAN: Cost is constant / independent of context.
```

### V41-012
```text
NUMBER(S): 45T, 100.6M, 64K, 1M, 34T
CLAIM: Pre-trained on 45T multimodal tokens; batch 100.6M tokens; sparse attention from scratch at 64K sequence length, extended to 1M at 34T tokens.
SOURCE: V41_PAPER
MODEL: DeepSeek-V4.1-Flash
PAGE/SECTION/TABLE: §4.2.2
PRIMARY OR SECONDARY: primary (VERIFIED_PRIMARY)
ALLOWED WORDING: 45 trillion tokens, about a hundred million tokens per training step
WHAT THE NUMBER DOES NOT MEAN: n/a
```

### V41-014
```text
NUMBER(S): 
CLAIM: Paper reports no GPU type, GPU count, GPU-hours, or training cost for V4.1-Flash.
SOURCE: V41_PAPER
MODEL: DeepSeek-V4.1-Flash
PAGE/SECTION/TABLE: whole paper searched
PRIMARY OR SECONDARY: primary (absence) (VERIFIED_PRIMARY)
ALLOWED WORDING: The paper does not say what hardware trained V4.1-Flash, or what it cost.
WHAT THE NUMBER DOES NOT MEAN: Any V4.1 GPU count or cost figure.
```

### V41-015
```text
NUMBER(S): 
CLAIM: Limitations: CSA2 selection errors and approximate SWA state reconstruction may degrade untested boundary cases.
SOURCE: V41_PAPER
MODEL: DeepSeek-V4.1-Flash
PAGE/SECTION/TABLE: §6
PRIMARY OR SECONDARY: primary (VERIFIED_PRIMARY)
ALLOWED WORDING: DeepSeek flags its own risks: the selector can pick wrong, and approximate replay may fail on edge cases.
WHAT THE NUMBER DOES NOT MEAN: n/a
```

### V41-016
```text
NUMBER(S): 
CLAIM: The FP4 format choice (OCP MXFP4 for indexer; NVFP4-like for main KV) is made partly for compatibility across hardware platforms.
SOURCE: V41_PAPER
MODEL: DeepSeek-V4.1-Flash
PAGE/SECTION/TABLE: §2.4.4
PRIMARY OR SECONDARY: primary (VERIFIED_PRIMARY)
ALLOWED WORDING: DeepSeek chose number formats that work across many hardware platforms
WHAT THE NUMBER DOES NOT MEAN: DeepSeek designed its own chips.
```

### GEN-002
```text
NUMBER(S): ~2
CLAIM: Multiplying an (m x n) by (n x p) matrix takes m*n*p multiply-adds (~2mnp FLOPs).
SOURCE: textbook
MODEL: n/a
PAGE/SECTION/TABLE: definition
PRIMARY OR SECONDARY: derived (DERIVED)
ALLOWED WORDING: a 3x3 times 3x3 product needs 27 multiplications
WHAT THE NUMBER DOES NOT MEAN: n/a
```

### GEN-003
```text
NUMBER(S): 2 
CLAIM: A dense forward pass costs roughly 2 FLOPs per active parameter per token.
SOURCE: standard scaling-law approximation (Kaplan et al. 2020)
MODEL: n/a
PAGE/SECTION/TABLE: approximation
PRIMARY OR SECONDARY: secondary (VERIFIED_SECONDARY)
ALLOWED WORDING: a useful rule of thumb: about two operations per active parameter, per token
WHAT THE NUMBER DOES NOT MEAN: Exact FLOP counts for DeepSeek models.
```

### GEN-004
```text
NUMBER(S): 6 
CLAIM: Training costs roughly 6 FLOPs per active parameter per token (forward + backward).
SOURCE: standard approximation
MODEL: n/a
PAGE/SECTION/TABLE: approximation
PRIMARY OR SECONDARY: secondary (VERIFIED_SECONDARY)
ALLOWED WORDING: training is roughly three times a forward pass
WHAT THE NUMBER DOES NOT MEAN: Exact DeepSeek FLOP totals.
```

### DER-001
```text
NUMBER(S): 6 x, 37, 14.8, 3.3, 004.
CLAIM: 6 x 37e9 x 14.8e12 ~= 3.3e24 FLOPs: a rough estimate of V3 pre-training compute using GEN-004.
SOURCE: derived from V3-001, V3-002, GEN-004
MODEL: DeepSeek-V3
PAGE/SECTION/TABLE: our arithmetic
PRIMARY OR SECONDARY: derived (DERIVED)
ALLOWED WORDING: a back-of-envelope estimate: about 3 times 10 to the 24 operations — our estimate, not DeepSeek's figure
WHAT THE NUMBER DOES NOT MEAN: DeepSeek reported 3.3e24 FLOPs.
```

### EXP-006
```text
NUMBER(S): 80 GB
CLAIM: The H800 carries 80 GB of HBM memory, like the H100 SXM.
SOURCE: vendor spec summaries
MODEL: n/a
PAGE/SECTION/TABLE: spec comparisons
PRIMARY OR SECONDARY: secondary (VERIFIED_SECONDARY)
ALLOWED WORDING: each H800 holds 80 gigabytes of fast memory
WHAT THE NUMBER DOES NOT MEAN: n/a
```

### DER-002
```text
NUMBER(S): 61 , 32,768 , 2 , ~4.0 M, ~524 GB, 128K
CLAIM: With V3's shape but ordinary multi-head attention (61 layers x 32,768 cached numbers x 2 bytes BF16), KV cache would be ~4.0 MB per token, ~524 GB at 128K tokens.
SOURCE: derived from V3-008, V3-010
MODEL: DeepSeek-V3 (hypothetical MHA)
PAGE/SECTION/TABLE: our arithmetic
PRIMARY OR SECONDARY: derived (DERIVED)
ALLOWED WORDING: a hypothetical: if V3 had used ordinary attention, a quick calculation gives about 4 megabytes of memory per token
WHAT THE NUMBER DOES NOT MEAN: DeepSeek reported 4 MB per token.
```

### DER-003
```text
NUMBER(S): 45T, 100.6M, 447 
CLAIM: 45T tokens / 100.6M tokens per step ~= 447 thousand optimizer steps for V4.1-Flash pre-training (ignoring warmup detail).
SOURCE: derived from V41-012
MODEL: DeepSeek-V4.1-Flash
PAGE/SECTION/TABLE: our arithmetic
PRIMARY OR SECONDARY: derived (DERIVED)
ALLOWED WORDING: roughly 450 thousand steps — our arithmetic from the paper's numbers
WHAT THE NUMBER DOES NOT MEAN: n/a
```

### DER-004
```text
NUMBER(S): 671B, 1 , ~671 GB, 80 GB
CLAIM: 671B parameters at 1 byte (FP8) is ~671 GB, more than eight 80 GB GPUs just to hold V3's weights.
SOURCE: derived from V3-001, EXP-006
MODEL: DeepSeek-V3
PAGE/SECTION/TABLE: our arithmetic
PRIMARY OR SECONDARY: derived (DERIVED)
ALLOWED WORDING: just storing the weights needs more than eight GPUs' worth of memory
WHAT THE NUMBER DOES NOT MEAN: n/a
```

### DER-005
```text
NUMBER(S): ~2 , 37B, 74 
CLAIM: ~2 FLOPs x 37B active parameters ~= 74 billion operations per token for a V3 forward pass (rule of thumb).
SOURCE: derived from GEN-003, V3-001
MODEL: DeepSeek-V3
PAGE/SECTION/TABLE: our arithmetic
PRIMARY OR SECONDARY: derived (DERIVED)
ALLOWED WORDING: roughly 74 billion operations for every single token — a rule-of-thumb estimate
WHAT THE NUMBER DOES NOT MEAN: DeepSeek reported 74 GFLOPs per token.
```

### DER-006
```text
NUMBER(S): 7168 x, 7168 , 7168, 2 , 51,380,224 
CLAIM: One 7168 x 7168 matrix (V3 hidden size) times a vector is 7168^2 = 51,380,224 multiplications.
SOURCE: derived from V3-008
MODEL: DeepSeek-V3
PAGE/SECTION/TABLE: our arithmetic
PRIMARY OR SECONDARY: derived (DERIVED)
ALLOWED WORDING: about 51 million multiplications for one token through one square matrix
WHAT THE NUMBER DOES NOT MEAN: n/a
```

### DER-007
```text
NUMBER(S): 37, 671 , 5.5%
CLAIM: V3 active fraction: 37/671 ~= 5.5%.
SOURCE: derived from V3-001
MODEL: DeepSeek-V3
PAGE/SECTION/TABLE: our arithmetic
PRIMARY OR SECONDARY: derived (DERIVED)
ALLOWED WORDING: about 5.5 percent of the model is active for a given token
WHAT THE NUMBER DOES NOT MEAN: n/a
```

### V3-012
```text
NUMBER(S): 
CLAIM: DeepSeek reports V3 outperforms other open-source models and achieves performance comparable to leading closed-source models.
SOURCE: V3_README
MODEL: DeepSeek-V3
PAGE/SECTION/TABLE: README §1
PRIMARY OR SECONDARY: primary (self-reported) (VERIFIED_PRIMARY)
ALLOWED WORDING: by their own benchmarks, comparable to leading closed models
WHAT THE NUMBER DOES NOT MEAN: V3 beat GPT-4 / is the best model in the world.
```

### V41-017
```text
NUMBER(S): 
CLAIM: V4.1-Flash extends auxiliary-loss-free load balancing with separate expert-wise correction biases for text and image tokens.
SOURCE: V41_PAPER
MODEL: DeepSeek-V4.1-Flash
PAGE/SECTION/TABLE: §2.1.1
PRIMARY OR SECONDARY: primary (VERIFIED_PRIMARY)
ALLOWED WORDING: separate nudges for text and for images
WHAT THE NUMBER DOES NOT MEAN: n/a
```

### V41-021
```text
NUMBER(S): 2 , 1 , 1.
CLAIM: Encoder CSA2 layers use compression rate m=2 (every 2 tokens -> 1 entry); decoder uses m=1.
SOURCE: V41_PAPER
MODEL: DeepSeek-V4.1-Flash
PAGE/SECTION/TABLE: §4.2.1
PRIMARY OR SECONDARY: primary (VERIFIED_PRIMARY)
ALLOWED WORDING: early layers merge neighbouring tokens into shared entries
WHAT THE NUMBER DOES NOT MEAN: n/a
```

### V41-022
```text
NUMBER(S): 2 , 3 , 6 , 1 , 5 , 4 
CLAIM: Encoder: 2 SWA layers then 3 groups of 6 (1 Full + 5 Reuse); decoder: 5 groups of 4 (first group Full+3 Reuse; others Reindex+3 Reuse).
SOURCE: V41_PAPER
MODEL: DeepSeek-V4.1-Flash
PAGE/SECTION/TABLE: §4.2.1
PRIMARY OR SECONDARY: primary (VERIFIED_PRIMARY)
ALLOWED WORDING: groups of six in the encoder, groups of four in the decoder
WHAT THE NUMBER DOES NOT MEAN: n/a
```

### V41-023
```text
NUMBER(S): 
CLAIM: Despite much smaller KV cache, V4.1-Flash delivers substantially better performance than DeepSeek-V4-Flash (self-reported).
SOURCE: V41_PAPER
MODEL: DeepSeek-V4.1-Flash
PAGE/SECTION/TABLE: Abstract; §6
PRIMARY OR SECONDARY: primary (self-reported) (VERIFIED_PRIMARY)
ALLOWED WORDING: DeepSeek reports it performs substantially better than its predecessor, on their own evaluations
WHAT THE NUMBER DOES NOT MEAN: Independently verified to be better.
```

### GEN-005
```text
NUMBER(S): ≈2, 3 
CLAIM: In large Transformers most parameters sit in the feed-forward (MLP) matrices (≈2/3 in standard dense designs; more in MoE).
SOURCE: standard architecture accounting (e.g. Kaplan et al. 2020)
MODEL: n/a
PAGE/SECTION/TABLE: parameter accounting
PRIMARY OR SECONDARY: secondary (VERIFIED_SECONDARY)
ALLOWED WORDING: most of the parameters live in the feed-forward matrices
WHAT THE NUMBER DOES NOT MEAN: n/a
```

### GEN-007
```text
NUMBER(S): 1991, 2017, 2014, 2018
CLAIM: Mixture-of-Experts (Jacobs et al. 1991; Shazeer et al. 2017), attention (Bahdanau 2014; Vaswani 2017) and reduced-precision training (Micikevicius et al. 2018) predate DeepSeek.
SOURCE: literature
MODEL: n/a
PAGE/SECTION/TABLE: citations
PRIMARY OR SECONDARY: primary (papers) (VERIFIED_SECONDARY)
ALLOWED WORDING: these ideas existed before DeepSeek
WHAT THE NUMBER DOES NOT MEAN: DeepSeek invented MoE / attention / low precision.
```
