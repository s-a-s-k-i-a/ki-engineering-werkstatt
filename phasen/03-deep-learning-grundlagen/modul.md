---
id: 3
titel: Deep Learning Grundlagen — PyTorch 2.7, Autograd, MLPs/CNNs, MLflow
dauer_stunden: 6
schwierigkeit: mittel
stand: 2026-04-29
lernziele:
  - PyTorch-Tensoren, Autograd, nn.Module verstehen
  - MLP- und CNN-Bausteine bauen (Linear, Conv, ResNet-Block)
  - Training-Loop-Hygiene 2026 (BF16, Grad-Accum, Cosine+Warmup)
  - PyTorch Lightning vs. Vanilla PyTorch einordnen
  - MLflow 3 lokal als DSGVO-konformen Tracking-Stack einsetzen
---

# Phase 03 · Deep Learning Grundlagen

> **Stop using TensorFlow.** — 2026 ist PyTorch Industrie-Standard. PyTorch 2.7 (Blackwell B200-Support, April 2026) plus MLflow 3.11 als DACH-konformer Tracking-Stack. Lightning 2.6.1 für Standard-Trainings, Vanilla für LLM-Pretraining.

**Status**: ✅ vollständig ausgearbeitet · **Dauer**: ~ 6 h · **Schwierigkeit**: mittel

## 🎯 Was du in diesem Modul lernst

- **PyTorch 2.7-Grundlagen**: Tensors, Autograd, nn.Module, torch.compile
- **Architektur-Bausteine**: Linear, GELU, BatchNorm/RMSNorm, Conv2d, ResNet-Block
- **Training-Loop-Hygiene**: BF16, Gradient Accumulation, Cosine-Schedule mit Warmup
- **Lightning vs. Vanilla PyTorch**: Wann was
- **MLflow 3 lokal**: DACH-konformes Tracking statt W&B

## 📚 Inhalts-Übersicht

| Lektion | Titel | Datei |
|---|---|---|
| 03.01 | PyTorch Tensors, Autograd, nn.Module | [`lektionen/01-pytorch-tensors-und-autograd.md`](lektionen/01-pytorch-tensors-und-autograd.md) ✅ |
| 03.02 | MLP- und CNN-Bausteine, Aktivierungen, Norm-Schichten | [`lektionen/02-mlp-und-cnn-bausteine.md`](lektionen/02-mlp-und-cnn-bausteine.md) ✅ |
| 03.03 | Training-Loop-Hygiene + MLflow 3 lokal | [`lektionen/03-training-loop-hygiene-und-tracking.md`](lektionen/03-training-loop-hygiene-und-tracking.md) ✅ |

## 💻 Hands-on-Projekt

**Deep-Learning-Kalkulator**: profiliert ein DL-Vorhaben (Daten-Typ, Größe, Hardware, Hosting, Sensibilität) und empfiehlt Architektur + Optimizer + Hardware + Tracking-Tool + Compliance-Pflichten.

```bash
uv run marimo edit phasen/03-deep-learning-grundlagen/code/01_pytorch_dl_kalkulator.py
```

## 🧱 Faustregeln 2026

| Frage | Antwort |
|---|---|
| Welcher Optimizer? | AdamW (lr=1e-3, weight_decay=0.01) |
| Welcher Scheduler? | Cosine-Schedule mit 500-1000 Warmup-Steps |
| Welche Precision? | BF16 (auf H100/H200/B200) |
| Lightning oder Vanilla? | Lightning für Standard, Vanilla für LLM-Pretraining (TorchTitan) |
| Tracking? | MLflow 3 lokal in DACH; Comet/Neptune für EU-Cloud; W&B nur mit AVV+SCC+TIA |

## ⚖️ DACH-Compliance-Anker

→ [`compliance.md`](compliance.md): AI-Act Art. 11 (Tech-Doku, reproducibility), DSGVO Art. 44 (Drittland-Transfer beim Tracking-Tool), AI-Act Art. 12 (Logging).

## 🔄 Wartung

Stand: 29.04.2026 · Reviewer: Saskia Teichmann ([@s-a-s-k-i-a](https://github.com/s-a-s-k-i-a)) · Nächster Review: 09/2026 (PyTorch 2.8 wird Q3 erwartet, Blackwell-Optimierungen).
