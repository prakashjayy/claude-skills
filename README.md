# claude-skills

A collection of Claude Code skills for common workflows. Clone this repo and point Claude Code at it to use these skills.

## Available skills

| Skill | Trigger | Description |
|---|---|---|
| `paper-2-blog` | arxiv URL / paper ID / "explain this paper" | Downloads an arxiv paper and writes an accessible first-principles blog post. Add `--use-simple-examples` to ground every concept with real numbers and step-by-step worked examples. |
| `notebook-style` | jupyter / .ipynb / "structure this notebook" | Structures Jupyter notebooks with a pedagogical layout: one idea per cell, narrative markdown between code, progressive concept-building. |
| `setup-uv` | "setup uv" / "init repo with uv" / "uv project" | Sets up a Python repo using the `uv` package manager with `pyproject.toml`. Supports `--torch` for PyTorch with CPU/CUDA/macOS variants. |
| `write-a-skill` | "write a skill" / "create a skill" / "build a skill" | Scaffolds a new Claude Code skill with proper structure, description, and bundled reference files. |
| `github-ready` | "github-ready" / "remove claude from commits" / "clean commit history" | Installs a `commit-msg` hook and adds a CLAUDE.md rule so Claude's name never appears in git history. |
| `paper-2-math-background` | arxiv URL / paper ID / "what math do I need" / "math primer" | Analyzes a research paper and produces a detailed math primer — prerequisite concepts from first principles, precise subscript notation, ASCII diagrams per concept, and a curated resource section via live web search. |
| `paper-2-code` | arxiv ID / PDF / "implement this paper" / "reproduce this paper" | Converts a research paper into a runnable PyTorch project — architecture, losses, training loop, evaluation, and config — with interactive, compute-aware dataset selection. Runs as a full pipeline or as individual subskills. |
| `pragmatic-py` | "pragmatic-py" / "pragmatic style" / "clean python style" | Writes Python in a minimal-boilerplate, functional-first style — short functions, backtick docstrings, selective type hints, and `store_attr`/`patch` idioms. |
