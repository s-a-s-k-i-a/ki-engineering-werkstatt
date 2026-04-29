---
id: 07.03
titel: KV-Cache, FlashAttention-3/4 und vLLM PagedAttention
phase: 07-transformer-architektur
dauer_minuten: 90
schwierigkeit: mittel
stand: 2026-04-29
voraussetzungen: [07.02]
lernziele:
  - KV-Cache als Speicher-Hauptkostenfaktor der LLM-Inferenz verstehen
  - FlashAttention-3 (H100) vs. FlashAttention-4 (B200) einordnen
  - vLLM V1 mit PagedAttention + Chunked Prefill als 2026-Inference-Standard
  - Prefill-Phase vs. Decode-Phase unterscheiden — und warum das für Production wichtig ist
compliance_anker:
  - inference-eu-hosting
ai_act_artikel:
  - art-15
---

## Worum es geht

> Stop ignoring the KV-Cache. — Bei LLM-Inferenz ist der **KV-Cache** typischerweise **80 % des VRAM-Verbrauchs** und **80 % der Kosten** — nicht das Modell selbst. Wer KV-Cache versteht, versteht warum vLLM, SGLang und PagedAttention existieren, und warum FlashAttention so wichtig ist.

Diese Lektion zerlegt die Inference-Optimierungen, die 2026 Produktions-Stack ausmachen.

## Voraussetzungen

- Lektion 07.02 (Multi-Head + GQA)

## Konzept

### Schritt 1: Prefill vs. Decode

LLM-Inferenz besteht aus **zwei** Phasen mit sehr unterschiedlichen Eigenschaften:

| Phase | Was passiert | Compute |
|---|---|---|
| **Prefill** | gesamten Prompt einmal in Parallel verarbeiten | **compute-bound** (Matrix×Matrix) |
| **Decode** | Token-für-Token autoregressiv generieren | **memory-bound** (KV-Cache lesen) |

**Konsequenz**: bei 4k-Prompt + 200 Output-Tokens ist Prefill ~80 % der Latenz, Decode ~20 % — aber Prefill ist „schnell pro Token", Decode „langsam pro Token". GPU-Auslastung in Decode ist oft < 30 %.

### Schritt 2: KV-Cache — was wird gecacht?

Während autoregressiver Generation muss bei jedem neuen Token die Attention-Berechnung über **alle vorherigen** Tokens erneut laufen. Trick: **K und V der vorherigen Tokens cachen**.

Pro Token, pro Layer, pro KV-Head: ein Vektor mit `d_head` Werten.

**Größe**:

```text
KV-Cache = 2 × n_layers × n_kv_heads × d_head × seq_len × dtype-Bytes
```

**Beispiel Llama 3.3 70B** (n_layers=80, n_kv_heads=8 (GQA), d_head=128, fp16):

```text
Pro Token: 2 × 80 × 8 × 128 × 2 = 327 KB
Bei 8k Tokens: 2.6 GB
Bei 128k Tokens: 41 GB    ← genau deshalb braucht Long-Context fette GPUs
```

Mit Vanilla MHA (32 KV-Heads) wäre das 4× größer: ~ 165 GB für 128k. **GQA reduziert genau diese Kosten**.

### Schritt 3: PagedAttention — vLLM's Innovation

Klassisch wird KV-Cache als **kontinuierlicher Block pro Anfrage** alloziert. Problem: bei dynamischen Sequenz-Längen entsteht **interne Fragmentierung** — viel reservierter, ungenutzter Speicher.

**PagedAttention** (Kwon et al. 2023, vLLM) nutzt das gleiche Prinzip wie Operating-System-Virtual-Memory:

- KV-Cache in **kleine Blöcke** (z.B. 16 Tokens) zerlegt
- Blöcke nicht-kontinuierlich im Speicher
- Pro Anfrage **Seitentabelle** mit Block-Pointern

**Wirkung**: VRAM-Auslastung steigt von ~ 60 % auf ~ 96 %. Bei gleicher Hardware **2-4× mehr concurrent users**.

### Schritt 4: vLLM V1 — der 2026-Inference-Stack

**vLLM V1** (Default seit v0.8.0, Januar 2025) ist 2026 die **Standard-Inference-Engine** für offene Gewichte:

- **PagedAttention** always-on
- **Chunked Prefill** default-on — kombiniert Prefill und Decode in einem Batch (verhindert Decode-Stalls während langer Prefills)
- **FlashAttention-3** integriert
- **Continuous Batching** — neue Anfragen werden ohne Batch-Cycle-Warten eingespeist
- **Speculative Decoding** — kleines Draft-Modell macht Vorschläge, großes verifiziert
- **Multi-LoRA-Inference** (Phase 12)

**Faustregel**: bei eigener LLM-Inference auf > 1k Anfragen/Tag → vLLM. Alternativen: SGLang (etwas schneller bei strukturierten Prompts), TensorRT-LLM (NVIDIA-only, etwas schneller, schwerer zu deployen).

### Schritt 5: FlashAttention-3 vs. FlashAttention-4

**FlashAttention-2** (2023) brachte bereits 2-4× Speedup gegenüber naiver Implementierung durch Fused-Kernels und IO-Awareness.

**FlashAttention-3** (Juli 2024, Dao et al.):

- Optimiert für **H100 Hopper** mit asynchronen Kernels und FP8
- BF16: bis 840 TFLOPs/s (85 % der theoretischen H100-Maximum)
- FP8: bis 1.3 PFLOPs/s

**FlashAttention-4** (2026, Dao-AILab):

- Optimiert für **B200 Blackwell** mit unterschiedlich-skalierender Hardware-Topologie
- BF16: bis 1605 TFLOPs/s auf B200 (71 % Auslastung)
- 1.1-1.3× schneller als cuDNN 9.13, 2.1-2.7× schneller als Triton

**Praxis 2026**:

- H100/H200 → FlashAttention-3 (in vLLM V1, Standard)
- B200/GB200 → FlashAttention-4
- Für eigene Inference: einfach vLLM nehmen, läuft beides automatisch

### Schritt 6: KV-Cache-Compression — die nächste Front

Aktive Forschung 2026 (zur Kenntnis, nicht zur Implementation):

- **Quantization** (KV-Cache in 4-bit oder 8-bit speichern)
- **Eviction Policies** (alte Tokens kicken)
- **MLA / Multi-Head Latent Attention** (DeepSeek, kompakter als GQA)

**Relevanz für DACH-Praxis 2026**: meist über vLLM-Konfigurations-Flags abrufbar — **nicht** selbst implementieren.

## Code-Walkthrough — KV-Cache-Berechnung

```python
def kv_cache_groesse_gb(
    n_layers: int,
    n_kv_heads: int,
    d_head: int,
    seq_len: int,
    dtype_bytes: int = 2,  # fp16/bf16
) -> float:
    """KV-Cache in GB."""
    bytes_total = 2 * n_layers * n_kv_heads * d_head * seq_len * dtype_bytes
    return bytes_total / (1024 ** 3)


# Llama 3.3 70B mit GQA (n_kv_heads = 8)
print(kv_cache_groesse_gb(80, 8, 128, 8_000))     # ≈ 2.4 GB
print(kv_cache_groesse_gb(80, 8, 128, 128_000))   # ≈ 39 GB

# Llama 70B *ohne* GQA (n_kv_heads = 64)
print(kv_cache_groesse_gb(80, 64, 128, 128_000))  # ≈ 312 GB  → unmöglich auf 1 GPU
```

## Hands-on

→ [`code/01_attention_und_kv_cache.py`](../code/01_attention_und_kv_cache.py)

Marimo-Notebook: KV-Cache-Kalkulator für 6 populäre Modelle (Llama 3.3, Mistral Large 3, Qwen3, Pharia, GPT-OSS, DeepSeek-V4) auf 5 typische Sequenz-Längen, plus VRAM-Bedarf-Vergleich GPU-Klasse.

## Selbstcheck

- [ ] Welche zwei Inference-Phasen gibt es, und wo liegt der Bottleneck jeweils?
- [ ] Warum hat ein 70B-Modell **mit** GQA 4-8× kleineren KV-Cache als ohne?
- [ ] Was macht PagedAttention konzeptuell?
- [ ] Welche FlashAttention-Version auf H100 vs. B200?

## Compliance-Anker

- **AI-Act Art. 15** (Robustness): KV-Cache-Eviction-Policies können Antworten unvorhersehbar machen — bei Hochrisiko-Systemen dokumentieren.
- **EU-Hosting**: vLLM auf STACKIT (BSI C5 Type 2), IONOS, OVH, Scaleway = DSGVO-konformer Inference-Stack. Phase 17 zeigt End-to-End-Setup.

→ [`compliance.md`](../compliance.md)

## Quellen

- Kwon et al. (2023): „Efficient Memory Management for Large Language Model Serving with PagedAttention" (vLLM-Paper) — <https://arxiv.org/abs/2309.06180>
- Dao et al. (2024): „FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision" — <https://arxiv.org/abs/2407.08608>
- vLLM V1 Documentation — <https://docs.vllm.ai/en/latest/>
- Dao-AILab (Flash-Attention Repository) — <https://github.com/Dao-AILab/flash-attention>
- Xiao et al. (2024): „Efficient Streaming LLMs" (StreamingLLM, Attention-Sinks) — <https://arxiv.org/abs/2309.17453>

## Weiterführend

- Phase 09 (Long-Context-Eval): wie sich behauptete vs. effektive Context-Länge bemerkbar macht
- Phase 10 (LLM von Null): nano-GPT mit KV-Cache
- Phase 17 (Production): vLLM-Deployment auf STACKIT/IONOS/OVH
