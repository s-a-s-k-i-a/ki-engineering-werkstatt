# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "pydantic>=2.9",
# ]
# ///

"""Lösungs-Skelett — Übung 15.01 — Autonomie + 4-Schicht-Memory.

Smoke-test-tauglich. Reine Pydantic-Logik.
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
        # 🎯 Lösung Übung 15.01 — Autonomie-Klassifikation + Memory

        Drei Use-Cases → L-Stufe + 4-Schicht-Memory + RTBF + HITL.
        """
    )
    return


@app.cell
def _():
    """Pydantic-Profil-Schema."""
    from pydantic import BaseModel

    class AutonomieProfil(BaseModel):
        name: str
        aktion_typ: str  # "info_only", "reversibel", "destruktiv", "entscheidung"
        rechtsrelevant: bool
        betroffene: str  # "person", "behoerde", "kommerziell"
        cost_cap_moeglich: bool
        konfidenz_hoch: bool
        ai_act_anhang_iii: bool

    return (AutonomieProfil,)


@app.cell
def _():
    """Klassifikations-Logik."""

    def klassifiziere(p) -> dict:
        if p.ai_act_anhang_iii and p.aktion_typ == "entscheidung":
            return {
                "stufe": "STOP",
                "begruendung": "AI-Act Anhang III + DSGVO Art. 22 (automatisierte Entscheidung)",
                "kontrollen": ["zwingender Mensch-im-Loop", "Anfechtungs-Recht", "Logik-Erklärung"],
            }
        if p.rechtsrelevant:
            return {
                "stufe": "L2",
                "begruendung": "rechtlich-relevant → Mensch entscheidet",
                "kontrollen": ["Vorschlag + Mensch entscheidet", "Audit-Trail", "RDG-Disclaimer"],
            }
        if p.aktion_typ == "destruktiv":
            return {
                "stufe": "L3",
                "begruendung": "destruktive Aktion → HITL bei kritisch",
                "kontrollen": ["HITL bei kritischen Operationen", "Reversibilitäts-Check"],
            }
        if p.cost_cap_moeglich and p.konfidenz_hoch:
            return {
                "stufe": "L4",
                "begruendung": "reversibel + Cost-Cap + hohe Konfidenz",
                "kontrollen": ["Cost-Cap", "Auto-Audit pro Run", "Konfidenz-Eskalation < 0.85"],
            }
        return {
            "stufe": "L2-L3",
            "begruendung": "Standard-Default für unklare Cases",
            "kontrollen": ["Vorschlag + Mensch entscheidet", "Audit-Trail"],
        }

    def memory_plan(p) -> dict:
        return {
            "Working": "letzte 50 Turns im Conversation-Context (kurzfristig)",
            "Episodic": f"alle Sessions des Users {p.betroffene} (Postgres-Checkpoint, "
            "90-Tage-Auto-Pruning, RTBF binnen 30 Tagen)",
            "Semantic": "extrahierte Fakten ('User mag früh aufstehen', 'Termin xyz') "
            "in Vector-DB (Qdrant)",
            "Procedural": "gelernte Workflows ('immer Termin als ICS exportieren') in Tool-Konfig",
        }

    def rtbf_plan(p) -> list[str]:
        return [
            "DELETE /api/user/{id} → orchestriert 4 Lösch-Operationen:",
            "  1. Working: Session-Cache invalidieren",
            "  2. Episodic: Postgres-Checkpoint-Rows löschen",
            "  3. Semantic: Qdrant-Vectors mit user_id-Tag löschen",
            "  4. Procedural: Tool-Config-Entries entfernen",
            "Signiertes Lösch-Log mit SHA-256 + Timestamp + Audit-Anker",
            "DSGVO Art. 17 — Bestätigung an Nutzer:in binnen 30 Tagen",
        ]

    def hitl_eskalation(p) -> list[str]:
        eskalationen = []
        if p.rechtsrelevant:
            eskalationen.append("immer HITL bei rechtsrelevanten Themen")
        if p.aktion_typ == "destruktiv":
            eskalationen.append("HITL bei git-/db-/file-destruktiven Aktionen")
        if p.aktion_typ == "entscheidung":
            eskalationen.append("zwingender HITL bei Entscheidungen über Personen")
        eskalationen.append("Konfidenz < 0.85 → eskaliere zu Mensch")
        eskalationen.append("Konfidenz < 0.70 → STOP + Fehlerbericht")
        return eskalationen

    return hitl_eskalation, klassifiziere, memory_plan, rtbf_plan


@app.cell
def _(AutonomieProfil):
    """Drei Use-Cases."""
    profile = [
        AutonomieProfil(
            name="Persönlicher Voice-Assistent",
            aktion_typ="reversibel",
            rechtsrelevant=False,
            betroffene="person",
            cost_cap_moeglich=True,
            konfidenz_hoch=True,
            ai_act_anhang_iii=False,
        ),
        AutonomieProfil(
            name="Bürger-Service-Agent",
            aktion_typ="entscheidung",
            rechtsrelevant=True,  # Verwaltungs-Akte sind rechtlich relevant
            betroffene="behoerde",
            cost_cap_moeglich=True,
            konfidenz_hoch=False,
            ai_act_anhang_iii=False,  # Bürger-Service nicht zwingend Hochrisiko
        ),
        AutonomieProfil(
            name="Bewerber-Vorauswahl-Bot",
            aktion_typ="entscheidung",
            rechtsrelevant=True,
            betroffene="person",
            cost_cap_moeglich=True,
            konfidenz_hoch=True,
            ai_act_anhang_iii=True,  # Anhang III Nr. 1a: Recruiting/HR
        ),
    ]
    return (profile,)


@app.cell
def _(hitl_eskalation, klassifiziere, memory_plan, mo, profile, rtbf_plan):
    """Detail pro Use-Case."""
    blocks_detail = []
    for p in profile:
        k_det = klassifiziere(p)
        memory_det = memory_plan(p)
        rtbf_det = rtbf_plan(p)
        hitl_det = hitl_eskalation(p)

        kontrollen_str = "\n".join(f"  - {x}" for x in k_det["kontrollen"])
        memory_str = "\n".join(f"  - **{layer}**: {desc}" for layer, desc in memory_det.items())
        rtbf_str = "\n".join(f"  - {x}" for x in rtbf_det)
        hitl_str = "\n".join(f"  - {x}" for x in hitl_det)

        blocks_detail.append(
            f"### {p.name}\n\n"
            f"- **Stufe**: **{k_det['stufe']}** *(Grund: {k_det['begruendung']})*\n"
            f"- **Pflicht-Kontrollen**:\n{kontrollen_str}\n"
            f"- **4-Schicht-Memory**:\n{memory_str}\n"
            f"- **RTBF-Endpoint**:\n{rtbf_str}\n"
            f"- **HITL-Eskalation**:\n{hitl_str}\n"
        )
    mo.md("## Detail pro Use-Case\n\n" + "\n".join(blocks_detail))
    return


@app.cell
def _(klassifiziere, memory_plan, profile, rtbf_plan):
    """Smoke-Test: 5 Akzeptanz-Asserts."""
    p_voice = profile[0]
    p_buerger = profile[1]
    p_hr = profile[2]

    # 1. Voice-Assistent → L4 (reversibel + Cost-Cap + hohe Konfidenz)
    voice_k = klassifiziere(p_voice)
    assert voice_k["stufe"] == "L4"

    # 2. Bürger-Service → L2 (rechtsrelevant)
    buerger_k = klassifiziere(p_buerger)
    assert buerger_k["stufe"] == "L2"

    # 3. HR-Bewerber-Bot → STOP (AI-Act Anhang III + entscheidung)
    hr_k = klassifiziere(p_hr)
    assert hr_k["stufe"] == "STOP"
    assert "Mensch-im-Loop" in hr_k["kontrollen"][0]

    # 4. Memory-Plan hat 4 Schichten
    for prof in profile:
        memory_test = memory_plan(prof)
        assert set(memory_test.keys()) == {"Working", "Episodic", "Semantic", "Procedural"}

    # 5. RTBF-Plan in allen Use-Cases vorhanden
    for prof in profile:
        plan = rtbf_plan(prof)
        assert any("DSGVO Art. 17" in x for x in plan)

    print("✅ Übung 15.01 — alle 5 Asserts grün")
    return


if __name__ == "__main__":
    app.run()
