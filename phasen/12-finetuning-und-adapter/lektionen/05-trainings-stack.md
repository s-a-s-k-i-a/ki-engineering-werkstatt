---
id: 12.05
titel: Trainings-Stack 2026 — Unsloth, axolotl, TRL im Vergleich
phase: 12-finetuning-und-adapter
dauer_minuten: 75
schwierigkeit: fortgeschritten
stand: 2026-04-29
voraussetzungen: [12.02, 12.03]
lernziele:
  - Unsloth (Single-GPU-Speedup), axolotl (YAML-Config), TRL (Programmatic) abgrenzen
  - Wann welcher Stack
  - Konkrete Trainings-Kommandos für Llama-3.3-8B mit GermanQuAD
  - GPU-Memory-Pattern und Optimizer-Choice
compliance_anker:
  - reproduzierbarkeit-yaml
ai_act_artikel:
  - art-12
---

## Worum es geht

> Stop arguing about transformers vs. axolotl vs. unsloth. — drei Stacks, drei klare Use-Cases. Stand 04/2026 sind alle drei produktiv: Unsloth `2026.4.x` (Single-GPU-Speedup), axolotl `v0.16.1` (YAML-Config), TRL `v1.3.0` (programmatic).

## Voraussetzungen

- Lektion 12.02 (Adapter-Mathematik)
- Lektion 12.03 (Datensatz-Aufbau)
- NVIDIA-GPU mit ≥ 24 GB VRAM (RTX 4090/5090, A100, H100)

## Konzept

### Drei-Stack-Vergleich

| Aspekt | Unsloth | axolotl | TRL |
|---|---|---|---|
| **Approach** | Single-GPU Speedup-Library | YAML-Config-First | Python-API |
| **Stable-Version 04/2026** | rolling `2026.4.x` | v0.16.1 (02.04.2026) | v1.3.0 (26.04.2026) |
| **Speedup vs. Vanilla HF** | **2× schneller, 70 % weniger VRAM** | gut, aber primär durch FA2 + DeepSpeed | Vanilla |
| **MoE-Support** | ja | ja, mit Fused-Kernels (15× schneller) | manuell |
| **Multi-GPU** | DDP/FSDP GA seit 2026 | FSDP1/FSDP2/DeepSpeed/Ray | manuell |
| **DPO/KTO/GRPO** | ja, Notebooks | ja, im YAML | ja, dedizierte Trainer |
| **Wann?** | Single-GPU-Prototyping | Reproduzierbare Configs für Team | Custom-Trainer + maximale Kontrolle |

### Unsloth — Single-GPU-Sweet-Spot

[github.com/unslothai/unsloth](https://github.com/unslothai/unsloth) — Stand 04/2026 mit 250+ Notebook-Templates ([github.com/unslothai/notebooks](https://github.com/unslothai/notebooks)).

Installation:

```bash
uv pip install unsloth
# Mit Triton + Bitsandbytes für 4-bit
```

Quickstart-Pattern:

```python
from unsloth import FastLanguageModel
from trl import SFTTrainer
from datasets import load_dataset

modell, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Llama-3.3-8B-Instruct-bnb-4bit",
    max_seq_length=2048,
    dtype=None,  # auto
    load_in_4bit=True,
)

# LoRA-Adapter dranschrauben
modell = FastLanguageModel.get_peft_model(
    modell,
    r=16,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    lora_alpha=32,
    lora_dropout=0.05,
    bias="none",
    use_gradient_checkpointing="unsloth",  # Unsloth-eigenes Checkpointing
    random_state=42,
    use_rslora=False,
    loftq_config=None,
)

# Datensatz
dataset = load_dataset("deepset/germanquad", split="train")

# Trainer
trainer = SFTTrainer(
    model=modell,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=2048,
    packing=True,
    args=TrainingArguments(
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        warmup_steps=20,
        num_train_epochs=3,
        learning_rate=2e-4,
        bf16=True,
        logging_steps=10,
        optim="adamw_8bit",
        weight_decay=0.01,
        lr_scheduler_type="cosine",
        seed=42,
        output_dir="outputs/llama33-8b-germanquad",
    ),
)

trainer.train()

# Save Adapter
modell.save_pretrained("adapters/llama33-8b-germanquad")
```

Vorteile:

- 2× schneller als Vanilla HF auf RTX 4090
- 70 % weniger VRAM — 8B QLoRA passt in 12 GB
- Vorgefertigte 4-bit-Modelle in `unsloth/`-Namespace
- Multi-GPU GA seit Frühjahr 2026

### axolotl — YAML-Config-First

[github.com/axolotl-ai-cloud/axolotl](https://github.com/axolotl-ai-cloud/axolotl) v0.16.1 (02.04.2026).

```bash
uv pip install axolotl[flash-attn,deepspeed]==0.16.1
```

`config.yaml`:

```yaml
base_model: meta-llama/Llama-3.3-8B-Instruct
model_type: AutoModelForCausalLM
tokenizer_type: AutoTokenizer

load_in_4bit: true
strict: false

datasets:
  - path: deepset/germanquad
    type: chat_template
    chat_template: llama3
    field_messages: messages

dataset_prepared_path: last_run_prepared
output_dir: ./outputs/llama33-8b-germanquad

sequence_len: 2048
sample_packing: true
pad_to_sequence_len: true

adapter: qlora
lora_r: 16
lora_alpha: 32
lora_dropout: 0.05
lora_target_modules:
  - q_proj
  - k_proj
  - v_proj
  - o_proj
  - gate_proj
  - up_proj
  - down_proj

gradient_accumulation_steps: 4
micro_batch_size: 4
num_epochs: 3
optimizer: adamw_8bit
lr_scheduler: cosine
learning_rate: 0.0002

bf16: auto
flash_attention: true
gradient_checkpointing: true

warmup_steps: 20
weight_decay: 0.01
seed: 42

# DeepSpeed (Multi-GPU)
deepspeed: deepspeed_configs/zero3_bf16.json
```

Training:

```bash
axolotl preprocess config.yaml
axolotl train config.yaml
```

> Vorteil: das gesamte Trainings-Setup ist als YAML committet → reproduzierbar, audit-fähig, vom Team teilbar. Pflicht-Pattern für AI-Act Art. 12.

### TRL — Python-API für Custom-Cases

Stand 04/2026: TRL v1.3.0 ([github.com/huggingface/trl](https://github.com/huggingface/trl)) mit produktiven Trainern: `SFTTrainer`, `DPOTrainer`, `KTOTrainer`, `GRPOTrainer`, `RewardTrainer`.

> Hinweis: `PPOTrainer`/`PPOConfig` sind in TRL v1.3.0 nach `trl.experimental.ppo` verschoben und werden in v0.29 entfernt — produktiv nur eingeschränkt empfohlen.

Wann TRL direkt: wenn du Custom-Reward-Funktionen, eigene Loss-Mods oder Forschungs-Setups brauchst.

```python
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig

modell = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.3-8B-Instruct",
                                              load_in_4bit=True,
                                              torch_dtype="bfloat16")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.3-8B-Instruct")

dataset = load_dataset("deepset/germanquad", split="train")

lora = LoraConfig(
    r=16, lora_alpha=32, lora_dropout=0.05, bias="none",
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    task_type="CAUSAL_LM",
)

trainer = SFTTrainer(
    model=modell,
    train_dataset=dataset,
    peft_config=lora,
    args=SFTConfig(
        output_dir="outputs",
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        num_train_epochs=3,
        learning_rate=2e-4,
        bf16=True,
        optim="adamw_8bit",
        lr_scheduler_type="cosine",
        seed=42,
    ),
)
trainer.train()
```

### Optimizer-Wahl 2026

| Optimizer | Memory pro Param | Geschwindigkeit | Wann |
|---|---|---|---|
| **AdamW (FP32)** | 16 Bytes | Baseline | nie für QLoRA |
| **AdamW 8-bit** (`adamw_8bit`) | 4 Bytes | etwas schneller | **Standard 2026** |
| **AdamW 4-bit** (`adamw_4bit`) | 2 Bytes | gleich | kontroversielle Qualitäts-Daten |
| **Lion** | 8 Bytes | schneller | aggressiver, weniger stabil |
| **Adafactor** | ~ 4 Bytes | langsamer | wenn Memory der Bottleneck |

**Empfehlung 2026**: `adamw_8bit` aus bitsandbytes — produktiver Default für QLoRA.

### Trainings-Hyperparameter — die Defaults

```python
training_args = {
    "learning_rate": 2e-4,           # konservativ + stabil für LoRA
    "num_train_epochs": 3,           # 1 für > 50k samples, 3-5 für < 5k
    "per_device_train_batch_size": 4,
    "gradient_accumulation_steps": 4,  # effektive batch_size 16
    "warmup_ratio": 0.1,             # 10 % der Steps
    "lr_scheduler_type": "cosine",   # cosine besser als linear
    "weight_decay": 0.01,
    "max_grad_norm": 1.0,            # gradient clipping
    "seed": 42,                      # Reproduzierbarkeit
    "bf16": True,                    # auf Hopper / Ampere
    "fp16": False,                   # nur als Fallback
}
```

### GPU-Memory-Pattern

Bei Llama-3.3-8B QLoRA mit batch_size=4, seq_len=2048:

| Komponente | VRAM |
|---|---|
| Basis-Modell (4-bit) | ~ 5,5 GB |
| LoRA-Adapter (FP16, r=16) | ~ 100 MB |
| Optimizer (AdamW 8-bit) | ~ 200 MB |
| Activations + Gradients | ~ 4–6 GB |
| KV-Cache (forward) | ~ 1 GB |
| **Gesamt** | **~ 11–13 GB** |

Passt in 16-GB-GPU mit ein wenig Spielraum. Bei 70B mit r=64: ~ 60 GB → 1× H100/H200.

### Cost-Realität (Stand 04/2026)

| Modell-Klasse | GPU | Stunden | EUR-Cost (bei € 2,73/h Scaleway H100) |
|---|---|---|---|
| 7B QLoRA, 5k samples | RTX 4090 (lokal) | 1–2 | nur Strom (~ 0,30 €) |
| 7B QLoRA, 50k samples | 1× H100 | 4–8 | ~ 11–22 € |
| 32B QLoRA, 50k samples | 1× H100 | 12–20 | ~ 33–55 € |
| 70B QLoRA, 50k samples | 1× H100/H200 | 24–48 | ~ 65–130 € |
| 405B QLoRA | 4× H100 | 100+ | ~ 1.000 €+ |

> **EU-Anbieter 2026**: [Scaleway H100 ab € 2,73/h](https://www.scaleway.com/en/h100/), [OVHcloud H100/H200](https://www.ovhcloud.com/en/public-cloud/gpu/). **Hetzner kein H100** im Cloud-Angebot — nicht für QLoRA-70B+ geeignet.

## Hands-on

1. Wähle einen Stack (Unsloth für Anfänger, axolotl für Reproduzierbarkeit, TRL für Custom)
2. Llama-3.3-8B mit GermanQuAD finetunen (3 Epochen) — Stand-Latenz dokumentieren
3. Adapter speichern + laden + Vergleich gegen Basis-Modell
4. axolotl-Config in Git committen — Reproduzierbarkeits-Test mit Kollegen

## Selbstcheck

- [ ] Du wählst Unsloth / axolotl / TRL je nach Use-Case.
- [ ] Du nutzt `adamw_8bit` als Optimizer-Default.
- [ ] Du dokumentierst Hyperparameter + Daten-Hash für Audit.
- [ ] Du schätzt VRAM-Bedarf vorab korrekt ein.
- [ ] Du kennst die EUR-Kosten pro Modell-Klasse.

## Compliance-Anker

- **Reproduzierbarkeit (AI-Act Art. 12)**: axolotl-YAML committet ins Repo, Daten-Hash dokumentiert
- **Trainings-Audit-Trail**: jeder Run = ein Wandb / Phoenix-Span mit Hyperparametern + Loss-Curve

## Quellen

- Unsloth GitHub — <https://github.com/unslothai/unsloth>
- Unsloth Notebooks — <https://github.com/unslothai/notebooks>
- axolotl Releases v0.16.1 — <https://github.com/axolotl-ai-cloud/axolotl/releases>
- axolotl Docs — <https://docs.axolotl.ai>
- TRL v1.3.0 — <https://github.com/huggingface/trl/releases>
- TRL Docs — <https://huggingface.co/docs/trl>
- Bitsandbytes (8-bit Optimizer) — <https://github.com/bitsandbytes-foundation/bitsandbytes>
- Scaleway H100-Pricing — <https://www.scaleway.com/en/h100/>

## Weiterführend

→ Lektion **12.06** (Adapter merging vs. runtime loading)
→ Lektion **12.07** (Multi-LoRA-Inference mit vLLM)
→ Lektion **12.08** (Hands-on: QLoRA auf Qwen3-7B mit dt. Charity-Dialogen)
