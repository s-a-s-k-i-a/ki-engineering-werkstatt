---
id: 15.03
titel: Hands-on — Long-Running-Personal-Assistant mit 4-Schicht-Memory
phase: 15-autonome-systeme
dauer_minuten: 180
schwierigkeit: experte
stand: 2026-04-29
voraussetzungen: [15.01, 15.02, 14.05]
lernziele:
  - End-to-End Long-Running-Agent mit allen 4 Memory-Schichten
  - L3-Autonomie mit Konfidenz-Eskalation
  - DSGVO-konforme Memory-Pruning + RTBF-Endpoint
  - Phoenix-Audit-Trail
compliance_anker:
  - end-to-end-autonomous-audit
ai_act_artikel:
  - art-12
  - art-13
  - art-14
dsgvo_artikel:
  - art-17
  - art-22
  - art-25
---

## Worum es geht

> Stop building stateless chatbots. — diese Lektion baut **end-to-end** einen Long-Running-Personal-Assistenten mit 4-Schicht-Memory + L3-Autonomie + DSGVO-RTBF.

## Voraussetzungen

- Lektionen 15.01 + 15.02
- Phase 14.05 (LangGraph)

## Konzept

### Architektur

```mermaid
flowchart TB
    User --> UI[Chat-UI]
    UI --> LG[LangGraph<br/>State-Machine]

    LG --> WM[Working Memory<br/>State]
    LG --> EM[Episodic<br/>Postgres-Checkpointer]
    LG --> SM[Semantic<br/>Qdrant Berlin]
    LG --> PM[Procedural<br/>LoRA-Adapter]

    LG --> Conf{Konfidenz<br/>Check}
    Conf -->|>=0.7| Auto[Auto-Action]
    Conf -->|<0.7| HITL[HITL-Eskalation]

    LG --> Phoenix[Phoenix<br/>Audit-Trail]
    LG --> Cron[Auto-Pruning<br/>Cron]
    LG --> RTBF[/forget-me/<br/>Endpoint]

    classDef ext fill:#FF6B3D,color:#0E1116
    classDef int fill:#3D8BFF,color:#FFF
    class User,UI,HITL,RTBF ext
    class LG,WM,EM,SM,PM,Conf,Auto,Phoenix,Cron int
```

### Schritt 1 — State + Memory definieren

```python
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.types import interrupt
from qdrant_client import QdrantClient
from datetime import datetime, UTC
import hashlib


class AssistantState(TypedDict):
    messages: Annotated[list, add_messages]
    user_pseudonym: str
    session_id: str
    konfidenz: float
    benoetigte_tools: list[str]
    semantic_recall: list[dict]


# Postgres für Episodic Memory
checkpointer = PostgresSaver.from_conn_string(
    "postgresql://agent:secret@postgres-eu.example.de:5432/assistant"
)

# Qdrant für Semantic Memory
qdrant = QdrantClient(url="https://qdrant-eu.example.de")
```

### Schritt 2 — Memory-Recall-Node

```python
async def recall_node(state: AssistantState) -> dict:
    """Lade Semantic Memory für aktuelle Konversation."""
    last_msg = state["messages"][-1].content

    # Embed Query
    embedding = await embed_de(last_msg)

    # Top-5 aus User-spezifischem Memory
    user_collection = f"semantic_{state['user_pseudonym']}"
    try:
        recall = qdrant.search(
            collection_name=user_collection,
            query_vector=embedding,
            limit=5,
        )
        facts = [r.payload for r in recall]
    except Exception:
        facts = []  # Erste Session — noch kein Memory

    return {"semantic_recall": facts}
```

### Schritt 3 — Konfidenz-basierte-Decision-Node

```python
from pydantic import BaseModel, Field
from pydantic_ai import Agent


class DecisionWithConfidence(BaseModel):
    aktion: str
    konfidenz: float = Field(ge=0.0, le=1.0)
    begruendung: str
    benoetigte_tools: list[str]


decide_agent = Agent(
    "anthropic:claude-sonnet-4-6",
    output_type=DecisionWithConfidence,
    system_prompt=(
        "Du bist Personal Assistant. Entscheide nächste Aktion + gib Konfidenz "
        "(0.0–1.0) an. Bei niedriger Konfidenz oder destruktiver Aktion: "
        "expliziter Hinweis."
    ),
)


async def decide_node(state: AssistantState) -> dict:
    context = build_prompt(state["messages"], state["semantic_recall"])
    decision = (await decide_agent.run(context)).output

    return {
        "konfidenz": decision.konfidenz,
        "benoetigte_tools": decision.benoetigte_tools,
    }
```

### Schritt 4 — HITL-Eskalation bei niedriger Konfidenz

```python
async def execute_or_escalate_node(state: AssistantState) -> dict:
    """Auto-Aktion oder HITL je nach Konfidenz."""
    if state["konfidenz"] < 0.7:
        # HITL via interrupt()
        approved = interrupt({
            "frage": (
                f"Konfidenz {state['konfidenz']:.0%} — Aktion: "
                f"{state.get('aktion')}. OK?"
            ),
            "user": state["user_pseudonym"],
        })
        if not approved:
            return {"messages": [{"role": "assistant", "content": "Aktion abgebrochen."}]}

    # Auto-Aktion
    result = await execute_action(state)
    return {"messages": [{"role": "assistant", "content": result}]}
```

### Schritt 5 — Memory-Update-Node

```python
async def update_memory_node(state: AssistantState) -> dict:
    """Speichere wichtige Fakten in Semantic Memory."""
    last_assistant = state["messages"][-1].content
    last_user = state["messages"][-2].content

    # Extrahiere wichtige Fakten via LLM
    facts = await extract_facts(last_user, last_assistant)

    # Speichern in User-spezifischem Memory
    user_collection = f"semantic_{state['user_pseudonym']}"
    for fact in facts:
        embedding = await embed_de(fact["text"])
        qdrant.upsert(
            collection_name=user_collection,
            points=[{
                "id": hash(fact["text"]),
                "vector": embedding,
                "payload": {
                    "fact": fact["text"],
                    "kategorie": fact["kategorie"],
                    "ts": datetime.now(UTC).isoformat(),
                },
            }],
        )

    return {}
```

### Schritt 6 — Komplette State-Machine

```python
graph = StateGraph(AssistantState)
graph.add_node("recall", recall_node)
graph.add_node("decide", decide_node)
graph.add_node("execute", execute_or_escalate_node)
graph.add_node("update_memory", update_memory_node)

graph.set_entry_point("recall")
graph.add_edge("recall", "decide")
graph.add_edge("decide", "execute")
graph.add_edge("execute", "update_memory")
graph.set_finish_point("update_memory")

# Compile mit Postgres-Checkpointer + interrupt vor execute
app = graph.compile(
    checkpointer=checkpointer,
    interrupt_before=["execute"],  # immer Eskalations-Stelle
)
```

### Schritt 7 — RTBF-Endpoint

```python
from fastapi import FastAPI

api = FastAPI()


@api.post("/forget-me/{user_pseudonym}")
async def forget_me(user_pseudonym: str):
    """DSGVO Art. 17 Right-to-be-Forgotten."""
    # 1. Working Memory löschen (laufende Threads)
    # ... (in LangGraph: alle Threads für user_pseudonym beenden)

    # 2. Episodic Memory (Postgres)
    await postgres.execute(
        "DELETE FROM checkpoints WHERE thread_id LIKE %s",
        (f"{user_pseudonym}%",),
    )

    # 3. Semantic Memory (Qdrant)
    qdrant.delete_collection(f"semantic_{user_pseudonym}")

    # 4. Audit-Log (mit Hash, nicht Klartext)
    log_audit({
        "event": "user_forgotten",
        "user_hash": hashlib.sha256(user_pseudonym.encode()).hexdigest()[:16],
        "ts": datetime.now(UTC).isoformat(),
    })

    return {"status": "deleted", "user_hash": "..."}
```

### Schritt 8 — Auto-Pruning-Cron

```python
import asyncio
from datetime import timedelta


async def pruning_cron():
    """Läuft täglich, prunet alte Memory-Einträge."""
    while True:
        await asyncio.sleep(86400)  # 24 h

        # Working Memory: Threads inaktiv > 24 h
        await postgres.execute(
            """
            DELETE FROM checkpoints
            WHERE last_active < NOW() - INTERVAL '24 hours'
            AND status = 'active'
            """
        )

        # Episodic: max. 90 Tage
        await postgres.execute(
            """
            DELETE FROM checkpoints
            WHERE created_at < NOW() - INTERVAL '90 days'
            """
        )

        # Semantic: nur RTBF-Trigger (kein Auto-Lösch)
        log_audit({"event": "memory_pruning_run", "ts": datetime.now(UTC).isoformat()})
```

### Phoenix-Tracing für Audit

```python
from phoenix.otel import register

register(
    project_name="long-running-assistant",
    auto_instrument=True,  # alle LangGraph + Pydantic-AI-Calls automatisch
)
```

Im Phoenix-UI: jeder Memory-Recall, jede Konfidenz-Entscheidung, jede HITL-Eskalation als Span sichtbar — DSFA-tauglicher Audit-Trail.

## Hands-on (4-6 h)

1. LangGraph + Postgres-Checkpointer + Qdrant lokal aufsetzen
2. State-Machine mit den 4 Nodes implementieren
3. Multi-Session-Test mit Pseudonym-Memory-Continuity
4. RTBF-Endpoint testen — alle 3 Memory-Schichten löschen
5. Konfidenz < 0,7 Test — HITL muss eskalieren
6. Phoenix-Tracing aktivieren + Spans prüfen

## Selbstcheck

- [ ] Du baust End-to-End-Long-Running-Agent mit 4 Memory-Schichten.
- [ ] Du implementierst Konfidenz-basierte HITL-Eskalation.
- [ ] Du baust RTBF-Endpoint mit Audit-Log.
- [ ] Du planst Auto-Pruning-Cron.
- [ ] Du tracest mit Phoenix für DSFA-Audit.

## Compliance-Anker

- **AI-Act Art. 14**: Konfidenz-Eskalation als Human-Oversight
- **DSGVO Art. 17**: RTBF-Endpoint vollständig
- **DSGVO Art. 22**: HITL bei kritischen Entscheidungen
- **DSGVO Art. 25**: Pseudonyme + Hash-only-Logging

## Quellen

- LangGraph Persistence — <https://langchain-ai.github.io/langgraph/concepts/persistence/>
- LangGraph Memory — <https://langchain-ai.github.io/langgraph/concepts/memory/>
- Phoenix Tracing — <https://arize.com/docs/phoenix/>
- Qdrant Cloud — <https://qdrant.tech/>

## Weiterführend

→ Phase **17.05** (Docker-Compose-Stack mit Postgres + Qdrant + Phoenix)
→ Phase **18.07** (Red-Teaming gegen Memory-Leakage)
→ Phase **20** (DSFA + AVV für Long-Running-Agenten)
