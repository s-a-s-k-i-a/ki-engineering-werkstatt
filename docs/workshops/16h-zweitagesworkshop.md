# 16-h-Zweitagesworkshop „AI Engineering DACH End-to-End"

> Zwei Tage à 8 Stunden. Vollständiger AI-Engineering-Stack für DACH-2026 — von Mathe-Crash über Transformer-Internals bis Production-Deployment auf EU-Cloud mit AI-Act-Konformitätserklärung. Teilnehmende verlassen den Workshop mit einem **Production-tauglichen Mini-Capstone** + einem realistischen Verständnis, was Foundation-Modelle 2026 leisten und wo ihre Grenzen liegen.

## Zielgruppe

- KI-Engineers / ML-Engineers, die einen DACH-spezifischen Stack lernen wollen
- Backend-Devs mit 2+ Jahren Erfahrung, die in eine senior ML-Rolle wechseln
- Quereinsteiger:innen aus angrenzenden Bereichen (Data Engineering, DevOps, Cloud-Architektur)
- Lehrende an Hochschulen, die ein Modul „Angewandtes AI Engineering" konzipieren

## Voraussetzungen

### Vorwissen

- Python (Decorators, async, Type-Hints, Dataclasses oder Pydantic)
- Lineare Algebra auf Schul-Niveau (Vektoren, Matrizen, Skalarprodukt)
- Wahrscheinlichkeit auf Schul-Niveau (P, bedingte W., Mittelwert)
- Docker / Docker-Compose Grundlagen
- Optional: PyTorch-Hello-World schon mal gesehen

### Setup vor Tag 1

```bash
gh repo clone s-a-s-k-i-a/ki-engineering-werkstatt
cd ki-engineering-werkstatt
just setup           # uv sync + pre-commit install
just smoke           # alle Tests grün?
docker compose pull  # für Tag 2: Qdrant + LiteLLM + Phoenix
```

Plus:

- **EU-API-Keys**: Mistral + Aleph Alpha (Pflicht), Anthropic / OpenAI mit AVV (optional)
- **GPU-Zugang** für Tag 2: lokal RTX 3090+ (24 GB VRAM), oder ein vorbereiteter Hetzner-/Scaleway-/STACKIT-Demo-Account
- **Beispiel-Use-Case**: jede:r bringt einen eigenen Production-Kandidaten mit (z. B. Vertrags-Q&A, Issue-Triage, Mandanten-Bot, Wartungs-Doku-Suche)

### Hardware

- 32+ GB RAM (Apple Silicon ab M2 Pro, oder x86_64 + 32 GB)
- 50+ GB freier Speicher (Modell-Cache + Docker-Volumes)
- Stabiles Internet (≥ 50 Mbit/s — HuggingFace + EU-API-Calls + Live-Demo-Streams)

## Lernergebnisse

Nach den zwei Tagen können Teilnehmende:

- **Transformer-Internals** erklären (Self-Attention, GQA, RoPE, KV-Cache) und kritisch einordnen
- **PyTorch 2.7** mit MLflow 3 für reproduzierbares Training nutzen
- **Klassisches ML vs. Deep Learning** anhand von Daten-Größe + -Typ entscheiden
- **LoRA / QLoRA** mit Unsloth oder axolotl auf 24-GB-GPU ausführen
- **RAG vollständig** bauen (Vanilla + Hybrid + GraphRAG-Light) mit deutschen Korpora
- **Multi-Agent-Workflows** mit Pydantic AI + LangGraph + MCP entwerfen
- **Production-Deployment** auf EU-Cloud (vLLM + LiteLLM + Phoenix + Langfuse) konfigurieren
- **Bias-Audit + Self-Censorship-Audit** durchführen
- **AI-Act-Anhang-IV-Konformitätserklärung** + DSFA + AVV-Vertrag erstellen
- Den **eigenen Use-Case** als Mini-Capstone bis zum Workshop-Ende live demoen

## Tag 1 — Foundation + Tooling (8 × 45 min)

### 09:00–09:30 · Welcome + Markt-Realität (Phase 00)

- Anti-Marketing + Bitkom / KfW / VDMA-Zahlen
- DACH-Anbieter-Landschaft (post-Cohere-Aleph-Alpha-Merger)
- Hardware-Hierarchie (H100 / H200 / B200) + EU-Cloud-Optionen
- **Diskussion (15 min)**: jede:r teilt den eigenen Use-Case + Compliance-Klasse

### 09:30–10:30 · Mathe-Crash (Phase 01)

- Vektoren + Embeddings + Kosinus-Ähnlichkeit
- Cross-Entropy / KL-Divergenz / Perplexität — das Trainings-Trio
- Gradient Descent + AdamW als 2026-Standard
- **Hands-on**: [`phasen/01-mathematik-grundlagen/code/01_embedding_explorer.py`](../../phasen/01-mathematik-grundlagen/code/01_embedding_explorer.py)

### 10:30–10:45 · Pause ☕

### 10:45–12:00 · Klassisches ML + PyTorch-Bausteine (Phase 02 + 03)

- Wann Boosting (XGBoost / LightGBM) statt LLM (Phase 02.02)
- SHAP für AI-Act-Erklärbarkeit (Phase 02.03)
- PyTorch 2.7: Tensors / Autograd / nn.Module / torch.compile (Phase 03.01)
- BF16 + Gradient Accumulation + Cosine-Schedule (Phase 03.03)
- **Hands-on**: Permutation-Importance auf synthetischem Bonitäts-Dataset

### 12:00–13:00 · Mittagspause 🍽

### 13:00–14:30 · Tokenizer + Embeddings + Transformer-Architektur (Phase 05 + 07)

- Deutsche Tokenizer-Effizienz: Pharia / Mistral / Llama / Qwen vs. GPT-5.5
- Embedding-Modelle: bge-m3 / mistral-embed / Aleph-Alpha-luminous
- Self-Attention von Hand: Q / K / V / Softmax-Skalierung (Phase 07.01)
- Multi-Head + GQA + RoPE + Yarn (Phase 07.02)
- KV-Cache + FlashAttention-3 / -4 + vLLM PagedAttention (Phase 07.03)
- **Hands-on**: KV-Cache-Kalkulator für eigenen Modell-Plan

### 14:30–14:45 · Pause ☕

### 14:45–16:00 · LLM-Engineering: Pydantic AI + Anbieter (Phase 11)

- Pydantic AI v1.85: Agent / Dependencies / Streaming / Tool-Use
- Anbieter-Showdown (Anthropic / OpenAI / Mistral / Aleph Alpha / DeepSeek / Qwen)
- Cost-Tracking + Caching (Anthropic Prompt-Cache + Redis-Semantic)
- Eval-Strategien: Promptfoo + Ragas + Inspect-AI

### 16:00–17:00 · Finetuning-Crash (Phase 12, light)

- LoRA + QLoRA-Mathematik in 30 min
- Unsloth vs. axolotl: wann was
- **Hands-on (optional, GPU-Zugang)**: kleines LoRA auf deutschem Instruct-Set
- Multi-LoRA-Inference mit vLLM
- Wrap-up Tag 1: Q&A + Hausaufgabe (eigenen Use-Case-Korpus für Tag-2-RAG vorbereiten)

## Tag 2 — Anwendung + Production (8 × 45 min)

### 09:00–10:30 · RAG-Tiefenmodul vollständig (Phase 13)

- Vanilla RAG → Hybrid (BM25 + Dense + RRF) → ColBERT / Late-Interaction → Re-Ranking → GraphRAG → LazyGraphRAG → Agentic RAG
- Tag-2-Hauptprojekt-Anteil: **eigenen Use-Case-Korpus** in Qdrant indexieren
- Ragas-Score-Vergleich: 4 RAG-Varianten auf eigenem Korpus
- Quellen-Attribution-Pflicht (AI-Act Art. 50.4)

### 10:30–10:45 · Pause ☕

### 10:45–12:00 · Agenten + MCP + LangGraph (Phase 14 + 15)

- Single-Agent (Pydantic AI) vs. Supervisor-Pattern (LangGraph)
- MCP-Spec 2025-11-25: was Tools sind, wann ein MCP-Server lohnt
- DSPy für Pipeline-Optimierung (Lektion 14.06)
- Long-Running-Agenten: 4-Schicht-Memory + Postgres-Checkpointer (Phase 15.02)
- HITL-Pattern + AI-Act Art. 14 (Phase 15.01)
- **Hands-on**: eigenen Use-Case als Multi-Agent-Workflow skizzieren

### 12:00–13:00 · Mittagspause 🍽

### 13:00–14:00 · Reasoning + GRPO (Phase 16)

- Reasoning-Modelle 2026: GPT-5.5 Pro / Opus 4.7 / DeepSeek-V4 / R1
- Test-Time-Compute vs. mehr Pretrain-Daten — die 2025-Erkenntnis
- GRPO-Mathematik (R1-Trainings-Referenz, Lektion 16.04)
- RLVR (Verifiable Rewards) für Math / Code / Schema
- **Live-Demo**: Reasoning-Selektor-Notebook für eigenen Use-Case

### 14:00–15:30 · Production-Stack End-to-End (Phase 17)

- vLLM V1 + PagedAttention + Chunked Prefill + Speculative Decoding
- LiteLLM Proxy v1.83.14: Multi-Provider-Gateway, EU-Routing-Switch, Cost-Cap
- Phoenix v14 + Langfuse v3.171: Tracing + Eval + Datasets
- **Hands-on**: kompletter Production-Stack auf eigenem Laptop via Docker-Compose
- BSI-C5-/SecNumCloud-Mapping für eigenes Hosting

### 15:30–15:45 · Pause ☕

### 15:45–16:30 · Ethik + Bias-Audit + Safety (Phase 18)

- Bias-Audit-Pipeline (DIR + Equalized Odds, Lektion 18.02)
- DPO als RLHF-Alternative (Lektion 18.04)
- Self-Censorship-Audit asiatischer Modelle (Lektion 18.08)
- Safety-Frameworks: NeMo Guardrails + Llama Guard 4 (Lektion 18.09)
- **Hands-on**: Bias-Audit auf eigenes RAG-System

### 16:30–17:30 · AI-Act-Konformitätserklärung + Capstone-Demo (Phase 20 + 18.10)

- AI-Act-Anhang-IV-Vorlage durchgehen
- AVV-Mustervertrag für eigenen Use-Case (Phase 20.02)
- DSFA-Vollversion mit Tierheim-Bot als Beispiel (Phase 20.03)
- ai.txt + UrhG-§-44b-TDM-Opt-out (Phase 20.06)
- **Capstone-Demo (10 min pro Teilnehmer:in oder Team)**: jede:r präsentiert den eigenen Mini-Capstone (RAG / Agent / Bias-Audit-Output)
- Wrap-up: Roadmap nach dem Workshop

## Phasen-Mapping (vollständig)

| Tag | Phasen | Lektionen-Auswahl |
|---|---|---|
| Tag 1 | 00, 01, 02, 03, 05, 07, 11, 12 | je 2-4 Kern-Lektionen |
| Tag 2 | 13, 14, 15, 16, 17, 18, 20 | je 2-3 Kern-Lektionen + Capstone |

**Nicht im Workshop** (aus Zeitgründen, in Selbststudium nachzuholen): Phasen 04 (Computer Vision), 06 (Audio), 08 (Generative), 09 (State-Space), 10 (LLM von Null), 19 (Capstones B-E).

## Material-Pakete

### Was Trainer:innen mitbringen

- **Folien-Set Tag 1** (~ 120 Slides): Foundation-Heavy, viele Live-Coding-Slots
- **Folien-Set Tag 2** (~ 100 Slides): Production-Heavy, vorgefertigte Demos
- **Pre-built Docker-Stack**: LiteLLM-Proxy + Qdrant + Phoenix + Langfuse als Compose-File
- **Beispiel-Korpora** für RAG (deutsches Recht, deutscher Maschinenbau, deutsche Wikipedia-Subsets)
- **3 Branchen-Konformitäts-Templates** (Recht, Health, Maschinenbau)
- **Bewertungs-Rubrik** für Capstone-Demos
- **Backup-API-Keys** mit höherem Rate-Limit für ~ 20 Teilnehmende
- **Print-Spickzettel** mit Quellen-URLs (Phasen-Index, AI-Act-Artikel-Map)

### Was Teilnehmende mitnehmen

- Lauffähiger Production-Mini-Stack (Docker-Compose) auf eigenem Laptop
- Eigene RAG-App auf eigenem Use-Case-Korpus
- Multi-Agent-Workflow-Skizze für eigenen Use-Case
- Bias-Audit-Output für eigenes System
- AI-Act-Konformitätserklärung (YAML) + DSFA-Skizze für eigenen Use-Case
- Phoenix-Dashboard-URL mit eigenen Traces
- Lese-Liste für Vertiefung in Phasen 04, 06, 08, 09, 10, 16
- Optional: kostenfreies 90-min-Folge-Coaching nach 4 Wochen

## Trainer:innen-Checkliste

- [ ] Curriculum **vollständig** durchgespielt (alle 21 Phasen smoke-test-grün)
- [ ] Beide Tage **mindestens 1× komplett** geübt mit Stoppuhr
- [ ] Docker-Compose-Stack **belastungsgetestet** (gleichzeitig 20+ User)
- [ ] EU-API-Keys mit höherem Rate-Limit + AVV
- [ ] GPU-Demo-Account (Hetzner / Scaleway / STACKIT) mit gestoppter Kosten-Limit
- [ ] Aktualität der Library-Versionen geprüft (Pydantic AI / vLLM / LiteLLM / Phoenix / Langfuse — Stand < 4 Wochen)
- [ ] AI-Act-Stand geprüft (BNetzA-MIG, GPAI Code of Practice, BSI AIC4)
- [ ] Backup-Internet (LTE-Hotspot, idealerweise 5G)
- [ ] Capstone-Bewertungs-Rubrik finalisiert
- [ ] Folge-Coaching-Termine vor-blockiert

## Erfolgs-Metriken

Erfolgreicher 16-h-Workshop:

- ≥ 80 % der Teilnehmenden haben am Ende des Tag-2-Demos einen lauffähigen Mini-Capstone
- ≥ 90 % können Transformer-Internals (GQA, RoPE, KV-Cache) verbal erklären
- ≥ 70 % haben einen eigenen Bias-Audit-Output
- 100 % haben eine AI-Act-Konformitäts-YAML für ihren Use-Case
- ≥ 60 % haben ein vLLM- oder LiteLLM-Setup mit eigenem EU-API-Key getestet

## Anti-Patterns

- **Nicht** Tag 1 zur Hälfte mit Math-Theorie füllen — die Zielgruppe ist aktions-orientiert
- **Nicht** Phasen 10 (LLM-Pretraining) oder 12 (Vollständiges Finetuning) in voller Tiefe abdecken — das sprengt 2 Tage
- **Nicht** mehr als 2 LLM-Anbieter parallel im Hands-on — Verwirrung
- **Nicht** Capstone-Demo am Ende ausfallen lassen — das ist der Lern-Anker
- **Nicht** ohne stabile GPU-Backup auf On-Prem-Inferenz setzen — Plan B muss EU-Cloud sein

## Optionale Erweiterungen

Wer den 16-h-Workshop liefert, kann Vertiefungs-Tage anschließen:

- **Tag 3 — Computer Vision + Audio** (Phasen 04 + 06): Qwen3-VL, SigLIP-2, Whisper, Voxtral, F5-TTS
- **Tag 3 — Generative Modelle** (Phase 08): FLUX.2 (BFL Freiburg), LTX-2.3, TRELLIS.2, Watermark-Pflicht
- **Tag 3 — LLM von Null** (Phase 10): nanochat, litgpt, Aleph-Alpha-GermanWeb
- **Tag 3 — Capstone-Vertiefung** (Phasen 19.A–E): WP-RAG, DSGVO-Crawler, Charity-Bot, AktG-RAG, Voice-Agent

## Stand

29.04.2026 · 16-h-Format basiert auf Phasen 00 / 01 / 02 / 03 / 05 / 07 / 11 / 12 / 13 / 14 / 15 / 16 / 17 / 18 / 20 · Format-Reviewer: Saskia Teichmann.
