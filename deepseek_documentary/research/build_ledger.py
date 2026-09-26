"""Single source of truth for the claim ledger. Run to regenerate claim_ledger.csv.

Status values:
  VERIFIED_PRIMARY     read directly in a primary source (paper PDF, official README/config, SEC filing)
  PRIMARY_EXCERPT      primary-source wording confirmed via quoted excerpt (full text fetch blocked in build env)
  VERIFIED_SECONDARY   reputable secondary source (CSET, CSIS, CRS, law-firm analyses)
  DERIVED              our own arithmetic from verified numbers (shown on screen as such)
"""
import csv, pathlib

COLS = ["claim_id", "claim", "source", "source_type", "date", "model_version", "location",
        "confidence", "status", "allowed_wording", "forbidden_overstatement"]

R = [
# ---------------- export controls ----------------
("EXP-001", "Oct 2022 US rules restricted export to China of top AI chips such as NVIDIA A100 and H100; one control criterion was chip-to-chip interconnect of 600 GB/s or more.",
 "COVINGTON_2022; EPOCH_EXPORT; BIS_2023", "secondary+primary page", "2022-10-07", "n/a", "ECCN 3A090 summary", "high", "VERIFIED_SECONDARY",
 "In October 2022 the US restricted exports of top AI chips like the A100 and H100 to China.", "China was cut off from all GPUs / all NVIDIA chips."),
("EXP-002", "NVIDIA created China-specific A800 and H800 chips with reduced interconnect bandwidth to fall under the 2022 thresholds.",
 "CSET_2023; EPOCH_EXPORT", "secondary", "2023", "n/a", "explainer", "high", "VERIFIED_SECONDARY",
 "NVIDIA responded with China versions, the A800 and H800, with slower chip-to-chip links.", "The H800 is a weak or slow chip overall."),
("EXP-003", "The October 17, 2023 BIS update switched to performance / performance-density criteria and captured the A800 and H800.",
 "CSET_2023; CSIS_2023; BIS_2023", "secondary+primary page", "2023-10-17", "n/a", "explainer", "high", "VERIFIED_SECONDARY",
 "In October 2023 the rules were tightened, and the H800 itself was restricted.", "DeepSeek used banned / smuggled chips."),
("EXP-004", "On April 9, 2025 NVIDIA was told a licence is required to export H20 to China; on April 14 it was told this applies for the indefinite future.",
 "NVDA_8K_2025_04", "primary (SEC filing)", "2025-04-09", "n/a", "Form 8-K Item 8.01", "high", "VERIFIED_PRIMARY",
 "In April 2025 even the H20, a chip designed for the Chinese market, required a US export licence.", "H20 was permanently banned."),
("EXP-005", "H800 NVLink bandwidth is reduced relative to H100 (widely reported ~400 GB/s vs 900 GB/s); compute cores and memory essentially unchanged.",
 "EPOCH_EXPORT; vendor spec summaries", "secondary", "2023", "n/a", "spec comparisons", "medium", "VERIFIED_SECONDARY",
 "Same engine, narrower pipes: the H800 kept its compute but its GPU-to-GPU links were cut — widely reported as about 400 versus 900 gigabytes per second.", "Exact figure stated as official NVIDIA specification."),
# ---------------- DeepSeek-V2 ----------------
("V2-001", "DeepSeek-V2 has 236B total parameters with 21B activated per token.", "V3_README (table); V2_REPORT", "primary", "2024-05", "DeepSeek-V2", "README comparison table", "high", "VERIFIED_PRIMARY",
 "DeepSeek-V2: 236 billion parameters, about 21 billion active per token.", ""),
("V2-002", "MLA reduced KV cache by 93.3% relative to DeepSeek 67B.", "V2_REPORT", "primary", "2024-05", "DeepSeek-V2", "Abstract", "high", "PRIMARY_EXCERPT",
 "DeepSeek reported that MLA cut the KV cache by 93.3 percent compared with their earlier 67-billion-parameter model.", "MLA invented KV-cache compression / reduces all memory 93%."),
# ---------------- DeepSeek-V3 ----------------
("V3-001", "DeepSeek-V3 has 671B total parameters, 37B activated per token.", "V3_README", "primary", "2024-12", "DeepSeek-V3", "README §1", "high", "VERIFIED_PRIMARY",
 "671 billion parameters in total — but only 37 billion active for any one token.", "V3 uses 37B parameters total."),
("V3-002", "DeepSeek-V3 was pre-trained on 14.8T tokens.", "V3_README", "primary", "2024-12", "DeepSeek-V3", "README §1-2", "high", "VERIFIED_PRIMARY",
 "trained on 14.8 trillion tokens", ""),
("V3-003", "Full training of DeepSeek-V3 required 2.788M H800 GPU hours: 2.664M pre-training + 119K context extension + 5K post-training.", "V3_README; V3_REPORT", "primary", "2024-12", "DeepSeek-V3", "README §1-2; report Table 1", "high", "VERIFIED_PRIMARY",
 "DeepSeek reports 2.788 million H800 GPU-hours for the full training run.", "The whole of DeepSeek cost 2.788M GPU hours."),
("V3-004", "Training used a cluster of 2,048 NVIDIA H800 GPUs; each trillion tokens took 180K GPU hours, i.e. 3.7 days.", "V3_REPORT", "primary", "2024-12", "DeepSeek-V3", "Abstract/§1 & §3.1", "high", "PRIMARY_EXCERPT",
 "a cluster of 2,048 H800s; each trillion tokens took about 3.7 days", ""),
("V3-005", "Assuming $2 per H800 GPU hour rental, the official training run costs $5.576M; this excludes prior research and ablation experiments.", "V3_REPORT", "primary", "2024-12", "DeepSeek-V3", "§1 Table 1 and following text", "high", "PRIMARY_EXCERPT",
 "At an assumed rental price of $2 per GPU-hour, DeepSeek estimated the final run at about $5.6 million — and explicitly excluded research, experiments, staff and hardware.", "DeepSeek built its AI for $5.6 million. / Total cost of DeepSeek was $5.6M."),
("V3-006", "DeepSeek-V3 used an FP8 mixed-precision training framework, validated at extremely large scale for the first time (per DeepSeek).", "V3_README", "primary", "2024-12", "DeepSeek-V3", "README §2", "high", "VERIFIED_PRIMARY",
 "DeepSeek says V3 was the first to validate FP8 training at this scale.", "FP8 was invented by DeepSeek."),
("V3-007", "DeepSeek-V3 adopts MLA and DeepSeekMoE, validated in DeepSeek-V2.", "V3_README", "primary", "2024-12", "DeepSeek-V3", "README §1", "high", "VERIFIED_PRIMARY",
 "V3 reuses two ideas proven in V2: Multi-head Latent Attention and DeepSeekMoE.", ""),
("V3-008", "V3 MoE layers: 256 routed experts + 1 shared expert, 8 routed experts activated per token; 61 layers; hidden dim 7168; 128 heads.", "V3 inference/configs/config_671B.json", "primary (official config)", "2024-12", "DeepSeek-V3", "config_671B.json", "high", "VERIFIED_PRIMARY",
 "256 routed experts plus one shared expert per layer; each token visits 8 of the 256.", ""),
("V3-009", "V3's MLA caches a 512-dim compressed KV latent plus a 64-dim positional key per token per layer (kv_lora_rank 512, qk_rope_head_dim 64).", "V3 config_671B.json", "primary (official config)", "2024-12", "DeepSeek-V3", "config_671B.json", "high", "VERIFIED_PRIMARY",
 "Instead of full keys and values for every head, V3 stores one 512-number summary plus a 64-number position key.", ""),
("V3-010", "Standard multi-head attention with V3's shape (128 heads, 128-dim K and V) would cache 2x128x128 = 32,768 numbers per token per layer vs 576 for MLA (~57x fewer).", "derived from V3-008, V3-009", "derived", "2024-12", "DeepSeek-V3", "our arithmetic", "high", "DERIVED",
 "If V3 had used ordinary attention, a quick calculation from its published shape gives about 32 thousand numbers per token per layer; MLA stores 576.", "DeepSeek reports a 57x reduction."),
("V3-011", "DualPipe overlaps computation and all-to-all communication in cross-node MoE training; custom kernels use InfiniBand across nodes and NVLink within nodes.", "V3_REPORT", "primary", "2024-12", "DeepSeek-V3", "§3.2", "high", "PRIMARY_EXCERPT",
 "DeepSeek built a pipeline schedule, DualPipe, so that GPUs compute while tokens are in flight.", "Communication cost is zero."),
# ---------------- DeepSeek-V4.1-Flash (supplied paper) ----------------
("V41-001", "DeepSeek-V4.1-Flash is a multimodal MoE model with 552B backbone parameters (plus 196B Engram parameters), up to 1M-token context.", "V41_PAPER", "primary", "2026-09-17", "DeepSeek-V4.1-Flash", "Abstract; §2.1", "high", "VERIFIED_PRIMARY",
 "552 billion backbone parameters, contexts up to a million tokens.", "552B total parameters (omits Engram) / V4.1 has 748B active."),
("V41-002", "Activates 8B parameters per token during prefill and 16B during decode (Causal Encoder-Decoder).", "V41_PAPER", "primary", "2026-09-17", "DeepSeek-V4.1-Flash", "Abstract; §2.1; §4.2.1", "high", "VERIFIED_PRIMARY",
 "about 16 billion active while writing, only 8 billion while reading the prompt", ""),
("V41-003", "Global KV cache footprint is 890 bytes per token, roughly 1/4 of DeepSeek-V4-Flash.", "V41_PAPER", "primary", "2026-09-17", "DeepSeek-V4.1-Flash", "Abstract; Fig. 1b", "high", "VERIFIED_PRIMARY",
 "890 bytes of global memory per token — about a quarter of its predecessor.", "Total memory per token is 890 bytes (excludes SWA KV)."),
("V41-004", "Fig. 1b global KV cache per token: DeepSeek-V1 389,120 B (2023.11); V3.2 48,068 B (2025.12); V4-Flash 3,514 B (2026.04); V4.1-Flash 890 B (2026.09). ~437x vs V1.", "V41_PAPER", "primary", "2026-09-17", "V1, V3.2, V4-Flash, V4.1-Flash", "Figure 1(b)", "high", "VERIFIED_PRIMARY",
 "DeepSeek's own chart: from about 389 thousand bytes per token in their first model to 890 — roughly 437 times smaller.", "Numbers presented as independent measurements."),
("V41-005", "Persistent KV cache (SSD/host memory) reduced to roughly 1/8 of V4-Flash via SWA Bounded Replay.", "V41_PAPER", "primary", "2026-09-17", "DeepSeek-V4.1-Flash", "Abstract; §3.2.2", "high", "VERIFIED_PRIMARY",
 "the long-term stored cache shrinks to about an eighth", ""),
("V41-006", "Architecture: 40 layers = 20-layer causal encoder + 20-layer decoder; hidden dim 5120; first two layers SWA-only; SWA window 128.", "V41_PAPER", "primary", "2026-09-17", "DeepSeek-V4.1-Flash", "§2.1; §4.2.1", "high", "VERIFIED_PRIMARY",
 "40 layers, split into a 20-layer encoder and a 20-layer decoder", ""),
("V41-007", "Each MoE layer has 1 shared expert and 384 routed experts; 6 routed experts activated per token.", "V41_PAPER", "primary", "2026-09-17", "DeepSeek-V4.1-Flash", "§4.2.1", "high", "VERIFIED_PRIMARY",
 "384 routed experts per layer, 6 chosen per token, plus one shared expert", ""),
("V41-008", "CSA2 selects top-512 KV entries per query via a lightweight indexer; layers run in Full, Reindex, or Reuse mode sharing global KV across layers.", "V41_PAPER", "primary", "2026-09-17", "DeepSeek-V4.1-Flash", "§2.3; §4.2.1; Fig. 4", "high", "VERIFIED_PRIMARY",
 "a small indexer picks the 512 most relevant memories; later layers reuse the same memory instead of storing their own", ""),
("V41-009", "Main KV cache stored in FP4 (E2M1 values with an E4M3 scale per 16 channels); SWA KV kept in FP8; nearly halves storage vs V4's FP8 main KV.", "V41_PAPER", "primary", "2026-09-17", "DeepSeek-V4.1-Flash", "§2.4.4", "high", "VERIFIED_PRIMARY",
 "the main memory is stored in 4-bit numbers, with one shared scale for every 16 values", ""),
("V41-010", "CED reduces prefill from O(NL) to ~O(NL/2): decoder global KV is projected from the final encoder hidden state, nearly halving prefill computation.", "V41_PAPER", "primary", "2026-09-17", "DeepSeek-V4.1-Flash", "§2.2 Eq.1", "high", "VERIFIED_PRIMARY",
 "reading a prompt costs roughly half the computation", ""),
("V41-011", "Extending context 256-fold from 4K to 1M increases V4.1-Flash single-token decode FLOPs by only about 1/4.", "V41_PAPER", "primary", "2026-09-17", "DeepSeek-V4.1-Flash", "§1; Fig. 2", "high", "VERIFIED_PRIMARY",
 "going from 4 thousand to a million tokens of context raises the cost of each new token by only about a quarter", "Cost is constant / independent of context."),
("V41-012", "Pre-trained on 45T multimodal tokens; batch 100.6M tokens; sparse attention from scratch at 64K sequence length, extended to 1M at 34T tokens.", "V41_PAPER", "primary", "2026-09-17", "DeepSeek-V4.1-Flash", "§4.2.2", "high", "VERIFIED_PRIMARY",
 "45 trillion tokens, about a hundred million tokens per training step", ""),
("V41-013", "Post-training introduces no algorithmic innovation (SFT, RL, on-policy distillation); changes lie in the data pipeline.", "V41_PAPER", "primary", "2026-09-17", "DeepSeek-V4.1-Flash", "§1", "high", "VERIFIED_PRIMARY",
 "DeepSeek itself says the post-training recipe is standard; the new ideas are in architecture and systems.", ""),
("V41-014", "Paper reports no GPU type, GPU count, GPU-hours, or training cost for V4.1-Flash.", "V41_PAPER", "primary (absence)", "2026-09-17", "DeepSeek-V4.1-Flash", "whole paper searched", "high", "VERIFIED_PRIMARY",
 "The paper does not say what hardware trained V4.1-Flash, or what it cost.", "Any V4.1 GPU count or cost figure."),
("V41-015", "Limitations: CSA2 selection errors and approximate SWA state reconstruction may degrade untested boundary cases.", "V41_PAPER", "primary", "2026-09-17", "DeepSeek-V4.1-Flash", "§6", "high", "VERIFIED_PRIMARY",
 "DeepSeek flags its own risks: the selector can pick wrong, and approximate replay may fail on edge cases.", ""),
("V41-016", "The FP4 format choice (OCP MXFP4 for indexer; NVFP4-like for main KV) is made partly for compatibility across hardware platforms.", "V41_PAPER", "primary", "2026-09-17", "DeepSeek-V4.1-Flash", "§2.4.4", "high", "VERIFIED_PRIMARY",
 "DeepSeek chose number formats that work across many hardware platforms", "DeepSeek designed its own chips."),
# ---------------- general / textbook ----------------
("GEN-001", "Scaled dot-product attention: softmax(QK^T / sqrt(d)) V.", "VASWANI_2017", "primary", "2017", "n/a", "Eq. 1", "high", "VERIFIED_PRIMARY",
 "Attention(Q,K,V) = softmax(QK^T / sqrt(d)) V", ""),
("GEN-002", "Multiplying an (m x n) by (n x p) matrix takes m*n*p multiply-adds (~2mnp FLOPs).", "textbook", "derived", "n/a", "n/a", "definition", "high", "DERIVED",
 "a 3x3 times 3x3 product needs 27 multiplications", ""),
("GEN-003", "A dense forward pass costs roughly 2 FLOPs per active parameter per token.", "standard scaling-law approximation (Kaplan et al. 2020)", "secondary", "2020", "n/a", "approximation", "medium", "VERIFIED_SECONDARY",
 "a useful rule of thumb: about two operations per active parameter, per token", "Exact FLOP counts for DeepSeek models."),
("GEN-004", "Training costs roughly 6 FLOPs per active parameter per token (forward + backward).", "standard approximation", "secondary", "2020", "n/a", "approximation", "medium", "VERIFIED_SECONDARY",
 "training is roughly three times a forward pass", "Exact DeepSeek FLOP totals."),
("DER-001", "6 x 37e9 x 14.8e12 ~= 3.3e24 FLOPs: a rough estimate of V3 pre-training compute using GEN-004.", "derived from V3-001, V3-002, GEN-004", "derived", "n/a", "DeepSeek-V3", "our arithmetic", "medium", "DERIVED",
 "a back-of-envelope estimate: about 3 times 10 to the 24 operations — our estimate, not DeepSeek's figure", "DeepSeek reported 3.3e24 FLOPs."),
("EXP-006", "The H800 carries 80 GB of HBM memory, like the H100 SXM.", "vendor spec summaries", "secondary", "2023", "n/a", "spec comparisons", "medium", "VERIFIED_SECONDARY",
 "each H800 holds 80 gigabytes of fast memory", ""),
("DER-002", "With V3's shape but ordinary multi-head attention (61 layers x 32,768 cached numbers x 2 bytes BF16), KV cache would be ~4.0 MB per token, ~524 GB at 128K tokens.", "derived from V3-008, V3-010", "derived", "n/a", "DeepSeek-V3 (hypothetical MHA)", "our arithmetic", "high", "DERIVED",
 "a hypothetical: if V3 had used ordinary attention, a quick calculation gives about 4 megabytes of memory per token", "DeepSeek reported 4 MB per token."),
("DER-003", "45T tokens / 100.6M tokens per step ~= 447 thousand optimizer steps for V4.1-Flash pre-training (ignoring warmup detail).", "derived from V41-012", "derived", "n/a", "DeepSeek-V4.1-Flash", "our arithmetic", "high", "DERIVED",
 "roughly 450 thousand steps — our arithmetic from the paper's numbers", ""),
("DER-004", "671B parameters at 1 byte (FP8) is ~671 GB, more than eight 80 GB GPUs just to hold V3's weights.", "derived from V3-001, EXP-006", "derived", "n/a", "DeepSeek-V3", "our arithmetic", "high", "DERIVED",
 "just storing the weights needs more than eight GPUs' worth of memory", ""),
("DER-005", "~2 FLOPs x 37B active parameters ~= 74 billion operations per token for a V3 forward pass (rule of thumb).", "derived from GEN-003, V3-001", "derived", "n/a", "DeepSeek-V3", "our arithmetic", "medium", "DERIVED",
 "roughly 74 billion operations for every single token — a rule-of-thumb estimate", "DeepSeek reported 74 GFLOPs per token."),
("DER-006", "One 7168 x 7168 matrix (V3 hidden size) times a vector is 7168^2 = 51,380,224 multiplications.", "derived from V3-008", "derived", "n/a", "DeepSeek-V3", "our arithmetic", "high", "DERIVED",
 "about 51 million multiplications for one token through one square matrix", ""),
("DER-007", "V3 active fraction: 37/671 ~= 5.5%.", "derived from V3-001", "derived", "n/a", "DeepSeek-V3", "our arithmetic", "high", "DERIVED",
 "about 5.5 percent of the model is active for a given token", ""),
("V3-012", "DeepSeek reports V3 outperforms other open-source models and achieves performance comparable to leading closed-source models.", "V3_README", "primary (self-reported)", "2024-12", "DeepSeek-V3", "README §1", "high", "VERIFIED_PRIMARY",
 "by their own benchmarks, comparable to leading closed models", "V3 beat GPT-4 / is the best model in the world."),
("V41-017", "V4.1-Flash extends auxiliary-loss-free load balancing with separate expert-wise correction biases for text and image tokens.", "V41_PAPER", "primary", "2026-09-17", "DeepSeek-V4.1-Flash", "§2.1.1", "high", "VERIFIED_PRIMARY",
 "separate nudges for text and for images", ""),
("V41-018", "KV cost reduces along three multiplicative dimensions: entry size, sequence dimension, layer dimension.", "V41_PAPER", "primary", "2026-09-17", "DeepSeek-V4.1-Flash", "§2.3", "high", "VERIFIED_PRIMARY",
 "the cache is three numbers multiplied together", ""),
("V41-019", "Long-horizon agents have made workloads increasingly input-heavy.", "V41_PAPER", "primary", "2026-09-17", "DeepSeek-V4.1-Flash", "Abstract", "high", "VERIFIED_PRIMARY",
 "DeepSeek describes these workloads as increasingly input heavy", ""),
("V41-020", "Prior sparse attention reduced long-sequence compute, making persistent storage and data movement increasingly prominent bottlenecks.", "V41_PAPER", "primary", "2026-09-17", "DeepSeek-V4.1-Flash", "§1", "high", "VERIFIED_PRIMARY",
 "storage and data movement became the prominent bottlenecks", "Compute is no longer a cost."),
("V41-021", "Encoder CSA2 layers use compression rate m=2 (every 2 tokens -> 1 entry); decoder uses m=1.", "V41_PAPER", "primary", "2026-09-17", "DeepSeek-V4.1-Flash", "§4.2.1", "high", "VERIFIED_PRIMARY",
 "early layers merge neighbouring tokens into shared entries", ""),
("V41-022", "Encoder: 2 SWA layers then 3 groups of 6 (1 Full + 5 Reuse); decoder: 5 groups of 4 (first group Full+3 Reuse; others Reindex+3 Reuse).", "V41_PAPER", "primary", "2026-09-17", "DeepSeek-V4.1-Flash", "§4.2.1", "high", "VERIFIED_PRIMARY",
 "groups of six in the encoder, groups of four in the decoder", ""),
("V41-023", "Despite much smaller KV cache, V4.1-Flash delivers substantially better performance than DeepSeek-V4-Flash (self-reported).", "V41_PAPER", "primary (self-reported)", "2026-09-17", "DeepSeek-V4.1-Flash", "Abstract; §6", "high", "VERIFIED_PRIMARY",
 "DeepSeek reports it performs substantially better than its predecessor, on their own evaluations", "Independently verified to be better."),
("GEN-005", "In large Transformers most parameters sit in the feed-forward (MLP) matrices (≈2/3 in standard dense designs; more in MoE).", "standard architecture accounting (e.g. Kaplan et al. 2020)", "secondary", "n/a", "n/a", "parameter accounting", "high", "VERIFIED_SECONDARY",
 "most of the parameters live in the feed-forward matrices", ""),
("GEN-007", "Mixture-of-Experts (Jacobs et al. 1991; Shazeer et al. 2017), attention (Bahdanau 2014; Vaswani 2017) and reduced-precision training (Micikevicius et al. 2018) predate DeepSeek.", "literature", "primary (papers)", "1991-2018", "n/a", "citations", "high", "VERIFIED_SECONDARY",
 "these ideas existed before DeepSeek", "DeepSeek invented MoE / attention / low precision."),
]

out = pathlib.Path(__file__).with_name("claim_ledger.csv")
with out.open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(COLS)
    for r in R:
        assert len(r) == len(COLS), r[0]
        w.writerow(r)
print(f"wrote {len(R)} claims -> {out}")

# Number ledger: every claim that carries a number, in the record format used for review.
import re
NUM_RE = r"(?<![A-Za-z\d.])[~≈]?\d[\d,.]*\s?(?:[BTMK]|GB|MB|%|x)?"
lines = ["# Number ledger", "", "Generated from `build_ledger.py`. One record per quantitative claim.", ""]
for r in R:
    rec = dict(zip(COLS, r))
    if not re.search(r"\d", rec["claim"]):
        continue
    nums = ", ".join(dict.fromkeys(re.findall(NUM_RE, rec["claim"])))
    lines += [f"### {rec['claim_id']}", "```text",
              f"NUMBER(S): {nums}",
              f"CLAIM: {rec['claim']}",
              f"SOURCE: {rec['source']}",
              f"MODEL: {rec['model_version']}",
              f"PAGE/SECTION/TABLE: {rec['location']}",
              f"PRIMARY OR SECONDARY: {rec['source_type']} ({rec['status']})",
              f"ALLOWED WORDING: {rec['allowed_wording']}",
              f"WHAT THE NUMBER DOES NOT MEAN: {rec['forbidden_overstatement'] or 'n/a'}",
              "```", ""]
out.with_name("number_ledger.md").write_text("\n".join(lines))
print("wrote number_ledger.md")
