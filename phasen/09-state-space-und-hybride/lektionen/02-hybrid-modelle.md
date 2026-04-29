---
id: 09.02
titel: Hybrid-Modelle — Jamba 1.5, Hunyuan-TurboS, Zamba 2
phase: 09-state-space-und-hybride
dauer_minuten: 60
schwierigkeit: fortgeschritten
stand: 2026-04-29
voraussetzungen: [09.01]
lernziele:
  - Hybrid-Architektur (Transformer + SSM) verstehen
  - AI21 Jamba 1.5 + Hunyuan-TurboS produktiv einsetzen
  - Long-Context-Use-Cases in DACH
compliance_anker:
  - lizenz-disziplin-hybrid
ai_act_artikel:
  - art-15
---

## Worum es geht

> Stop choosing between Transformer and Mamba. — 2026 dominieren **Hybride**: Transformer-Layer für Recall + SSM-Layer für lange Kontexte. **AI21 Jamba 1.5** (Israel) und **Hunyuan-TurboS** (China) sind die produktiven Beispiele.

## Voraussetzungen

- Lektion 09.01 (SSM-Basics)

## Konzept

### Warum Hybride?

Pure-Transformer: O(N²) — bei 1M Tokens unbezahlbar.
Pure-SSM: linear, aber Recall schwächer.

**Hybrid** = beides kombiniert:

- Transformer-Layer für **wichtige Stellen** (Recall, In-Context-Learning)
- SSM-Layer für **Long-Range-Kontext** (linear in N)

```mermaid
flowchart TB
    Input[Input-Tokens] --> Mix[Hybrid-Block]

    Mix --> SSM[Mamba-Layer<br/>O(N) linear]
    Mix --> Attn[Attention-Layer<br/>O(N²) — selektiv]

    SSM --> Concat[Mix-Output]
    Attn --> Concat

    Concat --> Next[Nächste Schicht]

    classDef hybrid fill:#FF6B3D,color:#0E1116
    class SSM,Attn,Concat,Next hybrid
```

### AI21 Jamba 1.5 (Israel, 08.2024)

URL: <https://www.ai21.com/jamba/>

| Variante | Params | Aktiv | Kontext |
|---|---|---|---|
| **Jamba 1.5 Mini** | 52B | 12B (MoE) | **256k Tokens** |
| **Jamba 1.5 Large** | 398B | 94B (MoE) | **256k Tokens** |

**Architektur**: jeder 8. Layer ist Attention, der Rest Mamba — plus MoE.

- Open-Weights (Jamba-1.5-Open-License)
- Multilingual inkl. DE
- DACH-Tauglichkeit: gut

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

modell = AutoModelForCausalLM.from_pretrained(
    "ai21labs/AI21-Jamba-1.5-Mini",
    torch_dtype="bfloat16",
    device_map="auto",
)
tokenizer = AutoTokenizer.from_pretrained("ai21labs/AI21-Jamba-1.5-Mini")

# 256k-Context-Inferenz
inputs = tokenizer(
    sehr_langer_text,  # bis 256k Tokens
    return_tensors="pt",
).to("cuda")
output = modell.generate(**inputs, max_new_tokens=200)
```

> Hauptvorteil 2026: 256k-Context bei **20× weniger Memory** als Transformer-only.

### Hunyuan-TurboS (Tencent, 2024)

- **erstes industrielles Mamba-Transformer-Hybrid**
- 560B Total / 56B aktiv (MoE)
- Stand 04/2026 in Tencent Cloud verfügbar; Open-Weights-Detail prüfen

> ⚠️ **DACH-Compliance**: Hunyuan-Familie hat **EU-Region-Ausschluss bei einigen Lizenzen** (siehe Phase 08.03 für Hunyuan3D). Vor produktivem Einsatz Lizenz-Detail prüfen — community-License oft DACH-tauglich, aber > 100M MAU separat zu lizenzieren.

### Zamba 2 (Zyphra, 2024)

URL: <https://www.zyphra.com/post/zamba-2>

- 2.7B / 7B Hybrid
- Open-Weights, Apache-style
- Forschungs-fokus

### Wann Hybrid statt Standard-LLM?

| Use-Case | Empfehlung |
|---|---|
| Standard-Chat (< 32k) | **Transformer** (Llama, Qwen, Mistral) — Phase 11 |
| Long-Document-RAG (50k–200k) | **Jamba 1.5 Mini** — Hybrid |
| Mega-Context (> 256k) | **Jamba 1.5 Large** oder **DeepSeek-V4** (1M Context, Phase 16) |
| Long-Audio-Transkripte | **Mamba-basiert** (Phase 06) |
| Forschung Hybrid-Architektur | **Zamba 2** |

### DACH-Use-Case-Beispiele

#### Vertrags-Analyse (200-Seiten-PDF)

```python
# Vorher: Document-Splitting + RAG
# Mit Jamba 1.5 Mini:
contract_text = pdf_zu_text("vertrag-200-seiten.pdf")  # ~ 80k Tokens
prompt = f"{contract_text}\n\nFasse die wichtigsten Klauseln zusammen."
# Inferenz in 1 Pass möglich
```

#### Multi-Dokument-Analyse

```python
# 10 Verträge je 30 Seiten = ~ 200k Tokens
all_contracts = "\n\n---\n\n".join([pdf_zu_text(p) for p in vertrag_paths])
# Jamba 1.5 Mini schafft das in einem Pass
```

> Realität: bei 200k-Token-Calls auf Jamba 1.5 Mini (lokal): ~ 60 s Inferenz auf 1× H100. Cloud-Transformer-API würde teuer + viele Round-Trips kosten.

### Inferenz-Stack-Reife (Stand 04/2026)

| Stack | Jamba 1.5 Support | Mamba-Support |
|---|---|---|
| **Transformers (HF)** | ✓ direkt | ✓ via mamba-ssm |
| **vLLM** | ⚠️ in Arbeit | nicht eindeutig belegbar |
| **SGLang** | ⚠️ unklar | nicht eindeutig belegbar |
| **llama.cpp** | nein | nein |

> Stand 04/2026: Jamba 1.5 läuft am besten direkt mit Transformers. vLLM-Integration in Arbeit — vor Production-Einsatz Live-Check.

### Compute-Realität

Bei Jamba 1.5 Mini (52B / 12B aktiv) mit 100k-Context:

| GPU | Inferenz-Zeit | Memory |
|---|---|---|
| 1× H100 (80 GB) | ~ 30–60 s | ~ 70 GB |
| 1× H200 (141 GB) | ~ 30–50 s | ~ 70 GB (mehr Headroom) |
| 2× H100 mit TP | ~ 20–30 s | je 40 GB |

### Anti-Pattern

- ❌ Jamba für 4k-Token-Chats nutzen — unnötig overengineered
- ❌ Pure-Mamba für In-Context-Learning — schwächer als Transformer
- ❌ Hunyuan-TurboS in DACH-Production ohne Lizenz-Detail-Check

## Hands-on

1. Jamba 1.5 Mini lokal mit Transformers (braucht ~ 70 GB VRAM für 100k-Context)
2. Long-Document-Test: 50-Seiten-PDF in 1 Pass analysieren
3. Vergleich gegen Transformer (Llama 3.3 70B mit 32k-Window) — qualitativ
4. Optional: Zamba 2 für Forschungs-Vergleich

## Selbstcheck

- [ ] Du erklärst Hybrid-Architektur (Transformer + Mamba).
- [ ] Du nutzt Jamba 1.5 für Long-Context-Tasks > 100k.
- [ ] Du kennst die EU-Lizenz-Caveats für Hunyuan-Familie.
- [ ] Du wählst Hybrid vs. Transformer je nach Context-Länge.

## Compliance-Anker

- **AI-Act Art. 15**: Hybrid-Architekturen haben weniger Eval-Reife — Robustness-Tests pflicht
- **Lizenz**: Jamba 1.5 Open-License + Hunyuan Community License im Detail prüfen

## Quellen

- Jamba 1.5 — <https://www.ai21.com/jamba/>
- Jamba 1.5 Tech-Report — <https://arxiv.org/abs/2408.12570>
- Hunyuan-TurboS — <https://huggingface.co/tencent/Hunyuan-TurboS>
- Zamba 2 — <https://www.zyphra.com/post/zamba-2>
- Mamba-2 / SSD — <https://arxiv.org/abs/2405.21060>

## Weiterführend

→ Lektion **09.03** (Long-Context-Eval + Use-Cases in DACH)
→ Phase **16** (DeepSeek-V4 als 1M-Context-Alternative)
→ Phase **13** (RAG für Long-Context-Strategien)
