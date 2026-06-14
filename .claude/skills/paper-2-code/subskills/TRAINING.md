# Training Subskill

Produces `src/datasets.py` and `src/trainer.py` extracted from the paper's training procedure.

---

## Phase 1 — Extract training procedure from paper

From the paper's implementation/training details section, collect:

**Optimizer**
- Type: AdamW, SGD, LARS, etc.
- Learning rate (base lr + scaling rule if mentioned, e.g. `lr = base_lr × batch_size / 256`)
- Weight decay
- Momentum (if SGD)
- Beta1, Beta2 (if Adam)
- Layer-wise decay if mentioned (common in ViT finetuning)

**Scheduler**
- Type: cosine annealing, linear warmup + cosine, step decay, constant
- Warmup epochs
- Min lr at end

**Batch size and distributed training**
- Total batch size and per-GPU batch size
- Number of GPUs used in paper (for context — user may have fewer)

**Augmentation pipeline**
- Every augmentation mentioned: random crop, horizontal flip, color jitter, Gaussian blur, solarization, grayscale, etc.
- Parameters: crop scale range, color jitter strength, blur kernel size
- Multi-crop details if SSL (global crop size, local crop size, number of each)

**Training duration**
- Number of epochs
- Any curriculum (e.g. warmup teacher temperature)

**Gradient clipping** — clip value if mentioned

**Mixed precision** — fp16/bf16 if mentioned

---

## Phase 2 — Write `src/datasets.py`

```python
"""
<PaperTitle> — Data loading and augmentation.
Augmentation source: <paper section / table reference>
"""

from __future__ import annotations
import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms


def build_train_transform(cfg: dict) -> transforms.Compose:
    """
    Augmentation pipeline from paper.
    Each transform is commented with the paper reference where it was specified.
    """
    img_size = cfg["dataset"]["image_size"]
    mean = cfg["dataset"]["mean"]
    std  = cfg["dataset"]["std"]

    return transforms.Compose([
        transforms.RandomResizedCrop(img_size, scale=(0.2, 1.0)),  # paper Section 3
        transforms.RandomHorizontalFlip(),
        transforms.ColorJitter(brightness=0.4, contrast=0.4,       # paper Appendix
                               saturation=0.4, hue=0.1),
        transforms.ToTensor(),
        transforms.Normalize(mean=mean, std=std),
    ])


def build_val_transform(cfg: dict) -> transforms.Compose:
    img_size = cfg["dataset"]["image_size"]
    return transforms.Compose([
        transforms.Resize(int(img_size * 256 / 224)),
        transforms.CenterCrop(img_size),
        transforms.ToTensor(),
        transforms.Normalize(mean=cfg["dataset"]["mean"], std=cfg["dataset"]["std"]),
    ])


def build_dataloaders(cfg: dict) -> tuple[DataLoader, DataLoader]:
    """Return (train_loader, val_loader)."""
    root = cfg["dataset"]["root"]
    train_ds = datasets.ImageFolder(
        root=f"{root}/{cfg['dataset']['train_split']}",
        transform=build_train_transform(cfg),
    )
    val_ds = datasets.ImageFolder(
        root=f"{root}/{cfg['dataset']['val_split']}",
        transform=build_val_transform(cfg),
    )
    train_loader = DataLoader(
        train_ds,
        batch_size=cfg["training"]["batch_size"],
        shuffle=True,
        num_workers=cfg["training"]["num_workers"],
        pin_memory=True,
        drop_last=True,
    )
    val_loader = DataLoader(
        val_ds,
        batch_size=cfg["training"]["batch_size"] * 2,
        shuffle=False,
        num_workers=cfg["training"]["num_workers"],
        pin_memory=True,
    )
    return train_loader, val_loader
```

### Multi-crop (SSL)
If the paper uses multi-crop (e.g. DINO, SwAV), implement a `MultiCropDataset` wrapper:

```python
class MultiCropDataset(torch.utils.data.Dataset):
    """
    Applies multiple independent crop transforms to each image.
    Returns a list of tensors [global_crop_1, global_crop_2, local_1, ..., local_N]
    """
    def __init__(self, base_dataset, global_transforms, local_transforms):
        self.dataset = base_dataset
        self.global_transforms = global_transforms  # list of 2 transforms
        self.local_transforms = local_transforms    # list of N transforms

    def __len__(self): return len(self.dataset)

    def __getitem__(self, idx):
        img, label = self.dataset[idx]
        crops = [t(img) for t in self.global_transforms + self.local_transforms]
        return crops, label
```

---

## Phase 3 — Write `src/trainer.py`

```python
"""
<PaperTitle> — Training engine.
Training procedure: <paper section reference>
"""

from __future__ import annotations
import math
import time
from pathlib import Path
import torch
import torch.nn as nn
from torch.utils.data import DataLoader


class Trainer:
    def __init__(
        self,
        model: nn.Module,
        loss_fn: nn.Module,
        train_loader: DataLoader,
        val_loader: DataLoader,
        cfg: dict,
    ):
        self.model = model
        self.loss_fn = loss_fn
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.cfg = cfg
        self.device = torch.device("cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")
        self.model.to(self.device)
        self.optimizer = self._build_optimizer()
        self.scheduler = self._build_scheduler()
        self.scaler = torch.amp.GradScaler(enabled=cfg["training"].get("fp16", False))
        self.save_dir = Path(cfg["training"].get("checkpoint_dir", "checkpoints"))
        self.save_dir.mkdir(exist_ok=True)

    def _build_optimizer(self) -> torch.optim.Optimizer:
        opt_cfg = self.cfg["training"]["optimizer"]
        name = opt_cfg["type"].lower()
        params = self._param_groups()  # apply weight decay only to non-bias/norm params
        if name == "adamw":
            return torch.optim.AdamW(params, lr=opt_cfg["lr"], weight_decay=opt_cfg["weight_decay"],
                                     betas=(opt_cfg.get("beta1", 0.9), opt_cfg.get("beta2", 0.999)))
        elif name == "sgd":
            return torch.optim.SGD(params, lr=opt_cfg["lr"], momentum=opt_cfg.get("momentum", 0.9),
                                   weight_decay=opt_cfg["weight_decay"])
        raise ValueError(f"Unknown optimizer: {name}")

    def _param_groups(self) -> list[dict]:
        # Don't apply weight decay to bias and normalization parameters
        decay, no_decay = [], []
        for name, p in self.model.named_parameters():
            if not p.requires_grad: continue
            if p.ndim == 1 or "bias" in name or "norm" in name:
                no_decay.append(p)
            else:
                decay.append(p)
        wd = self.cfg["training"]["optimizer"]["weight_decay"]
        return [{"params": decay, "weight_decay": wd}, {"params": no_decay, "weight_decay": 0.0}]

    def _build_scheduler(self) -> torch.optim.lr_scheduler.LRScheduler:
        sched_cfg = self.cfg["training"]["scheduler"]
        total_steps = len(self.train_loader) * self.cfg["training"]["epochs"]
        warmup_steps = len(self.train_loader) * sched_cfg.get("warmup_epochs", 0)
        if sched_cfg["type"] == "cosine":
            base = torch.optim.lr_scheduler.CosineAnnealingLR(
                self.optimizer, T_max=total_steps - warmup_steps,
                eta_min=sched_cfg.get("min_lr", 0.0)
            )
            if warmup_steps == 0:
                return base
            warmup = torch.optim.lr_scheduler.LinearLR(
                self.optimizer, start_factor=1e-6, end_factor=1.0, total_iters=warmup_steps
            )
            return torch.optim.lr_scheduler.SequentialLR(
                self.optimizer, schedulers=[warmup, base], milestones=[warmup_steps]
            )
        raise ValueError(f"Unknown scheduler: {sched_cfg['type']}")

    def fit(self):
        best_val_loss = float("inf")
        for epoch in range(1, self.cfg["training"]["epochs"] + 1):
            t0 = time.time()
            train_metrics = self._train_epoch(epoch)
            val_metrics   = self._val_epoch(epoch)
            elapsed = time.time() - t0

            self._log(epoch, train_metrics, val_metrics, elapsed)

            if val_metrics.get("loss", float("inf")) < best_val_loss:
                best_val_loss = val_metrics["loss"]
                self._save_checkpoint(epoch, is_best=True)
            elif epoch % self.cfg["training"].get("save_every", 10) == 0:
                self._save_checkpoint(epoch, is_best=False)

            # update EMA teacher if model has one
            if hasattr(self.model, "update_teacher"):
                self.model.update_teacher()

    def _train_epoch(self, epoch: int) -> dict:
        self.model.train()
        total_loss = 0.0
        for batch in self.train_loader:
            imgs, labels = self._to_device(batch)
            with torch.amp.autocast(device_type=self.device.type,
                                     enabled=self.cfg["training"].get("fp16", False)):
                out = self.model(imgs)
                loss_dict = self.loss_fn(out, labels)
                loss = loss_dict["total"] if isinstance(loss_dict, dict) else loss_dict

            self.optimizer.zero_grad()
            self.scaler.scale(loss).backward()
            if clip := self.cfg["training"].get("grad_clip"):
                self.scaler.unscale_(self.optimizer)
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), clip)
            self.scaler.step(self.optimizer)
            self.scaler.update()
            self.scheduler.step()
            total_loss += loss.item()
        return {"loss": total_loss / len(self.train_loader)}

    @torch.no_grad()
    def _val_epoch(self, epoch: int) -> dict:
        self.model.eval()
        total_loss, correct, total = 0.0, 0, 0
        for batch in self.val_loader:
            imgs, labels = self._to_device(batch)
            out = self.model(imgs)
            loss_dict = self.loss_fn(out, labels)
            loss = loss_dict["total"] if isinstance(loss_dict, dict) else loss_dict
            total_loss += loss.item()
            if isinstance(out, torch.Tensor) and out.ndim == 2:
                correct += (out.argmax(1) == labels).sum().item()
                total += labels.size(0)
        metrics = {"loss": total_loss / len(self.val_loader)}
        if total > 0:
            metrics["acc"] = correct / total
        return metrics

    def _to_device(self, batch):
        if isinstance(batch, (list, tuple)):
            return [b.to(self.device) if isinstance(b, torch.Tensor) else b for b in batch]
        return batch.to(self.device)

    def _save_checkpoint(self, epoch: int, is_best: bool):
        fname = "best.pt" if is_best else f"epoch_{epoch:04d}.pt"
        torch.save({
            "epoch": epoch,
            "model": self.model.state_dict(),
            "optimizer": self.optimizer.state_dict(),
            "scheduler": self.scheduler.state_dict(),
        }, self.save_dir / fname)

    def _log(self, epoch: int, train: dict, val: dict, elapsed: float):
        parts = [f"Epoch {epoch:4d}"]
        parts += [f"train/{k}: {v:.4f}" for k, v in train.items()]
        parts += [f"val/{k}: {v:.4f}" for k, v in val.items()]
        parts.append(f"time: {elapsed:.1f}s")
        print("  ".join(parts))
```

---

## Trainer customizations by paper type

### SSL (self-supervised, no labels)
- `_val_epoch` should call the k-NN evaluator from `src/evaluate.py` every N epochs
- `_train_epoch` receives list of crops, not `(imgs, labels)` — adjust accordingly
- Teacher update happens outside `_train_epoch`

### Generative models (VAE, diffusion)
- `_val_epoch` logs reconstruction loss + KL separately
- No accuracy metric

### Detection / segmentation
- `_val_epoch` calls `torchmetrics` or `pycocotools` for mAP — do not implement from scratch
- Add `uv add torchmetrics` if needed
