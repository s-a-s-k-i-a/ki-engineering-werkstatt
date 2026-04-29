# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "pydantic>=2.9",
# ]
# ///

"""VLM-Selektor — wählt VLM basierend auf Use-Case + Hardware + Compliance.

Smoke-Test-tauglich: keine externen Calls. Modell-Daten Stand 29.04.2026.
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
        # 👁️ VLM-Selektor · Phase 04

        Wählt das passende Vision-Language-Modell basierend auf:

        - Hardware-Profil (Edge / Mid-Range-GPU / Server)
        - Use-Case (OCR / Allgemein / Edge / Multi-Modal RAG)
        - Compliance (DSGVO-strict / Standard)

        Stand: 29.04.2026. Smoke-Test-tauglich.
        """
    )
    return


@app.cell
def _():
    """Pydantic-Schemas."""
    from typing import Literal

    from pydantic import BaseModel

    class VLM(BaseModel):
        name: str
        params_b: float
        lizenz: Literal["apache-2.0", "mit", "gemma", "meta"]
        plattform: Literal["edge", "mid-range", "server", "browser"]
        spezialitaet: Literal["allgemein", "ocr", "edge", "multi-modal-embedding"]
        deutsch_qualitaet: Literal["sehr-gut", "gut", "mittel"]
        vram_q4_gb: float | None = None

    class Profil(BaseModel):
        hardware: Literal["smartphone", "rtx-4090", "h100", "cluster"]
        use_case: Literal["ocr", "allgemein", "edge", "multi-modal-embedding"]
        compliance: Literal["dsgvo-strict", "standard"]
        deutsch_pflicht: bool = True

    return Profil, VLM


@app.cell
def _(VLM):
    """VLM-Katalog Stand 29.04.2026."""
    katalog = [
        VLM(
            name="Qwen3-VL-32B-Instruct",
            params_b=32,
            lizenz="apache-2.0",
            plattform="mid-range",
            spezialitaet="allgemein",
            deutsch_qualitaet="sehr-gut",
            vram_q4_gb=20,
        ),
        VLM(
            name="Qwen3-VL-8B-Instruct",
            params_b=8,
            lizenz="apache-2.0",
            plattform="mid-range",
            spezialitaet="allgemein",
            deutsch_qualitaet="sehr-gut",
            vram_q4_gb=5,
        ),
        VLM(
            name="Qwen3-VL-235B-A22B (MoE)",
            params_b=235,
            lizenz="apache-2.0",
            plattform="server",
            spezialitaet="allgemein",
            deutsch_qualitaet="sehr-gut",
        ),
        VLM(
            name="LightOnOCR-2-1B",
            params_b=1,
            lizenz="apache-2.0",
            plattform="mid-range",
            spezialitaet="ocr",
            deutsch_qualitaet="sehr-gut",
            vram_q4_gb=2,
        ),
        VLM(
            name="MiniCPM-o 2.6",
            params_b=8,
            lizenz="apache-2.0",
            plattform="edge",
            spezialitaet="edge",
            deutsch_qualitaet="gut",
            vram_q4_gb=5,
        ),
        VLM(
            name="MiniCPM-V 4.0",
            params_b=4.1,
            lizenz="apache-2.0",
            plattform="edge",
            spezialitaet="edge",
            deutsch_qualitaet="gut",
            vram_q4_gb=3,
        ),
        VLM(
            name="SmolVLM2-2.2B",
            params_b=2.2,
            lizenz="apache-2.0",
            plattform="browser",
            spezialitaet="edge",
            deutsch_qualitaet="mittel",
            vram_q4_gb=1.5,
        ),
        VLM(
            name="InternVL3.5-8B",
            params_b=8,
            lizenz="mit",
            plattform="mid-range",
            spezialitaet="allgemein",
            deutsch_qualitaet="gut",
            vram_q4_gb=5,
        ),
        VLM(
            name="PaliGemma 2-10B",
            params_b=10,
            lizenz="gemma",
            plattform="mid-range",
            spezialitaet="allgemein",
            deutsch_qualitaet="gut",
            vram_q4_gb=6,
        ),
        VLM(
            name="jina-clip-v2",
            params_b=0.5,
            lizenz="apache-2.0",
            plattform="mid-range",
            spezialitaet="multi-modal-embedding",
            deutsch_qualitaet="sehr-gut",
            vram_q4_gb=1,
        ),
    ]
    return (katalog,)


@app.cell
def _(katalog):
    """Empfehlungs-Logik."""

    hardware_to_plattform = {
        "smartphone": ["edge", "browser"],
        "rtx-4090": ["mid-range", "edge", "browser"],
        "h100": ["server", "mid-range", "edge"],
        "cluster": ["server"],
    }

    def empfehle(profil: dict) -> list[str]:
        plattformen = hardware_to_plattform[profil["hardware"]]
        kandidaten = [
            m
            for m in katalog
            if m.plattform in plattformen and m.spezialitaet == profil["use_case"]
        ]
        if profil["deutsch_pflicht"]:
            kandidaten = [m for m in kandidaten if m.deutsch_qualitaet in ("gut", "sehr-gut")]
        if profil["compliance"] == "dsgvo-strict":
            # Nur Apache 2.0 + MIT für absolute Lizenz-Sicherheit
            kandidaten = [m for m in kandidaten if m.lizenz in ("apache-2.0", "mit")]

        return [m.name for m in kandidaten[:3]]

    return (empfehle,)


@app.cell
def _(empfehle, mo):
    """Test-Profile."""
    profile = [
        {
            "name": "Mandanten-Smartphone-OCR",
            "hardware": "smartphone",
            "use_case": "edge",
            "compliance": "dsgvo-strict",
            "deutsch_pflicht": True,
        },
        {
            "name": "Rechnungs-OCR auf RTX 4090",
            "hardware": "rtx-4090",
            "use_case": "ocr",
            "compliance": "dsgvo-strict",
            "deutsch_pflicht": True,
        },
        {
            "name": "Server-Dokument-Analyse",
            "hardware": "h100",
            "use_case": "allgemein",
            "compliance": "standard",
            "deutsch_pflicht": True,
        },
        {
            "name": "Multi-Modal RAG",
            "hardware": "rtx-4090",
            "use_case": "multi-modal-embedding",
            "compliance": "dsgvo-strict",
            "deutsch_pflicht": True,
        },
    ]

    rows_profile = []
    for p in profile:
        empf = empfehle(p)
        empf_text = ", ".join(empf) if empf else "—"
        rows_profile.append(
            f"| {p['name']} | {p['hardware']} | {p['use_case']} | {p['compliance']} | {empf_text} |"
        )

    mo.md(
        "## Profil-Empfehlungen\n\n"
        "| Profil | Hardware | Use-Case | Compliance | Top-3-Modelle |\n"
        "|---|---|---|---|---|\n" + "\n".join(rows_profile)
    )
    return


@app.cell
def _(katalog, mo):
    """Modell-Katalog."""
    rows_kat = []
    for m in katalog:
        vram = f"{m.vram_q4_gb} GB" if m.vram_q4_gb else "Cluster"
        rows_kat.append(
            f"| **{m.name}** | {m.params_b}B | {m.lizenz} | "
            f"{m.plattform} | {m.spezialitaet} | {m.deutsch_qualitaet} | {vram} |"
        )

    mo.md(
        "## VLM-Katalog (Stand 29.04.2026)\n\n"
        "| Modell | Params | Lizenz | Plattform | Speziell | DE | VRAM Q4 |\n"
        "|---|---|---|---|---|---|---|\n" + "\n".join(rows_kat)
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Compliance-Anker

        - **AI-Act Art. 5**: Untargeted Face-Scraping verboten — Use-Case prüfen
        - **DSGVO Art. 9**: biometrische Daten = besondere Kategorie
        - **DSGVO Art. 25**: on-device-Edge-VLM für PII-haltige Bilder
        - **Lizenz-Disziplin**: Apache 2.0 / MIT für volle kommerzielle Freiheit

        ## Quellen

        - Qwen3-VL — <https://github.com/QwenLM/Qwen3-VL>
        - LightOnOCR-2-1B — <https://huggingface.co/lightonai/LightOnOCR-1B-1025>
        - MiniCPM-o 2.6 — <https://github.com/OpenBMB/MiniCPM-o>
        - SigLIP-2 — <https://huggingface.co/blog/siglip2>
        - jina-clip-v2 — <https://jina.ai/models/jina-clip-v2/>
        - AI-Act Art. 5 — <https://artificialintelligenceact.eu/article/5/>
        """
    )
    return


if __name__ == "__main__":
    app.run()
