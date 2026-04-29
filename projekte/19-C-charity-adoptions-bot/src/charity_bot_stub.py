# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "pydantic>=2.9",
# ]
# ///

"""Charity-Adoptions-Bot Stub — Capstone 19.C.

Smoke-Test-tauglich: keine echten LLM-/ASR-/TTS-Calls. Stub-State-Machine
zeigt LangGraph-HITL-Pattern. Vollversion siehe README.md.
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
        # 🐕 Charity-Adoptions-Bot · Capstone 19.C

        Stub-Pipeline für End-to-End-Adoptions-Flow:

        - **verstehe_anfrage** (Pydantic AI extrahiert TierVorlieben)
        - **suche_tiere** (RAG-Stub)
        - **schlage_termin_vor** (HITL — pausiert für Approval)
        - **buche_termin** (nach Approval)
        - **sende_email** (Bestätigung)

        Smoke-Test-tauglich (keine externen Calls). Vollversion siehe README.md.
        """
    )
    return


@app.cell
def _():
    """Pydantic-Schemas."""
    from typing import Literal

    from pydantic import BaseModel, Field

    class TierVorlieben(BaseModel):
        art: Literal["Hund", "Katze", "Kleintier"]
        alter_max: int = Field(ge=0, le=20)
        eigenschaften: list[str] = Field(max_length=5)
        haus_groesse: Literal["klein", "mittel", "gross"] | None = None
        kinder_im_haushalt: bool | None = None

    class TierProfil(BaseModel):
        id: str
        art: str
        alter: int
        rasse: str
        eigenschaften: list[str]
        match_score: float = Field(ge=0.0, le=1.0)

    class TerminVorschlag(BaseModel):
        tag: str
        uhrzeit: str
        tier_id: str
        mitarbeiter_pseudonym: str

    class AdoptionsResult(BaseModel):
        user_pseudonym: str
        vorlieben: TierVorlieben
        kandidaten: list[TierProfil]
        termin: TerminVorschlag | None = None
        approved: bool = False
        bestaetigungs_id: str | None = None
        status: Literal[
            "init",
            "verstanden",
            "gematcht",
            "termin_vorgeschlagen",
            "approved",
            "gebucht",
            "abgeschlossen",
            "abgebrochen",
        ] = "init"

    return AdoptionsResult, TerminVorschlag, TierProfil, TierVorlieben


@app.cell
def _(AdoptionsResult, TerminVorschlag, TierProfil, TierVorlieben):
    """Stub-State-Machine."""

    def verstehe_anfrage(user_msg: str, user_pseudonym: str) -> AdoptionsResult:
        """Stub: extrahiert TierVorlieben aus User-Anfrage."""
        # Naive Heuristik (in Production: Pydantic AI mit Claude Sonnet 4.6)
        msg = user_msg.lower()
        art = "Hund" if "hund" in msg else "Katze" if "katze" in msg else "Kleintier"
        alter_max = 5 if "jung" in msg else 12 if "senior" in msg or "alt" in msg else 8
        eigenschaften = []
        if "ruhig" in msg:
            eigenschaften.append("ruhig")
        if "kind" in msg or "famili" in msg:
            eigenschaften.append("kindertauglich")
        if "wohnung" in msg:
            eigenschaften.append("wohnungstauglich")

        vorlieben = TierVorlieben(
            art=art,
            alter_max=alter_max,
            eigenschaften=eigenschaften[:5],
            kinder_im_haushalt="kind" in msg or "famili" in msg,
        )
        return AdoptionsResult(
            user_pseudonym=user_pseudonym,
            vorlieben=vorlieben,
            kandidaten=[],
            status="verstanden",
        )

    def suche_tiere(state: AdoptionsResult) -> AdoptionsResult:
        """Stub: 3 Tier-Kandidaten."""
        kandidaten = [
            TierProfil(
                id="bello-001",
                art=state.vorlieben.art,
                alter=8,
                rasse="Mischling",
                eigenschaften=["ruhig", "kindertauglich"],
                match_score=0.92,
            ),
            TierProfil(
                id="luna-002",
                art=state.vorlieben.art,
                alter=4,
                rasse="Border Collie",
                eigenschaften=["aktiv", "intelligent"],
                match_score=0.65,
            ),
            TierProfil(
                id="max-003",
                art=state.vorlieben.art,
                alter=11,
                rasse="Senior-Mischling",
                eigenschaften=["ruhig", "anhänglich"],
                match_score=0.78,
            ),
        ]
        kandidaten.sort(key=lambda k: k.match_score, reverse=True)
        return state.model_copy(update={"kandidaten": kandidaten[:3], "status": "gematcht"})

    def schlage_termin_vor(state: AdoptionsResult) -> AdoptionsResult:
        """Stub: Termin-Vorschlag — in Production: interrupt() für Mitarbeiter-Approval."""
        if not state.kandidaten:
            return state.model_copy(update={"status": "abgebrochen"})
        bestes_tier = state.kandidaten[0]
        termin = TerminVorschlag(
            tag="Mi",
            uhrzeit="14:00",
            tier_id=bestes_tier.id,
            mitarbeiter_pseudonym="MA-007",
        )
        return state.model_copy(update={"termin": termin, "status": "termin_vorgeschlagen"})

    def mitarbeiter_approval_stub(state: AdoptionsResult, approve: bool) -> AdoptionsResult:
        """Stub: Mitarbeiter-Approval — in Production: HITL via interrupt()."""
        if not approve:
            return state.model_copy(update={"approved": False, "status": "abgebrochen"})
        return state.model_copy(update={"approved": True, "status": "approved"})

    def buche_termin(state: AdoptionsResult) -> AdoptionsResult:
        """Stub: Termin-Buchung nach Approval."""
        if not state.approved:
            return state.model_copy(update={"status": "abgebrochen"})
        return state.model_copy(
            update={
                "bestaetigungs_id": "buch-2026-04-001",
                "status": "gebucht",
            }
        )

    def sende_email(state: AdoptionsResult) -> AdoptionsResult:
        """Stub: E-Mail wird in Production via SMTP versendet."""
        if state.status != "gebucht":
            return state
        return state.model_copy(update={"status": "abgeschlossen"})

    return (
        buche_termin,
        mitarbeiter_approval_stub,
        schlage_termin_vor,
        sende_email,
        suche_tiere,
        verstehe_anfrage,
    )


@app.cell
def _(
    buche_termin,
    mitarbeiter_approval_stub,
    mo,
    schlage_termin_vor,
    sende_email,
    suche_tiere,
    verstehe_anfrage,
):
    """Test mit 3 Adoptions-Anfragen."""
    test_anfragen = [
        (
            "buerger-001",
            "Hallo, ich suche einen ruhigen Senior-Hund für unsere Familie mit 2 Kindern.",
        ),
        (
            "buerger-002",
            "Wir möchten eine wohnungstaugliche Katze adoptieren — sind beide berufstätig.",
        ),
        ("buerger-003", "Ich suche ein junges Kaninchen für meinen Sohn."),
    ]

    rows = []
    for pseudonym, msg in test_anfragen:
        # State-Machine durchlaufen
        s = verstehe_anfrage(msg, pseudonym)
        s = suche_tiere(s)
        s = schlage_termin_vor(s)
        s = mitarbeiter_approval_stub(s, approve=True)  # Simuliere MA-Approval
        s = buche_termin(s)
        s = sende_email(s)

        bestes = s.kandidaten[0] if s.kandidaten else None
        bestes_id = bestes.id if bestes else "—"
        bestes_score = f"{bestes.match_score:.2f}" if bestes else "—"
        status_marker = "✅ " if s.status == "abgeschlossen" else "⚠️ "
        rows.append(
            f"| {pseudonym} | {s.vorlieben.art} | "
            f"{bestes_id} | {bestes_score} | "
            f"{status_marker}{s.status} |"
        )

    mo.md(
        "## Test-Adoptions-Anfragen (Stub)\n\n"
        "| Pseudonym | Art | Bestes Match | Score | Status |\n|---|---|---|---|---|\n"
        + "\n".join(rows)
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Vollversion-Wegweiser

        ```python
        from langgraph.graph import StateGraph
        from langgraph.types import interrupt

        graph = StateGraph(AdoptionState)
        graph.add_node("verstehe_anfrage", verstehe_anfrage)
        # ...

        # HITL-Pattern in schlage_termin_vor:
        def schlage_termin_vor(state):
            termin = ...
            bestaetigt = interrupt({"frage": f"Termin {termin} ok?"})
            return {"termin": termin, "approved": bestaetigt}

        # Compile mit Postgres-Checkpointer für State-Persistenz
        app = graph.compile(
            checkpointer=PostgresCheckpointer(...),
            interrupt_before=["schlage_termin_vor"],
        )
        ```

        ## DSGVO-Pattern

        - **`user_pseudonym`** statt Klarname (Hash der Email)
        - **AVV** mit Anthropic Enterprise (München-Office)
        - **HITL** via `interrupt()` — keine vollautomatische Entscheidung (Art. 22)
        - **Audit-Logging** via Phoenix mit Hashes statt PII
        - **Right-to-be-Forgotten**: Lösch-Endpoint für Pseudonym → Klarnamen-Mapping

        ## Compliance-Anker

        - **AI-Act Art. 14** (Human Oversight): HITL via `interrupt()`
        - **AI-Act Art. 50** (Transparenz): „Du sprichst mit einer KI"-Hinweis
        - **DSGVO Art. 22** (Automatisierte Entscheidungen): Mitarbeiter-Approval pflicht
        - **DSGVO Art. 25** (Privacy by Design): Pseudonyme von Anfang an

        ## Quellen

        - LangGraph HITL — <https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/>
        - Whisper-large-v3 — <https://huggingface.co/openai/whisper-large-v3>
        - Phoenix Tracing — <https://arize.com/docs/phoenix/>
        - Phase 14.09 (Pattern-Bauanleitung)
        """
    )
    return


if __name__ == "__main__":
    app.run()
