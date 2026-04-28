---
id: 0.06
titel: Dev-Container mit Docker (optional, für Linux/WSL)
phase: 00-werkzeugkasten
dauer_minuten: 30
schwierigkeit: einsteiger
stand: 2026-04-28
voraussetzungen: [0.02]
lernziele:
  - Den Sinn von Dev-Containern für KI-Projekte erklären (reproducible Setup)
  - Eine `devcontainer.json` für VS Code lesen und schreiben
  - Docker-Compose für Multi-Service-Stacks nutzen (Ollama + Qdrant + Phoenix)
  - Wann ein Dev-Container nicht nötig ist
compliance_anker:
  - reproducible-environment
colab_badge: false
---

## Worum es geht

> Stop saying „auf meinem Rechner läuft's". — ein Dev-Container ist eine versionierte, reproduzierbare Maschine.

Ein **Dev-Container** ist ein Docker-Image, das deine gesamte Entwicklungsumgebung beschreibt: OS, Python-Version, Pakete, VS-Code-Extensions, Ports. Wer den Container startet, hat **identisch dasselbe Setup wie du**.

## Voraussetzungen

- Phase 00.02 (uv installiert)
- Docker Desktop (macOS/Win) oder Docker Engine (Linux): <https://www.docker.com/products/docker-desktop/>
- VS Code mit „Dev Containers" Extension (optional, aber empfohlen)

## Wann du das brauchst — und wann nicht

| Situation | Dev-Container? |
|---|---|
| Du arbeitest allein auf deinem Mac | nicht nötig |
| Workshop mit 20 Teilnehmer:innen, alle sollen identisches Setup haben | sehr empfohlen |
| Mehrere Co-Maintainer auf verschiedenen OS | empfohlen |
| Du willst RAG-Stack lokal mit Qdrant + Phoenix testen | empfohlen (Compose) |
| GitHub Codespaces / Cloud-IDE | Pflicht |
| CI-Reproduktion lokal | sehr empfohlen |

Wenn dein Setup auf macOS / Linux mit `uv sync` durchläuft, ist ein Dev-Container Bonus, kein Pflicht.

## Konzept

### `devcontainer.json` — minimales Beispiel

Lege im Repo `.devcontainer/devcontainer.json` an:

```json
{
  "name": "ki-engineering-werkstatt",
  "image": "mcr.microsoft.com/devcontainers/python:3.13-bookworm",
  "features": {
    "ghcr.io/astral-sh/uv:1": {}
  },
  "postCreateCommand": "uv sync --all-extras --dev",
  "customizations": {
    "vscode": {
      "extensions": [
        "charliermarsh.ruff",
        "ms-python.python",
        "marimo-team.vscode-marimo"
      ]
    }
  },
  "forwardPorts": [2718, 11434, 6006, 6333],
  "remoteUser": "vscode"
}
```

Was das macht:

- **`image`**: offizielles Microsoft-Dev-Container-Image mit Python 3.13 auf Debian 12 (Bookworm)
- **`features`**: lädt automatisch das `uv`-Feature aus `ghcr.io/astral-sh/uv:1`
- **`postCreateCommand`**: nach Container-Start: `uv sync` mit allen Extras
- **`extensions`**: Ruff, Python, Marimo VS Code-Extensions vorinstallieren
- **`forwardPorts`**:
  - 2718 → Marimo
  - 11434 → Ollama
  - 6006 → Phoenix (Observability)
  - 6333 → Qdrant (Vector-DB)

### VS Code öffnen

```bash
# Im Repo-Verzeichnis
code .
# → VS Code fragt: "Reopen in Container?" → Ja
# → Dev-Container baut, ~ 2-5 Min beim ersten Mal, dann <10 s
```

### Multi-Service-Stack mit Docker-Compose

Wenn du mehr als nur Python brauchst (für Phase 13 RAG: Qdrant + Phoenix dazu), nutze `docker-compose`. Im Werkstatt-Repo gibt es schon ein Beispiel:

```yaml
# infrastruktur/docker/compose-fullstack.yml (Auszug)
services:
  qdrant:
    image: qdrant/qdrant:v1.12.4
    ports: ["6333:6333"]
    volumes: [qdrant_data:/qdrant/storage]

  postgres:
    image: pgvector/pgvector:pg17
    environment: { POSTGRES_PASSWORD: dev }
    ports: ["5432:5432"]

  phoenix:
    image: arizephoenix/phoenix:latest
    ports: ["6006:6006"]

volumes:
  qdrant_data:
```

Starten:

```bash
cd /pfad/zum/repo
docker compose -f infrastruktur/docker/compose-fullstack.yml up -d
# Phoenix UI: http://localhost:6006
# Qdrant UI:  http://localhost:6333/dashboard
```

Stoppen:

```bash
docker compose -f infrastruktur/docker/compose-fullstack.yml down
```

### GitHub Codespaces

Wenn dein Repo eine `.devcontainer/devcontainer.json` hat, kannst du es **direkt im Browser** in GitHub Codespaces starten:

1. Auf GitHub: Repo öffnen → Button **„Code"** → **„Codespaces"**
2. „Create codespace on main"
3. Cloud-IDE startet, nach ~ 2 Min. ist alles bereit

Das nutzt GitHub-Server (4-Core / 8 GB RAM kostenlos für 60 h/Monat). Für reine Lehr-Demos super, für GPU-Workloads zu schwach.

## Hands-on (15 Min., optional)

```bash
# 1. Docker installieren (siehe Voraussetzungen)
docker --version

# 2. Dev-Container-Datei anlegen
mkdir -p .devcontainer
cat > .devcontainer/devcontainer.json <<'EOF'
{
  "name": "ki-test",
  "image": "mcr.microsoft.com/devcontainers/python:3.13-bookworm",
  "features": { "ghcr.io/astral-sh/uv:1": {} },
  "postCreateCommand": "uv --version",
  "remoteUser": "vscode"
}
EOF

# 3. In VS Code öffnen, "Reopen in Container" wählen.
# Nach 2-5 Min: VS Code läuft im Container, du siehst unten links "Dev Container: ki-test"

# 4. Im Container-Terminal verifizieren
uv --version
# → uv 0.11.8

# 5. Container verlassen: VS Code → Command Palette → "Dev Containers: Reopen Folder Locally"
```

## Selbstcheck

- [ ] Du verstehst, dass Dev-Container = Docker-Image + VS-Code-Konfig.
- [ ] Du kannst eine minimale `devcontainer.json` selbst schreiben.
- [ ] Du weißt, wann Dev-Container Pflicht sind (Workshops, Codespaces) und wann optional.
- [ ] Du kannst `docker compose up -d` für Multi-Service-Stacks (Qdrant, Phoenix) ausführen.

## Compliance-Anker

- **Reproduzierbarkeit (AI-Act Art. 11)**: Dev-Container + `uv.lock` = lückenlose Reproduzierbarkeit.
- **Onboarding (AI Literacy, Art. 4)**: Neue Mitarbeitende sind in 5 Min. produktiv, statt 5 Tage Setup-Hölle. Reduziert Onboarding-Drift.
- **Datenschutz**: Dev-Container kapselt Test-Daten — sie verlassen den Container nur explizit.

## Quellen

- VS Code Dev Containers Docs — <https://code.visualstudio.com/docs/devcontainers/containers> (Zugriff 2026-04-28)
- Dev Container Spec — <https://containers.dev>
- Microsoft Container Registry, Python-Devcontainer-Tags — <https://mcr.microsoft.com/en-us/product/devcontainers/python/about>
- Astral uv Devcontainer-Feature — <https://github.com/astral-sh/setup-uv>
- Docker Compose Spec — <https://docs.docker.com/compose/compose-file/>

## Weiterführend

→ Lektion **00.07** (Markt & Realität) — du verstehst jetzt, wie KI-Projekte aufgesetzt werden. Was sagt der Markt?
→ Phase **17** (Production EU-Hosting) — Dev-Container + Helm-Charts für K8s-Deployment
