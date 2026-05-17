# claude-skills

A collection of Claude Code skills for common workflows. Clone this repo and point Claude Code at it to use these skills.

## Available skills

| Skill | Trigger | Description |
|---|---|---|
| `paper-2-blog` | arxiv URL / paper ID / "explain this paper" | Downloads an arxiv paper and writes an accessible first-principles blog post. Add `--use-simple-examples` to ground every concept with real numbers and step-by-step worked examples. |
| `notebook-style` | jupyter / .ipynb / "structure this notebook" | Structures Jupyter notebooks with a pedagogical layout: one idea per cell, narrative markdown between code, progressive concept-building. |
| `setup-uv` | "setup uv" / "init repo with uv" / "uv project" | Sets up a Python repo using the `uv` package manager with `pyproject.toml`. Supports `--torch` for PyTorch with CPU/CUDA/macOS variants. |
| `write-a-skill` | "write a skill" / "create a skill" / "build a skill" | Scaffolds a new Claude Code skill with proper structure, description, and bundled reference files. |
