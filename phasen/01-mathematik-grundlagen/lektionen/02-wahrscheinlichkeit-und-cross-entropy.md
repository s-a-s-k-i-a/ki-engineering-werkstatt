---
id: 01.02
titel: Wahrscheinlichkeit, Cross-Entropy und KL-Divergenz — was LLMs minimieren
phase: 01-mathematik-grundlagen
dauer_minuten: 90
schwierigkeit: leicht
stand: 2026-04-29
voraussetzungen: [01.01]
lernziele:
  - Wahrscheinlichkeitsverteilungen über Tokens als LLM-Output verstehen
  - Cross-Entropy-Loss intuitiv begreifen — die Universal-Loss-Funktion für LLMs
  - KL-Divergenz erkennen, wenn sie auftaucht (DPO, GRPO, Knowledge-Distillation)
  - Perplexität als „wie verwirrt ist das Modell?" interpretieren
compliance_anker:
  - eval-metrik-dokumentation
ai_act_artikel:
  - art-15
---

## Worum es geht

> Stop treating loss as magic. — Wenn ein LLM trainiert wird, **minimiert es Cross-Entropy**. Wenn ein RLHF-/DPO-/GRPO-Algorithmus läuft, **steht KL-Divergenz im Loss**. Wenn ein Eval-Bericht „Perplexität 12.3" zeigt, **ist das Cross-Entropy in einer anderen Form**.

Diese drei Konzepte — Cross-Entropy, KL-Divergenz, Perplexität — sind **eine** Idee in drei Verkleidungen. Wer sie versteht, versteht warum ein LLM was tut.

## Voraussetzungen

- Lektion 01.01 (Vektoren)
- Schul-Wahrscheinlichkeit (P(A) zwischen 0 und 1, Summe = 1)

## Konzept

### Schritt 1: Tokens sind Ziehungen aus einer Verteilung

Ein LLM sagt nie „das nächste Token ist X". Es sagt „über alle 100 000+ möglichen Tokens habe ich folgende Wahrscheinlichkeitsverteilung":

```text
Eingabe: "Der Hund ist im"
Output-Verteilung über 100k Tokens:

  "Garten"  → 0.31
  "Park"    → 0.18
  "Haus"    → 0.12
  "Wald"    → 0.09
  ... (99 996 weitere mit kleineren Werten)
```

**Wichtig**: alle Wahrscheinlichkeiten summieren zu 1.0 — das macht die **Softmax**-Funktion am Ende des Modells. (Mehr dazu in Phase 03.)

### Schritt 2: Cross-Entropy — der „Trainings-Schmerz"

Während Training kennt das Modell für jedes Beispiel das **wahre nächste Token** (z.B. „Garten"). Die Trainings-Aufgabe lautet:

> Erhöhe die Wahrscheinlichkeit, die du dem wahren Token zugewiesen hast.

Mathematisch ausgedrückt mit **Cross-Entropy**:

```text
CE(p_wahr, q_modell) = -Σ p_wahr(x) × log(q_modell(x))
```

Bei One-Hot-wahrer-Verteilung (d.h. genau ein Token ist „richtig"):

```text
CE = -log(q_modell(richtiges Token))
```

**Intuition**:

- Modell sagt 0.99 für das richtige Token → `-log(0.99) ≈ 0.01` → wenig Schmerz
- Modell sagt 0.01 für das richtige Token → `-log(0.01) ≈ 4.6` → viel Schmerz

Beim Training versucht der Optimizer, diesen Schmerz zu minimieren. Über Milliarden Token = Sprache lernen.

### Schritt 3: KL-Divergenz — „wie sehr unterscheiden sich zwei Verteilungen?"

KL (Kullback-Leibler-Divergenz) misst, wie weit eine Verteilung `q` von einer Referenz `p` abweicht:

```text
KL(p || q) = Σ p(x) × log(p(x) / q(x))
            = Cross-Entropy(p, q) - Entropie(p)
```

**Wertebereich**: 0 bis ∞.

- **0** = identische Verteilungen
- **groß** = sehr unterschiedlich

**Asymmetrisch**: `KL(p || q) ≠ KL(q || p)`. Das ist wichtig — in DPO/GRPO wird gezielt `KL(neues Modell || Referenz-Modell)` gerechnet, nicht umgekehrt.

**Wo KL-Divergenz auftaucht**:

- **DPO/GRPO** (Phase 16): KL-Term im Loss verhindert, dass das Modell zu weit vom SFT-Modell abdriftet
- **Knowledge-Distillation** (Phase 12): Schüler-Modell lernt Verteilung des Lehrer-Modells via KL
- **VAE / Diffusion** (Phase 08): KL als Regularisierungsterm
- **Speculative Decoding**: KL zwischen Draft- und Target-Modell entscheidet Acceptance

### Schritt 4: Perplexität — Cross-Entropy mit Lipgloss

Perplexität ist eine **monotone Transformation** von Cross-Entropy:

```text
Perplexität = exp(durchschnittliche Cross-Entropy)
```

**Intuition**: „Wie viele Tokens hätte das Modell im Durchschnitt als gleich-wahrscheinliche Optionen erwogen?"

- **Perplexität 1.0**: perfekte Vorhersage (in Praxis nie erreichbar)
- **Perplexität 10**: Modell ist „verwirrt" zwischen ~10 plausiblen Optionen
- **Perplexität 100**: schwaches Modell oder schwierige Domäne (z.B. Lyrik)

**Typische Werte 2026** (Stand 04/2026, deutsche Wikipedia-Test-Set):

| Modell | Perplexität (DE Wikipedia) |
|---|---|
| GPT-2 (2019) | ~ 30-40 |
| Llama 3.3 70B | ~ 6-8 |
| Mistral Large 3 | ~ 5-7 |
| GPT-5.5 / Claude Opus 4.7 | nicht öffentlich publiziert |

> **Achtung**: Perplexität ist **nur intra-Modell vergleichbar**. Zwei Modelle mit unterschiedlichem Tokenizer haben nicht-vergleichbare Perplexitäten — siehe Phase 05 zur Tokenizer-Effizienz.

## Code-Walkthrough

```python
import numpy as np

def cross_entropy(p_wahr: np.ndarray, q_modell: np.ndarray) -> float:
    """Standard-Cross-Entropy. p, q als Wahrscheinlichkeitsverteilungen."""
    eps = 1e-12  # gegen log(0)
    return float(-np.sum(p_wahr * np.log(q_modell + eps)))

def kl_divergenz(p: np.ndarray, q: np.ndarray) -> float:
    """KL(p || q)."""
    eps = 1e-12
    return float(np.sum(p * (np.log(p + eps) - np.log(q + eps))))

def perplexitaet(durchschnitt_ce: float) -> float:
    return float(np.exp(durchschnitt_ce))


# Beispiel: Modell sagt "Garten" mit 0.31 voraus, das richtige Token ist "Garten"
p_wahr = np.array([1.0, 0.0, 0.0, 0.0])  # One-Hot
q_modell = np.array([0.31, 0.18, 0.12, 0.39])

print(f"CE = {cross_entropy(p_wahr, q_modell):.3f}")    # ~1.17
print(f"PPL = {perplexitaet(1.17):.2f}")                 # ~3.2
```

In PyTorch (Phase 03 Vorgriff):

```python
import torch
import torch.nn.functional as F

logits = torch.tensor([[2.1, 1.5, 1.0, 2.2]])    # vor Softmax!
zielindex = torch.tensor([3])                       # "richtiges" Token an Index 3

# F.cross_entropy macht intern Log-Softmax + NLL-Loss in einem Schritt (numerisch stabil)
loss = F.cross_entropy(logits, zielindex)
print(loss.item())   # ≈ 1.17
```

## Hands-on

→ [`code/01_embedding_explorer.py`](../code/01_embedding_explorer.py)

Im Hands-on-Notebook gibt es einen **Cross-Entropy-Demo-Tab**, der zeigt: gleicher Wahrheits-Token, drei verschiedene Modell-Verteilungen, drei sehr unterschiedliche Loss-Werte. Plus Perplexitäts-Berechnung.

## Selbstcheck

- [ ] Wenn das Modell für das richtige Token Wahrscheinlichkeit 0.5 vorhersagt — wie hoch ist die Cross-Entropy? (Lösung: `-log(0.5) ≈ 0.693`)
- [ ] Warum hat KL-Divergenz **zwei** Argumente, Cross-Entropy aber nur eins „richtig"-Verteilung als Hauptbezug?
- [ ] Wo taucht KL-Divergenz im DPO-Loss auf? (Antwort siehe Phase 16)
- [ ] Welche Perplexität entspricht einem Modell, das immer eine Gleichverteilung über 10 Tokens ausgibt? (Lösung: 10)

## Compliance-Anker

- **AI-Act Art. 15** (Accuracy / Robustness): Hochrisiko-Systeme müssen Eval-Metriken dokumentieren — Perplexität ist eine Standard-Metrik für LLM-Komponenten, aber keine Garantie für Korrektheit (siehe Phase 16/18).

→ [`compliance.md`](../compliance.md)

## Quellen

- Shannon (1948): „A Mathematical Theory of Communication" — <https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf>
- Kullback & Leibler (1951): „On Information and Sufficiency" — <https://www.jstor.org/stable/2236703>
- PyTorch Cross-Entropy Loss — <https://pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html>
- Stanford CS224N: „Word Vectors" Vorlesung — <https://web.stanford.edu/class/cs224n/>

## Weiterführend

- Phase 03 (Deep Learning): wie Backprop CE-Loss minimiert
- Phase 12 (Finetuning): Knowledge-Distillation mit KL
- Phase 16 (Reasoning): DPO/GRPO mit KL-Term
- Phase 18 (Ethik): warum niedrige Perplexität ≠ ethisch korrekt
