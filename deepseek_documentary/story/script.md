# Narration script — DeepSeek Did the Impossible — The First-Principles Story of How

Voice: Kokoro-82M (`am_michael`). Total runtime ≈ 35:49. Timestamps from the preview render when available. `[[ID]]` tags point to `research/claim_ledger.csv` and are not spoken.


---

## ACT 1 — The Impossible Constraint   ·   MUSIC: tension


### s0101 · Buy more GPUs


**[00:00–00:05]**

NARRATOR:
> For years, the race to build better AI looked almost embarrassingly simple.

[PAUSE 0.6s]

VISUAL: Black. A single small GPU block fades in at centre and hums.


SFX: hum


**[00:05–00:08]**

NARRATOR:
> Want a smarter model? Buy more GPUs.

[PAUSE 0.4s]

VISUAL: The block multiplies into a row, then a grid of dozens.


**[00:09–00:13]**

NARRATOR:
> Want it smarter still? Build a bigger data centre. Spend more money.

[PAUSE 0.4s]

VISUAL: Grid explodes to hundreds of blocks; camera pulls back; a pulse of light sweeps across them.


SFX: pulse


**[00:14–00:18]**

NARRATOR:
> Better intelligence, it seemed, was mostly a shopping problem.

[PAUSE 1.0s]

VISUAL: The wall of GPUs glows steadily. A thin price-tag label ticks upward.


### s0102 · Then the rules changed


**[00:20–00:21]**

NARRATOR:
> Then the rules changed.

[PAUSE 0.8s]

VISUAL: CUT TO BLACK. Silence. A timeline line draws across the screen.


SFX: impact


**[00:22–00:33]**

NARRATOR:
> In October 2022, the United States restricted exports of the most powerful AI chips, like NVIDIA's A100 and H100, to China. [[EXP-001]]

[PAUSE 0.4s]

VISUAL: Marker 'Oct 2022'. Chip cards A100 and H100 slide in, then receive a red 'restricted' bar.


**[00:34–00:44]**

NARRATOR:
> NVIDIA answered with China versions, the A800 and the H800. Nearly the same chips, but with slower connections between them. [[EXP-002]]

[PAUSE 0.4s]

VISUAL: Cards A800 and H800 appear under the timeline, their link-lines drawn thinner.


**[00:44–00:52]**

NARRATOR:
> A year later, in October 2023, the rules were tightened again, and the H800 itself was restricted. [[EXP-003]]

[PAUSE 0.4s]

VISUAL: Marker 'Oct 2023'. H800 and A800 receive red bars.


**[00:53–01:03]**

NARRATOR:
> And by April 2025, even the H20, a chip built specifically for the Chinese market, needed a US export licence. [[EXP-004]]

[PAUSE 1.0s]

VISUAL: Marker 'Apr 2025'. H20 card appears and is flagged 'licence required'. Source line fades in at bottom.


### s0103 · What if you can't buy your way out?

LOOP OPENED: L1 — How do you compete when you can't simply buy more compute?; L9 — What does '890 bytes' measure?


**[01:05–01:11]**

NARRATOR:
> In the middle of all this, a Chinese lab called DeepSeek published a model called DeepSeek V3.

[PAUSE 0.3s]

VISUAL: Timeline shrinks to the top. A clean model card 'DeepSeek-V3 · Dec 2024' fades in.


**[01:12–01:21]**

NARRATOR:
> They reported training it on a cluster of 2,048 H800s, the very chip that had been designed to sit just under the line. [[V3-004]]

[PAUSE 0.4s]

VISUAL: The card fills: 2,048 H800 GPUs. A small grid of 2,048 dots materialises beside it.


**[01:21–01:33]**

NARRATOR:
> The full training run, they said, took about 2.8 million GPU hours. [[V3-003]] And, by their own benchmarks, the model it produced was comparable to leading closed models. [[V3-012]]

[PAUSE 0.6s]

VISUAL: Line '2.788M H800 GPU-hours (reported)'. Tag 'reported by DeepSeek' in small caps.


**[01:34–01:41]**

NARRATOR:
> People called it impossible. It wasn't. But it was surprising. And the reason it was surprising is the whole story.

[PAUSE 0.8s]

VISUAL: The word IMPOSSIBLE appears large, then is crossed and replaced by SURPRISING.


**[01:42–01:50]**

NARRATOR:
> Because the real question isn't how many chips they had. It's this. What do you do when you can't simply buy your way out of a problem?

[PAUSE 1.0s]

VISUAL: Everything clears. The central question types itself onto the screen and stays.


**[01:51–02:07]**

NARRATOR:
> Less than two years later, DeepSeek published another paper, about a different wall entirely. Memory. They got one number down to 890 bytes. [[V41-003]] By the end of this video, you'll know exactly what that number measures, and why it matters.

[PAUSE 0.6s]

VISUAL: Question moves to top as a small persistent title. Big '890 bytes' appears with a '?' — then shrinks into the corner.


**[02:08–02:13]**

NARRATOR:
> But to get there, we have to start at the very bottom. With a single multiplication.

[PAUSE 1.2s]

VISUAL: Everything collapses into a single glowing dot at the centre.


SFX: whoosh


---

## ACT 2 — What Does Compute Even Mean?   ·   MUSIC: curious


### s0201 · One multiplication

LOOP OPENED: L2 — What does 'compute' actually mean?


**[02:15–02:19]**

NARRATOR:
> Here is the most important operation in all of modern AI. [[MATH]]

[PAUSE 0.5s]

VISUAL: The dot becomes the expression 3 × 4.


**[02:19–02:23]**

NARRATOR:
> Three times four. Twelve. That's it. One multiplication.

[PAUSE 0.6s]

VISUAL: 3 × 4 transforms into = 12. A small counter '1 operation' appears.


**[02:24–02:34]**

NARRATOR:
> Now let's give those numbers jobs. Suppose the three is a piece of information coming in, an input. And the four is how much we care about it. A weight.

[PAUSE 0.4s]

VISUAL: 3 gets a label 'input x', 4 gets 'weight w'. Colours shift to input-blue and parameter-amber.


**[02:35–02:46]**

NARRATOR:
> A neuron, in an artificial neural network, is barely more than this. It takes several inputs, multiplies each one by its own weight, and adds everything up.

[PAUSE 0.4s]

VISUAL: Three inputs on the left flow into a circle through three weighted edges; products appear on edges and sum into the neuron.


**[02:46–02:54]**

NARRATOR:
> Those weights are what people mean when they say a model has parameters. Every parameter is just one number, one of these weights.

[PAUSE 0.8s]

VISUAL: The weights glow amber; label 'parameters = the weights'.


### s0202 · Multiply, add, repeat


**[02:56–03:04]**

NARRATOR:
> Line the inputs up in a column, line the weights up in a row, and this whole neuron becomes one tidy operation. [[MATH]]

[PAUSE 0.4s]

VISUAL: The neuron diagram morphs into a row vector w and a column vector x.


**[03:04–03:11]**

NARRATOR:
> Multiply the first pair. The second pair. The third. Then add. Mathematicians call it a dot product.

[PAUSE 0.4s]

VISUAL: Pairs highlight one at a time; products drop into a running sum; label 'dot product'.


**[03:12–03:23]**

NARRATOR:
> Notice what it cost. Three multiplications, and a few additions. People lump a multiply and an add together and count them as floating point operations. FLOPs.

[PAUSE 0.4s]

VISUAL: Counter ticks: 3 multiplies, 2 adds. The word FLOP is defined underneath.


**[03:23–03:28]**

NARRATOR:
> Hold on to that word. Everything in this story is going to be measured in it.

[PAUSE 0.8s]

VISUAL: The word FLOP brightens and slides to the top-right as a persistent unit label.


### s0203 · Rows meet columns


**[03:30–03:40]**

NARRATOR:
> A real layer doesn't have one neuron. It has many, all looking at the same inputs. Stack their weight rows on top of each other, and you get a matrix. [[MATH]]

[PAUSE 0.4s]

VISUAL: One weight row duplicates into three rows, forming a 3 by 3 matrix W beside input vector x.


**[03:40–03:49]**

NARRATOR:
> Each row meets the input, does its dot product, and produces one output. Row one, output one. Row two, output two.

[PAUSE 0.3s]

VISUAL: Row 1 slides over x, multiplies, yields y1. Row 2 yields y2. Row 3 yields y3.


**[03:49–03:58]**

NARRATOR:
> And if we feed in three inputs at once, three tokens say, it becomes a matrix times a matrix. Every row meets every column.

[PAUSE 0.3s]

VISUAL: x widens into a 3 by 3 matrix X. Result grid fills cell by cell as rows sweep across columns.


**[03:58–04:07]**

NARRATOR:
> Three rows, three columns, three multiplications each. Twenty-seven multiplications, for the smallest matrix you can draw. [[GEN-002]]

[PAUSE 0.8s]

VISUAL: Counter races to 27. Equation (m×n)·(n×p) → m·n·p multiplications appears.


### s0204 · From twenty-seven to billions


**[04:09–04:18]**

NARRATOR:
> Now the real thing. Inside DeepSeek V3, each token is represented by 7,168 numbers. [[V3-008]]

[PAUSE 0.4s]

VISUAL: The 3×3 matrix zooms out; grid lines multiply until the matrix is a fine texture labelled 7168 × 7168.


**[04:18–04:28]**

NARRATOR:
> Pushing one token through a single square matrix of that size takes about 51 million multiplications. [[DER-006]] One token. One matrix.

[PAUSE 0.5s]

VISUAL: Counter jumps from 27 to 51,380,224.


**[04:28–04:42]**

NARRATOR:
> A model is hundreds of these matrices, stacked in layers. A useful rule of thumb: running a model costs about two operations for every parameter it uses, for every token it reads or writes. [[GEN-003]]

[PAUSE 0.4s]

VISUAL: Matrices stack into a tall column of layers; the rule '≈ 2 FLOPs × active parameters × tokens' writes out.


**[04:43–04:53]**

NARRATOR:
> For V3, with its 37 billion active parameters, that's roughly 74 billion operations. [[DER-005]] For every single word fragment it produces.

[PAUSE 0.6s]

VISUAL: 37,000,000,000 × 2 → ≈ 74 billion FLOPs per token. A token block flashes.


**[04:54–05:04]**

NARRATOR:
> So that's what compute is. Not magic. Not thinking, exactly. Multiplication and addition, repeated an astronomical number of times.

[PAUSE 0.4s]

VISUAL: Zoom out: the layer stack becomes a tiny glowing speck among countless others.


**[05:04–05:09]**

NARRATOR:
> Which raises an obvious question. What kind of machine can do that fast enough?

[PAUSE 1.0s]

VISUAL: The speck becomes a single GPU block outline.


LOOP CLOSED: L2 — What does 'compute' actually mean?


---

## ACT 3 — Why GPUs Matter   ·   MUSIC: pulse


### s0301 · One lane or ten thousand


**[05:11–05:20]**

NARRATOR:
> A normal processor, a CPU, is built like a few brilliant specialists. Each one is fast and clever, but there are only a handful of them.

[PAUSE 0.3s]

VISUAL: Left: a CPU with 8 large cores. Multiplication tasks queue up and pass through in sequence.


**[05:21–05:26]**

NARRATOR:
> Give them a matrix multiplication, and they mostly work through it a chunk at a time.

[PAUSE 0.3s]

VISUAL: A 16x16 result grid fills slowly, cell groups lighting in order.


**[05:26–05:36]**

NARRATOR:
> But look at what a matrix multiplication actually is. Every output cell is its own little dot product. None of them needs to wait for any other. [[MATH]]

[PAUSE 0.4s]

VISUAL: Grid cells separate slightly; each shows a tiny independent row·column icon.


**[05:36–05:49]**

NARRATOR:
> A graphics processor, a GPU, bets everything on that fact. Instead of a few clever cores, it has thousands of simple ones, all doing multiply and add at the same time.

[PAUSE 0.3s]

VISUAL: Right: GPU block with a dense grid of tiny cores. The same 16x16 grid fills almost at once.


SFX: pulse


**[05:49–06:02]**

NARRATOR:
> That's why GPUs, originally built to colour in pixels for video games, became the engines of AI. The mathematics of neural networks is, almost perfectly, parallel.

[PAUSE 0.8s]

VISUAL: Side-by-side race: CPU grid is still 10% full when GPU grid finishes.


### s0302 · The pipe, not the engine

LOOP OPENED: L3 — Why aren't more GPUs enough?


**[06:04–06:12]**

NARRATOR:
> But here's the thing most people miss. Doing the arithmetic is only half the job. The numbers have to get to the cores first.

[PAUSE 0.4s]

VISUAL: GPU core grid on the right; on the left a large memory bank labelled HBM; a pipe connects them.


**[06:12–06:24]**

NARRATOR:
> The weights live in memory. Every time you use them, they have to travel through a pipe into the compute units. And that pipe has a width. Bandwidth. How many bytes per second can flow.

[PAUSE 0.4s]

VISUAL: Number-particles flow along the pipe. Pipe width is annotated 'bandwidth (bytes / s)'.


**[06:24–06:36]**

NARRATOR:
> If the cores can eat numbers faster than the pipe can deliver them, the cores sit idle. Waiting. And a waiting GPU is the most expensive way to do nothing ever invented.

[PAUSE 0.5s]

VISUAL: Pipe narrows; particles trickle; cores dim one by one; label 'idle'.


**[06:37–06:50]**

NARRATOR:
> So there are really three walls. Compute: how fast you can multiply. Memory: how much you can hold, and how fast you can read it. And communication: how fast separate chips can talk to each other.

[PAUSE 0.4s]

VISUAL: Three tall pillars rise, colour-coded: COMPUTE (orange), MEMORY (teal), COMMUNICATION (violet).


**[06:51–06:58]**

NARRATOR:
> Keep these three walls in mind. Every clever idea in the rest of this story is an attack on one of them.

[PAUSE 0.8s]

VISUAL: The three pillars shrink into a small persistent legend at the bottom-left.


### s0303 · Same engine, narrower pipes


**[06:59–07:14]**

NARRATOR:
> Now, a model the size of V3 doesn't fit on one GPU. Even stored at just one byte per parameter, its weights would need more than eight GPUs' worth of fast memory, before you've done anything at all. [[DER-004]] [[EXP-006]]

[PAUSE 0.4s]

VISUAL: A long bar '671 GB of weights' next to a single GPU's '80 GB' bar; the weights bar is split across 9 GPU blocks.


**[07:14–07:25]**

NARRATOR:
> So the model gets split across many GPUs, and those GPUs have to constantly exchange numbers. The connections between them become part of the computer.

[PAUSE 0.4s]

VISUAL: Nine GPUs arranged in a ring; links draw between them; numbers flow along the links.


**[07:26–07:43]**

NARRATOR:
> And this is exactly where the export rules bit. The H800 kept essentially the same engine as the H100. What got cut was the pipe between chips. Widely reported as about 400 gigabytes per second, instead of 900. [[EXP-005]]

[PAUSE 0.5s]

VISUAL: Two GPU pairs side by side: H100 pair with a thick link '≈900 GB/s', H800 pair with a thinner link '≈400 GB/s'. Label 'widely reported'.


**[07:44–07:57]**

NARRATOR:
> Same engine. Narrower pipes. Remember that, because it's going to matter much more than it seems right now. And it raises a question we'll come back to. If you can just add more chips, why isn't that enough?

[PAUSE 1.0s]

VISUAL: The thinner H800 link pulses. The question 'Why aren't more GPUs enough?' appears and pins to the corner.


---

## ACT 4 — Inside a Transformer   ·   MUSIC: minimal


### s0401 · What does 'it' mean?

LOOP OPENED: L4 — What does 'it' refer to, and how can a machine know?


**[07:59–08:07]**

NARRATOR:
> So we know the hardware. But what is all that multiplication actually for? Let's open up a language model and look.

[PAUSE 0.4s]

VISUAL: Camera flies into the GPU block; the grid dissolves into darkness.


SFX: whoosh


**[08:08–08:12]**

NARRATOR:
> Here's a sentence. The animal didn't cross the street because it was tired.

[PAUSE 0.6s]

VISUAL: The sentence types across the screen.


**[08:13–08:16]**

NARRATOR:
> Question. What does it refer to? The animal, or the street?

[PAUSE 0.8s]

VISUAL: 'it' highlights; two arcs reach tentatively to 'animal' and 'street'.


**[08:17–08:27]**

NARRATOR:
> You knew instantly. The animal. Streets don't get tired. But notice how you knew. You looked at other words in the sentence and pulled their meaning into this one.

[PAUSE 0.4s]

VISUAL: Arc to 'animal' strengthens, to 'street' fades; 'tired' glows as the clue.


**[08:28–08:35]**

NARRATOR:
> A model has to do the same thing, with nothing but numbers. So first, the text becomes pieces. Tokens.

[PAUSE 0.6s]

VISUAL: The sentence splits into rounded token blocks with small gaps; the token colour is established.


### s0402 · Words as arrows


**[08:37–08:42]**

NARRATOR:
> Each token is then swapped for a list of numbers. A vector. We call it an embedding.

[PAUSE 0.4s]

VISUAL: Token 'animal' drops down; a column of 6 numbers unrolls beneath it.


**[08:42–08:50]**

NARRATOR:
> Real models use thousands of numbers per token. We'll draw just two, so we can see them as an arrow on a page.

[PAUSE 0.3s]

VISUAL: The column compresses into a 2D arrow on a small plane.


**[08:50–09:02]**

NARRATOR:
> These numbers are learned. During training, words that behave alike drift near each other. Animal lands near dog. Street lands near road. Tired lands near sleepy.

[PAUSE 0.5s]

VISUAL: Plane fills with labelled arrows clustering: animal/dog/cat; street/road; tired/sleepy.


**[09:03–09:12]**

NARRATOR:
> Meaning, in a model, is a direction. And that means we can measure how related two words are with the operation we already know. The dot product.

[PAUSE 0.8s]

VISUAL: Two arrows animal and dog; the angle between them is shaded; 'a · b' appears.


### s0403 · Questions and advertisements


**[09:14–09:25]**

NARRATOR:
> Here's the trick at the heart of every modern language model. Each token makes three new vectors from its embedding, each by multiplying with its own learned matrix.

[PAUSE 0.4s]

VISUAL: Token 'it' with its embedding; three arrows fan out to vectors labelled Q, K, V, each via a small matrix W_Q, W_K, W_V.


**[09:25–09:31]**

NARRATOR:
> A query. What am I looking for? For it, something like: which noun am I talking about?

[PAUSE 0.3s]

VISUAL: Q vector highlights with a speech-bubble paraphrase 'which noun am I?'


**[09:31–09:38]**

NARRATOR:
> A key. What do I have to offer? Every token advertises itself. Animal says: I'm a living thing, a noun.

[PAUSE 0.3s]

VISUAL: Every token shows a small K tag; 'animal' K bubble: 'living noun'.


**[09:39–09:44]**

NARRATOR:
> And a value. If you do pay attention to me, here's the information I'll hand over.

[PAUSE 0.4s]

VISUAL: V tags appear beneath each token as small filled bars.


**[09:44–09:57]**

NARRATOR:
> To decide where it should look, we take its query, and dot it with the key of every word so far. A model that writes left to right can only look back. A big result means a good match.

[PAUSE 0.4s]

VISUAL: Q of 'it' sweeps across all K's; score numbers pop above each earlier token: animal highest, street next; later tokens are masked.


**[09:57–10:06]**

NARRATOR:
> Do this for every token at once, and those dot products form a grid. Query times key transpose. Q K transpose. [[GEN-001]]

[PAUSE 0.8s]

VISUAL: Scores assemble into an n×n grid (heatmap), upper triangle masked (causal); QKᵀ writes beside it.


### s0404 · Scores into attention


**[10:08–10:18]**

NARRATOR:
> But raw scores are awkward. They can be negative, and they don't add up to anything in particular. We want percentages. How much attention should go where. [[MATH]]

[PAUSE 0.4s]

VISUAL: Row of scores for 'it' shown as bars, some negative.


**[10:18–10:27]**

NARRATOR:
> So we do two things. First, raise e to the power of each score. Everything becomes positive, and big scores become much bigger.

[PAUSE 0.4s]

VISUAL: Each bar transforms through e^x: all positive, the 'animal' bar dominates.


**[10:27–10:33]**

NARRATOR:
> Then divide each by the total. Now they add up to one. This is called softmax.

[PAUSE 0.4s]

VISUAL: Bars normalise into a stacked 100% bar; formula softmax(s_i) = e^{s_i} / Σ e^{s_j}.


**[10:34–10:48]**

NARRATOR:
> One more small detail. Before the softmax, the scores are divided by the square root of the vector length. Long vectors produce huge dot products, and this keeps the softmax from becoming too sharp to learn.

[PAUSE 0.4s]

VISUAL: QKᵀ becomes QKᵀ/√d inside softmax(...).


**[10:48–10:55]**

NARRATOR:
> And here's the result. It sends most of its attention to animal. The model has worked out what you worked out.

[PAUSE 0.8s]

VISUAL: Attention arcs from 'it' drawn with thickness = weight; the arc to 'animal' thickest.


### s0405 · Borrowing meaning


**[10:57–11:04]**

NARRATOR:
> Now it collects its reward. Take each token's value vector, scale it by its attention weight, and add them all up.

[PAUSE 0.4s]

VISUAL: Value bars shrink or grow by weight and fly into 'it', summing into a new vector.


**[11:05–11:10]**

NARRATOR:
> The new vector for it is no longer just it. It now carries a large dose of animal.

[PAUSE 0.4s]

VISUAL: The 'it' embedding arrow rotates toward the 'animal' cluster on the 2D plane.


**[11:11–11:21]**

NARRATOR:
> Put together, the whole mechanism fits on one line. Attention of Q, K and V equals softmax of Q K transpose over root d, times V. [[GEN-001]]

[PAUSE 0.6s]

VISUAL: Full equation Attention(Q,K,V) = softmax(QKᵀ/√d)V assembles from the pieces already on screen.


**[11:22–11:37]**

NARRATOR:
> Look at it again, though. Three matrix multiplications to make Q, K and V. One to compare everything with everything. One more to blend the values. It's our old friend, multiply and add, all the way down.

[PAUSE 0.8s]

VISUAL: Each matmul in the equation flashes compute-orange in turn.


LOOP CLOSED: L4 — What does 'it' refer to, and how can a machine know?


### s0406 · Many heads, then thinking


**[11:38–11:51]**

NARRATOR:
> One attention pattern can only capture one kind of relationship at a time. So models run many in parallel, each with its own Q, K and V matrices. They're called heads.

[PAUSE 0.4s]

VISUAL: The single attention heatmap splits into 4 smaller heatmaps with different patterns (pronouns, neighbours, verbs, punctuation).


**[11:51–12:02]**

NARRATOR:
> One head might track pronouns. Another, which word came just before. Another, subject and verb. Nobody tells them to. They specialise on their own.

[PAUSE 0.4s]

VISUAL: Each head gets a tentative caption; captions marked 'illustrative'.


**[12:02–12:17]**

NARRATOR:
> After attention comes the second half of each block. A feed-forward network. Two big matrices applied to each token on its own. If attention is where tokens talk to each other, this is where each token thinks it over.

[PAUSE 0.4s]

VISUAL: Block diagram: [Attention] → [Feed-forward]; inside FFN a wide matrix expands then contracts the vector.


**[12:17–12:27]**

NARRATOR:
> And in large models, most of the parameters live right here, in these feed-forward matrices. [[GEN-005]] Remember that. It's about to become important.

[PAUSE 0.8s]

VISUAL: A parameter-share bar: FFN takes the large majority; label 'most parameters live here' (general rule of thumb).


### s0407 · Stack, and predict


**[12:29–12:34]**

NARRATOR:
> Attention, then feed-forward. That's one block. Now stack them. Dozens of times.

[PAUSE 0.3s]

VISUAL: The block duplicates upwards into a tall tower of layers.


**[12:35–12:45]**

NARRATOR:
> At the top, the final vector is compared against every token in the vocabulary, and turned, with softmax again, into a probability for what comes next.

[PAUSE 0.4s]

VISUAL: Top of tower emits a probability bar chart over candidate next tokens: 'and' 0.41, '.' 0.22, 'so' 0.12...


**[12:45–12:54]**

NARRATOR:
> Pick one. Add it to the text. Run the whole thing again. That's how every chatbot you've ever used writes. One token at a time.

[PAUSE 0.4s]

VISUAL: Chosen token flies back to the input sequence; tower pulses again.


**[12:54–12:58]**

NARRATOR:
> That's a Transformer. And now we can see the problem coming.

[PAUSE 1.0s]

VISUAL: Camera pulls back; the tower sits small in the frame.


---

## ACT 5 — The Computational Explosion   ·   MUSIC: rising


### s0501 · Bigger, and bigger


**[13:00–13:09]**

NARRATOR:
> Researchers kept discovering the same thing. Make the model bigger, train it on more text, and it gets better. Smoothly, predictably, better.

[PAUSE 0.4s]

VISUAL: A rising curve 'capability vs. scale' draws itself (schematic, no numbers).


**[13:10–13:18]**

NARRATOR:
> So they made them bigger. More layers. Wider matrices. More heads. And every one of those multiplies the parameter count.

[PAUSE 0.3s]

VISUAL: The tower grows taller; each layer grows wider; a parameter counter spins upward.


**[13:18–13:30]**

NARRATOR:
> But remember our rule of thumb. Two operations per parameter, per token. [[GEN-003]] In an ordinary, dense model, every single token has to pass through every single weight.

[PAUSE 0.4s]

VISUAL: A token block travels up the tower; every matrix it passes lights up. All of them.


**[13:30–13:35]**

NARRATOR:
> Double the model, double the cost of every word. Forever. For every user.

[PAUSE 0.8s]

VISUAL: Two towers, the second twice as big; cost meter under each, the second twice as high.


### s0502 · Do we need all of it?

LOOP OPENED: L5 — Does a model need all of itself for every token?


**[13:37–13:42]**

NARRATOR:
> Now think about what that means in practice. You ask a giant model, what's two plus two.

[PAUSE 0.4s]

VISUAL: Token stream '2 + 2 =' enters the tower.


**[13:43–13:53]**

NARRATOR:
> And to answer, it fires every weight it has. Including the ones that learned French poetry, and medieval history, and how to write a SQL query.

[PAUSE 0.4s]

VISUAL: Regions inside the tower are faintly labelled: poetry, history, code, biology, maths; all light up.


**[13:53–13:59]**

NARRATOR:
> That seems wasteful. When you do arithmetic, you don't consult everything you know about poetry.

[PAUSE 0.5s]

VISUAL: Only the maths region stays bright; the others dim.


**[14:00–14:08]**

NARRATOR:
> So here's the question that changes everything. What if a model didn't need to use all of itself, every single time?

[PAUSE 1.2s]

VISUAL: The question types out; the tower splits into faint separate blocks behind it.


---

## ACT 6 — Mixture of Experts   ·   MUSIC: discovery


### s0601 · Splitting the thinker


**[14:10–14:16]**

NARRATOR:
> Go back to the feed-forward network, the part of each block where most of the parameters live.

[PAUSE 0.3s]

VISUAL: One Transformer block; the FFN box highlights.


**[14:16–14:26]**

NARRATOR:
> Now, instead of one huge feed-forward network, cut it into several smaller ones. Each is a complete little network on its own. We'll call them experts.

[PAUSE 0.4s]

VISUAL: The FFN box slices into 8 smaller boxes E1..E8, each in expert-green.


**[14:27–14:33]**

NARRATOR:
> Here's the key idea. For any given token, we only run a few of them. The rest stay switched off.

[PAUSE 0.4s]

VISUAL: Two of the 8 light up; six stay dark.


**[14:33–14:42]**

NARRATOR:
> The model can hold the knowledge of all eight experts. But each token only pays for two. This is called a Mixture of Experts.

[PAUSE 0.8s]

VISUAL: Labels: 'stored: 8 experts' vs 'computed: 2 experts'. Title 'Mixture of Experts (MoE)'.


### s0602 · Who decides?


**[14:44–14:49]**

NARRATOR:
> Which raises an obvious question. Who decides which experts a token should visit?

[PAUSE 0.4s]

VISUAL: A token hovers in front of 8 experts; question mark.


**[14:50–14:57]**

NARRATOR:
> Another small learned piece of the network. A router. It looks at the token and gives every expert a score.

[PAUSE 0.4s]

VISUAL: A router diamond appears between token and experts; score bars rise above each expert.


**[14:57–15:03]**

NARRATOR:
> Watch what happens with different tokens. The word integral lights up one pair of experts.

[PAUSE 0.3s]

VISUAL: Token 'integral' → router → experts E2 and E5 light.


**[15:03–15:11]**

NARRATOR:
> The code word def lights up a different pair. The word mitochondria, another. Even a word like the gets its own routing.

[PAUSE 0.5s]

VISUAL: Tokens 'def', 'mitochondria', 'the' route to different expert pairs in turn.


**[15:12–15:26]**

NARRATOR:
> Nobody hand-assigns topics. The router and the experts learn together, and the specialisation emerges from training. Real experts rarely map to tidy human subjects. We're simplifying for the picture.

[PAUSE 0.8s]

VISUAL: Expert topic captions fade to '?'; disclaimer 'illustrative labels'.


### s0603 · The mathematics of choosing


**[15:28–15:37]**

NARRATOR:
> In symbols, it's short. The router is just a matrix. Multiply the token's vector by it, and you get one score per expert. [[MATH]]

[PAUSE 0.4s]

VISUAL: s = W_r x; vector of 8 scores.


**[15:37–15:43]**

NARRATOR:
> Turn the scores into weights, keep only the top k, and throw the rest away. That's top k routing.

[PAUSE 0.4s]

VISUAL: Scores → gate weights g_i; top-2 highlighted; the others crossed out.


**[15:44–15:54]**

NARRATOR:
> The output is the chosen experts' answers, blended by their weights. The same weighted-sum trick as attention, just applied to experts instead of words.

[PAUSE 0.4s]

VISUAL: y = Σ_{i ∈ top-k} g_i · E_i(x); two expert outputs scale and merge.


**[15:55–16:07]**

NARRATOR:
> But there's a trap. If the router falls in love with one expert, every token piles into it, while the others sit idle. You'd have a giant model, secretly behaving like a small one.

[PAUSE 0.4s]

VISUAL: Tokens stream toward E3; E3's load bar overflows; others empty.


**[16:08–16:23]**

NARRATOR:
> So training has to balance the load. DeepSeek does it by nudging each expert's score up or down, depending on how busy it has been. In V4.1 Flash, they even keep separate nudges for text and for images. [[V41-017]]

[PAUSE 0.8s]

VISUAL: Small bias arrows adjust each expert's score; load bars even out.


### s0604 · DeepSeek's version

LOOP OPENED: L6 — Where do experts live, and how do tokens reach them?


**[16:25–16:36]**

NARRATOR:
> DeepSeek pushed this idea further than most. Two changes. First, lots of small experts instead of a few big ones, so tokens can mix and match more precisely.

[PAUSE 0.3s]

VISUAL: 8 big experts shatter into a dense grid of 64 small ones.


**[16:37–16:46]**

NARRATOR:
> Second, one shared expert that every token always visits, to hold common knowledge, so the specialists don't all have to relearn the basics.

[PAUSE 0.4s]

VISUAL: A distinct shared expert slab appears at left, connected to every token.


**[16:46–16:54]**

NARRATOR:
> DeepSeek V2 had 236 billion parameters, but only about 21 billion active per token. [[V2-001]]

[PAUSE 0.3s]

VISUAL: Bar: 236B total, 21B lit.


**[16:55–17:07]**

NARRATOR:
> V3 went further. In each of its expert layers, 256 routed experts plus one shared expert. Each token visits just 8 of the 256. [[V3-008]]

[PAUSE 0.3s]

VISUAL: Grid of 256 small experts + 1 shared; 8 light up for a passing token.


**[17:07–17:16]**

NARRATOR:
> 671 billion parameters stored. 37 billion used for any one token. [[V3-001]] About five and a half percent. [[DER-007]]

[PAUSE 0.5s]

VISUAL: Bar 671B with a 37B sliver lit; '≈ 5.5% active'.


**[17:17–17:27]**

NARRATOR:
> And the 2026 model, V4.1 Flash, uses 384 routed experts per layer, with 6 chosen for each token. [[V41-007]]

[PAUSE 0.4s]

VISUAL: Grid morphs to 384 experts; 6 lit.


**[17:28–17:39]**

NARRATOR:
> So a model can be enormous, and still cheap to run, per token. That answers our question. But it creates a brand new one. Where do all these experts actually live?

[PAUSE 1.0s]

VISUAL: Expert grid pulls apart into clusters, each cluster sitting on a GPU block.


LOOP CLOSED: L5 — Does a model need all of itself for every token?


---

## ACT 7 — The Communication Problem   ·   MUSIC: tension


### s0701 · Experts on islands


**[17:41–17:53]**

NARRATOR:
> Remember, a model like V3 is far too big for one GPU. So the experts are spread out. A few here, a few there, across many GPUs, across many machines.

[PAUSE 0.4s]

VISUAL: Four GPU islands, each hosting a cluster of expert squares.


**[17:54–18:05]**

NARRATOR:
> Now follow a single token. The router says: you need expert 12, expert 97, and expert 200. And they're on three different GPUs.

[PAUSE 0.4s]

VISUAL: A token on island 1; router marks three experts on islands 2, 3, 4; dotted paths appear.


**[18:05–18:12]**

NARRATOR:
> So the token's vector has to be sent there. Computed. And the results sent back. Dispatch, then combine.

[PAUSE 0.3s]

VISUAL: Token copies fly out along the paths, experts flash, results fly back and merge.


**[18:12–18:25]**

NARRATOR:
> Now do that for every token in a batch, at every expert layer. Every GPU is sending to every other GPU, all at once. Engineers call it all to all communication.

[PAUSE 0.8s]

VISUAL: Dozens of tokens; paths from every island to every island form a dense web.


SFX: whoosh


### s0702 · The cost of waiting


**[18:27–18:36]**

NARRATOR:
> Let's draw what one GPU's time looks like. Compute. Then wait for tokens to arrive. Compute. Wait for results to come back.

[PAUSE 0.4s]

VISUAL: A horizontal timeline: orange compute blocks alternating with violet communication blocks, with grey idle gaps.


**[18:37–18:46]**

NARRATOR:
> Those grey gaps are the GPU doing nothing, while its numbers are stuck in the wires. And the narrower the wire, the longer the gaps.

[PAUSE 0.4s]

VISUAL: Communication blocks stretch; idle gaps widen.


**[18:46–19:00]**

NARRATOR:
> Now you can see why the H800's narrower links mattered. MoE saves compute, but it spends communication. And communication was exactly the resource the export rules had squeezed. [[EXP-005]]

[PAUSE 0.4s]

VISUAL: Label 'H800: narrower links'; the violet blocks swell further. The legend's COMMUNICATION pillar glows.


**[19:00–19:17]**

NARRATOR:
> That's the answer to the question from earlier. Why aren't more GPUs enough? Because every GPU you add is another island, and islands have to talk. Past a point, you're not limited by how fast you can think. You're limited by how fast you can talk.

[PAUSE 1.0s]

VISUAL: Island count grows 4 → 16; link web thickens; utilisation meter drops.


LOOP CLOSED: L3 — Why aren't more GPUs enough?


### s0703 · Hiding the wait


**[19:19–19:24]**

NARRATOR:
> DeepSeek's answer for V3 wasn't a faster wire. It was a smarter schedule.

[PAUSE 0.4s]

VISUAL: Timeline from before returns.


**[19:25–19:37]**

NARRATOR:
> The idea is simple to say and very hard to build. While one batch of tokens is travelling, compute on a different batch. Keep the engine busy while the mail is in the post.

[PAUSE 0.4s]

VISUAL: Two interleaved timelines slide together so communication of batch A overlaps compute of batch B; idle gaps vanish.


**[19:37–19:47]**

NARRATOR:
> They called their pipeline schedule DualPipe, and wrote custom communication code so that computation and communication overlap almost completely. [[V3-011]]

[PAUSE 0.4s]

VISUAL: Label 'DualPipe (DeepSeek-V3)'; the overlapped timeline is solid orange with violet underneath.


**[19:47–20:01]**

NARRATOR:
> Then they attacked the size of the mail itself. Numbers in a computer take up space. A common format uses 16 bits for each one. V3 trained with much of its maths in just 8 bits. [[V3-006]]

[PAUSE 0.4s]

VISUAL: A 16-bit box of cells shrinks to an 8-bit box; label 'FP8'.


**[20:01–20:14]**

NARRATOR:
> Half the bits means half the bytes to store, half the bytes to move, and faster arithmetic on hardware built for it. DeepSeek says V3 was the first to prove this works at such a scale. [[V3-006]]

[PAUSE 0.5s]

VISUAL: Tokens in the pipe shrink to half size; twice as many fit through the same pipe.


**[20:14–20:21]**

NARRATOR:
> It's a pattern worth noticing. Not more hardware. A better understanding of where the time was actually going.

[PAUSE 1.0s]

VISUAL: The three-pillar legend: COMPUTE and COMMUNICATION pillars get a checkmark tick.


LOOP CLOSED: L6 — Where do experts live, and how do tokens reach them?


---

## ACT 8 — The Memory Wall   ·   MUSIC: minimal


### s0801 · Writing one token at a time


**[20:24–20:30]**

NARRATOR:
> There's one wall left. And it's the one that shows up when you actually use these models. Memory.

[PAUSE 0.5s]

VISUAL: The MEMORY pillar in the legend glows and moves to centre.


**[20:30–20:38]**

NARRATOR:
> Remember how a model writes. One token at a time. Each new token looks back, with attention, at every token before it.

[PAUSE 0.4s]

VISUAL: A sequence of tokens; a new token appears at the end and draws attention arcs to all previous tokens.


**[20:39–20:50]**

NARRATOR:
> To do that, it needs every earlier token's key and value. Now, those don't change. The key for animal is the same at word ten as it was at word five.

[PAUSE 0.4s]

VISUAL: Each earlier token shows its K and V tags, frozen.


**[20:50–21:01]**

NARRATOR:
> So instead of recomputing them for every new word, the model saves them. A shelf of keys and values that grows by one entry per token. The KV cache.

[PAUSE 0.8s]

VISUAL: K,V tags slide off onto a shelf below; each new token adds a box to the shelf. Label 'KV cache'.


### s0802 · How big is the shelf?

LOOP OPENED: L7 — How small can a memory of the past be?


**[21:03–21:11]**

NARRATOR:
> Let's measure the shelf. For ordinary attention, each token stores a key and a value, for every head, in every layer. [[MATH]]

[PAUSE 0.4s]

VISUAL: Formula: bytes/token = 2 × layers × heads × head_dim × bytes.


**[21:11–21:27]**

NARRATOR:
> Here's a hypothetical. If a model with V3's shape had used ordinary attention, with 128 heads of 128 numbers, over 61 layers, that's about 4 megabytes, for every single token. [[DER-002]] [[V3-008]]

[PAUSE 0.4s]

VISUAL: Numbers plug in: 2 × 61 × 128 × 128 × 2 bytes ≈ 4.0 MB. Tag 'hypothetical, our arithmetic'.


**[21:27–21:36]**

NARRATOR:
> Now a long conversation. A hundred and twenty eight thousand tokens. That's over five hundred gigabytes. For one conversation. [[DER-002]]

[PAUSE 0.5s]

VISUAL: The shelf stretches far off-screen; a memory bar climbs past six stacked 80 GB GPU lines.


**[21:37–21:52]**

NARRATOR:
> The weights are shared by every user. But this cache is personal. Every conversation carries its own. That's what fills the memory of a GPU during serving, and it's what limits how many people one machine can serve at once.

[PAUSE 0.4s]

VISUAL: Several users, each with their own shelf, all trying to fit into one GPU's memory box. It overflows.


**[21:52–21:57]**

NARRATOR:
> So the question becomes: how small can a memory of the past possibly be?

[PAUSE 1.0s]

VISUAL: Question types out and pins to the corner.


### s0803 · Compress the memory


**[22:00–22:06]**

NARRATOR:
> DeepSeek's first big answer, back in V2, was called Multi-head Latent Attention. M L A.

[PAUSE 0.4s]

VISUAL: Title 'Multi-head Latent Attention (MLA) · DeepSeek-V2'.


**[22:07–22:25]**

NARRATOR:
> Here's the intuition. All those keys and values, across all the heads, are made from the same token. They're highly redundant. So instead of storing them all, store one small compressed summary, a latent vector, and rebuild the keys and values from it when you need them.

[PAUSE 0.4s]

VISUAL: A tall stack of 128 K/V head strips squeezes through a funnel into one thin latent bar, then expands back into heads on the other side.


**[22:25–22:36]**

NARRATOR:
> The rebuild is just another matrix multiplication. And multiplication is the thing GPUs have in abundance. You're trading cheap compute for expensive memory.

[PAUSE 0.4s]

VISUAL: The expansion step is labelled 'W_up · c (compute)'; the latent bar labelled 'stored (memory)'.


**[22:36–22:51]**

NARRATOR:
> In V3's published configuration, each token stores a 512 number summary, plus 64 numbers for position. [[V3-009]] 576 numbers, instead of roughly 32 thousand. [[V3-010]]

[PAUSE 0.4s]

VISUAL: Two bars: 32,768 vs 576, scaled correctly.


**[22:51–23:02]**

NARRATOR:
> When they introduced it in V2, DeepSeek reported a 93.3 percent cut in KV cache compared with their earlier 67 billion parameter model. [[V2-002]]

[PAUSE 0.8s]

VISUAL: Citation card: DeepSeek-V2 · −93.3% KV cache vs DeepSeek 67B.


### s0804 · Three dials


**[23:04–23:09]**

NARRATOR:
> Now step back. The size of the cache is really three numbers multiplied together. [[V41-018]]

[PAUSE 0.4s]

VISUAL: Equation: cache = (size of each entry) × (number of entries along the sequence) × (number of layers keeping one).


**[23:10–23:17]**

NARRATOR:
> How big each entry is. How many entries you keep along the sequence. And how many layers keep their own.

[PAUSE 0.4s]

VISUAL: Three dials appear: ENTRY SIZE, SEQUENCE, LAYERS.


**[23:17–23:24]**

NARRATOR:
> MLA turned the first dial. Make each entry smaller. But the other two dials were still there, untouched.

[PAUSE 0.4s]

VISUAL: ENTRY SIZE dial turns down; the other two stay at max.


**[23:25–23:32]**

NARRATOR:
> And by 2026, a new kind of workload was about to make those two dials the only ones that mattered.

[PAUSE 1.0s]

VISUAL: SEQUENCE and LAYERS dials pulse.


---

## ACT 9 — DeepSeek-V4.1-Flash: Pushing the Memory Wall   ·   MUSIC: discovery


### s0901 · The agent problem


**[23:34–23:45]**

NARRATOR:
> By 2026, people weren't just chatting with models. They were handing them jobs. Read this code base. Run the tests. Fix the bug. Try again.

[PAUSE 0.4s]

VISUAL: A loop diagram: model → tool call → result → model, spinning, with the context bar growing each lap.


**[23:45–23:58]**

NARRATOR:
> Every tool call pours more text back into the context. The inputs grow enormous, the outputs stay small. DeepSeek describes these workloads as increasingly input heavy. [[V41-019]]

[PAUSE 0.4s]

VISUAL: Input bar balloons, output bar stays thin; label 'input-heavy'.


**[23:58–24:14]**

NARRATOR:
> In September 2026, DeepSeek published a paper about exactly this, for a model called DeepSeek V4.1 Flash. 552 billion backbone parameters, and contexts of up to a million tokens. [[V41-001]]

[PAUSE 0.4s]

VISUAL: Paper card: 'DeepSeek-V4.1-Flash: Pushing the Limits of KV Cache Compression · arXiv 2609.19969'. Stats appear.


**[24:15–24:29]**

NARRATOR:
> And the paper is candid about the bottleneck. Earlier sparse attention had already tamed much of the compute cost of long contexts, which left storage and data movement as the prominent bottlenecks. The KV cache. [[V41-020]]

[PAUSE 0.8s]

VISUAL: Legend: COMPUTE pillar dims (tamed); MEMORY and COMMUNICATION pillars flare.


### s0902 · Don't look at everything


**[24:31–24:38]**

NARRATOR:
> First, the sequence dial. When a new token is written, does it really need to look at all million earlier tokens? [[V41-001]]

[PAUSE 0.4s]

VISUAL: A new token and a very long strip of past entries; attention lines to all of them, too dense to see.


**[24:39–24:51]**

NARRATOR:
> V4.1 Flash says no. A small, cheap scorer, called an indexer, quickly rates the past entries, and the model attends properly only to the top 512. [[V41-008]]

[PAUSE 0.4s]

VISUAL: A light indexer scan passes along the strip; 512 cells highlight; full attention lines only to those.


**[24:52–25:07]**

NARRATOR:
> Early layers also compress the past, merging neighbouring tokens into shared entries. [[V41-021]] And every layer keeps a short, precise window of the most recent 128 tokens, so nothing nearby gets lost. [[V41-006]]

[PAUSE 0.4s]

VISUAL: Pairs of cells merge into single cells (compression ratio 2); a bright window of recent tokens sits at the right end.


**[25:07–25:18]**

NARRATOR:
> Remember the grid of every token compared with every other? Double the text and that grid quadruples. Picking a fixed number of entries keeps each new token's work on a leash.

[PAUSE 0.8s]

VISUAL: The n×n attention grid from Act 4 reappears, then thins into sparse columns.


### s0903 · Layers that share a memory


**[25:20–25:28]**

NARRATOR:
> Now the layer dial. Traditionally, every layer keeps its own shelf of keys and values. Forty layers, forty shelves.

[PAUSE 0.4s]

VISUAL: A stack of 40 layers, each with its own cache shelf beside it.


**[25:28–25:36]**

NARRATOR:
> V4.1 Flash introduces what it calls Compressed Sparse Attention 2. Its layers come in three modes. [[V41-008]]

[PAUSE 0.3s]

VISUAL: Three mode badges: FULL, REINDEX, REUSE.


**[25:37–25:53]**

NARRATOR:
> A Full layer builds the shared memory and picks which entries matter. A Reindex layer borrows that memory, but re-scores it with its own question. And a Reuse layer borrows both, the memory and the selection. It keeps only its own query.

[PAUSE 0.4s]

VISUAL: FULL layer writes a shelf; REINDEX layer draws from that shelf with a new selection; REUSE layer draws both.


**[25:53–26:05]**

NARRATOR:
> In the encoder, layers come in groups of six. One Full, then five Reuse. In the decoder, groups of four. [[V41-022]] Most layers stop storing their own shelf entirely.

[PAUSE 0.4s]

VISUAL: Most of the 40 shelves collapse and vanish; only a few remain.


**[26:05–26:18]**

NARRATOR:
> The trade is the same one MLA made. A little more computation, and a lot less memory. And DeepSeek is upfront that it has a cost: the shared selection can occasionally pick the wrong entries. [[V41-015]]

[PAUSE 0.8s]

VISUAL: A small caution marker beside the REUSE badge: 'selection can err (§6)'.


### s0904 · Four bits


**[26:20–26:28]**

NARRATOR:
> Then the entry size dial again. This time not by storing fewer numbers, but by storing each number with fewer bits.

[PAUSE 0.4s]

VISUAL: An 8-bit cell box shrinks to 4 bits.


**[26:29–26:40]**

NARRATOR:
> Four bits give you only sixteen patterns. In the format DeepSeek uses, they stand for: zero, a half, one, one and a half, two, three, four, six, and their negatives. [[V41-009]] [[MATH]]

[PAUSE 0.4s]

VISUAL: A number line with the FP4 (E2M1) values marked as ticks: 0, 0.5, 1, 1.5, 2, 3, 4, 6 and mirror negatives.


**[26:40–26:51]**

NARRATOR:
> That's a very coarse ruler. The trick is to give every group of 16 numbers its own shared scale, so the ruler stretches to fit whatever range that group needs. [[V41-009]]

[PAUSE 0.4s]

VISUAL: A group of 16 real values; a scale factor stretches the tick ruler to cover them; each value snaps to the nearest tick.


**[26:52–27:04]**

NARRATOR:
> DeepSeek stores the main cache this way, and keeps the more sensitive local window in 8 bits. Compared with the 8 bit main cache of V4, that nearly halves its storage. [[V41-009]]

[PAUSE 0.8s]

VISUAL: Two cache shelves side by side: FP8 vs FP4, the FP4 one half the height.


### s0905 · Reading half as hard


**[27:06–27:16]**

NARRATOR:
> One more idea, aimed at the moment a long prompt first arrives. This is called prefill, reading the input, as opposed to decode, writing the output.

[PAUSE 0.4s]

VISUAL: Two phases labelled PREFILL (a huge block of input tokens) and DECODE (tokens emitted one by one).


**[27:16–27:32]**

NARRATOR:
> V4.1 Flash splits its 40 layers into a 20 layer encoder and a 20 layer decoder. [[V41-006]] The upper half doesn't compute its long-range memory from its own layers. It projects it directly from the encoder's final output. [[V41-010]]

[PAUSE 0.4s]

VISUAL: A 40-layer stack split at the middle; arrows from the layer-20 output fan up into each decoder layer's memory.


**[27:33–27:42]**

NARRATOR:
> So when a long prompt arrives, only the bottom half has to process all of it. The paper says this nearly halves prefill computation. [[V41-010]]

[PAUSE 0.4s]

VISUAL: Prompt block flows through the bottom 20 layers only; top half stays dim; label '≈ half the prefill compute'.


**[27:42–27:51]**

NARRATOR:
> Which is why the paper reports about 8 billion active parameters per token when reading, and about 16 billion when writing. [[V41-002]]

[PAUSE 0.8s]

VISUAL: Two meters: PREFILL 8B active, DECODE 16B active.


### s0906 · 890 bytes


**[27:53–28:03]**

NARRATOR:
> Now put the dials together. Here's a chart from DeepSeek's own paper. The global KV cache per token, across generations of their models. [[V41-004]]

[PAUSE 0.4s]

VISUAL: Recreated horizontal bar chart axes appear; attribution line 'Data: DeepSeek-AI, arXiv:2609.19969, Fig. 1(b)'.


**[28:03–28:10]**

NARRATOR:
> Their first model, in 2023: about 389 thousand bytes per token. [[V41-004]]

[PAUSE 0.3s]

VISUAL: Bar DeepSeek-V1 (2023.11): 389,120 B.


**[28:10–28:16]**

NARRATOR:
> V3.2, at the end of 2025: about 48 thousand. [[V41-004]]

[PAUSE 0.3s]

VISUAL: Bar V3.2 (2025.12): 48,068 B.


**[28:16–28:23]**

NARRATOR:
> V4 Flash, in April 2026: 3,514. [[V41-004]]

[PAUSE 0.3s]

VISUAL: Bar V4-Flash (2026.04): 3,514 B.


**[28:23–28:27]**

NARRATOR:
> And V4.1 Flash: 890 bytes. [[V41-003]]

[PAUSE 1.0s]

VISUAL: Bar V4.1-Flash (2026.09): 890 B — a sliver. The '890 bytes' teaser from Act 1 flies in and lands on it.


SFX: impact


**[28:28–28:41]**

NARRATOR:
> That's the number from the start. About 437 times smaller than their first model, and roughly a quarter of the model just before it. [[V41-004]] [[V41-003]] Less than a kilobyte, to remember each token.

[PAUSE 0.5s]

VISUAL: Annotations '≈ 437× smaller than V1' and '≈ 4× smaller than V4-Flash'.


**[28:41–28:54]**

NARRATOR:
> And one more result. Stretching the context 256 times, from 4 thousand tokens to a million, raises the compute for each new token by only about a quarter. [[V41-011]]

[PAUSE 0.4s]

VISUAL: Two markers on a context axis 4K → 1M; a cost line rising only +25%.


**[28:54–29:11]**

NARRATOR:
> The paper also reports that, despite this far smaller memory, V4.1 Flash performs substantially better than the model before it. [[V41-023]] That's DeepSeek's claim, on their own benchmarks. But it's the claim that matters. They didn't trade quality for memory.

[PAUSE 1.0s]

VISUAL: Small card: 'better overall performance than V4-Flash (reported)'.


LOOP CLOSED: L7 — How small can a memory of the past be?; L9 — What does '890 bytes' measure?


---

## ACT 10 — How a Model Learns   ·   MUSIC: minimal


### s1001 · Measuring wrongness

LOOP OPENED: L8 — Where do the weights come from? How was V3 trained?


**[29:14–29:22]**

NARRATOR:
> We've talked about running a model. But where do all those billions of weights come from in the first place? Nobody writes them by hand.

[PAUSE 0.4s]

VISUAL: The tower of layers, weights shown as a field of amber dots with random values.


**[29:22–29:30]**

NARRATOR:
> They start as random numbers. And a model with random weights, asked to continue the cat sat on the, will guess nonsense.

[PAUSE 0.4s]

VISUAL: Prompt 'the cat sat on the' → probability bars nearly flat; 'mat' has 2%.


**[29:30–29:42]**

NARRATOR:
> But we know the right answer. Mat. So we can measure how wrong the model was. The standard measure is the negative log of the probability it gave the right answer. It's called the loss. [[MATH]]

[PAUSE 0.4s]

VISUAL: Formula L = −log p(mat); with p = 0.02, L ≈ 3.9.


**[29:43–29:54]**

NARRATOR:
> Confident and right, the loss is near zero. Confident and wrong, it's huge. Now the entire goal of training fits in one sentence. Make that number smaller.

[PAUSE 0.8s]

VISUAL: Curve −log p over p from 0 to 1; a dot slides from left (high loss) to right (near zero).


### s1002 · Walking downhill


**[29:55–30:02]**

NARRATOR:
> Picture just one weight. Change it a little, and the loss goes up or down. Plot that, and you get a landscape. [[MATH]]

[PAUSE 0.4s]

VISUAL: A 1D loss curve over weight w with a ball on its slope.


**[30:03–30:09]**

NARRATOR:
> The slope at our current position tells us which way is downhill. That slope is called the gradient.

[PAUSE 0.4s]

VISUAL: Tangent line at the ball; an arrow along −gradient.


**[30:09–30:19]**

NARRATOR:
> So we take a small step downhill. New weight equals old weight, minus a small step size times the gradient. Then measure again. Step again.

[PAUSE 0.4s]

VISUAL: w ← w − η ∇L. The ball steps down the curve in several small hops, settling near the minimum.


**[30:20–30:36]**

NARRATOR:
> A real model does this for every one of its weights at once, in a landscape with billions of dimensions. The algorithm that finds all those slopes efficiently, by working backwards from the loss through every layer, is called backpropagation.

[PAUSE 0.4s]

VISUAL: The 1D curve morphs into a 3D-looking contour surface; gradient arrows ripple back down through the layer tower.


**[30:36–30:45]**

NARRATOR:
> And the backward pass costs roughly twice as much as the forward pass. So training costs about six operations per parameter, per token. [[GEN-004]]

[PAUSE 0.8s]

VISUAL: Forward arrow '2', backward arrow '4', total '≈ 6 FLOPs × active params × tokens'.


### s1003 · The loop


**[30:47–30:56]**

NARRATOR:
> So training is a loop. Take a batch of text. Run it forward. Measure the loss. Run backwards to get gradients. Nudge every weight. Repeat.

[PAUSE 0.4s]

VISUAL: Circular diagram: BATCH → FORWARD → LOSS → BACKWARD → UPDATE → (back to BATCH), spinning.


**[30:57–31:05]**

NARRATOR:
> How big a batch? For V4.1 Flash, the paper reports about a hundred million tokens in every single step. [[V41-012]]

[PAUSE 0.3s]

VISUAL: Batch card: 100.6M tokens per step.


**[31:05–31:15]**

NARRATOR:
> And it trained on 45 trillion tokens in total. [[V41-012]] Divide one by the other, and that's roughly 450 thousand turns of this loop. [[DER-003]]

[PAUSE 0.4s]

VISUAL: 45T ÷ 100.6M ≈ 447K steps; the loop counter spins up.


**[31:15–31:30]**

NARRATOR:
> Every turn involving all the walls at once. Compute for the forward and backward passes. Memory for the weights and the optimizer. And communication, because thousands of GPUs have to agree on the update.

[PAUSE 0.8s]

VISUAL: The three pillars light in sequence around the loop.


### s1004 · What V3's training took


**[31:32–31:38]**

NARRATOR:
> Now we can read DeepSeek V3's training numbers with understanding, instead of awe.

[PAUSE 0.4s]

VISUAL: A clean ledger panel titled 'DeepSeek-V3 training (reported)'.


**[31:38–31:56]**

NARRATOR:
> 37 billion active parameters. 14.8 trillion tokens. [[V3-001]] [[V3-002]] Plug them into the rule of thumb, six times parameters times tokens, and you get roughly three times ten to the twenty-four operations. That's our estimate, not a figure from DeepSeek. [[DER-001]]

[PAUSE 0.4s]

VISUAL: 6 × 37×10⁹ × 14.8×10¹² ≈ 3.3×10²⁴; tag 'our estimate'.


**[31:57–32:11]**

NARRATOR:
> DeepSeek reports that each trillion tokens took 180 thousand H800 GPU hours. About three point seven days, on their cluster of 2,048 GPUs. [[V3-004]]

[PAUSE 0.4s]

VISUAL: Row: '180K GPU-hours per trillion tokens ≈ 3.7 days on 2,048 H800s'.


**[32:11–32:21]**

NARRATOR:
> And the whole run, pre-training, context extension and post-training, added up to 2.788 million GPU hours. [[V3-003]]

[PAUSE 0.8s]

VISUAL: Stacked bar: pre-training 2.664M + extension + post-training = 2.788M GPU-hours.


LOOP CLOSED: L8 — Where do the weights come from? How was V3 trained?


---

## ACT 11 — The Numbers, Honestly   ·   MUSIC: minimal


### s1101 · What the famous number means


**[32:23–32:29]**

NARRATOR:
> Which brings us to the most quoted number in this whole story. About 5.6 million dollars. [[V3-005]]

[PAUSE 0.4s]

VISUAL: '$5.576M' large in the centre.


**[32:30–32:43]**

NARRATOR:
> Here's where it comes from. DeepSeek took those 2.788 million GPU hours and assumed a rental price of two dollars per GPU hour. [[V3-005]] [[V3-003]] That's it. Hours times a price.

[PAUSE 0.4s]

VISUAL: 2.788M × $2 = $5.576M written out.


**[32:44–33:02]**

NARRATOR:
> And in the same report, they say plainly what it excludes. The costs of prior research and ablation experiments on architectures, algorithms and data. [[V3-005]] It also doesn't include buying the GPUs, the people, or the failed attempts that taught them what to build.

[PAUSE 0.4s]

VISUAL: Two columns: INCLUDED (final training run GPU time) vs NOT INCLUDED (research, experiments, hardware purchase, staff).


**[33:02–33:14]**

NARRATOR:
> So the honest headline was never that DeepSeek built a frontier model for 5.6 million dollars. [[V3-005]] It's that the final training run, by their accounting, was remarkably efficient.

[PAUSE 0.5s]

VISUAL: Crossed-out headline 'Built for $5.6M' → corrected 'final run ≈ $5.6M of GPU time (reported)'.


**[33:15–33:26]**

NARRATOR:
> And some things are simply not public. The V4.1 Flash paper, for instance, doesn't say what hardware it was trained on, or what it cost. [[V41-014]] So we won't guess.

[PAUSE 0.8s]

VISUAL: Ledger row: V4.1-Flash — hardware: not reported; cost: not reported.


### s1102 · So what was surprising?


**[33:28–33:40]**

NARRATOR:
> So what actually was surprising? Not a secret invention. Mixture of experts, attention, low precision numbers. Those ideas existed before DeepSeek. [[GEN-007]]

[PAUSE 0.4s]

VISUAL: Three idea cards (MoE, attention, low precision) each tagged 'prior art'.


**[33:40–33:47]**

NARRATOR:
> What was surprising was how far they were pushed, and how deliberately each one was aimed at a specific wall.

[PAUSE 0.4s]

VISUAL: A table forms: WALL → IDEA.


**[33:47–33:59]**

NARRATOR:
> Compute: activate only the experts you need. Communication: overlap the waiting and shrink the numbers. Memory: compress the cache, share it across layers, store it in four bits.

[PAUSE 0.4s]

VISUAL: Rows fill: COMPUTE → MoE (37B of 671B); COMMUNICATION → DualPipe + FP8; MEMORY → MLA → CSA2 + FP4 (890 B/token).


**[33:59–34:09]**

NARRATOR:
> Each one, on its own, is a sensible engineering choice. Together, they add up to a system shaped around its bottlenecks. Not around its budget.

[PAUSE 1.0s]

VISUAL: The table glows; a caption 'shaped around the bottlenecks'.


---

## ACT 12 — The Whole Machine   ·   MUSIC: resolution


### s1201 · See it all at once


**[34:11–34:15]**

NARRATOR:
> Let's zoom out and look at the whole machine, one last time.

[PAUSE 0.4s]

VISUAL: Camera pulls back to an empty dark stage.


**[34:15–34:29]**

NARRATOR:
> Text becomes tokens. Tokens become vectors. Attention lets them borrow meaning from each other. A router sends each one to a handful of experts. The output becomes a guess about the next token.

[PAUSE 0.4s]

VISUAL: Pipeline builds left to right: DATA → TOKENS → EMBEDDINGS → ATTENTION → ROUTER → EXPERTS → OUTPUT, reusing each icon from earlier acts.


**[34:29–34:39]**

NARRATOR:
> The guess is scored. The loss flows backwards. Every weight moves a tiny step. And the loop begins again. Hundreds of thousands of times. [[DER-003]]

[PAUSE 0.4s]

VISUAL: A return path: OUTPUT → LOSS → GRADIENTS → UPDATE loops back to the start.


**[34:39–34:49]**

NARRATOR:
> And over all of it, the three walls. Compute, wherever numbers multiply. Memory, wherever numbers wait. Communication, wherever numbers travel.

[PAUSE 0.8s]

VISUAL: Coloured overlays: COMPUTE glows on attention/experts, MEMORY on the KV cache and weights, COMMUNICATION on the router→experts links.


### s1202 · What you do when you can't buy your way out


**[34:51–34:57]**

NARRATOR:
> So, back to the question we started with. What do you do when you can't simply buy your way out?

[PAUSE 0.6s]

VISUAL: The central question from Act 1 returns to centre.


**[34:57–35:10]**

NARRATOR:
> You stop treating intelligence as a shopping problem, and start treating it as a physics problem. Where do the numbers go? How long do they wait? How far do they travel? How many bits do they really need?

[PAUSE 0.5s]

VISUAL: The four questions appear one by one under the pillars.


**[35:10–35:19]**

NARRATOR:
> The constraint didn't make the problem easier. But it may have made understanding it more valuable. When you can't add more, you have to waste less.

[PAUSE 0.8s]

VISUAL: The GPU wall from the opening returns — thinner, but every block lit and busy.


**[35:20–35:34]**

NARRATOR:
> And that leaves one question open. Everything in this story was about fitting the mathematics to hardware that already existed. DeepSeek even chose its four-bit format so it would work across many kinds of chips. [[V41-016]]

[PAUSE 0.5s]

VISUAL: A chip outline and an equation outline sit side by side, separate.


**[35:35–35:42]**

NARRATOR:
> So what happens when the algorithms and the hardware start being designed together, each one shaped around the other?

[PAUSE 1.0s]

VISUAL: The chip and the equation slide together and interlock.


**[35:43–35:45]**

NARRATOR:
> That's a story for another time.

[PAUSE 2.5s]

VISUAL: Fade to title card: 'DeepSeek Did the Impossible — The First-Principles Story of How'. Sources note.


LOOP CLOSED: L1 — How do you compete when you can't simply buy more compute?
