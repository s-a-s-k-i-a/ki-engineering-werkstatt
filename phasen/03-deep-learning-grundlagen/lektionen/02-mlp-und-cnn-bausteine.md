---
id: 03.02
titel: MLP- und CNN-Bausteine — von der linearen Schicht zur ResNet-Architektur
phase: 03-deep-learning-grundlagen
dauer_minuten: 90
schwierigkeit: mittel
stand: 2026-04-29
voraussetzungen: [03.01]
lernziele:
  - MLP-Bausteine: Linear, ReLU/GeLU, Dropout, BatchNorm/LayerNorm
  - CNN-Bausteine: Conv2d, Pool, ResNet-Block
  - Aktivierungs-Funktionen-Familie 2026 (ReLU, GeLU, SiLU/Swish)
  - Wann CNN, wann ViT (Vision Transformer)
compliance_anker:
  - urhebrechtliche-bilder
ai_act_artikel:
  - art-10
---

## Worum es geht

> Stop treating layers as magic. — Eine **Linear-Schicht** ist eine Matrixmultiplikation plus Bias. Eine **Conv-Schicht** ist eine Faltung mit gelernten Filtern. **Activation** ist eine elementweise Funktion. Mehr braucht es nicht, um MLPs und CNNs zu bauen.

Diese Lektion zerlegt die Bausteine ehrlich: was sie mathematisch tun, wann man sie braucht, und ein Standard-MLP- und ein Standard-ResNet-Block in 30 Zeilen PyTorch.

## Voraussetzungen

- Lektion 03.01 (Tensors, Autograd, nn.Module)

## Konzept

### Schritt 1: nn.Linear — die Brot-und-Butter-Schicht

```python
nn.Linear(in_features, out_features)  # y = x @ W.T + b
```

- `W` ∈ ℝ^(out × in), `b` ∈ ℝ^out — gelernt
- 99 % aller Schichten in LLMs sind Linear (in MLPs, Attention, FFN)

**Initialisierung 2026**: PyTorch nutzt per Default Kaiming-Uniform für Linear-Schichten. Bei eigenen Schichten: meist passt das.

### Schritt 2: Aktivierungs-Funktionen

Ohne Nichtlinearität ist ein 100-Layer-Netz mathematisch gleich einer Linear-Schicht. Standard-Funktionen 2026:

| Funktion | Wann |
|---|---|
| **ReLU** `max(0, x)` | klassisch, schnell, „dying neurons" |
| **GeLU** `x · Φ(x)` | Standard in Transformers (BERT, GPT) |
| **SiLU/Swish** `x · sigmoid(x)` | Llama-Familie, smooth |
| **SwiGLU** | LLM-FFN-Standard 2026 (Llama, Mistral, Qwen) |

**Faustregel**: GeLU/SiLU für Transformer-FFN, ReLU für klassische CNN.

### Schritt 3: Dropout — Regularisierung

```python
nn.Dropout(p=0.1)
```

Setzt zufällig `p` Anteil der Aktivierungen auf 0 — **nur während Training**. Im Eval-Modus (`modell.eval()`) ist Dropout aus.

**Werte 2026**:

- LLMs: oft `p=0.0` (Daten-Menge reicht als Regularisierung)
- CNN-Klassifikator: `p=0.2-0.5`
- MLP klein: `p=0.2`

### Schritt 4: BatchNorm vs. LayerNorm vs. RMSNorm

```python
nn.BatchNorm2d(channels)   # CNN, normalisiert über Batch + räumlich
nn.LayerNorm(features)     # Transformer, normalisiert über Feature-Dim pro Sample
```

**RMSNorm** (Llama-Familie, 2019/2023) ist eine vereinfachte LayerNorm-Variante ohne Mean-Subtraktion — schneller, leicht besser bei LLMs:

```python
class RMSNorm(nn.Module):
    def __init__(self, dim, eps=1e-6):
        super().__init__()
        self.weight = nn.Parameter(torch.ones(dim))
        self.eps = eps

    def forward(self, x):
        return self.weight * x / torch.sqrt(x.pow(2).mean(-1, keepdim=True) + self.eps)
```

**Faustregel 2026**:

- CNN → BatchNorm
- Transformer → RMSNorm (LLM-Standard) oder LayerNorm
- BatchNorm + sehr kleine Batches (1-4) → schwierig, dann LayerNorm

### Schritt 5: CNN-Bausteine

```python
nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding)
nn.MaxPool2d(kernel_size)
nn.AvgPool2d(kernel_size)
```

**Faustregeln**:

- 3×3 Conv mit padding=1 erhält räumliche Größe
- Pool mit stride=2 halbiert die räumliche Größe und verdoppelt typisch die Channels
- Pre-trained Backbones (ResNet50, ConvNeXt, EfficientNet) sind 2026 fast immer der bessere Start als from-scratch

### Schritt 6: ResNet-Block — der Klassiker

ResNet (He et al., 2015) führte **Skip-Connections** ein, die das Vanishing-Gradient-Problem für tiefe Netze lösen:

```python
class ResNetBlock(nn.Module):
    def __init__(self, channels):
        super().__init__()
        self.conv1 = nn.Conv2d(channels, channels, 3, padding=1)
        self.bn1 = nn.BatchNorm2d(channels)
        self.conv2 = nn.Conv2d(channels, channels, 3, padding=1)
        self.bn2 = nn.BatchNorm2d(channels)

    def forward(self, x):
        residual = x
        x = torch.relu(self.bn1(self.conv1(x)))
        x = self.bn2(self.conv2(x))
        return torch.relu(x + residual)   # ← Skip-Connection
```

**Skip-Connections sind universell** — sie sind in CNNs (ResNet), Transformers (FFN-Block), Mamba (State-Space) zu finden.

### Schritt 7: Wann CNN, wann ViT (Vision Transformer)?

| Bedingung | Empfehlung |
|---|---|
| Wenig Daten (< 10k Bilder) | **CNN** mit Pre-trained Backbone (ResNet50, EfficientNet-B0) |
| Viele Daten (> 100k) | **ViT** oder **ConvNeXt** |
| Edge-Deployment, < 50ms Latenz | **MobileNet-V3** oder **EfficientNet-Lite** |
| Multimodal (Bild + Text) | **CLIP / SigLIP / Qwen-VL** (Phase 04) |

In Phase 04 (Computer Vision) gehen wir tiefer auf VLMs und Pre-trained Backbones ein.

## Code-Walkthrough — MLP für Tabular Data

```python
import torch
import torch.nn as nn

class TabularMLP(nn.Module):
    """Standard-MLP für tabular Klassifikation.

    Architektur: 4 Linear-Schichten, GELU, Dropout, BatchNorm.
    """

    def __init__(self, eingang_dim: int, num_classes: int):
        super().__init__()
        self.netz = nn.Sequential(
            nn.Linear(eingang_dim, 256),
            nn.BatchNorm1d(256),
            nn.GELU(),
            nn.Dropout(0.2),
            nn.Linear(256, 128),
            nn.BatchNorm1d(128),
            nn.GELU(),
            nn.Dropout(0.2),
            nn.Linear(128, 64),
            nn.GELU(),
            nn.Linear(64, num_classes),
        )

    def forward(self, x):
        return self.netz(x)
```

**Anmerkung**: Für tabular Data ist klassisches ML (Phase 02) oft besser. Das hier ist nur, um die Bausteine zu verinnerlichen.

## Hands-on

→ [`code/01_pytorch_dl_kalkulator.py`](../code/01_pytorch_dl_kalkulator.py)

Im Notebook gibt es einen **Architektur-Tab**, der für 5 Daten-Typen (tabular, Bild klein, Bild groß, Sequenz, Audio) die Modell-Empfehlung + Beispiel-Bausteine ausgibt.

## Selbstcheck

- [ ] Was macht `nn.Linear(64, 32)` mathematisch?
- [ ] Welche Aktivierung in einem 2026-LLM-FFN?
- [ ] BatchNorm bei Batch-Size 1 — Problem oder okay?
- [ ] Wann ViT besser als ResNet? Wann umgekehrt?

## Compliance-Anker

- **AI-Act Art. 10** (Daten-Governance): Bei Bild-Trainings-Daten — Urheberrechte beachten. ImageNet ist für **Forschung** lizenziert, nicht zwingend für kommerzielle Modelle. Eigene Bilder + DSGVO Art. 9 (biometrische Daten) → DSFA.

→ [`compliance.md`](../compliance.md)

## Quellen

- He et al. (2015): „Deep Residual Learning for Image Recognition" (ResNet) — <https://arxiv.org/abs/1512.03385>
- Hendrycks & Gimpel (2016): „Gaussian Error Linear Units (GELUs)" — <https://arxiv.org/abs/1606.08415>
- Zhang & Sennrich (2019): „Root Mean Square Layer Normalization" (RMSNorm) — <https://arxiv.org/abs/1910.07467>
- Liu et al. (2022): „A ConvNet for the 2020s" (ConvNeXt) — <https://arxiv.org/abs/2201.03545>

## Weiterführend

- Phase 04 (Computer Vision): VLMs + State-of-the-art-Backbones
- Phase 07 (Transformer): wie diese Bausteine im Transformer-Block kombiniert werden
