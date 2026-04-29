---
id: 09
titel: State-Space & Hybride — Mamba, Jamba 1.5, Hunyuan-TurboS
dauer_stunden: 6
schwierigkeit: fortgeschritten
stand: 2026-04-29
lernziele:
  - State-Space-Modelle (Mamba) als linear-time-Alternative zu Transformers
  - Hybrid-Architekturen (Jamba 1.5, Hunyuan-TurboS) für Long-Context
  - Long-Context-Eval (NIAH, RULER) — behauptet vs. effektiv
  - Wann Long-Context, wann RAG (Phase 13)
---

# Phase 09 · State-Space & Hybride

> **Stop trusting context-length claims.** — Llama 3.3 behauptet 128k, RULER zeigt ~ 32k effektiv. **Hybride** (Jamba 1.5, Hunyuan-TurboS) sind 2026 die produktive Antwort für Long-Context bei vernünftiger Memory.

**Status**: ✅ vollständig ausgearbeitet · **Dauer**: ~ 6 h · **Schwierigkeit**: fortgeschritten

## 🎯 Was du in diesem Modul lernst

- **State-Space-Modelle**: Mamba + Mamba-2 als O(N)-Alternative zu Transformer-O(N²)
- **Hybrid-Modelle**: Jamba 1.5 (AI21, Israel) + Hunyuan-TurboS (Tencent) für Long-Context
- **Long-Context-Eval**: NIAH, RULER, ZeroSCROLLS — Pflicht-Tests vor Production
- **Wann Long-Context, wann RAG**: 30–100× Cost-Differenz beachten

## 📚 Inhalts-Übersicht

| Lektion | Titel | Datei |
|---|---|---|
| 09.01 | State-Space-Modelle — Mamba, Mamba-2 | [`lektionen/01-mamba-state-space.md`](lektionen/01-mamba-state-space.md) ✅ |
| 09.02 | Hybrid-Modelle — Jamba 1.5, Hunyuan-TurboS | [`lektionen/02-hybrid-modelle.md`](lektionen/02-hybrid-modelle.md) ✅ |
| 09.03 | Long-Context-Eval — NIAH, RULER | [`lektionen/03-long-context-eval.md`](lektionen/03-long-context-eval.md) ✅ |

## 💻 Hands-on-Projekt

**Long-Context-Kalkulator**: Marimo-Notebook, das je nach Token-Volumen + Frequenz den richtigen Ansatz empfiehlt (Standard-LLM / RAG / Long-Context-Hybrid).

```bash
uv run marimo edit phasen/09-state-space-und-hybride/code/01_long_context_kalkulator.py
```

## 🧱 Long-Context-Wahl 2026 (Faustregel)

| Use-Case | Empfehlung |
|---|---|
| < 32k Tokens, Standard-Chat | Phase 11 (Standard-LLM) |
| 32k–200k, **wiederkehrend** | **RAG** (Phase 13) — 30–100× günstiger |
| 32k–200k, einmalig | Jamba 1.5 Mini (Hybrid) oder Opus 4.7 |
| > 200k, Long-Single-Doc | Jamba 1.5 Large oder DeepSeek-V4 (1M, ⚠️ CN-API) |
| Audio / sehr lange Sequenzen | Mamba-basiert (Phase 06) |

## ⚖️ DACH-Compliance-Anker

→ [`compliance.md`](compliance.md): AI-Act Art. 13 (Cost-Transparenz für Long-Context-Calls), AI-Act Art. 15 (Eval-Pflicht — NIAH/RULER vor Production), Hunyuan-Familie EU-Lizenz-Caveats.

## 🔄 Wartung

Stand: 29.04.2026 · Reviewer: Saskia Teichmann ([@s-a-s-k-i-a](https://github.com/s-a-s-k-i-a)) · Nächster Review: 07/2026 (Mamba-3, Jamba 2 erwartet, RULER-Updates für neue Modelle).
