# Roadmap

> Stand: 2026-04-29 · Repo gestartet 2026-04-28. **Alle 21 Phasen + alle 5 Capstones in 2 Tagen ausgearbeitet.** Iteratives Wachstum, keine festen Quartals-Slots — wir bauen, wenn Zeit ist.

## Status-Legende

- ✅ vollständig ausgearbeitet (Lektionen + Code + Übungen + Notebook + Compliance + Smoke-Tests grün)
- 🚧 Skelett vorhanden, in aktiver Entwicklung
- ⏳ Skelett vorhanden, später geplant

## Phasen-Übersicht

| Status | Phase | Titel |
|---|---|---|
| ✅ | 00 | **Werkzeugkasten** — Hardware, uv, Marimo, EU-Cloud |
| ✅ | 01 | **Mathematik-Grundlagen** — Vektoren, Cross-Entropy, KL, Gradient Descent, AdamW |
| ✅ | 02 | **Klassisches ML** — sklearn, XGBoost/LightGBM, SHAP für AI-Act-Hochrisiko |
| ✅ | 03 | **Deep Learning Grundlagen** — PyTorch 2.7, Autograd, MLP/CNN, MLflow 3 |
| ✅ | 04 | **Computer Vision** — Qwen3-VL, SigLIP-2, LightOnOCR, MiniCPM-o, jina-clip-v2 |
| ✅ | 05 | **Deutsche Tokenizer** |
| ✅ | 06 | **Sprache & Audio** — Whisper-large-v3, Voxtral, F5-TTS (CC-BY-NC!), LiveKit, EU-Hosting |
| ✅ | 07 | **Transformer-Architektur** — Self-Attention, GQA, RoPE, KV-Cache, FlashAttention-3/4 |
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

**Bilanz**: 21 ✅ · 0 🚧 · 0 ⏳ — alle Phasen + alle Capstones ausgearbeitet

## Releases

### v0.2.0 — 2026-04-29

Aktueller Release. Enthält Phasen 00, 05, 11, 12, 13, 14, 16, 17, 18, 20 + Capstone 19.A. → [GitHub Release](https://github.com/s-a-s-k-i-a/ki-engineering-werkstatt/releases/tag/v0.2.0)

### v0.3.0 — geplant für nächste Iteration

Bündelt alle Block-A-/B-/C-/D-Phasen (Capstones 19.B–E + Foundation 04/06/08/10 + Mid-Stack 09/15 + Grundlagen 01/02/03/07). release-please erzeugt automatisch.

## Was als nächstes ansteht

Curriculum-Vollausbau ist abgeschlossen — was bleibt sind **Wartung** und **iterative Erweiterungen**.

### Curriculum-Vollausbau abgeschlossen ✅

- [x] **Block A — Capstones 19.A–E** (Real-World-Portfolio) — 2026-04-29
- [x] **Block B — Foundation-Phasen 04/06/08/10** (Quereinsteiger:innen-Lernpfad) — 2026-04-29
- [x] **Block C — Mid-Stack-Phasen 09/15** (State-Space + Autonome Systeme) — 2026-04-29
- [x] **Block D — Grundlagen-Phasen 01/02/03/07** (Mathematik, Klassisches ML, DL, Transformer) — 2026-04-29

## Iterative Erweiterungen (nach Bedarf)

Punkte ohne festen Termin — werden ausgelöst durch externe Trigger oder Saskia-Bedarf:

- [ ] **Issue #9 — Fakten-Check-Pass** (Versionen, URLs, Pricings, Statistiken) vor Stakeholder-Outreach
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
| 2026-04-29 (Tag 2) | Phasen 01, 02, 03, 04, 06, 07, 08, 09, 10, 12, 15, 16, 18 + Capstones 19.A–E + v0.2.0 Release |

**Resultat**: alle 21 Phasen + alle 5 Capstones in 2 Tagen ausgearbeitet. Smoke-Test-Disziplin und Block-by-Block-Commit-Strategie haben das Tempo getragen. Die Geschwindigkeit ist allerdings **nicht garantiert** — Wartungs-Kadenz unten ist die laufende Verpflichtung.

## Wartungs-Kadenz (für fertige Phasen)

- **AI-Act-Tracker**: monatliche Updates bei neuen BSI-/EDPB-/EU-AI-Office-Veröffentlichungen
- **Quellen-Review**: quartalsweise — alle URLs lychee-checken, neue Versionen prüfen
- **Modell-Pricing**: alle 6 Wochen — Anbieter-Pages re-verifizieren (Volatilität bei OpenAI/Anthropic/Mistral)
- **Modul-Stand-Datum**: bei jeder inhaltlichen Änderung
- **Roadmap**: nach jedem Modul-Abschluss

## Mitwirken

Wenn du eine Phase früher haben willst: PR mit konkreter Lektion ist der schnellste Weg. Siehe [`CONTRIBUTING.md`](CONTRIBUTING.md). Issues/Discussions zur Priorisierung sind willkommen — sie verschieben tatsächlich, was als nächstes drankommt.
