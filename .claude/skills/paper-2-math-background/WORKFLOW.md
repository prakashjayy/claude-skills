# Detailed Workflow

## Step 1 — Ingest the paper

Accept any of:
- Bare arxiv ID: `2301.07041` → fetch `https://arxiv.org/abs/2301.07041` then `https://arxiv.org/pdf/2301.07041`
- arxiv URL (any format): extract ID first, then follow same path
- Direct PDF URL: fetch directly
- Pasted abstract or text: use as-is

**Fetch strategy:**
1. WebFetch the abstract page to get title, authors, abstract
2. If `paper-2-blog`'s `scripts/extract_pages.py` is available, run it on the downloaded PDF to get key pages
3. Otherwise: WebFetch the HTML version (`https://ar5iv.org/abs/<id>`) as a fallback — it renders LaTeX

Minimum needed: title, abstract, introduction, and the methods/theory section where math appears.

---

## Step 2 — Build the mathematical inventory

Read the extracted text and list **every distinct mathematical object** used:

| Category | Examples to look for |
|---|---|
| Probability & measure | distributions, densities, expectations, KL divergence, entropy |
| Linear algebra | matrix factorizations (SVD, eigen), norms, inner products, projections |
| Calculus & analysis | gradients, Jacobians, Hessians, integrals, Taylor expansions, functionals |
| Optimization | loss functions, Lagrangians, KKT conditions, convergence rates |
| Information theory | mutual information, entropy, coding bounds |
| Geometry & topology | manifolds, geodesics, Riemannian metrics |
| Graph theory | adjacency matrices, Laplacians, spectral properties |
| Named theorems | Bayes' theorem, Jensen's inequality, Rademacher complexity, PAC bounds |
| Algorithms | EM algorithm, MCMC, attention mechanism, diffusion process |

For each item record: **name**, **notation used in paper**, **section/equation number**.

---

## Step 3 — Build the prerequisite tree

For each concept, ask: *"What simpler concept must a reader know first?"*

Trace until you reach something a student with calculus + linear algebra would know. Example:

```
Variational Inference
└── KL Divergence
    └── Entropy
        └── Probability distributions
            └── Random variables          ← stop here (foundational)
```

Produce a full ASCII tree covering all concepts. This becomes the **Prerequisites map** section.

Order the primer sections: topological sort of the tree (foundational concepts first).

---

## Step 4 — Write the primer

One `##` section per concept, in prerequisite order (foundational → paper-specific).

### Per-concept template

```markdown
## [Concept Name]

**Intuition** — One paragraph, zero math. Use a physical or everyday analogy.
Explain what this concept *does*, not what it *is*.

**Formal definition**

> **Definition.** [Name] is defined as...
>
> $$ [equation using notation from NOTATION.md] $$

**Diagram**

[ASCII/Unicode visual — see DIAGRAMS.md for templates. Every concept needs one.]

**Key properties**

- Property 1 (with brief justification)
- Property 2
- ...

**Connection to paper**

One sentence: how and where this concept appears in the paper being studied.
```

**Writing rules:**
- Intuition section: no equations, no jargon, no "simply" or "just"
- Formal definition: use [NOTATION.md](NOTATION.md) notation faithfully — subscript everything
- Every symbol that appears must be defined on first use
- Properties should include at least one non-obvious one (not just the definition restated)
- The connection sentence cites the section/equation number from the paper

---

## Step 5 — Draw diagrams

Every section **must** have a diagram. Use only:
- Box-drawing characters: `─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼ ╭ ╮ ╯ ╰`
- Arrows: `→ ← ↑ ↓ ↔ ⇒ ⟹ ⟶`
- Math symbols: `∑ ∏ ∫ ∂ ∇ ≤ ≥ ≈ ∈ ∉ ⊂ ∩ ∪ ⊗ ⊕`
- Subscript/superscript unicode where needed: `₀ ₁ ₂ ᵀ ⁻¹`

All diagrams go in fenced code blocks.

See [DIAGRAMS.md](DIAGRAMS.md) for ready-to-adapt templates for: probability, linear algebra, calculus, neural networks, information theory, Bayesian networks, optimization landscapes.

**Diagram checklist:**
- [ ] Every box and arrow has a label
- [ ] Tensor/matrix dimensions shown explicitly: `W ∈ ℝ^{d_out × d_in}`
- [ ] Left-to-right for data flow; top-to-bottom for hierarchies
- [ ] No unexplained symbols

---

## Step 6 — Search for resources

For each concept in the inventory, run **all** of these WebSearch queries:

```
"[concept name]" site:distill.pub
"[concept name]" explained site:lilianweng.github.io
"[concept name]" intuition site:betterexplained.com
"[concept name]" visual explanation site:3blue1brown.com
"[concept name]" tutorial filetype:pdf
"[concept name]" site:math.stackexchange.com OR site:stats.stackexchange.com
"[concept name]" lecture notes site:cs.stanford.edu OR site:cs.cmu.edu OR site:mit.edu
```

For each result:
- Record: title, URL, one-line description of what it teaches
- Prefer: interactive/visual explanations > lecture notes > Wikipedia
- Reject: paywalled links, broken links, content that's surface-level only

**Compile into groups:**
- Group resources by topic (matching the primer sections)
- Within each group: sort by quality (Distill/3B1B first, then university notes, then others)
- Add a `★` marker to the single best resource per topic

---

## Step 7 — Assemble and save

Structure of the final output file:

```markdown
# Mathematical Background: [Paper Title]

> **Paper:** [full citation with arxiv link]
> **Primer covers:** [N] concepts across [M] topic areas

## Prerequisites map

[Full ASCII prerequisite tree from Step 3]

---

[One section per concept, ordered foundational → specific]

---

## Resources

### [Topic A]
- ★ [Best Title](url) — [what it teaches]
- [Title](url) — [what it teaches]

### [Topic B]
...
```

Save to `<paper-id>-math-background.md` (or user-specified path).

**Final report to user:**
- Path to the output file
- Total concepts covered
- Deepest concept in the prerequisite tree (= what the paper is "really about" mathematically)
- List of topics where resources were found vs. sparse
