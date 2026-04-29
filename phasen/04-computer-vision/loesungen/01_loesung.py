# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "pydantic>=2.9",
# ]
# ///

"""Lösungs-Skelett — Übung 04.01 — VLM-Selektor + KUG-Compliance.

Smoke-test-tauglich. Kein VLM-Inference, reine Pydantic-Logik.
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
        # 🎯 Lösung Übung 04.01 — VLM-Selektor + KUG-Compliance

        Drei DACH-Vision-Use-Cases → VLM + Inference-Stack + KUG-Pflichten.
        """
    )
    return


@app.cell
def _():
    """Pydantic-Profil-Schema."""
    from pydantic import BaseModel, Field

    class VisionProfil(BaseModel):
        name: str
        task: str
        latenz_ms: int = Field(ge=10)
        hosting: str  # "edge", "eu_cloud", "on_prem"
        personen_im_bild: bool
        volumen_pro_tag: int = Field(ge=1)

    return (VisionProfil,)


@app.cell
def _():
    """Empfehlungs-Logik."""

    def empfehle_vlm(p) -> dict:
        if p.hosting == "edge" and p.latenz_ms < 1000:
            return {
                "modell": "MiniCPM-o-2.6 oder SmolVLM2 (Edge)",
                "grund": "läuft auf Tablet/Phone, < 6 GB VRAM",
            }
        if p.task == "ocr":
            return {"modell": "LightOnOCR-2-1B", "grund": "OCR-Spezialist, klein + schnell"}
        if p.task == "image_search":
            return {
                "modell": "SigLIP-2 oder jina-clip-v2",
                "grund": "starke Embeddings für Image-Search",
            }
        if p.task == "multimodal_chat":
            return {
                "modell": "Qwen3-VL-32B (Apache 2.0)",
                "grund": "Open-VLM-Spitze für Multimodal-Chat",
            }
        return {"modell": "Qwen3-VL-7B", "grund": "guter Default für mittlere VLM-Aufgaben"}

    def inference_stack(p) -> str:
        if p.hosting == "edge":
            return "llama.cpp / MLX (Apple) / Ollama"
        return "vLLM V1 oder SGLang (EU-Cloud)"

    def kug_compliance(p) -> list[str]:
        pflichten = []
        if p.personen_im_bild:
            pflichten.append("KUG Art. 22 — Einwilligung der abgebildeten Personen")
            pflichten.append("Auto-Lösch-Pipeline für Roh-Bilder (DSGVO Art. 5)")
            pflichten.append("Gesichts-Pseudonymisierung vor Speicherung (Art. 25)")
            pflichten.append("DSGVO Art. 9 (biometrisch) → DSFA falls Identifizierung")
            pflichten.append(
                "AI-Act Anhang III Nr. 1 prüfen (biometrische Identifizierung = Hochrisiko)"
            )
        pflichten.append("EXIF-Strip vor Upload (GPS / Device-ID = PII)")
        return pflichten

    def avv_liste(p) -> list[str]:
        if p.hosting == "edge":
            return ["Kein AVV nötig — kein Datentransfer"]
        if p.hosting == "on_prem":
            return ["Kein AVV nötig — eigene Infrastruktur"]
        return [
            "IONOS AI Model Hub (DE, BSI C5)",
            "OVHcloud (FR, SecNumCloud)",
            "Scaleway (FR, HDS für Health)",
            "STACKIT (DE, BSI C5 Type 2)",
        ]

    return avv_liste, empfehle_vlm, inference_stack, kug_compliance


@app.cell
def _(VisionProfil):
    """Drei Use-Cases."""
    profile = [
        VisionProfil(
            name="Werkstatt-Schadenshilfe",
            task="multimodal_chat",
            latenz_ms=800,
            hosting="edge",
            personen_im_bild=False,
            volumen_pro_tag=200,
        ),
        VisionProfil(
            name="Behörden-OCR (Bauamt)",
            task="ocr",
            latenz_ms=2000,
            hosting="eu_cloud",
            personen_im_bild=True,  # Briefe enthalten Bürger:innen-Daten
            volumen_pro_tag=5_000,
        ),
        VisionProfil(
            name="Tierheim-Foto-Galerie",
            task="image_search",
            latenz_ms=1500,
            hosting="eu_cloud",
            personen_im_bild=True,  # Pfleger:innen oft mit drauf
            volumen_pro_tag=100,
        ),
    ]
    return (profile,)


@app.cell
def _(avv_liste, empfehle_vlm, inference_stack, kug_compliance, mo, profile):
    """Detail pro Use-Case."""
    blocks = []
    for p in profile:
        v = empfehle_vlm(p)
        s = inference_stack(p)
        kug = kug_compliance(p)
        avvs = avv_liste(p)
        kug_str = "\n".join(f"  - {x}" for x in kug)
        avv_str = "\n".join(f"  - {x}" for x in avvs)
        blocks.append(
            f"### {p.name}\n\n"
            f"- **VLM**: {v['modell']} *({v['grund']})*\n"
            f"- **Inference-Stack**: {s}\n"
            f"- **KUG-/DSGVO-Pflichten**:\n{kug_str}\n"
            f"- **AVV-Optionen**:\n{avv_str}\n"
        )
    mo.md("## Detail pro Use-Case\n\n" + "\n".join(blocks))
    return


@app.cell
def _(avv_liste, empfehle_vlm, kug_compliance, profile):
    """Smoke-Test: 4 Akzeptanz-Asserts."""
    p_werkstatt = profile[0]
    p_ocr = profile[1]
    p_tierheim = profile[2]

    # 1. Werkstatt → Edge-Modell (MiniCPM-o oder SmolVLM2)
    werkstatt_modell = empfehle_vlm(p_werkstatt)["modell"]
    assert "MiniCPM-o" in werkstatt_modell or "SmolVLM2" in werkstatt_modell

    # 2. OCR → LightOnOCR oder Edge-Modell-Fallback
    ocr_modell = empfehle_vlm(p_ocr)["modell"]
    assert "LightOnOCR" in ocr_modell

    # 3. Tierheim mit Personen → KUG-Pflicht
    tierheim_kug = kug_compliance(p_tierheim)
    assert any("KUG" in p for p in tierheim_kug)
    assert any("Pseudonymisierung" in p or "Auto-Lösch" in p for p in tierheim_kug)

    # 4. EU-Cloud-Hosting → AVV-Liste mit IONOS/OVH/Scaleway/STACKIT
    avv_test = avv_liste(p_ocr)
    assert any("IONOS" in a or "OVH" in a or "Scaleway" in a or "STACKIT" in a for a in avv_test)

    print("✅ Übung 04.01 — alle 4 Asserts grün")
    return


if __name__ == "__main__":
    app.run()
