---
id: 10
titel: LLM von Null — nanochat, litgpt, llm.c, Pretrain-Realitäts-Check
dauer_stunden: 12
schwierigkeit: fortgeschritten
stand: 2026-04-29
lernziele:
  - Pretraining-Frameworks 2026 (nanoGPT deprecated → nanochat, litgpt, llm.c)
  - Tokenizer-Training mit SentencePiece + HF tokenizers für DE-Korpus
  - DE-Pretraining-Daten (Aleph-Alpha-GermanWeb, FineWeb-2, OSCAR-2301)
  - Hands-on GPT-2-124M-Mini-Pretrain auf RTX 4090
  - Realitäts-Check: 99 % der Use-Cases brauchen LoRA-Finetune (Phase 12) statt Pretrain
---

# Phase 10 · LLM von Null

> **Stop pretending LLMs are magic.** — Karpathy hat nanoGPT im Nov 2025 deprecated. Nachfolger: **nanochat** (GPT-2-Grade in 3 h auf 8×H100 für ~ $ 73). Aber **99 % der DACH-Use-Cases brauchen kein Pretrain** — LoRA-Finetune (Phase 12) reicht. Diese Phase ist Lehre + Forschung.

**Status**: ✅ vollständig ausgearbeitet · **Dauer**: ~ 12 h · **Schwierigkeit**: fortgeschritten

## 🎯 Was du in diesem Modul lernst

- **Pretraining-Frameworks 2026**: nanoGPT deprecated → nanochat (Karpathy), litgpt (Lightning), llm.c
- **Tokenizer-Training**: SentencePiece + HF tokenizers, Komposita-Effizienz
- **DE-Pretraining-Daten**: Aleph-Alpha-GermanWeb (628B Wörter), FineWeb-2 DE, OSCAR-2301 — Lizenz-Disziplin pflicht
- **Compute-Realität**: Chinchilla-Formel, 1.5B × 50B Tokens ≈ ~ € 760 auf Scaleway
- **Hands-on**: GPT-2-124M-Mini-Pretrain auf RTX 4090 in ~ 4-8 h
- **Realitäts-Check**: wann Pretrain wirklich nötig (selten!)

## 📚 Inhalts-Übersicht

| Lektion | Titel | Datei |
|---|---|---|
| 10.01 | Pretraining-Frameworks 2026 | [`lektionen/01-frameworks.md`](lektionen/01-frameworks.md) ✅ |
| 10.02 | Tokenizer-Training für DE-Korpus | [`lektionen/02-tokenizer-training.md`](lektionen/02-tokenizer-training.md) ✅ |
| 10.03 | DE-Pretraining-Daten + Lizenz-Disziplin | [`lektionen/03-pretraining-daten-de.md`](lektionen/03-pretraining-daten-de.md) ✅ |
| 10.04 | **Hands-on**: GPT-2-124M-Mini-Pretrain auf RTX 4090 | [`lektionen/04-hands-on-mini-pretrain.md`](lektionen/04-hands-on-mini-pretrain.md) ✅ |

## 💻 Hands-on-Projekt

**Pretrain-Kalkulator**: Marimo-Notebook mit Chinchilla-Formel + Cost-Schätzung für verschiedene Modell-Größen (124M / 1.5B / 7B / 70B). Plus „Wann Pretrain — wann nicht"-Tabelle.

```bash
uv run marimo edit phasen/10-llm-von-null/code/01_pretrain_kalkulator.py
```

## 🧱 Pretraining-Wahl 2026 (Faustregel)

| Use-Case | Empfehlung |
|---|---|
| **Lehre / Verständnis** | **nanochat** auf 1× H100 oder GPT-2-124M auf RTX 4090 |
| **DACH-Sovereignty (1.5B+)** | **litgpt** auf 8× H100 + Aleph-Alpha-GermanWeb |
| **Standard-Mittelstand-Use-Case** | **NICHT pretrain** — LoRA-Finetune (Phase 12) statt |
| **Custom-Architektur-Forschung** | **llm.c** für volle Kontrolle |
| **100B+-Modelle** | Megatron-LM (NVIDIA) — nicht für DACH-Mittelstand |

## ⚖️ DACH-Compliance-Anker

→ [`compliance.md`](compliance.md): UrhG § 44b (TDM-Opt-out für eigene Crawls), AI-Act Art. 10 (Daten-Governance + Filter-Pipeline), AI-Act Art. 12 (Reproduzierbarkeits-Manifest).

## 🔄 Wartung

Stand: 29.04.2026 · Reviewer: Saskia Teichmann ([@s-a-s-k-i-a](https://github.com/s-a-s-k-i-a)) · Nächster Review: 07/2026 (nanochat-Updates, FineWeb-3-Veröffentlichung erwartet, neue DACH-Pretraining-Tutorials).
