---
id: 17.06
titel: Helm-Charts auf K8s — vLLM Production Stack, LiteLLM, Phoenix, Langfuse
phase: 17-production-und-eu-hosting
dauer_minuten: 75
schwierigkeit: fortgeschritten
stand: 2026-04-28
voraussetzungen: [17.02, 17.05]
lernziele:
  - Wann Helm/K8s vs. Docker-Compose
  - Vier offizielle Helm-Charts kennen (vLLM Production Stack, LiteLLM, Phoenix, Langfuse)
  - NVIDIA GPU-Operator auf EU-Cloud-K8s aufsetzen (STACKIT SKE / OVH Managed K8s)
  - Häufige 2026er-Stolperfallen (Driver/CUDA, Bitnami-Restruktur, MIG)
compliance_anker:
  - immutable-infrastructure
  - audit-via-gitops
ai_act_artikel:
  - art-12
dsgvo_artikel:
  - art-32
---

## Worum es geht

> Stop hand-rolling K8s manifests for LLM stacks. — 2026 gibt es offizielle Helm-Charts für vLLM, LiteLLM, Phoenix und Langfuse. Helm + ArgoCD + GitOps liefern dir Audit-Trail + Rollback + Auto-Scaling out-of-the-box.

## Voraussetzungen

- Lektion 17.02 (vLLM)
- Lektion 17.05 (Docker-Compose — du kennst die Service-Topologie)
- K8s-Grundwissen (Pod, Service, ConfigMap, Secret)

## Konzept

### Wann Helm + K8s?

| Trigger | Aktion |
|---|---|
| ≥ 5 GPUs verteilt auf ≥ 2 Nodes | K8s Pflicht |
| Multi-Tenant (Mandanten-Isolation) | K8s + Namespaces |
| Auto-Scaling nötig (Token-Spitzen) | K8s + HPA |
| Multi-Model + Multi-LoRA | K8s + vLLM Production Stack |
| Audit-Trail über Infrastruktur-Änderungen | GitOps (ArgoCD/Flux) |

Sonst: Docker-Compose (Lektion 17.05).

### Die vier offiziellen Helm-Charts (Stand 04/2026)

```mermaid
flowchart TB
    Repo[Helm Repos] --> A[vLLM<br/>production-stack]
    Repo --> B[LiteLLM<br/>litellm-helm]
    Repo --> C[Phoenix<br/>phoenix-helm]
    Repo --> D[Langfuse<br/>langfuse-k8s]

    A --> A1[Multi-Replica vLLM<br/>+ LMCache + Prom/Grafana<br/>+ Round-Robin/Session-Routing]
    B --> B1[LiteLLM Proxy<br/>+ Postgres + Redis<br/>+ DB-Migration-Hook]
    C --> C1[Phoenix v14<br/>+ Postgres-Backend]
    D --> D1[Langfuse v3<br/>+ Postgres + ClickHouse + Redis + S3]

    classDef helm fill:#FF6B3D,color:#0E1116
    class A,B,C,D helm
```

Quellen mit Versions-Stand:

- **vLLM Production Stack** — `https://vllm-project.github.io/production-stack` ([github.com/vllm-project/production-stack](https://github.com/vllm-project/production-stack))
- **LiteLLM Helm** — offizielles Chart, K8s 1.21+, Helm 3.8+ ([docs.litellm.ai/docs/proxy/deploy#helm](https://docs.litellm.ai/docs/proxy/deploy#helm))
- **Phoenix Helm** — `arizephoenix/phoenix-helm` ([Phoenix Self-Hosting](https://arize.com/docs/phoenix/self-hosting))
- **Langfuse k8s** — `https://langfuse.github.io/langfuse-k8s` Chart 1.x ([Langfuse Helm-Doku](https://langfuse.com/self-hosting/deployment/kubernetes-helm))

> **SGLang** hat Stand 04/2026 **kein offizielles Helm-Chart** — eigene Manifests oder via Custom-Helm.

### NVIDIA GPU-Operator — auf EU-Cloud-K8s

```bash
# Cluster-weite Installation
helm repo add nvidia https://helm.ngc.nvidia.com/nvidia
helm repo update
helm install gpu-operator nvidia/gpu-operator \
    --namespace gpu-operator --create-namespace \
    --set toolkit.enabled=true \
    --set driver.enabled=false  # bei Hosted-K8s übernimmt der Provider die Driver
```

Auf STACKIT SKE: Driver wird vom Provider gemanagt — `driver.enabled=false`. Auf OVH Managed K8s: gleichermaßen. Auf eigener Bare-Metal-K8s: `driver.enabled=true`.

### vLLM Production Stack — `values.yaml`

```yaml
# Basis-Skelett für STACKIT SKE / OVH Managed K8s
servingEngineSpec:
  modelSpec:
    - name: "llama33-70b-awq"
      model: "meta-llama/Llama-3.3-70B-Instruct"
      quantization: "awq"
      replicaCount: 2
      resources:
        gpuCount: 2  # 2× H100 oder H200
      hf_token: "${HF_TOKEN}"
      vllmConfig:
        maxModelLen: 32768
        gpuMemoryUtilization: 0.92
        enablePrefixCaching: true
      lmcache:
        enabled: true
        cpuOffloadingBufferSize: 60  # GB pro Replica

routerSpec:
  enabled: true
  replicaCount: 2
  routingLogic: "session"  # oder "roundrobin"

monitoring:
  prometheus:
    enabled: true
  grafana:
    enabled: true
    dashboards:
      vllm: true  # vorgefertigte vLLM-Dashboards
```

Deploy:

```bash
helm repo add vllm https://vllm-project.github.io/production-stack
helm repo update
helm install vllm vllm/vllm-stack -f values.yaml \
    --namespace ai-stack --create-namespace
```

### LiteLLM-Helm — `values.yaml`

```yaml
replicaCount: 3

masterkey: "${LITELLM_MASTER_KEY}"

db:
  deployStandalone: false   # externe Postgres nutzen (HA)
  url: "postgresql://litellm:${PG_PW}@postgres-rw.db:5432/litellm"

redis:
  deployStandalone: false
  url: "redis://redis-master.cache:6379"

ingress:
  enabled: true
  className: "nginx"
  hosts:
    - host: ki-api.example.de
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: litellm-tls
      hosts: [ki-api.example.de]

# Provider-Endpoints kommen via ConfigMap
configMap:
  config.yaml:
    model_list:
      - model_name: "llama33-70b"
        litellm_params:
          model: "openai/llama33-70b-awq"
          api_base: "http://vllm-router.ai-stack:80/v1"
      - model_name: "claude-sonnet-4-6"
        litellm_params:
          model: "anthropic/claude-sonnet-4-6"
```

### Phoenix-Helm — `values.yaml`

```yaml
auth:
  enabled: true
  username: admin
  password: "${PHOENIX_ADMIN_PW}"

storage:
  postgresql:
    enabled: true
    auth:
      username: phoenix
      password: "${PG_PW}"
    primary:
      persistence:
        size: 100Gi

ingress:
  enabled: true
  className: "nginx"
  host: phoenix.example.de
```

### Langfuse-Helm — `values.yaml` (Achtung: Bitnami-Image-Restruktur)

```yaml
postgresql:
  enabled: true
  image:
    registry: docker.io
    repository: bitnamilegacy/postgresql  # NEU seit 28.08.2025
    tag: 17.0.0

clickhouse:
  enabled: true
  image:
    repository: bitnamilegacy/clickhouse
    tag: 24.x

redis:
  enabled: true
  image:
    repository: bitnamilegacy/redis
    tag: 7.x

s3:
  enabled: true
  # MinIO oder externer S3-kompatibler Bucket

ingress:
  enabled: true
  hosts:
    - host: langfuse.example.de
      paths: [{ path: /, pathType: Prefix }]
```

> ⚠️ **Bitnami-Restruktur (28.08.2025)**: alle Bitnami-basierten Subcharts müssen auf `bitnamilegacy/*` umgestellt werden. Sonst greifen die Default-Image-Tags ins Leere ([Langfuse-k8s Issue-Tracker](https://github.com/langfuse/langfuse-k8s/issues)).

### GitOps mit ArgoCD

Empfohlenes Pattern für Audit-Trail:

```yaml
# argocd-app-vllm.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: vllm-stack
  namespace: argocd
spec:
  project: ai-stack
  source:
    repoURL: https://gitlab.example.de/infra/ai-stack.git
    targetRevision: main
    path: vllm/
    helm:
      valueFiles: [values.yaml, values.production.yaml]
  destination:
    server: https://kubernetes.default.svc
    namespace: ai-stack
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

Vorteile:

- Jede Helm-Values-Änderung = Git-Commit = Audit-Trail
- Rollback per `git revert`
- Dry-Run via PR-Review
- Drift-Detection automatisch

### Stolperfallen 2026

| Problem | Ursache | Fix |
|---|---|---|
| `nvidia.com/gpu: 0/0 available` | Driver-Mismatch H100/H200 | Treiber ≥ 550.x, CUDA ≥ 12.4 |
| Doppelte GPU-Allocation | Mix aus `nvidia-device-plugin` + GPU-Operator | nur GPU-Operator nutzen |
| Langfuse-Helm bricht | Bitnami-Image-Restruktur | `bitnamilegacy/*` in values.yaml |
| MIG-Profile fehlen | nicht alle Provider exposen MIG | bei STACKIT „whole GPU", bei Scaleway dokumentiert |
| vLLM-Pod OOM-Killed | KV-Cache-Overcommit | `gpu_memory_utilization: 0.85` (statt 0.92) |
| Phoenix-DB-Migration hängt | v14-Breaking-Changes | Pod-Logs auf „migration job complete" warten |

### Sicherheits-Pattern

| Pattern | Implementation |
|---|---|
| **Network Policies** | nur LiteLLM erreicht vLLM, nur Caddy/Ingress erreicht LiteLLM |
| **Secrets** | External Secrets Operator + Vault / SOPS / sealed-secrets |
| **PodSecurityStandards** | `restricted` für alle App-Workloads |
| **GPU-Node-Isolation** | Taints + Tolerations für GPU-Workloads |
| **Audit-Logging** | K8s API-Server-Audit + ArgoCD-Application-History |

## Hands-on

1. STACKIT-SKE oder OVH-Managed-K8s aufsetzen mit 1× H100 oder H200
2. NVIDIA GPU-Operator installieren, `kubectl get nodes -o wide` zeigt GPU
3. vLLM Production Stack mit Llama-3.3-70B-AWQ deployen (1 Replica)
4. LiteLLM-Helm darüber, ConfigMap mit `vllm-router` als Backend
5. Smoke-Test: `curl ki-api.example.de/v1/chat/completions` mit Master-Key
6. Phoenix-Helm + Langfuse-Helm parallel installieren
7. ArgoCD aufsetzen + alle vier Charts als Applications definieren

## Selbstcheck

- [ ] Du nennst die vier offiziellen Helm-Charts mit URL.
- [ ] Du installierst NVIDIA GPU-Operator korrekt für STACKIT/OVH.
- [ ] Du kennst die Bitnami-Image-Restruktur (28.08.2025) und ihren Fix.
- [ ] Du nutzt GitOps (ArgoCD/Flux) für Audit-Trail.
- [ ] Du isolierst GPU-Pods via Taints + NetworkPolicies.

## Compliance-Anker

- **Audit-via-GitOps (AI-Act Art. 12)**: jede Infrastruktur-Änderung ist ein Git-Commit.
- **Immutable Infrastructure (DSGVO Art. 32)**: keine `kubectl edit`-Hotfixes — alle Änderungen via Helm + ArgoCD.
- **Secret-Hygiene**: External Secrets Operator + Vault statt YAML-Secrets.

## Quellen

- vLLM Production Stack — <https://github.com/vllm-project/production-stack>
- LiteLLM Helm-Deployment — <https://docs.litellm.ai/docs/proxy/deploy#helm>
- Phoenix Self-Hosting — <https://arize.com/docs/phoenix/self-hosting>
- Langfuse Helm-Deployment — <https://langfuse.com/self-hosting/deployment/kubernetes-helm>
- NVIDIA GPU-Operator Platform-Support — <https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/platform-support.html>
- STACKIT SKE GPU-Operator — <https://docs.stackit.cloud/products/runtime/kubernetes-engine/how-tos/use-nvidia-gpus/>
- ArgoCD Docs — <https://argo-cd.readthedocs.io/>

## Weiterführend

→ Lektion **17.07** (LiteLLM-Konfiguration im Detail)
→ Lektion **17.08** (Phoenix + Langfuse — was wann tracen)
→ Phase **20.05** (Audit-Logging mit OpenTelemetry GenAI)
