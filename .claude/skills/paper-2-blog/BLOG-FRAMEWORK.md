# Blog Writing Framework — ELI5 from First Principles

The goal: a curious 12-year-old (not literally 5) with no domain knowledge should finish the post understanding *why* this paper matters and *roughly how* it works — without feeling talked down to.

---

## Blog structure

```
1. Title
2. One-line hook
3. The Problem (plain English)
4. Why It's Hard (what people tried before)
5. The Big Idea (the paper's core insight)
6. Math Primer (only if the paper uses math — first-principles explanations)
7. How It Works (step-by-step, with analogies and diagrams)
8. The Results (numbers with context)
9. Why It Matters (real-world so-what)
10. One-sentence TL;DR
```

---

## Section-by-section instructions

### 1. Title
- Short, curiosity-driven, no jargon.
- Bad: *"Attention Is All You Need"*
- Good: *"How a Simple 'Paying Attention' Trick Rewrote the Rules of AI Language"*

### 2. One-line hook
One sentence that makes a non-expert think "wait, tell me more." Lead with impact or surprise, not methodology.

> "What if the secret to making AI understand language wasn't to read sentences word by word — but to look at every word at once, like scanning a whole page?"

### 3. The Problem
- State the problem in terms of real-world consequences, not technical metrics.
- Use a concrete scenario: *"Imagine you're trying to translate a book from French to English one word at a time, never allowed to look back…"*
- End this section with: *"So the question was: can we do better?"*

### 4. Why It's Hard
- Explain 1–2 previous approaches in one paragraph each.
- For each: what did it try, why did it make sense, what was its fatal flaw?
- Use the pattern: *"People tried X. That worked for Y, but broke down when Z."*
- Never go deeper than one level of technical detail here.

### 5. The Big Idea
- This is the heart of the post. Take as much space as needed.
- Lead with the insight in one bold sentence, then explain it.
- Use the **"explain like a magic trick"** structure:
  1. Show the result first ("here's what it can do that nothing else could")
  2. Reveal the mechanism ("the trick is…")
  3. Show why the mechanism works ("it works because…")
- Every new term: define it immediately in parentheses using plain language.
  - Bad: *"The model uses multi-head self-attention."*
  - Good: *"The model uses something called 'attention' — think of it as the model deciding which words in a sentence are most relevant to understanding each other word."*

### 6. Math Primer *(include only if the paper uses non-trivial math)*

Introduce every mathematical concept the reader will encounter — before they encounter it in the mechanism. Each concept gets its own mini-section:

**Structure for each concept:**
1. **Name it plainly** — one sentence saying what this thing is in human terms.
2. **Ground it with a concrete example** — use small numbers and a real-world scenario (not x and y).
3. **Show the intuition** — why does the math behave the way it does? What is it *measuring* or *doing*?
4. **Connect it to the paper** — one sentence saying exactly where/how this paper uses it.

**Example (softmax):**
> Softmax is a function that turns a list of raw scores into probabilities that add up to 1.
>
> Say a model thinks word A scores 3, word B scores 1, word C scores 0. Raw scores don't tell you "how much more likely is A than C?" Softmax converts those scores to probabilities — roughly 88%, 11%, 1% — so you can compare and sample from them meaningfully.
>
> The trick is exponentiation: it amplifies differences between scores, making the winner win *harder*. That's useful when you want the model to be decisive, not wishy-washy.
>
> In this paper, softmax appears in the attention formula to turn compatibility scores between words into a probability distribution over which words to attend to.

**Rules:**
- Cover every equation the paper uses in the "How It Works" section — no orphan math.
- Never use the word "trivial" or assume prior calculus knowledge.
- If two concepts build on each other, introduce them in dependency order.
- Keep each concept to one short paragraph + one example. Do not go deeper than needed.

### 7. How It Works
- Walk through the mechanism step by step. Use numbered steps.
- For each step, pair the technical action with a physical analogy.
- Analogy sources that work well: cooking, LEGO, post-it notes, libraries, classrooms, sports teams, maps.
- Keep each step to 2–3 sentences max.
- Reference Math Primer concepts by name when they appear ("this is where softmax comes in").
- **Embed diagrams** for any step where a visual would replace a paragraph of description. Draw them as ASCII/Unicode art in a fenced code block, placed immediately after the step they illustrate:
  ````markdown
  ```
    Input ──→ [Encoder] ──→ z ──→ [Decoder] ──→ Output
  ```
  ````
  Follow the diagram with a one-sentence caption in italics explaining what it shows.

**Analogy quality test:** Could a 12-year-old picture it? If not, find a simpler one.

### 8. The Results
- Never quote a raw metric without context.
  - Bad: *"Achieved 92.4% on BLEU score."*
  - Good: *"On the standard translation benchmark, this method made 92 correct calls per 100 — the previous best was 85. That gap is enormous in practice: it's the difference between 'mostly readable' and 'actually useful.'"*
- Include: what benchmark, what the number means in human terms, how big the improvement is relative to what came before.
- If the paper beats a baseline: say by how much AND what that feels like ("twice as fast", "half as many errors").

### 9. Why It Matters
- Answer: *"If this works, what changes in the world?"*
- Think 3 levels out:
  1. Direct use (what researchers/engineers can now build)
  2. Downstream use (what products or services this enables)
  3. Societal implication (who benefits, any risks?)
- Keep it grounded. Don't oversell, don't undersell.

### 10. TL;DR
One sentence. Subject + verb + object + why it matters.
> *"This paper replaced slow sequential AI with a 'look-at-everything-at-once' approach, making language models faster and smarter — and basically started the modern era of AI."*

---

## Terminology Warnings

When a paper uses a term in a way that diverges from its standard meaning in the broader community, insert an inline blockquote warning at the exact point where the term first appears in the blog.

### Format

```markdown
> **⚠️ Terminology warning:** The paper uses **[term]** to mean [what the paper means].
> In most [ML / statistics / CS] literature, **[term]** means [standard definition] — [brief example that makes the distinction concrete].
> The paper's usage is common in [specific subfield or community] but will mislead readers coming from [other context].
```

### Rules

- Place the warning *immediately after* the sentence that introduces the term — not in a footnote, not at the end of the section.
- Keep it to 2–3 sentences. The goal is to inoculate the reader, not to write a survey of the literature.
- Always name the community where the standard definition lives (e.g. "supervised learning", "classical statistics", "information theory") so the reader knows which frame of reference you're anchoring to.
- If the paper's usage is arguably acceptable but risky, say so: *"This usage is defensible but uncommon outside [subfield]."*
- If a term is used loosely throughout the whole paper (not just once), add the warning at first use and note *"the paper uses this term throughout in the same loose sense."*
- Do not warn about terms the paper explicitly defines itself and uses consistently with its own definition — only warn when the paper's usage silently conflicts with a common external definition.

### Examples of mismatches worth flagging

| Term as used in paper | Standard meaning | Paper's meaning | Worth warning? |
|---|---|---|---|
| "concept drift" | P(Y\|X) changes | P(X) changes | Yes |
| "inference" (deep learning) | running a trained model forward | probabilistic inference (computing posteriors) | Yes, if context is ambiguous |
| "energy" (energy-based models) | scalar score function | physical energy | Yes |
| "regularization" | penalty on model complexity | any form of constraint | Only if the paper uses it unusually |
| "attention" | learned weighted average | general notion of focus | Only if conflated with human attention |

---

## Writing rules

| Rule | Why |
|---|---|
| No paragraph longer than 4 sentences | Forces clarity |
| Define every acronym on first use | Reader never gets lost |
| At least one analogy per technical concept | Builds mental model |
| "So what?" after every result | Keeps reader engaged |
| Active voice only | More readable |
| No "groundbreaking", "revolutionary", "state-of-the-art" | Clichés that say nothing |
| Short sentences when explaining mechanisms | Reduces cognitive load |
| Math Primer before every equation that appears in How It Works | Reader never hits unexplained symbols |
| Every diagram has a one-sentence italic caption below it | Context without alt text |
| Diagrams are ASCII/Unicode art in fenced code blocks — no image files | Self-contained markdown, no external dependencies |
| Terminology warning blockquote at first use of any term the paper uses non-standardly | Prevents reader confusion before it happens |

## Tone
Warm, curious, enthusiastic — like a smart friend who just read the paper and can't wait to tell you about it. Not academic. Not dumbed-down. Respectful of the reader's intelligence but not their domain knowledge.

## Length
- Target: 800–1200 words
- Never pad. If you've explained something clearly in 600 words, stop at 600.
- The "How It Works" section earns the most space — that's the payoff.

## What to skip
- Related work beyond what's needed to explain "why it's hard"
- Implementation details (batch size, learning rate, hardware)
- Limitations section (unless it dramatically changes the "why it matters" story)
- Acknowledgements, funding, author affiliations
