# Vektorstores — Empfehlung

> EU-Bonus = Standort + AVV. Self-Hosting ist Default für DACH-KMU.

## Empfehlungen

| Use-Case | Empfehlung |
|---|---|
| Postgres-Stack vorhanden | **pgvector** |
| Berlin-/EU-Bonus, Production | **Qdrant Cloud (EU)** oder self-hosted |
| Embedded / Edge | **LanceDB** |
| Maximale Skalierung | **Weaviate** oder **Vespa** |

## Qdrant via Docker-Compose

Siehe `qdrant-compose.yml`:

```bash
docker compose -f qdrant-compose.yml up -d
# UI: http://localhost:6333/dashboard
```

## pgvector via SQL-Init

Siehe `pgvector-init.sql`:

```bash
docker run --name pg-vec -e POSTGRES_PASSWORD=dev -p 5432:5432 -d pgvector/pgvector:pg17
psql -h localhost -U postgres -f pgvector-init.sql
```

## Compliance

- Embeddings sind invertierbar — wie Plaintext schützen
- AVV mit Vector-DB-Provider
- Bei Cloud: EU-Region erzwingen
- Bei Self-Hosting: Backup-Strategie inkl. Verschlüsselung
