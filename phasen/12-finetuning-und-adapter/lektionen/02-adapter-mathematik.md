---
id: 12.02
titel: Adapter-Mathematik — rank, alpha, target_modules, dropout
phase: 12-finetuning-und-adapter
dauer_minuten: 45
schwierigkeit: fortgeschritten
stand: 2026-04-29
voraussetzungen: [12.01]
lernziele:
  - LoRA-Adapter-Mathematik im Detail (rank, scaling, target_modules)
  - Wie alpha und r interagieren (Skalierungs-Faktor)
  - target_modules pro Architektur richtig setzen
  - Adapter-Größen abschätzen (in MB)
compliance_anker:
  - reproduzierbarkeit-rank-config
ai_act_artikel:
  - art-12
---

## Worum es geht

> Stop copy-pasting `r=8, alpha=16`. — die LoRA-Hyperparameter sind kein Geheimnis, aber die Zusammenhänge zwischen Rank, Skalierungs-Faktor, Dropout und Target-Modules entscheiden über 30 % Qualitäts-Differenz.

## Voraussetzungen

- Lektion 12.01 (Trade-offs)
- Lineare Algebra (Matrix-Multiplikation, Rank)

## Konzept

### LoRA in einer Gleichung

Sei W ∈ ℝ^(d×k) die Original-Gewichts-Matrix einer Linear-Schicht. Statt W zu trainieren:

```text
W_neu = W + ΔW
ΔW = (alpha / r) × B × A
```

Mit:

- B ∈ ℝ^(d×r) — initial **null** (damit ΔW=0 beim Start)
- A ∈ ℝ^(r×k) — initial **gaussian-random**
- r — Rank, viel kleiner als min(d, k)
- alpha — Skalierungs-Faktor

Der Kern-Trick: ΔW hat Rank ≤ r. Statt d × k Parametern trainierst du nur r × (d + k). Bei Llama-3-7B (d ≈ 4096) und r=16: ~ 130k Params pro Linear statt ~ 16M.

### Wie alpha und r interagieren

Der Skalierungs-Faktor `alpha / r` bestimmt, wie stark der Adapter auf das Basis-Modell „durchschlägt".

| `r` | `alpha` | Skalierungs-Faktor | Effekt |
|---|---|---|---|
| 8 | 8 | 1.0 | konservativ — Adapter wirkt schwach |
| 16 | 32 | 2.0 | **Standard** — gute Balance |
| 32 | 64 | 2.0 | mehr Kapazität, gleicher Skalierungs-Faktor |
| 64 | 16 | 0.25 | hoher Rank, schwache Wirkung — selten sinnvoll |
| 16 | 64 | 4.0 | aggressiv — kann Basis-Modell überschreiben |

**Konvention 2026**: `alpha = 2 × r` ist der pragmatische Default. Bei sehr kleinen Datensets (< 5k samples): `alpha = r` (vorsichtiger).

### `target_modules` pro Architektur

Welche Linear-Layers werden mit LoRA-Adaptern versehen? Das hängt von der Modell-Architektur ab:

#### Llama / Mistral / Qwen — Standard 7-Module-Setup

```python
target_modules = [
    "q_proj", "k_proj", "v_proj", "o_proj",  # Attention
    "gate_proj", "up_proj", "down_proj",       # MLP / Gated-MLP
]
```

Das deckt **alle Linear-Schichten** im Transformer-Block ab. Maximale Flexibilität, höchste Adapter-Größe.

#### Nur Attention (kompakter)

```python
target_modules = ["q_proj", "v_proj"]
```

LoRA-Original-Paper zeigt: nur Q und V reichen oft schon. Adapter ist dann **3–4× kleiner** bei minimalem Qualitätsverlust.

> Empfehlung 2026: für Domain-Tuning (z. B. „Steuer-Sprach-Stil") nur `q_proj` + `v_proj`. Für Verhaltens-Änderung (z. B. „immer formal antworten"): alle 7.

#### MoE-Modelle (Mixtral, DeepSeek, Qwen-MoE)

Bei Mixture-of-Experts brauchst du LoRA-Adapter pro Expert:

```python
target_modules = [
    "q_proj", "k_proj", "v_proj", "o_proj",
    "block_sparse_moe.experts.*.w1",
    "block_sparse_moe.experts.*.w2",
    "block_sparse_moe.experts.*.w3",
]
```

> Stand 04/2026: axolotl v0.16.x hat **MoE+LoRA-Fused-Kernels** — 15× schneller, 40× weniger Memory ([axolotl Releases](https://github.com/axolotl-ai-cloud/axolotl/releases)).

### Adapter-Größe abschätzen

Bei Llama-3-7B (32 Transformer-Blöcke, hidden_dim=4096, intermediate_dim=14336) und r=16:

```text
Pro Block (7 Linear-Layers, alle 4096 oder 14336):
  4 × Attention:  4 × (4096 × 16 + 16 × 4096) × 2 (Adam-states) = ~ 1 MB
  3 × MLP:        3 × (14336 × 16 + 16 × 4096) × 2 = ~ 2 MB
  → Pro Block: ~ 3 MB
× 32 Blöcke = ~ 100 MB
```

So passt ein 7B-LoRA-Adapter in 100 MB SafeTensors-Datei. Bei r=64: ~ 400 MB. Bei nur Q+V: ~ 30 MB.

### Dropout für Adapter

`lora_dropout` schützt vor Overfitting auf kleine Datasets:

| Dataset-Größe | Empfohlener Dropout |
|---|---|
| < 1.000 samples | 0.1 |
| 1k–10k samples | 0.05 |
| 10k–100k samples | 0.0–0.05 |
| > 100k samples | 0.0 |

### Bias-Training: `bias`-Parameter

In PEFT:

```python
LoraConfig(bias="none")  # default
LoraConfig(bias="lora_only")  # bias-Vektoren der LoRA-Layer mit-trainiert
LoraConfig(bias="all")  # alle bias-Vektoren mit-trainiert
```

> Empfehlung: `none` für 95 % der Fälle. `lora_only` nur, wenn dein Datenset > 50k samples hat und du jedes Quäntchen Qualität brauchst.

### DoRA — die LoRA-Erweiterung 2025/26

**DoRA** (Liu et al. 2024, [arxiv.org/abs/2402.09353](https://arxiv.org/abs/2402.09353)) zerlegt Gewichte in **Magnitude** und **Direction**:

```text
W = m × (W / ||W||)        # decompose
W_neu = m × ((W + BA) / ||W + BA||)
```

Empirisch +0.5–2 % Qualität gegenüber LoRA bei gleichem Speicher. Stand PEFT v0.19.1: per `use_dora=True` aktivierbar. Performance-Overhead ~ 10–20 % beim Training.

### LoRA+ — separate Lernraten

**LoRA+** (Hayou et al. 2024, [arxiv.org/abs/2402.12354](https://arxiv.org/abs/2402.12354)): A und B brauchen unterschiedliche Lernraten. Empirisch: B sollte ~ 16× höher gelernt werden als A.

Stand 04/2026 in axolotl + TRL produktiv unterstützt.

### Reproduzierbarkeits-Anker

Pflicht für AI-Act-Doku (Art. 12):

```yaml
# adapter-config.yaml — committet ins Repo
base_model: "meta-llama/Llama-3.3-8B-Instruct"
lora_config:
  r: 16
  lora_alpha: 32
  lora_dropout: 0.05
  bias: "none"
  target_modules: ["q_proj", "k_proj", "v_proj", "o_proj",
                   "gate_proj", "up_proj", "down_proj"]
  use_dora: false
training:
  seed: 42
  learning_rate: 2e-4
  num_epochs: 3
  batch_size: 4
  gradient_accumulation_steps: 4
dataset:
  name: "interner-support-2026-04"
  hash: "sha256:abc123..."  # Reproduzierbarkeit pflicht
  samples: 12_345
```

## Hands-on

1. Berechne für Llama-3.3-70B (80 Layer, hidden_dim=8192) die LoRA-Adapter-Größe bei r=16, alle 7 Module
2. Schätze die VRAM-Reduktion: Full-FT 70B vs. QLoRA 70B mit r=16
3. Lies die DoRA-Paper-Section „Experiments" — wann lohnt der Mehraufwand?

## Selbstcheck

- [ ] Du erklärst die LoRA-Gleichung W_neu = W + (α/r) × BA.
- [ ] Du wählst `r` und `alpha` für ein konkretes Use-Case-Profil.
- [ ] Du nennst die `target_modules` für Llama / Mistral / Qwen.
- [ ] Du schätzt die Adapter-Größe in MB ab.

## Compliance-Anker

- **Reproduzierbarkeit (AI-Act Art. 12)**: alle Hyperparameter + Daten-Hash committed ins Repo
- **Audit-Trail**: jeder Trainings-Run = ein Tag im Modell-Repository (Phase 17.06)

## Quellen

- LoRA-Paper (Hu et al. 2021) — <https://arxiv.org/abs/2106.09685>
- QLoRA-Paper (Dettmers et al. 2023) — <https://arxiv.org/abs/2305.14314>
- DoRA-Paper (Liu et al. 2024) — <https://arxiv.org/abs/2402.09353>
- LoRA+ Paper (Hayou et al. 2024) — <https://arxiv.org/abs/2402.12354>
- PEFT LoRA-Config-Doku — <https://huggingface.co/docs/peft/conceptual_guides/lora>
- HF Adapter-Hub — <https://huggingface.co/docs/peft/main/en/task_guides/lora_based_methods>

## Weiterführend

→ Lektion **12.03** (Datensatz-Aufbau für Instruction-Tuning)
→ Lektion **12.07** (Multi-LoRA-Inference mit vLLM)
