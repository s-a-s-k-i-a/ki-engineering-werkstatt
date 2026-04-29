---
id: 17.07
titel: LiteLLM Proxy — Multi-Provider, Cost-Tracking, EU-Routing
phase: 17-production-und-eu-hosting
dauer_minuten: 75
schwierigkeit: mittel
stand: 2026-04-28
voraussetzungen: [11.05, 17.05]
lernziele:
  - LiteLLM Proxy v1.83.14 (Stand 04/2026) als Multi-Provider-Gateway aufsetzen
  - Cost-Tracking pro User / Tag / Modell mit Budget-Alerts
  - EU-Routing-Switch (Default = EU, Fallback = US mit Logging-Marker)
  - Caching-Layer (In-Memory, Redis, Redis-Semantic, Qdrant-Semantic)
  - Audit-Logging und Slack-Alerts
compliance_anker:
  - eu-routing-default
  - cost-cap-pflicht
  - audit-trail-tool-calls
ai_act_artikel:
  - art-13
  - art-15
  - art-17
dsgvo_artikel:
  - art-32
  - art-44
---

## Worum es geht

> Stop scattering API-keys across services. — LiteLLM Proxy ist die zentrale Schaltstelle für Multi-Provider-LLM-Apps: ein OpenAI-kompatibler Endpoint, hinter dem 50+ Provider routen, mit Cost-Tracking, Caching, Rate-Limits und EU-Default-Routing. Stand 28.04.2026: **v1.83.14-stable** ([Releases](https://github.com/BerriAI/litellm/releases)).

## Voraussetzungen

- Phase 11.05 (Anbieter-Vergleich mit Token-Pricing)
- Lektion 17.05 (Docker-Compose-Stack mit Postgres + Redis)

## Konzept

### Was LiteLLM löst

```mermaid
flowchart LR
    App1[App / SDK]
    App2[Marimo Notebook]
    App3[CLI / Skript]
    App1 --> Proxy[LiteLLM Proxy<br/>:4000<br/>OpenAI-kompatibel]
    App2 --> Proxy
    App3 --> Proxy

    Proxy --> A[Anthropic]
    Proxy --> O[OpenAI]
    Proxy --> M[Mistral]
    Proxy --> S[STACKIT]
    Proxy --> I[IONOS]
    Proxy --> V[OVHcloud]
    Proxy --> Sc[Scaleway]
    Proxy --> L[lokales vLLM]

    Proxy -.-> R[Redis<br/>Cache]
    Proxy -.-> P[Postgres<br/>Spend + Logs]
    Proxy -.-> Sl[Slack-Alerts]

    classDef ext fill:#FF6B3D,color:#0E1116
    classDef int fill:#3D8BFF,color:#FFF
    class App1,App2,App3,A,O,M,S,I,V,Sc,L ext
    class Proxy,R,P,Sl int
```

### Drei Use-Cases auf einmal

LiteLLM löst gleichzeitig:

1. **Single-API für Multi-Provider** — du tauschst Provider per ConfigMap, nicht im Code
2. **Cost-Tracking** — pro User, Team, Tag, Modell mit Budgets + Alerts
3. **EU-Routing-Disziplin** — Default-Routing zu EU-Anbieter, Fallback nur mit Logging

### Installation + Quickstart (Docker)

```bash
docker run -d \
  --name litellm \
  -p 4000:4000 \
  -e DATABASE_URL=postgresql://litellm:${POSTGRES_PASSWORD}@postgres:5432/litellm \
  -e LITELLM_MASTER_KEY=sk-prod-... \
  -e ANTHROPIC_API_KEY=sk-ant-... \
  -e IONOS_API_KEY=... \
  -v $PWD/litellm-config.yaml:/app/config.yaml \
  ghcr.io/berriai/litellm:main-stable \
  --config /app/config.yaml --port 4000
```

### `litellm-config.yaml` — der EU-First-Stack

```yaml
model_list:
  # === EU-Default-Modelle (Priorität 1) ===
  - model_name: "claude-sonnet-4-6"
    litellm_params:
      model: "anthropic/claude-sonnet-4-6"
      api_key: os.environ/ANTHROPIC_API_KEY
      # Anthropic Münchner Office + EU-Datazone
      # AVV: Enterprise-Tier
    metadata:
      tier: "premium"
      eu_compliant: true
      avv_signed: "2026-01-15"

  - model_name: "mistral-large-3"
    litellm_params:
      model: "mistral/mistral-large-3"
      api_key: os.environ/MISTRAL_API_KEY
    metadata:
      tier: "premium"
      eu_compliant: true

  - model_name: "ionos-llama-70b"
    litellm_params:
      model: "openai/llama-3.1-70b-instruct"
      api_base: "https://openai.inference.de-txl.ionos.com/v1"
      api_key: os.environ/IONOS_API_KEY
    metadata:
      tier: "standard"
      eu_compliant: true
      rz_standort: "Frankfurt"

  - model_name: "stackit-mistral-nemo"
    litellm_params:
      model: "openai/mistral-nemo"
      api_base: "https://api.stackit.cloud/ai-model-serving/v1"
      api_key: os.environ/STACKIT_API_KEY
    metadata:
      eu_compliant: true
      bsi_c5_type_2: true

  # === Lokale Modelle (Priorität 0 — billigster Fallback) ===
  - model_name: "lokal-llama-70b"
    litellm_params:
      model: "openai/llama-3.3-70b"
      api_base: "http://vllm:8000/v1"
      api_key: "sk-local-dummy"
    metadata:
      tier: "lokal"
      eu_compliant: true
      hosting: "self"

  # === US-Fallback (nur mit Logging-Marker) ===
  - model_name: "claude-opus-4-7"
    litellm_params:
      model: "anthropic/claude-opus-4-7"
      api_key: os.environ/ANTHROPIC_API_KEY
    metadata:
      tier: "premium-us"
      eu_compliant: false  # explizit markiert
      requires_avv_sign_off: true

router_settings:
  routing_strategy: "simple-shuffle"
  fallbacks:
    - "claude-sonnet-4-6": ["mistral-large-3", "ionos-llama-70b"]
    - "ionos-llama-70b": ["stackit-mistral-nemo", "lokal-llama-70b"]
  num_retries: 2
  timeout: 30
  allowed_fails: 3
  cooldown_time: 60

litellm_settings:
  cache: true
  cache_params:
    type: "redis-semantic"
    similarity_threshold: 0.92
    host: "redis"
    port: 6379
    ttl: 3600

  success_callback: ["langfuse"]
  failure_callback: ["langfuse", "slack"]

  drop_params: true   # Provider-spezifische Params automatisch droppen

general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY
  database_url: os.environ/DATABASE_URL

  # Rate-Limits
  global_max_parallel_requests: 100

  # Alerting
  alerting: ["slack"]
  alerting_threshold: 5  # Sekunden Latenz
  alerting_args:
    daily_report_time: "09:00"
    daily_report_models: ["claude-sonnet-4-6", "ionos-llama-70b"]
```

### Cost-Tracking pro User + Tag

LiteLLM trackt **pro Master-Key oder Virtual-Key** den Token-Verbrauch und die EUR-Kosten. Setup:

```bash
# Virtual-Key pro User erstellen
curl -X POST http://litellm:4000/key/generate \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "buerger-amt-saskia",
    "team_id": "team-recht",
    "max_budget": 25.0,
    "budget_duration": "30d",
    "models": ["claude-sonnet-4-6", "ionos-llama-70b"],
    "rpm_limit": 10,
    "tpm_limit": 50000
  }'

# Spend-Report pro User
curl http://litellm:4000/global/spend/report?date_range=last_30_days \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY"
```

> **Cache-Hit-Tracking**: LiteLLM trackt Anthropic `cache_creation_input_tokens` + `cache_read_input_tokens` und OpenAI `prompt_tokens_details.cached_tokens` korrekt. `completion_cost()` berücksichtigt Cache-Hit-vs.-Miss-Preise. Granularität in Spend-Reports: laut Docu nicht explizit dokumentiert ([LiteLLM Cost-Tracking](https://docs.litellm.ai/docs/proxy/cost_tracking)) — eigenes Audit-Log empfohlen.

### EU-Routing-Disziplin

Der Punkt: 80 % aller LLM-Requests im DACH-Mittelstand sollen **default zu EU-Anbietern** routen. Pattern:

```yaml
# In der App: kein Modell-Name nennen, sondern Tier
- model_name: "tier-premium"
  litellm_params:
    model: "anthropic/claude-sonnet-4-6"  # Anthropic Münchner Office + EU-Datazone

# Fallback-Kette — alles EU
fallbacks:
  - "tier-premium": ["mistral-large-3", "ionos-llama-70b"]
```

Wenn ein US-Modell nötig ist (z. B. GPT-5.4 für spezifische Tasks):

```yaml
- model_name: "tier-premium-us"
  litellm_params:
    model: "openai/gpt-5-4"
  metadata:
    eu_compliant: false
    requires_avv_sign_off: true
    log_marker: "us-routing"  # für Audit
```

In deiner App kannst du dann pre-flight prüfen:

```python
import litellm

response = litellm.completion(
    model="tier-premium-us",
    messages=[...],
    metadata={"audit_reason": "spezifischer GPT-5.4-Use-Case", "approved_by": "tech-lead"}
)
# Audit-Log enthält log_marker="us-routing" — bei Behörden-Anfrage filterbar
```

### Caching-Layer

LiteLLM unterstützt Stand v1.83.14:

| Backend | Wann |
|---|---|
| **In-Memory** | Single-Instance, Quick-Test |
| **Disk** | Single-Instance, Persistierung über Restart |
| **Redis** | Multi-Instance, exakte Cache-Hits |
| **Redis-Semantic** | Multi-Instance, fuzzy-matching (cosine-Similarity) |
| **Qdrant-Semantic** | EU-tauglich (Qdrant Berlin), produktiv für RAG-Patterns |
| **S3 / GCS** | Long-Term Caching, Cold-Storage |

Beispiel mit Qdrant-Semantic:

```yaml
litellm_settings:
  cache: true
  cache_params:
    type: "qdrant-semantic"
    qdrant_api_base: "http://qdrant:6333"
    qdrant_collection_name: "litellm_cache"
    similarity_threshold: 0.92
    embedding_model: "openai/text-embedding-3-small"  # oder lokales BGE
    ttl: 7200
```

### Audit-Logging + Slack-Alerts

Stand v1.83.14:

```yaml
litellm_settings:
  success_callback: ["langfuse", "datadog"]
  failure_callback: ["langfuse", "slack"]

# Plus: Webhook für jeden Tool-Call
general_settings:
  webhook_url: "https://your-audit-pipeline.example.de/litellm-events"
```

Alerts in Slack:

| Trigger | Alert |
|---|---|
| Response-Time > 5s | Latenz-Spitze |
| Budget > 80 % | Budget-Warning |
| 5+ Fails in 60s | Provider-Outage |
| New Virtual-Key created | Audit-Notification |

### Production-Helm-Chart

Stand 04/2026 ist der LiteLLM-Helm-Chart offiziell ([docs.litellm.ai/docs/proxy/deploy#helm](https://docs.litellm.ai/docs/proxy/deploy#helm)):

- K8s 1.21+, Helm 3.8+
- PreSync-Hook für DB-Migrations
- Read-only-FS-fähig (PodSecurityStandards `restricted`-tauglich)
- Min-Spec: 4 vCPU / 8 GB RAM

→ Deployment-Detail in Lektion 17.06.

## Hands-on

1. LiteLLM lokal mit Docker-Compose starten (aus Lektion 17.05)
2. ConfigMap mit 3 EU-Providern (Anthropic, IONOS, lokales vLLM) bauen
3. Virtual-Key pro Mandant erstellen mit Budget 25 €/Monat
4. Test: 10 Requests gegen `tier-premium` schicken — Spend-Report prüfen
5. Cache-Hit-Test: denselben Prompt 5× — ab dem 2. Hit muss aus Redis kommen
6. EU-Fallback-Test: Anthropic-Endpoint mocken, Fallback zu Mistral verifizieren

## Selbstcheck

- [ ] Du startest LiteLLM Proxy mit Multi-Provider-Config.
- [ ] Du erstellst Virtual-Keys mit Budget pro Mandant.
- [ ] Du implementierst EU-Routing-Disziplin (Default = EU, US-Fallback mit Marker).
- [ ] Du nutzt Redis-Semantic oder Qdrant-Semantic-Cache.
- [ ] Du loggst alle Calls an Langfuse / Phoenix.

## Compliance-Anker

- **EU-Routing-Default (DSGVO Art. 44)**: Default-Routing zu EU-Provider.
- **Cost-Cap (AI-Act Art. 13)**: Token-Budget pro Mandant + Slack-Alert bei Überschreitung.
- **Audit-Trail (Art. 12)**: jeder Call wird via Webhook + Langfuse strukturiert geloggt.
- **Robustness (Art. 15)**: Fallback-Chain + `num_retries` als TOM.

## Quellen

- LiteLLM Releases (v1.83.14-stable 26.04.2026) — <https://github.com/BerriAI/litellm/releases>
- LiteLLM Cost Tracking — <https://docs.litellm.ai/docs/proxy/cost_tracking>
- LiteLLM Prompt Caching — <https://docs.litellm.ai/docs/completion/prompt_caching>
- LiteLLM Production Deployment — <https://docs.litellm.ai/docs/proxy/prod>
- LiteLLM Provider Liste — <https://docs.litellm.ai/docs/providers>
- LiteLLM Routing Strategy — <https://docs.litellm.ai/docs/proxy/reliability>

## Weiterführend

→ Lektion **17.08** (Phoenix + Langfuse Tracing — was LiteLLM in den Callbacks füttert)
→ Lektion **17.09** (Cost-Monitoring-Dashboard mit Grafana)
→ Lektion **17.10** (Caching deep-dive: Anthropic Prompt-Cache + Redis-Semantic)
→ Phase **20.05** (Audit-Logging-Pipeline aus LiteLLM-Webhooks)
