---
id: 17.05
titel: Docker-Compose Multi-LLM-Stack — vLLM + LiteLLM + Postgres + Phoenix
phase: 17-production-und-eu-hosting
dauer_minuten: 60
schwierigkeit: mittel
stand: 2026-04-28
voraussetzungen: [17.02, 17.07]
lernziele:
  - Production-tauglichen Multi-LLM-Stack mit Docker-Compose orchestrieren
  - GPU-Passthrough an Container konfigurieren (NVIDIA Container Toolkit)
  - Service-Dependencies + Healthchecks definieren
  - Volumes, Networks, Secrets sauber strukturieren
  - Wann Docker-Compose, wann K8s
compliance_anker:
  - infrastructure-as-code
  - secret-management
ai_act_artikel:
  - art-12
dsgvo_artikel:
  - art-32
---

## Worum es geht

> Stop running pip-installed services on bare metal. — Docker-Compose ist 2026 immer noch der Sweet-Spot für Single-Box-Production: ein YAML, ein `docker compose up`, und du hast vLLM + LiteLLM + Postgres + Phoenix als reproduzierbaren Stack. K8s ist Overkill für ≤ 4 GPUs.

## Voraussetzungen

- Lektion 17.02 (vLLM)
- Lektion 17.07 (LiteLLM Proxy — kommt direkt nach dieser, gerne vor- oder rückwärts lesen)
- Docker + NVIDIA Container Toolkit installiert ([nvidia-docker2 GitHub](https://github.com/NVIDIA/nvidia-docker))

## Konzept

### Reference-Stack

```mermaid
flowchart TB
    Client[Client / IDE / Browser] --> Caddy[Caddy<br/>TLS-Terminator]
    Caddy --> LiteLLM[LiteLLM Proxy<br/>:4000]
    LiteLLM --> vLLM[vLLM<br/>:8000<br/>GPU]
    LiteLLM --> EU[EU-Cloud-Provider<br/>STACKIT/IONOS/OVH]
    LiteLLM --> Redis[Redis<br/>:6379<br/>Semantic Cache]
    LiteLLM --> PG[(Postgres<br/>:5432<br/>Spend + Logs)]
    LiteLLM -- OTel --> Phoenix[Phoenix<br/>:6006<br/>Tracing]
    Phoenix --> PG2[(Postgres oder SQLite)]

    classDef ext fill:#FF6B3D,color:#0E1116
    classDef svc fill:#3D8BFF,color:#FFF
    class Client,Caddy,EU ext
    class LiteLLM,vLLM,Redis,PG,Phoenix,PG2 svc
```

### `docker-compose.yml` Skelett

```yaml
services:
  # Reverse-Proxy mit automatischen Let's-Encrypt-Zertifikaten
  caddy:
    image: caddy:2-alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile:ro
      - caddy_data:/data
    depends_on:
      - litellm
    restart: unless-stopped

  # LiteLLM Proxy — Multi-Provider-Routing + Cost-Tracking
  litellm:
    image: ghcr.io/berriai/litellm:main-stable
    ports:
      - "127.0.0.1:4000:4000"
    environment:
      - DATABASE_URL=postgresql://litellm:${POSTGRES_PASSWORD}@postgres:5432/litellm
      - LITELLM_MASTER_KEY=${LITELLM_MASTER_KEY}
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - IONOS_API_KEY=${IONOS_API_KEY}
    volumes:
      - ./litellm-config.yaml:/app/config.yaml:ro
    command: ["--config", "/app/config.yaml", "--port", "4000"]
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: unless-stopped

  # vLLM mit GPU-Passthrough
  vllm:
    image: vllm/vllm-openai:v0.20.0
    ports:
      - "127.0.0.1:8000:8000"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    environment:
      - HF_TOKEN=${HF_TOKEN}
    command:
      - --model=meta-llama/Llama-3.3-70B-Instruct
      - --quantization=awq
      - --max-model-len=32768
      - --gpu-memory-utilization=0.92
      - --enable-prefix-caching
    volumes:
      - hf_cache:/root/.cache/huggingface
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 5m  # Modell-Lade-Zeit
    restart: unless-stopped

  # Phoenix — Tracing + Eval-Dashboards
  phoenix:
    image: arizephoenix/phoenix:version-14
    ports:
      - "127.0.0.1:6006:6006"
      - "127.0.0.1:4317:4317"  # OTel-gRPC
    environment:
      - PHOENIX_SQL_DATABASE_URL=postgresql://phoenix:${POSTGRES_PASSWORD}@postgres:5432/phoenix
    depends_on:
      postgres:
        condition: service_healthy
    restart: unless-stopped

  # Redis — Semantic Cache
  redis:
    image: redis:7-alpine
    command: ["redis-server", "--maxmemory", "2gb", "--maxmemory-policy", "allkeys-lru"]
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
    restart: unless-stopped

  # Postgres — Shared für LiteLLM + Phoenix
  postgres:
    image: postgres:17-alpine
    environment:
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_MULTIPLE_DATABASES=litellm,phoenix
    volumes:
      - pg_data:/var/lib/postgresql/data
      - ./init-multi-db.sh:/docker-entrypoint-initdb.d/init-multi-db.sh:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
    restart: unless-stopped

volumes:
  caddy_data:
  hf_cache:
  pg_data:
```

### `Caddyfile`

```text
ki.example.de {
    reverse_proxy litellm:4000
    encode gzip
}

phoenix.example.de {
    reverse_proxy phoenix:6006
    basicauth {
        admin {env.PHOENIX_HASHED_PASSWORD}
    }
}
```

> Caddy holt automatisch Let's-Encrypt-Zertifikate. Phoenix-Dashboard kommt hinter Basic-Auth — niemals direkt ans Internet.

### `.env`-Datei (NICHT committen!)

```text
# .env — gitignored, mit gitleaks/trufflehog gescannt
LITELLM_MASTER_KEY=sk-prod-...
POSTGRES_PASSWORD=...
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
IONOS_API_KEY=...
HF_TOKEN=hf_...
PHOENIX_HASHED_PASSWORD=...  # via caddy hash-password
```

### NVIDIA Container Toolkit Setup

Vor `docker compose up`:

```bash
# Ubuntu / Debian
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/libnvidia-container/gpgkey \
    | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list \
    | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' \
    | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Test
docker run --rm --gpus all nvidia/cuda:12.4.0-base-ubuntu22.04 nvidia-smi
```

### Service-Healthchecks

Wichtige Pattern:

- **vLLM** ist langsam beim Start (Modell-Download + GPU-Init). `start_period: 5m` gibt ihm Zeit.
- **Postgres** muss vor LiteLLM + Phoenix laufen (`condition: service_healthy`).
- **Redis** ist schnell, aber LiteLLM hängt sich auf, wenn Cache-Backend fehlt → Healthcheck.
- **Caddy** startet zuletzt — wenn LiteLLM nicht antwortet, gibt Caddy 502, aber bricht nicht ab.

### Backup-Strategie

Postgres ist der einzige stateful Service. Nightly-Backup via cron:

```bash
docker compose exec -T postgres \
    pg_dumpall -U postgres > /backup/pg-$(date +%F).sql
```

> Beachte: bei Self-Hosting ist **du** der Backup-Verantwortliche. Restore-Test alle 3 Monate (Phase 20.05 hat das Audit-Pattern).

### Wann Docker-Compose, wann K8s?

| Faktor | Docker-Compose | K8s |
|---|---|---|
| GPU-Anzahl | 1–4 | 5+ |
| Nodes | Single-Box | Multi-Node-Cluster |
| Auto-Scaling | nein | ja (HPA) |
| Failover | nein (manuell) | ja (Pod-Reschedule) |
| Setup-Komplexität | niedrig | hoch |
| Operations-Aufwand | minimal | nicht-trivial |
| Wann | Dev, Staging, Single-Box-Production | Multi-GPU + Multi-Model |

> Faustregel: **Docker-Compose bis 4 GPUs auf einer Hetzner-Box / IONOS-Server**. Ab 5 GPUs oder Multi-Node: Helm + K8s (Lektion 17.06).

## Hands-on

1. Repo `infrastruktur/docker/` clonen oder lokal aufsetzen
2. `.env` ausfüllen, `docker compose up -d`
3. `curl http://localhost:4000/v1/chat/completions` mit `Authorization: Bearer $LITELLM_MASTER_KEY`
4. Phoenix-Dashboard öffnen — der erste Trace muss erscheinen
5. Backup-Skript einrichten + einen Restore-Test durchspielen

## Selbstcheck

- [ ] Du orchestrierst vLLM + LiteLLM + Postgres + Phoenix in einer `docker-compose.yml`.
- [ ] GPU-Passthrough funktioniert (`nvidia-smi` im Container).
- [ ] Healthchecks und Service-Dependencies sind sauber.
- [ ] `.env` ist gitignored und gitleaks-clean.
- [ ] Postgres-Backup-Pipeline läuft.

## Compliance-Anker

- **Infrastructure-as-Code**: `docker-compose.yml` + `Caddyfile` werden versioniert (Audit-Trail).
- **Secret-Management (DSGVO Art. 32)**: API-Keys in `.env`, never im Image / Compose-File.
- **TOM**: Caddy Let's-Encrypt-TLS für jede externe API, basicauth für Dashboards.

## Quellen

- Docker Compose Spec — <https://docs.docker.com/compose/compose-file/>
- NVIDIA Container Toolkit — <https://github.com/NVIDIA/nvidia-docker>
- Caddy Docs — <https://caddyserver.com/docs/>
- LiteLLM Docker — <https://docs.litellm.ai/docs/proxy/deploy>
- vLLM Docker — <https://docs.vllm.ai/en/stable/serving/deploying_with_docker.html>
- Phoenix Self-Hosting — <https://arize.com/docs/phoenix/self-hosting>

## Weiterführend

→ Lektion **17.06** (Helm / K8s — wenn Compose nicht mehr reicht)
→ Lektion **17.07** (LiteLLM-Konfiguration im Detail)
→ Phase **20.05** (Audit-Logging + Backup-Pattern)
