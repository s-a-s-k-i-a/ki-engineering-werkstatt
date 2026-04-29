# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "pydantic>=2.9",
# ]
# ///

"""Klassisches-ML-Selektor — Phase 02 Hands-on.

Profiliert tabular Use-Cases nach Daten-Größe / -Typ / Latenz / Compliance-Klasse
und empfiehlt:

- Modell-Familie (LogReg / Random Forest / XGBoost / LightGBM / CatBoost)
- Eval-Strategie (Stratified-K-Fold-CV vs. einzelner Split, Train-Size)
- Compliance-Pflichten (AI-Act-Risikoklasse, SHAP, Bias-Audit)

Smoke-test-tauglich. Keine sklearn-Installation nötig — die Lektionen zeigen
den vollständigen sklearn-Code mit XGBoost/SHAP zum Drop-In.
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
        # 🌳 Klassisches-ML-Selektor · Phase 02

        Empfiehlt **Modell + Eval-Strategie + Compliance-Pflichten** für tabular
        Use-Cases im DACH-Mittelstand.

        Die Lektionen zeigen den vollständigen sklearn-/XGBoost-/SHAP-Code als
        Drop-In — dieser Selektor klassifiziert *welches* Werkzeug für *welchen*
        Use-Case.

        Stand: 29.04.2026 · **Achtung**: Kreditscoring = AI-Act Anhang III Nr. 5b
        Hochrisiko (alle Pflichten).
        """
    )
    return


@app.cell
def _():
    """Pydantic-Schemas für Use-Case-Profil + Empfehlung."""
    from pydantic import BaseModel, Field

    class UseCaseProfil(BaseModel):
        name: str
        n_samples: int = Field(ge=100, le=100_000_000)
        feature_typ: str  # "tabular_numerisch", "tabular_gemischt", "viel_kategorisch"
        latenz_ms: int = Field(ge=1, le=10_000, default=200)
        unbalanciert: bool = False
        ai_act_hochrisiko: bool = False
        agg_geschuetztes_merkmal: bool = False

    return (UseCaseProfil,)


@app.cell
def _(UseCaseProfil):
    """Empfehlungs-Logik."""

    def empfehle(p: UseCaseProfil) -> dict:
        # Modell-Familie
        if p.n_samples < 1_000:
            modell = "Logistic Regression (oder kleiner Decision Tree)"
            grund = "zu wenig Daten für komplexere Modelle"
        elif p.feature_typ == "viel_kategorisch":
            modell = "CatBoost"
            grund = "kategoriale Features ohne One-Hot"
        elif p.n_samples > 1_000_000 and p.latenz_ms < 50:
            modell = "LightGBM"
            grund = "Speed + Memory bei großem Tabular"
        elif p.n_samples > 100_000:
            modell = "XGBoost (oder LightGBM)"
            grund = "Standard-Boosting für mittel-große Tabular-Daten"
        else:
            modell = "XGBoost (Logistic Regression als Pflicht-Baseline)"
            grund = "etablierter Standard für KMU-Datasets"

        # Eval
        if p.n_samples < 5_000:
            eval_strategie = "Stratified-5-Fold-CV (Daten zu knapp für 80/10/10)"
        else:
            eval_strategie = "Stratified-Split 70/15/15 + 5-Fold-CV auf Train"

        # Sampling-Strategie
        sampling = "class_weight='balanced'" if p.unbalanciert else "kein Resampling"

        # Compliance
        compliance = []
        if p.ai_act_hochrisiko:
            compliance.append("AI-Act Art. 9-15 (alle Hochrisiko-Pflichten)")
            compliance.append("CE-Kennzeichnung + EU-Datenbank-Eintrag (Anhang VIII)")
            compliance.append("DSFA nach DSGVO Art. 35")
            compliance.append("Konformitätsbewertung vor Inverkehrbringen")
        if p.agg_geschuetztes_merkmal:
            compliance.append("Bias-Audit auf AGG-Merkmale (DP < 5 %, EOpp < 10 %)")
            compliance.append("Proxy-Bias prüfen (PLZ, Vorname, Geburtsjahr)")
        compliance.append("SHAP-Erklärbarkeit (lokal + global, DSGVO Art. 22)")

        return {
            "modell": modell,
            "modell_grund": grund,
            "eval_strategie": eval_strategie,
            "sampling": sampling,
            "compliance_pflichten": compliance,
        }

    return (empfehle,)


@app.cell
def _(UseCaseProfil, empfehle, mo):
    """Beispiel-Profile."""
    profile = [
        UseCaseProfil(
            name="KMU-Kreditscoring (Hannover)",
            n_samples=8_000,
            feature_typ="tabular_gemischt",
            latenz_ms=200,
            unbalanciert=True,
            ai_act_hochrisiko=True,
            agg_geschuetztes_merkmal=True,
        ),
        UseCaseProfil(
            name="Customer-Churn Telekommunikation",
            n_samples=2_000_000,
            feature_typ="tabular_gemischt",
            latenz_ms=30,
            unbalanciert=True,
            ai_act_hochrisiko=False,
            agg_geschuetztes_merkmal=False,
        ),
        UseCaseProfil(
            name="Predictive Maintenance Maschinenbau",
            n_samples=120_000,
            feature_typ="tabular_numerisch",
            latenz_ms=500,
            unbalanciert=True,
            ai_act_hochrisiko=False,
            agg_geschuetztes_merkmal=False,
        ),
        UseCaseProfil(
            name="Pflanzen-Kategorisierung Gartenbau",
            n_samples=600,
            feature_typ="viel_kategorisch",
            latenz_ms=1000,
            unbalanciert=False,
            ai_act_hochrisiko=False,
            agg_geschuetztes_merkmal=False,
        ),
        UseCaseProfil(
            name="Bewerber-Scoring HR (illegal!)",
            n_samples=15_000,
            feature_typ="tabular_gemischt",
            latenz_ms=200,
            unbalanciert=True,
            ai_act_hochrisiko=True,
            agg_geschuetztes_merkmal=True,
        ),
    ]

    rows_p = []
    for prof_row in profile:
        e_row = empfehle(prof_row)
        rows_p.append(
            f"| **{prof_row.name}** | {prof_row.n_samples:,} | {e_row['modell']} | "
            f"{e_row['eval_strategie'][:30]}... | {len(e_row['compliance_pflichten'])} Pflichten |"
        )

    mo.md(
        "## 1. Use-Case-Empfehlungen\n\n"
        "| Profil | n | Modell | Eval | Compliance |\n"
        "|---|---|---|---|---|\n" + "\n".join(rows_p)
    )
    return (profile,)


@app.cell
def _(empfehle, mo, profile):
    """Compliance-Detail pro Profil."""
    blocks = []
    for prof_det in profile:
        e_det = empfehle(prof_det)
        compl = "\n".join(f"  - {c}" for c in e_det["compliance_pflichten"])
        blocks.append(
            f"### {prof_det.name}\n\n"
            f"- **Modell**: {e_det['modell']} ({e_det['modell_grund']})\n"
            f"- **Eval**: {e_det['eval_strategie']}\n"
            f"- **Sampling**: {e_det['sampling']}\n"
            f"- **Compliance-Pflichten**:\n{compl}\n"
        )
    mo.md("## 2. Compliance-Detail\n\n" + "\n".join(blocks))
    return


@app.cell
def _(UseCaseProfil, empfehle):
    """Smoke-Test."""
    test = UseCaseProfil(
        name="Test",
        n_samples=10_000,
        feature_typ="tabular_gemischt",
        latenz_ms=100,
        unbalanciert=True,
        ai_act_hochrisiko=True,
        agg_geschuetztes_merkmal=True,
    )
    e_smoke = empfehle(test)
    assert "XGBoost" in e_smoke["modell"]
    assert any("AI-Act" in c for c in e_smoke["compliance_pflichten"])
    assert any("SHAP" in c for c in e_smoke["compliance_pflichten"])
    print("✅ Phase 02 Smoke-Test grün")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Faustregeln 2026

        | Wenn... | Dann... |
        |---|---|
        | n < 1.000 | Logistic Regression / einfacher Baum |
        | n 1.000–100.000 | XGBoost (mit LogReg-Baseline) |
        | n > 1M, low-latency | LightGBM |
        | viele kategoriale Features | CatBoost |
        | unbalanciert | `class_weight="balanced"` oder `scale_pos_weight` |
        | AI-Act Hochrisiko | SHAP + Bias-Audit + DSFA + CE-Kennzeichnung |
        | AGG-Merkmal involviert | Bias-Audit (DP/EOpp), Proxy-Test |

        ## Wichtige Hinweise

        - Diese Hands-on ist ein **Selektor**, kein vollständiges Training. Die
          Lektionen zeigen den vollen sklearn-/XGBoost-/SHAP-Code.
        - **Bewerber-Scoring** ist nach AI-Act-Anhang-III-1a Hochrisiko und
          stellt nach DSGVO Art. 22 eine automatisierte Entscheidung dar — in
          Praxis darf ohne menschliches Eingreifen nicht entschieden werden
          (siehe Phase 15 + 20).
        - **Kreditscoring** ist nach AI-Act-Anhang-III-5b Hochrisiko mit allen
          Pflichten (Art. 9-15 + CE + EU-Datenbank).
        - **SHAP-Erklärbarkeit** ist 2026 Industrie-Standard, aber **nicht
          alleiniger Beweis** für DSGVO-Art-22-Konformität.
        """
    )
    return


if __name__ == "__main__":
    app.run()
