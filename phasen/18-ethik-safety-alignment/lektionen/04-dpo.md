---
id: 18.04
titel: DPO — Direct Preference Optimization (ohne Reward-Modell)
phase: 18-ethik-safety-alignment
dauer_minuten: 60
schwierigkeit: fortgeschritten
stand: 2026-04-29
voraussetzungen: [18.03, 12.05]
lernziele:
  - DPO-Loss-Funktion verstehen
  - Wann DPO statt RLHF
  - TRL `DPOTrainer` v1.3.0 praktisch
  - DPO für Bias-Korrektur
compliance_anker:
  - praeferenz-daten-lizenz
ai_act_artikel:
  - art-15
---

## Worum es geht

> Stop training reward models when you have preference pairs. — DPO (Rafailov et al. 2023, [arxiv.org/abs/2305.18290](https://arxiv.org/abs/2305.18290)) eliminiert das Reward-Modell und ist 2026 der **stabilste** Alignment-Pfad bei verfügbaren Präferenz-Paaren.

## Voraussetzungen

- Lektion 18.03 (RLHF konzeptuell)
- Phase 12.05 (TRL-Stack)

## Konzept

### DPO in einer Gleichung

```text
L_DPO = -E[(x, y_w, y_l) ~ D] log σ ( β × log( π(y_w|x) / π_ref(y_w|x) )
                                       - β × log( π(y_l|x) / π_ref(y_l|x) ) )
```

Wo:

- `y_w` (chosen) = bevorzugte Antwort, `y_l` (rejected) = abgelehnte Antwort
- `π_ref` = frozen Reference-Modell (= SFT-Modell vor DPO)
- `β` = KL-Constraint-Strength (typisch 0.1)

**Intuition**: DPO maximiert die Wahrscheinlichkeit der bevorzugten Antwort relativ zur abgelehnten — ohne separat ein Reward-Modell zu trainieren.

### Datensatz-Format

```python
# DPO erwartet pro Sample: prompt + chosen + rejected
{
    "prompt": "Erklär mir DSGVO Art. 5 in einfachen Worten.",
    "chosen": "Die DSGVO Art. 5 legt sechs Grundsätze für die Verarbeitung personenbezogener Daten fest: Rechtmäßigkeit, Treu und Glauben, Transparenz, Zweckbindung, Datenminimierung, Richtigkeit, Speicherbegrenzung, Integrität und Vertraulichkeit. ...",
    "rejected": "DSGVO Art. 5 ist ein wichtiger Paragraph zum Datenschutz."  # zu kurz, zu unspezifisch
}
```

### Wo Präferenz-Paare herkommen

| Quelle | Pattern | Lizenz-Hinweis |
|---|---|---|
| **Eigene User-Feedback** (Daumen hoch/runter) | binär — KTO besser als DPO | DSGVO-konforme Speicherung pflicht |
| **Annotator-Pool** | echte Pairs | DACH-Repräsentativität |
| **LLM-generierte Pairs** (Modell A vs. Modell B) | Cost-effizient | Lizenz von beiden Modellen prüfen |
| **Public-Datasets** (Anthropic HH-RLHF, OpenAssistant) | EN-Standard | Lizenz im Detail prüfen |
| **DACH-Datasets** (SauerkrautLM-DPO) | DE-spezifisch | VAGOsolutions-Lizenz |

> Stand 04/2026: [SauerkrautLM-v2-14b-DPO](https://huggingface.co/VAGOsolutions/SauerkrautLM-v2-14b-DPO) ist eines der wenigen produktiven DPO-trainierten DE-Modelle.

### TRL `DPOTrainer` Quickstart

Stand TRL v1.3.0 (26.04.2026):

```python
from trl import DPOTrainer, DPOConfig
from datasets import load_dataset
from peft import LoraConfig

# Datensatz mit prompt/chosen/rejected
dataset = load_dataset("path/to/dpo-dataset-de", split="train")

trainer = DPOTrainer(
    model="Qwen/Qwen3-7B-Instruct",  # SFT-Modell
    ref_model=None,                  # bei PEFT: Modell ohne Adapter als ref
    args=DPOConfig(
        output_dir="outputs/qwen3-7b-dpo",
        per_device_train_batch_size=2,
        gradient_accumulation_steps=8,
        num_train_epochs=1,           # DPO meistens 1 Epoch
        learning_rate=5e-6,           # niedriger als SFT
        beta=0.1,                     # KL-Strength
        bf16=True,
        logging_steps=10,
        seed=42,
    ),
    train_dataset=dataset,
    peft_config=LoraConfig(
        r=64, lora_alpha=128, lora_dropout=0.0,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                        "gate_proj", "up_proj", "down_proj"],
    ),
)

trainer.train()
```

### β — der wichtigste Hyperparameter

| β | Verhalten |
|---|---|
| 0.01 | sehr aggressive Optimierung — Modell weicht stark vom SFT ab, Drift-Risiko |
| **0.1** | Standard 2026 — gute Balance |
| 0.5 | konservativ — kaum Veränderung gegenüber SFT |
| 1.0 | fast kein Training-Signal — Modell bleibt nahe SFT |

> Bei DACH-Use-Cases mit < 5k Präferenz-Pairs: β=0.1–0.2 empfohlen.

### DPO für Bias-Korrektur

Pattern: aus Bias-Audit (Lektion 18.02) **Korrektur-Pairs** generieren:

```python
korrektur_pairs = [
    {
        "prompt": "Die Krankenschwester betritt den Raum.",
        "chosen": "Sie/Er legt die Patientenakte ab und überprüft die Vitalzeichen.",
        "rejected": "Sie legt ihre Tasche ab und beginnt mit der Pflegerunde.",
    },
    {
        "prompt": "Ahmet bewirbt sich auf den Job als Software-Entwickler.",
        "chosen": "Er hat 5 Jahre Erfahrung in Python und kann gut mit verteilten Systemen umgehen.",
        "rejected": "Er ist motiviert, hat aber Sprachschwierigkeiten.",
    },
    # ... 200+ Pairs
]
```

DPO-Run mit diesen Pairs reduziert messbar Bias auf der Ziel-Dimension. Bei 200 hochwertigen Pairs typisch -30 bis -50 % Bias-Score.

### DPO-Varianten 2026

| Variante | Idee | Wann |
|---|---|---|
| **DPO** (vanilla) | Standard-Pairs | Default |
| **IPO** (Identity-PO) | robuster bei rauschigen Labels | wenn Pairs unsicher |
| **ORPO** | kombiniert SFT + DPO in einem Step | schneller, ohne separate SFT-Stufe |
| **KTO** (Kahneman-Tversky) | nur binäre Labels (gut/schlecht), keine Pairs | bei Daumen-hoch/runter-Feedback |
| **Anchored Preference Optimization (APO)** | mit zusätzlichen Anchor-Antworten | bei mehreren Output-Dimensionen |

> Stand TRL v1.3.0 sind DPO, IPO, ORPO, KTO produktiv. Default 2026: **DPO** für Pairs, **KTO** für binäre Labels.

### Audit-Trail

```yaml
# DPO-Run-Manifest
methode: "DPO"
basis_modell: "Qwen/Qwen3-7B-Instruct"
sft_zwischenschritt: true
referenz_modell: "Qwen/Qwen3-7B-Instruct"  # gleicher Snapshot

datensatz:
  pfad: "datasets/dpo-bias-korrektur-2026-04.jsonl"
  sha256: "abc..."
  pairs: 287
  quelle: "Bias-Audit 2026-04-29 + manuelle Kuratierung"

hyperparameter:
  beta: 0.1
  learning_rate: 5e-6
  num_epochs: 1
  batch_size_eff: 16
  seed: 42

eval_pre_dpo:
  bias_score_geschlecht: 0.42
  bias_score_migration: 0.38
  bias_score_region: 0.31

eval_post_dpo:
  bias_score_geschlecht: 0.18  # -57 %
  bias_score_migration: 0.21   # -45 %
  bias_score_region: 0.19      # -39 %
```

> Pflicht für AI-Act Art. 12 — Trainings-Manifest committet ins Repo.

### Wann DPO **nicht** funktioniert

- **Verrauschte Labels**: Pairs widersprüchlich, Annotator-Disagreement hoch → IPO statt DPO
- **Zu wenige Pairs** (< 500): SFT-Daten oft besser
- **Multi-Objective** (z. B. Bias + Genauigkeit + Kürze): DPO optimiert nur eine Achse
- **Mode Collapse**: Modell gibt nur noch Antworten ähnlich der `chosen`-Verteilung

## Hands-on

1. Generiere 100 Bias-Korrektur-Pairs aus deinem Bias-Audit-Output (18.02)
2. DPO auf Qwen3-7B-Instruct mit diesen Pairs (1 h auf RTX 4090)
3. Re-Audit: ist Bias messbar reduziert?
4. Vergleich: DPO vs. SFT mit denselben Daten

## Selbstcheck

- [ ] Du erklärst die DPO-Loss-Funktion.
- [ ] Du nutzt TRL `DPOTrainer` mit korrektem β.
- [ ] Du wählst DPO / IPO / KTO / ORPO je nach Daten.
- [ ] Du nutzt DPO als Bias-Korrektur-Pfad nach Audit.
- [ ] Du dokumentierst pre/post-DPO-Eval im Manifest.

## Compliance-Anker

- **AI-Act Art. 15 (Robustness)**: DPO als Bias-Mitigation pflichtbewusst nach Audit
- **DSGVO**: User-Feedback als Trainings-Daten = Einwilligung pflicht (Art. 6/7)
- **Lizenz**: Lizenz der Pairs prüfen (eigene Annotation vs. SauerkrautLM-DPO)

## Quellen

- DPO-Paper (Rafailov et al. 2023) — <https://arxiv.org/abs/2305.18290>
- IPO-Paper — <https://arxiv.org/abs/2310.12036>
- KTO-Paper (Ethayarajh et al. 2024) — <https://arxiv.org/abs/2402.01306>
- ORPO-Paper — <https://arxiv.org/abs/2403.07691>
- TRL DPOTrainer — <https://huggingface.co/docs/trl/dpo_trainer>
- SauerkrautLM-DPO — <https://huggingface.co/VAGOsolutions/SauerkrautLM-v2-14b-DPO>

## Weiterführend

→ Lektion **18.05** (GRPO im Alignment-Kontext)
→ Lektion **18.06** (Constitutional AI)
→ Phase **12.05** (Trainings-Stack mit DPO-Integration)
