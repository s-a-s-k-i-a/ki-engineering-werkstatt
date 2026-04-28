---
id: 11.02
titel: Structured Outputs mit Pydantic AI
phase: 11-llm-engineering
dauer_minuten: 60
schwierigkeit: mittel
stand: 2026-04-28
voraussetzungen: [11.01]
lernziele:
  - Pydantic AI v1.x als Multi-Provider-Framework einsetzen
  - LLM-Outputs zu validierten Pydantic-Modellen formen
  - Validierungsfehler robust mit Retry behandeln
  - Multi-Provider-Switching ohne Code-Änderung
compliance_anker:
  - typed-output-quality-gate
ai_act_artikel:
  - art-13
  - art-15
---

## Worum es geht

> Stop guessing what your LLM returned. — Pydantic AI macht aus „freier Text" ein **typsicheres Schema**.

**Pydantic AI** (aktuelle Version 1.87.0, 25.04.2026) ist das Production-Framework des Pydantic-Teams für LLM-Apps. Es kombiniert:

- **Pydantic v2-Modelle** als Output-Schema (Validierung, Typsicherheit)
- **Multi-Provider-Support** (OpenAI, Anthropic, Mistral, Gemini, DeepSeek, Ollama, ...)
- **Tool-/Function-Calling** mit Type-Hints
- **Streaming** mit fortlaufender Validierung

Domain-Hinweis (Stand 2026): `ai.pydantic.dev` redirected auf `pydantic.dev/docs/ai/`.

## Voraussetzungen

- Lektion 11.01 (Prompt-Patterns)
- Phase 00.04 (Ollama) **oder** ein API-Key (z. B. Anthropic, IONOS)

## Konzept

### Warum strukturierte Outputs?

Klassischer LLM-Aufruf gibt Freitext zurück. In Production willst du **JSON, das validiert ist**:

```python
# Klassisch (zerbrechlich):
text = response.choices[0].message.content
# → "Die Stadt heißt Berlin und hat etwa 3,7 Millionen Einwohner."
# → musst regex/parsing schreiben

# Structured Output mit Pydantic AI:
class StadtInfo(BaseModel):
    stadt: str
    einwohner: int

result = agent.run_sync(...).output
# → StadtInfo(stadt="Berlin", einwohner=3_700_000)
# → typsicher, validiert, IDE-Autocomplete
```

### Hello, Pydantic AI

Installation:

```bash
uv add pydantic-ai
```

Minimal-Beispiel mit Ollama (lokal):

```python
from pydantic import BaseModel
from pydantic_ai import Agent

class Adoptions_FAQ_Antwort(BaseModel):
    """Strukturierte Antwort auf eine FAQ-Frage."""
    kurzantwort: str
    benötigte_dokumente: list[str]
    nächster_schritt: str

agent = Agent(
    "ollama:qwen3:8b",  # läuft lokal!
    output_type=Adoptions_FAQ_Antwort,
    system_prompt=(
        "Du bist Assistenz einer deutschen Tierschutz-Organisation. "
        "Antworte auf Deutsch, knapp und korrekt."
    ),
)

result = agent.run_sync("Was brauche ich, um einen Hund zu adoptieren?")
print(result.output)
# → Adoptions_FAQ_Antwort(
#     kurzantwort='Du brauchst Personalausweis, Adressnachweis...',
#     benötigte_dokumente=['Personalausweis', 'Adressnachweis', ...],
#     nächster_schritt='Vereinbare einen Termin im Tierheim.',
#   )
```

Was passiert hier:

1. Pydantic AI sendet das Schema als JSON-Schema an das LLM
2. LLM antwortet im JSON-Format gemäß Schema
3. Pydantic AI **validiert** die Antwort gegen `Adoptions_FAQ_Antwort`
4. Bei Validierungsfehler: automatischer Retry mit Fehler-Beschreibung
5. Du bekommst ein typsicheres Pydantic-Objekt

### Tool-/Function-Calling

```python
@agent.tool_plain
def freie_termine(woche: int) -> list[str]:
    """Liste freier Termine für die gegebene Kalenderwoche."""
    # Hier: deine echte Logik (DB-Query etc.)
    return ["Mo 10:00", "Mi 14:00", "Do 15:30"]
```

Pydantic AI:

- Liest Funktions-Signatur und Docstring
- Generiert automatisch das Tool-Schema
- Schickt es als „Tool" an das LLM
- Wenn das LLM das Tool aufruft, ruft Pydantic AI deine Funktion mit validierten Argumenten auf

### Multi-Provider-Switching

Ein Agent, mehrere Provider — Code bleibt identisch:

```python
# OpenAI
agent = Agent("openai:gpt-5-4-mini", output_type=...)
# Anthropic
agent = Agent("anthropic:claude-sonnet-4-6", output_type=...)
# Mistral (Frankreich)
agent = Agent("mistral:mistral-medium-3-1", output_type=...)
# IONOS (Deutschland)
agent = Agent(
    "openai:meta-llama/Llama-3.1-8B-Instruct",
    output_type=...,
    api_key=os.environ["IONOS_AI_API_KEY"],
    base_url="https://openai.inference.de-txl.ionos.com/v1",
)
# Ollama lokal
agent = Agent("ollama:qwen3:8b", output_type=...)
```

→ Du baust einmal, deployst gegen jeden Anbieter. Lektion 11.05 zeigt den Live-Vergleich.

### Retry-Logik

Wenn das Modell ein Schema-Verstoß produziert (z. B. `"einwohner": "drei Millionen"` statt int), passiert:

1. Pydantic-Validierung scheitert mit `ValidationError`
2. Pydantic AI sendet die Fehlermeldung zurück ans Modell
3. Modell korrigiert
4. Repeat — Default 3 Versuche

Du kannst das konfigurieren:

```python
agent = Agent(..., retries=5)
```

### Streaming mit Validierung

```python
async with agent.run_stream(user_input) as stream:
    async for partial in stream.stream():
        # partial ist ein StadtInfo-Objekt mit den bisher
        # gestreamten Feldern befüllt
        print(partial)
```

Die Pydantic-Modelle werden live mit-validiert, während die Tokens reinkommen.

## Hands-on

```python
# /tmp/test_pydantic_ai.py
from pydantic import BaseModel, Field
from pydantic_ai import Agent

class Klassifikation(BaseModel):
    kategorie: str = Field(description="Login | Abrechnung | Kündigung | Sonstiges")
    konfidenz: float = Field(ge=0.0, le=1.0)
    begründung: str

agent = Agent(
    "ollama:qwen3:8b",
    output_type=Klassifikation,
    system_prompt="Du klassifizierst Support-Anfragen auf Deutsch.",
)

beispiele = [
    "Ich kann mich nicht einloggen",
    "Meine letzte Rechnung ist falsch",
    "Wie kündige ich mein Abo?",
    "Wo ist mein Paket?",
]

for b in beispiele:
    r = agent.run_sync(b)
    print(f"{b:50s} → {r.output.kategorie} ({r.output.konfidenz:.2f})")
```

```bash
uv run python /tmp/test_pydantic_ai.py
```

## Selbstcheck

- [ ] Du erklärst, warum Pydantic AI gegenüber dem nackten OpenAI-SDK Mehrwert bringt.
- [ ] Du kennst die `output_type=`-Syntax und ihre Pydantic-v2-Validierung.
- [ ] Du verstehst, dass `@agent.tool_plain` Schema **automatisch** aus Type-Hints + Docstring ableitet.
- [ ] Du wechselst Provider, ohne Geschäftslogik anzupassen — nur `Agent("anbieter:modell", ...)`.

## Compliance-Anker

- **Quality-Gate (AI-Act Art. 15)**: typsichere Outputs erleichtern automatisierte Tests und Audits — Schema-Drift wird sofort sichtbar.
- **Tech-Doku (Art. 11)**: Pydantic-Modelle sind selbst-dokumentierend. Du kannst sie direkt in deine API-Doku einbetten.
- **Datenschutz**: Validierung verhindert ungewollten Datenfluss („PII im Output, weil Modell halluziniert hat" → Pydantic erkennt das, wenn dein Schema strikt ist).

## Quellen

- Pydantic AI Docs — <https://pydantic.dev/docs/ai/overview/> (Zugriff 2026-04-28)
- Pydantic AI Releases — <https://github.com/pydantic/pydantic-ai/releases> (aktuell v1.87.0)
- Pydantic v2 Docs — <https://docs.pydantic.dev/latest/>

## Weiterführend

→ Lektion **11.03** (Function Calling / Tool Use — Tools tiefer)
→ Lektion **11.04** (MCP — Tool-Standardisierung über Prozess-Grenzen)
→ Phase **14** (Agenten — Pydantic AI als Default-Framework)
