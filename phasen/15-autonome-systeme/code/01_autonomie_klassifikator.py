# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "pydantic>=2.9",
# ]
# ///

"""Autonomie-Klassifikator — wann L2/L3/L4 erlaubt vs. HITL pflicht.

Smoke-Test-tauglich. Klassifiziert Use-Cases nach AI-Act + DSGVO Pflicht-Stellen.
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
        # 🤖 Autonomie-Klassifikator · Phase 15

        Klassifiziert deinen Use-Case nach Autonomie-Stufe:

        - L0-L1: Mensch macht alles / Tools assistieren
        - L2: Agent schlägt vor, Mensch entscheidet
        - L3: Agent macht, HITL bei kritisch
        - L4: vollständig autonom in Domäne
        - L5: vollständig autonom überall (existiert nicht produktiv 2026)

        Plus: AI-Act Art. 14 + DSGVO Art. 22 Pflicht-Checks.

        Stand: 29.04.2026.
        """
    )
    return


@app.cell
def _():
    """Pydantic-Schemas."""
    from typing import Literal

    from pydantic import BaseModel, Field

    class UseCaseProfil(BaseModel):
        beschreibung: str
        rechtlich_relevant: bool = Field(description="Recht / Medizin / Finanzen?")
        ai_act_hochrisiko: bool = Field(description="Anhang III?")
        destruktive_aktion: bool = Field(description="nicht reversibel?")
        cost_cap_moeglich: bool = Field(description="Token-Budget möglich?")

    class Klassifikation(BaseModel):
        empfohlene_stufe: Literal["L0-L1", "L2", "L3", "L4", "STOP"]
        begruendung: str
        pflicht_kontrollen: list[str]
        rechtsgrundlagen: list[str]

    return Klassifikation, UseCaseProfil


@app.cell
def _(Klassifikation):
    """Klassifikations-Logik."""

    def klassifiziere(profil: dict) -> Klassifikation:
        kontrollen = []
        rechtsgrundlagen = []

        # Hard Stops
        if profil["rechtlich_relevant"]:
            return Klassifikation(
                empfohlene_stufe="STOP",
                begruendung=(
                    "Rechtlich/medizinisch/finanziell relevante Entscheidungen "
                    "verlangen Mensch im Loop (DSGVO Art. 22)."
                ),
                pflicht_kontrollen=[
                    "Mensch-im-Loop Pflicht",
                    "Anfechtungsrecht für Betroffene",
                    "DSFA pflicht (Phase 20.03)",
                ],
                rechtsgrundlagen=["DSGVO Art. 22", "AI-Act Art. 14"],
            )

        if not profil["cost_cap_moeglich"]:
            return Klassifikation(
                empfohlene_stufe="STOP",
                begruendung="Cost-Cap-DoS-Risiko ohne Token-Budget zu groß.",
                pflicht_kontrollen=["Cost-Cap pflicht vor Production"],
                rechtsgrundlagen=["AI-Act Art. 13"],
            )

        # Hochrisiko = L2-L3 mit hoher HITL-Frequenz
        if profil["ai_act_hochrisiko"]:
            kontrollen.append("Konfidenz-Threshold mit HITL bei < 0.8")
            kontrollen.append("Audit-Log mind. 6 Monate")
            kontrollen.append("Human Oversight Pflicht (Art. 14)")
            rechtsgrundlagen.append("AI-Act Art. 14 + Anhang III")
            stufe = "L2"
            grund = (
                "Hochrisiko-System nach AI-Act Anhang III — Mensch-im-Loop "
                "Pflicht bei kritischen Entscheidungen."
            )
        elif profil["destruktive_aktion"]:
            kontrollen.append("HITL bei kritischen Aktionen pflicht")
            kontrollen.append("Konfidenz-Threshold mit HITL bei < 0.7")
            kontrollen.append("Audit-Log + Rollback-Mechanismus")
            rechtsgrundlagen.append("AI-Act Art. 14 (Robustness)")
            stufe = "L3"
            grund = "Destruktive Aktionen erfordern HITL bei kritisch."
        else:
            kontrollen.append("Cost-Cap pflicht (max-tokens, recursion-limit)")
            kontrollen.append("Audit-Log via Phoenix")
            kontrollen.append("Konfidenz-Tracking")
            rechtsgrundlagen.append("AI-Act Art. 13")
            stufe = "L4"
            grund = "Reversible Aktionen mit Cost-Cap = L4-Autonomie ok."

        return Klassifikation(
            empfohlene_stufe=stufe,
            begruendung=grund,
            pflicht_kontrollen=kontrollen,
            rechtsgrundlagen=rechtsgrundlagen,
        )

    return (klassifiziere,)


@app.cell
def _(klassifiziere, mo):
    """Test-Profile."""
    profile = [
        {
            "name": "Bewerbungs-Auswahl-Bot",
            "rechtlich_relevant": True,
            "ai_act_hochrisiko": True,
            "destruktive_aktion": False,
            "cost_cap_moeglich": True,
        },
        {
            "name": "Personal-Assistent (E-Mail-Drafts)",
            "rechtlich_relevant": False,
            "ai_act_hochrisiko": False,
            "destruktive_aktion": False,
            "cost_cap_moeglich": True,
        },
        {
            "name": "Code-Agent (Cursor-Stil)",
            "rechtlich_relevant": False,
            "ai_act_hochrisiko": False,
            "destruktive_aktion": True,  # git push, rm
            "cost_cap_moeglich": True,
        },
        {
            "name": "Bürger-Service-Bot",
            "rechtlich_relevant": False,  # nur Auskunft
            "ai_act_hochrisiko": True,  # öffentliche Verwaltung
            "destruktive_aktion": False,
            "cost_cap_moeglich": True,
        },
        {
            "name": "Trading-Bot",
            "rechtlich_relevant": True,  # Finanzen
            "ai_act_hochrisiko": True,
            "destruktive_aktion": True,
            "cost_cap_moeglich": True,
        },
        {
            "name": "Bookmark-Tagger (privat)",
            "rechtlich_relevant": False,
            "ai_act_hochrisiko": False,
            "destruktive_aktion": False,
            "cost_cap_moeglich": False,  # Privat-Tool, kein Cap
        },
    ]

    rows = []
    for p in profile:
        k = klassifiziere(p)
        marker = (
            "🔴"
            if k.empfohlene_stufe == "STOP"
            else "🟡"
            if k.empfohlene_stufe in ("L2", "L3")
            else "🟢"
        )
        rows.append(f"| {p['name']} | {marker} {k.empfohlene_stufe} | {k.begruendung[:60]}... |")

    mo.md(
        "## Klassifikation-Test\n\n"
        "| Use-Case | Stufe | Begründung |\n|---|---|---|\n" + "\n".join(rows)
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Autonomie-Stufen-Übersicht

        | Stufe | Beschreibung | Wann |
        |---|---|---|
        | **L0-L1** | Mensch macht alles / Tools assistieren | Standard für Hochrisiko |
        | **L2** | Agent schlägt vor, Mensch entscheidet | Hochrisiko-Systeme |
        | **L3** | Agent macht, HITL bei kritisch | destruktive Aktionen |
        | **L4** | vollständig autonom in Domäne | reversibel + Cost-Cap |
        | **L5** | vollständig autonom überall | existiert nicht 2026 |

        ## Entscheidungs-Flow

        ```mermaid
        flowchart TB
            Start[Use-Case] --> Q1{Recht/Medizin/Finanzen?}
            Q1 -->|ja| STOP[STOP — DSGVO Art. 22]
            Q1 -->|nein| Q2{Hochrisiko<br/>Anhang III?}
            Q2 -->|ja| L2[L2 — Vorschlag + Mensch entscheidet]
            Q2 -->|nein| Q3{Destruktiv?}
            Q3 -->|ja| L3[L3 — HITL bei kritisch]
            Q3 -->|nein| Q4{Cost-Cap möglich?}
            Q4 -->|ja| L4[L4 — autonom]
            Q4 -->|nein| STOP
        ```

        ## Compliance-Anker

        - **AI-Act Art. 14**: Human Oversight Pflicht für Hochrisiko
        - **DSGVO Art. 22**: Mensch bei automatisierten Entscheidungen
        - **AI-Act Art. 13**: Cost-Caps für L4-Autonomie

        ## Quellen

        - AI-Act Art. 14 — <https://artificialintelligenceact.eu/article/14/>
        - AI-Act Anhang III — <https://artificialintelligenceact.eu/annex/3/>
        - DSGVO Art. 22 — <https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32016R0679>
        """
    )
    return


if __name__ == "__main__":
    app.run()
