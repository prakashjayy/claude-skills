---
name: notebook-style
description: Structures Jupyter notebooks using a pedagogical workflow: short intro → imports → progressive concept-building cells → visualizations → consolidate into functions → complex demos → applications. Enforces one idea per cell, narrative markdown between code, and the pattern of raw exploration first then function consolidation. Use when user mentions jupyter, notebook, .ipynb, "clean up my notebook", "structure this notebook", or asks to write a notebook on any concept/dataset.
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

**Raw before clean.**  
Write the math/logic inline in cells first. Only after it works, refactor into functions.  
Functions appear in the second half of the notebook.

**Imports are isolated.**  
One cell, all imports. Nothing else in it.

---

## Notebook Phases

### Phase 1 — Setup (2 cells)
- Markdown: concept intro, what we're building, dataset context
- Code: all imports

### Phase 2 — Concept Building (3–10 cells per sub-concept)
For each sub-concept:
1. Markdown: what this sub-concept is, one-liner
2. Code: minimal working example (raw, no functions yet)
3. Code: visualize
4. Markdown: what does the output tell us?

### Phase 3 — Consolidation (2–4 cells)
- Code: collect the raw logic into well-named functions
- Code: demo those functions on a richer/combined example
- Markdown: what changed? why are functions better here?

### Phase 4 — Applications (1–2 cells)
- Markdown: real-world use cases, pointers to what comes next

---

## Anti-Patterns to Avoid

| Anti-pattern | Fix |
|---|---|
| 100-line cell | Split by operation; move helpers to functions |
| `import` buried mid-notebook | Hoist all imports to cell 2 |
| No markdown between concept shifts | Add transition markdown cells |
| Functions appear before raw demo | Raw exploration first, functions second |
| Visualization without interpretation | Follow every plot with a markdown explanation |
| Intro cell that is a wall of text | Max 5 sentences; move detail into later cells |

---

## Example: Fourier Transform Notebook Outline

```
[1] md  : What is the Fourier Transform? (5 lines)
[2] code: import numpy, matplotlib, scipy
[3] code: plot a single sin wave
[4] md  : Why move to frequency domain?
[5] code: show Euler's formula e^(iθ) = cos+isin
[6] code: animate winding frequency concept
[7] md  : What is the winding number / frequency?
[8] code: compute amplitude and phase for one freq
[9] code: plot amplitude spectrum
[10] md : What do amplitude and phase tell us?
[11] code: → consolidate: def fourier_decompose(signal, fs)
[12] code: generate composite sin (3 frequencies), run function, plot
[13] md : Where is FFT used? (audio, images, signal processing)
[14] code: load 4×4 image, compute 2D DFT manually, show magnitude
[15] md : What comes next — convolution, filters, spectrogram
```

See [EXAMPLES.md](EXAMPLES.md) for annotated cell-level code.  
See [MATPLOTLIB.md](MATPLOTLIB.md) for visualization rules (bmh style, figure sizing, subplot templates).
