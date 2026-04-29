---
id: 1
titel: Mathematik für KI — Lineare Algebra, Wahrscheinlichkeit, Information
dauer_stunden: 6
schwierigkeit: leicht
stand: 2026-04-29
lernziele:
  - Vektor-/Matrizen-Operationen als Embedding-Ähnlichkeit interpretieren
  - Cross-Entropy, KL-Divergenz und Perplexität verstehen
  - Gradient Descent von Hand auf einem 2D-Toy nachvollziehen
  - Information-Theory als Brücke zu LLMs erkennen (Perplexität = Modell-Verwirrung)
  - AdamW als 2026-Pretraining-Optimizer einordnen
---

# Phase 01 · Mathematik für KI

> **Stop fearing math.** — Du brauchst genug Math, um zu verstehen, was passiert, wenn dein LLM „verwirrt" ist. Visuelle Intuition first, Beweise nur wo unverzichtbar. Beispiele konsequent auf deutschen Wörtern.

**Status**: ✅ vollständig ausgearbeitet · **Dauer**: ~ 6 h · **Schwierigkeit**: leicht (Schul-Mathematik reicht)

## 🎯 Was du in diesem Modul lernst

- **Vektoren** als Bedeutungs-Richtungen (Embeddings)
- **Kosinus-Ähnlichkeit** für RAG-Retrieval
- **Cross-Entropy** als universeller LLM-Loss
- **KL-Divergenz** in DPO/GRPO/Distillation
- **Perplexität** als „Modell-Verwirrung"
- **Gradient Descent** + AdamW (2026-Standard)
- **Information-Theory**-Grundlagen

## 📚 Inhalts-Übersicht

| Lektion | Titel | Datei |
|---|---|---|
| 01.01 | Vektoren als Bedeutungs-Richtungen — Embeddings & Kosinus | [`lektionen/01-vektoren-und-embeddings.md`](lektionen/01-vektoren-und-embeddings.md) ✅ |
| 01.02 | Wahrscheinlichkeit, Cross-Entropy, KL-Divergenz, Perplexität | [`lektionen/02-wahrscheinlichkeit-und-cross-entropy.md`](lektionen/02-wahrscheinlichkeit-und-cross-entropy.md) ✅ |
| 01.03 | Gradient Descent von Hand & Information-Theory | [`lektionen/03-gradient-descent-und-information.md`](lektionen/03-gradient-descent-und-information.md) ✅ |

## 💻 Hands-on-Projekt

**Mathe-Werkstatt-Notebook**: drei interaktive Demos in einem Marimo-Notebook — Embedding-Nachbarn auf 30 deutschen Wörtern, Cross-Entropy für drei Modell-Verteilungen, Gradient-Descent-Trajektorie für drei Lernraten.

```bash
uv run marimo edit phasen/01-mathematik-grundlagen/code/01_embedding_explorer.py
```

## 🧱 Faustregeln 2026

| Frage | Antwort |
|---|---|
| Welche Embedding-Metrik? | Kosinus (oder Skalarprodukt, falls L2-normalisiert) |
| Welcher LLM-Loss? | Cross-Entropy (immer) |
| Welcher Optimizer? | AdamW (Pretraining + Finetuning) |
| Lernrate-Größenordnung? | `1e-4` bis `1e-5` (LLMs), `1e-3` (kleinere Modelle) |
| Perplexität vergleichbar? | **Nur intra-Modell** (Tokenizer-Bias) |

## ⚖️ DACH-Compliance-Anker

→ [`compliance.md`](compliance.md): Datasets-Lizenzen (10kGNAD CC BY-NC-SA), AI-Act Art. 10 (Daten-Governance), AI-Act Art. 11 (Reproduzierbare Trainings-Hyperparameter), DSGVO Art. 5 Abs. 1 lit. c (Datenminimierung in Embedding-Korpora).

## 🔄 Wartung

Stand: 29.04.2026 · Reviewer: Saskia Teichmann ([@s-a-s-k-i-a](https://github.com/s-a-s-k-i-a)) · Nächster Review: 10/2026 (Optimizer-Landschaft 2026 noch in Bewegung — Muon, Sophia).
