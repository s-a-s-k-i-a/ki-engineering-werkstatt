# Dev-Container & Compose-Stacks

> Reproduzierbar überall — Mac, Linux, Windows-WSL.

## Files

- `dev-container.Dockerfile` — Python 3.13 + uv + Marimo + minimaler Stack
- `compose-fullstack.yml` — Qdrant + Postgres + Phoenix + dein Code-Volume

## Schneller Start

```bash
# Dev-Container für lokales Arbeiten
docker build -f dev-container.Dockerfile -t ki-werkstatt-dev .
docker run --rm -it -v $(pwd):/work -p 2718:2718 ki-werkstatt-dev marimo edit --host 0.0.0.0

# Vollstack für Showcase 13 (RAG mit Qdrant + Phoenix)
docker compose -f compose-fullstack.yml up -d
```

## Wann nutzen

- Lehr-Workshops (alle Teilnehmer:innen identische Umgebung)
- Mac-/Win-Nutzer:innen mit zickigen Python-Setups
- CI-Reproduktion lokal
