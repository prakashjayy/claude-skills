---
name: paper-2-math-background
description: Analyzes a research paper and produces a detailed mathematical primer covering every prerequisite concept from first principles — with precise subscript notation (P_{XY}(x,y) style), ASCII/Unicode diagrams per concept embedded in markdown, and a resource section assembled via live web search. Use when user provides a paper (arxiv ID, URL, or text) and asks for math background, prerequisites, "what math do I need", "math primer", "explain the math in", or "understand this paper mathematically".
---

# Paper 2 Math Background

## Quick start

```
/paper-2-math-background 2301.07041
/paper-2-math-background https://arxiv.org/abs/2301.07041
/paper-2-math-background https://arxiv.org/abs/2301.07041 --output results/
```

If no output path is given, save to `<paper-id>-math-background.md` in the current directory.

## Workflow

Full details in [WORKFLOW.md](WORKFLOW.md). Steps:

1. **Ingest** — fetch paper via WebFetch (arxiv abstract + PDF); fall back to abstract + intro if PDF unavailable
2. **Inventory** — extract every mathematical object: distributions, operators, named theorems, loss functions, algorithms
3. **Prerequisite tree** — trace each concept back to something a calculus/linear-algebra student would know; order foundational → paper-specific
4. **Write primer** — one `##` section per concept following the per-concept template in [WORKFLOW.md](WORKFLOW.md)
5. **Diagrams** — mandatory ASCII/Unicode diagram in every section; templates in [DIAGRAMS.md](DIAGRAMS.md)
6. **Resources** — WebSearch each concept with 5+ targeted queries; collect URLs + one-line descriptions; deduplicate
7. **Save** — write final markdown; print path and total concept count

## Notation rules

Full reference in [NOTATION.md](NOTATION.md). Non-negotiable:
- Subscript names the random variable; argument is its value: `P_{XY}(x, y)`, **never** `P(X, Y)`
- Conditionals: `P_{X|Y}(x ∣ y)`, not `P(X|Y)`
- Expectations: `𝔼_{X ∼ P_X}[f(X)]`
- Gradients: `∇_θ ℒ(θ)`, not `∇ℒ`
- Spaces: `ℝ^d`, `L²(ℝ^d)`, `𝒳`

## Output structure

```markdown
# Mathematical Background: [Paper Title]

## Prerequisites map
[ASCII dependency tree of all concepts]

## [Concept Name]
**Intuition** · **Definition** · **Diagram** · **Key properties** · **Connection to paper**

...  (ordered foundational → specific)

## Resources
### [Topic A]
- [Title](url) — what it teaches
### [Topic B]
...
```

## Advanced reference

| Topic | File |
|---|---|
| Step-by-step workflow with search queries | [WORKFLOW.md](WORKFLOW.md) |
| Notation system and conventions | [NOTATION.md](NOTATION.md) |
| ASCII/Unicode diagram templates | [DIAGRAMS.md](DIAGRAMS.md) |
