# Losses Subskill

Extracts every loss function from the paper and implements them as `src/losses.py`.

---

## Phase 1 — Inventory losses from paper

Scan the paper for:
1. **Named loss functions** with equation numbers (e.g. "cross-entropy loss (Eq. 2)", "InfoNCE")
2. **Weighted combinations**: `L = α L_recon + β L_kl`
3. **Auxiliary losses**: perceptual loss, gradient penalty, etc.
4. **Temperature parameters**: τ or similar scaling factors
5. **Stop-gradient / detach** instructions (critical for SSL)

For each loss, record:
- Name used in paper
- Mathematical formula (exact notation)
- Inputs required (what comes from model, what from data)
- Any conditions (only applied after N epochs, only for certain crops, etc.)

---

## Phase 2 — Map to PyTorch primitives

| Paper loss | PyTorch equivalent | Notes |
|---|---|---|
| Cross-entropy | `F.cross_entropy` | check if targets are soft or hard |
| MSE / L2 | `F.mse_loss` | |
| InfoNCE / NT-Xent | implement from scratch | no standard PyTorch implementation |
| KL divergence | `F.kl_div` | needs log-space input |
| Cosine similarity | `F.cosine_similarity` | |
| Perceptual (VGG) | implement using `torchvision.models.vgg16` | |
| Binary cross-entropy | `F.binary_cross_entropy_with_logits` | |
| Focal loss | implement from scratch | |
| ELBO / VAE loss | implement from scratch | |

---

## Phase 3 — Write `src/losses.py`

Structure:

```python
"""
<PaperTitle> — Loss functions.
Paper section: <section number and name>
"""

from __future__ import annotations
import torch
import torch.nn as nn
import torch.nn.functional as F


class <LossName>(nn.Module):
    """
    <Formula from paper, one line>
    Inputs:
      pred:   (B, K) — student softmax output
      target: (B, K) — teacher softmax output (detached)
    Output: scalar loss
    """
    def __init__(self, temperature: float = 0.1, **kwargs):
        super().__init__()
        self.temperature = temperature
        # register any buffers (e.g. running center for DINO)

    def forward(self, pred: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        # Implement formula exactly as in paper
        # Add inline comment referencing equation number: # Eq. (2)
        ...


class CombinedLoss(nn.Module):
    """
    Weighted combination: L = α * loss_A + β * loss_B
    Alpha and beta from configs/default.yaml → training.loss_weights
    """
    def __init__(self, cfg: dict):
        super().__init__()
        weights = cfg["training"].get("loss_weights", {})
        self.loss_a = <LossA>(...)
        self.loss_b = <LossB>(...)
        self.alpha = weights.get("a", 1.0)
        self.beta  = weights.get("b", 1.0)

    def forward(self, **kwargs) -> dict[str, torch.Tensor]:
        la = self.loss_a(...)
        lb = self.loss_b(...)
        total = self.alpha * la + self.beta * lb
        return {"total": total, "loss_a": la.detach(), "loss_b": lb.detach()}


def build_loss(cfg: dict) -> nn.Module:
    """Build loss from config dict."""
    ...
```

### Rules

1. **Exact formula match**: copy the paper's formula into a comment above the `forward` method. Example:
   ```python
   # H(P_t, P_s) = -P_t * log(P_s)   [Eq. 2]
   loss = -(target * torch.log(pred + 1e-8)).sum(dim=-1).mean()
   ```

2. **Detach where the paper says stop-gradient**: always mark with a comment:
   ```python
   target = target.detach()  # stop-gradient on teacher output [Section 3.1]
   ```

3. **Numerical stability**: add `+ 1e-8` to log arguments, clamp before sqrt, etc.

4. **Return a dict** from `CombinedLoss.forward()`: `{"total": ..., "loss_a": ..., "loss_b": ...}`. This lets the trainer log each component separately.

5. **Temperature as a parameter, not a constant**: even if the paper uses a fixed value, pass it through config so it can be changed.

---

## Phase 4 — Sanity test

Add a `__main__` block:

```python
if __name__ == "__main__":
    import yaml
    cfg = yaml.safe_load(open("configs/default.yaml"))
    loss_fn = build_loss(cfg)

    # create dummy inputs matching expected shapes
    B, K = 4, cfg["model"]["out_dim"]
    pred   = torch.randn(B, K)
    target = torch.randn(B, K).detach()

    out = loss_fn(pred=pred, target=target)
    if isinstance(out, dict):
        for k, v in out.items():
            print(f"  {k}: {v.item():.4f}")
    else:
        print(f"  loss: {out.item():.4f}")
    print("✓ Losses OK")
```

Run it and report output shapes and loss values to the user.

---

## Common patterns to watch for

### DINO-style centering
If paper applies a running-mean centering before softmax:
```python
class DINOLoss(nn.Module):
    def __init__(self, out_dim, center_momentum=0.9, teacher_temp=0.07, student_temp=0.1):
        super().__init__()
        self.student_temp = student_temp
        self.teacher_temp = teacher_temp
        self.center_momentum = center_momentum
        self.register_buffer("center", torch.zeros(1, out_dim))

    @torch.no_grad()
    def update_center(self, teacher_output: torch.Tensor):
        batch_center = teacher_output.mean(dim=0, keepdim=True)
        self.center = self.center * self.center_momentum + batch_center * (1 - self.center_momentum)

    def forward(self, student_out, teacher_out):
        student_out = student_out / self.student_temp
        teacher_out = F.softmax((teacher_out - self.center) / self.teacher_temp, dim=-1).detach()
        student_out = F.log_softmax(student_out, dim=-1)
        loss = -(teacher_out * student_out).sum(dim=-1).mean()
        self.update_center(teacher_out)
        return loss
```

### Contrastive InfoNCE
```python
def info_nce(z1, z2, temperature=0.07):
    # normalize
    z1 = F.normalize(z1, dim=-1)
    z2 = F.normalize(z2, dim=-1)
    B = z1.size(0)
    logits = torch.mm(z1, z2.T) / temperature   # (B, B)
    labels = torch.arange(B, device=z1.device)
    loss = F.cross_entropy(logits, labels)
    return loss
```

### VAE ELBO
```python
def elbo_loss(recon, x, mu, logvar, beta=1.0):
    recon_loss = F.mse_loss(recon, x, reduction='sum') / x.size(0)
    kl = -0.5 * (1 + logvar - mu.pow(2) - logvar.exp()).sum(dim=-1).mean()
    return recon_loss + beta * kl
```
