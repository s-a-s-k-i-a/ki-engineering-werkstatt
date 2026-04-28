# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "pyyaml>=6.0",
#   "rich>=13.9",
# ]
# ///

"""AI-Act-Klassifizierungs-Demo — drei realistische Beispiele.

Smoke-Test-tauglich: nutzt `werkzeuge.ai_act_classifier.klassifiziere`
direkt, kein CLI-Subprozess nötig.
"""

import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
        # AI-Act-Klassifizierung — drei Beispiele

        Wir klassifizieren drei reale KI-System-Beispiele:

        1. **Charity-Adoptions-Bot** (Chatbot mit FAQ + Termin-Buchung)
        2. **HR-Screening Kreditbank** (Lebenslauf-Scoring + Kreditscoring)
        3. **Behördliches Social-Scoring** (sollte gar nicht erst gebaut werden)

        Jedes System wird als YAML-Modell-Karte beschrieben und durchläuft
        die `klassifiziere`-Funktion aus `werkzeuge/ai_act_classifier.py`.
        """
    )
    return


@app.cell
def _(mo):
    """Beispiel 1: Charity-Adoptions-Bot."""
    from werkzeuge.ai_act_classifier import klassifiziere

    karte_adoption = {
        "name": "Charity-Adoptions-Bot",
        "version": "0.1.0",
        "use_case_kategorien": [],  # kein Anh. III Use-Case
        "transparenz_trigger": ["chatbot"],  # Art. 50 Abs. 1
        "risiko_indikatoren": {},  # keine Verbote
        "ist_gpai": False,
    }
    befund = klassifiziere(karte_adoption)
    mo.md(
        f"## 1) Charity-Adoptions-Bot\n\n"
        f"**Risiko**: `{befund.risiko.value}` — {len(befund.pflichten)} Pflichten\n\n"
        f"**Begründung**: {befund.begruendung}\n\n"
        f"**Top-Pflichten**:\n" + "\n".join(f"- {p}" for p in befund.pflichten[:3])
    )
    return befund, karte_adoption, klassifiziere


@app.cell
def _(klassifiziere, mo):
    """Beispiel 2: HR-Screening Kreditbank."""
    karte_hr = {
        "name": "Bank-HR-Screener",
        "version": "1.0.0",
        "use_case_kategorien": [
            "beschaeftigung-hr",  # Anh. III Nr. 4
            "wesentliche-private-dienste",  # Anh. III Nr. 5b (Kreditscoring)
        ],
        "transparenz_trigger": [],
        "risiko_indikatoren": {},
        "ist_gpai": False,
    }
    befund_hr = klassifiziere(karte_hr)
    mo.md(
        f"## 2) HR-Screening Kreditbank\n\n"
        f"**Risiko**: `{befund_hr.risiko.value}` — **Hochrisiko**\n\n"
        f"**Pflichten** (Auszug):\n" + "\n".join(f"- {p}" for p in befund_hr.pflichten[:6])
    )
    return (befund_hr,)


@app.cell
def _(klassifiziere, mo):
    """Beispiel 3: Behördliches Social Scoring (verboten)."""
    karte_ss = {
        "name": "City-Bonus-Score",
        "use_case_kategorien": [],
        "transparenz_trigger": [],
        "risiko_indikatoren": {"social-scoring": True},
        "ist_gpai": False,
    }
    befund_ss = klassifiziere(karte_ss)
    mo.md(
        f"## 3) Behördliches Social Scoring\n\n"
        f"**Risiko**: `{befund_ss.risiko.value}` — **darf NICHT gebaut/betrieben werden**\n\n"
        f"**Begründung**: {befund_ss.begruendung}\n\n"
        f"Bußgelder bis 35 Mio. € / 7 % Jahresumsatz."
    )
    return (befund_ss,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### CLI-Variante

        Dieselben Klassifizierungen über die Kommandozeile:

        ```bash
        ki-act-classifier --modell-karte vorlagen/model-card-adoption-bot.yaml
        ki-act-classifier --modell-karte vorlagen/model-card-hr.yaml --als-json
        ```

        ### Was du in der Vollversion machst

        - Schreibe eine `model-card.yaml` für dein eigenes Projekt
        - Klassifiziere und speichere das Ergebnis als Audit-Artefakt
        - Bei Hochrisiko: gehe Lektion 20.03 (DSFA) durch
        - Verlinke das Klassifizierungs-Ergebnis in deinem CHANGELOG

        ### Quellen

        - [AI Act Volltext (DE)](https://eur-lex.europa.eu/legal-content/DE/ALL/?uri=CELEX:32024R1689)
        - [TÜV Consulting Digital Omnibus 2026](https://consulting.tuv.com/aktuelles/ki-im-fokus/eu-ai-act-2026-zwischenstand)
        - [BfDI AI-Act-Hub](https://www.bfdi.bund.de/SharedDocs/Kurzmeldungen/DE/2024/AI-Act.html)
        """
    )
    return


if __name__ == "__main__":
    app.run()
