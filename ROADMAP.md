# Roadmap

> Stand: 2026-04-29 · Repo gestartet 2026-04-28. **10 von 21 Phasen + 1 Capstone in 2 Tagen ausgearbeitet.** Iteratives Wachstum, keine festen Quartals-Slots — wir bauen, wenn Zeit ist.

## Status-Legende

- ✅ vollständig ausgearbeitet (Lektionen + Code + Übungen + Notebook + Compliance + Smoke-Tests grün)
- 🚧 Skelett vorhanden, in aktiver Entwicklung
- ⏳ Skelett vorhanden, später geplant

## Phasen-Übersicht

| Status | Phase | Titel |
|---|---|---|
| ✅ | 00 | **Werkzeugkasten** — Hardware, uv, Marimo, EU-Cloud |
| ⏳ | 01 | Mathematik-Grundlagen |
| ⏳ | 02 | Klassisches ML |
| ⏳ | 03 | Deep Learning Grundlagen |
| ✅ | 04 | **Computer Vision** — Qwen3-VL, SigLIP-2, LightOnOCR, MiniCPM-o, jina-clip-v2 |
| ✅ | 05 | **Deutsche Tokenizer** |
| ✅ | 06 | **Sprache & Audio** — Whisper-large-v3, Voxtral, F5-TTS (CC-BY-NC!), LiveKit, EU-Hosting |
| ⏳ | 07 | Transformer-Architektur |
| ✅ | 08 | **Generative Modelle** — FLUX.2 (BFL Freiburg!), LTX-2.3, TRELLIS.2, Watermark-Pflicht |
| ✅ | 09 | **State-Space & Hybride** — Mamba, Jamba 1.5, Hunyuan-TurboS, Long-Context-Eval |
| ✅ | 10 | **LLM von Null** — nanochat, litgpt, llm.c, Aleph-Alpha-GermanWeb |
| ✅ | 11 | **LLM-Engineering** — Pydantic AI, MCP, Anbieter-Vergleich |
| ✅ | 12 | **Finetuning & Adapter** — LoRA, QLoRA, Unsloth, axolotl, Multi-LoRA-Inference |
| ✅ | 13 | **RAG-Tiefenmodul** |
| ✅ | 14 | **Agenten & MCP** — Pydantic AI, LangGraph, DSPy, Multi-Agent, MCP |
| ✅ | 15 | **Autonome Systeme** — Autonomie-Stufen, Long-Running-Memory, HITL, AI-Act Art. 14 |
| ✅ | 16 | **Reasoning & Test-Time-Compute** — GPT-5.5, Opus 4.7, DeepSeek-R1, GRPO, RLVR |
| ✅ | 17 | **Production & EU-Hosting** — vLLM, LiteLLM, STACKIT, IONOS, OVH, Phoenix, Langfuse |
| ✅ | 18 | **Ethik, Safety, Alignment** — Bias-Audit, DPO/GRPO, Constitutional AI, Self-Censorship, Anhang IV |
| ✅ | 19 | **Capstones** — 19.A WP-Plugin-Helfer-RAG, 19.B DSGVO-Checker, 19.C Charity-Bot, 19.D AktG-RAG, 19.E Voice-Agent |
| ✅ | 20 | **Recht & Governance** |

**Bilanz**: 17 ✅ · 0 🚧 · 4 ⏳

## Releases

### v0.2.0 — 2026-04-29

Aktueller Release. Enthält Phasen 00, 05, 11, 12, 13, 14, 16, 17, 18, 20 + Capstone 19.A. → [GitHub Release](https://github.com/s-a-s-k-i-a/ki-engineering-werkstatt/releases/tag/v0.2.0)

### v0.3.0 — geplant für nächste Iteration

Wenn alle Capstones (19.B–19.E) und/oder die Foundation-Phasen (10 LLM von Null, 04 Computer Vision, 06 Audio) fertig sind. release-please bündelt automatisch.

## Was als nächstes ansteht

Reihenfolge nach Saskia-Use-Case-Relevanz, nicht nach Phasen-Nummer:

### Capstones (Real-World-Portfolio) — alle ausgearbeitet ✅

- [x] **19.A — WP-Plugin-Helfer-RAG** (Multi-Agent + AST-Splitting + Issue-Triage) — 2026-04-29
- [x] **19.B — DSGVO-Compliance-Checker** (Playwright-Crawler + DSFA-Light-Bericht) — 2026-04-29
- [x] **19.C — Charity-Adoptions-Bot** (LangGraph + HITL + Whisper + F5-TTS) — 2026-04-29
- [x] **19.D — Aktiengesetz-RAG** (Hybrid-RAG + Reasoning + § RDG-Disclaimer) — 2026-04-29
- [x] **19.E — Mehrsprachiger Voice-Agent** (DE↔EN↔TR mit Auto-Lösch-Pipeline) — 2026-04-29

### Foundation-Phasen (für Quereinsteiger:innen-Lernpfad) — alle ausgearbeitet ✅

- [x] **Phase 04 — Computer Vision** (Qwen3-VL, SigLIP-2, LightOnOCR-2-1B, MiniCPM-o) — 2026-04-29
- [x] **Phase 06 — Sprache & Audio** (Whisper-large-v3, Voxtral, F5-TTS, LiveKit) — 2026-04-29
- [x] **Phase 08 — Generative Modelle** (FLUX.2 BFL Freiburg, LTX-2.3, TRELLIS.2) — 2026-04-29
- [x] **Phase 10 — LLM von Null** (nanochat, litgpt, llm.c, Aleph-Alpha-GermanWeb) — 2026-04-29

### Mid-Stack-Phasen

- [ ] **Phase 09 — State-Space & Hybride** (Mamba/Mamba-2, Jamba 1.5, Hunyuan-TurboS)
- [ ] **Phase 15 — Autonome Systeme** (Long-Running-Agents, Selbst-Reflexion, Memory-Architekturen)

### Grundlagen-Phasen (Pflicht für „Quereinsteiger:innen"-Pfad)

- [ ] **Phase 01 — Mathematik** (Lineare Algebra, Wahrscheinlichkeit, Calculus für Deep Learning)
- [ ] **Phase 02 — Klassisches ML** (sklearn, Trees, Boosting, Eval-Metriken)
- [ ] **Phase 03 — Deep Learning Grundlagen** (PyTorch, Backprop, Optimizer)
- [ ] **Phase 07 — Transformer-Architektur** (Attention, Multi-Head, FlashAttention)

## Iterative Erweiterungen (nach Bedarf)

Punkte ohne festen Termin — werden ausgelöst durch externe Trigger oder Saskia-Bedarf:

- [ ] **AI-Act-Tracker** auf neuen BNetzA-KI-MIG-Stand aktualisieren (sobald veröffentlicht)
- [ ] **Logo + Social-Preview** als finale PNG-Renderings (statt SVG-Placeholder)
- [ ] **Echte Marimo-Notebooks** mit aktiven Modell-Aufrufen (heute Stub-Smoke; live-API-Variante als zweites Notebook pro Phase)
- [ ] **Workshop-Material**: 4-/8-/16-h-Format aus den 21 Phasen ableiten
- [ ] **EN-Schwesterrepo** `ki-engineering-werkstatt-en` mit Cross-Linking (wenn Demand)
- [ ] **Mehrsprachige Erweiterung** (FR / IT) — abhängig von Community-Bedarf

## Tatsächliche Entwicklungs-Geschwindigkeit (für Erwartungs-Management)

| Datum | Output |
|---|---|
| 2026-04-28 (Tag 1) | Repo-Setup + Phasen 00, 05, 11, 13, 14, 17, 20 + komplettes Tooling/CI/CD |
| 2026-04-29 (Tag 2) | Phasen 12, 16, 18 + Capstone 19.A + v0.2.0 Release |

Bei diesem Tempo ist das gesamte Curriculum (alle 21 Phasen + alle 5 Capstones) realistisch in **wenigen weiteren Sessions** fertigstellbar. Die Geschwindigkeit ist allerdings **nicht garantiert** — sie hängt davon ab, wann Saskia Zeit hat. Nichts hier hat ein Liefer-Datum.

## Wartungs-Kadenz (für fertige Phasen)

- **AI-Act-Tracker**: monatliche Updates bei neuen BSI-/EDPB-/EU-AI-Office-Veröffentlichungen
- **Quellen-Review**: quartalsweise — alle URLs lychee-checken, neue Versionen prüfen
- **Modell-Pricing**: alle 6 Wochen — Anbieter-Pages re-verifizieren (Volatilität bei OpenAI/Anthropic/Mistral)
- **Modul-Stand-Datum**: bei jeder inhaltlichen Änderung
- **Roadmap**: nach jedem Modul-Abschluss

## Mitwirken

Wenn du eine Phase früher haben willst: PR mit konkreter Lektion ist der schnellste Weg. Siehe [`CONTRIBUTING.md`](CONTRIBUTING.md). Issues/Discussions zur Priorisierung sind willkommen — sie verschieben tatsächlich, was als nächstes drankommt.
