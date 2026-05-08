---
name: notebook-style
description: 'Structures Jupyter notebooks using a pedagogical workflow: short intro → imports → progressive concept-building cells → visualizations → define functions as soon as a concept is explained → reuse downstream. Enforces one idea per cell and narrative markdown between code. Use when user mentions jupyter, notebook, .ipynb, "clean up my notebook", "structure this notebook", or asks to write a notebook on any concept/dataset.'
---

# Notebook Style

Notebooks are **workflows, not scripts.** Each cell is a paragraph in a story.  
Build raw → visualize → refine → functionize → apply — **per concept, not once at the end.**

---

## Cell Pattern

```
[1] md  : Concept intro (3–5 sentences, no equations yet)
[2] code: All imports — nothing else

↓ repeat for each sub-concept ↓

  md  : What is this sub-concept? (one-liner)
  code: Minimal raw inline example
  code: Visualize it
  md  : What does the output tell us?
  code: def concept_fn(...) — wrap the proven logic
        skip only if trivial and never reused downstream

↑ downstream cells call earlier functions, never re-implement ↑

[N-1] code: Compose sub-concept functions into a richer end-to-end demo
[N]   md  : Where is this used in the real world?
```

---

## Rules

**One cell, one idea.** >20 lines → split or move to a function.

**Markdown between every concept shift.** No two conceptually distinct code cells adjacent.

**Visualize before explaining.** Plot first, interpret in the next markdown cell. Follow [MATPLOTLIB.md](MATPLOTLIB.md).

**Raw before clean, per concept.** Write inline first, verify it works, then wrap into a function. Downstream cells call that function — never re-implement.

**Imports are isolated.** One cell, all imports, nothing else.

---

## Anti-Patterns

| Anti-pattern | Fix |
|---|---|
| 100-line cell | Split by operation; move helpers to a function |
| `import` buried mid-notebook | Hoist all imports to cell 2 |
| No markdown between concept shifts | Add a transition markdown cell |
| Function defined before its concept is shown | Show raw inline first, then wrap |
| Re-implementing logic already functionized | Call the existing function |
| All functions deferred to end of notebook | Functionize each concept right after it's explained |
| Visualization without interpretation | Follow every plot with a markdown cell |
| Intro cell wall of text | Max 5 sentences; move detail to later cells |

---

## Example: Fourier Transform Outline

```
[1]  md  : What is the Fourier Transform? (5 lines)
[2]  code: import numpy, matplotlib, scipy
[3]  code: plot a single sin wave (raw inline)
[4]  code: def make_signal(freq, duration, fs)
[5]  md  : Why move to frequency domain?
[6]  code: compute amplitude and phase for one freq (raw inline)
[7]  code: plot amplitude spectrum — calls make_signal()
[8]  code: def compute_spectrum(signal, fs)
[9]  md  : What do amplitude and phase tell us?
[10] code: composite signal → make_signal() + compute_spectrum() → plot
[11] md  : Where is FFT used? (audio, images, signal processing)
[12] code: load image, call compute_spectrum() on rows, show magnitude
[13] md  : What comes next — convolution, filters, spectrogram
```

See [MATPLOTLIB.md](MATPLOTLIB.md) for visualization rules.
