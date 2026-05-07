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
6. How It Works (step-by-step, with analogies)
7. The Results (numbers with context)
8. Why It Matters (real-world so-what)
9. One-sentence TL;DR
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

### 6. How It Works
- Walk through the mechanism step by step. Use numbered steps.
- For each step, pair the technical action with a physical analogy.
- Analogy sources that work well: cooking, LEGO, post-it notes, libraries, classrooms, sports teams, maps.
- Keep each step to 2–3 sentences max.
- If there's a diagram or equation in the paper, describe what it's *doing* in plain language — never reproduce it as-is.

**Analogy quality test:** Could a 12-year-old picture it? If not, find a simpler one.

### 7. The Results
- Never quote a raw metric without context.
  - Bad: *"Achieved 92.4% on BLEU score."*
  - Good: *"On the standard translation benchmark, this method made 92 correct calls per 100 — the previous best was 85. That gap is enormous in practice: it's the difference between 'mostly readable' and 'actually useful.'"*
- Include: what benchmark, what the number means in human terms, how big the improvement is relative to what came before.
- If the paper beats a baseline: say by how much AND what that feels like ("twice as fast", "half as many errors").

### 8. Why It Matters
- Answer: *"If this works, what changes in the world?"*
- Think 3 levels out:
  1. Direct use (what researchers/engineers can now build)
  2. Downstream use (what products or services this enables)
  3. Societal implication (who benefits, any risks?)
- Keep it grounded. Don't oversell, don't undersell.

### 9. TL;DR
One sentence. Subject + verb + object + why it matters.
> *"This paper replaced slow sequential AI with a 'look-at-everything-at-once' approach, making language models faster and smarter — and basically started the modern era of AI."*

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
