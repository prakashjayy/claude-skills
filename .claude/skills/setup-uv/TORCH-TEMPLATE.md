# PyTorch pyproject.toml Template

Use this when `--torch` is passed. Replace `<repo-name>` with the actual project name.

```toml
[project]
name = "<repo-name>"
version = "0.1.0"
requires-python = ">=3.10"
description = ""
readme = "README.md"
dependencies = []

[project.optional-dependencies]
# macOS (Apple Silicon / Intel) — MPS acceleration built into the CPU wheel
# Linux CPU-only
torch-cpu = [
  "torch>=2.6.0",
  "torchvision>=0.21.0",
  "torchaudio>=2.6.0",
]
# Linux with NVIDIA GPU (CUDA 12.4)
torch-cuda = [
  "torch>=2.6.0",
  "torchvision>=0.21.0",
  "torchaudio>=2.6.0",
]

[tool.uv]
# Prevent accidental co-installation of both extras
conflicts = [
  [
    { extra = "torch-cpu" },
    { extra = "torch-cuda" },
  ],
]

[tool.uv.sources]
torch = [
  # macOS always uses CPU index (MPS is bundled)
  { index = "pytorch-cpu", marker = "sys_platform == 'darwin'" },
  # Linux explicit extras
  { index = "pytorch-cpu", extra = "torch-cpu" },
  { index = "pytorch-cuda", extra = "torch-cuda" },
]
torchvision = [
  { index = "pytorch-cpu", marker = "sys_platform == 'darwin'" },
  { index = "pytorch-cpu", extra = "torch-cpu" },
  { index = "pytorch-cuda", extra = "torch-cuda" },
]
torchaudio = [
  { index = "pytorch-cpu", marker = "sys_platform == 'darwin'" },
  { index = "pytorch-cpu", extra = "torch-cpu" },
  { index = "pytorch-cuda", extra = "torch-cuda" },
]

[[tool.uv.index]]
name = "pytorch-cpu"
url = "https://download.pytorch.org/whl/cpu"
explicit = true

[[tool.uv.index]]
name = "pytorch-cuda"
url = "https://download.pytorch.org/whl/cu124"
explicit = true

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

## Notes

- CUDA index pinned to **cu124** (CUDA 12.4). Update to `cu126` etc. if the user has a newer driver.
- The `conflicts` block prevents `torch-cpu` and `torch-cuda` from being installed together.
- `sys_platform == 'darwin'` routes macOS to the CPU index automatically, regardless of which extra is requested.
