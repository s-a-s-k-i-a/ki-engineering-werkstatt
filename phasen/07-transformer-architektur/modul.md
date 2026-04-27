---
id: 7
titel: Transformer-Architektur — Attention, RoPE, GQA, KV-Cache
dauer_stunden: 12
schwierigkeit: mittel
stand: 2026-04-27
lernziele:
  - Self-Attention von Hand (Q, K, V, Softmax-Skalierung) bauen
  - RoPE/ALiBi/Yarn für lange Kontexte verstehen
  - KV-Cache und PagedAttention erklären (warum 80% der Inference-Kosten)
  - FlashAttention-3 Memory-Hierarchie intuitiv erfassen
  - Encoder vs. Decoder vs. Encoder-Decoder — wann was
---

# Transformer-Architektur

> Stop treating Transformer as a black box. — 100 Zeilen PyTorch reichen, um zu verstehen, was passiert.

Schwerpunkt: 2026-Standard (GQA, RoPE, Flash-Attention-3, KV-Cache als first-class). Verbindet sich mit Phase 05 (Tokenizer) und Phase 10 (LLM von Null).

## Inhalts-Übersicht

| Lektion | Titel |
|---|---|
| 07.01 | Self-Attention von Hand (Q, K, V) |
| 07.02 | Multi-Head und Group-Query-Attention |
| 07.03 | Positional Encodings: RoPE, ALiBi, Yarn |
| 07.04 | KV-Cache-Mechanik |
| 07.05 | PagedAttention (vLLM) — Speicher-Magie |
| 07.06 | FlashAttention-3 (Memory-Hierarchie) |
| 07.07 | Encoder vs. Decoder vs. Encoder-Decoder |
| 07.08 | Hands-on: nano-GPT-Block mit RoPE auf 1MB Wikitext-DE |

## Status

🚧 Im Aufbau.
