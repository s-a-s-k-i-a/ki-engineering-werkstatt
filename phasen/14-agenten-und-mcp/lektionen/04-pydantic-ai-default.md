---
id: 14.04
titel: Pydantic AI als Default-Framework — Agents, Dependencies, Streaming
phase: 14-agenten-und-mcp
dauer_minuten: 60
schwierigkeit: mittel
stand: 2026-04-28
voraussetzungen: [11.02, 14.01]
lernziele:
  - Pydantic-AI-Agent als typsicheres Konzept einsetzen
  - Dependencies-Injection mit `RunContext[Deps]` anwenden
  - Multi-Step-Workflows mit `iter()` und Streaming
  - MCP-Toolsets in Pydantic AI integrieren
compliance_anker:
  - typed-output-quality-gate
  - dependency-injection-statt-hardcoded-pii
ai_act_artikel:
  - art-13
  - art-15
---

## Worum es geht

> Stop wiring tools manually. — Pydantic AI gibt dir typsichere Agents mit Dependency-Injection und MCP-First-Support.

Phase 11 hat dir Pydantic AI für **Single-Output-Calls** gezeigt. Diese Lektion vertieft auf **Agent-Workflows**: Dependencies, Streaming, Iteration, MCP-Integration.

## Voraussetzungen

- Lektion 11.02 (Pydantic AI Structured Outputs)
- Lektion 14.01 (Agent-Definition)
- Aktuell: `pydantic-ai 1.85.1` (PyPI, Stand 22.04.2026).

## Konzept

### Der Agent als typisierte Klasse

```python
from dataclasses import dataclass
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext

@dataclass
class Deps:
    """Dependencies, die in Tools / System-Prompts injiziert werden."""
    db_pool: object  # echte DB-Connection
    user_id: str    # pseudonymisiert

class TerminAntwort(BaseModel):
    bestaetigung_id: str
    datum: str
    naechster_schritt: str

agent: Agent[Deps, TerminAntwort] = Agent(
    "anthropic:claude-sonnet-4-6",
    deps_type=Deps,
    output_type=TerminAntwort,
    system_prompt="Du buchst Termine im Tierheim. Auf Deutsch.",
)
```

Drei Type-Parameter zählen:

- **Deps** — was Tools / Prompts erhalten
- **Output** — Pydantic-Schema der finalen Antwort
- **Model-ID** — OpenAI / Anthropic / Mistral / Ollama / ...

→ IDE-Autocomplete, Type-Checker happy, Production-tauglich.

### Dynamische System-Prompts

```python
@agent.system_prompt
def user_kontext(ctx: RunContext[Deps]) -> str:
    """User-spezifischer System-Prompt mit DB-Lookup."""
    user_info = ctx.deps.db_pool.fetch_user(ctx.deps.user_id)
    return f"User-Sprache: {user_info.sprache}. Termine bevorzugt: {user_info.zeitfenster}."
```

Der Decorator wird **bei jedem Run** aufgerufen — System-Prompt ist also immer aktuell.

### Tools mit RunContext

```python
@agent.tool
async def freie_termine(ctx: RunContext[Deps], woche: int) -> list[dict]:
    """Liste freier Termine für die User-Region."""
    user_info = await ctx.deps.db_pool.fetch_user_async(ctx.deps.user_id)
    return await ctx.deps.db_pool.termine_in_woche(woche, user_info.region)


@agent.tool_plain
def heutiges_datum() -> str:
    """Gibt das heutige Datum zurück (kein Context nötig)."""
    from datetime import date
    return date.today().isoformat()
```

Unterschied:

- **`@agent.tool`** — bekommt `RunContext[Deps]` als ersten Parameter (Zugriff auf DB, User-ID etc.)
- **`@agent.tool_plain`** — ohne Context, statelose Funktion

### Multi-Step mit `iter()`

Der Default-Loop läuft automatisch. Wenn du **jeden Schritt inspizieren** willst (z. B. für Audit-Logging oder UI-Streaming):

```python
from pydantic_ai import Agent

async with agent.iter("Buche Termin nächste Woche", deps=Deps(db_pool, "user-123")) as run:
    async for node in run:
        print(f"Knoten: {type(node).__name__}")
        # → ModelRequestNode, ToolCallNode, ModelResponseNode, ...
        if hasattr(node, "tool_calls"):
            for tc in node.tool_calls:
                # Audit-Log jeder Tool-Call
                logger.info("tool_called", name=tc.tool_name, args=tc.args)
    final = run.result.output
```

Vorteil: jeder Schritt wird zugänglich — Token-Tracking, UI-Updates, Audit-Hooks.

### Streaming

```python
async with agent.run_stream("Erkläre Adoption", deps=deps) as stream:
    async for partial in stream.stream():
        # partial ist ein TerminAntwort-Objekt mit den
        # bisher gestreamten Feldern befüllt
        update_ui(partial)
    final = await stream.get_data()
```

Token kommen **schrittweise** rein, Pydantic validiert mit-fließend.

### Konfiguration

```python
agent = Agent(
    "anthropic:claude-sonnet-4-6",
    deps_type=Deps,
    output_type=TerminAntwort,
    output_retries=3,        # Validation-Retries (war: result_retries)
    model_settings={
        "temperature": 0.1,
        "max_tokens": 1024,
        "timeout": 30,
    },
)
```

⚠️ **Migration v0 → v1**: `result_retries` heißt jetzt `output_retries`. Code anpassen.

### MCP-Toolsets integrieren

```python
from pydantic_ai.mcp import MCPServerStdio, MCPServerStreamableHTTP

agent = Agent(
    "anthropic:claude-sonnet-4-6",
    deps_type=Deps,
    output_type=TerminAntwort,
    toolsets=[
        # Lokaler MCP-Server (Stdio)
        MCPServerStdio("uv", ["run", "python", "adoption_server.py"]),
        # Remote MCP-Server (HTTP, mit Auth)
        MCPServerStreamableHTTP(
            "https://api.example.de/mcp",
            headers={"Authorization": "Bearer TOKEN"},
        ),
    ],
)
```

→ Tools aus dem MCP-Server werden mit den `@agent.tool`-Tools gemerged. Das LLM sieht alle.

### Wann Pydantic AI, wann LangGraph?

| Kriterium | Pydantic AI | LangGraph |
|---|---|---|
| Single-Agent + Tools | ✅ | overkill |
| Komplexe State-Machines | begrenzt | ✅ |
| Persistent State / HITL | manuell | ✅ |
| Type-Safety | sehr hoch | mittel |
| Multi-Agent | OK über Sub-Agent-als-Tool | ✅ nativ |

→ **Pydantic AI als Default**, LangGraph wenn die Komplexität es rechtfertigt.

## Hands-on

Erweitere den Agent aus Lektion 11.02:

1. Füge `Deps`-Klasse mit `db_pool` und `user_id` hinzu
2. Konvertiere `@agent.tool_plain` zu `@agent.tool` mit `RunContext[Deps]`
3. Füge dynamischen System-Prompt hinzu (z. B. User-Sprache)
4. Nutze `iter()` und logge jeden Tool-Call
5. Streame die Antwort (Marimo-Notebook eignet sich gut)

## Selbstcheck

- [ ] Du erklärst, warum `Deps` besser ist als globale Variablen.
- [ ] Du kennst den Unterschied zwischen `@agent.tool` und `@agent.tool_plain`.
- [ ] Du nutzt `iter()` für Audit-Logging jedes Schritts.
- [ ] Du kennst die Migration `result_retries` → `output_retries`.
- [ ] Du integrierst MCP-Toolsets ohne Code-Duplizierung.

## Compliance-Anker

- **Dependencies-Injection statt PII im Code**: User-ID in `Deps` halten, nicht im System-Prompt einbetten.
- **`iter()` ermöglicht Audit-Hooks** vor jedem Tool-Call (siehe Phase 20.05).
- **Type-Safety = Quality-Gate (AI-Act Art. 15)**: jede Schema-Verletzung wird zur Laufzeit erkannt.

## Quellen

- Pydantic AI Docs — <https://ai.pydantic.dev/> (Zugriff 2026-04-28)
- Pydantic AI Releases — <https://github.com/pydantic/pydantic-ai/releases> (aktuell: 1.85.1, 22.04.2026)
- Pydantic AI MCP-Doc — <https://ai.pydantic.dev/mcp/>
- Migration Guide v0 → v1 — <https://ai.pydantic.dev/migration/>

## Weiterführend

→ Lektion **14.05** (LangGraph für State-Machines)
→ Lektion **14.07** (Multi-Agent — Pydantic AI als Sub-Agent in LangGraph)
