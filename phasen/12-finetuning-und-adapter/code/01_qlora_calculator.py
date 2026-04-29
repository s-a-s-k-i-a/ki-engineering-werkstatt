# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "pydantic>=2.9",
# ]
# ///

"""QLoRA-Calculator — VRAM, Trainings-Zeit, EUR-Kosten für Finetune-Setups.

Smoke-Test-tauglich: keine externen API-Calls. Heuristiken aus Lektion 12.05
plus EU-GPU-Pricing Stand 29.04.2026 (Scaleway H100 € 2,73/h, RTX 4090
€ 0,80/h Strom).
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
        # 🧮 QLoRA-Calculator · Phase 12

        Dieses Notebook berechnet **VRAM-Bedarf, Trainings-Zeit und EUR-Kosten**
        für QLoRA-Setups — basierend auf:

        - Modell-Größe (7B / 14B / 32B / 70B)
        - LoRA-Rank
        - Datensatz-Größe + Sequenz-Länge + Epochen
        - GPU-Wahl (RTX 4090, H100, H200)

        Pricing-Stand: 29.04.2026 (Scaleway H100 € 2,73/h verifiziert in
        Phase 17.04). Volatil — vor Produktiv-Einsatz im Anbieter-Portal
        re-verifizieren.

        Smoke-Test-tauglich (keine API-Calls).
        """
    )
    return


@app.cell
def _():
    """Pydantic-Modelle: Modell-Profil, Trainings-Setup, Schätzung."""
    from typing import Literal

    from pydantic import BaseModel, Field

    class ModellProfil(BaseModel):
        name: str
        params_b: float
        hidden_dim: int
        n_layers: int
        ist_moe: bool = False
        active_params_b: float | None = None

    class GPU(BaseModel):
        name: str
        vram_gb: int
        eur_pro_stunde: float
        compute_relativ: float
        anbieter: Literal["lokal", "scaleway", "ovh", "stackit"]

    class TrainingsSetup(BaseModel):
        modell: str
        rank: int = Field(ge=4, le=256)
        target_modules: int = Field(ge=2, le=7, description="Anzahl Linear-Module mit LoRA")
        samples: int = Field(ge=100, le=1_000_000)
        seq_len: int = Field(ge=512, le=32_768)
        epochs: int = Field(ge=1, le=10)
        batch_size_eff: int = Field(ge=1, le=128)
        gpu: str

    class Schaetzung(BaseModel):
        vram_basis_gb: float
        vram_adapter_mb: float
        vram_optimizer_gb: float
        vram_activations_gb: float
        vram_total_gb: float
        passt_in_gpu: bool
        warnungen: list[str]
        trainings_zeit_h: float
        eur_kosten: float

    return GPU, ModellProfil, Schaetzung, TrainingsSetup


@app.cell
def _(GPU, ModellProfil):
    """Modell- und GPU-Kataloge."""
    modelle = {
        "Qwen3-7B": ModellProfil(
            name="Qwen3-7B-Instruct", params_b=7.6, hidden_dim=4096, n_layers=28
        ),
        "Llama-3.3-8B": ModellProfil(
            name="Llama-3.3-8B-Instruct", params_b=8.0, hidden_dim=4096, n_layers=32
        ),
        "Mistral-Nemo-12B": ModellProfil(
            name="Mistral-Nemo-12B-Instruct", params_b=12.2, hidden_dim=5120, n_layers=40
        ),
        "Qwen3-14B": ModellProfil(
            name="Qwen3-14B-Instruct", params_b=14.7, hidden_dim=5120, n_layers=48
        ),
        "Qwen3-32B": ModellProfil(
            name="Qwen3-32B-Instruct", params_b=32.5, hidden_dim=5120, n_layers=64
        ),
        "Llama-3.3-70B": ModellProfil(
            name="Llama-3.3-70B-Instruct", params_b=70.6, hidden_dim=8192, n_layers=80
        ),
        "Llama-3.3-405B": ModellProfil(
            name="Llama-3.3-405B-Instruct", params_b=405.0, hidden_dim=16384, n_layers=126
        ),
    }

    gpus = {
        "RTX 4090": GPU(
            name="RTX 4090 (lokal)",
            vram_gb=24,
            eur_pro_stunde=0.80,  # nur Strom, eigene Hardware
            compute_relativ=1.0,
            anbieter="lokal",
        ),
        "RTX 5090": GPU(
            name="RTX 5090 (lokal)",
            vram_gb=32,
            eur_pro_stunde=1.20,
            compute_relativ=1.4,
            anbieter="lokal",
        ),
        "H100 80GB (Scaleway)": GPU(
            name="H100 80GB",
            vram_gb=80,
            eur_pro_stunde=2.73,
            compute_relativ=2.5,
            anbieter="scaleway",
        ),
        "H200 141GB (OVH)": GPU(
            name="H200 141GB",
            vram_gb=141,
            eur_pro_stunde=3.50,
            compute_relativ=3.0,
            anbieter="ovh",
        ),
    }
    return gpus, modelle


@app.cell
def _(Schaetzung, gpus, modelle):
    """Schätzungs-Logik."""

    def schaetze(setup: dict) -> Schaetzung:
        warnungen = []
        m = modelle[setup["modell"]]
        g = gpus[setup["gpu"]]

        # 1. VRAM Basis-Modell (4-bit-quantisiert)
        vram_basis_gb = m.params_b * 0.5  # ~ 0.5 GB pro Mrd. Params bei 4-bit

        # 2. LoRA-Adapter (FP16)
        # Pro Layer: rank × (hidden_dim + hidden_dim) × 2 Bytes (FP16)
        # × n_layers × n_target_modules
        adapter_params = setup["rank"] * 2 * m.hidden_dim * m.n_layers * setup["target_modules"]
        vram_adapter_mb = (adapter_params * 2) / 1e6  # FP16 = 2 Bytes

        # 3. Optimizer (AdamW 8-bit) — 4 Bytes pro trainable Param
        vram_optimizer_gb = (adapter_params * 4) / 1e9

        # 4. Activations (sequence-length-abhängig, batch-abhängig)
        # Heuristik: ~ batch × seq_len × hidden_dim × n_layers × 4 Bytes / 1e9
        vram_activations_gb = (
            setup["batch_size_eff"] * setup["seq_len"] * m.hidden_dim * m.n_layers * 4 / 1e9
        ) * 0.05  # gradient_checkpointing reduziert ~ 95 %

        vram_total = (
            vram_basis_gb + vram_adapter_mb / 1024 + vram_optimizer_gb + vram_activations_gb
        )

        passt = vram_total <= g.vram_gb * 0.92

        if not passt:
            warnungen.append(
                f"VRAM-Bedarf ({vram_total:.1f} GB) überschreitet GPU-Größe "
                f"({g.vram_gb} GB) — kleinere Batch-Size, niedrigerer Rank, "
                f"oder größere GPU nötig."
            )

        # Trainings-Zeit (heuristisch)
        # Basis: 7B QLoRA auf RTX 4090, 5k samples × 1 epoch = 1 h
        baseline_h = 1.0
        steps_relativ = (
            setup["samples"]
            * setup["epochs"]
            / max(setup["batch_size_eff"], 1)
            / 5_000  # 5k samples × 1 epoch baseline
        )
        modell_skala = m.params_b / 7.0  # linear in Modell-Größe
        seq_skala = setup["seq_len"] / 2048  # längere Sequenzen kosten

        trainings_zeit_h = baseline_h * steps_relativ * modell_skala * seq_skala / g.compute_relativ

        # EUR-Kosten
        eur_kosten = trainings_zeit_h * g.eur_pro_stunde

        if trainings_zeit_h > 100:
            warnungen.append(
                f"Trainings-Zeit ({trainings_zeit_h:.0f} h) sehr lang — "
                f"Multi-GPU-Setup oder kleineres Modell erwägen."
            )

        return Schaetzung(
            vram_basis_gb=vram_basis_gb,
            vram_adapter_mb=vram_adapter_mb,
            vram_optimizer_gb=vram_optimizer_gb,
            vram_activations_gb=vram_activations_gb,
            vram_total_gb=vram_total,
            passt_in_gpu=passt,
            warnungen=warnungen,
            trainings_zeit_h=trainings_zeit_h,
            eur_kosten=eur_kosten,
        )

    return (schaetze,)


@app.cell
def _(mo, schaetze):
    """Drei Beispiel-Setups."""
    setups = [
        {
            "name": "Klein: 7B QLoRA, RTX 4090",
            "modell": "Qwen3-7B",
            "rank": 16,
            "target_modules": 7,
            "samples": 5_000,
            "seq_len": 2048,
            "epochs": 3,
            "batch_size_eff": 16,
            "gpu": "RTX 4090",
        },
        {
            "name": "Mittel: 14B QLoRA, H100",
            "modell": "Qwen3-14B",
            "rank": 16,
            "target_modules": 7,
            "samples": 20_000,
            "seq_len": 2048,
            "epochs": 3,
            "batch_size_eff": 16,
            "gpu": "H100 80GB (Scaleway)",
        },
        {
            "name": "Groß: 70B QLoRA, H200",
            "modell": "Llama-3.3-70B",
            "rank": 32,
            "target_modules": 7,
            "samples": 50_000,
            "seq_len": 4096,
            "epochs": 3,
            "batch_size_eff": 16,
            "gpu": "H200 141GB (OVH)",
        },
    ]

    rows = []
    for s in setups:
        r = schaetze(s)
        warn_text = " · ".join(r.warnungen)[:60] if r.warnungen else "—"
        rows.append(
            f"| {s['name']} | {r.vram_total_gb:.1f} GB | "
            f"{'✅' if r.passt_in_gpu else '⚠️'} | "
            f"{r.trainings_zeit_h:.1f} h | € {r.eur_kosten:.0f} | "
            f"{warn_text} |"
        )

    mo.md(
        "## Drei Beispiel-Setups\n\n"
        "| Setup | VRAM | Passt? | Trainings-Zeit | EUR-Kosten | Warnungen |\n"
        "|---|---|---|---|---|---|\n" + "\n".join(rows)
    )
    return (setups,)


@app.cell
def _(gpus, mo, modelle):
    """Modell- und GPU-Katalog anzeigen."""
    modell_rows = []
    for k, v in modelle.items():
        modell_rows.append(f"| {k} | {v.params_b} | {v.hidden_dim} | {v.n_layers} |")

    gpu_rows = []
    for k, v in gpus.items():
        gpu_rows.append(
            f"| **{k}** | {v.vram_gb} GB | € {v.eur_pro_stunde:.2f}/h | "
            f"{v.compute_relativ}× | {v.anbieter} |"
        )

    mo.md(
        "## Modell-Katalog\n\n"
        "| Modell | Params (Mrd.) | Hidden-Dim | Layers |\n"
        "|---|---|---|---|\n" + "\n".join(modell_rows) + "\n\n## GPU-Katalog (Stand 29.04.2026)\n\n"
        "| GPU | VRAM | Stundenpreis | Compute-Faktor | Anbieter |\n"
        "|---|---|---|---|---|\n" + "\n".join(gpu_rows)
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Wie du das nutzt

        1. Pass `setups` mit deinen Werten an
        2. Schau auf VRAM, Zeit und EUR-Kosten
        3. Bei nicht-passendem VRAM: Rank reduzieren, Batch-Size kleiner, oder größere GPU
        4. Vor Produktiv-Einsatz Pricing im Anbieter-Portal re-verifizieren

        ## Annahmen + Limitierungen

        - VRAM-Schätzung: ± 15 % je nach FlashAttention-Version
        - Trainings-Zeit: Heuristik aus 7B+RTX 4090-Baseline; bei MoE-Modellen anders
        - EUR-Kosten: ohne Datentransfer, ohne Storage, ohne Setup-Overhead

        ## Compliance-Anker

        - **AI-Act Art. 10 (Daten-Governance)**: Datensatz-Hash committed
        - **AI-Act Art. 12 (Logging)**: Trainings-Manifest mit Hyperparametern
        - **DSGVO Art. 25**: lokales Training (RTX 4090) = kein Drittland-Transfer

        ## Quellen

        - LoRA-Paper — <https://arxiv.org/abs/2106.09685>
        - QLoRA-Paper — <https://arxiv.org/abs/2305.14314>
        - Scaleway H100-Pricing (verifiziert 29.04.2026) — <https://www.scaleway.com/en/h100/>
        - OVHcloud H200 — <https://www.ovhcloud.com/en/public-cloud/gpu/h200/>
        - Unsloth Speedup-Benchmarks — <https://github.com/unslothai/unsloth>
        """
    )
    return


if __name__ == "__main__":
    app.run()
