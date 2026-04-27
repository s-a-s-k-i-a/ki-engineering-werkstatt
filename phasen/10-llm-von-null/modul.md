---
id: 10
titel: LLM von Null bauen — nano-GPT auf deutschem Korpus
dauer_stunden: 16
schwierigkeit: fortgeschritten
stand: 2026-04-27
lernziele:
  - 50-M-Parameter-LLM von Grund auf bauen, trainieren, samplen
  - Datenpipeline (OSCAR-DE-Subset, Cleaning, BPE-Tokenizer trainieren)
  - Modell-Architektur mit RoPE, GQA, RMSNorm umsetzen
  - Skalierungsgesetze (Chinchilla für Arme: 20 Tokens/Parameter)
  - Quantisierung (GGUF) für lokale Inferenz
---

# LLM von Null

> Stop pretending LLMs are magic. — wer 50M Parameter selbst trainiert hat, versteht den Rest sofort.

Inspiration: Karpathy nano-GPT + Sebastian Raschka „Build a Large Language Model From Scratch" — auf deutschem Korpus.

## Inhalts-Übersicht

| Lektion | Titel |
|---|---|
| 10.01 | Datenpipeline: OSCAR-DE-Subset, Cleaning |
| 10.02 | BPE-Tokenizer trainieren auf 50MB DE-Wikipedia |
| 10.03 | Modell-Architektur: nano-GPT mit RoPE/GQA/RMSNorm |
| 10.04 | Training-Loop: AdamW, Warmup, Cosine, Grad Clipping |
| 10.05 | Skalierungsgesetze (Chinchilla 20:1) |
| 10.06 | Inferenz und Sampling-Strategien |
| 10.07 | Evaluation: Perplexität auf Held-out Wikitext-DE |
| 10.08 | GGUF-Konvertierung für llama.cpp |

## Hauptprojekt (3-4h)

„LLäMmlein-Mini" — 50M-Parameter-Modell auf 50MB deutschem Wikipedia, end-to-end. Generiert plausible deutsche Sätze nach Training.

## Status

🚧 Im Aufbau.
