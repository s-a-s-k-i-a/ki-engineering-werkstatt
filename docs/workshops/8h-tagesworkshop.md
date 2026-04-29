# 8-h-Tagesworkshop „DACH-konforme LLM-App End-to-End"

> Eintägiger Hands-on-Workshop für **Backend-Entwickler:innen mit Python-Erfahrung**, die eine LLM-Anwendung im DACH-Umfeld bauen sollen. Teilnehmende verlassen den Workshop mit einer **lauffähigen RAG-App** (Retrieval-Augmented Generation), die auf einem **EU-Stack** läuft, **Pydantic-AI-typisiert** ist, **Caching + Cost-Tracking** hat und **AI-Act-konform** dokumentiert ist.

## Zielgruppe

- Backend-Entwickler:innen (Python, 1+ Jahre Berufserfahrung)
- Full-Stack-Engineers, die in eine ML-Rolle wechseln
- Solo-Founder mit Python-Background, die einen Use-Case prototypisieren
- DevOps / SRE, die LLM-Workloads in Production-Pipelines integrieren müssen

## Voraussetzungen

### Vorwissen

- Python (`pip install`, `venv`, Decorators, Type-Hints, async)
- HTTP / REST-APIs (request / response)
- Grundverständnis Vektoren / Embeddings (oder Bereitschaft, das in 30 min zu lernen)
- Optional: Docker-Compose-Grundlagen

### Setup vor dem Workshop

```bash
gh repo clone s-a-s-k-i-a/ki-engineering-werkstatt
cd ki-engineering-werkstatt
just setup           # uv sync + pre-commit install
just smoke           # alle Tests grün?
```

Plus mindestens **einen** der folgenden API-Keys:

- Mistral (EU-Frontend-Default; <https://console.mistral.ai>)
- Aleph Alpha luminous (Heidelberg; <https://app.aleph-alpha.com>)
- Anthropic mit AVV (Münchner-Office-Anker)
- OpenAI mit AVV + EU-Region-Routing

### Hardware

- 16+ GB RAM (Apple Silicon ab M1 / x86_64-Linux / Windows-WSL2)
- ~ 5 GB freier Speicher (Marimo-Notebooks + Modell-Cache)
- Stabiles Internet (≥ 25 Mbit/s — Hugging-Face-Downloads + API-Calls)

## Lernergebnisse

Nach dem Tagesworkshop können Teilnehmende:

- **Pydantic AI** für strukturierte LLM-Outputs einsetzen (Validation, Tool-Use, Streaming)
- **Anbieter-Wahl** treffen mit EU-First-Prinzip + Cost-Tabelle
- **RAG-Pipeline** End-to-End bauen (Chunking → Embedding → Qdrant → Re-Ranking → Generierung)
- **LiteLLM Proxy** als Multi-Provider-Gateway aufsetzen, mit Cost-Cap + EU-Routing
- **Phoenix / Langfuse** für Observability einbinden
- **AI-Act-Anhang-IV-Konformitätserklärung** für ihren Use-Case erstellen

## Agenda (8 × 45 min + Pausen)

### Vormittag — Foundation (4 × 45 min)

#### 09:00–09:30 · Welcome + EU-Cloud-Stack-Auswahl (Phase 00)

- Anti-Marketing + Markt-Realität
- EU-Cloud-Hardware-Matrix: H100 / H200 / B200, on-prem vs. cloud
- STACKIT (BSI C5 Type 2), IONOS AI Model Hub, OVH, Scaleway, Hetzner GPU
- Trade-off: Pricing × Compliance × Latenz

> **Material**: [`phasen/00-werkzeugkasten/lektionen/05-eu-cloud-stack.md`](../../phasen/00-werkzeugkasten/lektionen/05-eu-cloud-stack.md)

#### 09:30–10:15 · Tokenizer-Effizienz auf Deutsch (Phase 05)

- Warum deutsche Texte 30–60 % mehr Tokens brauchen als englische
- Tokenizer-Showdown: GPT-5.5 / Claude / Llama-4 / Pharia / Mistral / Teuken-7B
- **Hands-on**: jede:r misst eigenen Beispiel-Text-Token-Count + EUR-Kosten

> **Notebook**: [`phasen/05-deutsche-tokenizer/code/01_tokenizer_showdown.py`](../../phasen/05-deutsche-tokenizer/code/01_tokenizer_showdown.py)

#### 10:15–10:30 · Pause ☕

#### 10:30–12:00 · Pydantic AI + Anbieter-Vergleich + Caching (Phase 11)

- Pydantic AI v1.85: typisierte Outputs, Tool-Use, Streaming
- **Hands-on**: Hello-World-Pydantic-AI-Agent mit deinem EU-API-Key
- Anbieter-Vergleich: gleicher Prompt, 5 Modelle, Cost + Latency + Output-Qualität
- Caching: Anthropic Prompt-Cache (90 % off), Redis-Semantic-Cache, Qdrant-Semantic
- **Übung**: Cost-Cap (€ 0,10 / Request) implementieren

> **Material**: Phase 11 (Lektionen 02 + 04 + 05 + 07)
> **Notebook**: [`phasen/11-llm-engineering/code/01_anbieter_showdown.py`](../../phasen/11-llm-engineering/code/01_anbieter_showdown.py)

#### 12:00–13:00 · Mittagspause 🍽

### Nachmittag — Anwendung + Production (4 × 45 min)

#### 13:00–14:30 · RAG-Pipeline End-to-End (Phase 13)

- Vanilla RAG (Lektion 13.01) → Hybrid (BM25 + Dense + RRF) (Lektion 13.02) → Re-Ranking (bge-reranker-v2-m3)
- **Hands-on**: deutscher Wikipedia-Subset + Qdrant + Pharia-1-control
- 4 RAG-Varianten testen, Ragas-Score + EUR-Kosten + Latenz vergleichen
- AI-Act Art. 50.4: Quellen-Attribution-Pflicht

> **Notebook**: [`phasen/13-rag-tiefenmodul/code/01_vanilla_rag.py`](../../phasen/13-rag-tiefenmodul/code/01_vanilla_rag.py)

#### 14:30–15:15 · Agenten-Light + MCP (Phase 14)

- Single-Agent vs. Supervisor (Phase 15)
- **Hands-on**: einfacher Pydantic-AI-Agent mit Tool-Use auf eigenem Use-Case
- MCP-Spec: Was ist Model Context Protocol, wann lohnt es sich (kurzer Überblick, Vertiefung in 16-h-Workshop)

> **Material**: Phase 14 Lektionen 01–04

#### 15:15–15:30 · Pause ☕

#### 15:30–16:30 · Production-Stack: vLLM + LiteLLM + Phoenix (Phase 17)

- vLLM V1 mit PagedAttention + Chunked Prefill
- LiteLLM Proxy v1.83.14: Multi-Provider, Cost-Tracking, EU-Routing
- Phoenix v14 + Langfuse v3 für Tracing
- **Hands-on**: LiteLLM-Proxy mit Docker-Compose lokal starten, deinen Pydantic-AI-Agent durch den Proxy schicken
- Audit-Logs als DSGVO-Pflicht

> **Notebook**: [`phasen/17-production-und-eu-hosting/code/`](../../phasen/17-production-und-eu-hosting/)

#### 16:30–17:00 · AI-Act-Konformitätserklärung + DSFA für deinen Use-Case (Phase 20 + 18)

- **Hands-on**: jede:r erstellt für ihren Tagesprojekt-Use-Case eine Konformitäts-YAML (Phase 18.10)
- DSFA-Light-Template ausfüllen
- AI-Act-Klassifikator-CLI laufen lassen
- Wrap-up: was bei eigenem Use-Case noch fehlt, Lese-Liste für Vertiefung

> **Material**: [`werkzeuge/ai_act_classifier.py`](../../werkzeuge/ai_act_classifier.py), [`docs/rechtliche-perspektive/dsgvo-checklisten.md`](../rechtliche-perspektive/dsgvo-checklisten.md)

## Phasen-Mapping

| Tagesabschnitt | Phasen | Lektionen |
|---|---|---|
| Vormittag | 00, 05, 11 | 00.05, 05.01, 11.02, 11.04, 11.05, 11.07 |
| Nachmittag | 13, 14, 17, 18, 20 | 13.01–13.04, 14.01–14.04, 17.04–17.09, 18.10, 20.01 |

**Nicht abgedeckt** im 8-h-Format: Phasen 01–04 (Math/ML/DL/CV), 06–10 (Audio/Transformer/Generative/SSM/LLM-Pretraining), 12 (Finetuning), 15 (Autonome Systeme), 16 (Reasoning), 19 (Capstones). → Diese sind im **16-h-Format** drin.

## Material-Pakete

### Was Trainer:innen mitbringen

- Folien-Set (~ 100 Slides) mit Live-Code-Sektionen
- **Vorbereitete Demo-Daten**:
  - Mini-Wikipedia-DE-Subset (50 MB) für RAG
  - 3 Beispiel-Use-Cases unterschiedlicher Branchen
  - LiteLLM-Proxy-Compose-File getestet
- Backup-Plan: Ollama-Local mit Llama-3.3-8B falls EU-API-Calls scheitern
- AI-Act-Konformitäts-YAML-Templates für 5 Branchen-Beispiele

### Was Teilnehmende mitnehmen

- Eigenes Repo-Fork mit funktionierendem RAG-Mini-Stack
- LiteLLM-Proxy-Konfiguration mit eigenem EU-API-Key
- Erste Konformitätserklärung-YAML-Skizze
- Phoenix-Tracing-Dashboard mit eigenen Traces
- Lese-Liste: `docs/lernpfade/wp-entwicklerin.md` oder `data-scientist.md`

## Trainer:innen-Checkliste (Vorbereitung)

- [ ] Phasen 11 + 13 + 17 + 20 mindestens 2× selbst durchgespielt
- [ ] LiteLLM-Proxy-Compose lokal stabil
- [ ] Qdrant + Pharia / Mistral als RAG-Stack getestet
- [ ] EU-API-Keys mit höherem Rate-Limit (für Live-Demos mit ~ 30 Teilnehmenden)
- [ ] Backup-Wifi / Tethering bei externem Workshop
- [ ] Vorbereiteter `dist-notebooks/`-Build (alle Notebooks pre-rendered, falls Marimo-Issues)

## Erfolgs-Metrik

Erfolgreicher Workshop-Tag:

- ≥ 80 % der Teilnehmenden haben am Ende einen lauffähigen Pydantic-AI-Agent mit eigenem API-Key
- ≥ 60 % haben einen RAG-Demo durchlaufen lassen (Qdrant + Embedding + Generierung)
- ≥ 40 % haben LiteLLM-Proxy lokal gestartet und einen Request durchgeschickt
- 100 % können benennen, welche AI-Act-Risikoklasse ihr Use-Case hat

## Anti-Patterns

- **Nicht** mit Phase 01 / 03 (Math / Deep Learning) starten — das frustriert Backend-Devs ohne ML-Hintergrund
- **Nicht** zu viele Anbieter parallel — beim Hands-on auf max. 2 EU-Provider fokussieren
- **Nicht** das LiteLLM-Setup auf den Schluss legen — wenn das nicht klappt, kippt der ganze Tag
- **Nicht** „du installierst dann zuhause" — Setup muss vor dem Workshop laufen, sonst Slot-Verlust

## Optional: Folge-Sessions

Wer das 8-h-Format anbietet, kann ergänzende 2-h-Vertiefungen anschließen:

- **Vertiefung Agents** (Phase 14 + 15): LangGraph + Postgres-Checkpointer + HITL
- **Vertiefung Finetuning** (Phase 12): LoRA + Unsloth auf 24-GB-GPU
- **Vertiefung Bias-Audit** (Phase 18): SHAP + DPO + Self-Censorship-Audit
- **Vertiefung Reasoning** (Phase 16): GRPO-Mathematik + Test-Time-Compute

## Stand

29.04.2026 · 8-h-Format basiert auf Phasen 00 / 05 / 11 / 13 / 14 / 17 / 18 / 20 · Format-Reviewer: Saskia Teichmann.
