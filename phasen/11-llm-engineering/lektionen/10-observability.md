---
id: 11.10
titel: Observability — OpenTelemetry GenAI + Phoenix / Langfuse (EU-self-hosted)
phase: 11-llm-engineering
dauer_minuten: 60
schwierigkeit: mittel
stand: 2026-04-28
voraussetzungen: [11.05, 11.08]
lernziele:
  - OpenTelemetry GenAI Semantic Conventions verstehen
  - Phoenix lokal aufsetzen und Traces betrachten
  - Langfuse self-hosted (EU) vs. Cloud-EU-Region wählen
  - Tracing als Audit-Logging-Schicht (AI-Act Art. 12) nutzen
compliance_anker:
  - tracing-eu-self-hosted
  - audit-logging-art-12
ai_act_artikel:
  - art-12
  - art-13
dsgvo_artikel:
  - art-5-abs-1-lit-c
  - art-32
---

## Worum es geht

> Stop debugging LLM-Apps with print(). — Tracing zeigt **jeden Tool-Call, jeden Token, jede Latenz** in einer UI.

**OpenTelemetry GenAI Semantic Conventions** (Status 04/2026: **Development / Experimental** — Felder können sich noch ändern) standardisieren, **wie** LLM-Aufrufe ge-traced werden. **Phoenix** (Arize) und **Langfuse** sind die zwei führenden UIs darauf.

## Voraussetzungen

- Lektion 11.05 (du verstehst Anbieter-Aufrufe)
- Lektion 11.08 (du verstehst Eval-Mindset)
- Optional: Docker für Phoenix-Self-Host

## Konzept

### Was Tracing für LLM-Apps bringt

Klassische APM-Tools (Datadog, NewRelic) tracen HTTP-Calls. Bei LLM-Apps brauchst du zusätzlich:

- **Welches Modell** wurde verwendet, in welcher Version?
- **Wie viele Tokens** Input/Output, wie viele aus dem Cache?
- **Welche Tool-Calls** mit welchen Argumenten?
- **Welche Cost** in EUR pro Request?
- **Welche Latenz** für Retrieval, Generation, Tool-Execution einzeln?

OpenTelemetry GenAI definiert dafür **standardisierte Attribute**.

### Wichtigste OpenTelemetry-GenAI-Felder (Stand 04/2026, Development)

| Attribut | Was |
|---|---|
| `gen_ai.operation.name` | z. B. `chat`, `text_completion`, `embeddings` |
| `gen_ai.provider.name` | z. B. `anthropic`, `openai`, `mistral_ai` |
| `gen_ai.request.model` | z. B. `claude-sonnet-4-6` |
| `gen_ai.response.model` | tatsächlich verwendetes Modell (kann abweichen) |
| `gen_ai.usage.input_tokens` | Input-Token-Count |
| `gen_ai.usage.output_tokens` | Output-Token-Count |
| `gen_ai.usage.cache_creation.input_tokens` | Cache-Write-Tokens |
| `gen_ai.usage.cache_read.input_tokens` | Cache-Read-Tokens |
| `gen_ai.usage.reasoning.output_tokens` | Reasoning-Modelle (o3, R1) |
| `gen_ai.request.temperature` / `top_p` / `top_k` | Sampling-Params |
| `gen_ai.request.max_tokens` / `stream` | Request-Params |
| `gen_ai.input.messages` / `gen_ai.output.messages` | (Opt-In wegen PII!) |
| `gen_ai.system_instructions` | (Opt-In) |

> ⚠️ Felder mit „Opt-In" speichern Plaintext-Prompts. Bei PII: Hashes statt Plaintext loggen — siehe Phase 20.05.

> ⚠️ **Versions-Drift**: Älteres Attribut hieß `gen_ai.system` (deprecated) → migriert auf `gen_ai.provider.name`. In gemischten Tracing-Pipelines beide prüfen.

### Phoenix (Arize) — Open Source, lokal

Apache 2.0, GitHub `Arize-ai/phoenix`. Auf OpenTelemetry aufgebaut.

**Self-Hosting (Empfehlung für DACH)**:

```bash
docker run -p 6006:6006 arizephoenix/phoenix:latest
# UI: http://localhost:6006
```

**Tracing aktivieren** (Pydantic AI):

```python
import os
os.environ["PHOENIX_PROJECT_NAME"] = "tierheim-bot"

from phoenix.otel import register
register(project_name="tierheim-bot", auto_instrument=True)

# Ab jetzt: jeder Pydantic-AI-Call wird ge-traced
from pydantic_ai import Agent
agent = Agent("anthropic:claude-sonnet-4-6")
# ...
```

UI auf `localhost:6006` zeigt jeden Aufruf mit:

- Model-Name, Versionen
- Token-Counts (inkl. Cache)
- Latenz (Retrieval, Generation, Tool je separat)
- Tool-Calls mit Argumenten
- Estimated Cost in USD

**EU-Cloud-Variante**: Phoenix-Cloud bietet **keine** explizite EU-Region (Stand 04/2026). Bei DSGVO-kritischen Setups → **Self-Host** in EU-Cloud (Scaleway, OVH, IONOS).

### Langfuse — EU-Cloud verfügbar

Open Source, optional Cloud. **Cloud-EU-Region explizit verfügbar** (US, EU, Japan, HIPAA-US wählbar) — relevanter Pluspunkt für DACH.

**Self-Hosting**:

```bash
git clone https://github.com/langfuse/langfuse.git
cd langfuse
docker compose up -d
# UI: http://localhost:3000
```

**Cloud-Pricing (Stand 04/2026)**:

| Plan | Preis | Features |
|---|---|---|
| Hobby | $0 | 50 k Units, 30 Tage Retention, 2 User |
| Core | $29/Mo | 100 k Units, 90 Tage |
| Pro | $199/Mo | 100 k Units, 3 Jahre, SOC2 / ISO27001 / HIPAA-BAA |
| Teams | + $300/Mo | SSO, RBAC |
| Enterprise | ab $2.499/Mo | dedicated support |

**Tracing aktivieren** (Langfuse Decorator):

```python
from langfuse.openai import openai  # statt: from openai import openai

# Ab jetzt: jeder OpenAI-Call wird ge-traced
client = openai.OpenAI(...)
r = client.chat.completions.create(...)
```

### Welche Wahl wann?

| Frage | Empfehlung |
|---|---|
| brauchst nur lokales Debugging | **Phoenix lokal** |
| brauchst SOC2 / HIPAA / Enterprise-Compliance | **Langfuse Cloud Pro** (EU-Region!) |
| willst gar nichts in die Cloud | **Phoenix oder Langfuse self-hosted** |
| nutzt OpenTelemetry-Collector schon | **Phoenix** (OTel-native) |
| nutzt LangChain / LlamaIndex / Haystack | **Langfuse** (alle drei haben native Integrationen) |

## Audit-Logging vs. Tracing

| Aspekt | Tracing (Phoenix/Langfuse) | Audit-Logging (Phase 20.05) |
|---|---|---|
| Zweck | Debugging, Performance | Compliance-Nachweis |
| Detail | Plaintext / Hashes | Hashes |
| Aufbewahrung | Tage bis Wochen | **Mind. 6 Monate** (AI-Act Art. 12) |
| Wer hat Zugriff | Dev-Team | Beauftragte:r + Audit |

→ Beide sind **komplementär**. Tracing für Dev, Audit-Log für Recht.

## Hands-on (30 Min.)

```bash
# Phoenix lokal starten
docker run -p 6006:6006 arizephoenix/phoenix:latest

# In deinem Code (oder im Marimo-Notebook):
uv add arize-phoenix arize-phoenix-otel openinference-instrumentation-pydantic-ai
```

```python
import os
os.environ["PHOENIX_PROJECT_NAME"] = "phase-11-test"

from phoenix.otel import register
register(project_name="phase-11-test", auto_instrument=True)

from pydantic_ai import Agent

agent = Agent("ollama:qwen3:8b", system_prompt="Antworte auf Deutsch.")
agent.run_sync("Was ist BPE-Tokenisierung?")
agent.run_sync("Was ist DPO?")

# Browser auf http://localhost:6006 → Traces sichtbar
```

## Selbstcheck

- [ ] Du nennst die fünf wichtigsten OpenTelemetry-GenAI-Felder.
- [ ] Du erkennst, dass `gen_ai.input.messages` PII-Risiko hat (Opt-In!).
- [ ] Du wählst Phoenix vs. Langfuse je nach Anforderung.
- [ ] Du verstehst den Unterschied Tracing (Dev) vs. Audit-Log (Compliance).

## Compliance-Anker

- **Audit-Logging (AI-Act Art. 12)**: Tracing kann eine Datenquelle für Audit-Logs sein, ersetzt sie aber nicht. Aufbewahrung mind. 6 Monate, Hashes statt Plaintext.
- **EU-Hosting**: Phoenix self-hosted in EU-Cloud, oder Langfuse Cloud EU-Region. Niemals Tracing-Daten naiv in US-Cloud — sonst SCC + TIA + EU-Datazone aktivieren.
- **Datenminimierung (Art. 5 Abs. 1 lit. c DSGVO)**: nur tracen, was du brauchst. Plaintext-Prompts mit User-Daten **nicht** unverschlüsselt speichern.

## Quellen

- OpenTelemetry GenAI Spans Spec — <https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-spans/> (Zugriff 2026-04-28)
- Phoenix (Arize) — <https://phoenix.arize.com/>
- Phoenix Docs — <https://docs.arize.com/phoenix/>
- Langfuse Docs — <https://langfuse.com/docs>
- Langfuse Pricing (EU-Region) — <https://langfuse.com/pricing>
- Langfuse Self-Hosting — <https://langfuse.com/docs/deployment/self-host>
- OpenInference (Phoenix-Instrumentations) — <https://github.com/Arize-ai/openinference>

## Weiterführend

→ Phase **17** (Production EU-Hosting) — Phoenix/Langfuse im vollständigen Stack mit LiteLLM-Proxy
→ Phase **20** (Recht & Governance) — Audit-Logging-Pattern (Lektion 20.05)
