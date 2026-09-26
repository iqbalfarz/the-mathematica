# Architecture map (what each idea attacks)

| Wall | Idea | Model | What it changes | Claim |
|---|---|---|---|---|
| Compute | Mixture of Experts (fine-grained routed + shared experts) | V2, V3, V4.1 | active params ≪ total (37B/671B; 16B/552B decode) | V3-001, V41-002 |
| Compute | Causal Encoder-Decoder | V4.1 | prefill ≈ halved; 8B active in prefill | V41-010, V41-002 |
| Compute | Sparse attention: indexer + top-512 | V3.2→V4.1 | per-token attention work bounded | V41-008, V41-011 |
| Communication | DualPipe compute/comm overlap | V3 | hides all-to-all latency | V3-011 |
| Communication + compute | FP8 mixed precision | V3 | half the bytes of 16-bit | V3-006 |
| Memory (entry size) | MLA latent KV | V2, V3 | 576 vs ~32,768 numbers/token/layer | V3-009/010, V2-002 |
| Memory (entry size) | FP4 main KV cache | V4.1 | ≈ half of FP8 storage | V41-009 |
| Memory (sequence) | Compression m=2 + SWA window 128 | V4.1 | fewer entries per sequence | V41-021, V41-006 |
| Memory (layers) | CSA2 cross-layer KV/index reuse | V4.1 | most layers keep no own global KV | V41-008, V41-022 |
| Memory (persistent) | SWA Bounded Replay | V4.1 | persistent KV ≈ ⅛ | V41-005 |

Dependency graph taught in the film:
multiply → dot product → matrix multiply → parameters → FLOPs → GPU parallelism → memory/bandwidth → tokens/embeddings → Q·K·V attention → softmax → heads/FFN/stack → scaling cost → MoE/router/top-k → load balancing → all-to-all communication → overlap + FP8 → autoregressive decode → KV cache → MLA → three dials → sparse attention → CSA2 reuse → FP4 → CED prefill → loss → gradient descent → training loop → the numbers → synthesis.
