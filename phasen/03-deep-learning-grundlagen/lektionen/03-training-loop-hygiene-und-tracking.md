---
id: 03.03
titel: Training-Loop-Hygiene + lokales Tracking mit MLflow 3
phase: 03-deep-learning-grundlagen
dauer_minuten: 90
schwierigkeit: mittel
stand: 2026-04-29
voraussetzungen: [03.02]
lernziele:
  - Mixed Precision (BF16), Gradient Accumulation, LR-Scheduler-Standards 2026
  - PyTorch Lightning vs. nackter PyTorch — wann was
  - MLflow 3.11 (lokal, DACH-konform) statt W&B (US-Datenresidenz)
  - DSGVO Art. 44 + AI-Act Art. 11: Tracking-Disziplin
compliance_anker:
  - mlflow-lokal-statt-wandb-us
  - reproducible-training
ai_act_artikel:
  - art-11
dsgvo_artikel:
  - art-44
---

## Worum es geht

> Stop hand-rolling training loops. — 2026 sind die Standard-Patterns klar: **Mixed Precision** (bf16), **Gradient Accumulation**, **Cosine-Schedule-with-Warmup**, **Gradient-Clipping**. Plus ein **lokales Tracking** mit MLflow 3 statt W&B aus US-Compliance-Gründen.

Diese Lektion zeigt das End-to-End-Pattern für ein Training mit AI-Act-konformer Tech-Doku — und beantwortet die Lightning-vs-Vanilla-Frage.

## Voraussetzungen

- Lektion 03.02 (MLP/CNN-Bausteine)

## Konzept

### Schritt 1: Reproduzierbarkeit — Pflicht-Disziplin

Vor jedem Training:

```python
import random
import numpy as np
import torch

SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
torch.cuda.manual_seed_all(SEED)

# Deterministic-Modus (mit Performance-Trade-off)
# torch.use_deterministic_algorithms(True)
```

**AI-Act Art. 11** verlangt nachvollziehbare Trainings-Runs. Random-Seed setzen und committen ist Minimum.

### Schritt 2: Mixed Precision (BF16)

```python
from torch.amp import autocast, GradScaler

scaler = GradScaler("cuda")

for batch in loader:
    optimizer.zero_grad()
    with autocast("cuda", dtype=torch.bfloat16):
        loss = loss_fn(modell(batch.x), batch.y)
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
```

**Speedup**: 1.5-2× auf H100/H200/B200 vs. fp32. Memory: halb.

**Wann fp16 statt bf16?** Eigentlich nie (mehr) auf modernen GPUs. fp16 hat Range-Probleme; bf16 ist sicherer.

### Schritt 3: Gradient Accumulation — große Batches auf kleinen GPUs

Wenn dein Effektiv-Batch-Size 256 sein soll, aber nur 32 ins VRAM passen:

```python
ACCUM_STEPS = 8

for i, batch in enumerate(loader):
    with autocast("cuda", dtype=torch.bfloat16):
        loss = loss_fn(modell(batch.x), batch.y) / ACCUM_STEPS
    scaler.scale(loss).backward()

    if (i + 1) % ACCUM_STEPS == 0:
        scaler.step(optimizer)
        scaler.update()
        optimizer.zero_grad()
```

Effektiv: 32 × 8 = 256.

### Schritt 4: Cosine-Schedule-with-Warmup

```python
from torch.optim.lr_scheduler import CosineAnnealingLR
from torch.optim.lr_scheduler import LinearLR, SequentialLR

warmup_steps = 1000
total_steps = 50_000

scheduler = SequentialLR(
    optimizer,
    schedulers=[
        LinearLR(optimizer, start_factor=0.01, total_iters=warmup_steps),
        CosineAnnealingLR(optimizer, T_max=total_steps - warmup_steps),
    ],
    milestones=[warmup_steps],
)
```

**Standard 2026** für LLM-Pretraining + Finetuning. Warmup verhindert Instabilität in den ersten Schritten, Cosine-Schedule kühlt smooth ab.

### Schritt 5: Gradient-Clipping

```python
torch.nn.utils.clip_grad_norm_(modell.parameters(), max_norm=1.0)
```

Clip auf Norm ≤ 1.0 (LLMs) oder 5.0 (CNNs) verhindert Explosion bei langen Sequenzen.

### Schritt 6: PyTorch Lightning vs. nackter PyTorch

**Vanilla PyTorch**:

- Maximaler Control
- Mehr Boilerplate
- Standard für Research-Code

**PyTorch Lightning** (2.6.1, Stand Januar 2026):

- Standard-Pattern out-of-the-box (Mixed Precision, DDP, Logging)
- Weniger Code, weniger Bugs durch falsche Pattern-Reihenfolge
- Ein bisschen Magie (für Anfänger:innen manchmal verwirrend)
- Performance-Overhead: vernachlässigbar (~ 0.06s/Epoche)

**Faustregel 2026**:

- Erste Schritte / Prototyp → Vanilla PyTorch (verstehen, was passiert)
- Production-Trainings, Multi-GPU, Standard-Pattern → Lightning
- LLM-Pretraining → Vanilla + DeepSpeed/FSDP, oder TorchTitan (PyTorch-natives Pretraining-Framework, 2025)

### Schritt 7: MLflow 3 statt W&B

**Weights & Biases** (W&B) ist beliebt, aber:

- Hosting primär in USA → DSGVO-Drittland-Transfer (Art. 44 + SCC + TIA)
- Bei sensiblen Trainings-Logs problematisch

**MLflow 3.11** (März 2026):

- Open-Source (Apache 2.0)
- Self-hosted on EU-Server (lokal, On-Prem, OVH/STACKIT/IONOS)
- Native OpenTelemetry-GenAI-Trace-Export (2026 Standard)
- Pickle-free Serialisierung mit `torch.export` (Sicherheit)

**Setup** (Compose-File in [`infrastruktur/observability/`](../../../infrastruktur/observability/)):

```yaml
services:
  mlflow:
    image: ghcr.io/mlflow/mlflow:v3.11.1
    ports:
      - "5000:5000"
    volumes:
      - mlflow-data:/mlflow
    environment:
      - MLFLOW_BACKEND_STORE_URI=sqlite:////mlflow/mlflow.db
```

**Code-Pattern**:

```python
import mlflow

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("kreditrisiko-mlp")

with mlflow.start_run():
    mlflow.log_params({
        "lr": 1e-3,
        "batch_size": 64,
        "epochs": 20,
        "optimizer": "AdamW",
        "scheduler": "Cosine+Warmup",
        "seed": SEED,
    })
    for epoch in range(20):
        # ... training
        mlflow.log_metric("train_loss", train_loss, step=epoch)
        mlflow.log_metric("val_f1", val_f1, step=epoch)
    mlflow.pytorch.log_model(modell, "modell")
```

### Schritt 8: Production-Tracking-Stack-Wahl 2026

| Tool | Hosting | Wann |
|---|---|---|
| **MLflow 3** | self-hosted (Docker) | Standard für DACH-On-Prem |
| **Aim** | self-hosted | leichtgewichtige Alternative |
| **Comet** | Cloud (EU-Region möglich) | wenn man kein Self-Hosting will |
| **W&B** | Cloud (US primär) | nur mit AVV/SCC/TIA, ggf. Forschung |
| **Neptune** | Cloud (DE-Provider seit 2025) | DACH-Cloud-Option |

## Code-Walkthrough — vollständiger Training-Loop

```python
import torch
import torch.nn as nn
from torch.amp import autocast, GradScaler
from torch.optim.lr_scheduler import CosineAnnealingLR, LinearLR, SequentialLR
import mlflow

# Setup
device = "cuda" if torch.cuda.is_available() else "cpu"
modell = TabularMLP(eingang_dim=10, num_classes=2).to(device)

# Loss + Optimizer + Scheduler
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.AdamW(modell.parameters(), lr=1e-3, weight_decay=0.01)

total_steps = len(loader) * 20  # 20 Epochs
scheduler = SequentialLR(
    optimizer,
    schedulers=[
        LinearLR(optimizer, start_factor=0.01, total_iters=500),
        CosineAnnealingLR(optimizer, T_max=total_steps - 500),
    ],
    milestones=[500],
)
scaler = GradScaler("cuda")

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("dl-grundlagen")
with mlflow.start_run():
    mlflow.log_params({
        "lr": 1e-3, "weight_decay": 0.01, "batch_size": 64, "seed": 42,
        "optimizer": "AdamW", "scheduler": "Cosine+Warmup", "amp": "bf16",
    })
    for epoch in range(20):
        modell.train()
        for batch in loader:
            x, y = batch.x.to(device), batch.y.to(device)
            optimizer.zero_grad()
            with autocast("cuda", dtype=torch.bfloat16):
                loss = loss_fn(modell(x), y)
            scaler.scale(loss).backward()
            scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(modell.parameters(), 1.0)
            scaler.step(optimizer)
            scaler.update()
            scheduler.step()

        mlflow.log_metric("train_loss", loss.item(), step=epoch)
```

## Hands-on

→ [`code/01_pytorch_dl_kalkulator.py`](../code/01_pytorch_dl_kalkulator.py)

Im Notebook gibt es einen **Tracking-Tab**, der für drei Hosting-Szenarien (DACH-On-Prem, Hybrid, Cloud) die richtige Tracking-Wahl + Compliance-Hinweis ausgibt.

## Selbstcheck

- [ ] Was bewirkt `optimizer.zero_grad()` in einer Gradient-Accumulation-Schleife? (Antwort: nur am Boundary nullsetzen, sonst nicht)
- [ ] Warum bf16 statt fp16?
- [ ] Welcher Scheduler ist 2026 LLM-Standard? (Cosine-Schedule-with-Warmup)
- [ ] Warum MLflow statt W&B in DACH? (DSGVO-Drittland-Transfer)

## Compliance-Anker

- **AI-Act Art. 11** (Tech-Doku): Trainings-Hyperparameter, Random-Seed, Modell-Hash, Daten-Hash, Loss-Verlauf — alles loggen, archivieren.
- **DSGVO Art. 44** (Drittland-Transfer): W&B-/HuggingFace-Tracking mit Personenbezug → SCC + TIA. Lokal MLflow ist die einfachste Lösung.

→ [`compliance.md`](../compliance.md)

## Quellen

- PyTorch 2.7 Release Notes — <https://pytorch.org/blog/pytorch-2-7/>
- MLflow 3.11.1 Release — <https://mlflow.org/releases/>
- TorchTitan Paper — <https://arxiv.org/abs/2410.06511>
- Loshchilov & Hutter (2017): „SGDR: Stochastic Gradient Descent with Warm Restarts" (Cosine-Schedule) — <https://arxiv.org/abs/1608.03983>

## Weiterführend

- Phase 10 (LLM von Null): Pretraining-Loop mit DDP/FSDP
- Phase 12 (Finetuning): LoRA + AdamW + Cosine-Schedule
- Phase 17 (Production): Phoenix + Langfuse für Inference-Tracking
