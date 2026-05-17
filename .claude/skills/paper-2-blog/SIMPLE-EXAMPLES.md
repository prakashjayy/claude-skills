# Simple Examples Subskill

Activated by `--use-simple-examples`. Augments every technical concept in the blog with a concrete worked example that uses real numbers, a mini step-by-step workflow, or a simple calculation — before the analogy, not instead of it.

---

## Core rule

Every technical concept must be grounded in **one worked example** that follows this pattern:

```
Concept name (plain English definition)
→ Concrete setup with real numbers
→ Step-by-step walkthrough
→ Result stated plainly
→ [Optional] Trivia: surprising implication of the math
```

Never use abstract placeholders (x, y, n) in the example. Use specific values that fit in one sentence each step.

---

## Worked example template

**Topic:** Vector Quantization in VQ-VAE

**Concept:** Mapping continuous feature vectors to the nearest entry in a learned lookup table (codebook).

**Concrete setup:**
> Say our encoder produces a feature map of shape `16 × 512 × 8 × 8` (batch of 16 images, 512 channels, 8×8 spatial grid). Flatten each image's spatial grid: `512 × 64` — so one image gives us **64 feature vectors**, each 512-dimensional.

**Step-by-step walkthrough:**
> 1. Our codebook has **1,024 entries**, each also 512-dimensional.
> 2. For each of the 64 vectors, compute L2 distance to all 1,024 codebook entries.
> 3. Replace each vector with the index of its nearest codebook entry.
> 4. One image becomes a sequence of 64 integers: `[120, 456, 1023, 0, 77, ...]`

**Result stated plainly:**
> The continuous feature map is now a compact integer sequence. The decoder learns to reconstruct the image from these integers alone.

**Trivia (surprising implication):**
> Each of the 64 positions can independently pick from 1,024 choices → 1,024⁶⁴ possible image codes. That's more combinations than atoms in the observable universe. This is why VQ-VAE needs enormous datasets: the codebook must learn to cover a useful slice of that astronomical space.

---

## How to apply this to each blog section

### The Problem
Add a concrete failure case with numbers.
> *"A naive model trained on 10,000 images tries to generate a face. The pixel space has 256³ˣ⁵¹²ˣ⁵¹² ≈ 10^¹·⁸ᴹ possible images. Sampling randomly would never land on anything face-shaped."*

### Why It's Hard
For each prior approach, show where the numbers break down.
> *"RNNs process sequences step-by-step. A 512-token sentence requires 512 sequential operations — nothing runs in parallel. On a modern GPU that's 40ms per sentence. The Transformer does the same in 2ms by processing all 512 tokens simultaneously."*

### The Big Idea
Lead with the reveal, then show it with numbers.
> *"Instead of one big probability over all 50,000 vocabulary words at once, the model makes 16 independent smaller decisions. Each head attends to 32 dimensions of a 512-dimensional embedding. 16 × 32 = 512 — same total, but 16 parallel views of the data."*

### Math Primer
Every equation gets a numerical walkthrough before the formula appears.

**Format:**
1. Name the operation in plain English.
2. Run it on 3–5 concrete numbers.
3. State what the output means.
4. Then show the formula (or skip it if the intuition is enough).

> **Softmax example:**
> Scores: `[3.0, 1.0, 0.0]`
> Exponentiate: `[e³, e¹, e⁰] = [20.1, 2.7, 1.0]`
> Sum: `23.8`
> Probabilities: `[20.1/23.8, 2.7/23.8, 1.0/23.8] = [0.84, 0.11, 0.04]`
> The winner (score 3.0) gets 84% of the probability mass. That's decisiveness through exponentiation.

### How It Works
Each numbered step gets a mini-calculation or data-shape annotation.

> **Step 3 — Compute attention scores**
> Query matrix Q: shape `[64, 64]` (64 tokens, 64-dim keys)
> Key matrix K: shape `[64, 64]`
> Raw scores: Q × Kᵀ → shape `[64, 64]` — one score per token pair.
> Divide by √64 = 8 to prevent vanishing gradients. Apply softmax row-wise.
> Each row is now a probability distribution: "how much should token i attend to token j?"

### The Results
Always convert the metric into a human-scale quantity.
> *"BLEU improved from 41.0 to 41.8 on EN→DE translation. That 0.8 gap means roughly 1 in 100 phrases that used to be wrong is now correct. Across a 500-page document, that's ~5 pages of improved accuracy."*

---

## Quality checks for simple examples

| Check | Pass condition |
|---|---|
| Uses real numbers | No x, y, n — actual integers or floats |
| One image fits one tweet | Setup < 280 chars |
| Walkthrough is sequential | Each step builds on the previous |
| Result is stated in the same units as the setup | No unit switches |
| Trivia (if present) is surprising | Reader thinks "wait, really?" |

---

## What to skip

- Do not add examples for concepts already explained by analogy alone (if the analogy is genuinely sufficient).
- Do not force numbers onto qualitative concepts (e.g. "the model learns to be polite" doesn't need a number).
- One example per concept — do not stack multiple worked examples for the same idea.
