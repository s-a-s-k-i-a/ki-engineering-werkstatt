---
id: 15
titel: Autonome Systeme — Long-Running-Agents, Memory, HITL, AI-Act Art. 14
dauer_stunden: 8
schwierigkeit: fortgeschritten
stand: 2026-04-29
lernziele:
  - Autonomie-Stufen abgrenzen (L0-L5) — 95 % der Production-Systeme = L2-L3
  - AI-Act Art. 14 + DSGVO Art. 22 als HITL-Pflicht-Pattern
  - Long-Running-Agenten mit 4-Schicht-Memory (Working/Episodic/Semantic/Procedural)
  - LangGraph + Postgres-Checkpointer für persistierten State
  - Right-to-be-Forgotten + Konfidenz-Eskalation
---

# Phase 15 · Autonome Systeme

> **Stop calling everything an "autonomous agent".** — 95 % der „autonomen" Production-Systeme 2026 sind tatsächlich L2-L3 mit klaren HITL-Stellen. Echte L4-Autonomie hat hohe Compliance-Hürden (AI-Act Art. 14, DSGVO Art. 22).

**Status**: ✅ vollständig ausgearbeitet · **Dauer**: ~ 8 h · **Schwierigkeit**: fortgeschritten

## 🎯 Was du in diesem Modul lernst

- **Autonomie-Stufen** (L0-L5): wann L4 erlaubt, wann HITL pflicht
- **AI-Act Art. 14**: Human Oversight als Pflicht-Pattern für Hochrisiko
- **DSGVO Art. 22**: Mensch bei automatisierten Entscheidungen
- **4-Schicht-Memory**: Working / Episodic / Semantic / Procedural
- **LangGraph + Postgres-Checkpointer** für Long-Running-Agenten
- **DSGVO-Memory-Compliance**: Auto-Pruning + Right-to-be-Forgotten
- **Hands-on**: Long-Running-Personal-Assistant mit allen 4 Memory-Schichten

## 📚 Inhalts-Übersicht

| Lektion | Titel | Datei |
|---|---|---|
| 15.01 | Autonom vs. Supervisor — wann welches Pattern | [`lektionen/01-autonome-vs-supervisor.md`](lektionen/01-autonome-vs-supervisor.md) ✅ |
| 15.02 | Long-Running-Agenten — Memory-Architekturen | [`lektionen/02-long-running-memory.md`](lektionen/02-long-running-memory.md) ✅ |
| 15.03 | **Hands-on**: Long-Running-Personal-Assistant | [`lektionen/03-hands-on-long-running.md`](lektionen/03-hands-on-long-running.md) ✅ |

## 💻 Hands-on-Projekt

**Autonomie-Klassifikator**: Marimo-Notebook, das je nach Use-Case-Profil (rechtlich-relevant / Hochrisiko / destruktiv / Cost-Cap-möglich) die empfohlene Autonomie-Stufe + Pflicht-Kontrollen ausgibt.

```bash
uv run marimo edit phasen/15-autonome-systeme/code/01_autonomie_klassifikator.py
```

## 🧱 Autonomie-Wahl 2026 (Faustregel)

| Use-Case | Stufe |
|---|---|
| Recht / Medizin / Finanzen | **STOP** — DSGVO Art. 22 |
| Hochrisiko (Anhang III) | **L2** — Vorschlag + Mensch entscheidet |
| Destruktive Aktionen (git, rm) | **L3** — HITL bei kritisch |
| Reversibel + Cost-Cap | **L4** — autonom |
| Bewerbungs-/Kredit-Entscheidung | STOP — Mensch zwingend |
| Customer-Support-Bot | L2-L3 mit Eskalation |
| Code-Agent (Cursor-Stil) | L3 mit Code-Review |

## ⚖️ DACH-Compliance-Anker

→ [`compliance.md`](compliance.md): AI-Act Art. 14 (Human Oversight), DSGVO Art. 22 (automatisierte Entscheidungen), DSGVO Art. 17 (Right-to-be-Forgotten), DSGVO Art. 25 (Privacy by Design für Memory).

## 🔄 Wartung

Stand: 29.04.2026 · Reviewer: Saskia Teichmann ([@s-a-s-k-i-a](https://github.com/s-a-s-k-i-a)) · Nächster Review: 07/2026 (LangGraph-Memory-Updates, AI-Act-Anhang-III-Konkretisierungen Q3/2026 erwartet).
