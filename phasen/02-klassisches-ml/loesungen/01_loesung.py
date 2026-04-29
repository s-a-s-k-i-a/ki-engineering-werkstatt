# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "pydantic>=2.9",
# ]
# ///

"""Lösungs-Skelett — Übung 02.01 — KMU-Modell-Selektor + Bias-Audit-Plan.

Smoke-test-tauglich. Reine Pydantic-Logik, kein sklearn-Training.
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
        # 🎯 Lösung Übung 02.01 — KMU-Modell-Selektor

        Drei reale DACH-KMU-Use-Cases, drei begründete Modell-Auswahlen,
        drei Bias-Audit-Pläne.
        """
    )
    return


@app.cell
def _():
    """Pydantic-Profil-Schema."""
    from pydantic import BaseModel, Field

    class KmuProfil(BaseModel):
        name: str
        n_samples: int = Field(ge=100)
        feature_typ: str
        latenz_ms: int = Field(ge=1)
        unbalanciert: bool
        ai_act_hochrisiko: bool
        agg_geschuetztes_merkmal: bool

    return (KmuProfil,)


@app.cell
def _():
    """Modell-Auswahl + Eval + Bias-Audit-Pflichten."""

    def empfehle_modell(p) -> dict:
        if p.n_samples > 500_000 and p.latenz_ms < 100:
            return {"modell": "LightGBM", "grund": "großes Tabular + low-latency"}
        if p.feature_typ == "viel_kategorisch":
            return {"modell": "CatBoost", "grund": "kategoriale Features ohne One-Hot"}
        if p.n_samples < 5_000:
            return {
                "modell": "Logistic Regression / kleiner Decision Tree",
                "grund": "zu wenig Daten für komplexe Modelle",
            }
        return {
            "modell": "XGBoost (mit LogReg-Baseline)",
            "grund": "Standard für KMU-Tabular-Datasets",
        }

    def empfehle_eval(p) -> dict:
        if p.feature_typ == "zeitreihe" or "sensor" in p.name.lower():
            return {
                "strategie": "Time-Split (alte Daten = Train, jüngere = Val/Test)",
                "grund": "Zeit-Leakage vermeiden",
            }
        if p.n_samples < 5_000:
            return {
                "strategie": "Stratified-5-Fold-CV",
                "grund": "zu wenig Daten für 80/10/10-Single-Split",
            }
        return {"strategie": "Stratified-Split 70/15/15 + 5-Fold-CV auf Train", "grund": "Standard"}

    def bias_audit_pflichten(p) -> list[str]:
        pflichten = ["MLflow-3-Logging der Trainings-Hyperparameter (Art. 11)"]
        if p.unbalanciert:
            pflichten.append("class_weight='balanced' oder scale_pos_weight setzen")
        if p.agg_geschuetztes_merkmal:
            pflichten.append("Demographic Parity (DP < 5 %) auf AGG-Merkmale")
            pflichten.append("Equalized Odds (EOpp < 10 %) auf AGG-Merkmale")
            pflichten.append("Proxy-Bias-Test (PLZ, Vorname, Geburtsjahr)")
        if p.ai_act_hochrisiko:
            pflichten.append("AI-Act Art. 9-15 (alle Hochrisiko-Pflichten)")
            pflichten.append("CE-Kennzeichnung + EU-Datenbank-Eintrag (Anhang VIII)")
            pflichten.append("DSFA nach DSGVO Art. 35")
        pflichten.append("SHAP-Erklärbarkeit (lokal pro Entscheidung, Art. 13 + DSGVO Art. 22)")
        return pflichten

    return bias_audit_pflichten, empfehle_eval, empfehle_modell


@app.cell
def _(KmuProfil):
    """Drei Use-Cases."""
    profile = [
        KmuProfil(
            name="Maschinenbau-Predictive-Maintenance",
            n_samples=850_000,
            feature_typ="tabular_numerisch",
            latenz_ms=50,
            unbalanciert=True,
            ai_act_hochrisiko=False,
            agg_geschuetztes_merkmal=False,
        ),
        KmuProfil(
            name="Steuerberatung-Mandanten-Churn",
            n_samples=12_000,
            feature_typ="tabular_gemischt",
            latenz_ms=300,
            unbalanciert=True,
            ai_act_hochrisiko=False,
            agg_geschuetztes_merkmal=True,
        ),
        KmuProfil(
            name="Bildungs-Drop-out-Vorhersage",
            n_samples=4_500,
            feature_typ="tabular_gemischt",
            latenz_ms=500,
            unbalanciert=True,
            ai_act_hochrisiko=True,  # Anhang III Nr. 3 (Bildung)
            agg_geschuetztes_merkmal=True,
        ),
    ]
    return (profile,)


@app.cell
def _(bias_audit_pflichten, empfehle_eval, empfehle_modell, mo, profile):
    """Übersichts-Tabelle."""
    rows_uebersicht = []
    for p_uebers in profile:
        m_uebers = empfehle_modell(p_uebers)
        e_uebers = empfehle_eval(p_uebers)
        bias_uebers = bias_audit_pflichten(p_uebers)
        rows_uebersicht.append(
            f"| **{p_uebers.name}** | {p_uebers.n_samples:,} | {m_uebers['modell']} | "
            f"{e_uebers['strategie'][:30]}... | {len(bias_uebers)} Pflichten |"
        )

    mo.md(
        "## Use-Case-Empfehlungen\n\n"
        "| Profil | n | Modell | Eval | Compliance |\n"
        "|---|---|---|---|---|\n" + "\n".join(rows_uebersicht)
    )
    return


@app.cell
def _(bias_audit_pflichten, empfehle_eval, empfehle_modell, mo, profile):
    """Detail pro Use-Case."""
    blocks_detail = []
    for p_det in profile:
        m_det = empfehle_modell(p_det)
        e_det = empfehle_eval(p_det)
        bias_det = bias_audit_pflichten(p_det)
        bias_det_str = "\n".join(f"  - {b}" for b in bias_det)
        blocks_detail.append(
            f"### {p_det.name}\n\n"
            f"- **Modell**: {m_det['modell']} *({m_det['grund']})*\n"
            f"- **Eval**: {e_det['strategie']} *({e_det['grund']})*\n"
            f"- **Compliance**:\n{bias_det_str}\n"
        )
    mo.md("## Detail pro Use-Case\n\n" + "\n".join(blocks_detail))
    return


@app.cell
def _(bias_audit_pflichten, empfehle_modell, profile):
    """Smoke-Test: 4 Akzeptanz-Asserts."""
    p_maschinen = profile[0]
    p_churn = profile[1]
    p_dropout = profile[2]

    # 1. Maschinenbau → LightGBM (groß + low-latency)
    assert empfehle_modell(p_maschinen)["modell"].startswith("LightGBM")

    # 2. Mandanten-Churn → Bias-Audit-Pflicht (AGG-Merkmal)
    bias_churn = bias_audit_pflichten(p_churn)
    assert any("Demographic" in b for b in bias_churn)
    assert any("Equalized" in b for b in bias_churn)

    # 3. Bildungs-Drop-out → AI-Act-Hochrisiko-Markierung
    bias_drop = bias_audit_pflichten(p_dropout)
    assert any("AI-Act" in b and "Hochrisiko" in b for b in bias_drop)
    assert any("DSFA" in b for b in bias_drop)

    # 4. SHAP-Pflicht in jedem Use-Case
    for prof in profile:
        assert any("SHAP" in b for b in bias_audit_pflichten(prof))

    print("✅ Übung 02.01 — alle 4 Asserts grün")
    return


if __name__ == "__main__":
    app.run()
