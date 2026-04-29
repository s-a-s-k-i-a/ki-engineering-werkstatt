# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "pydantic>=2.9",
# ]
# ///

"""Deep-Learning-Kalkulator — Phase 03 Hands-on.

Profiliert ein DL-Vorhaben nach:

- Daten-Typ (tabular / Bild / Sequenz / Audio)
- Daten-Größe + Hardware-Budget
- Hosting-Szenario (DACH-On-Prem / Hybrid / Cloud)

und empfiehlt:

- Modell-Architektur (MLP, ResNet, ViT, Transformer)
- Optimizer + Scheduler
- Hardware (GPU-Klasse, VRAM)
- Tracking-Tool (MLflow lokal vs. Comet EU vs. W&B mit Vorbehalt)

Smoke-test-tauglich. Keine PyTorch-Installation nötig — die Lektionen zeigen
den vollständigen PyTorch-/Lightning-/MLflow-Code zum Drop-In.
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
        # 🧠 Deep-Learning-Kalkulator · Phase 03

        Empfiehlt **Architektur + Hardware + Tracking** für ein DL-Vorhaben.

        Stand: 29.04.2026 (PyTorch 2.7, MLflow 3.11, Lightning 2.6.1).
        """
    )
    return


@app.cell
def _():
    """Pydantic-Schemas."""
    from pydantic import BaseModel, Field

    class DLProfil(BaseModel):
        name: str
        daten_typ: str  # "tabular", "bild_klein", "bild_gross", "sequenz", "audio"
        n_samples: int = Field(ge=100, le=1_000_000_000)
        gpu_vram_gb: int = Field(ge=8, le=192, default=24)
        hosting: str = Field(default="dach_on_prem")
        # "dach_on_prem", "hybrid_eu", "cloud_us"
        latenz_ms: int = Field(ge=1, le=10_000, default=200)
        sensible_daten: bool = False

    return (DLProfil,)


@app.cell
def _(DLProfil):
    """Empfehlungs-Logik."""

    def empfehle(p: DLProfil) -> dict:
        # Architektur
        if p.daten_typ == "tabular":
            arch = "Boosting (Phase 02) — DL meist nicht nötig"
            grund = "tree-based schlägt DL bei Tabular < 1M (Grinsztajn 2022)"
        elif p.daten_typ == "bild_klein":
            arch = "ResNet50 mit Pre-trained Backbone" if p.n_samples < 50_000 else "ConvNeXt-Tiny"
            grund = "Pre-trained Backbones bei kleinen Datasets robust"
        elif p.daten_typ == "bild_gross":
            arch = "ViT-Base (Vision Transformer)" if p.n_samples > 100_000 else "ConvNeXt-Small"
            grund = "ViT braucht viele Daten, sonst ConvNeXt sicherer"
        elif p.daten_typ == "sequenz":
            arch = "Transformer (Phase 07) oder Mamba/Jamba (Phase 09)"
            grund = "klassische LSTMs sind 2026 niche"
        elif p.daten_typ == "audio":
            arch = "Whisper / Voxtral (Phase 06) als Pre-trained, dann Finetuning"
            grund = "Audio-Foundation-Models > from-scratch"
        else:
            arch = "?"
            grund = "Daten-Typ nicht erkannt"

        # Optimizer
        opt = "AdamW (lr=1e-3, weight_decay=0.01)"
        scheduler = "Cosine-Schedule mit 500-1000 Warmup-Steps"

        # Hardware
        if p.gpu_vram_gb >= 80:
            hw = "H100 / H200 / B200 — bf16, gradient_accumulation optional"
        elif p.gpu_vram_gb >= 24:
            hw = "RTX 4090 / A6000 — bf16, gradient_accumulation für große Batches"
        else:
            hw = "RTX 4070 / 3090 — fp16, kleine Batches, kein LLM-Pretraining"

        # Tracking
        if p.hosting == "dach_on_prem":
            tracking = "MLflow 3.11 (Docker self-hosted)"
            tracking_grund = "On-Prem, DSGVO-vollständig"
        elif p.hosting == "hybrid_eu":
            tracking = "Comet (EU-Region) oder MLflow auf STACKIT/IONOS"
            tracking_grund = "EU-Cloud-Provider mit AVV"
        else:
            tracking = "W&B (mit AVV + SCC + TIA + DPIA falls sensible Daten)"
            tracking_grund = "DSGVO-Drittland-Transfer-Verfahren Pflicht"

        # Compliance
        compliance = []
        compliance.append("Random-Seed setzen (AI-Act Art. 11)")
        compliance.append("Hyperparameter-Logging mit Tracking-Tool")
        if p.sensible_daten:
            compliance.append("DSFA nach DSGVO Art. 35")
            compliance.append("Pseudonymisierung der Trainings-Daten (DSGVO Art. 25)")
            if p.hosting == "cloud_us":
                compliance.append("⚠️ Sensible Daten + US-Cloud = SCC + TIA")

        return {
            "architektur": arch,
            "architektur_grund": grund,
            "optimizer": opt,
            "scheduler": scheduler,
            "hardware": hw,
            "tracking": tracking,
            "tracking_grund": tracking_grund,
            "compliance_pflichten": compliance,
        }

    return (empfehle,)


@app.cell
def _(DLProfil, empfehle, mo):
    """Beispiel-Profile."""
    profile = [
        DLProfil(
            name="Tierheim-Bilder-Klassifikator",
            daten_typ="bild_klein",
            n_samples=8_000,
            gpu_vram_gb=24,
            hosting="dach_on_prem",
            latenz_ms=300,
            sensible_daten=False,
        ),
        DLProfil(
            name="Customer-Churn (Telekom)",
            daten_typ="tabular",
            n_samples=2_000_000,
            gpu_vram_gb=24,
            hosting="hybrid_eu",
            latenz_ms=30,
            sensible_daten=True,
        ),
        DLProfil(
            name="Whisper-Finetuning Hannover-Dialekt",
            daten_typ="audio",
            n_samples=20_000,
            gpu_vram_gb=80,
            hosting="dach_on_prem",
            latenz_ms=1000,
            sensible_daten=False,
        ),
        DLProfil(
            name="Medizin-Bild-Diagnose",
            daten_typ="bild_gross",
            n_samples=500_000,
            gpu_vram_gb=80,
            hosting="dach_on_prem",
            latenz_ms=2000,
            sensible_daten=True,
        ),
        DLProfil(
            name="Bewerber-Vorauswahl-Modell (illegal!)",
            daten_typ="tabular",
            n_samples=12_000,
            gpu_vram_gb=24,
            hosting="cloud_us",
            latenz_ms=200,
            sensible_daten=True,
        ),
    ]

    rows_p = []
    for prof in profile:
        e_prof = empfehle(prof)
        rows_p.append(
            f"| **{prof.name}** | {prof.daten_typ} | {e_prof['architektur'][:30]}... | "
            f"{e_prof['hardware'][:25]}... | {e_prof['tracking'][:20]}... |"
        )

    mo.md(
        "## 1. Use-Case-Empfehlungen\n\n"
        "| Profil | Daten-Typ | Architektur | Hardware | Tracking |\n"
        "|---|---|---|---|---|\n" + "\n".join(rows_p)
    )
    return (profile,)


@app.cell
def _(empfehle, mo, profile):
    """Detaillierte Pflichten pro Profil."""
    blocks = []
    for prof_det in profile:
        e_det = empfehle(prof_det)
        compl = "\n".join(f"  - {c}" for c in e_det["compliance_pflichten"])
        blocks.append(
            f"### {prof_det.name}\n\n"
            f"- **Architektur**: {e_det['architektur']} *(Grund: {e_det['architektur_grund']})*\n"
            f"- **Optimizer**: {e_det['optimizer']}\n"
            f"- **Scheduler**: {e_det['scheduler']}\n"
            f"- **Hardware**: {e_det['hardware']}\n"
            f"- **Tracking**: {e_det['tracking']} *({e_det['tracking_grund']})*\n"
            f"- **Compliance-Pflichten**:\n{compl}\n"
        )
    mo.md("## 2. Detail pro Profil\n\n" + "\n".join(blocks))
    return


@app.cell
def _(DLProfil, empfehle):
    """Smoke-Test."""
    test = DLProfil(
        name="Test",
        daten_typ="bild_klein",
        n_samples=10_000,
        gpu_vram_gb=24,
        hosting="dach_on_prem",
        latenz_ms=200,
        sensible_daten=True,
    )
    e_smoke = empfehle(test)
    assert "ResNet50" in e_smoke["architektur"]
    assert e_smoke["tracking"].startswith("MLflow")
    assert any("DSFA" in c for c in e_smoke["compliance_pflichten"])
    print("✅ Phase 03 Smoke-Test grün")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Faustregeln 2026

        | Wenn... | Dann... |
        |---|---|
        | Tabular < 1M | Boosting (Phase 02), kein DL |
        | Bild < 50k | Pre-trained ResNet50 / EfficientNet |
        | Bild > 100k | ViT / ConvNeXt |
        | Sequenz | Transformer / Mamba / Hybrid |
        | Audio | Whisper / Voxtral als Foundation |
        | DACH-On-Prem | MLflow 3 selbst gehostet |
        | EU-Cloud | Comet EU oder MLflow auf STACKIT/IONOS |
        | US-Cloud | nur mit AVV + SCC + TIA, bei sensiblen Daten DPIA |

        ## Wichtige Hinweise

        - **PyTorch 2.7** ist 2026-Standard (Blackwell B200-Support, CUDA 12.8).
        - **AdamW** + **Cosine-Schedule mit Warmup** ist 2026 LLM-/CNN-Standard.
        - **bf16** statt fp16 auf modernen GPUs.
        - **PyTorch Lightning 2.6.1** weiterhin valid für Standard-Trainings;
          für LLM-Pretraining → TorchTitan oder Vanilla + DeepSpeed.
        - **MLflow 3** über W&B aus DSGVO-Gründen, sofern man self-hosten kann.
        """
    )
    return


if __name__ == "__main__":
    app.run()
