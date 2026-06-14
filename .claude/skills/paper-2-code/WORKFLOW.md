# Full Pipeline Workflow

## Step 0 — Parse arguments

Extract from the invocation:
- `paper`: arxiv ID, arxiv URL, or local path starting with `@`
- `folder`: output directory (ask if missing)
- `--only <subskill>`: if present, run only that subskill and stop
- `--gpus N`: number of GPUs available (optional, used by dataset subskill)
- `--vram Xgb`: VRAM per GPU in GB (optional)
- `--storage Xgb`: available disk storage in GB (optional)

## Step 1 — Environment check

```bash
uv --version 2>/dev/null || echo "MISSING_UV"
[ -f pyproject.toml ] && echo "project exists" || echo "NEED_INIT"
uv run python -c "import pypdf, torch, torchvision" 2>/dev/null || echo "NEED_DEPS"
```

- If uv is missing or no `pyproject.toml`: invoke the `setup-uv` skill with `--torch`.
- If deps are missing: `uv add pypdf torch torchvision pyyaml`.

## Step 2 — Download / locate paper

If paper is an arxiv ID or URL:
```bash
mkdir -p <folder>/papers
curl -L "https://arxiv.org/pdf/<paper-id>" -o "<folder>/papers/<paper-id>.pdf"
```

If paper is `@path/to/file.pdf`, use that path directly.

## Step 3 — Extract paper sections

```bash
uv run python ~/.claude/skills/paper-2-code/scripts/extract_paper.py <pdf-path>
```

This prints: abstract, introduction, method/approach section, training/implementation details, experiments/results, and any algorithm pseudocode blocks. The output gives you the raw material for all subsequent subskills.

**From the extracted text, build an analysis document in memory (not written to disk):**

```
PAPER ANALYSIS
==============
Task type:        <classification / detection / segmentation / generation / SSL / etc.>
Architecture:     <ViT-B, ResNet-50, UNet, Diffusion, etc.>
Datasets used:    <list with sizes mentioned>
Loss functions:   <list with equation locations>
Key hyperparams:  <optimizer, lr, batch size, epochs, etc.>
Evaluation:       <metrics and protocols>
Pseudocode:       <algorithm blocks if any>
```

## Step 4 — Dataset (always first)

Run [DATASET.md](subskills/DATASET.md).

This is interactive — it will ask the user which dataset to use before continuing.
**Do not proceed to Step 5 until the user has confirmed a dataset and the download is complete.**

## Step 5 — Config

Run [CONFIG.md](subskills/CONFIG.md).

Produces `configs/default.yaml` using the paper analysis from Step 3.
This must exist before architecture/losses/train since those reference it.

## Step 6 — Architecture

Run [ARCHITECTURE.md](subskills/ARCHITECTURE.md).

Produces `src/model.py`. Reads `configs/default.yaml` for any dimension/depth params.

## Step 7 — Losses

Run [LOSSES.md](subskills/LOSSES.md).

Produces `src/losses.py`. References model output shapes from Step 6.

## Step 8 — Training

Run [TRAINING.md](subskills/TRAINING.md).

Produces `src/datasets.py` and `src/trainer.py`.

## Step 9 — Evaluation

Run [EVAL.md](subskills/EVAL.md).

Produces `src/evaluate.py`.

## Step 10 — Wire entrypoints

Write `train.py`:
```python
# train.py — generated entry point
import yaml, torch
from src.model import build_model
from src.losses import build_loss
from src.datasets import build_dataloaders
from src.trainer import Trainer

def main():
    cfg = yaml.safe_load(open("configs/default.yaml"))
    model = build_model(cfg)
    loss_fn = build_loss(cfg)
    train_loader, val_loader = build_dataloaders(cfg)
    trainer = Trainer(model, loss_fn, train_loader, val_loader, cfg)
    trainer.fit()

if __name__ == "__main__":
    main()
```

Write `eval.py`:
```python
# eval.py — generated entry point
import yaml, torch
from src.model import build_model
from src.evaluate import Evaluator

def main():
    cfg = yaml.safe_load(open("configs/default.yaml"))
    model = build_model(cfg)
    ckpt = torch.load(cfg["training"]["checkpoint_path"])
    model.load_state_dict(ckpt["model"])
    evaluator = Evaluator(model, cfg)
    evaluator.run()

if __name__ == "__main__":
    main()
```

## Step 11 — README

Write `README.md` with:
1. Paper citation (title, authors, arxiv link)
2. What the paper does in 2 sentences
3. Setup: `uv sync`
4. Training: `uv run python train.py`
5. Evaluation: `uv run python eval.py`
6. Expected results table (copied from paper, clearly marked as "paper's reported numbers")
7. Dataset citation

## Step 12 — Confirm

Report:
```
✓ Dataset:      data/<name>/ (<N> images, <size>GB)
✓ Config:       configs/default.yaml
✓ Architecture: src/model.py  (<param count> params)
✓ Losses:       src/losses.py
✓ Training:     src/trainer.py + src/datasets.py
✓ Evaluation:   src/evaluate.py
✓ Entrypoints:  train.py, eval.py

Run: uv run python train.py
```

---

## `--only` mode

When `--only <subskill>` is passed, skip all other steps and run only that subskill.
The paper analysis from Step 3 is still required — always run Steps 1–3 first.
