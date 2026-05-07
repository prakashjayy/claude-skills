---
name: setup-uv
description: Sets up a Python repository using the uv package manager with pyproject.toml. Checks for uv installation and installs it if missing. Optionally configures PyTorch with CPU, CUDA, and macOS/Linux platform-specific variants. Use when user says setup-uv, create a uv project, init repo with uv, or mentions setting up a Python project with optional torch/pytorch support. Required args: repo name and --torch flag.
---

# Setup UV

Sets up a Python project with uv. Required: **repo name** and **--torch** flag (use `--torch` to include PyTorch, omit to skip).

## Workflow

### Step 1 — Check and install uv

```bash
if ! command -v uv &>/dev/null; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
  source "$HOME/.local/bin/env" 2>/dev/null || export PATH="$HOME/.cargo/bin:$HOME/.local/bin:$PATH"
fi
uv --version
```

### Step 2 — Initialize project

```bash
uv init <repo-name>
cd <repo-name>
```

### Step 3a — No torch: leave pyproject.toml as-is, then sync

```bash
uv sync
```

### Step 3b — With `--torch`: replace pyproject.toml with the template in [TORCH-TEMPLATE.md](TORCH-TEMPLATE.md), then sync

Substitute `<repo-name>` for the `name` field. After writing the file:

```bash
# macOS or CPU-only Linux
uv sync --extra torch-cpu

# Linux with NVIDIA GPU (CUDA)
uv sync --extra torch-cuda
```

Ask the user which sync command to run if their target platform is ambiguous.

## Platform guide

| Platform | Command |
|---|---|
| macOS (Apple Silicon or Intel) | `uv sync --extra torch-cpu` |
| Linux — CPU only | `uv sync --extra torch-cpu` |
| Linux — NVIDIA GPU | `uv sync --extra torch-cuda` |

macOS gets MPS acceleration via the standard CPU wheel — no separate index needed.

## After setup

Print the final project structure with `find <repo-name> -not -path '*/.venv/*' | head -20` and confirm which torch extra was installed (if any).
