# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "pydantic>=2.9",
# ]
# ///

"""Lösungs-Skelett — Übung 11.01 — Support-Klassifikator mit Pydantic AI + Eval.

Dieses Notebook ist eine Vorlage. Trage deine eigenen API-Keys in `.env` ein
und tausche den Stub gegen echte Pydantic-AI-Aufrufe.

Smoke-Test-tauglich: keine externen API-Calls, nur Stub-Antworten.
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
        # 🎯 Lösung Übung 11.01 — Support-Klassifikator

        Ein Pydantic-AI-Agent mit:

        1. Strukturiertem Output (`SupportKlassifikation`)
        2. Tool-Calling (`kontostand_pruefen`)
        3. Multi-Provider-Vergleich (Stub für Smoke, echt mit Keys)
        4. Promptfoo-Eval-Setup
        """
    )
    return


@app.cell
def _():
    """Pydantic-Modell für strukturierten Output."""
    from typing import Literal

    from pydantic import BaseModel, Field

    class SupportKlassifikation(BaseModel):
        kategorie: Literal["Login", "Abrechnung", "Kündigung", "Sonstiges"]
        dringlichkeit: int = Field(ge=1, le=5)
        naechster_schritt: str = Field(min_length=10, max_length=200)
        tool_call_empfohlen: bool

    return (SupportKlassifikation,)


@app.cell
def _(SupportKlassifikation):
    """Tool als Mock — wird vom Agent aufgerufen, wenn passend."""

    def kontostand_pruefen(kunden_id: str) -> dict:
        """Mock: gibt Kontostand für Kunden-ID zurück."""
        # In Production: DB-Abfrage
        return {
            "kunden_id": kunden_id,
            "stand_eur": 247.50,
            "naechste_rechnung": "2026-05-15",
        }

    # Smoke-Stub: würde mit Pydantic AI als @agent.tool_plain registriert
    test_kontostand = kontostand_pruefen("TEST-001")
    assert test_kontostand["kunden_id"] == "TEST-001"
    return (kontostand_pruefen,)


@app.cell
def _(SupportKlassifikation):
    """Stub-Klassifikator (smoke-test-tauglich, keine API-Calls).

    In der Vollversion ersetzt durch:

        from pydantic_ai import Agent
        agent = Agent("anthropic:claude-sonnet-4-6", output_type=SupportKlassifikation)
        result = agent.run_sync(email_text)
    """

    def stub_klassifikator(email_text: str) -> SupportKlassifikation:
        """Stub-Logik: nutzt simple Keyword-Matching für Smoke-Test."""
        text_lower = email_text.lower()
        if "passwort" in text_lower or "einloggen" in text_lower:
            return SupportKlassifikation(
                kategorie="Login",
                dringlichkeit=3,
                naechster_schritt="Passwort-Reset-Link an User senden.",
                tool_call_empfohlen=False,
            )
        if "rechnung" in text_lower or "kontostand" in text_lower:
            return SupportKlassifikation(
                kategorie="Abrechnung",
                dringlichkeit=2,
                naechster_schritt="Kontostand prüfen, Detail-Rechnung anbieten.",
                tool_call_empfohlen=True,
            )
        if "kündig" in text_lower or "abo beend" in text_lower:
            return SupportKlassifikation(
                kategorie="Kündigung",
                dringlichkeit=4,
                naechster_schritt="Kündigungs-Workflow starten, Retention-Angebot prüfen.",
                tool_call_empfohlen=False,
            )
        return SupportKlassifikation(
            kategorie="Sonstiges",
            dringlichkeit=1,
            naechster_schritt="An menschlichen Support eskalieren.",
            tool_call_empfohlen=False,
        )

    return (stub_klassifikator,)


@app.cell
def _(mo, stub_klassifikator):
    """Test-Beispiele."""
    test_emails = [
        "Ich kann mich seit gestern nicht einloggen, mein Passwort funktioniert nicht.",
        "Die letzte Rechnung ist unklar. Können Sie meinen Kontostand prüfen? KdNr: 4711",
        "Wie kündige ich mein Abo? Ich möchte zum Monatsende beenden.",
        "Wann sind eure Öffnungszeiten?",
        "Mein Account zeigt einen falschen Namen an.",
    ]

    rows_test = []
    for email in test_emails:
        k = stub_klassifikator(email)
        rows_test.append(
            f"| {email[:60]}{'...' if len(email) > 60 else ''} | "
            f"{k.kategorie} | {k.dringlichkeit} | {k.tool_call_empfohlen} |"
        )

    mo.md(
        "## Test-Ergebnisse (Stub)\n\n"
        "| E-Mail | Kategorie | Dringlichkeit | Tool? |\n|---|---|---|---|\n" + "\n".join(rows_test)
    )
    return (test_emails,)


@app.cell
def _(mo):
    """Promptfoo-Konfig als Vorlage."""
    promptfoo_config = """description: "Support-Klassifikator Eval (Übung 11.01)"

prompts:
  - "Klassifiziere die folgende Support-E-Mail in: Login, Abrechnung, Kündigung, Sonstiges. Antworte als JSON.\\n\\nE-Mail: {{email}}"
  - "Du bist Support-Mitarbeiter:in. Klassifiziere die folgende E-Mail mit Begründung. JSON-Format.\\n\\nE-Mail: {{email}}"

providers:
  - id: anthropic:claude-sonnet-4-6
  - id: openai:gpt-5-4-mini

tests:
  - vars: { email: "Ich kann mich nicht einloggen" }
    assert:
      - type: contains
        value: "Login"
      - type: cost
        threshold: 0.001
  - vars: { email: "Meine Rechnung ist falsch" }
    assert:
      - type: contains
        value: "Abrechnung"
  - vars: { email: "Ich möchte kündigen" }
    assert:
      - type: contains
        value: "Kündigung"
  - vars: { email: "Wie sind eure Öffnungszeiten?" }
    assert:
      - type: contains
        value: "Sonstiges"
  - vars: { email: "Wo ist mein Paket? Ich warte seit 3 Wochen." }
    assert:
      - type: llm-rubric
        value: "Antwort erkennt Sonstiges-Kategorie und schlägt Eskalation an Versand-Service vor"
"""

    mo.md(
        "## Promptfoo-Konfiguration (Vorlage)\n\n"
        "Speichere als `loesungen/promptfooconfig.yaml` und starte mit `npx promptfoo eval`.\n\n"
        f"```yaml\n{promptfoo_config}```"
    )
    return (promptfoo_config,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Echte Pydantic-AI-Variante (für deinen Fork)

        Mit API-Keys in `.env`:

        ```python
        from pydantic_ai import Agent

        # Anthropic
        agent_claude = Agent(
            "anthropic:claude-sonnet-4-6",
            output_type=SupportKlassifikation,
            system_prompt="Du klassifizierst Support-E-Mails auf Deutsch.",
        )

        @agent_claude.tool_plain
        def kontostand_pruefen(kunden_id: str) -> dict:
            \"\"\"Liefert Kontostand für die gegebene Kunden-ID.\"\"\"
            return {"kunden_id": kunden_id, "stand_eur": 247.50}

        # Identischer Aufruf, anderer Provider:
        agent_gpt = Agent(
            "openai:gpt-5-4-mini",
            output_type=SupportKlassifikation,
            system_prompt="Du klassifizierst Support-E-Mails auf Deutsch.",
        )

        for provider, agent in [("Claude", agent_claude), ("GPT", agent_gpt)]:
            r = agent.run_sync("Ich kann mich nicht einloggen")
            print(f"{provider}: {r.output}")
            print(f"  Tokens: {r.usage().total_tokens}")
        ```

        ## Compliance-Anker

        - **AVV** mit Anthropic + OpenAI (Enterprise-Tier mit EU-Datazone)
        - **PII-Filter** vor LLM-Call: Kunden-IDs pseudonymisieren
        - **Audit-Log** mit Hash der E-Mail-Inhalte (siehe Phase 20.05)
        - **Promptfoo-CI-Gate** vor Production-Deploy
        """
    )
    return


if __name__ == "__main__":
    app.run()
