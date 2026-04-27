# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "pyyaml>=6.0",
# ]
# ///

"""Lösung Übung 20.01 — Beispielhafte Klassifizierung 'WP-Plugin-Helfer-RAG'."""

import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    """Klassifizierung des WP-Plugin-Helfer-RAG (Capstone 19.A)."""
    from werkzeuge.ai_act_classifier import klassifiziere

    karte = {
        "name": "WP-Plugin-Helfer-RAG",
        "version": "0.1.0",
        "use_case_kategorien": [],  # kein Anh. III
        "transparenz_trigger": ["chatbot"],  # Art. 50 Abs. 1
        "risiko_indikatoren": {},
        "ist_gpai": False,
    }
    befund = klassifiziere(karte)
    mo.md(
        f"## WP-Plugin-Helfer-RAG\n\n"
        f"**Risiko**: `{befund.risiko.value}` (begrenzt)\n\n"
        f"**Pflichten**:\n" + "\n".join(f"- {p}" for p in befund.pflichten) + "\n\n"
        "**Compliance-Plan (200 Wörter)**:\n\n"
        "Das System ist ein Chatbot, der WordPress-Plugin-Dokumentation per RAG zugänglich macht. "
        "Risiko-Klasse begrenzt → Art. 50 Transparenz: bei jedem Chat-Start ein KI-Hinweis "
        "('Du sprichst mit einer KI'). AI-Literacy nach Art. 4: Onboarding-Modul gem. `ai-literacy-onboarding.md`. "
        "DSGVO: AVV mit Aleph Alpha (Generator) und self-hosted Qdrant. Kein Personenbezug in "
        "WP-Doku, daher keine DSFA-Pflicht. Audit-Logging nach Art. 12 mit Schema aus "
        "`code/05_audit_logging.py`. Bias-Test in Phase 18 — Plugin-Doku ist domain-spezifisch, "
        "Bias-Risiko gering."
    )
    return befund, karte


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Adaptiere für dein eigenes System

        - Kopiere `vorlagen/model-card-tierheim-bot.yaml` und passe es an
        - Lasse `ki-act-classifier` laufen
        - Schreibe deinen 200-Wort-Compliance-Plan
        - Erstelle Issues für jede Pflicht aus dem Klassifizierungs-Output

        Wenn du fertig bist: PR mit `compliance.md` in deinem Capstone-Ordner.
        """
    )
    return


if __name__ == "__main__":
    app.run()
