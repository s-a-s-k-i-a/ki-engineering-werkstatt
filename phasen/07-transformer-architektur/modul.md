---
id: 7
titel: Transformer-Architektur — Self-Attention, GQA, RoPE, KV-Cache, FlashAttention
dauer_stunden: 8
schwierigkeit: mittel
stand: 2026-04-29
lernziele:
  - Self-Attention von Hand verstehen (Q, K, V, Softmax-Skalierung)
  - Multi-Head, Group-Query-Attention (GQA) und ihre Kompromisse
  - RoPE als 2026-Position-Encoding-Standard, Yarn für Long-Context
  - KV-Cache als Inference-Hauptkostenfaktor (80 % VRAM)
  - FlashAttention-3 vs. FlashAttention-4, vLLM V1 mit PagedAttention
---

# Phase 07 · Transformer-Architektur

> **Stop treating Transformer as a black box.** — Drei Matrixmultiplikationen + Softmax = Self-Attention. Multi-Head + GQA + RoPE + KV-Cache + FlashAttention-3/4 = state-of-the-art 2026. Schwerpunkt: **was modern ist** (GQA, RoPE, vLLM), nicht was 2018 stand der Lehre war.

**Status**: ✅ vollständig ausgearbeitet · **Dauer**: ~ 8 h · **Schwierigkeit**: mittel

## 🎯 Was du in diesem Modul lernst

- **Self-Attention** mathematisch + in 30 Zeilen PyTorch
- **Multi-Head / MQA / GQA**-Familie und warum GQA dominiert
- **RoPE** + **Yarn** für Position-Encoding und Long-Context
- **KV-Cache**-Mechanik und Sizing
- **FlashAttention-3** (H100) vs. **FlashAttention-4** (B200)
- **vLLM V1** mit PagedAttention + Chunked Prefill als Inference-Stack

## 📚 Inhalts-Übersicht

| Lektion | Titel | Datei |
|---|---|---|
| 07.01 | Self-Attention von Hand — Q, K, V, Softmax-Skalierung | [`lektionen/01-self-attention-von-hand.md`](lektionen/01-self-attention-von-hand.md) ✅ |
| 07.02 | Multi-Head, Group-Query-Attention, RoPE und Yarn | [`lektionen/02-mha-gqa-und-rope.md`](lektionen/02-mha-gqa-und-rope.md) ✅ |
| 07.03 | KV-Cache, FlashAttention-3/4, vLLM PagedAttention | [`lektionen/03-kv-cache-flashattention-vllm.md`](lektionen/03-kv-cache-flashattention-vllm.md) ✅ |

## 💻 Hands-on-Projekt

**KV-Cache-Kalkulator**: berechnet KV-Cache-Größe und Gesamt-VRAM für 6 populäre 2026er-Modelle (Llama 3.3, Mistral Large 3, Qwen3, Pharia, GPT-OSS, DeepSeek-V4) auf 4k/32k/128k Sequenz-Längen, plus GPU-Klasse-Empfehlung.

```bash
uv run marimo edit phasen/07-transformer-architektur/code/01_attention_und_kv_cache.py
```

## 🧱 Faustregeln 2026

| Frage | Antwort |
|---|---|
| Welche Attention-Variante in modernen LLMs? | GQA (alle: Llama, Mistral, Qwen, Pharia, GPT-OSS) |
| Welches Position-Encoding? | RoPE (mit Yarn-Erweiterung für Long-Context) |
| KV-Cache-Größe? | `2 × layers × kv_heads × d_head × seq_len × dtype_bytes` |
| Welcher FlashAttention-Stand? | FA-3 auf H100/H200, FA-4 auf B200 |
| Welcher Inference-Stack? | vLLM V1 (PagedAttention + Chunked Prefill default-on) |
| Encoder-Decoder oder Decoder-only? | Decoder-only ist 2026 LLM-Standard |

## ⚖️ DACH-Compliance-Anker

→ [`compliance.md`](compliance.md): AI-Act Art. 11 (Tech-Doku der Architektur), Art. 15 (Robustness bei KV-Cache-Eviction), DSGVO Art. 44 (EU-Inference-Hosting via STACKIT/IONOS/OVH/Scaleway).

## 🔄 Wartung

Stand: 29.04.2026 · Reviewer: Saskia Teichmann ([@s-a-s-k-i-a](https://github.com/s-a-s-k-i-a)) · Nächster Review: 09/2026 (FlashAttention-4 Integration in vLLM Q3/2026, Blackwell-Optimierungen erwartet).
