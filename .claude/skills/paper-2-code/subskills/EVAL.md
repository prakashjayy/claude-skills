# Eval Subskill

Extracts the paper's evaluation protocols and implements them as `src/evaluate.py`.

---

## Phase 1 — Identify evaluation protocols from paper

From the experiments / evaluation section, collect:

1. **Primary metric(s)**: Top-1 accuracy, mAP, FID, BLEU, Jaccard, etc.
2. **Evaluation protocols**: linear probe, k-NN, full fine-tuning, zero-shot, etc.
3. **Benchmarks**: what dataset and split are results reported on
4. **Special procedures**: e.g. "freeze backbone, train only linear head for 100 epochs"
5. **Baseline numbers**: what the paper claims (for comparison printing)

For each protocol, record:
- Input: what the model must produce (features, logits, generations)
- Output: the metric value
- Whether it requires additional training (linear probe) or not (k-NN)

---

## Phase 2 — Write `src/evaluate.py`

```python
"""
<PaperTitle> — Evaluation protocols.
Protocols: <list from paper>
"""

from __future__ import annotations
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from typing import Optional


class Evaluator:
    """
    Runs all evaluation protocols defined in the paper.
    Reads protocol config from cfg["evaluation"].
    """
    def __init__(self, model: nn.Module, cfg: dict):
        self.model = model
        self.cfg = cfg
        self.device = next(model.parameters()).device

    def run(self) -> dict[str, float]:
        results = {}
        protocols = self.cfg["evaluation"].get("protocols", ["linear_probe"])
        for protocol in protocols:
            if protocol == "linear_probe":
                results["linear_probe"] = self.linear_probe()
            elif protocol == "knn":
                results["knn"] = self.knn_eval()
            elif protocol == "top1":
                results["top1"] = self.top1_accuracy()
        self._print_results(results)
        return results

    def _extract_features(self, loader: DataLoader) -> tuple[torch.Tensor, torch.Tensor]:
        """Extract backbone features for all images. Returns (features, labels)."""
        all_feats, all_labels = [], []
        self.model.eval()
        with torch.no_grad():
            for imgs, labels in loader:
                imgs = imgs.to(self.device)
                # Use backbone features, not final head output
                feats = self.model.backbone(imgs) if hasattr(self.model, "backbone") else self.model(imgs)
                all_feats.append(feats.cpu())
                all_labels.append(labels)
        return torch.cat(all_feats), torch.cat(all_labels)

    def top1_accuracy(self, loader: Optional[DataLoader] = None) -> float:
        """Standard top-1 accuracy on the validation set."""
        from src.datasets import build_dataloaders
        _, val_loader = build_dataloaders(self.cfg)
        if loader is not None:
            val_loader = loader

        self.model.eval()
        correct = total = 0
        with torch.no_grad():
            for imgs, labels in val_loader:
                imgs, labels = imgs.to(self.device), labels.to(self.device)
                out = self.model(imgs)
                pred = out.argmax(dim=-1)
                correct += (pred == labels).sum().item()
                total += labels.size(0)
        acc = correct / total
        print(f"Top-1 accuracy: {acc * 100:.1f}%")
        return acc

    def linear_probe(self, epochs: int = 100) -> float:
        """
        Freeze backbone, train a single linear layer on top.
        Protocol: <paper section reference>
        """
        from src.datasets import build_dataloaders
        train_loader, val_loader = build_dataloaders(self.cfg)

        # Freeze all parameters
        for p in self.model.parameters():
            p.requires_grad_(False)

        n_classes = self.cfg["dataset"]["num_classes"]
        feat_dim = self._get_feat_dim()
        linear = nn.Linear(feat_dim, n_classes).to(self.device)

        optimizer = torch.optim.SGD(linear.parameters(), lr=0.01, momentum=0.9, weight_decay=0.0)
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            optimizer, T_max=epochs * len(train_loader)
        )

        for epoch in range(1, epochs + 1):
            linear.train()
            for imgs, labels in train_loader:
                imgs, labels = imgs.to(self.device), labels.to(self.device)
                with torch.no_grad():
                    feats = self.model.backbone(imgs) if hasattr(self.model, "backbone") else self.model(imgs)
                logits = linear(feats)
                loss = F.cross_entropy(logits, labels)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                scheduler.step()

        # Evaluate
        linear.eval()
        self.model.eval()
        correct = total = 0
        with torch.no_grad():
            for imgs, labels in val_loader:
                imgs, labels = imgs.to(self.device), labels.to(self.device)
                feats = self.model.backbone(imgs) if hasattr(self.model, "backbone") else self.model(imgs)
                pred = linear(feats).argmax(dim=-1)
                correct += (pred == labels).sum().item()
                total += labels.size(0)

        acc = correct / total
        print(f"Linear probe top-1: {acc * 100:.1f}%")
        return acc

    def knn_eval(self, k: int = 20, temperature: float = 0.07) -> float:
        """
        Weighted k-NN classifier on frozen features. No training required.
        Protocol: <paper section reference>
        k=20 from paper's ablation; temperature=0.07 is standard.
        """
        from src.datasets import build_dataloaders
        train_loader, val_loader = build_dataloaders(self.cfg)

        print("Extracting training features...")
        train_feats, train_labels = self._extract_features(train_loader)
        train_feats = F.normalize(train_feats, dim=-1)

        print("Evaluating k-NN...")
        correct = total = 0
        with torch.no_grad():
            for imgs, labels in val_loader:
                imgs = imgs.to(self.device)
                feats = self.model.backbone(imgs) if hasattr(self.model, "backbone") else self.model(imgs)
                feats = F.normalize(feats.cpu(), dim=-1)

                # cosine similarity → weighted vote
                sim = torch.mm(feats, train_feats.T)          # (B, N_train)
                topk_sim, topk_idx = sim.topk(k, dim=-1)      # (B, k)
                topk_labels = train_labels[topk_idx]           # (B, k)

                # temperature-scaled weighted vote
                weights = F.softmax(topk_sim / temperature, dim=-1)  # (B, k)
                n_classes = self.cfg["dataset"]["num_classes"]
                votes = torch.zeros(feats.size(0), n_classes)
                votes.scatter_add_(1, topk_labels, weights)
                pred = votes.argmax(dim=-1)
                correct += (pred == labels).sum().item()
                total += labels.size(0)

        acc = correct / total
        print(f"k-NN (k={k}) top-1: {acc * 100:.1f}%")
        return acc

    def _get_feat_dim(self) -> int:
        dummy = torch.zeros(1, 3, self.cfg["dataset"]["image_size"],
                            self.cfg["dataset"]["image_size"]).to(self.device)
        with torch.no_grad():
            out = self.model.backbone(dummy) if hasattr(self.model, "backbone") else self.model(dummy)
        return out.shape[-1]

    def _print_results(self, results: dict[str, float]):
        print("\n" + "=" * 50)
        print("EVALUATION RESULTS")
        print("=" * 50)
        baselines = self.cfg["evaluation"].get("paper_baselines", {})
        for metric, value in results.items():
            line = f"  {metric:20s}: {value * 100:.1f}%"
            if metric in baselines:
                line += f"  (paper: {baselines[metric] * 100:.1f}%)"
            print(line)
        print("=" * 50)
```

---

## Protocol selection by task type

| Task | Protocols to implement |
|---|---|
| Image classification (supervised) | `top1_accuracy` |
| Image classification (SSL pre-training) | `linear_probe`, `knn_eval` |
| Object detection | `map` via `torchmetrics.detection.MeanAveragePrecision` |
| Semantic segmentation | `miou` via `torchmetrics.JaccardIndex` |
| Image generation | `fid` via `torchmetrics.image.FrechetInceptionDistance` |
| Video tracking | Not implemented inline — note that DAVIS eval needs external tools |

For detection/segmentation, add `uv add torchmetrics` and use the library rather than implementing from scratch.

---

## Comparison table

After evaluation, always print the paper's reported numbers alongside yours so the user can see if replication is on track:

```
==================================================
EVALUATION RESULTS
==================================================
  linear_probe        : 76.1%  (paper: 77.0%)  ← within expected range
  knn_eval            : 72.8%  (paper: 74.5%)  ← gap likely due to smaller dataset
==================================================
```

Populate `paper_baselines` in `configs/default.yaml` → `evaluation` section during the config subskill.
