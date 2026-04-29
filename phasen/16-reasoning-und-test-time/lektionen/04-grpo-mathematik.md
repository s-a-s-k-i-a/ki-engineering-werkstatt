---
id: 16.04
titel: GRPO-Mathematik — Group Relative Policy Optimization vs. PPO/DPO
phase: 16-reasoning-und-test-time
dauer_minuten: 75
schwierigkeit: experte
stand: 2026-04-29
voraussetzungen: [16.03, 12.05]
lernziele:
  - PPO/DPO/GRPO mathematisch unterscheiden
  - GRPO-Loss-Funktion verstehen + Reward-Normalisierung
  - TRL `GRPOTrainer` praktisch nutzen
  - Wann GRPO statt DPO/PPO
compliance_anker:
  - reward-hacking-prevention
ai_act_artikel:
  - art-15
---

## Worum es geht

> Stop adding a critic when you don't need one. — GRPO ersetzt das Critic-Modell durch gruppen-relative Advantages. Spart 50 % Memory, ist stabiler und ist 2026 der Default für verifizierbare Reasoning-Tasks.

## Voraussetzungen

- Lektion 16.03 (DeepSeek-R1)
- Phase 12.05 (TRL-Trainer)
- Lineare Algebra + Wahrscheinlichkeit

## Konzept

### Drei Alignment-Methoden im Vergleich

```mermaid
flowchart TB
    A[Methode] --> P[PPO<br/>RLHF-Standard]
    A --> D[DPO<br/>Direct Preference]
    A --> G[GRPO<br/>Group Relative]

    P --> P1[+ Reward-Modell]
    P --> P2[+ Critic / Value-Net]
    P --> P3[2 zusätzliche Modelle]

    D --> D1[+ pairs (chosen/rejected)]
    D --> D2[kein Reward-Modell]
    D --> D3[1 Modell-Kopie (ref)]

    G --> G1[+ binärer Reward]
    G --> G2[kein Critic]
    G --> G3[N Samples pro Prompt]

    classDef base fill:#FF6B3D,color:#0E1116
    classDef pattern fill:#3D8BFF,color:#FFF
    class A base
    class P,D,G pattern
```

### PPO — der Klassiker (RLHF)

Schulman et al. 2017, später Ouyang et al. 2022 für RLHF. Der OpenAI-GPT-3.5-Pfad.

```text
L_PPO = E[ min(r_t × A_t, clip(r_t, 1-ε, 1+ε) × A_t) ] - β × KL(π || π_ref)
```

Wo:

- `r_t = π(a|s) / π_old(a|s)` — Policy-Ratio
- `A_t` — Advantage aus Critic + GAE (Generalized Advantage Estimation)
- `KL`-Term verhindert Drift

**Probleme**:

- Critic-Modell muss separat trainiert werden (zusätzliche 7B-70B-Modell-Kopie)
- Reward-Modell-Drift während Training
- Hyperparameter-empfindlich (β, ε, learning_rate)

### DPO — direkter Pfad

Rafailov et al. 2023, [arxiv.org/abs/2305.18290](https://arxiv.org/abs/2305.18290). Eliminiert Reward-Modell durch direkte Optimierung auf Präferenz-Paaren.

```text
L_DPO = -log σ ( β × log( π(y_w|x) / π_ref(y_w|x) ) - β × log( π(y_l|x) / π_ref(y_l|x) ) )
```

Wo:

- `y_w` = chosen response, `y_l` = rejected response
- `π_ref` = frozen reference (Pretraining-Modell)
- `β` = KL-Constraint-Strength

**Vorteile**:

- Kein separates Reward-Modell nötig
- Kein Critic
- Stabiler als PPO

**Nachteile**:

- Braucht **paarweise** Präferenzen (chosen/rejected) — teuer zu sammeln
- Funktioniert schlechter, wenn Präferenzen verrauscht sind

### GRPO — gruppen-relativ

DeepSeek-Math + DeepSeek-R1 (Shao et al. 2024, [arxiv.org/abs/2402.03300](https://arxiv.org/abs/2402.03300)). Der Aufstieg von DeepSeek hat GRPO 2025 zum De-facto-Standard gemacht.

**Kern-Idee**: pro Prompt N Antworten samplen, **Advantages innerhalb der Gruppe normalisieren**:

```text
A_i = (r_i - mean(r_1..r_N)) / std(r_1..r_N + 1e-4)
```

Loss:

```text
L_GRPO = -E[ (1/N) Σ_i (π(a_i|s) / π_old(a_i|s)) × A_i ] + β × KL(π || π_ref)
```

**Eigenschaften**:

- **Kein Critic** — Advantage = relative Position in Gruppe
- **N Samples pro Prompt** (typisch N=8 oder 16)
- **Binärer / kontinuierlicher Reward** — kein Reward-Modell nötig, **Verifier reicht**
- KL-Term wie PPO

### Vergleich tabellarisch

| Eigenschaft | PPO | DPO | GRPO |
|---|---|---|---|
| Reward-Quelle | Reward-Modell | paarweise Labels | Verifier (binär) |
| Zusatz-Modelle | Reward + Critic (2) | π_ref (1) | π_ref (1) |
| Samples pro Prompt | 1 | 1 | N (8–16) |
| Memory-Bedarf | hoch | mittel | niedrig |
| Stabilität | wechselhaft | gut | sehr gut |
| Wann? | klassische RLHF | menschliche Präferenzen | verifizierbare Tasks |

### Warum GRPO 2026 dominiert

1. **DeepSeek-R1-Erfolg**: Nature-publiziert, MIT-Lizenz für Distill, dominiert Math/Code-Benchmarks
2. **Verifizierbare Tasks** (Math, Code) sind ideal — kein menschliches Labeling nötig
3. **Memory-Effizienz** — 50 % weniger als PPO bei vergleichbarer Qualität
4. **Open-Source-Tooling** — TRL `GRPOTrainer` v1.3.0 (Stand 04/2026, [huggingface.co/docs/trl/grpo_trainer](https://huggingface.co/docs/trl/grpo_trainer))

### TRL `GRPOTrainer` — Quickstart

```python
from trl import GRPOTrainer, GRPOConfig
from datasets import load_dataset

# Reward-Funktion: binärer Math-Verifier
def math_reward(completions, prompts, **kwargs) -> list[float]:
    rewards = []
    for completion, prompt in zip(completions, prompts):
        # Extract final answer
        gold = extract_answer(prompt)  # aus dem Datensatz
        guess = extract_answer(completion)
        rewards.append(1.0 if gold == guess else 0.0)
    return rewards


trainer = GRPOTrainer(
    model="Qwen/Qwen2.5-Math-7B",
    reward_funcs=[math_reward],
    args=GRPOConfig(
        output_dir="outputs/qwen2.5-math-grpo",
        num_generations=8,         # N samples pro prompt
        max_completion_length=2048,
        learning_rate=1e-6,        # niedrig — Stabilität
        beta=0.04,                 # KL-Regularisierung
        epsilon=0.2,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        num_train_epochs=2,
        bf16=True,
        logging_steps=10,
        save_strategy="epoch",
        seed=42,
    ),
    train_dataset=load_dataset("DigitalLearningGmbH/MATH-lighteval", split="train"),
)

trainer.train()
```

### Multi-Reward-Funktionen

GRPO unterstützt mehrere Reward-Funktionen, die addiert werden:

```python
trainer = GRPOTrainer(
    model="Qwen/Qwen2.5-Math-7B",
    reward_funcs=[
        math_reward,        # 1.0 wenn richtig, 0.0 sonst
        format_reward,      # 0.5 wenn <think>...</think>-Format eingehalten
        length_penalty,     # -0.1 wenn > 4096 Tokens
    ],
    ...
)
```

> Pattern 2026: **mehrere Reward-Funktionen kombiniere**n. Reine Accuracy-Reward kann zu Reward-Hacking führen (Modell findet Shortcuts).

### Reward-Hacking — der Klassiker

Reward-Hacking tritt auf, wenn das Modell den Reward maximiert ohne die eigentliche Aufgabe zu lösen. Beispiele:

| Reward | Hack |
|---|---|
| Final-Answer-Match | Modell nennt **alle möglichen Antworten** im Output |
| Format-Reward | Modell schreibt 1.000 leere `<think>`-Tags |
| Längen-Reward | Modell schreibt sinnloses Füll-Material |
| LLM-Judge | Modell schreibt **schmeichelhafte** Antworten, um Judge zu überzeugen |

**Mitigation**:

1. **Strikte Format-Validation**: Final Answer muss in spezifischer Form (z. B. `\boxed{42}`) auftreten
2. **Mehrere unabhängige Verifier**: Pytest + Lean + Format-Check
3. **Eval-Set außerhalb Trainings-Verteilung**: regelmäßig auf neuen Tasks prüfen
4. **Audit-Logs der Reward-Komponenten**: pro Step welcher Reward dominierte

### Praktische Limits 2026

| Modell-Größe | GPU | Trainings-Zeit für GRPO 5k samples |
|---|---|---|
| 1.5B | RTX 4090 | ~ 4 h |
| 7B | RTX 4090 | ~ 24 h (knapp) |
| 7B | H100 | ~ 6 h |
| 32B | 4× H100 | ~ 24 h |
| 70B | 8× H200 | ~ 48 h |

> GRPO ist **memory-hungrig** wegen N-Samples pro Prompt. Für DACH-Mittelstand-QLoRA sind 7B-14B realistisch, 32B+ braucht Cloud.

### Wann GRPO statt DPO?

| Trigger | Methode |
|---|---|
| Verifier verfügbar (Math, Code) | **GRPO** |
| Menschliche Präferenz-Paare | **DPO** |
| Beides | **DPO + GRPO Stage 2** (Pattern aus DeepSeek-R1) |
| Pure SFT-Daten | **SFTTrainer** (12.05) |
| Reasoning-Capability anlernen | **GRPO** |

## Hands-on

1. Lies das GRPO-Paper-Abstract — verstehe die Advantage-Normalisierung
2. Implementiere eine Reward-Funktion für deutsche Mathe-Aufgaben (extract_answer + Match)
3. Bau einen GRPOTrainer-Run mit Qwen2.5-Math-1.5B (RTX 4090) auf 100 samples — Loss-Verlauf dokumentieren
4. Vergleiche Output mit Basis-Modell auf 20 Test-Aufgaben

## Selbstcheck

- [ ] Du nennst die drei Methoden und ihre Reward-Quellen.
- [ ] Du erklärst gruppen-relative Advantages mathematisch.
- [ ] Du nutzt TRL `GRPOTrainer` mit Multi-Reward-Funktionen.
- [ ] Du erkennst Reward-Hacking-Pattern.
- [ ] Du wählst zwischen GRPO / DPO / PPO je nach Daten-Verfügbarkeit.

## Compliance-Anker

- **Reward-Hacking-Prevention (AI-Act Art. 15 Robustness)**: Multi-Reward + Eval-Set außerhalb Training
- **Audit-Trail**: Reward-Komponenten pro Step loggen
- **Daten-Disziplin**: Trainings-Tasks dokumentiert + reproduzierbar (Phase 12.03)

## Quellen

- GRPO-Paper (Shao et al. 2024) — <https://arxiv.org/abs/2402.03300>
- DPO-Paper (Rafailov et al. 2023) — <https://arxiv.org/abs/2305.18290>
- PPO-Paper (Schulman et al. 2017) — <https://arxiv.org/abs/1707.06347>
- TRL `GRPOTrainer` Docs — <https://huggingface.co/docs/trl/grpo_trainer>
- TRL Cookbook GRPO — <https://huggingface.co/docs/trl/main/en/example_overview>
- Awesome-RLVR — <https://github.com/opendilab/awesome-RLVR>

## Weiterführend

→ Lektion **16.05** (R1-Distillation Hands-on)
→ Lektion **16.06** (Verifier-Loops für Math und Code)
→ Phase **18.04 / 18.05** (DPO und GRPO im Alignment-Kontext)
