---
id: 15.02
titel: Long-Running-Agenten — Memory-Architekturen + Postgres-Checkpointer
phase: 15-autonome-systeme
dauer_minuten: 60
schwierigkeit: fortgeschritten
stand: 2026-04-29
voraussetzungen: [15.01, 14.05]
lernziele:
  - Vier Memory-Typen (Working / Episodic / Semantic / Procedural) abgrenzen
  - LangGraph mit Postgres-Checkpointer für Persistenz
  - Memory-Pruning + Right-to-be-Forgotten
  - DACH-spezifische Memory-Compliance
compliance_anker:
  - memory-aufbewahrung
  - right-to-be-forgotten
ai_act_artikel:
  - art-12
dsgvo_artikel:
  - art-5
  - art-17
  - art-25
---

## Worum es geht

> Stop losing conversation context after each session. — Long-Running-Agenten brauchen **persistierten State** über Sessions hinweg. Postgres-Checkpointer + Vector-DB für die vier Memory-Typen.

## Voraussetzungen

- Lektion 15.01 (Autonomie-Stufen)
- Phase 14.05 (LangGraph)

## Konzept

### Vier Memory-Typen

| Typ | Inhalt | Storage | TTL |
|---|---|---|---|
| **Working** | aktuelle Konversation | LangGraph-State | bis Session-Ende |
| **Episodic** | vergangene Sessions | Postgres-Checkpointer | 90 Tage (DSGVO) |
| **Semantic** | User-Profil + Wissen | Vector-DB (Qdrant) | bis Right-to-be-Forgotten |
| **Procedural** | gelernte Patterns | LoRA-Adapter (Phase 12) | bis Re-Training |

### LangGraph Postgres-Checkpointer

URL: <https://langchain-ai.github.io/langgraph/concepts/persistence/>

```python
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph import StateGraph

# Postgres als persistente Memory
checkpointer = PostgresSaver.from_conn_string(
    "postgresql://agent:secret@postgres-eu.example.de:5432/agent_memory"
)

graph = StateGraph(AgentState)
# ... Nodes definieren ...
app = graph.compile(checkpointer=checkpointer)

# Session-ID = Thread-ID für Memory-Continuity
config = {"configurable": {"thread_id": "user-pseudonym-abc"}}

# Erste Session
app.invoke({"messages": [{"role": "user", "content": "Hallo"}]}, config=config)

# Spätere Session — kontinuiert State
app.invoke({"messages": [{"role": "user", "content": "Erinnerst du dich an gestern?"}]}, config=config)
```

### Semantic Memory mit Vector-DB

```python
from qdrant_client import QdrantClient


class SemanticMemory:
    def __init__(self, user_pseudonym: str):
        self.user = user_pseudonym
        self.client = QdrantClient(url="https://qdrant-eu.example.de")
        self.collection = f"semantic_memory_{user_pseudonym}"

    async def store(self, fact: str, kategorie: str):
        """Fakt im User-spezifischen Memory speichern."""
        embedding = await embed(fact)
        self.client.upsert(
            collection_name=self.collection,
            points=[{
                "id": hash(fact),
                "vector": embedding,
                "payload": {
                    "fact": fact,
                    "kategorie": kategorie,
                    "ts": datetime.now(UTC).isoformat(),
                }
            }],
        )

    async def recall(self, query: str, k: int = 5) -> list[dict]:
        """Top-K relevante Fakten."""
        embedding = await embed(query)
        results = self.client.search(
            collection_name=self.collection,
            query_vector=embedding,
            limit=k,
        )
        return [r.payload for r in results]
```

### Memory-Pruning (DSGVO Art. 5 lit. e)

```python
import asyncio
from datetime import datetime, UTC, timedelta


async def memory_pruning_pipeline(user_pseudonym: str):
    """Auto-Lösch-Job für alte Memory-Einträge."""
    # Working Memory: Auto-Lösch nach 24 h Inaktivität
    await delete_inactive_working_memory(user_pseudonym, age=timedelta(hours=24))

    # Episodic Memory: max. 90 Tage
    await delete_old_checkpoints(user_pseudonym, age=timedelta(days=90))

    # Semantic Memory: kein Auto-Lösch (User-Profil), nur bei Right-to-be-Forgotten
    # Procedural Memory: Adapter-Update statt Lösch
```

### Right-to-be-Forgotten (DSGVO Art. 17)

```python
async def loesch_user(user_pseudonym: str):
    """Vollständiges User-Memory löschen."""
    # 1. Working Memory
    await delete_working_memory(user_pseudonym)

    # 2. Episodic Memory (Postgres-Checkpoints)
    await postgres.execute(
        "DELETE FROM checkpoints WHERE thread_id = %s", (user_pseudonym,)
    )

    # 3. Semantic Memory (Qdrant-Collection)
    qdrant.delete_collection(f"semantic_memory_{user_pseudonym}")

    # 4. Procedural Memory: nur betroffene LoRA-Trainings-Daten markieren für Re-Training
    await mark_for_retraining(user_pseudonym)

    # 5. Audit-Log
    log_audit({
        "event": "user_forgotten",
        "user_hash": hash(user_pseudonym),
        "ts": datetime.now(UTC).isoformat(),
    })
```

> **Pflicht-Pattern** für DACH-Production: API-Endpoint `/forget-me/<user_id>` mit Audit-Log.

### Memory-Größen-Realität

Bei einem Personal-Assistant mit 1.000 aktiven Usern, 100 Konversationen pro User pro Monat:

| Memory-Typ | Größe pro User | Total für 1k User |
|---|---|---|
| Working | ~ 100 KB | ~ 100 MB |
| Episodic (Postgres) | ~ 50 MB | ~ 50 GB |
| Semantic (Qdrant) | ~ 10 MB | ~ 10 GB |
| Procedural (LoRA) | shared | ~ 100 MB |
| **Total** | ~ 60 MB | **~ 60 GB** |

→ Standard-Hetzner-Postgres-Server reicht für 10k+ User.

### Konfidenz-basierte Eskalation

```python
async def autonome_action(state, threshold: float = 0.7):
    """Eskaliere bei niedriger Konfidenz."""
    decision = await decide_with_confidence(state)

    if decision.confidence < threshold:
        log_audit({
            "event": "hitl_triggered",
            "konfidenz": decision.confidence,
            "reason": decision.reason,
        })
        return await wait_for_human_approval(state, decision)

    return await execute(decision.action)
```

> **Pflicht für L3-Autonomie**: Konfidenz-Threshold + HITL-Eskalation.

### DACH-spezifische Memory-Compliance

#### Bürger-Service-Bot (Phase 19.C)

- Pseudonym statt Klarname (DSGVO Art. 25)
- Episodic Memory **max. 30 Tage** (kürzer als Standard 90)
- Right-to-be-Forgotten Webform-Endpoint

#### Steuerberater-Mandantenchat

- Mandanten-Daten in Episodic Memory **mit AVV-Klausel**
- Procedural Memory (LoRA) **niemals** mit Mandanten-PII trainieren
- Lösung: LoRA pro Mandant + Mandanten-Bridge-Adapter

#### WP-Plugin-Helfer (Capstone 19.A)

- Code-Search ist nicht-personenbezogen → kein Memory-Pruning nötig
- Issue-Triage: Issue-Texte können PII enthalten → Pseudonymisierung pflicht

### Anti-Patterns

- ❌ User-PII direkt in LoRA-Trainings-Daten — keine RTBF möglich
- ❌ Working Memory ohne TTL — wird unendlich groß
- ❌ Episodic Memory ohne Pruning — DSGVO-Verstoß
- ❌ Konfidenz-Wert ignorieren — Hochrisiko bei niedriger Konfidenz

## Hands-on

1. LangGraph + Postgres-Checkpointer auf Hetzner-Postgres-Test
2. Multi-Session-Test mit thread_id-Persistenz
3. Memory-Pruning-Pipeline mit cron + Lösch-Logik
4. Right-to-be-Forgotten-Endpoint implementieren + audit-loggen

## Selbstcheck

- [ ] Du nennst die vier Memory-Typen + ihren Storage-Layer.
- [ ] Du nutzt LangGraph Postgres-Checkpointer für Persistenz.
- [ ] Du implementierst Memory-Pruning mit DSGVO-Aufbewahrung.
- [ ] Du baust Right-to-be-Forgotten-Endpoint.
- [ ] Du eskalierst bei Konfidenz < Threshold.

## Compliance-Anker

- **DSGVO Art. 5 lit. e**: Speicherbegrenzung — Auto-Pruning
- **DSGVO Art. 17**: Right-to-be-Forgotten — vollständiger Lösch-Workflow
- **DSGVO Art. 25**: Pseudonymisierung in Memory
- **AI-Act Art. 12**: Audit-Trail für alle Memory-Änderungen

## Quellen

- LangGraph Persistence — <https://langchain-ai.github.io/langgraph/concepts/persistence/>
- LangGraph Memory-Concepts — <https://langchain-ai.github.io/langgraph/concepts/memory/>
- DSGVO Art. 17 — <https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32016R0679>
- Phoenix Tracing — <https://arize.com/docs/phoenix/>

## Weiterführend

→ Lektion **15.03** (Hands-on: Long-Running-Agent mit Memory)
→ Phase **14.05** (LangGraph Foundation)
→ Phase **17.05** (Postgres-Stack im Docker-Compose)
