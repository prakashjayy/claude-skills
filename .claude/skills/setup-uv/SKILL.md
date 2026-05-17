---
name: setup-uv
description: Sets up a Python repository using the uv package manager with pyproject.toml. Checks for uv installation and installs it if missing. Optionally configures PyTorch with CPU, CUDA, and macOS/Linux platform-specific variants. Use when user says setup-uv, create a uv project, init repo with uv, or mentions setting up a Python project with optional torch/pytorch support. Required args: repo name and --torch flag.
---

# Setup UV

Sets up a Python project with uv. Required: **repo name** and **--torch** flag (use `--torch` to include PyTorch, omit to skip).

> **Important:** Everything is created **in the current working directory** — no subfolder is created. The repo name is only used as the `name` field in `pyproject.toml`. Never run `uv init <repo-name>` (that creates a folder). Always use `uv init .` to init in-place.

## Workflow

### Step 1 — Check and install uv

```bash
if ! command -v uv &>/dev/null; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
  source "$HOME/.local/bin/env" 2>/dev/null || export PATH="$HOME/.cargo/bin:$HOME/.local/bin:$PATH"
fi
uv --version
```

### Step 2 — Initialize project in-place

```bash
uv init .
```

This creates `pyproject.toml`, `README.md`, and `.python-version` in the current directory — no subfolder.

### Step 3 — Set the project name and create the package directory

After `uv init .`, open `pyproject.toml` and set `name = "<repo-name>"` (from the user's argument).

Then create the package directory so hatchling can locate it (otherwise `uv sync` fails with "Unable to determine which files to ship"):

```bash
mkdir -p <repo-name> && touch <repo-name>/__init__.py
```

### Step 4a — No torch: sync as-is

```bash
uv sync
```

### Step 4b — With `--torch`: overwrite pyproject.toml then sync

Read the template from [TORCH-TEMPLATE.md](TORCH-TEMPLATE.md). Write it to `./pyproject.toml` with `name = "<repo-name>"` substituted. Then:

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

Print the files created with `ls -1` and confirm which torch extra was installed (if any).
