---
id: 19
titel: Abschlussprojekte — 5 echte DACH-Capstones
dauer_stunden: 40
schwierigkeit: experte
stand: 2026-04-29
lernziele:
  - Ein vollständiges produktreifes Projekt mit DACH-Bezug bauen
  - Phasen 11/13/14/17/18/20 zusammenführen
  - DSFA, AI-Act-Klassifikation, AVV-Disziplin praktisch anwenden
  - Portfolio-Stück, das du Arbeitgebern oder Kunden zeigen kannst
---

# Phase 19 · Abschlussprojekte — 5 echte DACH-Capstones

> **Stop building toy projects.** — wähle einen echten Use-Case mit DACH-Bezug, baue ihn End-to-End, dokumentiere ihn AI-Act-konform.

**Status**: 🚧 1 von 5 Capstones voll ausgearbeitet (19.A) · weitere folgen iterativ.

## 🎯 Was du in diesem Modul baust

Wähle 1 aus 5 Capstones. Jeder 8–15 h, jeweils mit eigener `compliance.md`, AI-Act-Klassifikation, DSFA-Light, lauffähigem Code-Skelett.

## Capstones-Übersicht

| # | Capstone | Status | Schwierigkeit | Phasen-Bezug |
|---|---|---|---|---|
| 19.A | **WP-Plugin-Helfer-RAG** | ✅ ausgearbeitet | experte | 11/13/14/17/18/20 |
| 19.B | DSGVO-Compliance-Checker | ⏳ Skelett | mittel | 11/13/20 |
| 19.C | Charity-Adoptions-Bot | ⏳ Skelett | fortgeschritten | 11/13/14/17/20 |
| 19.D | Aktiengesetz-Rechtsfrage-Beantworter | ⏳ Skelett | experte | 13/16/20 |
| 19.E | Mehrsprachiger Voice-Agent | ⏳ Skelett | experte | 06/14/17 |

## 19.A — WP-Plugin-Helfer-RAG ✅

**Ziel**: Multilinguales Plugin-Doku-RAG mit Code-Search + Issue-Triage + PR-Vorschlägen.

**Stack**: Pydantic AI + Qdrant + WP-REST-API + tree-sitter-php

**Verzeichnis**: [`projekte/19-A-wp-plugin-helfer-rag/`](../../projekte/19-A-wp-plugin-helfer-rag/)

**Kern-Idee**: drei Sub-Agents (Doku / Code / Issue) hinter einem Supervisor. Real-World-Use-Case für Saskias citelayer®-Plugin-Familie (oder beliebige WP-Plugin-Familie).

→ [Capstone 19.A README](../../projekte/19-A-wp-plugin-helfer-rag/README.md)

## 19.B — DSGVO-Compliance-Checker ⏳

**Ziel**: Webseiten-Crawler analysiert Cookie-Banner, AVV-Links, Tracker → DSFA-Light-Bericht.

**Stack**: Playwright + Pydantic AI + Mistral oder Pharia-1

**Compliance-Bezug**: AI-Act + DSGVO + TTDSG

**Status**: Skelett mit `compliance.md` angelegt — Inhalt folgt Q3/Q4 2026.

## 19.C — Charity-Adoptions-Bot ⏳

**Ziel**: End-to-End-Voice-Chatbot: Adoptionsprozess, Termine buchen, Tierprofile.

**Stack**: Pharia/Mistral + Whisper + Coqui-TTS + LangGraph (HITL)

**Compliance-Bezug**: vollständige DSGVO-Pipeline (siehe Phase 14.09 als Bauanleitung)

**Status**: Pattern in Phase 14.09 dokumentiert; Capstone-Skelett angelegt — vollständige Implementation Q3 2026.

## 19.D — Aktiengesetz-Rechtsfrage-Beantworter ⏳

**Ziel**: Legal-RAG auf AktG + GermanLegal-Korpus mit Aleph Alpha Pharia, mit Quellen-Attribution + Disclaimer.

**Stack**: Pharia-1 + Qdrant + LangGraph + Phoenix

**Compliance-Bezug**: AI-Act Art. 50.4 (Quellen-Attribution), § RDG-Disclaimer, BAFA-zertifiziertes Modell

**Status**: Skelett angelegt — Hands-on-Aufbau mit Phasen 13 + 16 + 20.

## 19.E — Mehrsprachiger Voice-Agent ⏳

**Ziel**: DeepL + Whisper + Sesame-Pipeline für DE↔EN↔TR Live-Übersetzung mit Kontext-Memory.

**Stack**: Whisper + DeepL + LangGraph + Pharia/Mistral

**Compliance-Bezug**: DSGVO Art. 25 (Privacy by Design für Voice-Daten), Speech-to-Text-Audit-Pipeline

**Status**: Skelett angelegt — Phase 06 (Audio) als Voraussetzung.

## ⚖️ DACH-Compliance-Anker (alle Capstones)

→ [`compliance.md`](compliance.md): Pflicht-Pattern für jedes Capstone.

Pro Capstone:

- **AI-Act-Klassifizierung** (Phase 20.01)
- **DSFA-Light** (Phase 20.03)
- **AVV mit allen Cloud-Providern** (Phase 20.02)
- **Audit-Logging** mit Phoenix (Phase 17.08)
- **Bias-Audit** auf 30 Test-Probes (Phase 18.02)
- **Konformitätserklärung** als YAML (Phase 18.10)

## Lerneffekt

Capstones führen die **alle** vorherigen Phasen praktisch zusammen:

```mermaid
flowchart TB
    P11[Phase 11<br/>LLM-Engineering] --> Cap[Capstone]
    P13[Phase 13<br/>RAG] --> Cap
    P14[Phase 14<br/>Agenten + MCP] --> Cap
    P17[Phase 17<br/>Production EU] --> Cap
    P18[Phase 18<br/>Bias + Safety] --> Cap
    P20[Phase 20<br/>Recht & Governance] --> Cap

    Cap --> Port[Portfolio-Stück<br/>+ AI-Act-Doku]

    classDef phase fill:#FF6B3D,color:#0E1116
    classDef cap fill:#3D8BFF,color:#FFF
    class P11,P13,P14,P17,P18,P20 phase
    class Cap,Port cap
```

## 🔄 Wartung

Stand: 29.04.2026 · Reviewer: Saskia Teichmann ([@s-a-s-k-i-a](https://github.com/s-a-s-k-i-a)) · Nächster Review: 07/2026 (weitere Capstones 19.B–19.E iterativ ausarbeiten).
