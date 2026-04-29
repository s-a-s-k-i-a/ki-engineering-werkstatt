# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "pydantic>=2.9",
# ]
# ///

"""Lösungs-Skelett — Übung 03.01 — DL-Architektur + Tracking-Selektor.

Smoke-test-tauglich. Reine Pydantic-Logik, kein PyTorch-Import.
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
        # 🎯 Lösung Übung 03.01 — DL-Architektur + Tracking

        Drei DACH-DL-Vorhaben → Architektur + Optimizer + Tracking + VRAM-Budget.
        """
    )
    return


@app.cell
def _():
    """Pydantic-Profil-Schema."""
    from pydantic import BaseModel, Field

    class DlProfil(BaseModel):
        name: str
        daten_typ: str
        n_samples: int = Field(ge=100)
        gpu_vram_gb: int = Field(ge=8)
        hosting: str
        sensible_daten: bool
        ai_act_hochrisiko: bool

    return (DlProfil,)


@app.cell
def _():
    """Empfehlungs-Logik."""

    def empfehle_architektur(p) -> dict:
        if p.daten_typ == "bild_klein":
            arch = "ResNet50 mit Pre-trained Backbone" if p.n_samples < 50_000 else "ConvNeXt-Tiny"
        elif p.daten_typ == "bild_gross":
            arch = "ConvNeXt-Small" if p.n_samples < 100_000 else "ViT-Base"
        elif p.daten_typ == "sequenz":
            arch = "Decoder-only Transformer (Phase 07)"
        elif p.daten_typ == "text":
            arch = "Pre-trained LLM-Finetuning (Phase 12 LoRA)"
        else:
            arch = "?"
        return {"architektur": arch}

    def optimizer_setup(p) -> dict:
        accum = (
            "Gradient-Accumulation (effective batch ~ 256)"
            if p.gpu_vram_gb < 40
            else "Standard Batch"
        )
        return {
            "optimizer": "AdamW (lr=1e-3, weight_decay=0.01)",
            "scheduler": "Cosine-Schedule mit 500-1000 Warmup-Steps",
            "precision": "bf16 (auf H100/H200/B200)",
            "batching": accum,
        }

    def tracking_wahl(p) -> dict:
        if p.hosting == "dach_on_prem":
            return {
                "tool": "MLflow 3.11 (Docker self-hosted)",
                "grund": "On-Prem, DSGVO-vollständig",
            }
        if p.hosting == "hybrid_eu":
            return {
                "tool": "Comet (EU-Region) oder MLflow auf STACKIT/IONOS",
                "grund": "EU-Cloud-Provider mit AVV",
            }
        return {
            "tool": "W&B mit AVV + SCC + TIA + DPIA falls sensibel",
            "grund": "Drittland-Transfer-Verfahren Pflicht",
        }

    def vram_budget_check(p) -> dict:
        # Grobe Schätzung
        if "ResNet50" in empfehle_architektur(p)["architektur"]:
            modell_gb, aktivierungen_gb = 1.0, 4.0
        elif "ConvNeXt" in empfehle_architektur(p)["architektur"]:
            modell_gb, aktivierungen_gb = 2.0, 6.0
        elif "ViT" in empfehle_architektur(p)["architektur"]:
            modell_gb, aktivierungen_gb = 4.0, 8.0
        elif "Transformer" in empfehle_architektur(p)["architektur"]:
            modell_gb, aktivierungen_gb = 8.0, 16.0
        else:
            modell_gb, aktivierungen_gb = 1.0, 2.0
        budget = (modell_gb + aktivierungen_gb) * 1.2
        passt = budget <= p.gpu_vram_gb
        return {"benoetigt_gb": budget, "passt": passt}

    def ai_act_pflichten(p) -> list[str]:
        pflichten = ["Random-Seed setzen + Hyperparameter committen (Art. 11)"]
        if p.sensible_daten:
            pflichten.append("Pseudonymisierung der Trainings-Daten (Art. 25)")
            pflichten.append("DSFA nach DSGVO Art. 35")
        if p.ai_act_hochrisiko:
            pflichten.append("AI-Act Art. 9-15 Hochrisiko-Pflichten + CE-Kennzeichnung")
            pflichten.append("EU-Datenbank-Eintrag (Anhang VIII)")
        return pflichten

    return (
        ai_act_pflichten,
        empfehle_architektur,
        optimizer_setup,
        tracking_wahl,
        vram_budget_check,
    )


@app.cell
def _(DlProfil):
    """Drei Use-Cases."""
    profile = [
        DlProfil(
            name="Industrie-Defekt-Klassifikator",
            daten_typ="bild_klein",
            n_samples=8_000,
            gpu_vram_gb=24,
            hosting="dach_on_prem",
            sensible_daten=False,
            ai_act_hochrisiko=False,
        ),
        DlProfil(
            name="Hochschul-Chatbot",
            daten_typ="text",
            n_samples=50_000,
            gpu_vram_gb=24,
            hosting="hybrid_eu",
            sensible_daten=True,
            ai_act_hochrisiko=False,
        ),
        DlProfil(
            name="Krankenhaus-Bildgebung-Diagnose",
            daten_typ="bild_gross",
            n_samples=320_000,
            gpu_vram_gb=80,
            hosting="dach_on_prem",
            sensible_daten=True,
            ai_act_hochrisiko=True,
        ),
    ]
    return (profile,)


@app.cell
def _(
    ai_act_pflichten,
    empfehle_architektur,
    mo,
    optimizer_setup,
    profile,
    tracking_wahl,
    vram_budget_check,
):
    """Detail pro Use-Case."""
    blocks = []
    for p in profile:
        a = empfehle_architektur(p)
        o = optimizer_setup(p)
        t = tracking_wahl(p)
        v = vram_budget_check(p)
        pflichten = ai_act_pflichten(p)
        pflichten_str = "\n".join(f"  - {x}" for x in pflichten)
        passt_emoji = "✅" if v["passt"] else "⚠️"
        blocks.append(
            f"### {p.name}\n\n"
            f"- **Architektur**: {a['architektur']}\n"
            f"- **Optimizer**: {o['optimizer']} · {o['scheduler']} · {o['precision']}\n"
            f"- **Batching**: {o['batching']}\n"
            f"- **Tracking**: {t['tool']} *({t['grund']})*\n"
            f"- **VRAM-Budget**: {v['benoetigt_gb']:.1f} GB benötigt vs. {p.gpu_vram_gb} GB GPU {passt_emoji}\n"
            f"- **Compliance**:\n{pflichten_str}\n"
        )
    mo.md("## Detail pro Use-Case\n\n" + "\n".join(blocks))
    return


@app.cell
def _(ai_act_pflichten, empfehle_architektur, profile, tracking_wahl):
    """Smoke-Test: 5 Akzeptanz-Asserts."""
    p_defekt = profile[0]
    p_chatbot = profile[1]
    p_ct = profile[2]

    # 1. Defekt-Klassifikator → ResNet50 (klein + < 50k)
    assert "ResNet50" in empfehle_architektur(p_defekt)["architektur"]

    # 2. Chatbot mit sensiblen Daten + EU-Cloud → kein W&B-US
    chat_track = tracking_wahl(p_chatbot)["tool"]
    assert "Comet" in chat_track or "STACKIT" in chat_track or "MLflow" in chat_track

    # 3. CT-Scans → AI-Act-Hochrisiko-Markierung
    ct_pflichten = ai_act_pflichten(p_ct)
    assert any("Hochrisiko" in p for p in ct_pflichten)
    assert any("CE-Kennzeichnung" in p for p in ct_pflichten)

    # 4. CT-Scans → DSFA-Pflicht (sensible Daten)
    assert any("DSFA" in p for p in ct_pflichten)

    # 5. On-Prem-Vorhaben → MLflow lokal
    assert tracking_wahl(p_defekt)["tool"].startswith("MLflow")

    print("✅ Übung 03.01 — alle 5 Asserts grün")
    return


if __name__ == "__main__":
    app.run()
