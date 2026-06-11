---
name: paper-to-code
description: Converts a research paper (arxiv ID, URL, or local PDF) into a working PyTorch implementation — architecture, losses, training loop, evaluation, and hyperparameter config — all extracted directly from the paper. Handles dataset selection interactively: asks about compute resources, suggests compute-appropriate datasets (paper's + alternatives), and downloads the chosen one via a background agent. Subskills can be run independently. Use when user says "implement this paper", "paper to code", "replicate paper", "code this paper", "reproduce this paper", or provides an arxiv ID / PDF and wants runnable code.
---

# Paper to Code

Converts a research paper into a runnable PyTorch project. Runs as a full pipeline or as individual subskills.

## Quick start

```
/paper-to-code 2104.14294 dino/
/paper-to-code @dino/papers/dino-v1.pdf dino/
/paper-to-code 2104.14294 dino/ --gpus 1 --vram 8gb --storage 50gb

# Run one subskill only
/paper-to-code @paper.pdf out/ --only dataset
/paper-to-code @paper.pdf out/ --only architecture
/paper-to-code @paper.pdf out/ --only train
```

If output folder is omitted, ask the user before proceeding.

## Subskills

| Flag | File | Produces |
|---|---|---|
| `dataset` | [DATASET.md](subskills/DATASET.md) | `data/<name>/` downloaded + verified |
| `architecture` | [ARCHITECTURE.md](subskills/ARCHITECTURE.md) | `src/model.py` |
| `losses` | [LOSSES.md](subskills/LOSSES.md) | `src/losses.py` |
| `train` | [TRAINING.md](subskills/TRAINING.md) | `src/trainer.py` + `src/datasets.py` |
| `eval` | [EVAL.md](subskills/EVAL.md) | `src/evaluate.py` |
| `config` | [CONFIG.md](subskills/CONFIG.md) | `configs/default.yaml` |

## Output layout

```
<output-folder>/
├── configs/default.yaml     # all hyperparameters from paper
├── data/<dataset>/          # downloaded dataset
├── src/
│   ├── model.py             # architecture
│   ├── losses.py            # loss functions
│   ├── datasets.py          # data loading + augmentation
│   ├── trainer.py           # training engine
│   └── evaluate.py          # metrics
├── train.py                 # entry point: uv run python train.py
├── eval.py                  # entry point: uv run python eval.py
└── README.md                # replication instructions
```

## Full pipeline

See [WORKFLOW.md](WORKFLOW.md) for step-by-step instructions with commands.
