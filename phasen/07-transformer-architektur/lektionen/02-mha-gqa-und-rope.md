---
id: 07.02
titel: Multi-Head-Attention, Group-Query-Attention, RoPE und Yarn
phase: 07-transformer-architektur
dauer_minuten: 90
schwierigkeit: mittel
stand: 2026-04-29
voraussetzungen: [07.01]
lernziele:
  - Multi-Head-Attention als parallele Attention-Köpfe verstehen
  - Group-Query-Attention (GQA) als 2026-Standard für KV-Cache-Reduktion erkennen
  - RoPE als Standard-Position-Encoding (Llama, Mistral, Qwen, Pharia)
  - Yarn als Long-Context-Erweiterung von RoPE
compliance_anker:
  - reproducible-training
ai_act_artikel:
  - art-11
  - art-15
---

## Worum es geht

> Stop using vanilla MHA. — Vanilla Multi-Head-Attention (MHA) ist 2026 für **Inference** zu teuer. Group-Query-Attention (**GQA**) reduziert KV-Cache um 4-8× ohne nennenswerte Qualitäts-Verluste — und ist deshalb in **fast jedem** modernen LLM (Llama, Mistral, Qwen, Pharia, GPT-OSS) Standard.

Diese Lektion erklärt drei Erweiterungen: Multi-Head als Skalierung, GQA als Inference-Optimierung, RoPE+Yarn als Position-Encoding.

## Voraussetzungen

- Lektion 07.01 (Self-Attention)

## Konzept

### Schritt 1: Multi-Head-Attention (MHA)

Statt **einer** großen Attention-Schicht der Dimension `d_model` werden **mehrere** parallele „Köpfe" mit kleineren Dimensionen `d_k = d_model / h` betrieben:

```text
Kopf_i: Attention(Q_i, K_i, V_i) — eigene W_Q^i, W_K^i, W_V^i
Output = concat(Kopf_1, ..., Kopf_h) @ W_O
```

**Intuition**: jeder Kopf lernt **andere** Beziehungs-Muster — einer für Subjekt-Verb-Beziehung, einer für Negationen, einer für Koreferenz, etc.

Standard-Werte 2026: `h = 8` bis `h = 96` Köpfe.

### Schritt 2: Multi-Query-Attention (MQA)

**MQA** (Shazeer, 2019) reduziert: alle Köpfe teilen **eine** K- und V-Projektion, aber haben individuelle Q-Projektionen:

```text
Kopf_i: Attention(Q_i, K_shared, V_shared)
```

**Effekt**: KV-Cache wird um Faktor `h` kleiner. Aber leichte Qualitäts-Verschlechterung.

### Schritt 3: Group-Query-Attention (GQA) — der 2026-Kompromiss

**GQA** (Ainslie et al., 2023) ist der Mittelweg: K und V werden in **Gruppen** geteilt:

```text
h Köpfe gruppiert in g Gruppen — jede Gruppe teilt K, V

Beispiel: h = 32 Köpfe, g = 8 Gruppen → KV-Cache 4× kleiner
```

**Why GQA dominiert 2026**:

- KV-Cache-Reduktion 4-8× → mehr Tokens pro GPU
- Quality fast wie Full-MHA
- Llama 3.3 (g=8 für 70B), Mistral Large 3, Qwen3, Pharia, GPT-OSS — alle GQA

```python
class GroupedQueryAttention(nn.Module):
    def __init__(self, d_model, n_q_heads, n_kv_heads):
        super().__init__()
        assert n_q_heads % n_kv_heads == 0
        self.d_head = d_model // n_q_heads
        self.n_q = n_q_heads
        self.n_kv = n_kv_heads

        self.W_q = nn.Linear(d_model, n_q_heads * self.d_head, bias=False)
        self.W_k = nn.Linear(d_model, n_kv_heads * self.d_head, bias=False)
        self.W_v = nn.Linear(d_model, n_kv_heads * self.d_head, bias=False)
        self.W_o = nn.Linear(d_model, d_model, bias=False)
```

### Schritt 4: Position-Encoding — warum überhaupt?

Self-Attention ist **permutations-invariant**: ohne explizite Position weiss das Modell nicht, wer Subjekt und wer Objekt ist.

**Lösungen historisch**:

- **Sinusoidal** (Vaswani 2017): feste Sin/Cos-Wellen. Beweisbar gut, aber generalisiert schlecht.
- **Learned** (BERT, GPT-2): einfach, aber begrenzt auf Trainings-Sequenz-Länge.
- **ALiBi** (Press et al. 2022): Bias direkt auf Attention-Scores. Schnell, aber selten 2026.
- **RoPE** (Su et al. 2021): **2026-Standard**.
- **Yarn** (Peng et al. 2024): RoPE-Erweiterung für Long-Context.

### Schritt 5: RoPE (Rotary Position Embeddings)

Statt Position als zusätzlichen Vektor zu addieren, **rotiert** RoPE die Q- und K-Vektoren in 2D-Ebenen um Winkel, die von der Position abhängen:

```text
Position m, Frequenz θ_i:
  rotate(q_i, m × θ_i)
```

**Eigenschaften**:

- **Relative Position automatisch** im Skalarprodukt
- Trainings-Length kann erweitert werden via Frequenz-Skalierung
- Standard in Llama, Mistral, Qwen, Pharia, GPT-OSS

### Schritt 6: Yarn — Long-Context für RoPE

**Yarn** (Yet another RoPE extensioN, Peng et al. 2024) ist die saubere Methode, RoPE-trainierte Modelle auf längere Kontexte zu erweitern:

- Niedrige Frequenzen werden **interpoliert** (gestaucht)
- Hohe Frequenzen bleiben unverändert
- Plus „temperature scaling"

**Wirkung**: Llama-3.3 wurde via Yarn von 8k auf 128k Kontext erweitert (mit zusätzlichem kurzen Finetuning). Effektive Context-Länge bleibt darunter (siehe Phase 09 RULER-Eval).

### Schritt 7: Attention-Sinks (klein aber wichtig)

**Attention-Sinks** (StreamingLLM, Xiao et al. 2024) sind frühe Tokens (oft die ersten 4), die **abnormal hohe** Attention-Scores anziehen — wenn man sie aus dem KV-Cache evicted, kollabiert das Modell.

**Implementation 2026**: bei Sliding-Window-Inference die ersten paar Tokens immer behalten. Standard in vLLM und SGLang.

## Code-Walkthrough — Multi-Head + RoPE skizziert

```python
import torch
import torch.nn as nn
import math

class RoPE(nn.Module):
    """Rotary Position Embeddings (vereinfacht)."""

    def __init__(self, d_head: int, max_seq: int = 4096, base: int = 10000):
        super().__init__()
        inv_freq = 1.0 / (base ** (torch.arange(0, d_head, 2).float() / d_head))
        positions = torch.arange(max_seq).float()
        sinusoid = torch.einsum("i,j->ij", positions, inv_freq)
        self.register_buffer("cos", sinusoid.cos())
        self.register_buffer("sin", sinusoid.sin())

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: (B, h, N, d_head). Rotate Pairs (x_2k, x_2k+1).
        N = x.size(-2)
        cos = self.cos[:N].unsqueeze(0).unsqueeze(0)
        sin = self.sin[:N].unsqueeze(0).unsqueeze(0)
        x1, x2 = x[..., 0::2], x[..., 1::2]
        x_rot = torch.stack([x1 * cos - x2 * sin, x1 * sin + x2 * cos], dim=-1)
        return x_rot.flatten(-2)


# In Praxis: HuggingFace transformers, Llama-Familie hat das in
# transformers.models.llama.modeling_llama.LlamaRotaryEmbedding implementiert.
```

## Hands-on

→ [`code/01_attention_und_kv_cache.py`](../code/01_attention_und_kv_cache.py)

Im Notebook gibt es einen **GQA-Speicher-Tab**, der für gegebene Modell-Größe (Llama 70B, Mistral Large 3) die KV-Cache-Größe für unterschiedliche `n_kv_heads`-Werte berechnet — und zeigt, wie GQA die Memory-Last beim Long-Context senkt.

## Selbstcheck

- [ ] Was ist der Unterschied MHA / MQA / GQA?
- [ ] Warum ist GQA 2026 LLM-Standard?
- [ ] Welche Position-Encoding-Familie nutzen Llama, Mistral, Pharia? (Antwort: RoPE)
- [ ] Was macht Yarn?

## Compliance-Anker

- **AI-Act Art. 11 / 15** (Tech-Doku, Accuracy): Architektur-Eckdaten — Anzahl Heads, GQA-Gruppen, RoPE-Base, Context-Länge — gehören in die Modell-Karte (Phase 17/18).

→ [`compliance.md`](../compliance.md)

## Quellen

- Shazeer (2019): „Fast Transformer Decoding: One Write-Head is All You Need" (MQA) — <https://arxiv.org/abs/1911.02150>
- Ainslie et al. (2023): „GQA: Training Generalized Multi-Query Transformer Models" — <https://arxiv.org/abs/2305.13245>
- Su et al. (2021/24): „RoFormer: Enhanced Transformer with Rotary Position Embedding" — <https://arxiv.org/abs/2104.09864>
- Peng et al. (2024): „YaRN: Efficient Context Window Extension of Large Language Models" — <https://arxiv.org/abs/2309.00071>
- Xiao et al. (2024): „Efficient Streaming Language Models with Attention Sinks" — <https://arxiv.org/abs/2309.17453>

## Weiterführend

- Lektion 07.03 (KV-Cache, FlashAttention, vLLM PagedAttention)
- Phase 09 (Long-Context-Eval mit RULER)
- Phase 10 (LLM von Null mit RoPE)
