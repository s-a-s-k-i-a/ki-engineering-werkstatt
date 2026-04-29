# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "pydantic>=2.9",
# ]
# ///

"""Lösungs-Skelett — Übung 10.01 — Pretrain-Compute-Kalkulator.

Smoke-test-tauglich. Reine Berechnungs-Logik.
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
        # 🎯 Lösung Übung 10.01 — Pretrain-Compute-Kalkulator

        Drei Foundation-Modell-Vorhaben → Tokens + GPU-Stunden + Strom + Korpus.
        """
    )
    return


@app.cell
def _():
    """Pydantic-Profil-Schema."""
    from pydantic import BaseModel, Field

    class PretrainProfil(BaseModel):
        name: str
        parameter_n_b: float = Field(ge=0.1, le=2_000.0)  # in Milliarden
        gpu_typ: str  # "h100", "h200", "b200"
        n_gpus: int = Field(ge=1, le=10_000)
        tflops_pro_gpu_bf16: float = Field(ge=100, le=10_000)  # theoretisch
        mfu_real: float = Field(ge=0.1, le=0.7)  # Realitäts-Faktor
        release_lizenz: str

    return (PretrainProfil,)


@app.cell
def _():
    """Berechnungs-Funktionen."""

    gpu_watt = {"h100": 700, "h200": 1_000, "b200": 1_200}

    def chinchilla_tokens_b(parameter_n_b: float) -> float:
        """Chinchilla-optimal: ~20× Parameter."""
        return parameter_n_b * 20

    def total_flops(parameter_n_b: float, tokens_b: float) -> float:
        """6 × N × D (in FLOPs)."""
        return 6 * parameter_n_b * 1e9 * tokens_b * 1e9

    def gpu_tage(p, total_flops_val):
        """Wall-Clock in GPU-Tagen."""
        flops_pro_sek = p.tflops_pro_gpu_bf16 * 1e12 * p.mfu_real
        flops_pro_tag = flops_pro_sek * 86400
        gpu_tage_total = total_flops_val / flops_pro_tag
        return gpu_tage_total

    def wall_clock_tage(p, total_flops_val):
        return gpu_tage(p, total_flops_val) / p.n_gpus

    def strom_kwh(p, wall_clock_tage_val):
        watt_pro_gpu = gpu_watt.get(p.gpu_typ, 700)
        kw_total = p.n_gpus * watt_pro_gpu / 1000
        kwh = kw_total * wall_clock_tage_val * 24 * 1.3  # PUE 1.3
        return kwh

    def korpus_empfehlung(p) -> dict:
        if p.parameter_n_b < 3:
            korpora = [
                "Wikitext-DE (CC-BY-SA)",
                "10kGNAD (CC-BY-NC, nur Forschung)",
                "GermEval (gemischt, je Subkorpus prüfen)",
            ]
        elif p.parameter_n_b < 30:
            korpora = [
                "Aleph-Alpha-GermanWeb (für Forschung)",
                "Common Crawl DE (gefiltert)",
                "Curlicat DE-AT (politische Texte, frei)",
            ]
        else:
            korpora = [
                "Aleph-Alpha-GermanWeb",
                "Common Crawl DE/EN (Multi-Snapshot)",
                "C4 / RedPajama / FineWeb-Edu",
                "Code: TheStack v2",
            ]
        return {
            "korpora": korpora,
            "lizenz_check": "Apache 2.0-Release verlangt freie Korpora ohne NC-Klauseln",
        }

    return (
        chinchilla_tokens_b,
        gpu_tage,
        korpus_empfehlung,
        strom_kwh,
        total_flops,
        wall_clock_tage,
    )


@app.cell
def _(PretrainProfil):
    """Drei Use-Cases."""
    profile = [
        PretrainProfil(
            name="1B-Hochschul-Forschung",
            parameter_n_b=1.0,
            gpu_typ="h100",
            n_gpus=1,
            tflops_pro_gpu_bf16=989,  # H100 SXM5 BF16
            mfu_real=0.45,
            release_lizenz="Apache 2.0",
        ),
        PretrainProfil(
            name="7B-DACH-Domain-LLM",
            parameter_n_b=7.0,
            gpu_typ="h100",
            n_gpus=8,
            tflops_pro_gpu_bf16=989,
            mfu_real=0.50,
            release_lizenz="Apache 2.0",
        ),
        PretrainProfil(
            name="70B-Sovereign-AI",
            parameter_n_b=70.0,
            gpu_typ="h200",
            n_gpus=256,
            tflops_pro_gpu_bf16=989,  # ~ wie H100 für BF16
            mfu_real=0.45,
            release_lizenz="Custom (Sovereign)",
        ),
    ]
    return (profile,)


@app.cell
def _(
    chinchilla_tokens_b,
    korpus_empfehlung,
    mo,
    profile,
    strom_kwh,
    total_flops,
    wall_clock_tage,
):
    """Detail pro Use-Case."""
    blocks = []
    for p in profile:
        tokens_b = chinchilla_tokens_b(p.parameter_n_b)
        flops = total_flops(p.parameter_n_b, tokens_b)
        wall = wall_clock_tage(p, flops)
        kwh = strom_kwh(p, wall)
        eur = kwh * 0.30  # Industrie-Tarif DE
        korpus = korpus_empfehlung(p)
        korpus_str = "\n".join(f"  - {k}" for k in korpus["korpora"])
        blocks.append(
            f"### {p.name} ({p.parameter_n_b}B Parameter)\n\n"
            f"- **Chinchilla-Tokens**: {tokens_b:.0f} Mrd.\n"
            f"- **Gesamt-FLOPs**: {flops:.2e} ({flops / 1e21:.2f} ZFLOPs)\n"
            f"- **Wall-Clock**: {wall:.1f} Tage auf {p.n_gpus} × {p.gpu_typ.upper()} (MFU {p.mfu_real * 100:.0f} %)\n"
            f"- **Strom**: {kwh:.0f} kWh × 0,30 € = **{eur:.0f} €** (PUE 1.3 inkl.)\n"
            f"- **Lizenz-Check**: {korpus['lizenz_check']}\n"
            f"- **Korpus-Empfehlung**:\n{korpus_str}\n"
        )
    mo.md("## Detail pro Use-Case\n\n" + "\n".join(blocks))
    return


@app.cell
def _(chinchilla_tokens_b, profile, total_flops, wall_clock_tage):
    """Smoke-Test: 5 Akzeptanz-Asserts."""
    p1 = profile[0]
    p70 = profile[2]

    # 1. Chinchilla-Verhältnis: 20:1
    assert chinchilla_tokens_b(1.0) == 20.0
    assert chinchilla_tokens_b(70.0) == 1_400.0

    # 2. FLOPs-Größenordnung: 1B-Modell mit 20B Tokens ≈ 1.2e20 FLOPs
    flops_1b = total_flops(1.0, 20.0)
    assert 1e20 < flops_1b < 2e20, f"FLOPs für 1B/20B: {flops_1b}"

    # 3. 70B-Modell hat > 10²⁵ FLOPs nicht zwingend (klassisch ~ 5e23)
    flops_70b = total_flops(70.0, 1_400.0)
    assert 4e23 < flops_70b < 9e23, f"FLOPs für 70B/1.4T: {flops_70b}"

    # 4. Wall-Clock 1B auf Single-H100 mehrere Tage
    wall_1b = wall_clock_tage(p1, flops_1b)
    assert 1 < wall_1b < 30, f"1B-Wall-Clock: {wall_1b}"

    # 5. Wall-Clock 70B auf 256 H200 plausibel: 30-90 Tage
    wall_70b = wall_clock_tage(p70, flops_70b)
    assert 30 < wall_70b < 200, f"70B-Wall-Clock: {wall_70b}"

    print("✅ Übung 10.01 — alle 5 Asserts grün")
    return


if __name__ == "__main__":
    app.run()
