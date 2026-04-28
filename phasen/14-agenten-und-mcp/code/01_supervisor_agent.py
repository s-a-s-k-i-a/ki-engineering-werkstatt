# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "pydantic>=2.9",
# ]
# ///

"""Supervisor-Agent-Demo — zeigt Multi-Agent-Pattern mit Stub-Logik.

Smoke-Test-tauglich: keine externen API-Calls. Stub-Klassifikator + Stub-Sub-Agents.
Volle Variante mit Pydantic AI + echten Modellen siehe Lektion 14.07.
"""

import marimo

__generated_with = "0.23.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
        # 🎯 Supervisor-Agent-Demo · Phase 14

        Dieses Notebook zeigt das **Supervisor-Worker-Pattern** mit drei Sub-Agents:

        - **Recherche-Agent** — beantwortet Wissens-Fragen
        - **Mathe-Agent** — löst Berechnungen
        - **Termin-Agent** — bucht Termine

        Der Supervisor entscheidet, welcher Sub-Agent zuständig ist, sammelt das
        Ergebnis und gibt eine konsolidierte Antwort zurück.

        Smoke-Test-tauglich (keine API-Calls). In der Vollversion ersetzt du die
        Stub-Sub-Agents durch echte `pydantic_ai.Agent`-Instanzen.
        """
    )
    return


@app.cell
def _():
    """Sub-Agent-Stubs."""
    from typing import Literal

    from pydantic import BaseModel, Field

    class SubAgentAntwort(BaseModel):
        agent: Literal["recherche", "mathe", "termin"]
        antwort: str = Field(min_length=1, max_length=500)
        konfidenz: float = Field(ge=0.0, le=1.0)

    def recherche_agent(frage: str) -> SubAgentAntwort:
        """Stub: würde mit Pharia / Mistral / Claude beantwortet."""
        antworten = {
            "berlin": "Berlin hat etwa 3,7 Mio. Einwohner.",
            "ai act": "Der AI Act (EU 2024/1689) regelt KI-Pflichten ab Feb 2025.",
            "dsgvo": "Die DSGVO ist seit 25.05.2018 in Kraft.",
        }
        for key, val in antworten.items():
            if key in frage.lower():
                return SubAgentAntwort(agent="recherche", antwort=val, konfidenz=0.95)
        return SubAgentAntwort(agent="recherche", antwort="Keine Antwort gefunden.", konfidenz=0.3)

    def mathe_agent(aufgabe: str) -> SubAgentAntwort:
        """Stub: würde mit GPT-5.4 oder DeepSeek-R1 beantwortet."""
        try:
            # Naive Eval — in echt: SymPy oder LLM
            import re

            # Suche „X % von Y" Pattern
            m = re.search(r"(\d+)\s*%\s*von\s*(\d[\d.,]*)", aufgabe)
            if m:
                prozent = float(m.group(1))
                zahl_str = m.group(2).replace(".", "").replace(",", ".")
                zahl = float(zahl_str)
                ergebnis = zahl * prozent / 100
                return SubAgentAntwort(
                    agent="mathe",
                    antwort=f"{prozent}% von {zahl:,.0f} = {ergebnis:,.0f}".replace(",", "."),
                    konfidenz=1.0,
                )
            return SubAgentAntwort(
                agent="mathe", antwort="Konnte Aufgabe nicht parsen.", konfidenz=0.2
            )
        except Exception:
            return SubAgentAntwort(agent="mathe", antwort="Fehler bei Berechnung.", konfidenz=0.0)

    def termin_agent(anfrage: str) -> SubAgentAntwort:
        """Stub: würde MCP-Tool `freie_termine` rufen."""
        return SubAgentAntwort(
            agent="termin",
            antwort="Frei: Mo 10:00, Mi 14:00, Do 15:30 (KW 18, 2026).",
            konfidenz=0.9,
        )

    return SubAgentAntwort, mathe_agent, recherche_agent, termin_agent


@app.cell
def _(SubAgentAntwort, mathe_agent, recherche_agent, termin_agent):
    """Supervisor-Logik: einfache Routing-Heuristik (in echt: LLM)."""

    def supervisor_route(frage: str) -> SubAgentAntwort:
        """Routet die Frage an den passenden Sub-Agent.

        In Production: ein LLM (z. B. Claude Sonnet 4.6) entscheidet anhand
        einer Tool-Auswahl-Prompt, welcher Sub-Agent gerufen wird.
        """
        f_lower = frage.lower()
        if any(k in f_lower for k in ["%", "rechne", "wieviel", "summe"]):
            return mathe_agent(frage)
        if any(k in f_lower for k in ["termin", "frei", "uhr", "datum"]):
            return termin_agent(frage)
        return recherche_agent(frage)

    return (supervisor_route,)


@app.cell
def _(mo, supervisor_route):
    """Demo-Anfragen."""
    fragen = [
        "Wie viele Einwohner hat Berlin?",
        "Was ist 12 % von 3.700.000?",
        "Welche Termine sind in KW 18 frei?",
        "Wann ist die DSGVO in Kraft getreten?",
        "Berechne 5 % von 8.000",
    ]

    rows = []
    for frage in fragen:
        antwort_obj = supervisor_route(frage)
        rows.append(
            f"| {frage[:50]}{'...' if len(frage) > 50 else ''} | "
            f"**{antwort_obj.agent}** | {antwort_obj.antwort} | "
            f"{antwort_obj.konfidenz:.2f} |"
        )

    mo.md(
        "## Demo-Anfragen + Routing\n\n"
        "| Frage | Sub-Agent | Antwort | Konfidenz |\n"
        "|---|---|---|---|\n" + "\n".join(rows)
    )
    return (fragen,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## In der Vollversion (mit Pydantic AI)

        ```python
        from pydantic_ai import Agent

        # Sub-Agents
        recherche = Agent(
            "anthropic:claude-haiku-4-5",
            output_type=SubAgentAntwort,
            system_prompt="Du beantwortest Wissens-Fragen knapp.",
        )

        mathe = Agent(
            "openai:gpt-5-4-mini",
            output_type=SubAgentAntwort,
            system_prompt="Du löst mathematische Probleme.",
        )

        termin = Agent(
            "anthropic:claude-haiku-4-5",
            output_type=SubAgentAntwort,
            system_prompt="Du buchst Termine via MCP-Tool.",
            toolsets=[MCPServerStdio("uv", ["run", "python", "adoption_server.py"])],
        )

        # Supervisor mit Sub-Agents als Tools
        supervisor = Agent("anthropic:claude-sonnet-4-6")

        @supervisor.tool_plain
        async def frage_recherche(frage: str) -> SubAgentAntwort:
            return (await recherche.run(frage)).output

        @supervisor.tool_plain
        async def frage_mathe(aufgabe: str) -> SubAgentAntwort:
            return (await mathe.run(aufgabe)).output

        @supervisor.tool_plain
        async def buche_termin(anfrage: str) -> SubAgentAntwort:
            return (await termin.run(anfrage)).output

        result = await supervisor.run("Wie viele Einwohner hat Berlin, und was ist 12 % davon?")
        ```

        ## Compliance-Anker

        - **Audit-Trail**: jeder Sub-Agent-Aufruf = eigenes Phoenix-Span (siehe Lektion 11.10)
        - **Cost-Caps**: Multi-Agent kostet 5–10× mehr Tokens; Token-Budget pflicht
        - **Tool-Whitelisting**: Sub-Agents als Tools, nicht „alle Funktionen"

        ## Quellen

        - Anthropic „Building Effective Agents" — <https://www.anthropic.com/research/building-effective-agents>
        - Pydantic AI Multi-Agent — <https://ai.pydantic.dev/multi-agent/>
        - LangGraph Supervisor — <https://github.com/langchain-ai/langgraph/tree/main/libs/langgraph-supervisor>
        """
    )
    return


if __name__ == "__main__":
    app.run()
