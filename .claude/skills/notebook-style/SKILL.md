---
name: notebook-style
description: 'Structures Jupyter notebooks using a pedagogical workflow: short intro → imports → progressive concept-building cells → visualizations → define functions as soon as a concept is explained → reuse downstream. Enforces one idea per cell and narrative markdown between code. Use when user mentions jupyter, notebook, .ipynb, "clean up my notebook", "structure this notebook", or asks to write a notebook on any concept/dataset.'
---

# Notebook Style

## Core Philosophy

Notebooks are **workflows, not scripts.** Each cell is a paragraph in a story.  
Build raw → visualize → refine → functionize → apply.

---

## Cell Sequence Pattern

```
[1] Markdown: Concept intro (3–5 sentences max)
[2] Code: Imports only — no logic
[3] Code: Simplest possible example of the concept
[4] Markdown: Why does this matter? What are we about to explore?
[5] Code: First concrete step (single operation)
[6] Code: Visualize it
[7] Markdown: What did we just see? Explain the result
[8] Code: Next step — build on [5]
... repeat 5-8 for each sub-concept ...
[N-2] Code: Consolidate raw cells into clean functions
[N-1] Code: Demo functions on a harder/combined example
[N]   Markdown: Where is this used in the real world?
```

---

## Rules

**One cell, one idea.**  
If a cell does two things, split it.  
If it exceeds ~20 lines, it belongs in a function or a split cell.

**Markdown drives the narrative.**  
Every major transition (new sub-concept, new phase) needs a markdown cell.  
Don't let two conceptually distinct code cells be adjacent without explanation.

**Visualize before explaining.**  
Plot first, interpret in the next markdown cell. Let the reader see it first.  
For every visualization cell, follow [MATPLOTLIB.md](MATPLOTLIB.md).

**Raw before clean, per concept.**  
For each concept: write the logic inline first, verify it works, then wrap it into a function. Once defined, call that function in all downstream cells — don't re-implement it.

**Imports are isolated.**  
One cell, all imports. Nothing else in it.

---

## Notebook Phases

### Phase 1 — Setup (2 cells)
- Markdown: concept intro, what we're building, dataset context
- Code: all imports

### Phase 2 — Concept Building (4–10 cells per sub-concept)
For each sub-concept:
1. Markdown: what this sub-concept is, one-liner
2. Code: minimal working example (raw inline logic)
3. Code: visualize
4. Markdown: what does the output tell us?
5. Code: `def concept_fn(...)` — wrap the now-understood logic into a function
   (skip if trivial or not reused downstream)

Downstream sub-concepts call earlier functions rather than re-implementing.

### Phase 3 — Composition (2–3 cells)
- Code: compose the sub-concept functions into a complex end-to-end demo
- Markdown: what does the combined result show?

### Phase 4 — Applications (1–2 cells)
- Markdown: real-world use cases, pointers to what comes next

---

## Anti-Patterns to Avoid

| Anti-pattern | Fix |
|---|---|
| 100-line cell | Split by operation; move helpers to functions |
| `import` buried mid-notebook | Hoist all imports to cell 2 |
| No markdown between concept shifts | Add transition markdown cells |
| Function defined before its concept is shown | Show raw inline first, then wrap into a function |
| Re-implementing logic that was already functionized | Call the existing function; don't duplicate |
| All functions deferred to end of notebook | Functionize each concept right after it's explained |
| Visualization without interpretation | Follow every plot with a markdown explanation |
| Intro cell that is a wall of text | Max 5 sentences; move detail into later cells |

---

## Example: Fourier Transform Notebook Outline

```
[1]  md  : What is the Fourier Transform? (5 lines)
[2]  code: import numpy, matplotlib, scipy
[3]  code: plot a single sin wave (raw inline)
[4]  code: def make_signal(freq, duration, fs) — wrap signal generation
[5]  md  : Why move to frequency domain?
[6]  code: show Euler's formula e^(iθ) = cos+isin (raw inline)
[7]  md  : What is the winding number / frequency?
[8]  code: compute amplitude and phase for one freq (raw inline)
[9]  code: plot amplitude spectrum using make_signal()
[10] code: def compute_spectrum(signal, fs) — wrap amplitude/phase logic
[11] md  : What do amplitude and phase tell us?
[12] code: → composition: generate composite sin, call make_signal() + compute_spectrum(), plot
[13] md  : Where is FFT used? (audio, images, signal processing)
[14] code: load 4×4 image, call compute_spectrum() on rows, show magnitude
[15] md  : What comes next — convolution, filters, spectrogram
```

See [EXAMPLES.md](EXAMPLES.md) for annotated cell-level code.  
See [MATPLOTLIB.md](MATPLOTLIB.md) for visualization rules (bmh style, figure sizing, subplot templates).
