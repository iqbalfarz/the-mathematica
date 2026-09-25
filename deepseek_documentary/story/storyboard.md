# Storyboard

One entry per scene. Each scene is one Manim class in `src/docu/scenes/actNN.py`, rendered to `scene_NNN.mp4`. Every beat's visual intent is listed under the narration it serves.


## SCENE 001 · s0101 · Buy more GPUs

| Field | Value |
|---|---|
| Time | 00:00–00:19 |
| Act | 1 — The Impossible Constraint |
| Manim class | `docu.scenes.act01.S0101ColdOpen` |
| Output | `scene_001.mp4` |
| Claims | — (conceptual / pedagogical only) |
| Sources | — |
| Audio | music: tension; SFX: hum, pulse |
| Loop opened | — |
| Loop closed | — |

- **b1** — *For years, the race to build better AI looked almost embarrassingly simple.*  
  → Black. A single small GPU block fades in at centre and hums.
- **b2** — *Want a smarter model? Buy more GPUs.*  
  → The block multiplies into a row, then a grid of dozens.
- **b3** — *Want it smarter still? Build a bigger data centre. Spend more money.*  
  → Grid explodes to hundreds of blocks; camera pulls back; a pulse of light sweeps across them.
- **b4** — *Better intelligence, it seemed, was mostly a shopping problem.*  
  → The wall of GPUs glows steadily. A thin price-tag label ticks upward.

## SCENE 002 · s0102 · Then the rules changed

| Field | Value |
|---|---|
| Time | 00:19–01:05 |
| Act | 1 — The Impossible Constraint |
| Manim class | `docu.scenes.act01.S0102RulesChanged` |
| Output | `scene_002.mp4` |
| Claims | EXP-001, EXP-002, EXP-003, EXP-004 |
| Sources | COVINGTON_2022; EPOCH_EXPORT; BIS_2023 (ECCN 3A090 summary); CSET_2023; CSIS_2023; BIS_2023 (explainer); CSET_2023; EPOCH_EXPORT (explainer); NVDA_8K_2025_04 (Form 8-K Item 8.01) |
| Audio | music: tension; SFX: impact |
| Loop opened | — |
| Loop closed | — |

- **b1** — *Then the rules changed.*  
  → CUT TO BLACK. Silence. A timeline line draws across the screen.
- **b2** — *In October 2022, the United States restricted exports of the most powerful AI chips, like NVIDIA's A100 and H100, to China.*  
  → Marker 'Oct 2022'. Chip cards A100 and H100 slide in, then receive a red 'restricted' bar.
- **b3** — *NVIDIA answered with China versions, the A800 and the H800. Nearly the same chips, but with slower connections between them.*  
  → Cards A800 and H800 appear under the timeline, their link-lines drawn thinner.
- **b4** — *A year later, in October 2023, the rules were tightened again, and the H800 itself was restricted.*  
  → Marker 'Oct 2023'. H800 and A800 receive red bars.
- **b5** — *And by April 2025, even the H20, a chip built specifically for the Chinese market, needed a US export licence.*  
  → Marker 'Apr 2025'. H20 card appears and is flagged 'licence required'. Source line fades in at bottom.

## SCENE 003 · s0103 · What if you can't buy your way out?

| Field | Value |
|---|---|
| Time | 01:05–02:15 |
| Act | 1 — The Impossible Constraint |
| Manim class | `docu.scenes.act01.S0103TheQuestion` |
| Output | `scene_003.mp4` |
| Claims | V3-003, V3-004, V3-012, V41-003 |
| Sources | V3_README (README §1); V3_README; V3_REPORT (README §1-2; report Table 1); V3_REPORT (Abstract/§1 & §3.1); V41_PAPER (Abstract; Fig. 1b) |
| Audio | music: tension; SFX: whoosh |
| Loop opened | L1, L9 |
| Loop closed | — |

- **b1** — *In the middle of all this, a Chinese lab called DeepSeek published a model called DeepSeek V3.*  
  → Timeline shrinks to the top. A clean model card 'DeepSeek-V3 · Dec 2024' fades in.
- **b2** — *They reported training it on a cluster of 2,048 H800s, the very chip that had been designed to sit just under the line.*  
  → The card fills: 2,048 H800 GPUs. A small grid of 2,048 dots materialises beside it.
- **b3** — *The full training run, they said, took about 2.8 million GPU hours. And, by their own benchmarks, the model it produced was comparable to le…*  
  → Line '2.788M H800 GPU-hours (reported)'. Tag 'reported by DeepSeek' in small caps.
- **b4** — *People called it impossible. It wasn't. But it was surprising. And the reason it was surprising is the whole story.*  
  → The word IMPOSSIBLE appears large, then is crossed and replaced by SURPRISING.
- **b5** — *Because the real question isn't how many chips they had. It's this. What do you do when you can't simply buy your way out of a problem?*  
  → Everything clears. The central question types itself onto the screen and stays.
- **b6** — *Less than two years later, DeepSeek published another paper, about a different wall entirely. Memory. They got one number down to 890 bytes.…*  
  → Question moves to top as a small persistent title. Big '890 bytes' appears with a '?' — then shrinks into the corner.
- **b7** — *But to get there, we have to start at the very bottom. With a single multiplication.*  
  → Everything collapses into a single glowing dot at the centre.

## SCENE 004 · s0201 · One multiplication

| Field | Value |
|---|---|
| Time | 02:15–02:56 |
| Act | 2 — What Does Compute Even Mean? |
| Manim class | `docu.scenes.act02.S0201OneMultiplication` |
| Output | `scene_004.mp4` |
| Claims | — (conceptual / pedagogical only) |
| Sources | — |
| Audio | music: curious; SFX: none |
| Loop opened | L2 |
| Loop closed | — |

- **b1** — *Here is the most important operation in all of modern AI.*  
  → The dot becomes the expression 3 × 4.
- **b2** — *Three times four. Twelve. That's it. One multiplication.*  
  → 3 × 4 transforms into = 12. A small counter '1 operation' appears.
- **b3** — *Now let's give those numbers jobs. Suppose the three is a piece of information coming in, an input. And the four is how much we care about i…*  
  → 3 gets a label 'input x', 4 gets 'weight w'. Colours shift to input-blue and parameter-amber.
- **b4** — *A neuron, in an artificial neural network, is barely more than this. It takes several inputs, multiplies each one by its own weight, and add…*  
  → Three inputs on the left flow into a circle through three weighted edges; products appear on edges and sum into the neuron.
- **b5** — *Those weights are what people mean when they say a model has parameters. Every parameter is just one number, one of these weights.*  
  → The weights glow amber; label 'parameters = the weights'.

## SCENE 005 · s0202 · Multiply, add, repeat

| Field | Value |
|---|---|
| Time | 02:56–03:30 |
| Act | 2 — What Does Compute Even Mean? |
| Manim class | `docu.scenes.act02.S0202DotProduct` |
| Output | `scene_005.mp4` |
| Claims | — (conceptual / pedagogical only) |
| Sources | — |
| Audio | music: curious; SFX: none |
| Loop opened | — |
| Loop closed | — |

- **b1** — *Line the inputs up in a column, line the weights up in a row, and this whole neuron becomes one tidy operation.*  
  → The neuron diagram morphs into a row vector w and a column vector x.
- **b2** — *Multiply the first pair. The second pair. The third. Then add. Mathematicians call it a dot product.*  
  → Pairs highlight one at a time; products drop into a running sum; label 'dot product'.
- **b3** — *Notice what it cost. Three multiplications, and a few additions. People lump a multiply and an add together and count them as floating point…*  
  → Counter ticks: 3 multiplies, 2 adds. The word FLOP is defined underneath.
- **b4** — *Hold on to that word. Everything in this story is going to be measured in it.*  
  → The word FLOP brightens and slides to the top-right as a persistent unit label.

## SCENE 006 · s0203 · Rows meet columns

| Field | Value |
|---|---|
| Time | 03:30–04:09 |
| Act | 2 — What Does Compute Even Mean? |
| Manim class | `docu.scenes.act02.S0203MatrixMultiply` |
| Output | `scene_006.mp4` |
| Claims | GEN-002 |
| Sources | textbook (definition) |
| Audio | music: curious; SFX: none |
| Loop opened | — |
| Loop closed | — |

- **b1** — *A real layer doesn't have one neuron. It has many, all looking at the same inputs. Stack their weight rows on top of each other, and you get…*  
  → One weight row duplicates into three rows, forming a 3 by 3 matrix W beside input vector x.
- **b2** — *Each row meets the input, does its dot product, and produces one output. Row one, output one. Row two, output two.*  
  → Row 1 slides over x, multiplies, yields y1. Row 2 yields y2. Row 3 yields y3.
- **b3** — *And if we feed in three inputs at once, three tokens say, it becomes a matrix times a matrix. Every row meets every column.*  
  → x widens into a 3 by 3 matrix X. Result grid fills cell by cell as rows sweep across columns.
- **b4** — *Three rows, three columns, three multiplications each. Twenty-seven multiplications, for the smallest matrix you can draw.*  
  → Counter races to 27. Equation (m×n)·(n×p) → m·n·p multiplications appears.

## SCENE 007 · s0204 · From twenty-seven to billions

| Field | Value |
|---|---|
| Time | 04:09–05:10 |
| Act | 2 — What Does Compute Even Mean? |
| Manim class | `docu.scenes.act02.S0204ScaleExplodes` |
| Output | `scene_007.mp4` |
| Claims | DER-005, DER-006, GEN-003, V3-008 |
| Sources | V3 inference/configs/config_671B.json (config_671B.json); derived from GEN-003, V3-001 (our arithmetic); derived from V3-008 (our arithmetic); standard scaling-law approximation (Kaplan et al. 2020) (approximation) |
| Audio | music: curious; SFX: none |
| Loop opened | — |
| Loop closed | L2 |

- **b1** — *Now the real thing. Inside DeepSeek V3, each token is represented by 7,168 numbers.*  
  → The 3×3 matrix zooms out; grid lines multiply until the matrix is a fine texture labelled 7168 × 7168.
- **b2** — *Pushing one token through a single square matrix of that size takes about 51 million multiplications. One token. One matrix.*  
  → Counter jumps from 27 to 51,380,224.
- **b3** — *A model is hundreds of these matrices, stacked in layers. A useful rule of thumb: running a model costs about two operations for every param…*  
  → Matrices stack into a tall column of layers; the rule '≈ 2 FLOPs × active parameters × tokens' writes out.
- **b4** — *For V3, with its 37 billion active parameters, that's roughly 74 billion operations. For every single word fragment it produces.*  
  → 37,000,000,000 × 2 → ≈ 74 billion FLOPs per token. A token block flashes.
- **b5** — *So that's what compute is. Not magic. Not thinking, exactly. Multiplication and addition, repeated an astronomical number of times.*  
  → Zoom out: the layer stack becomes a tiny glowing speck among countless others.
- **b6** — *Which raises an obvious question. What kind of machine can do that fast enough?*  
  → The speck becomes a single GPU block outline.

## SCENE 008 · s0301 · One lane or ten thousand

| Field | Value |
|---|---|
| Time | 05:10–06:03 |
| Act | 3 — Why GPUs Matter |
| Manim class | `docu.scenes.act03.S0301CPUvsGPU` |
| Output | `scene_008.mp4` |
| Claims | — (conceptual / pedagogical only) |
| Sources | — |
| Audio | music: pulse; SFX: pulse |
| Loop opened | — |
| Loop closed | — |

- **b1** — *A normal processor, a CPU, is built like a few brilliant specialists. Each one is fast and clever, but there are only a handful of them.*  
  → Left: a CPU with 8 large cores. Multiplication tasks queue up and pass through in sequence.
- **b2** — *Give them a matrix multiplication, and they mostly work through it a chunk at a time.*  
  → A 16x16 result grid fills slowly, cell groups lighting in order.
- **b3** — *But look at what a matrix multiplication actually is. Every output cell is its own little dot product. None of them needs to wait for any ot…*  
  → Grid cells separate slightly; each shows a tiny independent row·column icon.
- **b4** — *A graphics processor, a GPU, bets everything on that fact. Instead of a few clever cores, it has thousands of simple ones, all doing multipl…*  
  → Right: GPU block with a dense grid of tiny cores. The same 16x16 grid fills almost at once.
- **b5** — *That's why GPUs, originally built to colour in pixels for video games, became the engines of AI. The mathematics of neural networks is, almo…*  
  → Side-by-side race: CPU grid is still 10% full when GPU grid finishes.

## SCENE 009 · s0302 · The pipe, not the engine

| Field | Value |
|---|---|
| Time | 06:03–06:59 |
| Act | 3 — Why GPUs Matter |
| Manim class | `docu.scenes.act03.S0302MemoryWall` |
| Output | `scene_009.mp4` |
| Claims | — (conceptual / pedagogical only) |
| Sources | — |
| Audio | music: pulse; SFX: none |
| Loop opened | L3 |
| Loop closed | — |

- **b1** — *But here's the thing most people miss. Doing the arithmetic is only half the job. The numbers have to get to the cores first.*  
  → GPU core grid on the right; on the left a large memory bank labelled HBM; a pipe connects them.
- **b2** — *The weights live in memory. Every time you use them, they have to travel through a pipe into the compute units. And that pipe has a width. B…*  
  → Number-particles flow along the pipe. Pipe width is annotated 'bandwidth (bytes / s)'.
- **b3** — *If the cores can eat numbers faster than the pipe can deliver them, the cores sit idle. Waiting. And a waiting GPU is the most expensive way…*  
  → Pipe narrows; particles trickle; cores dim one by one; label 'idle'.
- **b4** — *So there are really three walls. Compute: how fast you can multiply. Memory: how much you can hold, and how fast you can read it. And commun…*  
  → Three tall pillars rise, colour-coded: COMPUTE (orange), MEMORY (teal), COMMUNICATION (violet).
- **b5** — *Keep these three walls in mind. Every clever idea in the rest of this story is an attack on one of them.*  
  → The three pillars shrink into a small persistent legend at the bottom-left.

## SCENE 010 · s0303 · Same engine, narrower pipes

| Field | Value |
|---|---|
| Time | 06:59–07:59 |
| Act | 3 — Why GPUs Matter |
| Manim class | `docu.scenes.act03.S0303ManyGPUs` |
| Output | `scene_010.mp4` |
| Claims | DER-004, EXP-005, EXP-006 |
| Sources | EPOCH_EXPORT; vendor spec summaries (spec comparisons); derived from V3-001, EXP-006 (our arithmetic); vendor spec summaries (spec comparisons) |
| Audio | music: pulse; SFX: none |
| Loop opened | — |
| Loop closed | — |

- **b1** — *Now, a model the size of V3 doesn't fit on one GPU. Even stored at just one byte per parameter, its weights would need more than eight GPUs'…*  
  → A long bar '671 GB of weights' next to a single GPU's '80 GB' bar; the weights bar is split across 9 GPU blocks.
- **b2** — *So the model gets split across many GPUs, and those GPUs have to constantly exchange numbers. The connections between them become part of th…*  
  → Nine GPUs arranged in a ring; links draw between them; numbers flow along the links.
- **b3** — *And this is exactly where the export rules bit. The H800 kept essentially the same engine as the H100. What got cut was the pipe between chi…*  
  → Two GPU pairs side by side: H100 pair with a thick link '≈900 GB/s', H800 pair with a thinner link '≈400 GB/s'. Label 'widely reported'.
- **b4** — *Same engine. Narrower pipes. Remember that, because it's going to matter much more than it seems right now. And it raises a question we'll c…*  
  → The thinner H800 link pulses. The question 'Why aren't more GPUs enough?' appears and pins to the corner.

## SCENE 011 · s0401 · What does 'it' mean?

| Field | Value |
|---|---|
| Time | 07:59–08:36 |
| Act | 4 — Inside a Transformer |
| Manim class | `docu.scenes.act04.S0401TheSentence` |
| Output | `scene_011.mp4` |
| Claims | — (conceptual / pedagogical only) |
| Sources | — |
| Audio | music: minimal; SFX: whoosh |
| Loop opened | L4 |
| Loop closed | — |

- **b1** — *So we know the hardware. But what is all that multiplication actually for? Let's open up a language model and look.*  
  → Camera flies into the GPU block; the grid dissolves into darkness.
- **b2** — *Here's a sentence. The animal didn't cross the street because it was tired.*  
  → The sentence types across the screen.
- **b3** — *Question. What does it refer to? The animal, or the street?*  
  → 'it' highlights; two arcs reach tentatively to 'animal' and 'street'.
- **b4** — *You knew instantly. The animal. Streets don't get tired. But notice how you knew. You looked at other words in the sentence and pulled their…*  
  → Arc to 'animal' strengthens, to 'street' fades; 'tired' glows as the clue.
- **b5** — *A model has to do the same thing, with nothing but numbers. So first, the text becomes pieces. Tokens.*  
  → The sentence splits into rounded token blocks with small gaps; the token colour is established.

## SCENE 012 · s0402 · Words as arrows

| Field | Value |
|---|---|
| Time | 08:36–09:14 |
| Act | 4 — Inside a Transformer |
| Manim class | `docu.scenes.act04.S0402Embeddings` |
| Output | `scene_012.mp4` |
| Claims | — (conceptual / pedagogical only) |
| Sources | — |
| Audio | music: minimal; SFX: none |
| Loop opened | — |
| Loop closed | — |

- **b1** — *Each token is then swapped for a list of numbers. A vector. We call it an embedding.*  
  → Token 'animal' drops down; a column of 6 numbers unrolls beneath it.
- **b2** — *Real models use thousands of numbers per token. We'll draw just two, so we can see them as an arrow on a page.*  
  → The column compresses into a 2D arrow on a small plane.
- **b3** — *These numbers are learned. During training, words that behave alike drift near each other. Animal lands near dog. Street lands near road. Ti…*  
  → Plane fills with labelled arrows clustering: animal/dog/cat; street/road; tired/sleepy.
- **b4** — *Meaning, in a model, is a direction. And that means we can measure how related two words are with the operation we already know. The dot pro…*  
  → Two arrows animal and dog; the angle between them is shaded; 'a · b' appears.

## SCENE 013 · s0403 · Questions and advertisements

| Field | Value |
|---|---|
| Time | 09:14–10:07 |
| Act | 4 — Inside a Transformer |
| Manim class | `docu.scenes.act04.S0403QueryKeyValue` |
| Output | `scene_013.mp4` |
| Claims | GEN-001 |
| Sources | VASWANI_2017 (Eq. 1) |
| Audio | music: minimal; SFX: none |
| Loop opened | — |
| Loop closed | — |

- **b1** — *Here's the trick at the heart of every modern language model. Each token makes three new vectors from its embedding, each by multiplying wit…*  
  → Token 'it' with its embedding; three arrows fan out to vectors labelled Q, K, V, each via a small matrix W_Q, W_K, W_V.
- **b2** — *A query. What am I looking for? For it, something like: which noun am I talking about?*  
  → Q vector highlights with a speech-bubble paraphrase 'which noun am I?'
- **b3** — *A key. What do I have to offer? Every token advertises itself. Animal says: I'm a living thing, a noun.*  
  → Every token shows a small K tag; 'animal' K bubble: 'living noun'.
- **b4** — *And a value. If you do pay attention to me, here's the information I'll hand over.*  
  → V tags appear beneath each token as small filled bars.
- **b5** — *To decide where it should look, we take its query, and dot it with the key of every word so far. A model that writes left to right can only …*  
  → Q of 'it' sweeps across all K's; score numbers pop above each earlier token: animal highest, street next; later tokens are masked.
- **b6** — *Do this for every token at once, and those dot products form a grid. Query times key transpose. Q K transpose.*  
  → Scores assemble into an n×n grid (heatmap), upper triangle masked (causal); QKᵀ writes beside it.

## SCENE 014 · s0404 · Scores into attention

| Field | Value |
|---|---|
| Time | 10:07–10:56 |
| Act | 4 — Inside a Transformer |
| Manim class | `docu.scenes.act04.S0404Softmax` |
| Output | `scene_014.mp4` |
| Claims | — (conceptual / pedagogical only) |
| Sources | — |
| Audio | music: minimal; SFX: none |
| Loop opened | — |
| Loop closed | — |

- **b1** — *But raw scores are awkward. They can be negative, and they don't add up to anything in particular. We want percentages. How much attention s…*  
  → Row of scores for 'it' shown as bars, some negative.
- **b2** — *So we do two things. First, raise e to the power of each score. Everything becomes positive, and big scores become much bigger.*  
  → Each bar transforms through e^x: all positive, the 'animal' bar dominates.
- **b3** — *Then divide each by the total. Now they add up to one. This is called softmax.*  
  → Bars normalise into a stacked 100% bar; formula softmax(s_i) = e^{s_i} / Σ e^{s_j}.
- **b4** — *One more small detail. Before the softmax, the scores are divided by the square root of the vector length. Long vectors produce huge dot pro…*  
  → QKᵀ becomes QKᵀ/√d inside softmax(...).
- **b5** — *And here's the result. It sends most of its attention to animal. The model has worked out what you worked out.*  
  → Attention arcs from 'it' drawn with thickness = weight; the arc to 'animal' thickest.

## SCENE 015 · s0405 · Borrowing meaning

| Field | Value |
|---|---|
| Time | 10:56–11:38 |
| Act | 4 — Inside a Transformer |
| Manim class | `docu.scenes.act04.S0405WeightedValues` |
| Output | `scene_015.mp4` |
| Claims | GEN-001 |
| Sources | VASWANI_2017 (Eq. 1) |
| Audio | music: minimal; SFX: none |
| Loop opened | — |
| Loop closed | L4 |

- **b1** — *Now it collects its reward. Take each token's value vector, scale it by its attention weight, and add them all up.*  
  → Value bars shrink or grow by weight and fly into 'it', summing into a new vector.
- **b2** — *The new vector for it is no longer just it. It now carries a large dose of animal.*  
  → The 'it' embedding arrow rotates toward the 'animal' cluster on the 2D plane.
- **b3** — *Put together, the whole mechanism fits on one line. Attention of Q, K and V equals softmax of Q K transpose over root d, times V.*  
  → Full equation Attention(Q,K,V) = softmax(QKᵀ/√d)V assembles from the pieces already on screen.
- **b4** — *Look at it again, though. Three matrix multiplications to make Q, K and V. One to compare everything with everything. One more to blend the …*  
  → Each matmul in the equation flashes compute-orange in turn.

## SCENE 016 · s0406 · Many heads, then thinking

| Field | Value |
|---|---|
| Time | 11:38–12:28 |
| Act | 4 — Inside a Transformer |
| Manim class | `docu.scenes.act04.S0406HeadsAndFFN` |
| Output | `scene_016.mp4` |
| Claims | GEN-005 |
| Sources | standard architecture accounting (e.g. Kaplan et al. 2020) (parameter accounting) |
| Audio | music: minimal; SFX: none |
| Loop opened | — |
| Loop closed | — |

- **b1** — *One attention pattern can only capture one kind of relationship at a time. So models run many in parallel, each with its own Q, K and V matr…*  
  → The single attention heatmap splits into 4 smaller heatmaps with different patterns (pronouns, neighbours, verbs, punctuation).
- **b2** — *One head might track pronouns. Another, which word came just before. Another, subject and verb. Nobody tells them to. They specialise on the…*  
  → Each head gets a tentative caption; captions marked 'illustrative'.
- **b3** — *After attention comes the second half of each block. A feed-forward network. Two big matrices applied to each token on its own. If attention…*  
  → Block diagram: [Attention] → [Feed-forward]; inside FFN a wide matrix expands then contracts the vector.
- **b4** — *And in large models, most of the parameters live right here, in these feed-forward matrices. Remember that. It's about to become important.*  
  → A parameter-share bar: FFN takes the large majority; label 'most parameters live here' (general rule of thumb).

## SCENE 017 · s0407 · Stack, and predict

| Field | Value |
|---|---|
| Time | 12:28–12:59 |
| Act | 4 — Inside a Transformer |
| Manim class | `docu.scenes.act04.S0407TheStack` |
| Output | `scene_017.mp4` |
| Claims | — (conceptual / pedagogical only) |
| Sources | — |
| Audio | music: minimal; SFX: none |
| Loop opened | — |
| Loop closed | — |

- **b1** — *Attention, then feed-forward. That's one block. Now stack them. Dozens of times.*  
  → The block duplicates upwards into a tall tower of layers.
- **b2** — *At the top, the final vector is compared against every token in the vocabulary, and turned, with softmax again, into a probability for what …*  
  → Top of tower emits a probability bar chart over candidate next tokens: 'and' 0.41, '.' 0.22, 'so' 0.12...
- **b3** — *Pick one. Add it to the text. Run the whole thing again. That's how every chatbot you've ever used writes. One token at a time.*  
  → Chosen token flies back to the input sequence; tower pulses again.
- **b4** — *That's a Transformer. And now we can see the problem coming.*  
  → Camera pulls back; the tower sits small in the frame.

## SCENE 018 · s0501 · Bigger, and bigger

| Field | Value |
|---|---|
| Time | 12:59–13:36 |
| Act | 5 — The Computational Explosion |
| Manim class | `docu.scenes.act05.S0501Scaling` |
| Output | `scene_018.mp4` |
| Claims | GEN-003 |
| Sources | standard scaling-law approximation (Kaplan et al. 2020) (approximation) |
| Audio | music: rising; SFX: none |
| Loop opened | — |
| Loop closed | — |

- **b1** — *Researchers kept discovering the same thing. Make the model bigger, train it on more text, and it gets better. Smoothly, predictably, better…*  
  → A rising curve 'capability vs. scale' draws itself (schematic, no numbers).
- **b2** — *So they made them bigger. More layers. Wider matrices. More heads. And every one of those multiplies the parameter count.*  
  → The tower grows taller; each layer grows wider; a parameter counter spins upward.
- **b3** — *But remember our rule of thumb. Two operations per parameter, per token. In an ordinary, dense model, every single token has to pass through…*  
  → A token block travels up the tower; every matrix it passes lights up. All of them.
- **b4** — *Double the model, double the cost of every word. Forever. For every user.*  
  → Two towers, the second twice as big; cost meter under each, the second twice as high.

## SCENE 019 · s0502 · Do we need all of it?

| Field | Value |
|---|---|
| Time | 13:36–14:09 |
| Act | 5 — The Computational Explosion |
| Manim class | `docu.scenes.act05.S0502DoWeNeedAll` |
| Output | `scene_019.mp4` |
| Claims | — (conceptual / pedagogical only) |
| Sources | — |
| Audio | music: rising; SFX: none |
| Loop opened | L5 |
| Loop closed | — |

- **b1** — *Now think about what that means in practice. You ask a giant model, what's two plus two.*  
  → Token stream '2 + 2 =' enters the tower.
- **b2** — *And to answer, it fires every weight it has. Including the ones that learned French poetry, and medieval history, and how to write a SQL que…*  
  → Regions inside the tower are faintly labelled: poetry, history, code, biology, maths; all light up.
- **b3** — *That seems wasteful. When you do arithmetic, you don't consult everything you know about poetry.*  
  → Only the maths region stays bright; the others dim.
- **b4** — *So here's the question that changes everything. What if a model didn't need to use all of itself, every single time?*  
  → The question types out; the tower splits into faint separate blocks behind it.

## SCENE 020 · s0601 · Splitting the thinker

| Field | Value |
|---|---|
| Time | 14:09–14:43 |
| Act | 6 — Mixture of Experts |
| Manim class | `docu.scenes.act06.S0601SplitTheNetwork` |
| Output | `scene_020.mp4` |
| Claims | — (conceptual / pedagogical only) |
| Sources | — |
| Audio | music: discovery; SFX: none |
| Loop opened | — |
| Loop closed | — |

- **b1** — *Go back to the feed-forward network, the part of each block where most of the parameters live.*  
  → One Transformer block; the FFN box highlights.
- **b2** — *Now, instead of one huge feed-forward network, cut it into several smaller ones. Each is a complete little network on its own. We'll call th…*  
  → The FFN box slices into 8 smaller boxes E1..E8, each in expert-green.
- **b3** — *Here's the key idea. For any given token, we only run a few of them. The rest stay switched off.*  
  → Two of the 8 light up; six stay dark.
- **b4** — *The model can hold the knowledge of all eight experts. But each token only pays for two. This is called a Mixture of Experts.*  
  → Labels: 'stored: 8 experts' vs 'computed: 2 experts'. Title 'Mixture of Experts (MoE)'.

## SCENE 021 · s0602 · Who decides?

| Field | Value |
|---|---|
| Time | 14:43–15:27 |
| Act | 6 — Mixture of Experts |
| Manim class | `docu.scenes.act06.S0602TheRouter` |
| Output | `scene_021.mp4` |
| Claims | — (conceptual / pedagogical only) |
| Sources | — |
| Audio | music: discovery; SFX: none |
| Loop opened | — |
| Loop closed | — |

- **b1** — *Which raises an obvious question. Who decides which experts a token should visit?*  
  → A token hovers in front of 8 experts; question mark.
- **b2** — *Another small learned piece of the network. A router. It looks at the token and gives every expert a score.*  
  → A router diamond appears between token and experts; score bars rise above each expert.
- **b3** — *Watch what happens with different tokens. The word integral lights up one pair of experts.*  
  → Token 'integral' → router → experts E2 and E5 light.
- **b4** — *The code word def lights up a different pair. The word mitochondria, another. Even a word like the gets its own routing.*  
  → Tokens 'def', 'mitochondria', 'the' route to different expert pairs in turn.
- **b5** — *Nobody hand-assigns topics. The router and the experts learn together, and the specialisation emerges from training. Real experts rarely map…*  
  → Expert topic captions fade to '?'; disclaimer 'illustrative labels'.

## SCENE 022 · s0603 · The mathematics of choosing

| Field | Value |
|---|---|
| Time | 15:27–16:23 |
| Act | 6 — Mixture of Experts |
| Manim class | `docu.scenes.act06.S0603RoutingMath` |
| Output | `scene_022.mp4` |
| Claims | V41-017 |
| Sources | V41_PAPER (§2.1.1) |
| Audio | music: discovery; SFX: none |
| Loop opened | — |
| Loop closed | — |

- **b1** — *In symbols, it's short. The router is just a matrix. Multiply the token's vector by it, and you get one score per expert.*  
  → s = W_r x; vector of 8 scores.
- **b2** — *Turn the scores into weights, keep only the top k, and throw the rest away. That's top k routing.*  
  → Scores → gate weights g_i; top-2 highlighted; the others crossed out.
- **b3** — *The output is the chosen experts' answers, blended by their weights. The same weighted-sum trick as attention, just applied to experts inste…*  
  → y = Σ_{i ∈ top-k} g_i · E_i(x); two expert outputs scale and merge.
- **b4** — *But there's a trap. If the router falls in love with one expert, every token piles into it, while the others sit idle. You'd have a giant mo…*  
  → Tokens stream toward E3; E3's load bar overflows; others empty.
- **b5** — *So training has to balance the load. DeepSeek does it by nudging each expert's score up or down, depending on how busy it has been. In V4.1 …*  
  → Small bias arrows adjust each expert's score; load bars even out.

## SCENE 023 · s0604 · DeepSeek's version

| Field | Value |
|---|---|
| Time | 16:23–17:40 |
| Act | 6 — Mixture of Experts |
| Manim class | `docu.scenes.act06.S0604DeepSeekMoE` |
| Output | `scene_023.mp4` |
| Claims | DER-007, V2-001, V3-001, V3-008, V41-007 |
| Sources | V3 inference/configs/config_671B.json (config_671B.json); V3_README (README §1); V3_README (table); V2_REPORT (README comparison table); V41_PAPER (§4.2.1); derived from V3-001 (our arithmetic) |
| Audio | music: discovery; SFX: none |
| Loop opened | L6 |
| Loop closed | L5 |

- **b1** — *DeepSeek pushed this idea further than most. Two changes. First, lots of small experts instead of a few big ones, so tokens can mix and matc…*  
  → 8 big experts shatter into a dense grid of 64 small ones.
- **b2** — *Second, one shared expert that every token always visits, to hold common knowledge, so the specialists don't all have to relearn the basics.*  
  → A distinct shared expert slab appears at left, connected to every token.
- **b3** — *DeepSeek V2 had 236 billion parameters, but only about 21 billion active per token.*  
  → Bar: 236B total, 21B lit.
- **b4** — *V3 went further. In each of its expert layers, 256 routed experts plus one shared expert. Each token visits just 8 of the 256.*  
  → Grid of 256 small experts + 1 shared; 8 light up for a passing token.
- **b5** — *671 billion parameters stored. 37 billion used for any one token. About five and a half percent.*  
  → Bar 671B with a 37B sliver lit; '≈ 5.5% active'.
- **b6** — *And the 2026 model, V4.1 Flash, uses 384 routed experts per layer, with 6 chosen for each token.*  
  → Grid morphs to 384 experts; 6 lit.
- **b7** — *So a model can be enormous, and still cheap to run, per token. That answers our question. But it creates a brand new one. Where do all these…*  
  → Expert grid pulls apart into clusters, each cluster sitting on a GPU block.

## SCENE 024 · s0701 · Experts on islands

| Field | Value |
|---|---|
| Time | 17:40–18:25 |
| Act | 7 — The Communication Problem |
| Manim class | `docu.scenes.act07.S0701Islands` |
| Output | `scene_024.mp4` |
| Claims | — (conceptual / pedagogical only) |
| Sources | — |
| Audio | music: tension; SFX: whoosh |
| Loop opened | — |
| Loop closed | — |

- **b1** — *Remember, a model like V3 is far too big for one GPU. So the experts are spread out. A few here, a few there, across many GPUs, across many …*  
  → Four GPU islands, each hosting a cluster of expert squares.
- **b2** — *Now follow a single token. The router says: you need expert 12, expert 97, and expert 200. And they're on three different GPUs.*  
  → A token on island 1; router marks three experts on islands 2, 3, 4; dotted paths appear.
- **b3** — *So the token's vector has to be sent there. Computed. And the results sent back. Dispatch, then combine.*  
  → Token copies fly out along the paths, experts flash, results fly back and merge.
- **b4** — *Now do that for every token in a batch, at every expert layer. Every GPU is sending to every other GPU, all at once. Engineers call it all t…*  
  → Dozens of tokens; paths from every island to every island form a dense web.

## SCENE 025 · s0702 · The cost of waiting

| Field | Value |
|---|---|
| Time | 18:25–19:17 |
| Act | 7 — The Communication Problem |
| Manim class | `docu.scenes.act07.S0702WaitingGPUs` |
| Output | `scene_025.mp4` |
| Claims | EXP-005 |
| Sources | EPOCH_EXPORT; vendor spec summaries (spec comparisons) |
| Audio | music: tension; SFX: none |
| Loop opened | — |
| Loop closed | L3 |

- **b1** — *Let's draw what one GPU's time looks like. Compute. Then wait for tokens to arrive. Compute. Wait for results to come back.*  
  → A horizontal timeline: orange compute blocks alternating with violet communication blocks, with grey idle gaps.
- **b2** — *Those grey gaps are the GPU doing nothing, while its numbers are stuck in the wires. And the narrower the wire, the longer the gaps.*  
  → Communication blocks stretch; idle gaps widen.
- **b3** — *Now you can see why the H800's narrower links mattered. MoE saves compute, but it spends communication. And communication was exactly the re…*  
  → Label 'H800: narrower links'; the violet blocks swell further. The legend's COMMUNICATION pillar glows.
- **b4** — *That's the answer to the question from earlier. Why aren't more GPUs enough? Because every GPU you add is another island, and islands have t…*  
  → Island count grows 4 → 16; link web thickens; utilisation meter drops.

## SCENE 026 · s0703 · Hiding the wait

| Field | Value |
|---|---|
| Time | 19:17–20:21 |
| Act | 7 — The Communication Problem |
| Manim class | `docu.scenes.act07.S0703Overlap` |
| Output | `scene_026.mp4` |
| Claims | V3-006, V3-011 |
| Sources | V3_README (README §2); V3_REPORT (§3.2) |
| Audio | music: tension; SFX: none |
| Loop opened | — |
| Loop closed | L6 |

- **b1** — *DeepSeek's answer for V3 wasn't a faster wire. It was a smarter schedule.*  
  → Timeline from before returns.
- **b2** — *The idea is simple to say and very hard to build. While one batch of tokens is travelling, compute on a different batch. Keep the engine bus…*  
  → Two interleaved timelines slide together so communication of batch A overlaps compute of batch B; idle gaps vanish.
- **b3** — *They called their pipeline schedule DualPipe, and wrote custom communication code so that computation and communication overlap almost compl…*  
  → Label 'DualPipe (DeepSeek-V3)'; the overlapped timeline is solid orange with violet underneath.
- **b4** — *Then they attacked the size of the mail itself. Numbers in a computer take up space. A common format uses 16 bits for each one. V3 trained w…*  
  → A 16-bit box of cells shrinks to an 8-bit box; label 'FP8'.
- **b5** — *Half the bits means half the bytes to store, half the bytes to move, and faster arithmetic on hardware built for it. DeepSeek says V3 was th…*  
  → Tokens in the pipe shrink to half size; twice as many fit through the same pipe.
- **b6** — *It's a pattern worth noticing. Not more hardware. A better understanding of where the time was actually going.*  
  → The three-pillar legend: COMPUTE and COMMUNICATION pillars get a checkmark tick.

## SCENE 027 · s0801 · Writing one token at a time

| Field | Value |
|---|---|
| Time | 20:21–21:01 |
| Act | 8 — The Memory Wall |
| Manim class | `docu.scenes.act08.S0801WritingOneToken` |
| Output | `scene_027.mp4` |
| Claims | — (conceptual / pedagogical only) |
| Sources | — |
| Audio | music: minimal; SFX: none |
| Loop opened | — |
| Loop closed | — |

- **b1** — *There's one wall left. And it's the one that shows up when you actually use these models. Memory.*  
  → The MEMORY pillar in the legend glows and moves to centre.
- **b2** — *Remember how a model writes. One token at a time. Each new token looks back, with attention, at every token before it.*  
  → A sequence of tokens; a new token appears at the end and draws attention arcs to all previous tokens.
- **b3** — *To do that, it needs every earlier token's key and value. Now, those don't change. The key for animal is the same at word ten as it was at w…*  
  → Each earlier token shows its K and V tags, frozen.
- **b4** — *So instead of recomputing them for every new word, the model saves them. A shelf of keys and values that grows by one entry per token. The K…*  
  → K,V tags slide off onto a shelf below; each new token adds a box to the shelf. Label 'KV cache'.

## SCENE 028 · s0802 · How big is the shelf?

| Field | Value |
|---|---|
| Time | 21:01–21:57 |
| Act | 8 — The Memory Wall |
| Manim class | `docu.scenes.act08.S0802CacheGrowth` |
| Output | `scene_028.mp4` |
| Claims | DER-002, V3-008 |
| Sources | V3 inference/configs/config_671B.json (config_671B.json); derived from V3-008, V3-010 (our arithmetic) |
| Audio | music: minimal; SFX: none |
| Loop opened | L7 |
| Loop closed | — |

- **b1** — *Let's measure the shelf. For ordinary attention, each token stores a key and a value, for every head, in every layer.*  
  → Formula: bytes/token = 2 × layers × heads × head_dim × bytes.
- **b2** — *Here's a hypothetical. If a model with V3's shape had used ordinary attention, with 128 heads of 128 numbers, over 61 layers, that's about 4…*  
  → Numbers plug in: 2 × 61 × 128 × 128 × 2 bytes ≈ 4.0 MB. Tag 'hypothetical, our arithmetic'.
- **b3** — *Now a long conversation. A hundred and twenty eight thousand tokens. That's over five hundred gigabytes. For one conversation.*  
  → The shelf stretches far off-screen; a memory bar climbs past six stacked 80 GB GPU lines.
- **b4** — *The weights are shared by every user. But this cache is personal. Every conversation carries its own. That's what fills the memory of a GPU …*  
  → Several users, each with their own shelf, all trying to fit into one GPU's memory box. It overflows.
- **b5** — *So the question becomes: how small can a memory of the past possibly be?*  
  → Question types out and pins to the corner.

## SCENE 029 · s0803 · Compress the memory

| Field | Value |
|---|---|
| Time | 21:57–23:01 |
| Act | 8 — The Memory Wall |
| Manim class | `docu.scenes.act08.S0803LatentAttention` |
| Output | `scene_029.mp4` |
| Claims | V2-002, V3-009, V3-010 |
| Sources | V2_REPORT (Abstract); V3 config_671B.json (config_671B.json); derived from V3-008, V3-009 (our arithmetic) |
| Audio | music: minimal; SFX: none |
| Loop opened | — |
| Loop closed | — |

- **b1** — *DeepSeek's first big answer, back in V2, was called Multi-head Latent Attention. M L A.*  
  → Title 'Multi-head Latent Attention (MLA) · DeepSeek-V2'.
- **b2** — *Here's the intuition. All those keys and values, across all the heads, are made from the same token. They're highly redundant. So instead of…*  
  → A tall stack of 128 K/V head strips squeezes through a funnel into one thin latent bar, then expands back into heads on the other side.
- **b3** — *The rebuild is just another matrix multiplication. And multiplication is the thing GPUs have in abundance. You're trading cheap compute for …*  
  → The expansion step is labelled 'W_up · c (compute)'; the latent bar labelled 'stored (memory)'.
- **b4** — *In V3's published configuration, each token stores a 512 number summary, plus 64 numbers for position. 576 numbers, instead of roughly 32 th…*  
  → Two bars: 32,768 vs 576, scaled correctly.
- **b5** — *When they introduced it in V2, DeepSeek reported a 93.3 percent cut in KV cache compared with their earlier 67 billion parameter model.*  
  → Citation card: DeepSeek-V2 · −93.3% KV cache vs DeepSeek 67B.

## SCENE 030 · s0804 · Three dials

| Field | Value |
|---|---|
| Time | 23:01–23:31 |
| Act | 8 — The Memory Wall |
| Manim class | `docu.scenes.act08.S0804ThreeDials` |
| Output | `scene_030.mp4` |
| Claims | V41-018 |
| Sources | V41_PAPER (§2.3) |
| Audio | music: minimal; SFX: none |
| Loop opened | — |
| Loop closed | — |

- **b1** — *Now step back. The size of the cache is really three numbers multiplied together.*  
  → Equation: cache = (size of each entry) × (number of entries along the sequence) × (number of layers keeping one).
- **b2** — *How big each entry is. How many entries you keep along the sequence. And how many layers keep their own.*  
  → Three dials appear: ENTRY SIZE, SEQUENCE, LAYERS.
- **b3** — *MLA turned the first dial. Make each entry smaller. But the other two dials were still there, untouched.*  
  → ENTRY SIZE dial turns down; the other two stay at max.
- **b4** — *And by 2026, a new kind of workload was about to make those two dials the only ones that mattered.*  
  → SEQUENCE and LAYERS dials pulse.

## SCENE 031 · s0901 · The agent problem

| Field | Value |
|---|---|
| Time | 23:31–24:28 |
| Act | 9 — DeepSeek-V4.1-Flash: Pushing the Memory Wall |
| Manim class | `docu.scenes.act09.S0901Agents` |
| Output | `scene_031.mp4` |
| Claims | V41-001, V41-019, V41-020 |
| Sources | V41_PAPER (Abstract); V41_PAPER (Abstract; §2.1); V41_PAPER (§1) |
| Audio | music: discovery; SFX: none |
| Loop opened | — |
| Loop closed | — |

- **b1** — *By 2026, people weren't just chatting with models. They were handing them jobs. Read this code base. Run the tests. Fix the bug. Try again.*  
  → A loop diagram: model → tool call → result → model, spinning, with the context bar growing each lap.
- **b2** — *Every tool call pours more text back into the context. The inputs grow enormous, the outputs stay small. DeepSeek describes these workloads …*  
  → Input bar balloons, output bar stays thin; label 'input-heavy'.
- **b3** — *In September 2026, DeepSeek published a paper about exactly this, for a model called DeepSeek V4.1 Flash. 552 billion backbone parameters, a…*  
  → Paper card: 'DeepSeek-V4.1-Flash: Pushing the Limits of KV Cache Compression · arXiv 2609.19969'. Stats appear.
- **b4** — *And the paper is candid about the bottleneck. Earlier sparse attention had already tamed much of the compute cost of long contexts, which le…*  
  → Legend: COMPUTE pillar dims (tamed); MEMORY and COMMUNICATION pillars flare.

## SCENE 032 · s0902 · Don't look at everything

| Field | Value |
|---|---|
| Time | 24:28–25:17 |
| Act | 9 — DeepSeek-V4.1-Flash: Pushing the Memory Wall |
| Manim class | `docu.scenes.act09.S0902SparseAttention` |
| Output | `scene_032.mp4` |
| Claims | V41-001, V41-006, V41-008, V41-021 |
| Sources | V41_PAPER (Abstract; §2.1); V41_PAPER (§2.1; §4.2.1); V41_PAPER (§2.3; §4.2.1; Fig. 4); V41_PAPER (§4.2.1) |
| Audio | music: discovery; SFX: none |
| Loop opened | — |
| Loop closed | — |

- **b1** — *First, the sequence dial. When a new token is written, does it really need to look at all million earlier tokens?*  
  → A new token and a very long strip of past entries; attention lines to all of them, too dense to see.
- **b2** — *V4.1 Flash says no. A small, cheap scorer, called an indexer, quickly rates the past entries, and the model attends properly only to the top…*  
  → A light indexer scan passes along the strip; 512 cells highlight; full attention lines only to those.
- **b3** — *Early layers also compress the past, merging neighbouring tokens into shared entries. And every layer keeps a short, precise window of the m…*  
  → Pairs of cells merge into single cells (compression ratio 2); a bright window of recent tokens sits at the right end.
- **b4** — *Remember the grid of every token compared with every other? Double the text and that grid quadruples. Picking a fixed number of entries keep…*  
  → The n×n attention grid from Act 4 reappears, then thins into sparse columns.

## SCENE 033 · s0903 · Layers that share a memory

| Field | Value |
|---|---|
| Time | 25:17–26:17 |
| Act | 9 — DeepSeek-V4.1-Flash: Pushing the Memory Wall |
| Manim class | `docu.scenes.act09.S0903LayerReuse` |
| Output | `scene_033.mp4` |
| Claims | V41-008, V41-015, V41-022 |
| Sources | V41_PAPER (§2.3; §4.2.1; Fig. 4); V41_PAPER (§4.2.1); V41_PAPER (§6) |
| Audio | music: discovery; SFX: none |
| Loop opened | — |
| Loop closed | — |

- **b1** — *Now the layer dial. Traditionally, every layer keeps its own shelf of keys and values. Forty layers, forty shelves.*  
  → A stack of 40 layers, each with its own cache shelf beside it.
- **b2** — *V4.1 Flash introduces what it calls Compressed Sparse Attention 2. Its layers come in three modes.*  
  → Three mode badges: FULL, REINDEX, REUSE.
- **b3** — *A Full layer builds the shared memory and picks which entries matter. A Reindex layer borrows that memory, but re-scores it with its own que…*  
  → FULL layer writes a shelf; REINDEX layer draws from that shelf with a new selection; REUSE layer draws both.
- **b4** — *In the encoder, layers come in groups of six. One Full, then five Reuse. In the decoder, groups of four. Most layers stop storing their own …*  
  → Most of the 40 shelves collapse and vanish; only a few remain.
- **b5** — *The trade is the same one MLA made. A little more computation, and a lot less memory. And DeepSeek is upfront that it has a cost: the shared…*  
  → A small caution marker beside the REUSE badge: 'selection can err (§6)'.

## SCENE 034 · s0904 · Four bits

| Field | Value |
|---|---|
| Time | 26:17–27:02 |
| Act | 9 — DeepSeek-V4.1-Flash: Pushing the Memory Wall |
| Manim class | `docu.scenes.act09.S0904FourBits` |
| Output | `scene_034.mp4` |
| Claims | V41-009 |
| Sources | V41_PAPER (§2.4.4) |
| Audio | music: discovery; SFX: none |
| Loop opened | — |
| Loop closed | — |

- **b1** — *Then the entry size dial again. This time not by storing fewer numbers, but by storing each number with fewer bits.*  
  → An 8-bit cell box shrinks to 4 bits.
- **b2** — *Four bits give you only sixteen patterns. In the format DeepSeek uses, they stand for: zero, a half, one, one and a half, two, three, four, …*  
  → A number line with the FP4 (E2M1) values marked as ticks: 0, 0.5, 1, 1.5, 2, 3, 4, 6 and mirror negatives.
- **b3** — *That's a very coarse ruler. The trick is to give every group of 16 numbers its own shared scale, so the ruler stretches to fit whatever rang…*  
  → A group of 16 real values; a scale factor stretches the tick ruler to cover them; each value snaps to the nearest tick.
- **b4** — *DeepSeek stores the main cache this way, and keeps the more sensitive local window in 8 bits. Compared with the 8 bit main cache of V4, that…*  
  → Two cache shelves side by side: FP8 vs FP4, the FP4 one half the height.

## SCENE 035 · s0905 · Reading half as hard

| Field | Value |
|---|---|
| Time | 27:02–27:49 |
| Act | 9 — DeepSeek-V4.1-Flash: Pushing the Memory Wall |
| Manim class | `docu.scenes.act09.S0905EncoderDecoder` |
| Output | `scene_035.mp4` |
| Claims | V41-002, V41-006, V41-010 |
| Sources | V41_PAPER (Abstract; §2.1; §4.2.1); V41_PAPER (§2.1; §4.2.1); V41_PAPER (§2.2 Eq.1) |
| Audio | music: discovery; SFX: none |
| Loop opened | — |
| Loop closed | — |

- **b1** — *One more idea, aimed at the moment a long prompt first arrives. This is called prefill, reading the input, as opposed to decode, writing the…*  
  → Two phases labelled PREFILL (a huge block of input tokens) and DECODE (tokens emitted one by one).
- **b2** — *V4.1 Flash splits its 40 layers into a 20 layer encoder and a 20 layer decoder. The upper half doesn't compute its long-range memory from it…*  
  → A 40-layer stack split at the middle; arrows from the layer-20 output fan up into each decoder layer's memory.
- **b3** — *So when a long prompt arrives, only the bottom half has to process all of it. The paper says this nearly halves prefill computation.*  
  → Prompt block flows through the bottom 20 layers only; top half stays dim; label '≈ half the prefill compute'.
- **b4** — *Which is why the paper reports about 8 billion active parameters per token when reading, and about 16 billion when writing.*  
  → Two meters: PREFILL 8B active, DECODE 16B active.

## SCENE 036 · s0906 · 890 bytes

| Field | Value |
|---|---|
| Time | 27:49–29:10 |
| Act | 9 — DeepSeek-V4.1-Flash: Pushing the Memory Wall |
| Manim class | `docu.scenes.act09.S0906TheChart` |
| Output | `scene_036.mp4` |
| Claims | V41-003, V41-004, V41-011, V41-023 |
| Sources | V41_PAPER (Abstract; Fig. 1b); V41_PAPER (Abstract; §6); V41_PAPER (Figure 1(b)); V41_PAPER (§1; Fig. 2) |
| Audio | music: discovery; SFX: impact |
| Loop opened | — |
| Loop closed | L7, L9 |

- **b1** — *Now put the dials together. Here's a chart from DeepSeek's own paper. The global KV cache per token, across generations of their models.*  
  → Recreated horizontal bar chart axes appear; attribution line 'Data: DeepSeek-AI, arXiv:2609.19969, Fig. 1(b)'.
- **b2** — *Their first model, in 2023: about 389 thousand bytes per token.*  
  → Bar DeepSeek-V1 (2023.11): 389,120 B.
- **b3** — *V3.2, at the end of 2025: about 48 thousand.*  
  → Bar V3.2 (2025.12): 48,068 B.
- **b4** — *V4 Flash, in April 2026: 3,514.*  
  → Bar V4-Flash (2026.04): 3,514 B.
- **b5** — *And V4.1 Flash: 890 bytes.*  
  → Bar V4.1-Flash (2026.09): 890 B — a sliver. The '890 bytes' teaser from Act 1 flies in and lands on it.
- **b6** — *That's the number from the start. About 437 times smaller than their first model, and roughly a quarter of the model just before it. Less th…*  
  → Annotations '≈ 437× smaller than V1' and '≈ 4× smaller than V4-Flash'.
- **b7** — *And one more result. Stretching the context 256 times, from 4 thousand tokens to a million, raises the compute for each new token by only ab…*  
  → Two markers on a context axis 4K → 1M; a cost line rising only +25%.
- **b8** — *The paper also reports that, despite this far smaller memory, V4.1 Flash performs substantially better than the model before it. That's Deep…*  
  → Small card: 'better overall performance than V4-Flash (reported)'.

## SCENE 037 · s1001 · Measuring wrongness

| Field | Value |
|---|---|
| Time | 29:10–29:52 |
| Act | 10 — How a Model Learns |
| Manim class | `docu.scenes.act10.S1001Loss` |
| Output | `scene_037.mp4` |
| Claims | — (conceptual / pedagogical only) |
| Sources | — |
| Audio | music: minimal; SFX: none |
| Loop opened | L8 |
| Loop closed | — |

- **b1** — *We've talked about running a model. But where do all those billions of weights come from in the first place? Nobody writes them by hand.*  
  → The tower of layers, weights shown as a field of amber dots with random values.
- **b2** — *They start as random numbers. And a model with random weights, asked to continue the cat sat on the, will guess nonsense.*  
  → Prompt 'the cat sat on the' → probability bars nearly flat; 'mat' has 2%.
- **b3** — *But we know the right answer. Mat. So we can measure how wrong the model was. The standard measure is the negative log of the probability it…*  
  → Formula L = −log p(mat); with p = 0.02, L ≈ 3.9.
- **b4** — *Confident and right, the loss is near zero. Confident and wrong, it's huge. Now the entire goal of training fits in one sentence. Make that …*  
  → Curve −log p over p from 0 to 1; a dot slides from left (high loss) to right (near zero).

## SCENE 038 · s1002 · Walking downhill

| Field | Value |
|---|---|
| Time | 29:52–30:43 |
| Act | 10 — How a Model Learns |
| Manim class | `docu.scenes.act10.S1002GradientDescent` |
| Output | `scene_038.mp4` |
| Claims | GEN-004 |
| Sources | standard approximation (approximation) |
| Audio | music: minimal; SFX: none |
| Loop opened | — |
| Loop closed | — |

- **b1** — *Picture just one weight. Change it a little, and the loss goes up or down. Plot that, and you get a landscape.*  
  → A 1D loss curve over weight w with a ball on its slope.
- **b2** — *The slope at our current position tells us which way is downhill. That slope is called the gradient.*  
  → Tangent line at the ball; an arrow along −gradient.
- **b3** — *So we take a small step downhill. New weight equals old weight, minus a small step size times the gradient. Then measure again. Step again.*  
  → w ← w − η ∇L. The ball steps down the curve in several small hops, settling near the minimum.
- **b4** — *A real model does this for every one of its weights at once, in a landscape with billions of dimensions. The algorithm that finds all those …*  
  → The 1D curve morphs into a 3D-looking contour surface; gradient arrows ripple back down through the layer tower.
- **b5** — *And the backward pass costs roughly twice as much as the forward pass. So training costs about six operations per parameter, per token.*  
  → Forward arrow '2', backward arrow '4', total '≈ 6 FLOPs × active params × tokens'.

## SCENE 039 · s1003 · The loop

| Field | Value |
|---|---|
| Time | 30:43–31:28 |
| Act | 10 — How a Model Learns |
| Manim class | `docu.scenes.act10.S1003TheLoop` |
| Output | `scene_039.mp4` |
| Claims | DER-003, V41-012 |
| Sources | V41_PAPER (§4.2.2); derived from V41-012 (our arithmetic) |
| Audio | music: minimal; SFX: none |
| Loop opened | — |
| Loop closed | — |

- **b1** — *So training is a loop. Take a batch of text. Run it forward. Measure the loss. Run backwards to get gradients. Nudge every weight. Repeat.*  
  → Circular diagram: BATCH → FORWARD → LOSS → BACKWARD → UPDATE → (back to BATCH), spinning.
- **b2** — *How big a batch? For V4.1 Flash, the paper reports about a hundred million tokens in every single step.*  
  → Batch card: 100.6M tokens per step.
- **b3** — *And it trained on 45 trillion tokens in total. Divide one by the other, and that's roughly 450 thousand turns of this loop.*  
  → 45T ÷ 100.6M ≈ 447K steps; the loop counter spins up.
- **b4** — *Every turn involving all the walls at once. Compute for the forward and backward passes. Memory for the weights and the optimizer. And commu…*  
  → The three pillars light in sequence around the loop.

## SCENE 040 · s1004 · What V3's training took

| Field | Value |
|---|---|
| Time | 31:28–32:19 |
| Act | 10 — How a Model Learns |
| Manim class | `docu.scenes.act10.S1004TrainingV3` |
| Output | `scene_040.mp4` |
| Claims | DER-001, V3-001, V3-002, V3-003, V3-004 |
| Sources | V3_README (README §1); V3_README (README §1-2); V3_README; V3_REPORT (README §1-2; report Table 1); V3_REPORT (Abstract/§1 & §3.1); derived from V3-001, V3-002, GEN-004 (our arithmetic) |
| Audio | music: minimal; SFX: none |
| Loop opened | — |
| Loop closed | L8 |

- **b1** — *Now we can read DeepSeek V3's training numbers with understanding, instead of awe.*  
  → A clean ledger panel titled 'DeepSeek-V3 training (reported)'.
- **b2** — *37 billion active parameters. 14.8 trillion tokens. Plug them into the rule of thumb, six times parameters times tokens, and you get roughly…*  
  → 6 × 37×10⁹ × 14.8×10¹² ≈ 3.3×10²⁴; tag 'our estimate'.
- **b3** — *DeepSeek reports that each trillion tokens took 180 thousand H800 GPU hours. About three point seven days, on their cluster of 2,048 GPUs.*  
  → Row: '180K GPU-hours per trillion tokens ≈ 3.7 days on 2,048 H800s'.
- **b4** — *And the whole run, pre-training, context extension and post-training, added up to 2.788 million GPU hours.*  
  → Stacked bar: pre-training 2.664M + extension + post-training = 2.788M GPU-hours.

## SCENE 041 · s1101 · What the famous number means

| Field | Value |
|---|---|
| Time | 32:19–33:24 |
| Act | 11 — The Numbers, Honestly |
| Manim class | `docu.scenes.act11.S1101TheLedger` |
| Output | `scene_041.mp4` |
| Claims | V3-003, V3-005, V41-014 |
| Sources | V3_README; V3_REPORT (README §1-2; report Table 1); V3_REPORT (§1 Table 1 and following text); V41_PAPER (whole paper searched) |
| Audio | music: minimal; SFX: none |
| Loop opened | — |
| Loop closed | — |

- **b1** — *Which brings us to the most quoted number in this whole story. About 5.6 million dollars.*  
  → '$5.576M' large in the centre.
- **b2** — *Here's where it comes from. DeepSeek took those 2.788 million GPU hours and assumed a rental price of two dollars per GPU hour. That's it. H…*  
  → 2.788M × $2 = $5.576M written out.
- **b3** — *And in the same report, they say plainly what it excludes. The costs of prior research and ablation experiments on architectures, algorithms…*  
  → Two columns: INCLUDED (final training run GPU time) vs NOT INCLUDED (research, experiments, hardware purchase, staff).
- **b4** — *So the honest headline was never that DeepSeek built a frontier model for 5.6 million dollars. It's that the final training run, by their ac…*  
  → Crossed-out headline 'Built for $5.6M' → corrected 'final run ≈ $5.6M of GPU time (reported)'.
- **b5** — *And some things are simply not public. The V4.1 Flash paper, for instance, doesn't say what hardware it was trained on, or what it cost. So …*  
  → Ledger row: V4.1-Flash — hardware: not reported; cost: not reported.

## SCENE 042 · s1102 · So what was surprising?

| Field | Value |
|---|---|
| Time | 33:24–34:07 |
| Act | 11 — The Numbers, Honestly |
| Manim class | `docu.scenes.act11.S1102WhatWasSurprising` |
| Output | `scene_042.mp4` |
| Claims | GEN-007 |
| Sources | literature (citations) |
| Audio | music: minimal; SFX: none |
| Loop opened | — |
| Loop closed | — |

- **b1** — *So what actually was surprising? Not a secret invention. Mixture of experts, attention, low precision numbers. Those ideas existed before De…*  
  → Three idea cards (MoE, attention, low precision) each tagged 'prior art'.
- **b2** — *What was surprising was how far they were pushed, and how deliberately each one was aimed at a specific wall.*  
  → A table forms: WALL → IDEA.
- **b3** — *Compute: activate only the experts you need. Communication: overlap the waiting and shrink the numbers. Memory: compress the cache, share it…*  
  → Rows fill: COMPUTE → MoE (37B of 671B); COMMUNICATION → DualPipe + FP8; MEMORY → MLA → CSA2 + FP4 (890 B/token).
- **b4** — *Each one, on its own, is a sensible engineering choice. Together, they add up to a system shaped around its bottlenecks. Not around its budg…*  
  → The table glows; a caption 'shaped around the bottlenecks'.

## SCENE 043 · s1201 · See it all at once

| Field | Value |
|---|---|
| Time | 34:07–34:46 |
| Act | 12 — The Whole Machine |
| Manim class | `docu.scenes.act12.S1201WholeMachine` |
| Output | `scene_043.mp4` |
| Claims | DER-003 |
| Sources | derived from V41-012 (our arithmetic) |
| Audio | music: resolution; SFX: none |
| Loop opened | — |
| Loop closed | — |

- **b1** — *Let's zoom out and look at the whole machine, one last time.*  
  → Camera pulls back to an empty dark stage.
- **b2** — *Text becomes tokens. Tokens become vectors. Attention lets them borrow meaning from each other. A router sends each one to a handful of expe…*  
  → Pipeline builds left to right: DATA → TOKENS → EMBEDDINGS → ATTENTION → ROUTER → EXPERTS → OUTPUT, reusing each icon from earlier acts.
- **b3** — *The guess is scored. The loss flows backwards. Every weight moves a tiny step. And the loop begins again. Hundreds of thousands of times.*  
  → A return path: OUTPUT → LOSS → GRADIENTS → UPDATE loops back to the start.
- **b4** — *And over all of it, the three walls. Compute, wherever numbers multiply. Memory, wherever numbers wait. Communication, wherever numbers trav…*  
  → Coloured overlays: COMPUTE glows on attention/experts, MEMORY on the KV cache and weights, COMMUNICATION on the router→experts links.

## SCENE 044 · s1202 · What you do when you can't buy your way out

| Field | Value |
|---|---|
| Time | 34:46–35:44 |
| Act | 12 — The Whole Machine |
| Manim class | `docu.scenes.act12.S1202TheAnswer` |
| Output | `scene_044.mp4` |
| Claims | V41-016 |
| Sources | V41_PAPER (§2.4.4) |
| Audio | music: resolution; SFX: none |
| Loop opened | — |
| Loop closed | L1 |

- **b1** — *So, back to the question we started with. What do you do when you can't simply buy your way out?*  
  → The central question from Act 1 returns to centre.
- **b2** — *You stop treating intelligence as a shopping problem, and start treating it as a physics problem. Where do the numbers go? How long do they …*  
  → The four questions appear one by one under the pillars.
- **b3** — *The constraint didn't make the problem easier. But it may have made understanding it more valuable. When you can't add more, you have to was…*  
  → The GPU wall from the opening returns — thinner, but every block lit and busy.
- **b4** — *And that leaves one question open. Everything in this story was about fitting the mathematics to hardware that already existed. DeepSeek eve…*  
  → A chip outline and an equation outline sit side by side, separate.
- **b5** — *So what happens when the algorithms and the hardware start being designed together, each one shaped around the other?*  
  → The chip and the equation slide together and interlock.
- **b6** — *That's a story for another time.*  
  → Fade to title card: 'DeepSeek Did the Impossible — The First-Principles Story of How'. Sources note.
