# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "pydantic>=2.9",
# ]
# ///

"""Pretrain-Kalkulator — Compute, Cost, Zeit für Pretraining-Setups.

Smoke-Test-tauglich. Chinchilla-Formel: FLOPs = 6 × N × D.
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
        # 🧮 Pretrain-Kalkulator · Phase 10

        Schätzt für ein Pretraining-Setup:

        - Compute (Chinchilla: FLOPs ≈ 6 × N × D)
        - GPU-Stunden auf H100/H200
        - EUR-Cost auf EU-Cloud
        - Wall-Clock auf Multi-GPU

        Plus: Zeigt warum 99 % der Use-Cases LoRA-Finetune (Phase 12) brauchen, nicht Pretrain.

        Stand: 29.04.2026.
        """
    )
    return


@app.cell
def _():
    """Pydantic-Schemas."""
    from typing import Literal

    from pydantic import BaseModel, Field

    class PretrainProfil(BaseModel):
        modell_params_b: float = Field(ge=0.1, le=1000)
        tokens_b: float = Field(ge=0.1, le=10_000)
        gpu: Literal["RTX 4090", "H100", "H200"]
        anzahl_gpus: int = Field(ge=1, le=128)
        mfu: float = Field(
            ge=0.1, le=0.7, description="Model FLOPs Utilization, 0.5 ist realistisch"
        )

    class PretrainSchaetzung(BaseModel):
        flops: float
        gpu_stunden: float
        wall_clock_stunden: float
        cost_eur: float
        cost_min_aufschlag_eur: float  # +Restarts/Eval/Tokenizer

    return PretrainProfil, PretrainSchaetzung


@app.cell
def _(PretrainSchaetzung):
    """Kalkulations-Logik (Chinchilla)."""

    gpu_tflops_bf16 = {
        "RTX 4090": 165,  # ohne Tensor-Cores; mit FA2: ~ 330
        "H100": 989,
        "H200": 989,  # gleiche Compute, mehr VRAM
    }

    gpu_pricing_eur_h = {
        "RTX 4090": 0.80,  # nur Strom, eigene Hardware
        "H100": 2.73,  # Scaleway
        "H200": 3.50,  # OVH
    }

    def schaetze(profil: dict) -> PretrainSchaetzung:
        # Chinchilla-Formel
        n = profil["modell_params_b"] * 1e9
        d = profil["tokens_b"] * 1e9
        flops = 6 * n * d  # FLOPs total

        # GPU-TFLOPS effektiv
        tflops = gpu_tflops_bf16[profil["gpu"]] * 1e12 * profil["mfu"]

        # GPU-Stunden total (FLOPs / TFLOPS-pro-Sekunde / 3600s)
        gpu_stunden = flops / (tflops * 3600)

        # Wall-Clock auf Multi-GPU (linear scaling — vereinfacht)
        wall_clock = gpu_stunden / profil["anzahl_gpus"]

        # Cost
        cost = gpu_stunden * gpu_pricing_eur_h[profil["gpu"]]
        # Faktor 2-3 Aufschlag für Eval/Restarts/Tokenizer
        cost_aufschlag = cost * 2.5

        return PretrainSchaetzung(
            flops=flops,
            gpu_stunden=gpu_stunden,
            wall_clock_stunden=wall_clock,
            cost_eur=cost,
            cost_min_aufschlag_eur=cost_aufschlag,
        )

    return (schaetze,)


@app.cell
def _(mo, schaetze):
    """Realitäts-Check über mehrere Modell-Größen."""
    setups = [
        {
            "name": "Mini: GPT-2 124M, 1 GB DE",
            "modell_params_b": 0.124,
            "tokens_b": 0.2,
            "gpu": "RTX 4090",
            "anzahl_gpus": 1,
            "mfu": 0.4,
        },
        {
            "name": "Klein: nanochat 1.5B, 50B Tokens",
            "modell_params_b": 1.5,
            "tokens_b": 50,
            "gpu": "H100",
            "anzahl_gpus": 8,
            "mfu": 0.5,
        },
        {
            "name": "Mid: 7B, 200B Tokens",
            "modell_params_b": 7,
            "tokens_b": 200,
            "gpu": "H100",
            "anzahl_gpus": 64,
            "mfu": 0.5,
        },
        {
            "name": "Groß: 70B, 1T Tokens",
            "modell_params_b": 70,
            "tokens_b": 1000,
            "gpu": "H200",
            "anzahl_gpus": 128,
            "mfu": 0.5,
        },
    ]

    rows = []
    for s in setups:
        e = schaetze(s)
        rows.append(
            f"| {s['name']} | {s['modell_params_b']}B × {s['tokens_b']}B | "
            f"{s['anzahl_gpus']}× {s['gpu']} | "
            f"{e.gpu_stunden:.0f} h | {e.wall_clock_stunden:.0f} h | "
            f"€ {e.cost_eur:.0f} | € {e.cost_min_aufschlag_eur:.0f} |"
        )

    mo.md(
        "## Pretrain-Compute + Cost-Realität\n\n"
        "| Setup | Modell × Tokens | GPUs | GPU-h Total | Wall-Clock | Cost (Theoretisch) | Cost (mit Aufschlag) |\n"
        "|---|---|---|---|---|---|---|\n" + "\n".join(rows)
    )
    return


@app.cell
def _(mo):
    """Wann Pretrain — wann nicht."""
    pretrain_yes = [
        "Forschungs-Projekt mit Custom-Architektur",
        "DACH-Sovereignty (eigenes DE-Foundation-Modell)",
        "Custom-Tokenizer-Anforderung (nicht-Standard-Sprache)",
        "Lehre / Verständnis-Aufbau (124M-Repro reicht)",
    ]
    pretrain_no = [
        "Standard-DACH-Mittelstand-LLM-App → Phase 11 + 13 + LoRA-Finetune (Phase 12)",
        "Spezielle Domäne (Recht, Medizin, Steuer) → RAG (Phase 13) + LoRA (Phase 12)",
        "Tone-of-Voice oder Stil-Anpassung → DPO (Phase 18.04)",
        "Halluzinations-Reduktion → besseres RAG, nicht Pretrain",
    ]

    mo.md(
        "## Wann Pretrain WIRKLICH sinnvoll ist\n\n### ✅ Ja\n\n"
        + "\n".join(f"- {p}" for p in pretrain_yes)
        + "\n\n### ❌ Nein (LoRA / RAG schlägt es bei 99 % der Production-Use-Cases)\n\n"
        + "\n".join(f"- {p}" for p in pretrain_no)
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Compute-Annahmen

        - **Chinchilla-Formel**: FLOPs ≈ 6 × N_params × D_tokens
        - **MFU 50 %** für H100 BF16 (realistisch — 70 % nur in optimaler Konfiguration)
        - **MFU 40 %** für RTX 4090 (Consumer-Karte, weniger Optimierungs-Spielraum)
        - **Linear-Scaling auf Multi-GPU** ist Vereinfachung — bei > 32 GPUs Communication-Overhead beachten
        - **Aufschlag 2,5×** für Eval-Cycles, Restarts, Tokenizer-Iterationen — realistische Production-Praxis

        ## Wichtige Hinweise

        - **nanoGPT ist deprecated** seit Nov 2025 — nanochat ist Nachfolger
        - **DALL-E 4 / Whisper-v4 / Sesame-Anthropic** existieren nicht — siehe Issue #9 fact-check
        - **EU-GPU-Pricing** stieg Q1 2026 ~ 30 % (DRAM-Knappheit)

        ## Quellen

        - Chinchilla-Paper (Hoffmann et al. 2022) — <https://arxiv.org/abs/2203.15556>
        - Compute-Cost-Guide — <https://introl.com/blog/fine-tuning-infrastructure-lora-qlora-peft-scale-guide-2025>
        - Scaleway H100 — <https://www.scaleway.com/en/h100/>
        - OVHcloud H100 — <https://www.ovhcloud.com/en/public-cloud/gpu/h100/>
        """
    )
    return


if __name__ == "__main__":
    app.run()
