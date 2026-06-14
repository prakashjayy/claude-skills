# Architecture Subskill

Extracts the model architecture from the paper and implements it as `src/model.py`.

---

## Phase 1 — Parse architecture from paper

From the paper analysis, identify:

1. **Backbone**: the main feature extractor (e.g. ViT, ResNet, UNet encoder)
   - Number of layers / blocks / stages
   - Hidden dimension, number of heads (if transformer)
   - Input/output shape

2. **Head(s)**: task-specific modules attached to the backbone
   - Classification head, projection head, decoder, etc.
   - Activation functions, normalization

3. **Special components**: any non-standard modules
   - Custom attention mechanisms
   - Codebooks, quantizers
   - Momentum/EMA copies of the model

4. **Normalization**: BatchNorm, LayerNorm, GroupNorm, none
   - Note if the paper explicitly says "BN-free" — this affects head design

5. **Initialization**: any custom weight init mentioned

6. **Reference implementation**: check if paper links a GitHub repo
   - If yes: note it in a comment in the code but implement from scratch
   - Do not copy-paste from the repo; derive from the paper text

---

## Phase 2 — Check for existing PyTorch primitives

Before implementing from scratch, check if PyTorch or torchvision already has the component:

```python
# ViT  → torch.hub.load('facebookresearch/dino', 'dino_vits16')
#        OR timm.create_model('vit_small_patch16_224')
# ResNet → torchvision.models.resnet50(weights=None)
# UNet  → implement from scratch (standard U-Net not in torchvision)
```

If a standard backbone exists in `timm` or `torchvision`:
- Use it as the backbone with `weights=None` (no pretrained weights)
- Implement only the custom head / wrapper from scratch
- Note this clearly in a comment

If not, implement the full architecture from the paper.

---

## Phase 3 — Write `src/model.py`

Structure:

```python
"""
<PaperTitle> — <Component> implementation.
Paper: <arxiv link>
Architecture: <one-line description>
"""

from __future__ import annotations
import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from dataclasses import dataclass
from typing import Optional


@dataclass
class ModelConfig:
    """All architecture hyperparameters. Populated from configs/default.yaml."""
    # backbone
    embed_dim: int = 384
    depth: int = 12
    num_heads: int = 6
    patch_size: int = 16
    img_size: int = 224
    # head
    out_dim: int = 65536
    # ... (paper-specific fields)


class <BackboneName>(nn.Module):
    """
    <One-line description of what this module does>
    Input:  (B, C, H, W)
    Output: (B, embed_dim)
    """
    def __init__(self, cfg: ModelConfig) -> None:
        super().__init__()
        # ... layers

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Add shape comments on non-obvious operations
        # x: (B, C, H, W)
        ...
        # out: (B, embed_dim)
        return out


class <HeadName>(nn.Module):
    """
    <One-line description>
    Input:  (B, in_dim)
    Output: (B, out_dim)
    """
    def __init__(self, cfg: ModelConfig) -> None:
        super().__init__()
        ...

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        ...


def build_model(cfg: dict) -> nn.Module:
    """
    Entry point: build model from config dict (loaded from configs/default.yaml).
    Returns the full model ready for training.
    """
    model_cfg = ModelConfig(**cfg["model"])
    backbone = <BackboneName>(model_cfg)
    head = <HeadName>(model_cfg)
    return <FullModel>(backbone, head, model_cfg)
```

### Rules for writing the code

1. **Shape annotations**: every tensor that changes shape gets a comment `# (B, C, H, W) → (B, D)`
2. **One class per conceptual module** — backbone, head, wrapper each get their own class
3. **No magic numbers** — all dimensions reference `cfg` fields
4. **Match paper notation** — use the same variable names as the paper where unambiguous
5. **No forward compatibility** — implement what the paper describes, nothing more
6. **If paper has multiple architecture variants** (e.g. ViT-S/16, ViT-B/8): use a single class with config fields, not separate classes

---

## Phase 4 — Parameter count check

After writing the model, add a `__main__` block at the bottom:

```python
if __name__ == "__main__":
    import yaml
    cfg = yaml.safe_load(open("configs/default.yaml"))
    model = build_model(cfg)
    n_params = sum(p.numel() for p in model.parameters()) / 1e6
    print(f"Parameters: {n_params:.1f}M")
    # sanity forward pass
    x = torch.randn(2, 3, cfg["dataset"]["image_size"], cfg["dataset"]["image_size"])
    out = model(x)
    print(f"Output shape: {out.shape}")
```

Run it and report the parameter count to the user. Compare against paper's reported count (e.g. "Paper reports 21M params — got 21.0M ✓").

---

## Special architecture patterns

### Self-supervised teacher-student
If the paper has a teacher (EMA copy of student):

```python
class StudentTeacher(nn.Module):
    def __init__(self, student: nn.Module, momentum: float = 0.996):
        super().__init__()
        self.student = student
        self.teacher = copy.deepcopy(student)
        for p in self.teacher.parameters():
            p.requires_grad_(False)
        self.momentum = momentum

    @torch.no_grad()
    def update_teacher(self):
        for s, t in zip(self.student.parameters(), self.teacher.parameters()):
            t.data.mul_(self.momentum).add_((1 - self.momentum) * s.data)
```

### Diffusion / U-Net style
Split into `Encoder`, `Bottleneck`, `Decoder` classes with skip connections passed explicitly.

### Transformers (ViT-style)
Implement: `PatchEmbed` → `TransformerBlock` (with `Attention` + `MLP` sub-modules) → `CLSToken` logic.
Use `nn.MultiheadAttention` only if the paper uses standard attention. Implement custom attention if the paper describes a non-standard variant.
