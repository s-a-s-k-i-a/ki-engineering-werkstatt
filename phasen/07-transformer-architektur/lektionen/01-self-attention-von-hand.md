---
id: 07.01
titel: Self-Attention von Hand — Q, K, V und die Softmax-Skalierung
phase: 07-transformer-architektur
dauer_minuten: 90
schwierigkeit: mittel
stand: 2026-04-29
voraussetzungen: [01.01, 03.01]
lernziele:
  - Query, Key, Value als drei Linear-Projektionen verstehen
  - Skalierte Dot-Product-Attention von Hand rechnen
  - Causal-Maske vs. bidirektional verstehen
  - Encoder vs. Decoder vs. Encoder-Decoder einordnen
compliance_anker:
  - reproducible-training
ai_act_artikel:
  - art-11
---

<!-- colab-badge:begin -->
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/s-a-s-k-i-a/ki-engineering-werkstatt/blob/main/dist-notebooks/phasen/07-transformer-architektur/code/01_attention_und_kv_cache.ipynb)
<!-- colab-badge:end -->

## Worum es geht

> Stop treating Transformer as a black box. — Self-Attention besteht aus **drei Matrixmultiplikationen plus einem Softmax**. Wer das einmal von Hand gerechnet hat, hat 60 % des Transformers verstanden. Der Rest ist Plumbing.

Diese Lektion macht Self-Attention konkret: was Q, K, V geometrisch bedeuten, warum die Skalierung mit `√d_k` mathematisch nötig ist, und wann man Causal-Masking nutzt.

## Voraussetzungen

- Lektion 01.01 (Vektoren + Skalarprodukt)
- Lektion 03.01 (PyTorch nn.Linear)

## Konzept

### Schritt 1: Tokens werden zu Vektoren (Embedding)

Eingabe: ein Satz, Token-für-Token (Phase 05). Jedes Token wird zu einem **Embedding** der Dimension `d_model` (z.B. 768, 1024, 4096):

```text
"Der Hund schläft" → 3 Tokens → Matrix X ∈ ℝ^(3 × d_model)
```

### Schritt 2: Drei Projektionen — Q, K, V

Aus jedem Token-Embedding werden drei Vektoren berechnet — alle mit eigenen lernbaren Matrizen `W_Q`, `W_K`, `W_V`:

```text
Q = X @ W_Q          # Query  — "wonach suche ich?"
K = X @ W_K          # Key    — "was repräsentiere ich?"
V = X @ W_V          # Value  — "was ist mein Inhalt?"
```

**Geometrische Intuition**:

- **Query** ist die „Frage" eines Tokens an alle anderen
- **Key** ist das „Etikett" eines Tokens — was es zu Suche bietet
- **Value** ist der eigentliche Inhalt, der weitergegeben wird

Klassische Analogie: Datenbank-Lookup. Eine Query wird mit allen Keys verglichen; die Übereinstimmung gewichtet, wieviel Value zurückkommt.

### Schritt 3: Attention-Scores

Die Übereinstimmung Query ↔ Key ist ein **Skalarprodukt**:

```text
Scores = Q @ K.T       # ∈ ℝ^(N × N), N = Sequenz-Länge
```

Element `Scores[i, j]` = wie sehr passt Query von Token `i` zu Key von Token `j`. Hohe Werte = stark verwandt.

### Schritt 4: Skalierung mit √d_k — die `1/√d` Magie

Bei Dimension `d_k` ist das Skalarprodukt zweier Zufallsvektoren typischerweise **groß** (Varianz wächst mit `d_k`). Großes Skalarprodukt → Softmax saturiert → Gradient verschwindet → Training instabil.

Lösung: dividieren durch `√d_k`:

```text
Scores_skaliert = (Q @ K.T) / sqrt(d_k)
```

**Beispiel**: bei `d_k = 64` ist `√64 = 8`. Skores werden auf einen lehrbaren Bereich gestaucht.

### Schritt 5: Softmax über Sequenz-Achse

Pro Query (Zeile `i`) verteilt Softmax die Aufmerksamkeit über alle Keys:

```text
Attention_Weights[i, :] = softmax(Scores_skaliert[i, :])
```

Jede Zeile summiert zu 1.0 — eine **Aufmerksamkeits-Verteilung**.

### Schritt 6: Gewichtete Summe der Values

```text
Output = Attention_Weights @ V    # ∈ ℝ^(N × d_v)
```

Jeder Output-Vektor ist eine **gewichtete Summe** aller Value-Vektoren — gewichtet nach „wie sehr passen meine Query zu deinem Key".

### Die komplette Formel

```text
Attention(Q, K, V) = softmax(Q @ K.T / √d_k) @ V
```

**Das ist es**. Drei Matrixmultiplikationen plus ein Softmax.

### Schritt 7: Causal-Mask vs. Bidirektional

| Architektur | Maske | Beispiel |
|---|---|---|
| **Encoder** (BERT) | keine — alle Tokens schauen auf alle | Klassifikation, NER |
| **Decoder** (GPT) | **Causal** — Token `i` sieht nur Tokens ≤ `i` | Sprach-Generierung |
| **Encoder-Decoder** (T5, BART) | Encoder bidir., Decoder causal | Übersetzung, Summarization |

**Causal-Mask** wird vor Softmax durch `-∞` an Off-Diagonal-Positionen implementiert:

```text
Mask[i, j] = -inf wenn j > i, sonst 0
Scores_masked = Scores_skaliert + Mask
```

Nach Softmax sind die maskierten Positionen 0 — Token kann nicht in die Zukunft schauen.

### Schritt 8: Encoder vs. Decoder vs. Encoder-Decoder — wann was?

| Use-Case | Architektur 2026 |
|---|---|
| Klassifikation, Embedding (BAAI/bge-m3) | Encoder |
| Sprach-Generierung (LLM) | **Decoder-only** (Standard 2026: GPT, Llama, Mistral, Qwen, Pharia) |
| Übersetzung, Summarization | Decoder-only mit Prompt (state-of-the-art) oder Encoder-Decoder (T5/MBART, traditioneller) |

**Stand 2026**: Decoder-only LLMs dominieren. Encoder-Decoder (T5/BART) sind nische.

## Code-Walkthrough — Self-Attention von Hand in 30 Zeilen

```python
import torch
import torch.nn as nn
import math

class SelfAttention(nn.Module):
    """Skalierte Dot-Product-Self-Attention, Single-Head."""

    def __init__(self, d_model: int, d_k: int):
        super().__init__()
        self.d_k = d_k
        self.W_q = nn.Linear(d_model, d_k, bias=False)
        self.W_k = nn.Linear(d_model, d_k, bias=False)
        self.W_v = nn.Linear(d_model, d_k, bias=False)

    def forward(self, x: torch.Tensor, mask: torch.Tensor | None = None) -> torch.Tensor:
        """x: (batch, seq, d_model). mask: (seq, seq) mit 0 / -inf."""
        Q = self.W_q(x)                        # (B, N, d_k)
        K = self.W_k(x)
        V = self.W_v(x)

        scores = Q @ K.transpose(-2, -1)       # (B, N, N)
        scores = scores / math.sqrt(self.d_k)

        if mask is not None:
            scores = scores + mask             # -inf an verbotenen Positionen

        weights = torch.softmax(scores, dim=-1)  # (B, N, N)
        output = weights @ V                   # (B, N, d_k)
        return output


# Test mit Causal-Mask
N = 5
d_model = 16
d_k = 8

x = torch.randn(2, N, d_model)
mask = torch.triu(torch.full((N, N), float("-inf")), diagonal=1)

attn = SelfAttention(d_model, d_k)
print(attn(x, mask=mask).shape)   # torch.Size([2, 5, 8])
```

## Hands-on

→ [`code/01_attention_und_kv_cache.py`](../code/01_attention_und_kv_cache.py)

Marimo-Notebook: visualisiert Attention-Weights für einen kleinen Satz, zeigt die `√d_k`-Skalierung in Aktion (vor/nach), Causal-vs-Bidirektional-Maske.

## Selbstcheck

- [ ] Was ist die Dimension von `softmax(Q @ K.T / √d_k)` bei N Tokens? (Antwort: N × N)
- [ ] Warum dividieren wir durch `√d_k`?
- [ ] Wann nutzt man Causal-Mask?
- [ ] Welche Standard-Architektur 2026: Encoder-only, Decoder-only, oder Encoder-Decoder? (Antwort: Decoder-only)

## Compliance-Anker

- **AI-Act Art. 11** (Tech-Doku): Attention-Pattern (Causal vs. Bidirektional, Maskenstruktur, Sequenz-Länge) ist Teil der Architektur-Dokumentation.

→ [`compliance.md`](../compliance.md)

## Quellen

- Vaswani et al. (2017): „Attention Is All You Need" — <https://arxiv.org/abs/1706.03762>
- Karpathy: „Let's Build GPT (from scratch in code)" — <https://www.youtube.com/watch?v=kCc8FmEb1nY>
- Phuong & Hutter (2022): „Formal Algorithms for Transformers" — <https://arxiv.org/abs/2207.09238>

## Weiterführend

- Lektion 07.02 (Multi-Head, GQA, RoPE)
- Phase 10 (LLM von Null): nano-GPT-Block in voller Schönheit
