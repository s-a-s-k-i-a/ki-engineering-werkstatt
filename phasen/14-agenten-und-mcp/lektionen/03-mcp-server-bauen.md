---
id: 14.03
titel: Eigenen MCP-Server bauen (Python SDK 1.27)
phase: 14-agenten-und-mcp
dauer_minuten: 90
schwierigkeit: mittel
stand: 2026-04-28
voraussetzungen: [14.02]
lernziele:
  - Einen produktiven MCP-Server in Python schreiben (FastMCP)
  - Tools, Resources, Prompts mit korrektem Schema implementieren
  - Stdio- vs. HTTP-Transport entscheiden
  - Server lokal mit `mcp dev`-Inspector testen
compliance_anker:
  - mcp-tool-whitelisting
  - mcp-input-validation
ai_act_artikel:
  - art-12
  - art-15
---

## Worum es geht

> Stop integrating tools 1:1 in every LLM-app. — ein gut geschriebener MCP-Server lebt **einmal** und wird **überall** wiederverwendet.

Diese Lektion zeigt einen **echten** MCP-Server für einen Charity-Adoptions-Use-Case, smoke-test-tauglich, mit Tools, Resources und Prompts.

## Voraussetzungen

- Lektion 11.04 (MCP-Basics) und 14.02 (MCP-Spec deep dive)
- `uv add mcp` (verifiziert: `mcp 1.27.0` im Repo-Lockfile)

## Konzept

### Verzeichnis-Struktur eines MCP-Servers

```text
adoption-bot/
├── pyproject.toml
├── server.py          # Entry-Point mit FastMCP
├── tools/
│   ├── __init__.py
│   ├── termine.py     # Termin-Tools (Side-Effects)
│   └── tier_db.py     # Tier-Datenbank-Tools
├── resources/
│   ├── richtlinien.md
│   └── faq.md
└── tests/
    └── test_tools.py
```

### Server-Skelett

```python
# server.py
from mcp.server.fastmcp import FastMCP
from pathlib import Path

mcp = FastMCP(
    "Adoption-Server",
    instructions="""Server für eine Charity-Adoptions-Anwendung.
    Bietet Termin-Buchung, Tier-Profile und FAQ-Resources.""",
)

# === TOOLS ===

@mcp.tool()
def freie_termine(woche: int, kalenderjahr: int = 2026) -> list[dict]:
    """Liste freier Termine in der angegebenen Kalenderwoche.

    Args:
        woche: KW-Nummer (1-53).
        kalenderjahr: Jahr (Default: 2026).

    Returns:
        Liste von dicts mit `datum`, `uhrzeit`, `mitarbeiter:in`.
    """
    if not 1 <= woche <= 53:
        raise ValueError(f"woche muss zwischen 1 und 53 liegen, war {woche}")
    # echte DB-Abfrage hier
    return [
        {"datum": "2026-04-29", "uhrzeit": "10:00", "mitarbeiter:in": "Anna"},
        {"datum": "2026-05-01", "uhrzeit": "14:00", "mitarbeiter:in": "Bernd"},
    ]


@mcp.tool()
def buche_termin(datum: str, uhrzeit: str, name: str, telefon: str) -> str:
    """Bucht einen Beratungstermin.

    Args:
        datum: ISO-Datum, z. B. '2026-04-29'.
        uhrzeit: 'HH:MM'-Format.
        name: Name der Person (max. 100 Zeichen).
        telefon: Telefon mit Vorwahl.

    Returns:
        Bestätigungs-ID als String.
    """
    # Argument-Validierung (zusätzlich zum Schema)
    from datetime import datetime

    datetime.strptime(datum, "%Y-%m-%d")  # raised ValueError bei Fehler
    datetime.strptime(uhrzeit, "%H:%M")
    if not name.strip() or len(name) > 100:
        raise ValueError("Name muss zwischen 1 und 100 Zeichen sein")
    if not telefon.replace("+", "").replace(" ", "").isdigit():
        raise ValueError("Telefon enthält ungültige Zeichen")
    # echte Logik
    return f"BOOK-{datum}-{uhrzeit.replace(':', '')}-{hash(name) % 10000:04d}"


# === RESOURCES (read-only Daten) ===

@mcp.resource("adoption://richtlinien")
def adoptions_richtlinien() -> str:
    """Aktuelle Adoptions-Richtlinien (CC BY-SA 4.0)."""
    pfad = Path(__file__).parent / "resources" / "richtlinien.md"
    return pfad.read_text(encoding="utf-8")


@mcp.resource("adoption://faq")
def adoptions_faq() -> str:
    """Häufig gestellte Fragen rund um Adoption."""
    pfad = Path(__file__).parent / "resources" / "faq.md"
    return pfad.read_text(encoding="utf-8")


@mcp.resource("adoption://tier/{tier_id}")
def tier_profil(tier_id: str) -> dict:
    """Profil eines Tieres (alphanumerische ID)."""
    if not tier_id.isalnum() or len(tier_id) > 32:
        raise ValueError("Ungültige tier_id")
    return {
        "id": tier_id,
        "name": "Bella",
        "rasse": "Mischling",
        "alter_jahre": 4,
        "vermittelbar_ab": "2026-04-30",
    }


# === PROMPTS (User-Slash-Commands) ===

@mcp.prompt()
def beratungsgespraech(thema: str, ton: str = "freundlich") -> str:
    """Vorlage für ein Beratungsgespräch.

    Args:
        thema: Worum geht's? (z. B. 'Adoption Hund')
        ton: Sprachton (Default: 'freundlich')
    """
    return f"""Du bist Berater:in einer deutschen Tierschutz-Organisation.
Thema: {thema}.
Antworte im Ton: {ton}. Knappe deutsche Sätze.

Was sind die typischen Erstfragen, die du der interessierten Person stellst?"""


if __name__ == "__main__":
    mcp.run(transport="stdio")  # für lokale Clients
    # Production: mcp.run(transport="streamable-http", host="0.0.0.0", port=8080)
```

### Test mit `mcp dev`

```bash
uv run mcp dev server.py
# → öffnet UI auf http://localhost:6274
```

Du kannst:

- **Tools** einzeln aufrufen mit Test-Argumenten
- **Resources** lesen (mit URI-Templates)
- **Prompts** anwenden mit Parametern
- **Session-Log** sehen (Audit-Output)

### In Claude Desktop registrieren

`~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):

```json
{
  "mcpServers": {
    "adoption-bot": {
      "command": "uv",
      "args": [
        "--directory", "/pfad/zu/adoption-bot",
        "run", "python", "server.py"
      ]
    }
  }
}
```

Claude Desktop neu starten → Server erscheint im UI als „🔌 adoption-bot".

### HTTP-Transport für Multi-Tenant-Production

```python
if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8080,
        # Production: Auth aktivieren!
    )
```

OAuth2-Mechanismus aus Lektion 14.02 anwenden.

### Sicherheits-Pattern (Pflicht)

```python
import re
from typing import Annotated
from pydantic import Field, AfterValidator

def kein_pii(text: str) -> str:
    """Filter offensichtliche PII aus User-Input."""
    if re.search(r"\b\d{3,}\b", text):  # Telefon-/Karten-Nummern
        raise ValueError("Möglicherweise PII erkannt — bitte entfernen.")
    return text

@mcp.tool()
def textverarbeitung(
    text: Annotated[str, AfterValidator(kein_pii), Field(max_length=2000)],
) -> str:
    """Verarbeitet Text und gibt Zusammenfassung zurück."""
    return f"Zusammenfassung: {text[:200]}..."
```

## Hands-on (45 Min.)

```bash
mkdir adoption-bot && cd adoption-bot
uv init && uv add mcp
mkdir resources

# server.py erstellen (Code oben kopieren)
# resources/richtlinien.md und resources/faq.md mit Beispiel-Content füllen

# Lokal testen
uv run mcp dev server.py
# → Inspector öffnet, du siehst alle Tools / Resources / Prompts

# In Claude Desktop registrieren (siehe oben), Claude neu starten,
# Server-Symbol erscheint, du kannst die Tools direkt im Chat nutzen
```

## Selbstcheck

- [ ] Du hast einen MCP-Server mit mind. 2 Tools, 2 Resources, 1 Prompt geschrieben.
- [ ] Du testest ihn mit `mcp dev` lokal.
- [ ] Du implementierst Argument-Validierung in Tools (nicht nur via Schema).
- [ ] Du registrierst den Server in Claude Desktop oder einem anderen Client.

## Compliance-Anker

- **Tool-Whitelisting**: nur explizit dekorierte Tools sind sichtbar — gut.
- **Input-Validation (AI-Act Art. 15)**: zusätzlich zum JSON-Schema validieren (siehe `kein_pii`-Beispiel).
- **Audit-Logging**: alle Tool-Aufrufe loggen (Phase 20.05 zeigt das Pattern).
- **Resource-Lesen kann Side-Effect sein** (z. B. DB-Audit-Log) → bewusst designen.

## Quellen

- MCP Python SDK — <https://github.com/modelcontextprotocol/python-sdk> (verifiziert: `mcp 1.27.0`)
- MCP Server-Liste — <https://github.com/modelcontextprotocol/servers>
- FastMCP Tutorial — <https://github.com/jlowin/fastmcp>

## Weiterführend

→ Lektion **14.04** (Pydantic AI mit MCP-Toolset)
→ Lektion **14.07** (Multi-Agent — mehrere MCP-Server gleichzeitig)
