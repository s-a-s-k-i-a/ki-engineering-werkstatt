---
id: 17.11
titel: Hands-on — Pharia-1 auf STACKIT mit vLLM + LiteLLM + Langfuse
phase: 17-production-und-eu-hosting
dauer_minuten: 180
schwierigkeit: fortgeschritten
stand: 2026-04-29
voraussetzungen: [17.02, 17.04, 17.05, 17.06, 17.07, 17.08]
lernziele:
  - End-to-End-Production-Stack auf EU-Cloud aufsetzen
  - Pharia-1-7B (Open-Weights) als vLLM-Server hosten
  - LiteLLM Proxy davor mit Cost-Tracking + EU-Routing
  - Langfuse v3 (managed EU oder self-hosted) für Tracing
  - Komplette DSGVO + AI-Act-Compliance-Checkliste durchgehen
compliance_anker:
  - end-to-end-eu-stack
  - datenresidenz-bsi-c5
  - audit-pipeline-vollstaendig
ai_act_artikel:
  - art-12
  - art-13
  - art-14
  - art-15
  - art-17
dsgvo_artikel:
  - art-5
  - art-25
  - art-28
  - art-32
  - art-44
---

## Worum es geht

> Stop hoping „EU-Hosting" means anything without a checklist. — diese Lektion baut den **vollständigen Production-Stack** auf STACKIT (BSI C5 Type 2): Pharia-1-LLM-7B-control auf vLLM, LiteLLM-Proxy mit EU-Routing, Langfuse als Tracing-Backend. Alles zusammen DSGVO + AI-Act-konform.

> ⚠️ **Stand 28.04.2026**: Cohere-Aleph-Alpha-Merger ist angekündigt (25.04.2026), Pharia-Roadmap nach Merger offen. Pharia-1-LLM-7B-control bleibt als Open-Weights auf Hugging Face verfügbar — das ist die Basis dieser Lektion. Bei produktivem Einsatz empfehle ich, **direkt mit Aleph Alpha zu sprechen** über laufende Verträge.

## Voraussetzungen

- Lektionen 17.02 (vLLM), 17.04 (EU-Cloud), 17.05 (Docker-Compose), 17.06 (Helm), 17.07 (LiteLLM), 17.08 (Observability)
- STACKIT-Account mit aktivierter SKE (Kubernetes Engine) **ODER** lokaler GPU mit ≥ 24 GB VRAM für Test
- Hugging Face Account mit Pharia-Access (Open Weights nach Lizenz-Akzeptanz)

## Konzept

### Ziel-Architektur

```mermaid
flowchart TB
    Client[App / SDK]
    Client --> CL[Caddy + TLS<br/>ki.example.de]
    CL --> LL[LiteLLM Proxy<br/>4× Replica]
    LL --> VL[vLLM<br/>Pharia-1-7B<br/>Helm-Replicas]
    LL --> A[Anthropic Sonnet 4.6<br/>EU-Datazone]
    LL --> M[Mistral Large 3<br/>FR]

    LL -.-> R[Redis Cluster<br/>Cache]
    LL -.-> P[(Postgres HA<br/>Spend + Logs)]
    LL --> Lf[Langfuse v3<br/>EU-Cloud Frankfurt]

    subgraph SKE[" STACKIT Kubernetes Engine — Neckarsulm "]
        LL
        VL
        R
        P
    end

    Lf --- DPA["Langfuse DPA<br/>ISO 27001 + SOC 2"]

    classDef ext fill:#FF6B3D,color:#0E1116
    classDef int fill:#3D8BFF,color:#FFF
    class Client,A,M,Lf,DPA ext
    class CL,LL,VL,R,P int
```

### Vier Phasen der Implementation

```mermaid
flowchart LR
    A[1. STACKIT Setup<br/>SKE + GPU-Node] --> B[2. vLLM-Helm<br/>Pharia-1 deployen]
    B --> C[3. LiteLLM-Helm<br/>Routing + Budgets]
    C --> D[4. Langfuse-Anbindung<br/>+ Compliance-Verifikation]

    classDef step fill:#FF6B3D,color:#0E1116
    class A,B,C,D step
```

### Phase 1 — STACKIT SKE mit GPU-Node

```bash
# stackit-cli Setup
stackit auth login
stackit project list

# SKE-Cluster erstellen
stackit ske cluster create \
    --name ai-prod \
    --kubernetes-version 1.31 \
    --region eu01 \
    --node-pool '[
      {
        "name": "gpu-pool",
        "machine_type": "g1.8d.4ngpu.h100",
        "min": 1, "max": 3,
        "labels": {"nvidia.com/gpu": "true"},
        "taints": [{"key": "nvidia.com/gpu", "effect": "NoSchedule"}]
      }
    ]'

# kubeconfig laden
stackit ske credentials describe --cluster-name ai-prod > ~/.kube/config-stackit
export KUBECONFIG=~/.kube/config-stackit
```

> Hinweis: STACKIT-spezifische Machine-Types und CLI-Flags vor Production gegen die [STACKIT-Doku](https://docs.stackit.cloud/) re-verifizieren — die hier gezeigten Werte sind Beispiele und können sich ändern.

### Phase 1.5 — NVIDIA GPU-Operator

```bash
helm repo add nvidia https://helm.ngc.nvidia.com/nvidia
helm repo update

helm install gpu-operator nvidia/gpu-operator \
    --namespace gpu-operator --create-namespace \
    --set driver.enabled=false \
    --set toolkit.enabled=true \
    --set nodeSelector."nvidia\.com/gpu"=true \
    --set tolerations[0].key="nvidia.com/gpu" \
    --set tolerations[0].effect="NoSchedule"

# Verifikation
kubectl get nodes -o json | jq '.items[].status.allocatable["nvidia.com/gpu"]'
# Output: "1" (für deine GPU-Node)
```

### Phase 2 — vLLM mit Pharia-1-LLM-7B-control

`vllm-pharia.yaml`:

```yaml
servingEngineSpec:
  modelSpec:
    - name: "pharia-1-7b-control"
      model: "Aleph-Alpha/Pharia-1-LLM-7B-control"
      replicaCount: 2
      resources:
        gpuCount: 1  # 1× H100 reicht für 7B + Context 32k
      hf_token: "$(HF_TOKEN)"
      vllmConfig:
        maxModelLen: 32768
        gpuMemoryUtilization: 0.85
        enablePrefixCaching: true
        dtype: "bfloat16"  # Pharia-1 ist BF16-trainiert

routerSpec:
  enabled: true
  replicaCount: 2
  routingLogic: "session"  # State-Continuity wichtig für Conversational

monitoring:
  prometheus:
    enabled: true
    serviceMonitor:
      enabled: true
  grafana:
    enabled: true
```

```bash
# Deploy
helm repo add vllm https://vllm-project.github.io/production-stack
helm install vllm vllm/vllm-stack \
    --namespace ai-prod --create-namespace \
    -f vllm-pharia.yaml

# Wait for ready (Modell-Download dauert)
kubectl rollout status deployment/vllm-pharia-1-7b-control -n ai-prod --timeout=15m
```

Test:

```bash
kubectl port-forward -n ai-prod svc/vllm-router 8000:80

curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "pharia-1-7b-control",
    "messages": [
      {"role":"user","content":"Was ist die DSGVO Art. 5?"}
    ],
    "max_tokens": 200
  }'
```

### Phase 3 — LiteLLM Proxy

`litellm-values.yaml`:

```yaml
replicaCount: 4

masterkey: "$(LITELLM_MASTER_KEY)"

db:
  deployStandalone: false
  url: "postgresql://litellm:$(PG_PW)@postgres-rw.db:5432/litellm"

redis:
  deployStandalone: false
  url: "redis://redis-master.cache:6379"

ingress:
  enabled: true
  className: "nginx"
  hosts:
    - host: ki-api.example.de
      paths: [{path: /, pathType: Prefix}]
  tls:
    - secretName: litellm-tls
      hosts: [ki-api.example.de]

configMap:
  config.yaml:
    model_list:
      # Default-Tier: lokales Pharia-1
      - model_name: "default"
        litellm_params:
          model: "openai/pharia-1-7b-control"
          api_base: "http://vllm-router.ai-prod:80/v1"
          api_key: "sk-stackit-internal"
        metadata:
          eu_compliant: true
          rz_standort: "Neckarsulm"
          bsi_c5_type_2: true

      # Premium-Tier: Anthropic Münchner Office
      - model_name: "premium"
        litellm_params:
          model: "anthropic/claude-sonnet-4-6"
          api_key: os.environ/ANTHROPIC_API_KEY
        metadata:
          eu_compliant: true
          provider_office: "München"

      # Fallback-Tier: Mistral Large 3
      - model_name: "fallback"
        litellm_params:
          model: "mistral/mistral-large-3"
          api_key: os.environ/MISTRAL_API_KEY
        metadata:
          eu_compliant: true
          rz_standort: "Paris"

    router_settings:
      fallbacks:
        - "default": ["fallback", "premium"]
        - "premium": ["fallback"]
      num_retries: 2
      timeout: 30

    litellm_settings:
      cache: true
      cache_params:
        type: "redis-semantic"
        host: "redis-master.cache"
        similarity_threshold: 0.92
        ttl: 3600
      success_callback: ["langfuse"]
      failure_callback: ["langfuse"]

    general_settings:
      master_key: os.environ/LITELLM_MASTER_KEY
      database_url: os.environ/DATABASE_URL
```

```bash
helm install litellm berriai/litellm-helm \
    --namespace ai-prod \
    -f litellm-values.yaml
```

### Phase 4 — Langfuse Tracing

Variante A — **managed EU-Cloud (einfachster Pfad)**:

1. Account auf <https://cloud.langfuse.com> mit EU-Region
2. DPA signieren
3. Public + Secret Key generieren

```bash
# Als K8s-Secret deployen
kubectl create secret generic langfuse-keys -n ai-prod \
    --from-literal=public-key=pk-lf-... \
    --from-literal=secret-key=sk-lf-... \
    --from-literal=host=https://cloud.langfuse.com
```

LiteLLM-ConfigMap erweitern:

```yaml
litellm_settings:
  langfuse_public_key: os.environ/LANGFUSE_PUBLIC_KEY
  langfuse_secret_key: os.environ/LANGFUSE_SECRET_KEY
  langfuse_host: "https://cloud.langfuse.com"
```

Variante B — **self-hosted via Helm** (siehe Lektion 17.06 mit Bitnami-Restruktur).

### Compliance-Verifikation — die Pflicht-Checkliste

Vor Go-Live diese Punkte abhaken (**audit-fest dokumentieren**):

#### DSGVO

- [ ] **AVV STACKIT** signiert (Self-Service-Vertrag im Customer Portal)
- [ ] **AVV Anthropic Enterprise** signiert (mit EU-Datazone)
- [ ] **AVV Mistral** signiert (Standard-AVV)
- [ ] **AVV Langfuse** signiert (DPA für managed EU-Region)
- [ ] **PII-Filter** in OTel-Span-Processor aktiv (siehe Lektion 17.08)
- [ ] **Pseudonymisierung** der User-IDs vor LiteLLM (Hash, nicht Klartext)
- [ ] **Right-to-be-Forgotten-Workflow** dokumentiert
- [ ] **Aufbewahrungsfrist** definiert (Audit-Logs ≥ 6 Monate, Cache-TTL ≤ 2 h)

#### AI Act

- [ ] **Risiko-Klassifizierung** dokumentiert (Phase 20.01) — vermutlich „begrenzt" wegen Chat-Charakter
- [ ] **Audit-Trail** strukturiert + signiert (Phase 20.05)
- [ ] **Cost-Caps** pro User aktiv + getestet (Lektion 17.09)
- [ ] **Human Oversight** an kritischen Stellen (Lektion 14.05 — Adoption-Approval-Pattern)
- [ ] **Robustness-Eval** mit Promptfoo + Ragas (Phase 11.08, 11.09)
- [ ] **Self-Censorship-Audit** dokumentiert (Phase 18) — bei Pharia-1 nicht relevant, bei Qwen3 / DeepSeek-R1 Pflicht

#### Sicherheit

- [ ] **NetworkPolicies** — vLLM erreichbar nur von LiteLLM
- [ ] **PodSecurityStandards** = `restricted` für alle Workloads
- [ ] **gitleaks + trufflehog** in CI gegen Secret-Leaks
- [ ] **TLS** für alle externen Endpoints (Caddy / Ingress-Nginx)
- [ ] **Backup-Pipeline** Postgres nightly + Restore-Test alle 3 Monate
- [ ] **Incident-Runbook** bei NIS2-relevanten Events (siehe Phase 17 `compliance.md`)

### Performance-Erwartung (Stand 04/2026)

Auf 1× H100 mit Pharia-1-7B-control:

- Single-Stream-Latency: ~ 60–90 Tokens/s
- TTFT: ~ 150–300 ms p50
- Concurrent Throughput: ~ 800–1.500 Tokens/s aggregiert (16 Concurrent)
- Quality auf deutschem Text (BAFA-Vertrauensdienst-zertifiziert): vergleichbar mit Mistral 7B Instruct, oft besser bei Recht/Verwaltung-Vokabular

### Wann diese Architektur nicht passt

- **< 5M Tokens / Monat** → STACKIT AI Model Serving (managed) ist günstiger als eigenes vLLM
- **70B-Klasse-Modelle nötig** → OVHcloud Llama 3.3 70B Endpoint ist günstiger
- **Multi-LoRA-Setup** → eigene vLLM-Instance ist Pflicht (managed APIs unterstützen kein LoRA-Hot-Swap)
- **DSFA-Pflicht für „rein automatisierte Entscheidung"** → HITL-Pattern (Lektion 14.05) ist Pflicht, kein Stack-Issue allein

## Hands-on (4–8 h, je nach Tiefe)

Implementiere die obige Architektur in deiner eigenen STACKIT-Umgebung:

1. STACKIT-Account + SKE mit GPU-Node aufsetzen
2. NVIDIA GPU-Operator installieren
3. vLLM-Helm mit Pharia-1-7B deployen
4. LiteLLM-Helm mit drei Tiers (default/premium/fallback)
5. Langfuse-EU-Cloud-Account anlegen, DPA signieren, Tracing aktivieren
6. End-to-End-Test: 100 deutsche Anfragen, Spend-Report prüfen
7. Compliance-Checkliste durchgehen + Ergebnis in `audits/2026-04-stack.md` dokumentieren

## Selbstcheck

- [ ] Du deployst Pharia-1-7B auf STACKIT SKE.
- [ ] Du verbindest LiteLLM Proxy mit drei EU-Tiers + Routing.
- [ ] Du tracest alle Calls an Langfuse mit PII-Redaction.
- [ ] Du erfüllst die Pflicht-Checkliste (DSGVO + AI-Act + NIS2).
- [ ] Du dokumentierst die Architektur-Entscheidungen in einer DSFA-Light.

## Compliance-Anker

- **End-to-End-EU-Stack**: dieser Lehrbuch-Pattern erfüllt alle DACH-Compliance-Anforderungen 2026.
- **Datenresidenz**: STACKIT BSI C5 Type 2 + Anthropic München + Mistral FR + Langfuse Frankfurt.
- **Audit-Pipeline vollständig**: jeder Call hat ein Span, jeder Span hat einen Pseudonym-Hash, jede Anomalie hat einen Alert.

## Quellen

- STACKIT SKE GPU-Operator — <https://docs.stackit.cloud/products/runtime/kubernetes-engine/how-tos/use-nvidia-gpus/>
- STACKIT AI Model Serving — <https://stackit.com/en/products/data-ai/stackit-ai-model-serving>
- vLLM Production Stack — <https://github.com/vllm-project/production-stack>
- LiteLLM Helm — <https://docs.litellm.ai/docs/proxy/deploy>
- Langfuse Cloud (EU-Region) — <https://cloud.langfuse.com>
- Langfuse DPA — <https://langfuse.com/security/dpa>
- Pharia-1-LLM-7B-control HuggingFace — <https://huggingface.co/Aleph-Alpha/Pharia-1-LLM-7B-control>
- Cohere-Aleph-Alpha-Merger (Hintergrund) — <https://www.implicator.ai/cohere-buys-aleph-alpha-in-20bn-sovereign-ai-deal-backed-by-schwarz/>

## Weiterführend

→ Phase **20** (Recht & Governance — DSFA, AVV, AI-Literacy für diesen Stack)
→ Phase **19.A / 19.C** (Capstone — den Stack in einem realen Projekt nutzen)
→ Phase **18** (Self-Censorship-Audit — falls asiatische Modelle als Sub-Provider dazukommen)
