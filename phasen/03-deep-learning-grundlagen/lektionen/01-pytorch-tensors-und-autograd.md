---
id: 03.01
titel: PyTorch Tensors, Autograd und nn.Module — die drei Bausteine
phase: 03-deep-learning-grundlagen
dauer_minuten: 90
schwierigkeit: mittel
stand: 2026-04-29
voraussetzungen: [01.03]
lernziele:
  - Tensoren als GPU-fähige NumPy-Arrays verstehen
  - Autograd als automatischen Backpropagation-Motor begreifen
  - nn.Module als Standard-Wrapper für Schichten + Parameter nutzen
  - PyTorch 2.7 (Blackwell-Support) und torch.compile als 2026-Standard einordnen
compliance_anker:
  - reproducible-training
ai_act_artikel:
  - art-11
---

<!-- colab-badge:begin -->
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/s-a-s-k-i-a/ki-engineering-werkstatt/blob/main/dist-notebooks/phasen/03-deep-learning-grundlagen/code/01_pytorch_dl_kalkulator.ipynb)
<!-- colab-badge:end -->

## Worum es geht

> Stop using TensorFlow. — 2026 ist **PyTorch** Industrie-Standard für Forschung **und** Production. PyTorch 2.7 (April 2026, Blackwell B200-Support, CUDA 12.8) plus `torch.compile` für Inference-Speedup ist der Stack, auf dem die meisten DACH-Teams 2026 bauen.

Diese Lektion macht die drei PyTorch-Bausteine konkret: **Tensors** als GPU-fähige Arrays, **Autograd** als „Backprop-für-dich"-Motor, **nn.Module** als Wrapper.

## Voraussetzungen

- Lektion 01.03 (Gradient Descent von Hand)

## Konzept

### Schritt 1: Tensors — NumPy mit GPU

Ein **Tensor** ist eine n-dimensionale Array — wie ein NumPy-Array, aber:

- Kann auf **CUDA** (NVIDIA), **MPS** (Apple Silicon), **ROCm** (AMD) oder **XPU** (Intel) liegen
- Trackt automatisch **Gradient-Information** (siehe Autograd unten)
- Nutzt mit `torch.compile` automatische **Operator-Fusion** für Speedup

```python
import torch

# CPU-Tensor
a = torch.tensor([1.0, 2.0, 3.0])

# GPU-Tensor (CUDA)
b = torch.tensor([1.0, 2.0, 3.0], device="cuda")

# Apple Silicon
c = torch.tensor([1.0, 2.0, 3.0], device="mps")

# Mit Gradient-Tracking
w = torch.randn(10, requires_grad=True)
```

**Standard-2026-Pattern** für Device-Auswahl:

```python
device = (
    "cuda" if torch.cuda.is_available()
    else "mps" if torch.backends.mps.is_available()
    else "cpu"
)
```

### Schritt 2: Autograd — automatische Differenzierung

In Lektion 01.03 hast du Gradienten von Hand berechnet. PyTorch macht das **automatisch**, indem es jede Operation in einem **Computation Graph** trackt:

```python
import torch

w = torch.tensor([0.0, 0.0], requires_grad=True)

# Forward — Operationen werden im Graph aufgezeichnet
loss = (w[0] - 3) ** 2 + (w[1] + 1) ** 2

# Backward — automatisch alle Gradienten ableiten
loss.backward()

print(w.grad)   # tensor([-6., 2.])
```

**Wichtig**: jeder neuer Forward-Pass braucht `optimizer.zero_grad()` davor — sonst akkumulieren sich Gradienten. (Das ist auch der Trick für **Gradient Accumulation** bei großen Batches; siehe Lektion 03.03.)

### Schritt 3: nn.Module — der Schicht-Container

Ein **nn.Module** ist eine Klasse, die Parameter (Tensoren mit `requires_grad`) bündelt und einen `forward()`-Schritt definiert:

```python
import torch
import torch.nn as nn

class MLP(nn.Module):
    def __init__(self, eingang_dim: int, versteckt: int, ausgang_dim: int):
        super().__init__()
        self.l1 = nn.Linear(eingang_dim, versteckt)
        self.l2 = nn.Linear(versteckt, ausgang_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.l1(x)
        x = torch.relu(x)
        return self.l2(x)

modell = MLP(eingang_dim=10, versteckt=64, ausgang_dim=2)
```

**Vorteile**:

- Parameter werden automatisch gefunden (`modell.parameters()`)
- Gerätewechsel mit `modell.to("cuda")`
- Speichern/Laden mit `torch.save(modell.state_dict(), ...)`

### Schritt 4: PyTorch 2.7 + torch.compile

PyTorch 2.7 (April 2026) bringt:

- **Blackwell B200-Support** out-of-the-box
- **CUDA 12.8** Wheels offiziell
- **Triton 3.3** integriert (für `torch.compile`)
- **FlexAttention** mit PageAttention (Lektion 07.05) auf x86 CPU
- **torch.export**-Format als reproduzierbare Modell-Serialisierung

**`torch.compile` als 2026-Standard** für Inference und Training:

```python
modell_kompiliert = torch.compile(modell, mode="reduce-overhead")
# oder mit max performance:
modell_kompiliert = torch.compile(modell, mode="max-autotune")
```

`torch.compile` macht JIT-Kompilierung mit Operator-Fusion und Triton-Kernels. Speedup bei Inference: typisch 1.5-3× für LLMs auf H100.

### Schritt 5: Mixed Precision (BF16/FP16)

LLM-Training in 2026 läuft fast immer in **bf16** (BFloat16):

```python
from torch.amp import autocast, GradScaler

scaler = GradScaler("cuda")
for x, y in loader:
    optimizer.zero_grad()
    with autocast("cuda", dtype=torch.bfloat16):
        loss = loss_fn(modell(x), y)
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
```

**Warum bf16 statt fp16?** Gleicher Exponent-Range wie fp32, weniger numerische Probleme. Standard auf H100/H200/B200.

## Code-Walkthrough

```python
import torch
import torch.nn as nn

# Setup
device = "cuda" if torch.cuda.is_available() else "cpu"

# Modell — 2-Layer MLP für binäre Klassifikation
class Klassifikator(nn.Module):
    def __init__(self, eingang_dim: int):
        super().__init__()
        self.netz = nn.Sequential(
            nn.Linear(eingang_dim, 64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, 2),
        )

    def forward(self, x):
        return self.netz(x)

modell = Klassifikator(eingang_dim=10).to(device)

# Loss + Optimizer
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.AdamW(modell.parameters(), lr=1e-3)

# Compile (PyTorch 2.6+)
modell = torch.compile(modell)

# Training-Loop (vereinfacht)
modell.train()
for epoch in range(5):
    for x, y in loader:
        x, y = x.to(device), y.to(device)
        optimizer.zero_grad()
        logits = modell(x)
        loss = loss_fn(logits, y)
        loss.backward()
        optimizer.step()
```

## Hands-on

→ [`code/01_pytorch_dl_kalkulator.py`](../code/01_pytorch_dl_kalkulator.py)

Marimo-Notebook: profiliert Use-Cases nach Daten-Typ (tabular / Bild / Sequenz / Audio) und gibt Empfehlung für Modell-Architektur, Optimizer, Hardware (GPU-VRAM), Tracking-Tool (MLflow vs. W&B).

## Selbstcheck

- [ ] Welche drei Methoden gibt PyTorch dir für Device-Wahl? (cuda / mps / cpu, plus xpu/rocm)
- [ ] Was macht `optimizer.zero_grad()`?
- [ ] Wann nutzt du `torch.compile(...)`? (Antwort: in Production-Inference-Pfaden + ggf. Training)
- [ ] Wann bf16 statt fp16?

## Compliance-Anker

- **AI-Act Art. 11** (Tech-Doku): Random-Seeds setzen, Hyperparameter committen — Phase 03 ist die Stelle, wo du diese Disziplin lernst.
- **Reproduzierbarkeit**: `torch.manual_seed(42)`, `torch.use_deterministic_algorithms(True)` für deterministische Trainings-Runs (mit Performance-Trade-off).

→ [`compliance.md`](../compliance.md)

## Quellen

- PyTorch 2.7 Release Notes — <https://pytorch.org/blog/pytorch-2-7/>
- PyTorch Autograd Mechanics — <https://pytorch.org/docs/stable/notes/autograd.html>
- torch.compile Tutorial — <https://pytorch.org/tutorials/intermediate/torch_compile_tutorial.html>
- Sebastian Raschka: „What does torch.compile actually help with?" — <https://sebastianraschka.com/faq/docs/torch-compile-llm-workloads.html>

## Weiterführend

- Lektion 03.02 (MLP/CNN-Bausteine)
- Lektion 03.03 (Training-Loop-Hygiene + lokales Tracking)
