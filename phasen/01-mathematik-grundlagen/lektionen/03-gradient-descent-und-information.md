---
id: 01.03
titel: Gradient Descent von Hand und Information-Theory — wie Modelle lernen
phase: 01-mathematik-grundlagen
dauer_minuten: 90
schwierigkeit: leicht
stand: 2026-04-29
voraussetzungen: [01.02]
lernziele:
  - Gradient Descent geometrisch und algebraisch verstehen
  - Lernrate (η) als das wichtigste Hyperparameter erkennen
  - Adam, AdamW, Lion einordnen — und warum AdamW 2026 Standard ist
  - Information-Theory-Grundbegriffe (Entropie, Information) als Brücke zu LLMs
compliance_anker:
  - reproducible-training
ai_act_artikel:
  - art-11
---

## Worum es geht

> Stop calling backprop "magic". — Backpropagation ist Kettenregel + Vektor-Buchhaltung. Das eigentliche Lernen passiert durch **Gradient Descent**: man steht auf einer Loss-Landschaft und geht in Richtung steilstem Abstieg, bis man im (lokalen) Tal ankommt.

Diese Lektion macht Gradient Descent ohne Zauberei: ein 2D-Toy, von Hand durchgerechnet. Plus Information-Theory als Brücke zu Lektion 01.02.

## Voraussetzungen

- Lektion 01.02 (Cross-Entropy als Loss-Funktion)

## Konzept

### Schritt 1: Loss-Landschaft als Berg/Tal-System

Stell dir vor, das Modell hat **2 Parameter** `w₁, w₂`. Für jede Kombination gibt es einen Loss-Wert. Trägt man Loss als Höhe auf, ergibt sich eine **Loss-Landschaft**:

```text
        Loss
         ▲
         │      ╱╲
         │     ╱  ╲     ← Hochpunkt (schlechte Parameter)
         │    ╱    ╲
         │   ╱      ╲
         │  ╱        ╲___
         │ ╱          ╲   ╲___      ← Talsohle (gute Parameter)
         └────────────────────► (w₁, w₂)
```

**Ziel**: niedrigster Punkt finden — der globale Minimum.

**Realität**: bei Milliarden Parametern ist die Landschaft hochdimensional und nicht mehr visualisierbar. Aber das **Prinzip** bleibt: Gradient (steilste Abstiegs-Richtung) folgen.

### Schritt 2: Gradient — die „Pfeil-aus-jedem-Punkt"-Funktion

Der **Gradient** `∇L(w)` ist ein Vektor der gleichen Dimension wie `w`. Jede Komponente ist die **partielle Ableitung** des Loss nach diesem Parameter:

```text
∇L = [ ∂L/∂w₁ ,  ∂L/∂w₂ , ... ]
```

Geometrisch: `∇L` zeigt in die Richtung des **steilsten Anstiegs**. Wir wollen abwärts → wir gehen in Richtung **`-∇L`**.

### Schritt 3: Update-Regel (Vanilla SGD)

```text
w_neu = w_alt - η × ∇L(w_alt)
```

Mit:

- `η` (eta) = **Lernrate**, der wichtigste Hyperparameter
- `∇L` = Gradient des Loss bezüglich der Parameter

**Lernrate-Drama**:

- η zu klein: Training braucht ewig (bei LLMs: Wochen statt Tagen)
- η zu groß: Modell „springt" über das Minimum, divergiert oder oszilliert
- η = 0: kein Lernen (passiert manchmal versehentlich, wenn Adam Numeric instabil wird)

**Standard 2026** für LLMs: `η = 1e-4` bis `1e-5` mit **Cosine-Schedule** + **Warmup**. Siehe Phase 03 + Phase 10.

### Schritt 4: Stochastic Gradient Descent (SGD) — der Mini-Batch-Trick

Bei Milliarden Trainings-Beispielen ist es zu teuer, den **vollen** Gradienten über alle Daten zu berechnen. Lösung: **Stochastic** Gradient Descent — wir nehmen einen kleinen **Mini-Batch** (z.B. 32, 256 oder 4096 Beispiele), berechnen den Gradienten darauf, machen ein Update, und nehmen den nächsten Batch.

**Trade-off**:

- Kleiner Batch (32): rauschig, aber günstig pro Update
- Großer Batch (4096): glatter, aber teuer
- Sehr großer Batch (1M+, wie bei LLM-Pretraining): braucht Distributed-Training (Phase 10)

### Schritt 5: Adam, AdamW, Lion — Optimizer-Familie 2026

Vanilla SGD reicht nicht für LLMs. Moderne Optimizer halten Statistiken über Gradient-Verlauf:

- **Adam** (Kingma & Ba, 2014): Tracking von 1. Moment (Mittelwert) und 2. Moment (Varianz) pro Parameter. Adaptive Lernrate pro Parameter.
- **AdamW** (Loshchilov & Hutter, 2017): Adam + entkoppeltes Weight-Decay. **Standard 2026 für LLM-Pretraining**.
- **Lion** (Chen et al., 2023): vereinfachte Variante, nur ±1-Schritte; manchmal speicher-effizienter, weniger verbreitet als AdamW.
- **Muon** (Jordan et al., 2024): jüngste Entwicklung, in einigen Pretraining-Runs leicht überlegen, noch nicht durchgesetzt.

> **Faustregel 2026**: AdamW ist die sichere Wahl. Lion und Muon nur wenn man weiß warum.

### Schritt 6: Information-Theory — der Bezug zu Lektion 01.02

**Entropie** misst „durchschnittlichen Überraschungswert" einer Verteilung:

```text
H(p) = -Σ p(x) × log p(x)
```

**Information** eines Ereignisses: `I(x) = -log p(x)`. Seltenes Ereignis = hoher Informations-Gehalt.

**Verbindung zu Cross-Entropy** (Lektion 01.02):

```text
Cross-Entropy(p, q) = H(p) + KL(p || q)
```

Beim LLM-Training ist `H(p)` (Entropie der wahren Verteilung) konstant — Cross-Entropy minimieren = KL minimieren = Modell-Verteilung an wahre Verteilung annähern. **Das ist alles, was beim Pretraining passiert.**

## Code-Walkthrough — Gradient Descent in 10 Zeilen

```python
import numpy as np

def loss(w):
    """Toy-Loss: f(w) = (w[0] - 3)² + (w[1] + 1)² — Minimum bei (3, -1)."""
    return (w[0] - 3) ** 2 + (w[1] + 1) ** 2

def gradient(w):
    return np.array([2 * (w[0] - 3), 2 * (w[1] + 1)])

# Start, Lernrate
w = np.array([0.0, 0.0])
eta = 0.1

for schritt in range(50):
    g = gradient(w)
    w = w - eta * g
    if schritt % 10 == 0:
        print(f"Schritt {schritt:3d}: w = {w}, loss = {loss(w):.6f}")
```

Output (gekürzt):

```text
Schritt   0: w = [0.6 -0.2], loss = 6.40
Schritt  10: w = [2.679 -0.893], loss = 0.114
Schritt  40: w = [2.999 -1.000], loss = 0.000
```

In PyTorch (Phase 03 Vorgriff):

```python
import torch

w = torch.tensor([0.0, 0.0], requires_grad=True)
optimizer = torch.optim.AdamW([w], lr=0.1)

for schritt in range(50):
    optimizer.zero_grad()
    loss = (w[0] - 3) ** 2 + (w[1] + 1) ** 2
    loss.backward()       # Backprop
    optimizer.step()      # AdamW-Update
```

## Hands-on

→ [`code/01_embedding_explorer.py`](../code/01_embedding_explorer.py)

Im Notebook gibt es einen **Gradient-Descent-Tab**, der die Trajektorie eines 2D-Optimizers zeigt: Vanilla SGD vs. AdamW. Mit zu großer Lernrate sieht man explizit das Oszillieren.

## Selbstcheck

- [ ] Was passiert mit `η = 1.0` auf der Toy-Funktion oben? (Lösung: divergiert / oszilliert)
- [ ] Welche zwei Statistiken trackt Adam pro Parameter? (1. Moment, 2. Moment)
- [ ] Warum ist Cross-Entropy ≠ KL-Divergenz, obwohl beide „Verteilungs-Distanz" messen? (Wegen Entropie-Term `H(p)`)
- [ ] Welcher Optimizer ist 2026 LLM-Pretraining-Standard? (AdamW)

## Compliance-Anker

- **AI-Act Art. 11** (Tech-Doku): Hochrisiko-Systeme müssen Trainings-Hyperparameter dokumentieren. Für jeden Run: Optimizer, Lernrate, Batch-Size, Random-Seed. Phase 03 + Phase 10 zeigen MLflow-Setup dafür.

→ [`compliance.md`](../compliance.md)

## Quellen

- Kingma & Ba (2014): „Adam: A Method for Stochastic Optimization" — <https://arxiv.org/abs/1412.6980>
- Loshchilov & Hutter (2017/19): „Decoupled Weight Decay Regularization" (AdamW) — <https://arxiv.org/abs/1711.05101>
- Chen et al. (2023): „Symbolic Discovery of Optimization Algorithms" (Lion) — <https://arxiv.org/abs/2302.06675>
- Jordan et al. (2024): Muon — <https://kellerjordan.github.io/posts/muon/>
- Stanford CS231n: „Optimization" Notes — <https://cs231n.github.io/optimization-1/>

## Weiterführend

- Phase 03 (Deep Learning): Backprop = automatisches Gradient-Berechnen
- Phase 10 (LLM von Null): Pretraining-Optimizer-Setup (AdamW, Cosine-Schedule, Warmup)
