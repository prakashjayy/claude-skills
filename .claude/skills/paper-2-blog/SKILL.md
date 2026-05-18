---
name: paper-2-blog
description: Downloads a paper by URL or arxiv ID, reads it, and writes an accessible blog post explaining it from first principles — using analogies, plain language, diagrams, and terminology warnings where the paper uses terms non-standardly. Supports --use-simple-examples to add concrete worked examples with real numbers for every technical concept. Use when user mentions arxiv, a paper URL, a paper ID (e.g. 2301.07041), "explain this paper", "paper to blog", or "summarize research paper".
---

# Paper 2 Blog

## Quick start

```
/paper-2-blog 2301.07041 my-folder
/paper-2-blog https://arxiv.org/abs/2301.07041 my-folder
/paper-2-blog https://example.com/paper.pdf my-folder
/paper-2-blog 2301.07041 my-folder --use-simple-examples
```

If folder name is omitted, ask the user before proceeding.

## Workflows

Follow [WORKFLOW.md](WORKFLOW.md) for full details. Summary:

1. **Resolve** — extract paper ID from any arxiv URL format; confirm folder name
2. **Environment** — check uv + pypdf; invoke setup-uv skill if no `pyproject.toml` exists
3. **Download** — `mkdir -p <folder>` and `curl` the PDF
4. **Extract** — `uv run python scripts/extract_pages.py <folder>/<paper-id>.pdf`
5. **Identify** — build three lists: math concepts, visual opportunities, terminology mismatches
6. **Diagrams** — generate one PNG per visual opportunity using matplotlib; save to `<folder>/`
7. **Write** — produce `<folder>/blog.md` per [BLOG-FRAMEWORK.md](BLOG-FRAMEWORK.md); add terminology warning blockquotes; add worked examples if `--use-simple-examples`
8. **Confirm** — report paths of PDF, blog.md, and each PNG; print title and one-line hook

## Advanced features

| Feature | Reference |
|---|---|
| Blog structure, writing rules, terminology warning format | [BLOG-FRAMEWORK.md](BLOG-FRAMEWORK.md) |
| Worked examples with real numbers (`--use-simple-examples`) | [SIMPLE-EXAMPLES.md](SIMPLE-EXAMPLES.md) |
| Full step-by-step workflow with bash commands | [WORKFLOW.md](WORKFLOW.md) |
| PDF page extraction script | [scripts/extract_pages.py](scripts/extract_pages.py) |
